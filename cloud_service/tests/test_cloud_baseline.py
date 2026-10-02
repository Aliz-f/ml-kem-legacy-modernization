"""M4-08 through M4-11: atomic idempotency and baseline acceptance."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import logging

from fastapi.testclient import TestClient
import pytest

from cloud_service.app import create_app
from cloud_service.config import load_config
from cloud_service.storage.database import Database, StorageConflictError
from cloud_service.storage.models import StoredMeasurement
from cloud_service.storage.repository import MeasurementRepository
from cloud_service.validation import validate_measurement

ENDPOINT = "/api/v1/baseline/measurements"


@pytest.fixture
def payload():
    return {
        "device_id": "sensor-test", "gateway_id": "gateway-test",
        "temperature_c": 22.5, "humidity_pct": 44, "sequence_number": 1,
        "measured_at": "2026-09-21T12:00:00Z", "received_at": "2026-09-21T12:00:01Z",
    }


@pytest.fixture
def client(tmp_path):
    config = load_config({"DATABASE_URL": f"sqlite:///{(tmp_path / 'cloud.db').as_posix()}"})
    with TestClient(create_app(config)) as client:
        yield client


def test_acceptance_is_committed_and_correlated(client, payload, caplog):
    with caplog.at_level(logging.INFO, logger="cloud_service"):
        response = client.post(ENDPOINT, json=payload, headers={"X-Request-ID": "req-baseline-test"})
    assert response.status_code == 202
    assert response.json()["status"] == "accepted"
    record_id = response.json()["record_id"]
    independent = Database(client.app.state.config.database_url)
    try:
        stored = MeasurementRepository(independent).get(record_id)
        assert stored is not None
        assert stored.device_id == payload["device_id"]
        assert stored.gateway_id == payload["gateway_id"]
        assert stored.temperature_c == payload["temperature_c"]
        assert stored.humidity_pct == payload["humidity_pct"]
        assert stored.sequence_number == payload["sequence_number"]
        assert stored.gateway_received_at == validate_measurement(payload).received_at
        assert stored.cloud_received_at.utcoffset().total_seconds() == 0
        assert "request_id" not in stored.to_dict()
        with independent.transaction() as connection:
            assert "request_id" not in {row["name"] for row in connection.execute("PRAGMA table_info(measurements)")}
    finally:
        independent.close()
    assert "req-baseline-test" in caplog.text
    assert record_id in caplog.text
    assert "event=measurement_stored" in caplog.text
    assert "gateway_id='gateway-test'" in caplog.text
    assert "device_id='sensor-test'" in caplog.text
    assert "sequence_number=1" in caplog.text


def test_duplicate_log_keeps_frozen_common_correlation_fields(client, payload, caplog):
    assert client.post(ENDPOINT, json=payload).status_code == 202

    with caplog.at_level(logging.INFO, logger="cloud_service"):
        duplicate = client.post(ENDPOINT, json=payload, headers={"X-Request-ID": "req-baseline-duplicate"})

    assert duplicate.json()["status"] == "already_accepted"
    assert "event=measurement_duplicate" in caplog.text
    assert "request_id='req-baseline-duplicate'" in caplog.text
    assert "gateway_id='gateway-test'" in caplog.text
    assert "device_id='sensor-test'" in caplog.text
    assert "sequence_number=1" in caplog.text


def test_duplicate_and_lost_response_retry_preserve_original(client, payload):
    first = client.post(ENDPOINT, json=payload)
    original = client.app.state.repository.get(first.json()["record_id"])
    retry = client.post(ENDPOINT, json=payload, headers={"X-Request-ID": "req-retry"})
    changed = client.post(ENDPOINT, json={**payload, "temperature_c": 40, "gateway_id": "other"})
    for response in (retry, changed):
        assert response.status_code == 202
        assert response.json() == {"status": "already_accepted", "record_id": original.record_id}
    assert client.app.state.repository.list() == [original]


@pytest.mark.parametrize("update", [{"sequence_number": 2}, {"device_id": "second-device"}])
def test_distinct_logical_identity_creates_second_row(client, payload, update):
    first = client.post(ENDPOINT, json=payload)
    second = client.post(ENDPOINT, json={**payload, **update})
    assert first.status_code == second.status_code == 202
    assert second.json()["status"] == "accepted"
    assert first.json()["record_id"] != second.json()["record_id"]
    assert len(client.app.state.repository.list()) == 2


@pytest.mark.parametrize("body", [b"", b"{", b'{"x":}', b"\xff"])
def test_malformed_body_is_400_and_not_stored(client, body):
    response = client.post(ENDPOINT, content=body, headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_JSON"
    assert client.app.state.repository.list() == []


@pytest.mark.parametrize("update", [
    {"temperature_c": 86}, {"humidity_pct": -1}, {"sequence_number": -1},
    {"sequence_number": True}, {"device_id": ""}, {"gateway_id": " "},
    {"temperature_c": "22.5"}, {"measured_at": "invalid"},
    {"received_at": "2026-09-21T12:00:01"}, {"request_id": "not-a-body-field"},
])
def test_invalid_canonical_data_is_422(client, payload, update):
    response = client.post(ENDPOINT, json={**payload, **update})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_MEASUREMENT"
    assert client.app.state.repository.list() == []


@pytest.mark.parametrize("body", [{}, [], None, "text"])
def test_missing_fields_and_wrong_json_shape(client, body):
    import json

    response = client.post(ENDPOINT, content=json.dumps(body), headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    assert client.app.state.repository.list() == []


def test_duplicate_still_requires_validation(client, payload):
    original = client.post(ENDPOINT, json=payload).json()
    response = client.post(ENDPOINT, json={**payload, "humidity_pct": 101})
    assert response.status_code == 422
    assert len(client.app.state.repository.list()) == 1
    assert client.app.state.repository.get(original["record_id"]).humidity_pct == 44


def test_failed_write_returns_safe_503_then_retry_succeeds(client, payload, caplog):
    with client.app.state.database.transaction() as connection:
        connection.execute("""CREATE TRIGGER reject_test_insert BEFORE INSERT ON measurements
                              BEGIN SELECT RAISE(ABORT, 'private-storage-marker'); END""")
    response = client.post(ENDPOINT, json=payload)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "STORAGE_UNAVAILABLE"
    assert "private-storage-marker" not in response.text + caplog.text
    assert client.app.state.repository.list() == []
    with client.app.state.database.transaction() as connection:
        connection.execute("DROP TRIGGER reject_test_insert")
    assert client.post(ENDPOINT, json=payload).json()["status"] == "accepted"


def test_unexpected_repository_error_is_safe_500(client, payload, monkeypatch, caplog):
    def fail(_):
        raise RuntimeError("private-internal-marker")

    monkeypatch.setattr(client.app.state.repository, "save_idempotent", fail)
    response = client.post(ENDPOINT, json=payload)
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_ERROR"
    assert "private-internal-marker" not in response.text + caplog.text
    assert "event=baseline_internal_error component=cloud_service" in caplog.text
    assert client.app.state.repository.list() == []


def test_secure_body_never_falls_back_to_baseline(client, payload):
    response = client.post("/api/v1/secure/measurements", json=payload)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert client.app.state.repository.list() == []
    client.app.state.config = load_config({"SECURITY_MODE": "mlkem"})
    assert client.post(ENDPOINT, json=payload).status_code == 503
    assert client.app.state.repository.list() == []


def test_repository_absent_or_closed_never_accepts(client, payload):
    client.app.state.database.close()
    assert client.post(ENDPOINT, json=payload).status_code == 503
    client.app.state.repository = None
    assert client.post(ENDPOINT, json=payload).status_code == 503


def test_concurrent_duplicates_across_connections(tmp_path, payload):
    url = f"sqlite:///{(tmp_path / 'concurrent.db').as_posix()}"
    Database(url).close()
    measurement = validate_measurement(payload)

    def save(_):
        database = Database(url)
        try:
            return MeasurementRepository(database).save_idempotent(measurement)
        finally:
            database.close()

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(save, range(12)))
    assert sum(result.created for result in results) == 1
    assert len({result.measurement.record_id for result in results}) == 1
    reopened = Database(url)
    try:
        assert len(MeasurementRepository(reopened).list()) == 1
        assert not MeasurementRepository(reopened).save_idempotent(measurement).created
    finally:
        reopened.close()


def test_unrelated_record_id_collision_is_not_idempotent_success(client, payload, monkeypatch):
    repository = client.app.state.repository
    measurement = validate_measurement(payload)
    first = repository.save_idempotent(measurement)
    factory = StoredMeasurement.from_canonical
    monkeypatch.setattr(StoredMeasurement, "from_canonical", classmethod(
        lambda cls, value: factory(value, record_id=first.measurement.record_id)))
    with pytest.raises(StorageConflictError):
        repository.save_idempotent(replace(measurement, sequence_number=2))
    assert repository.list() == [first.measurement]
