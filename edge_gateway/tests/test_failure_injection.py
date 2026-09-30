"""Crypto failure injection for handshake, ciphertext, and session state."""

from __future__ import annotations

import asyncio
import json
import logging
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from edge_gateway.config import load_config
from edge_gateway.crypto.aad import build_aad
from edge_gateway.crypto.encoding import decode_binary, encode_binary
from edge_gateway.crypto.failure import CryptoFailureInjector
from edge_gateway.crypto.plaintext import serialize_canonical_measurement
from edge_gateway.crypto.kdf import derive_session_key
from edge_gateway.crypto.secure_transport import SecureTransport, SecureTransportError
from edge_gateway.crypto.session import SecureSession, SessionEstablishmentError, SessionManager, SessionState
from edge_gateway.crypto.symmetric import AeadError, decrypt
from edge_gateway.dispatch import CloudDispatch


def _injector(mode: str, rate: float = 1.0, seed: str | None = "seed-1") -> CryptoFailureInjector:
    return CryptoFailureInjector(mode, rate, seed)


def test_disabled_modes_never_select_a_crypto_fault():
    quiet = _injector("none", 1.0)
    other = _injector("processing_error", 1.0)
    stopped = _injector("mlkem_handshake_failure", 0.0)
    for injector in (quiet, other, stopped):
        assert injector.handshake_failure() is False
        assert injector.corrupt_ciphertext() is False
        assert injector.session_missing() is False
        assert injector.session_expired() is False


def test_rate_one_selects_only_the_configured_mode():
    injector = _injector("corrupt_ciphertext")
    assert injector.corrupt_ciphertext() is True
    assert injector.handshake_failure() is False
    assert injector.session_missing() is False


def test_same_seed_makes_the_same_decisions():
    left = CryptoFailureInjector("session_expired", 0.5, "same-seed")
    right = CryptoFailureInjector("session_expired", 0.5, "same-seed")
    decisions = [left.session_expired() for _ in range(24)]
    assert decisions == [right.session_expired() for _ in range(24)]
    assert len(set(decisions)) == 2


def test_enabled_warning_names_the_mode_and_not_the_seed(caplog: pytest.LogCaptureFixture):
    with caplog.at_level(logging.WARNING):
        CryptoFailureInjector("mlkem_handshake_failure", 1.0, "super-secret-seed")
    assert "event=failure_injection_enabled" in caplog.text
    assert "mode=mlkem_handshake_failure" in caplog.text
    assert "super-secret-seed" not in caplog.text


def test_from_config_uses_gateway_failure_settings():
    config = load_config({"FAILURE_MODE": "session_missing", "FAILURE_RATE": "1", "FAILURE_SEED": "abc"})
    injector = CryptoFailureInjector.from_config(config)
    assert injector.session_missing() is True
    assert injector.corrupt_ciphertext() is False


def test_injected_handshake_failure_leaves_no_session_and_skips_baseline():
    config = load_config(
        {
            "SECURITY_MODE": "mlkem",
            "FAILURE_MODE": "mlkem_handshake_failure",
            "FAILURE_RATE": "1",
        }
    )
    manager = SessionManager(
        "gateway-001",
        "http://127.0.0.1:9",
        0.2,
        injector=CryptoFailureInjector.from_config(config),
    )
    transport = SecureTransport(
        manager,
        cloud_url="http://127.0.0.1:9",
        timeout_seconds=0.2,
        max_retries=0,
    )

    class _Baseline:
        def __init__(self) -> None:
            self.calls: list[object] = []

        async def send(self, **kwargs: object) -> dict[str, str]:
            self.calls.append(kwargs)
            return {"status": "accepted"}

    baseline = _Baseline()
    dispatch = CloudDispatch(config, baseline=baseline, secure=transport)

    async def _send() -> None:
        await dispatch.send(
            request_id="req-8fb2",
            device_id="sensor-001",
            temperature_c=21.7,
            humidity_pct=42.5,
            measured_at="2026-09-21T13:45:31Z",
            sequence_number=184,
            received_at="2026-09-21T13:45:31.218Z",
        )

    with pytest.raises(SecureTransportError) as caught:
        asyncio.run(_send())
    assert caught.value.retryable is False
    assert baseline.calls == []
    assert manager.metrics.mlkem_handshake_failures_total == 1
    assert manager._session is None


class _Clock:
    def __init__(self) -> None:
        self.now = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self.now


