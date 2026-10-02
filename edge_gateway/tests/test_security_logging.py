"""Secret-safe security logs and bounded PQC metrics."""

from __future__ import annotations

import asyncio
import json
import logging
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat
from fastapi.testclient import TestClient

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from edge_gateway.crypto.encoding import decode_binary, encode_binary
from edge_gateway.crypto.failure import CryptoFailureInjector
from edge_gateway.crypto.kdf import derive_session_key
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.security_log import log_security
from edge_gateway.crypto.secure_transport import SecureTransport, SecureTransportError
from edge_gateway.crypto.session import SecureSession, SessionManager, SessionState
from edge_gateway.crypto.symmetric import encrypt, generate_nonce
from edge_gateway.dispatch import CloudDispatch


def test_rendered_metrics_keep_bounded_labels_and_zero_fallback():
    rendered = PqcMetrics().render()
    for name in (
        "gateway_mlkem_handshakes_total",
        "gateway_mlkem_handshake_failures_total",
        "gateway_mlkem_handshake_duration_seconds",
        "gateway_mlkem_public_key_duration_seconds",
        "gateway_mlkem_encapsulation_duration_seconds",
        "gateway_session_reestablishments_total",
        "gateway_active_session",
        "gateway_encryption_failures_total",
        "gateway_pqc_fallback_total 0",
        "gateway_injected_failures_total",
        'gateway_secure_message_duration_seconds_count{phase="first"}',
        'gateway_secure_message_duration_seconds_count{phase="steady"}',
    ):
        assert name in rendered
    for forbidden in ("request_id", "session_id", "device_id", "key_id"):
        assert forbidden not in rendered


def test_unsafe_log_values_are_dropped(caplog: pytest.LogCaptureFixture):
    with caplog.at_level(logging.DEBUG):
        log_security("not_a_security_event", gateway_id="gateway-001")
        log_security(
            "session_created",
            device_id="sensor-001",
            gateway_id="gateway-001",
            sequence_number=184,
            session_id="has space",
            key_id=b"raw-key",
        )
    assert "not_a_security_event" not in caplog.text
    assert "component=edge_gateway" in caplog.text
    assert "device_id=sensor-001" in caplog.text
    assert "gateway_id=gateway-001" in caplog.text
    assert "sequence_number=184" in caplog.text
    assert "session_id=" not in caplog.text
    assert b"raw-key" not in caplog.text.encode()


def test_metrics_endpoint_exposes_the_same_registry():
    metrics = PqcMetrics()
    metrics.record_handshake_failure("transport", 0.01)
    app = create_app(load_config({}), pqc_metrics=metrics)
    with TestClient(app) as client:
        body = client.get("/metrics").text
    assert 'gateway_service_info{security_mode="classical"} 1\n' in body
    assert 'gateway_mlkem_handshake_failures_total{reason="transport"} 1' in body
    assert "gateway_pqc_fallback_total 0" in body
    assert "request_id" not in body


def test_gateway_security_components_share_the_metrics_registry_by_default():
    manager = SessionManager("gateway-001", "http://127.0.0.1:9", 0.2)
    transport = SecureTransport(manager, cloud_url="http://127.0.0.1:9", timeout_seconds=0.2, max_retries=0)
    dispatch = CloudDispatch(
        load_config({"SECURITY_MODE": "mlkem"}),
        baseline=_Baseline(),
        secure=transport,
    )
    app = create_app(load_config({}), pqc_metrics=transport.metrics)

    assert transport.metrics is manager.metrics
    assert dispatch.pqc_metrics is manager.metrics
    assert app.state.pqc_metrics is manager.metrics


class _Clock:
    def __init__(self) -> None:
        self.now = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self.now


