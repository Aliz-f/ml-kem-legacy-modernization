"""M2-15 frozen Gateway outcome-to-Legacy response mapping."""

from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from edge_gateway.app import create_app
from edge_gateway.cloud.baseline import BaselineCloudError
from edge_gateway.config import load_config
from edge_gateway.crypto.secure_transport import SecureTransportError
from edge_gateway.errors import GatewayError, GatewayErrorCode


PATH = "/api/v1/measurements"
PAYLOAD = {
    "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
    "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 1,
}


class _Transport:
    def __init__(self, *, result: object | None = None, error: Exception | None = None) -> None:
        self.result = result or SimpleNamespace(status="accepted", record_id="rec-1")
        self.error = error
        self.calls = 0

    async def send(self, **kwargs: object) -> object:
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.result


@pytest.mark.parametrize(("payload", "status", "code"), [
    (b"{", 400, "INVALID_JSON"),
    (b'{"device_id":"sensor-001"}', 422, "INVALID_MEASUREMENT"),
])
def test_invalid_legacy_input_uses_frozen_client_error_mapping(payload, status, code):
    transport = _Transport()
    with TestClient(create_app(load_config({}), baseline_transport=transport)) as client:
        response = client.post(PATH, content=payload)
    assert response.status_code == status
    assert response.json()["error"]["code"] == code
    assert transport.calls == 0


@pytest.mark.parametrize(("first", "second", "code"), [
    (1, 1, "DUPLICATE_SEQUENCE"),
    (2, 1, "OUT_OF_ORDER_SEQUENCE"),
])
def test_sequence_rejections_use_frozen_conflict_mapping(first, second, code):
    transport = _Transport()
    with TestClient(create_app(load_config({}), baseline_transport=transport)) as client:
        assert client.post(PATH, json={**PAYLOAD, "sequence_number": first}).status_code == 202
        response = client.post(PATH, json={**PAYLOAD, "sequence_number": second})
    assert response.status_code == 409
    assert response.json()["error"]["code"] == code
    assert transport.calls == 1


@pytest.mark.parametrize("error", [
    BaselineCloudError("private baseline failure", retryable=True),
    BaselineCloudError("private baseline rejection", retryable=False),
    SecureTransportError("private secure failure", retryable=True),
    SecureTransportError("private session failure", retryable=False, code="SESSION_EXPIRED"),
    TimeoutError("private timeout"),
    ConnectionError("private connection"),
    GatewayError(GatewayErrorCode.CLOUD_UNAVAILABLE),
])
def test_cloud_and_secure_delivery_failures_map_to_safe_503(error, caplog):
    transport = _Transport(error=error)
    with TestClient(create_app(load_config({}), baseline_transport=transport)) as client:
        response = client.post(PATH, json=PAYLOAD)
    assert response.status_code == 503
    assert response.json() == {
        "error": {"code": "CLOUD_UNAVAILABLE", "message": "cloud service is unavailable"},
    }
    assert "private" not in response.text + caplog.text


def test_confirmed_cloud_acceptance_maps_to_202():
    transport = _Transport(result=SimpleNamespace(status="already_accepted", record_id="rec-1"))
    with TestClient(create_app(load_config({}), baseline_transport=transport)) as client:
        response = client.post(PATH, json=PAYLOAD)
    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}


def test_unexpected_gateway_failure_maps_to_safe_500(caplog):
    transport = _Transport(error=RuntimeError("private implementation detail"))
    with TestClient(create_app(load_config({}), baseline_transport=transport), raise_server_exceptions=False) as client:
        response = client.post(PATH, json=PAYLOAD)
    assert response.status_code == 500
    assert response.json() == {
        "error": {"code": "INTERNAL_ERROR", "message": "internal gateway error"},
    }
    assert "private implementation detail" not in response.text + caplog.text
