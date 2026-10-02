"""Gateway shutdown closes the HTTP client, then clears the session."""

import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from edge_gateway.crypto.secure_transport import SecureTransport, SecureTransportError
from edge_gateway.crypto.session import SecureSession, SessionState
from edge_gateway.dispatch import CloudDispatch

DOCUMENT = Path(__file__).parents[1] / "docs" / "secure-shutdown.md"
README = Path(__file__).parents[1] / "README.md"


class _Opener:
    def __init__(self, events: list[str]) -> None:
        self.events = events

    def close(self) -> None:
        self.events.append("http")

    def open(self, *_args: object, **_kwargs: object) -> object:
        raise AssertionError("HTTP client opened")


class _Sessions:
    def __init__(self, events: list[str]) -> None:
        self.events = events
        self.handshakes = 0
        moment = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)
        self.current = SecureSession(
            session_id="sess-shutdown",
            gateway_id="gateway-001",
            cloud_key_id="key-1",
            created_at=moment,
            expires_at=moment,
            session_key=bytearray(bytes.fromhex("ab" * 32)),
            state=SessionState.ACTIVE,
        )

    async def get_or_establish(self) -> SecureSession:
        self.handshakes += 1
        return self.current

    def invalidate(self, session_id: str | None = None) -> None:
        return None

    def close(self) -> None:
        assert self.events[-1] == "http"
        self.current.clear(SessionState.CLOSED)
        self.events.append("session")


class _Baseline:
    def __init__(self) -> None:
        self.calls = 0

    async def send(self, **_kwargs: object) -> dict[str, str]:
        self.calls += 1
        return {"status": "accepted"}


def _transport(sessions: _Sessions) -> SecureTransport:
    transport = SecureTransport(
        sessions,
        cloud_url="http://cloud-service:9000",
        timeout_seconds=1,
        max_retries=0,
    )
    transport._opener = _Opener(sessions.events)
    return transport


def _measurement() -> dict[str, object]:
    return {
        "request_id": "req-shutdown",
        "device_id": "sensor-001",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "measured_at": "2026-09-30T12:00:00Z",
        "sequence_number": 1,
        "received_at": "2026-09-30T12:00:01Z",
    }


def test_shutdown_closes_the_client_before_clearing_the_session(caplog: pytest.LogCaptureFixture) -> None:
    events: list[str] = []
    sessions = _Sessions(events)
    transport = _transport(sessions)
    key_hex = bytes(sessions.current.session_key).hex()

    with caplog.at_level(logging.DEBUG):
        transport.shutdown()
        transport.shutdown()

    assert events == ["http", "session"]
    assert transport._opener is None
    assert sessions.current.state is SessionState.CLOSED
    assert bytes(sessions.current.session_key) == b"\x00" * 32
    assert key_hex not in caplog.text


def test_shutdown_send_fails_closed_without_a_new_handshake() -> None:
    sessions = _Sessions([])
    transport = _transport(sessions)
    transport.shutdown()

    with pytest.raises(SecureTransportError) as caught:
        asyncio.run(transport.send(**_measurement()))  # type: ignore[arg-type]

    assert caught.value.retryable is False
    assert sessions.handshakes == 0


def test_dispatch_after_shutdown_does_not_call_baseline() -> None:
    sessions = _Sessions([])
    transport = _transport(sessions)
    transport.shutdown()
    baseline = _Baseline()
    dispatch = CloudDispatch(
        load_config({"SECURITY_MODE": "mlkem", "GATEWAY_ID": "gateway-001"}),
        baseline=baseline,  # type: ignore[arg-type]
        secure=transport,
    )

    with pytest.raises(SecureTransportError):
        asyncio.run(dispatch.send(**_measurement()))  # type: ignore[arg-type]

    assert baseline.calls == 0
    assert dispatch.metrics.secure_failures_total == 1
    assert dispatch.pqc_metrics.pqc_fallback_total == 0


def test_lifespan_runs_security_cleanup_after_stopping_work() -> None:
    app = create_app(load_config({}))
    calls: list[bool] = []

    class _Attached:
        def shutdown(self) -> None:
            calls.append(app.state.running is False)

    app.state.secure_transport = _Attached()
    with TestClient(app):
        assert app.state.running
    assert calls == [True]
    assert not app.state.running


def test_secure_shutdown_document_records_the_order_and_the_limitation() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert document.index("Close the HTTP client and drop it.") < document.index(
        "Clear the active session reference."
    )
    assert "Shutdown does not log key material." in document
    assert "Python does not guarantee secure memory zeroization." in document
    assert "M3-56 lists the HTTP client close after the session is cleared." in document
    assert "docs/secure-shutdown.md" in readme
    assert "does not print key material" in readme
