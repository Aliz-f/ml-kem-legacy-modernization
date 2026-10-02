"""GET /api/v1/crypto/public-key client."""

import json
import socket
import struct
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from edge_gateway.crypto.encoding import encode_binary
from edge_gateway.crypto.public_key import PublicKeyRejected
from edge_gateway.crypto.public_key_client import (
    PublicKeyTransportError,
    fetch_public_key,
)


def _public_key() -> bytes:
    private_key = MLKEM768PrivateKey.generate()
    return private_key.public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )


class _Response:
    def __init__(self, status: int, body: bytes, path: str = "/api/v1/crypto/public-key"):
        self.status = status
        self.body = body
        self.path = path
        self.delay_seconds = 0.0
        self.redirect_to: str | None = None
        self.reset = False


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
    def do_GET(self) -> None:  # noqa: N802
        response: _Response = self.server.response  # type: ignore[attr-defined]
        if self.path != response.path:
            self.send_error(404)
            return
        if response.delay_seconds:
            import time

            time.sleep(response.delay_seconds)
        if response.redirect_to is not None:
            self.send_response(302)
            self.send_header("Location", response.redirect_to)
            self.end_headers()
            return
        if response.reset:
            _reset_mid_body(self, 200)
            return
        self.send_response(response.status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response.body)))
        self.end_headers()
        self.wfile.write(response.body)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def cloud_server():
    response = _Response(200, b"{}")
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    server.response = response  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}", response
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


def _body(public_key: bytes) -> bytes:
    return json.dumps(
        {
            "protocol_version": "1",
            "algorithm": "ML-KEM-768",
            "key_id": "cloud-key-001",
            "public_key": encode_binary(public_key),
        }
    ).encode()


def test_fetch_returns_validated_public_key(cloud_server):
    base_url, response = cloud_server
    public_key = _public_key()
    response.body = _body(public_key)
    fetched = fetch_public_key(base_url, timeout_seconds=3)
    assert fetched.public_key == public_key
    assert fetched.key_id == "cloud-key-001"


def test_fetch_does_not_encapsulate(monkeypatch: pytest.MonkeyPatch, cloud_server):
    base_url, response = cloud_server
    response.body = _body(_public_key())

    def fail_encapsulate(public_key: bytes) -> tuple[bytes, bytes]:
        raise AssertionError("public-key client encapsulated")

    monkeypatch.setattr(
        "edge_gateway.crypto.mlkem.encapsulate",
        fail_encapsulate,
    )
    fetch_public_key(base_url, timeout_seconds=3)


@pytest.mark.parametrize(
    ("status", "retryable"),
    [(400, False), (422, False), (500, True), (503, True), (504, True)],
)
def test_http_status_is_classified(cloud_server, status: int, retryable: bool):
    base_url, response = cloud_server
    response.status = status
    response.body = b"{}"
    with pytest.raises(PublicKeyTransportError) as caught:
        fetch_public_key(base_url, timeout_seconds=3)
    assert caught.value.retryable is retryable


def test_invalid_json_is_not_a_transport_retry(cloud_server):
    base_url, response = cloud_server
    response.body = b"not-json"
    with pytest.raises(PublicKeyRejected):
        fetch_public_key(base_url, timeout_seconds=3)


def test_timeout_is_retryable(cloud_server):
    base_url, response = cloud_server
    response.delay_seconds = 1
    response.body = b"{}"
    with pytest.raises(PublicKeyTransportError) as caught:
        fetch_public_key(base_url, timeout_seconds=0.1)
    assert caught.value.retryable is True


def test_connection_failure_is_retryable():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    with pytest.raises(PublicKeyTransportError) as caught:
        fetch_public_key(f"http://127.0.0.1:{port}", timeout_seconds=1)
    assert caught.value.retryable is True


def test_redirect_is_not_followed(cloud_server):
    base_url, response = cloud_server
    response.redirect_to = base_url + "/elsewhere"
    with pytest.raises(PublicKeyTransportError) as caught:
        fetch_public_key(base_url, timeout_seconds=3)
    assert caught.value.retryable is False


def test_connection_reset_while_reading_is_retryable(cloud_server):
    base_url, response = cloud_server
    response.reset = True
    with pytest.raises(PublicKeyTransportError) as caught:
        fetch_public_key(base_url, timeout_seconds=3)
    assert caught.value.retryable is True


def test_oversized_body_is_rejected(cloud_server):
    base_url, response = cloud_server
    response.body = b"{" + b" " * (16 * 1024)
    with pytest.raises(PublicKeyRejected):
        fetch_public_key(base_url, timeout_seconds=3)


def test_cloud_url_and_timeout_are_validated():
    with pytest.raises(PublicKeyTransportError) as caught:
        fetch_public_key("ftp://cloud.example", timeout_seconds=3)
    assert caught.value.retryable is False
    with pytest.raises(PublicKeyTransportError):
        fetch_public_key("http://cloud.example", timeout_seconds=0)