class _Cloud:
    def __init__(self, clock: _Clock) -> None:
        self.clock = clock
        self.private_key = MLKEM768PrivateKey.generate()
        self.private_key_bytes = self.private_key.private_bytes(
            Encoding.Raw,
            PrivateFormat.Raw,
            NoEncryption(),
        )
        self.posts = 0
        self.shared_secret = b""
        self.session_key = b""
        self.measurement_status = 202

    def public_body(self) -> bytes:
        public_key = self.private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        return json.dumps(
            {
                "protocol_version": "1",
                "algorithm": "ML-KEM-768",
                "key_id": "cloud-key-001",
                "public_key": encode_binary(public_key),
            }
        ).encode()

    def session_body(self, request: dict[str, str]) -> bytes:
        self.posts += 1
        ciphertext = decode_binary(request["encapsulation_ciphertext"])
        self.shared_secret = self.private_key.decapsulate(ciphertext)
        self.session_key = derive_session_key(self.shared_secret)
        expires_at = (self.clock.now + timedelta(minutes=5)).isoformat().replace("+00:00", "Z")
        return json.dumps(
            {
                "protocol_version": "1",
                "session_id": f"sess-{self.posts}",
                "status": "established",
                "expires_at": expires_at,
            }
        ).encode()


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        cloud: _Cloud = self.server.cloud  # type: ignore[attr-defined]
        self._send(200, cloud.public_body())

    def do_POST(self) -> None:  # noqa: N802
        cloud: _Cloud = self.server.cloud  # type: ignore[attr-defined]
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        if self.path.endswith("/crypto/sessions"):
            self._send(200, cloud.session_body(json.loads(raw)))
            return
        body = json.dumps({"status": "accepted", "record_id": "rec-1"}).encode()
        self._send(cloud.measurement_status, body)

    def _send(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def cloud_url():
    clock = _Clock()
    cloud = _Cloud(clock)
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    server.cloud = cloud  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}", cloud, clock
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


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


def test_handshake_and_delivery_omit_secrets_and_separate_timings(
    cloud_url,
    caplog: pytest.LogCaptureFixture,
):
    url, cloud, clock = cloud_url
    metrics = PqcMetrics()
    manager = SessionManager("gateway-001", url, 1, clock=clock, metrics=metrics)
    transport = SecureTransport(manager, cloud_url=url, timeout_seconds=1, max_retries=0, metrics=metrics)

    async def _send() -> None:
        await transport.send(**_measurement())
        await transport.send(**_measurement())

    with caplog.at_level(logging.DEBUG):
        asyncio.run(_send())
        derive_session_key(cloud.shared_secret)
        encrypt(cloud.session_key, generate_nonce(), b"marker-plaintext", b"aad")

    rendered = caplog.text.encode()
    assert cloud.shared_secret not in rendered
    assert cloud.session_key not in rendered
    assert cloud.private_key_bytes not in rendered
    assert b"sensor-plaintext-marker" not in rendered
    assert "event=mlkem_public_key_received" in caplog.text
    assert "key_id=cloud-key-001" in caplog.text
    assert "event=mlkem_handshake_succeeded" in caplog.text
    assert "event=session_created" in caplog.text
    assert "event=session_reused" in caplog.text
    assert "event=encryption_succeeded" in caplog.text
    assert caplog.text.count("event=secure_delivery_started") == 2
    session = manager._session
    assert session is not None
    assert cloud.session_key.hex() not in repr(session)
    assert metrics.handshakes_succeeded == 1
    assert metrics.handshake_duration.count == 1
    assert metrics.public_key_duration.count == 1
    assert metrics.encapsulation_duration.count == 1
    assert metrics.handshake_duration.total_seconds >= metrics.public_key_duration.total_seconds
    assert metrics.handshake_duration.total_seconds >= metrics.encapsulation_duration.total_seconds
    assert metrics.message_duration["first"].count == 1
    assert metrics.message_duration["steady"].count == 1
    assert metrics.active_session == 1
    assert metrics.pqc_fallback_total == 0
    assert "request_id" not in metrics.render()


