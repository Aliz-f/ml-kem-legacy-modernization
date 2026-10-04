"""M4-05 through M4-07 storage model, SQLite lifecycle, and repository."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timezone
import traceback

import pytest

from cloud_service.models import CanonicalMeasurement
from cloud_service.storage.database import Database, StorageConflictError, StorageError
from cloud_service.storage.models import StoredMeasurement
from cloud_service.storage.repository import MeasurementRepository
from cloud_service.validation import MeasurementValidationError


@pytest.fixture
def measurement():
    return CanonicalMeasurement.from_dict({
        "device_id": "sensor-001", "gateway_id": "gateway-001",
        "temperature_c": 21.7, "humidity_pct": 42.5, "sequence_number": 184,
        "measured_at": "2026-09-21T13:45:31Z",
        "received_at": "2026-09-21T13:45:31.218Z",
    })


@pytest.fixture
def database():
    db = Database("sqlite:///:memory:")
    yield db
    db.close()


def test_exact_stored_model_mapping(measurement):
    now = datetime(2026, 9, 21, 13, 45, 32, tzinfo=timezone.utc)
    stored = StoredMeasurement.from_canonical(measurement, record_id="rec-test", cloud_received_at=now)
    assert stored.record_id == "rec-test"
    assert stored.cloud_received_at == now
    assert stored.gateway_received_at == measurement.received_at
    for field in ("device_id", "gateway_id", "temperature_c", "humidity_pct", "measured_at", "sequence_number"):
        assert getattr(stored, field) == getattr(measurement, field)
    assert set(stored.to_dict()) == {
        "record_id", "device_id", "gateway_id", "temperature_c", "humidity_pct",
        "measured_at", "gateway_received_at", "cloud_received_at", "sequence_number",
    }
    assert stored.to_dict()["gateway_received_at"] == "2026-09-21T13:45:31.218000Z"


def test_generated_metadata(measurement):
    before = datetime.now(timezone.utc)
    first = StoredMeasurement.from_canonical(measurement)
    second = StoredMeasurement.from_canonical(measurement)
    assert first.record_id.startswith("rec-") and first.record_id != second.record_id
    assert before <= first.cloud_received_at <= datetime.now(timezone.utc)


def test_invalid_metadata_and_domain_are_rejected(measurement, database):
    with pytest.raises(ValueError, match="record_id"):
        StoredMeasurement.from_canonical(measurement, record_id=" ")
    with pytest.raises(ValueError, match="cloud_received_at"):
        StoredMeasurement.from_canonical(measurement, cloud_received_at=datetime(2026, 1, 1))
    repository = MeasurementRepository(database)
    with pytest.raises(MeasurementValidationError):
        repository.save(replace(measurement, humidity_pct=101))
    assert repository.list() == []


def test_save_get_find_and_missing(database, measurement):
    repository = MeasurementRepository(database)
    stored = repository.save(measurement)
    assert repository.get(stored.record_id) == stored
    assert repository.find_by_device_sequence(measurement.device_id, measurement.sequence_number) == stored
    assert repository.get("absent") is None
    assert repository.find_by_device_sequence("absent", measurement.sequence_number) is None
    assert repository.find_by_device_sequence(measurement.device_id, 999) is None


def test_reopen_preserves_schema_and_committed_data(tmp_path, measurement):
    path = tmp_path / "cloud.db"
    url = f"sqlite:///{path.as_posix()}"
    first = Database(url)
    try:
        stored = MeasurementRepository(first).save(measurement)
    finally:
        first.close()
    second = Database(url)
    try:
        assert MeasurementRepository(second).get(stored.record_id) == stored
        with second.transaction() as connection:
            columns = connection.execute("PRAGMA table_info(measurements)").fetchall()
            assert {row["name"] for row in columns} == set(stored.to_dict())
            assert next(row for row in columns if row["name"] == "record_id")["pk"] == 1
            assert all(row["notnull"] for row in columns)
    finally:
        second.close()


def test_relative_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    db = Database("sqlite:///relative.db")
    db.close()
    assert (tmp_path / "relative.db").is_file()


def test_list_limit_filter_and_order(database, measurement):
    repository = MeasurementRepository(database)
    assert repository.list() == []
    first = repository.save(measurement)
    second = repository.save(replace(measurement, sequence_number=185))
    third = repository.save(replace(measurement, device_id="other"))
    assert repository.list() == [first, second, third]
    assert repository.list(1) == [first]
    assert repository.list(device_id="other") == [third]
    assert repository.list(1, device_id=measurement.device_id) == [first]
    assert repository.list(device_id="absent") == []


@pytest.mark.parametrize("limit", [0, -1, True, 1.5, "1"])
def test_invalid_repository_limits(database, limit):
    with pytest.raises(ValueError, match="limit"):
        MeasurementRepository(database).list(limit)


def test_database_uniqueness_is_a_conflict_not_idempotent_success(database, measurement):
    repository = MeasurementRepository(database)
    first = repository.save(measurement)
    with pytest.raises(StorageConflictError):
        repository.save(replace(measurement, temperature_c=22))
    assert repository.list() == [first]
    second = repository.save(replace(measurement, sequence_number=185))
    assert repository.list() == [first, second]


def test_parameterized_identifiers(database, measurement):
    repository = MeasurementRepository(database)
    device = "sensor'; DROP TABLE measurements; --"
    stored = repository.save(replace(measurement, device_id=device))
    assert repository.find_by_device_sequence(device, measurement.sequence_number) == stored
    assert repository.list(device_id=device) == [stored]
    assert repository.get("' OR 1=1 --") is None


def test_closed_database_errors_are_safe(database, measurement):
    repository = MeasurementRepository(database)
    database.close()
    database.close()
    assert database.closed
    for action in (lambda: repository.save(measurement), lambda: repository.get("missing"),
                   lambda: repository.find_by_device_sequence("sensor", 1), repository.list):
        with pytest.raises(StorageError, match="closed"):
            action()


def test_storage_failures_are_safe_and_leave_no_row(database, measurement, caplog):
    repository = MeasurementRepository(database)
    with database.transaction() as connection:
        connection.execute("PRAGMA query_only = ON")
    with pytest.raises(StorageError) as error:
        repository.save(measurement)
    rendered = "".join(traceback.format_exception(error.value))
    assert "readonly database" not in rendered
    assert measurement.device_id not in rendered
    assert repository.list() == []
    assert caplog.text == ""


def test_unrepresentable_sequence_is_rejected_as_invalid_measurement(database, measurement):
    with pytest.raises(MeasurementValidationError, match="sequence_number"):
        MeasurementRepository(database).save(replace(measurement, sequence_number=2**63))
    assert MeasurementRepository(database).list() == []


def test_transaction_rolls_back_on_error(database, measurement):
    repository = MeasurementRepository(database)
    stored = repository.save(measurement)
    with pytest.raises(StorageError):
        with database.transaction() as connection:
            connection.execute("DELETE FROM measurements")
            connection.execute("INSERT INTO nonexistent_table VALUES (1)")
    assert repository.get(stored.record_id) == stored


def test_corrupted_stored_row_is_translated(database, measurement):
    repository = MeasurementRepository(database)
    stored = repository.save(measurement)
    with database.transaction() as connection:
        connection.execute("UPDATE measurements SET measured_at = ?", ("private-corrupt-marker",))
    with pytest.raises(StorageError, match="stored measurement is invalid") as error:
        repository.get(stored.record_id)
    assert "private-corrupt-marker" not in "".join(traceback.format_exception(error.value))


def test_missing_parent_and_invalid_file_errors_are_safe(tmp_path):
    for path in (tmp_path / "missing-parent" / "private-path.db", tmp_path / "corrupt.db"):
        if path.parent == tmp_path:
            path.write_bytes(b"not a sqlite database")
        with pytest.raises(StorageError, match="initialization failed") as error:
            Database(f"sqlite:///{path.as_posix()}")
        assert str(path) not in "".join(traceback.format_exception(error.value))


def test_concurrent_repository_access(database, measurement):
    repository = MeasurementRepository(database)
    with ThreadPoolExecutor(max_workers=4) as pool:
        stored = list(pool.map(lambda n: repository.save(replace(measurement, sequence_number=n)), range(12)))
    assert len(repository.list()) == 12
    assert {item.record_id for item in repository.list()} == {item.record_id for item in stored}
