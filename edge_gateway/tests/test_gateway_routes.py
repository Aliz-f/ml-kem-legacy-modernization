"""M2-39 Legacy route contract with the selected Cloud transport stubbed."""

from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from edge_gateway.transport import CloudDeliveryError


PATH = "/api/v1/measurements"
VALID = {
    "device_id": "sensor-route", "temperature_c": 21.7, "humidity_pct": 42.5,
    "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 10,
}


class Transport:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.calls: list[dict[str, object]] = []

    async def send(self, **fields: object) -> object:
        self.calls.append(fields)
        if self.error is not None:
            raise self.error
        return SimpleNamespace(status="accepted", record_id="record-route")


def _client(transport: Transport) -> TestClient:
    return TestClient(create_app(load_config({}), baseline_transport=transport))


def test_valid_route_returns_202_only_after_cloud_success() -> None:
    transport = Transport()
    with _client(transport) as client:
        response = client.post(PATH, json=VALID)

    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    assert len(transport.calls) == 1
    assert transport.calls[0]["device_id"] == VALID["device_id"]
    assert transport.calls[0]["sequence_number"] == VALID["sequence_number"]
    assert str(transport.calls[0]["request_id"]).startswith("req-")


@pytest.mark.parametrize(("body", "status", "code"), [
    (b"{", 400, "INVALID_JSON"),
    ({key: value for key, value in VALID.items() if key != "humidity_pct"},
     422, "INVALID_MEASUREMENT"),
    ({**VALID, "temperature_c": 85.01}, 422, "INVALID_MEASUREMENT"),
    ({**VALID, "humidity_pct": 100.1}, 422, "INVALID_MEASUREMENT"),
    ({**VALID, "timestamp": "2026-09-21T13:45:31"}, 422, "INVALID_MEASUREMENT"),
    ({**VALID, "sequence_number": -1}, 422, "INVALID_MEASUREMENT"),
])
def test_invalid_route_input_is_rejected_before_cloud(body, status, code) -> None:
    transport = Transport()
    with _client(transport) as client:
        response = (
            client.post(PATH, content=body, headers={"Content-Type": "application/json"})
            if isinstance(body, bytes)
            else client.post(PATH, json=body)
        )

    assert response.status_code == status
    assert response.json()["error"]["code"] == code
    assert transport.calls == []


def test_duplicate_and_out_of_order_routes_return_409_without_cloud_delivery() -> None:
    transport = Transport()
    with _client(transport) as client:
        assert client.post(PATH, json=VALID).status_code == 202
        duplicate = client.post(PATH, json=VALID)
        older = client.post(PATH, json={**VALID, "sequence_number": 9})

    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["code"] == "DUPLICATE_SEQUENCE"
    assert older.status_code == 409
    assert older.json()["error"]["code"] == "OUT_OF_ORDER_SEQUENCE"
    assert len(transport.calls) == 1


def test_cloud_failure_returns_503_and_committed_sequence_remains_duplicate() -> None:
    transport = Transport(CloudDeliveryError("simulated failure"))
    with _client(transport) as client:
        failed = client.post(PATH, json=VALID)
        repeated = client.post(PATH, json=VALID)

    assert failed.status_code == 503
    assert failed.json()["error"]["code"] == "CLOUD_UNAVAILABLE"
    assert repeated.status_code == 409
    assert repeated.json()["error"]["code"] == "DUPLICATE_SEQUENCE"
    assert len(transport.calls) == 1