def test_seal_failure_is_counted_without_the_session_key(caplog: pytest.LogCaptureFixture):
    moment = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)
    key = bytearray(range(32))

    class _Sessions:
        async def get_or_establish(self) -> SecureSession:
            return SecureSession(
                session_id="sess-1",
                gateway_id="gateway-001",
                cloud_key_id="key-1",
                created_at=moment,
                expires_at=moment,
                session_key=key,
                state=SessionState.ACTIVE,
            )

        def invalidate(self, session_id: str | None = None) -> None:
            return None

    metrics = PqcMetrics()
    transport = SecureTransport(
        _Sessions(),
        cloud_url="http://127.0.0.1:9",
        timeout_seconds=0.2,
        max_retries=0,
        metrics=metrics,
    )
    fields = _measurement()
    fields["measured_at"] = "not-a-timestamp"
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(SecureTransportError) as caught:
            asyncio.run(transport.send(**fields))
    assert caught.value.retryable is False
    assert metrics.encryption_failures_total == 1
    assert bytes(key) not in caplog.text.encode()
    assert "event=encryption_failed" in caplog.text
    assert "reason=seal" in caplog.text
    assert "not-a-timestamp" not in caplog.text


def test_session_recovery_is_counted(caplog: pytest.LogCaptureFixture):
    moment = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)
    metrics = PqcMetrics()
    metrics.set_active_session(True)
    responses = [
        (409, {"error": {"code": "SESSION_EXPIRED", "message": "expired"}}),
        (202, {"status": "accepted", "record_id": "rec-2"}),
    ]

    class _Script:
        def pop(self) -> tuple[int, dict[str, object]]:
            return responses.pop(0)

    script = _Script()

    class _Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            self.rfile.read(length)
            status, payload = script.pop()
            body = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    class _Sessions:
        def __init__(self) -> None:
            self.metrics = metrics

        async def get_or_establish(self) -> SecureSession:
            metrics.set_active_session(True)
            return SecureSession(
                session_id="sess-2",
                gateway_id="gateway-001",
                cloud_key_id="key-1",
                created_at=moment,
                expires_at=moment,
                session_key=bytearray(range(32)),
                state=SessionState.ACTIVE,
            )

        def invalidate(self, session_id: str | None = None) -> None:
            metrics.set_active_session(False)

    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        transport = SecureTransport(
            _Sessions(),
            cloud_url=f"http://{host}:{port}",
            timeout_seconds=1,
            max_retries=0,
            metrics=metrics,
        )
        with caplog.at_level(logging.DEBUG):
            asyncio.run(transport.send(**_measurement()))
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()

    assert metrics.reestablishments["success"] == 1
    assert "event=session_reestablishment_started" in caplog.text
    assert "reason=SESSION_EXPIRED" in caplog.text
    assert "event=session_reestablishment_succeeded" in caplog.text
    assert metrics.message_duration["steady"].count == 1
    assert metrics.pqc_fallback_total == 0


class _Baseline:
    def __init__(self) -> None:
        self.calls: list[object] = []

    async def send(self, **kwargs: object) -> dict[str, str]:
        self.calls.append(kwargs)
        return {"status": "accepted"}


def test_injected_handshake_failure_stays_fail_closed(caplog: pytest.LogCaptureFixture):
    metrics = PqcMetrics()
    manager = SessionManager(
        "gateway-001",
        "http://127.0.0.1:9",
        0.2,
        metrics=metrics,
        injector=CryptoFailureInjector("mlkem_handshake_failure", 1.0, "seed"),
    )
    transport = SecureTransport(
        manager,
        cloud_url="http://127.0.0.1:9",
        timeout_seconds=0.2,
        max_retries=0,
        metrics=metrics,
    )
    baseline = _Baseline()
    dispatch = CloudDispatch(
        load_config({"SECURITY_MODE": "mlkem"}),
        baseline=baseline,
        secure=transport,
        pqc_metrics=metrics,
    )
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(SecureTransportError):
            asyncio.run(dispatch.send(**_measurement()))
    assert baseline.calls == []
    assert metrics.mlkem_handshake_failures_total == 1
    assert metrics.injected_failures["mlkem_handshake_failure"] == 1
    assert metrics.pqc_fallback_total == 0
    assert "event=mlkem_handshake_failed" in caplog.text
    assert "reason=injected" in caplog.text
    assert "event=pqc_fail_closed" in caplog.text
    assert "sensor-plaintext-marker" not in caplog.text
    assert "seed" not in caplog.text
