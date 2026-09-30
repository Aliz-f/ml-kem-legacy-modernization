"""Fail-closed selection between baseline and secure transport."""

from __future__ import annotations

import asyncio
import json
import logging
import threading
from dataclasses import replace
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from edge_gateway.config import GatewayConfig, load_config
from edge_gateway.crypto.secure_transport import SecureAcceptance, SecureTransport, SecureTransportError
from edge_gateway.crypto.session import SecureSession, SessionEstablishmentError, SessionState
from edge_gateway.dispatch import CloudDispatch


class _Baseline:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    async def send(self, **kwargs: object) -> dict[str, str]:
        self.calls.append(kwargs)
        return {"status": "accepted"}


class _Secure:
    def __init__(self, result: object | None = None, error: Exception | None = None) -> None:
        self.calls: list[dict[str, object]] = []
        self.result = result or SecureAcceptance(status="accepted", record_id="rec-1")
        self.error = error

    async def send(self, **kwargs: object) -> object:
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.result


class _Sessions:
    def __init__(self, failure: SessionEstablishmentError | None = None) -> None:
        self.failure = failure
        moment = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)
        self.current = SecureSession(
            session_id="sess-1",
            gateway_id="gateway-001",
            cloud_key_id="key-1",
            created_at=moment,
            expires_at=moment,
            session_key=bytearray(range(32)),
            state=SessionState.ACTIVE,
        )

    async def get_or_establish(self) -> SecureSession:
        if self.failure is not None:
            raise self.failure
        return self.current

    def invalidate(self) -> None:
        return None


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        server = self.server
        length = int(self.headers.get("Content-Length", "0"))
        server.paths.append(self.path)  # type: ignore[attr-defined]
        self.rfile.read(length)
        body = json.dumps(
            {"error": {"code": "SECURE_MESSAGE_REJECTED", "message": "rejected"}}
        ).encode("utf-8")
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def cloud():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    server.paths = []  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}", server.paths
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


def _config(mode: str) -> GatewayConfig:
    return load_config({"SECURITY_MODE": mode, "GATEWAY_ID": "gateway-001"})


def _measurement() -> dict[str, object]:
    return {
        "request_id": "req-8fb2",
        "device_id": "sensor-plaintext-marker",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z",
        "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218Z",
    }


def _secure(url: str, sessions: _Sessions) -> SecureTransport:
    return SecureTransport(sessions, cloud_url=url, timeout_seconds=1, max_retries=0)


def test_classical_mode_uses_only_the_baseline_transport():
    baseline = _Baseline()
    secure = _Secure()
    dispatch = CloudDispatch(_config("classical"), baseline=baseline, secure=secure)  # type: ignore[arg-type]
    result = asyncio.run(dispatch.send(**_measurement()))  # type: ignore[arg-type]
    assert result == {"status": "accepted"}
    assert len(baseline.calls) == 1
    assert baseline.calls[0]["gateway_id"] == "gateway-001"
    assert baseline.calls[0]["request_id"] == "req-8fb2"
    assert secure.calls == []


def test_mlkem_mode_uses_only_the_secure_transport():
    baseline = _Baseline()
    secure = _Secure()
    dispatch = CloudDispatch(_config("mlkem"), baseline=baseline, secure=secure)  # type: ignore[arg-type]
    result = asyncio.run(dispatch.send(**_measurement()))  # type: ignore[arg-type]
    assert result == SecureAcceptance(status="accepted", record_id="rec-1")
    assert len(secure.calls) == 1
    assert "gateway_id" not in secure.calls[0]
    assert baseline.calls == []
    assert dispatch.metrics.secure_failures_total == 0


def test_mlkem_handshake_failure_does_not_call_baseline(cloud):
    url, paths = cloud
    baseline = _Baseline()
    dispatch = CloudDispatch(
        _config("mlkem"),
        baseline=baseline,
        secure=_secure(url, _Sessions(SessionEstablishmentError("handshake failed", retryable=False))),
    )
    with pytest.raises(SecureTransportError) as caught:
        asyncio.run(dispatch.send(**_measurement()))  # type: ignore[arg-type]
    assert caught.value.retryable is False
    assert baseline.calls == []
    assert paths == []
    assert dispatch.metrics.secure_failures_total == 1


def test_encryption_failure_does_not_call_baseline(cloud):
    url, paths = cloud
    baseline = _Baseline()
    dispatch = CloudDispatch(_config("mlkem"), baseline=baseline, secure=_secure(url, _Sessions()))
    fields = _measurement()
    fields["measured_at"] = "yesterday"
    with pytest.raises(SecureTransportError) as caught:
        asyncio.run(dispatch.send(**fields))  # type: ignore[arg-type]
    assert caught.value.retryable is False
    assert baseline.calls == []
    assert paths == []
    assert dispatch.metrics.secure_failures_total == 1


def test_secure_rejection_does_not_call_baseline(cloud):
    url, paths = cloud
    baseline = _Baseline()
    dispatch = CloudDispatch(_config("mlkem"), baseline=baseline, secure=_secure(url, _Sessions()))
    with pytest.raises(SecureTransportError):
        asyncio.run(dispatch.send(**_measurement()))  # type: ignore[arg-type]
    assert baseline.calls == []
    assert paths == ["/api/v1/secure/measurements"]
    assert dispatch.metrics.secure_failures_total == 1


def test_mlkem_requires_secure_transport_and_fail_closed_policy():
    with pytest.raises(ValueError):
        CloudDispatch(_config("mlkem"), baseline=_Baseline())
    opened = replace(load_config({"SECURITY_MODE": "mlkem"}), pqc_failure_policy="fallback")
    with pytest.raises(ValueError):
        CloudDispatch(opened, baseline=_Baseline(), secure=_Secure())  # type: ignore[arg-type]


def test_secure_transport_has_no_baseline_fallback():
    import edge_gateway.crypto.secure_transport as transport

    text = Path(transport.__file__).read_text(encoding="utf-8")
    assert "BaselineTransport" not in text
    assert "baseline/measurements" not in text
    assert "explicit_classical_fallback" not in text


def test_failure_log_omits_the_measurement(caplog: pytest.LogCaptureFixture):
    secure = _Secure(error=SecureTransportError("rejected", retryable=False, code="SECURE_MESSAGE_REJECTED"))
    dispatch = CloudDispatch(_config("mlkem"), baseline=_Baseline(), secure=secure)  # type: ignore[arg-type]
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(SecureTransportError):
            asyncio.run(dispatch.send(**_measurement()))  # type: ignore[arg-type]
    assert "sensor-plaintext-marker" not in caplog.text
    assert "req-8fb2" not in caplog.text
    assert dispatch.metrics.secure_failures_total == 1
