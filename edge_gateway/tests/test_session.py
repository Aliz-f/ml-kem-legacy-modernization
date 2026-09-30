"""Gateway session establishment for protocol version 1."""

import asyncio
import json
import logging
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from edge_gateway.crypto.encoding import decode_binary, encode_binary
from edge_gateway.crypto.kdf import derive_session_key
from edge_gateway.crypto.mlkem import CIPHERTEXT_LENGTH
from edge_gateway.crypto.session import (
    SessionEstablishmentError,
    SessionManager,
    SessionMetrics,
    SessionState,
)
from edge_gateway.crypto.session_client import SessionRejected, parse_session_response


class _Clock:
    def __init__(self) -> None:
        self.now = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self.now


class _Cloud:
    def __init__(self, clock: _Clock) -> None:
        self.clock = clock
        self.private_key = MLKEM768PrivateKey.generate()
        self.posts = 0
        self.mode = "ok"
        self.session_key = b""
        self.gateway_id = ""
        self.key_id = ""
        self.ciphertext_length = 0

    def public_body(self) -> bytes:
        public_key = self.private_key.public_key().public_bytes(
            encoding=Encoding.Raw,
            format=PublicFormat.Raw,
        )
        return json.dumps(
            {
                "protocol_version": "1",
                "algorithm": "ML-KEM-768",
                "key_id": "cloud-key-001",
                "public_key": encode_binary(public_key),
            }
        ).encode()

    def session_body(self, request: dict[str, str]) -> tuple[int, bytes]:
        self.posts += 1
        self.gateway_id = request["gateway_id"]
        self.key_id = request["key_id"]
        ciphertext = decode_binary(request["encapsulation_ciphertext"])
        self.ciphertext_length = len(ciphertext)
        if self.mode == "reject":
            return 200, json.dumps(
                {
                    "protocol_version": "1",
                    "session_id": "sess-bad",
                    "status": "pending",
                    "expires_at": _stamp(self.clock.now + timedelta(minutes=5)),
                }
            ).encode()
        if self.mode == "unavailable":
            return 503, b"{}"
        shared_secret = self.private_key.decapsulate(ciphertext)
        self.session_key = derive_session_key(shared_secret)
        return 200, json.dumps(
            {
                "protocol_version": "1",
                "session_id": "sess-001",
                "status": "established",
                "expires_at": _stamp(self.clock.now + timedelta(minutes=5)),
            }
        ).encode()


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        cloud: _Cloud = self.server.cloud  # type: ignore[attr-defined]
        if self.path != "/api/v1/crypto/public-key":
            self.send_error(404)
            return
        body = cloud.public_body()
        self._send(200, body)

    def do_POST(self) -> None:  # noqa: N802
        cloud: _Cloud = self.server.cloud  # type: ignore[attr-defined]
        if self.path != "/api/v1/crypto/sessions":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length))
        status, body = cloud.session_body(request)
        self._send(status, body)

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


