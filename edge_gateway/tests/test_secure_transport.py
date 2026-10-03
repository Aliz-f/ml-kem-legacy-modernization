"""Secure measurement transport, retries, and one session recovery."""

from __future__ import annotations

import asyncio
import json
import logging
import socket
import struct
from typing import TypeAlias
import threading
from collections.abc import Callable
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from edge_gateway.metrics import GatewayMetrics

from edge_gateway.crypto.encoding import decode_binary
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.secure_transport import SecureAcceptance, SecureTransport, SecureTransportError
from edge_gateway.crypto.session import SecureSession, SessionEstablishmentError, SessionState
from edge_gateway.crypto.symmetric import NONCE_LENGTH


def _session(session_id: str) -> SecureSession:
    moment = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)
    return SecureSession(
        session_id=session_id,
        gateway_id="gateway-001",
        cloud_key_id="key-1",
        created_at=moment,
        expires_at=moment,
        session_key=bytearray(range(32)),
        state=SessionState.ACTIVE,
    )


class _Sessions:
    def __init__(self, failure: SessionEstablishmentError | None = None, *, fail_on_call: int = 1) -> None:
        self.failure = failure
        self.fail_on_call = fail_on_call
        self.calls = 0
        self.invalidated = 0
        self.invalidated_ids: list[str | None] = []
        self._ids = ["sess-1", "sess-2"]
        self.current: SecureSession | None = _session(self._ids.pop(0))

    async def get_or_establish(self) -> SecureSession:
        self.calls += 1
        if self.failure is not None and self.calls == self.fail_on_call:
            raise self.failure
        if self.current is None:
            self.current = _session(self._ids.pop(0))
        return self.current

    def invalidate(self, session_id: str | None = None) -> None:
        self.invalidated += 1
        self.invalidated_ids.append(session_id)
        if self.current is not None:
            self.current.clear(SessionState.EXPIRED)
            self.current = None


_ResponsePayload: TypeAlias = dict[str, object] | None


class _Cloud:
    def __init__(self) -> None:
        self.responses: list[tuple[int, _ResponsePayload]] = [(202, {"status": "accepted", "record_id": "rec-1"})]
        self.requests: list[tuple[str, bytes, str | None]] = []
        self.redirect_to: str | None = None
        self.delay_seconds = 0.0
        self.reset_next = 0


def _reset_mid_body(handler: BaseHTTPRequestHandler, status: int) -> None:
    """Send headers and a partial body, then abort the connection with RST."""
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", "100")
    handler.end_headers()
    handler.wfile.write(b'{"sta')
    handler.connection.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    handler.connection.close()
    handler.close_connection = True


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        cloud: _Cloud = self.server.cloud  # type: ignore[attr-defined]
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        cloud.requests.append((self.path, body, self.headers.get("X-Request-ID")))
        if cloud.delay_seconds:
            import time

            time.sleep(cloud.delay_seconds)
        if cloud.redirect_to is not None:
            self.send_response(302)
            self.send_header("Location", cloud.redirect_to)
            self.end_headers()
            return
        if cloud.reset_next:
            # Simulate a connection reset while the Cloud response is read.
            cloud.reset_next -= 1
            _reset_mid_body(self, 202)
            return
        status, payload = cloud.responses.pop(0)
        if payload is None:
            # Simulate the Cloud persisting the request but losing its response.
            # The declared byte is intentionally never written before close.
            self.send_response(status)
            self.send_header("Content-Length", "1")
            self.end_headers()
            self.close_connection = True
            return
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def cloud():
    script = _Cloud()
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    server.cloud = script  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}", script
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


def _send(transport: SecureTransport, **overrides: object) -> SecureAcceptance:
    fields: dict[str, object] = {
        "request_id": "req-8fb2",
        "device_id": "sensor-plaintext-marker",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z",
        "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218Z",
    }
    fields.update(overrides)
    return asyncio.run(transport.send(**fields))  # type: ignore[arg-type]


def _transport(
    url: str,
    sessions: _Sessions,
    *,
    max_retries: int = 2,
    timeout_seconds: float = 1,
    sleep: Callable[[float], None] | None = None,
) -> SecureTransport:
    return SecureTransport(
        sessions,
        cloud_url=url,
        timeout_seconds=timeout_seconds,
        max_retries=max_retries,
        **({"sleep": sleep} if sleep is not None else {}),
    )


