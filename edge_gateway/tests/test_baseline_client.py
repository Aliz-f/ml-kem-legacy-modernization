"""M2-13 classical Gateway-to-Cloud transport contract."""

import asyncio
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from fastapi.testclient import TestClient

from edge_gateway.app import create_app
from edge_gateway.cloud.baseline import BaselineAcceptance, BaselineCloudClient, BaselineCloudError
from edge_gateway.config import load_config


class _Cloud:
    def __init__(self) -> None:
        self.responses: list[tuple[int, object]] = [(202, {"status": "accepted", "record_id": "rec-1"})]
        self.requests: list[tuple[str, bytes, dict[str, str]]] = []
        self.delay_seconds = 0.0
        self.redirect_to: str | None = None


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        cloud: _Cloud = self.server.cloud  # type: ignore[attr-defined]
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        cloud.requests.append((self.path, body, dict(self.headers)))
        if cloud.delay_seconds:
            time.sleep(cloud.delay_seconds)
        if cloud.redirect_to is not None:
            self.send_response(302)
            self.send_header("Location", cloud.redirect_to)
            self.end_headers()
            return
        status, payload = cloud.responses.pop(0)
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


def _send(client: BaselineCloudClient, **overrides: object) -> BaselineAcceptance:
    fields: dict[str, object] = {
        "request_id": "req-baseline-1",
        "gateway_id": "gateway-001",
        "device_id": "sensor-001",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z",
        "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218Z",
    }
    fields.update(overrides)
    return asyncio.run(client.send(**fields))  # type: ignore[arg-type]


def test_client_posts_exact_canonical_body_and_request_header(cloud):
    url, script = cloud
    result = _send(BaselineCloudClient(cloud_url=url, timeout_seconds=1))
    assert result == BaselineAcceptance(status="accepted", record_id="rec-1")
    path, body, headers = script.requests[0]
    assert path == "/api/v1/baseline/measurements"
    assert headers["Content-Type"] == "application/json"
    assert headers["X-Request-Id"] == "req-baseline-1"
    assert json.loads(body) == {
        "gateway_id": "gateway-001", "device_id": "sensor-001",
        "temperature_c": 21.7, "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z", "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218Z",
    }
    assert b"request_id" not in body


def test_client_normalizes_idempotent_acceptance(cloud):
    url, script = cloud
    script.responses = [(202, {"status": "already_accepted", "record_id": "rec-existing"})]
    assert _send(BaselineCloudClient(cloud_url=url, timeout_seconds=1)) == BaselineAcceptance(
        status="already_accepted", record_id="rec-existing",
    )


def test_classical_app_constructs_and_uses_baseline_client(cloud):
    url, script = cloud
    config = load_config({"CLOUD_URL": url, "SECURITY_MODE": "classical"})
    payload = {
        "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
        "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 184,
    }
    with TestClient(create_app(config)) as gateway:
        response = gateway.post("/api/v1/measurements", json=payload)
    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert len(script.requests) == 1


@pytest.mark.parametrize(("status", "retryable"), [
    (400, False), (409, False), (422, False), (500, True), (502, True), (503, True), (504, True),
])
def test_http_failures_are_classified_without_retry(cloud, status, retryable):
    url, script = cloud
    script.responses = [(status, {"error": {"code": "PRIVATE_REMOTE_DETAIL", "message": "private"}})]
    with pytest.raises(BaselineCloudError) as caught:
        _send(BaselineCloudClient(cloud_url=url, timeout_seconds=1))
    assert caught.value.retryable is retryable
    assert caught.value.code == "PRIVATE_REMOTE_DETAIL"
    assert len(script.requests) == 1
    assert "PRIVATE_REMOTE_DETAIL" not in str(caught.value)


@pytest.mark.parametrize("payload", [
    {}, [], {"status": "accepted"}, {"status": "pending", "record_id": "rec-1"},
    {"status": "accepted", "record_id": " "}, "not-an-object",
])
def test_untrusted_success_response_is_rejected_without_retry(cloud, payload):
    url, script = cloud
    script.responses = [(202, payload)]
    with pytest.raises(BaselineCloudError) as caught:
        _send(BaselineCloudClient(cloud_url=url, timeout_seconds=1))
    assert caught.value.retryable is False
    assert len(script.requests) == 1


def test_timeout_and_connection_failures_are_retryable(cloud):
    url, script = cloud
    script.delay_seconds = 0.2
    with pytest.raises(BaselineCloudError) as timeout:
        _send(BaselineCloudClient(cloud_url=url, timeout_seconds=0.01))
    assert timeout.value.retryable is True
    with pytest.raises(BaselineCloudError) as connection:
        _send(BaselineCloudClient(cloud_url="http://127.0.0.1:9", timeout_seconds=1))
    assert connection.value.retryable is True


def test_redirect_is_rejected_and_constructor_validates_inputs(cloud):
    url, script = cloud
    script.redirect_to = url + "/redirected"
    with pytest.raises(BaselineCloudError) as redirect:
        _send(BaselineCloudClient(cloud_url=url, timeout_seconds=1))
    assert redirect.value.retryable is False
    with pytest.raises(ValueError):
        BaselineCloudClient(cloud_url="not-a-url", timeout_seconds=1)
    with pytest.raises(ValueError):
        BaselineCloudClient(cloud_url=url, timeout_seconds=0)
    with pytest.raises(ValueError):
        BaselineCloudClient(cloud_url=url, timeout_seconds=True)  # type: ignore[arg-type]