def _stamp(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _manager(url: str, clock: _Clock) -> SessionManager:
    return SessionManager(
        "gateway-001",
        url,
        timeout_seconds=3,
        clock=clock,
    )


def test_session_response_must_be_in_the_future_and_explicitly_zoned():
    now = datetime(2026, 9, 21, 13, 0, tzinfo=timezone.utc)
    with pytest.raises(SessionRejected):
        parse_session_response(
            {
                "protocol_version": "1",
                "session_id": "sess-001",
                "status": "established",
                "expires_at": "2026-09-21T13:05:00",
            },
            now=now,
        )
    with pytest.raises(SessionRejected):
        parse_session_response(
            {
                "protocol_version": "1",
                "session_id": "sess-001",
                "status": "established",
                "expires_at": "2026-09-21T15:05:00+02:00",
            },
            now=now,
        )
    with pytest.raises(SessionRejected):
        parse_session_response(
            {
                "protocol_version": "1",
                "session_id": "sess-001",
                "status": "established",
                "expires_at": _stamp(now - timedelta(seconds=1)),
            },
            now=now,
        )


def test_establishment_stores_one_active_session_with_matching_key(cloud_url):
    url, cloud, clock = cloud_url
    manager = _manager(url, clock)

    async def both():
        session = await manager.get_or_establish()
        again = await manager.get_or_establish()
        return session, again

    session, again = asyncio.run(both())
    assert session.state is SessionState.ACTIVE
    assert again.session_id == session.session_id == "sess-001"
    assert cloud.posts == 1
    assert cloud.gateway_id == "gateway-001"
    assert cloud.key_id == "cloud-key-001"
    assert cloud.ciphertext_length == CIPHERTEXT_LENGTH
    assert bytes(session.session_key) == cloud.session_key
    assert session.session_key.hex() not in repr(session)


def test_concurrent_callers_share_one_handshake(cloud_url):
    url, cloud, clock = cloud_url
    manager = _manager(url, clock)

    async def both():
        return await asyncio.gather(
            manager.get_or_establish(),
            manager.get_or_establish(),
        )

    first, second = asyncio.run(both())
    assert first.session_id == second.session_id
    assert cloud.posts == 1


def test_expired_session_is_replaced(cloud_url):
    url, cloud, clock = cloud_url
    manager = _manager(url, clock)

    async def replace():
        first = await manager.get_or_establish()
        clock.now = first.expires_at + timedelta(seconds=1)
        second = await manager.get_or_establish()
        return first, second

    first, second = asyncio.run(replace())
    assert cloud.posts == 2
    assert second.session_id == "sess-001"
    assert first.state is SessionState.EXPIRED
    assert bytes(first.session_key) == b"\x00" * len(first.session_key)


def test_rejected_response_does_not_become_active(cloud_url, caplog: pytest.LogCaptureFixture):
    url, cloud, clock = cloud_url
    manager = _manager(url, clock)
    cloud.mode = "reject"

    async def recover():
        with pytest.raises(SessionEstablishmentError) as caught:
            await manager.get_or_establish()
        cloud.mode = "ok"
        return caught, await manager.get_or_establish()

    with caplog.at_level(logging.DEBUG):
        caught, session = asyncio.run(recover())
    assert caught.value.retryable is False
    assert cloud.posts == 2
    assert session.state is SessionState.ACTIVE
    assert session.session_key.hex() not in caplog.text


def test_unavailable_cloud_is_retryable_and_leaves_no_session(cloud_url):
    url, cloud, clock = cloud_url
    manager = _manager(url, clock)
    cloud.mode = "unavailable"

    async def recover():
        with pytest.raises(SessionEstablishmentError) as caught:
            await manager.get_or_establish()
        cloud.mode = "ok"
        await manager.get_or_establish()
        return caught

    caught = asyncio.run(recover())
    assert caught.value.retryable is True
    assert cloud.posts == 2


@pytest.mark.parametrize("failure", ["mlkem", "kdf"])
def test_crypto_failure_is_classified_and_recorded(
    cloud_url,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
):
    url, cloud, clock = cloud_url
    metrics = SessionMetrics()
    manager = SessionManager("gateway-001", url, timeout_seconds=3, clock=clock, metrics=metrics)

    if failure == "mlkem":
        from edge_gateway.crypto.mlkem import MlKemError

        def fail_encapsulation(_public_key: bytes) -> tuple[bytes, bytes]:
            raise MlKemError("injected ML-KEM failure")

        monkeypatch.setattr("edge_gateway.crypto.session.encapsulate", fail_encapsulation)
    else:
        from edge_gateway.crypto.kdf import KdfError

        def fail_derivation(_shared_secret: bytes) -> bytes:
            raise KdfError("injected KDF failure")

        monkeypatch.setattr("edge_gateway.crypto.session.derive_session_key", fail_derivation)

    with pytest.raises(SessionEstablishmentError) as caught:
        asyncio.run(manager.get_or_establish())

    assert caught.value.retryable is False
    assert metrics.mlkem_handshake_failures_total == 1
    assert cloud.posts == 0


def test_close_wipes_the_session_key(cloud_url):
    url, _cloud, clock = cloud_url
    manager = _manager(url, clock)
    session = asyncio.run(manager.get_or_establish())
    manager.close()
    assert session.state is SessionState.CLOSED
    assert bytes(session.session_key) == b"\x00" * len(session.session_key)


def test_close_refuses_a_later_handshake(cloud_url):
    url, cloud, clock = cloud_url
    manager = _manager(url, clock)
    asyncio.run(manager.get_or_establish())
    manager.close()

    with pytest.raises(SessionEstablishmentError) as caught:
        asyncio.run(manager.get_or_establish())

    assert caught.value.retryable is False
    assert cloud.posts == 1