def _error(code: str) -> dict[str, object]:
    return {"error": {"code": code, "message": "failed"}}


def test_send_posts_one_envelope_and_reuses_the_session(cloud):
    url, script = cloud
    script.responses = [
        (202, {"status": "accepted", "record_id": "rec-1"}),
        (202, {"status": "accepted", "record_id": "rec-1"}),
    ]
    sessions = _Sessions()
    first = _send(_transport(url, sessions))
    second = _send(_transport(url, sessions))
    assert first == SecureAcceptance(status="accepted", record_id="rec-1")
    assert second.status == "accepted"
    assert sessions.calls == 2
    assert sessions.invalidated == 0
    assert [path for path, _, _ in script.requests] == [
        "/api/v1/secure/measurements",
        "/api/v1/secure/measurements",
    ]
    posted = [json.loads(body) for _, body, _ in script.requests]
    assert {item["session_id"] for item in posted} == {"sess-1"}
    assert {item["request_id"] for item in posted} == {"req-8fb2"}
    assert all(len(decode_binary(item["nonce"])) == NONCE_LENGTH for item in posted)
    assert posted[0]["nonce"] != posted[1]["nonce"]
    assert "sensor-plaintext-marker" not in script.requests[0][1].decode()
    assert script.requests[0][2] == "req-8fb2"


def test_transport_retry_resends_the_same_envelope(cloud, caplog):
    url, script = cloud
    script.responses = [
        (503, _error("STORAGE_UNAVAILABLE")),
        (504, _error("SERVICE_UNAVAILABLE")),
        (202, {"status": "already_accepted", "record_id": "rec-existing"}),
    ]
    delays: list[float] = []
    with caplog.at_level(logging.WARNING, logger="edge_gateway"):
        result = _send(_transport(url, _Sessions(), max_retries=2, sleep=delays.append))
    assert result.status == "already_accepted"
    bodies = [body for _, body, _ in script.requests]
    assert len(bodies) == 3
    assert bodies[0] == bodies[1] == bodies[2]
    assert delays == [1.0, 2.0]
    assert "event=cloud_delivery_retry component=edge_gateway request_id=req-8fb2 gateway_id=gateway-001 security_mode=mlkem attempt=2 reason=transport" in caplog.text
    assert "attempt=3" in caplog.text


def test_lost_response_retries_the_same_envelope(cloud):
    url, script = cloud
    script.responses = [
        (202, None),
        (202, {"status": "already_accepted", "record_id": "rec-existing"}),
    ]
    delays: list[float] = []
    result = _send(_transport(url, _Sessions(), max_retries=1, sleep=delays.append))
    assert result == SecureAcceptance(status="already_accepted", record_id="rec-existing")
    bodies = [body for _, body, _ in script.requests]
    assert bodies[0] == bodies[1]
    assert delays == [1.0]


def test_session_conflict_rebuilds_once_with_the_same_request_id(cloud):
    url, script = cloud
    script.responses = [
        (409, _error("SESSION_INVALID")),
        (202, {"status": "accepted", "record_id": "rec-2"}),
    ]
    sessions = _Sessions()
    result = _send(_transport(url, sessions, max_retries=2))
    assert result.record_id == "rec-2"
    assert sessions.invalidated == 1
    assert sessions.invalidated_ids == ["sess-1"]
    posted = [json.loads(body) for _, body, _ in script.requests]
    assert [item["session_id"] for item in posted] == ["sess-1", "sess-2"]
    assert [item["request_id"] for item in posted] == ["req-8fb2", "req-8fb2"]
    assert posted[0]["nonce"] != posted[1]["nonce"]
    assert len(script.requests) == 2


def test_a_second_session_conflict_is_not_recovered_again(cloud):
    url, script = cloud
    script.responses = [
        (409, _error("SESSION_EXPIRED")),
        (409, _error("SESSION_EXPIRED")),
    ]
    with pytest.raises(SecureTransportError) as caught:
        _send(_transport(url, _Sessions(), max_retries=2))
    assert caught.value.retryable is False
    assert caught.value.code == "SESSION_EXPIRED"
    assert len(script.requests) == 2


