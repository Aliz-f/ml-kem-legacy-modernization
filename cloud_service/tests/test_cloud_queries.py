"""M4-12/13 query shape, bounds, filters, missing records, and safe failures."""

from dataclasses import replace

from fastapi.testclient import TestClient
import pytest

from cloud_service.app import create_app
from cloud_service.config import load_config
from cloud_service.storage.database import StorageError
from cloud_service.validation import validate_measurement

PATH = "/api/v1/measurements"


@pytest.fixture
def client():
    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        yield client


@pytest.fixture
def measurement():
    return validate_measurement({
        "device_id": "sensor-1", "gateway_id": "gateway-1", "temperature_c": 22.5,
        "humidity_pct": 44, "sequence_number": 1,
        "measured_at": "2026-09-21T12:00:00Z", "received_at": "2026-09-21T12:00:01Z",
    })


def test_empty_list_and_missing_record(client):
    response = client.get(PATH)
    assert response.status_code == 200 and response.json() == {"items": []}
    response = client.get(PATH + "/absent")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "MEASUREMENT_NOT_FOUND", "message": "measurement not found"}}


def test_list_and_detail_match_stored_contract(client, measurement):
    stored = client.app.state.repository.save(measurement)
    assert client.get(PATH).json() == {"items": [stored.to_dict()]}
    detail = client.get(PATH + "/" + stored.record_id)
    assert detail.status_code == 200
    assert detail.json() == stored.to_dict()
    assert set(detail.json()) == {
        "record_id", "device_id", "gateway_id", "temperature_c", "humidity_pct",
        "measured_at", "gateway_received_at", "cloud_received_at", "sequence_number",
    }
    assert client.app.state.repository.list() == [stored]


def test_limits_default_and_maximum_are_applied(client, measurement):
    repository = client.app.state.repository
    for sequence in range(1001):
        repository.save(replace(measurement, sequence_number=sequence))
    assert len(client.get(PATH).json()["items"]) == 100
    assert len(client.get(PATH, params={"limit": 1000}).json()["items"]) == 1000
    first = client.get(PATH, params={"limit": 1}).json()["items"]
    assert len(first) == 1 and first[0]["sequence_number"] == 0
    assert len(repository.list(1001)) == 1001


def test_device_filter_and_limit_preserve_insertion_order(client, measurement):
    repository = client.app.state.repository
    first = repository.save(measurement)
    other = repository.save(replace(measurement, device_id="other"))
    second = repository.save(replace(measurement, sequence_number=2))
    assert client.get(PATH).json()["items"] == [row.to_dict() for row in (first, other, second)]
    assert client.get(PATH, params={"device_id": "sensor-1"}).json()["items"] == [first.to_dict(), second.to_dict()]
    assert client.get(PATH, params={"device_id": "sensor-1", "limit": 1}).json()["items"] == [first.to_dict()]
    assert client.get(PATH, params={"device_id": "absent"}).json() == {"items": []}


@pytest.mark.parametrize("limit", ["0", "-1", "1001", "1.5", "true", "", "abc", "1e2", "9" * 5000])
def test_invalid_limits_rejected_before_storage(client, limit, monkeypatch):
    def fail(*args, **kwargs):
        pytest.fail("Invalid query must not reach storage")
    monkeypatch.setattr(client.app.state.repository, "list", fail)
    response = client.get(PATH, params={"limit": limit})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_QUERY"


def test_filter_is_parameterized(client, measurement):
    repository = client.app.state.repository
    device = "sensor'; DROP TABLE measurements; --"
    stored = repository.save(replace(measurement, device_id=device))
    assert client.get(PATH, params={"device_id": device}).json() == {"items": [stored.to_dict()]}
    assert client.get(PATH, params={"device_id": "' OR 1=1 --"}).json() == {"items": []}
    assert repository.get(stored.record_id) == stored


@pytest.mark.parametrize("path", [PATH, PATH + "/absent"])
def test_closed_storage_is_503_not_empty_or_not_found(client, path):
    client.app.state.database.close()
    response = client.get(path)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "STORAGE_UNAVAILABLE"


@pytest.mark.parametrize("path", [PATH, PATH + "/absent"])
def test_missing_repository_is_503(client, path):
    client.app.state.repository = None
    assert client.get(path).status_code == 503


@pytest.mark.parametrize(("path", "method"), [(PATH, "list"), (PATH + "/absent", "get")])
@pytest.mark.parametrize(("error_type", "status"), [(StorageError, 503), (RuntimeError, 500)])
def test_safe_query_errors(client, path, method, error_type, status, monkeypatch, caplog):
    def fail(*args, **kwargs):
        raise error_type("private-query-marker")
    monkeypatch.setattr(client.app.state.repository, method, fail)
    response = client.get(path)
    assert response.status_code == status
    assert "private-query-marker" not in response.text + caplog.text