class _HandshakeCloud:
    def __init__(self, clock: _Clock) -> None:
        self.clock = clock
        self.private_key = MLKEM768PrivateKey.generate()
        self.posts = 0

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
        self.private_key.decapsulate(ciphertext)
        derive_session_key(self.private_key.decapsulate(ciphertext))
        return json.dumps(
            {
                "protocol_version": "1",
                "session_id": f"sess-{self.posts}",
                "status": "established",
                "expires_at": (self.clock.now + timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
            }
        ).encode()


class _HandshakeHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        cloud: _HandshakeCloud = self.server.cloud  # type: ignore[attr-defined]
        body = cloud.public_body()
        self._send(200, body)

    def do_POST(self) -> None:  # noqa: N802
        cloud: _HandshakeCloud = self.server.cloud  # type: ignore[attr-defined]
        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length))
        self._send(200, cloud.session_body(request))

    def _send(self, status: int, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def handshake_url():
    clock = _Clock()
    cloud = _HandshakeCloud(clock)
    server = ThreadingHTTPServer(("127.0.0.1", 0), _HandshakeHandler)
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


def test_session_missing_and_expired_force_a_new_handshake(handshake_url):
    url, cloud, clock = handshake_url

    async def _run(mode: str, ended: SessionState) -> None:
        manager = SessionManager(
            "gateway-001",
            url,
            1,
            clock=clock,
            injector=_injector(mode),
        )
        first = await manager.get_or_establish()
        held_key = bytes(first.session_key)
        second = await manager.get_or_establish()
        assert cloud.posts == 2
        assert first.state is ended
        assert bytes(first.session_key) == b"\x00" * len(held_key)
        assert second.session_id == "sess-2"
        assert second.state is SessionState.ACTIVE
        cloud.posts = 0

    asyncio.run(_run("session_missing", SessionState.FAILED))
    asyncio.run(_run("session_expired", SessionState.EXPIRED))


def test_disabled_injection_reuses_one_handshake(handshake_url):
    url, cloud, clock = handshake_url
    manager = SessionManager("gateway-001", url, 1, clock=clock, injector=_injector("none", 1.0))

    async def _run() -> None:
        first = await manager.get_or_establish()
        second = await manager.get_or_establish()
        assert first.session_id == second.session_id
        assert cloud.posts == 1

    asyncio.run(_run())


class _MeasurementCloud:
    def __init__(self) -> None:
        self.bodies: list[bytes] = []


class _MeasurementHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        cloud: _MeasurementCloud = self.server.cloud  # type: ignore[attr-defined]
        length = int(self.headers.get("Content-Length", "0"))
        cloud.bodies.append(self.rfile.read(length))
        body = json.dumps({"status": "accepted", "record_id": "rec-1"}).encode()
        self.send_response(202)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def measurement_url():
    cloud = _MeasurementCloud()
    server = ThreadingHTTPServer(("127.0.0.1", 0), _MeasurementHandler)
    server.cloud = cloud  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}", cloud
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


class _Sessions:
    def __init__(self) -> None:
        moment = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)
        self.session = SecureSession(
            session_id="sess-1",
            gateway_id="gateway-001",
            cloud_key_id="key-1",
            created_at=moment,
            expires_at=moment,
            session_key=bytearray(range(32)),
            state=SessionState.ACTIVE,
        )

    async def get_or_establish(self) -> SecureSession:
        return self.session

    def invalidate(self) -> None:
        return None


def test_corrupt_ciphertext_mutates_only_the_outgoing_copy(measurement_url):
    url, cloud = measurement_url
    sessions = _Sessions()
    original_key = bytes(sessions.session.session_key)
    transport = SecureTransport(
        sessions,
        cloud_url=url,
        timeout_seconds=1,
        max_retries=0,
        injector=_injector("corrupt_ciphertext"),
    )

    async def _send() -> None:
        await transport.send(
            request_id="req-8fb2",
            device_id="sensor-001",
            temperature_c=21.7,
            humidity_pct=42.5,
            measured_at="2026-09-21T13:45:31Z",
            sequence_number=184,
            received_at="2026-09-21T13:45:31.218Z",
        )

    asyncio.run(_send())
    posted = json.loads(cloud.bodies[0])
    nonce = decode_binary(posted["nonce"])
    ciphertext = bytearray(decode_binary(posted["ciphertext"]))
    plaintext = _plaintext()
    aad = _aad()
    with pytest.raises(AeadError):
        decrypt(original_key, nonce, bytes(ciphertext), aad)
    ciphertext[0] ^= 0x01
    assert decrypt(original_key, nonce, bytes(ciphertext), aad) == plaintext
    assert bytes(sessions.session.session_key) == original_key


def test_disabled_ciphertext_injection_still_authenticates(measurement_url):
    url, cloud = measurement_url
    sessions = _Sessions()
    transport = SecureTransport(
        sessions,
        cloud_url=url,
        timeout_seconds=1,
        max_retries=0,
        injector=_injector("none", 1.0),
    )

    async def _send() -> None:
        await transport.send(
            request_id="req-8fb2",
            device_id="sensor-001",
            temperature_c=21.7,
            humidity_pct=42.5,
            measured_at="2026-09-21T13:45:31Z",
            sequence_number=184,
            received_at="2026-09-21T13:45:31.218Z",
        )

    asyncio.run(_send())
    posted = json.loads(cloud.bodies[0])
    assert (
        decrypt(
            bytes(sessions.session.session_key),
            decode_binary(posted["nonce"]),
            decode_binary(posted["ciphertext"]),
            _aad(),
        )
        == _plaintext()
    )


def _plaintext() -> bytes:
    return serialize_canonical_measurement(
        device_id="sensor-001",
        temperature_c=21.7,
        humidity_pct=42.5,
        measured_at="2026-09-21T13:45:31Z",
        sequence_number=184,
        received_at="2026-09-21T13:45:31.218Z",
        gateway_id="gateway-001",
    )


def _aad() -> bytes:
    return build_aad(
        protocol_version="1",
        gateway_id="gateway-001",
        session_id="sess-1",
        request_id="req-8fb2",
    )


def test_invalid_failure_rate_is_rejected():
    with pytest.raises(ValueError):
        CryptoFailureInjector("none", 1.5)
    with pytest.raises(SessionEstablishmentError):
        asyncio.run(
            SessionManager(
                "gateway-001",
                "http://127.0.0.1:9",
                0.2,
                injector=_injector("mlkem_handshake_failure"),
            ).get_or_establish()
        )