def test_application_rejection_is_not_retried(cloud):
    url, script = cloud
    script.responses = [
        (400, _error("SECURE_MESSAGE_REJECTED")),
        (202, {"status": "accepted", "record_id": "rec-ignored"}),
    ]
    with pytest.raises(SecureTransportError) as caught:
        _send(_transport(url, _Sessions(), max_retries=2))
    assert caught.value.retryable is False
    assert caught.value.code == "SECURE_MESSAGE_REJECTED"
    assert len(script.requests) == 1


def test_exhausted_transport_retries_stay_retryable(cloud):
    url, script = cloud
    script.responses = [(503, _error("STORAGE_UNAVAILABLE"))] * 3
    delays: list[float] = []
    with pytest.raises(SecureTransportError) as caught:
        _send(_transport(url, _Sessions(), max_retries=2, sleep=delays.append))
    assert caught.value.retryable is True
    assert len(script.requests) == 3
    assert delays == [1.0, 2.0]


def test_invalid_measurement_and_session_failure_do_not_post(cloud):
    url, script = cloud
    sessions = _Sessions(SessionEstablishmentError("unavailable", retryable=True))
    with pytest.raises(SecureTransportError) as caught:
        _send(_transport(url, sessions))
    assert caught.value.retryable is True
    assert script.requests == []
    ready = _Sessions()
    with pytest.raises(SecureTransportError) as rejected:
        _send(_transport(url, ready), measured_at="yesterday")
    assert rejected.value.retryable is False
    assert script.requests == []


def test_redirect_and_non_accepted_success_are_not_retried(cloud):
    url, script = cloud
    script.redirect_to = url + "/elsewhere"
    with pytest.raises(SecureTransportError) as redirected:
        _send(_transport(url, _Sessions(), max_retries=2))
    assert redirected.value.retryable is False
    script.redirect_to = None
    script.responses = [(200, {"status": "accepted", "record_id": "rec-1"})]
    with pytest.raises(SecureTransportError) as other:
        _send(_transport(url, _Sessions(), max_retries=2))
    assert other.value.retryable is False
    assert len(script.requests) == 2


def test_timeout_is_retryable_without_a_second_session(cloud):
    url, script = cloud
    script.delay_seconds = 0.3
    sessions = _Sessions()
    with pytest.raises(SecureTransportError) as caught:
        _send(_transport(url, sessions, max_retries=0, timeout_seconds=0.05))
    assert caught.value.retryable is True
    assert sessions.invalidated == 0
    assert len(script.requests) == 1


def test_connection_reset_while_reading_retries_the_same_envelope(cloud):
    url, script = cloud
    script.reset_next = 1
    script.responses = [(202, {"status": "already_accepted", "record_id": "rec-existing"})]
    delays: list[float] = []
    result = _send(_transport(url, _Sessions(), max_retries=2, sleep=delays.append))
    assert result.status == "already_accepted"
    bodies = [body for _, body, _ in script.requests]
    assert len(bodies) == 2
    assert bodies[0] == bodies[1]
    assert delays == [1.0]


def test_exhausted_connection_resets_fail_closed_as_retryable(cloud):
    url, script = cloud
    script.reset_next = 2
    with pytest.raises(SecureTransportError) as caught:
        _send(_transport(url, _Sessions(), max_retries=1, sleep=lambda _: None))
    assert caught.value.retryable is True
    assert len(script.requests) == 2


def test_shutdown_during_retry_fails_closed_without_another_post(cloud):
    url, script = cloud
    script.responses = [(503, _error("SERVICE_UNAVAILABLE"))]
    sessions = _Sessions()
    transport = _transport(url, sessions, max_retries=2, sleep=lambda _: transport.shutdown())
    with pytest.raises(SecureTransportError) as caught:
        _send(transport)
    assert caught.value.retryable is False
    assert len(script.requests) == 1


