"""Real HTTP response failures through both Gateway delivery paths."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from edge_gateway.app import create_app
from edge_gateway.cloud.baseline import BaselineCloudClient
from edge_gateway.config import load_config
from edge_gateway.crypto.secure_transport import SecureTransport
from edge_gateway.crypto.session import SecureSession, SessionState


ACCEPTED = b'{"status":"accepted","record_id":"rec-1"}'
MEASUREMENT = {
    "device_id": "sensor-1", "temperature_c": 21.7, "humidity_pct": 42.5,
    "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 1,
}


@dataclass
class Reply:
    status: int = 202
    body: bytes = ACCEPTED
    missing_bytes: int = 0


class Cloud:
    def __init__(self):
        self.responses = [Reply()]
        self.requests = []


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        script = self.server.script
        body = self.rfile.read(int(self.headers["Content-Length"]))
        script.requests.append((self.path, body, self.headers.get("X-Request-ID")))
        reply = script.responses.pop(0)
        self.send_response(reply.status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(reply.body) + reply.missing_bytes))
        self.end_headers()
        self.wfile.write(reply.body)
        self.wfile.flush()
        self.close_connection = True

    def log_message(self, *args):
        pass


class Sessions:
    def __init__(self):
        self.calls = 0
        now = datetime.now(UTC)
        self.session = SecureSession(
            "sess-test", "gateway-001", "key-test", now, now + timedelta(seconds=300),
            bytearray(range(32)), SessionState.ACTIVE,
        )

    async def get_or_establish(self):
        self.calls += 1
        return self.session

    def invalidate(self, session_id=None):
        pytest.fail("ordinary response failures must not trigger session recovery")

    def close(self):
        self.session.clear(SessionState.CLOSED)


@pytest.fixture(params=["classical", "mlkem"])
def delivery(request):
    script = Cloud()
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.script = script
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    sessions, delays = Sessions(), []
    settings = load_config({"SECURITY_MODE": request.param})
    options = dict(cloud_url=f"http://127.0.0.1:{server.server_port}",
                   timeout_seconds=1, max_retries=2, sleep=delays.append)
    if request.param == "classical":
        transport = BaselineCloudClient(**options)
        app = create_app(settings, baseline_transport=transport)
    else:
        transport = SecureTransport(sessions, **options)
        app = create_app(settings, secure_transport=transport)
    try:
        with TestClient(app, raise_server_exceptions=False) as gateway:
            yield gateway, script, delays, sessions, transport
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


def assert_unavailable(response):
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "CLOUD_UNAVAILABLE"


def test_oversized_sequence_is_rejected_without_committing_sequence_state(delivery):
    gateway, script, _, _, _ = delivery
    response = gateway.post("/api/v1/measurements", json=MEASUREMENT | {"sequence_number": 2**63})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_MEASUREMENT"
    assert script.requests == []
    # If the invalid sequence had advanced the tracker, this would return 409.
    assert gateway.post("/api/v1/measurements", json=MEASUREMENT).status_code == 202
    assert len(script.requests) == 1


@pytest.mark.parametrize("partial", [b"", b'{"status":', ACCEPTED])
def test_truncated_acceptance_retries_identical_request(delivery, partial):
    gateway, script, delays, sessions, _ = delivery
    # Even syntactically valid JSON is incomplete if HTTP framing promises more.
    script.responses = [Reply(body=partial, missing_bytes=5), Reply()]
    response = gateway.post("/api/v1/measurements", json=MEASUREMENT)
    assert response.status_code == 202
    assert delays == [1.0]
    assert len(script.requests) == 2
    assert script.requests[0] == script.requests[1]
    assert sessions.calls <= 1


def test_truncated_acceptance_exhausts_the_existing_retry_bound(delivery):
    gateway, script, delays, sessions, _ = delivery
    script.responses = [Reply(body=b'{"status":', missing_bytes=5)] * 3
    assert_unavailable(gateway.post("/api/v1/measurements", json=MEASUREMENT))
    assert delays == [1.0, 2.0]
    assert len(script.requests) == 3
    assert script.requests[0] == script.requests[1] == script.requests[2]
    assert sessions.calls <= 1


@pytest.mark.parametrize("body", [
    b'{"status":[],"record_id":"rec-1"}',
    b'{"status":{},"record_id":"rec-1"}',
    b"\xff", b'{"status":', b"[" * 5000 + b"0" + b"]" * 5000,
    ACCEPTED + b" " * (16 * 1024),
])
def test_complete_malformed_acceptance_maps_to_503_without_retry(delivery, body):
    gateway, script, delays, _, _ = delivery
    script.responses = [Reply(body=body)]
    assert_unavailable(gateway.post("/api/v1/measurements", json=MEASUREMENT))
    assert len(script.requests) == 1
    assert delays == []


@pytest.mark.parametrize("status", [400, 409, 422, 500, 502, 503, 504])
@pytest.mark.parametrize("body", [b"\xff", b"[" * 5000 + b"0" + b"]" * 5000])
def test_malformed_error_body_preserves_http_retry_classification(delivery, status, body):
    gateway, script, delays, sessions, _ = delivery
    script.responses = [Reply(status=status, body=body), Reply()]
    response = gateway.post("/api/v1/measurements", json=MEASUREMENT)
    if status >= 500:
        assert response.status_code == 202
        assert len(script.requests) == 2
        assert script.requests[0] == script.requests[1]
        assert delays == [1.0]
    else:
        assert_unavailable(response)
        assert len(script.requests) == 1
        assert delays == []
    assert sessions.calls <= 1


@pytest.mark.parametrize("status", [202, 400, 503])
def test_connection_reset_while_reading_preserves_retry_policy(delivery, monkeypatch, status):
    gateway, script, delays, sessions, transport = delivery
    original_open = transport._opener.open
    attempts = []

    def open_response(request, **kwargs):
        attempts.append(request.data)
        if len(attempts) == 1:
            if status != 202:
                from urllib.error import HTTPError

                body = MagicMock()
                body.read.side_effect = ConnectionResetError("synthetic reset")
                raise HTTPError(request.full_url, status, "error", {}, body)
            response = MagicMock()
            response.__enter__.return_value = response
            response.read.side_effect = ConnectionResetError("synthetic reset")
            return response
        return original_open(request, **kwargs)

    monkeypatch.setattr(transport._opener, "open", open_response)
    response = gateway.post("/api/v1/measurements", json=MEASUREMENT)
    if status == 400:
        assert_unavailable(response)
        assert len(attempts) == 1 and delays == [] and script.requests == []
    else:
        assert response.status_code == 202
        assert len(attempts) == 2 and attempts[0] == attempts[1]
        assert delays == [1.0]
    assert sessions.calls <= 1