def test_message_phase_follows_whether_a_handshake_ran(cloud):
    url, script = cloud
    script.responses = [
        (202, {"status": "accepted", "record_id": "rec-1"}),
        (202, {"status": "accepted", "record_id": "rec-2"}),
    ]

    class _CountingSessions(_Sessions):
        def __init__(self) -> None:
            super().__init__()
            self.metrics = PqcMetrics()

        async def get_or_establish(self) -> SecureSession:
            if self.current is None:
                self.metrics.record_handshake_success(0.0, 0.0, 0.0)
            return await super().get_or_establish()

    sessions = _CountingSessions()
    # The held session expired locally; the gauge still reads active until
    # the next open replaces it with a new handshake.
    sessions.current = None
    sessions.metrics.set_active_session(True)
    transport = _transport(url, sessions)
    _send(transport)
    _send(transport)
    assert sessions.metrics.message_duration["first"].count == 1
    assert sessions.metrics.message_duration["steady"].count == 1


def test_keys_and_plaintext_are_not_logged(cloud, caplog: pytest.LogCaptureFixture):
    url, script = cloud
    script.responses = [(422, _error("INVALID_MEASUREMENT"))]
    key = bytes(range(32))
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(SecureTransportError):
            _send(_transport(url, _Sessions(), max_retries=0))
    rendered = caplog.text.encode()
    assert key not in rendered
    assert b"sensor-plaintext-marker" not in rendered


def test_retry_count_must_be_a_non_negative_integer():
    with pytest.raises(ValueError):
        SecureTransport(_Sessions(), cloud_url="http://127.0.0.1", timeout_seconds=1, max_retries=-1)
    with pytest.raises(ValueError):
        SecureTransport(_Sessions(), cloud_url="http://127.0.0.1", timeout_seconds=1, max_retries=True)  # type: ignore[arg-type]


@pytest.mark.parametrize("responses, attempts, failures, retries", [
    ([(202, {"status": "accepted", "record_id": "rec-1"})], 1, 0, 0),
    ([(503, {}), (202, {"status": "accepted", "record_id": "rec-1"})], 2, 1, 1),
    ([(409, {"error": {"code": "SESSION_EXPIRED"}}),
      (202, {"status": "accepted", "record_id": "rec-1"})], 2, 1, 0),
    ([(503, {})] * 3, 3, 3, 2),
    ([(422, {})], 1, 1, 0),
    ([(202, {})], 1, 1, 0),
])
def test_application_attempt_metrics_preserve_retry_and_recovery_semantics(
    cloud, responses, attempts, failures, retries,
):
    url, script = cloud
    script.responses = responses.copy()
    transport = _transport(url, _Sessions(), sleep=lambda _: None)
    if failures == attempts:
        with pytest.raises(SecureTransportError):
            _send(transport)
    else:
        _send(transport)
    text = transport.application_metrics.render()
    for name, value in {"cloud_requests": attempts, "cloud_failures": failures,
                        "cloud_retries": retries}.items():
        assert f"gateway_{name}_total {value}\n" in text
    assert f"gateway_cloud_request_duration_seconds_count {attempts}\n" in text
    assert len(script.requests) == attempts


def test_handshake_failure_does_not_count_a_measurement_http_attempt():
    registry = GatewayMetrics()
    sessions = _Sessions(SessionEstablishmentError("unavailable", retryable=False))
    transport = SecureTransport(sessions, cloud_url="http://cloud.invalid", timeout_seconds=1,
                                max_retries=2, application_metrics=registry)
    with pytest.raises(SecureTransportError):
        _send(transport)
    assert "gateway_cloud_requests_total 0\n" in registry.render()
    assert "gateway_cloud_failures_total 0\n" in registry.render()


def test_gateway_exports_secure_attempt_metrics_from_shared_registry(cloud):
    from fastapi.testclient import TestClient
    from edge_gateway.app import create_app
    from edge_gateway.config import load_config

    url, _ = cloud
    transport = _transport(url, _Sessions())
    app = create_app(load_config({"SECURITY_MODE": "mlkem"}), secure_transport=transport,
                     application_metrics=transport.application_metrics,
                     pqc_metrics=transport.metrics)
    with TestClient(app) as client:
        assert client.post("/api/v1/measurements", json={
            "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
            "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 1,
        }).status_code == 202
        text = client.get("/metrics").text
        assert "gateway_cloud_requests_total 1\n" in text
        assert "gateway_cloud_failures_total 0\n" in text
