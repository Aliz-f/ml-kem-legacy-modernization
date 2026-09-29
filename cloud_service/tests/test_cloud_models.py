"""Shared canonical schema parsed independently by Cloud."""

from datetime import datetime, timezone
import json

import pytest

from cloud_service.models import CanonicalMeasurement, MeasurementSchemaError


@pytest.fixture
def payload():
    return {
        "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z", "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218Z", "gateway_id": "gateway-001",
    }


def test_shared_example_and_round_trip(payload):
    original = payload.copy()
    model = CanonicalMeasurement.from_dict(payload)
    assert model.measured_at == datetime(2026, 9, 21, 13, 45, 31, tzinfo=timezone.utc)
    assert model.received_at.microsecond == 218000
    assert model.device_id == "sensor-001"
    assert model.gateway_id == "gateway-001"
    assert model.temperature_c == 21.7
    assert model.humidity_pct == 42.5
    assert model.sequence_number == 184
    serialized = json.loads(json.dumps(model.to_dict(), allow_nan=False))
    assert set(serialized) == set(payload)
    assert CanonicalMeasurement.from_dict(serialized) == model
    assert payload == original


@pytest.mark.parametrize("field", ["device_id", "temperature_c", "humidity_pct",
                                   "measured_at", "sequence_number", "received_at", "gateway_id"])
def test_missing_fields(payload, field):
    del payload[field]
    with pytest.raises(MeasurementSchemaError):
        CanonicalMeasurement.from_dict(payload)


@pytest.mark.parametrize(("field", "value"), [
    ("device_id", 3), ("gateway_id", None), ("temperature_c", "21.7"),
    ("temperature_c", True), ("humidity_pct", False), ("humidity_pct", []),
    ("sequence_number", 1.0), ("sequence_number", True), ("sequence_number", "1"),
    ("measured_at", 0), ("received_at", None),
    ("temperature_c", float("nan")), ("humidity_pct", float("inf")),
    ("temperature_c", 10**400),
])
def test_wrong_types_and_non_json_numbers(payload, field, value):
    payload[field] = value
    with pytest.raises(MeasurementSchemaError):
        CanonicalMeasurement.from_dict(payload)


@pytest.mark.parametrize("field", ["measured_at", "received_at"])
@pytest.mark.parametrize("value", ["", "not-a-date", "2026-09-21",
    "2026-09-21T13:45:31", "2026-09-21T13:45:31+03:00", "2026-02-30T13:45:31Z"])
def test_invalid_timestamps(payload, field, value):
    payload[field] = value
    with pytest.raises(MeasurementSchemaError, match=field):
        CanonicalMeasurement.from_dict(payload)


def test_utc_offset_and_integer_sensor_values(payload):
    payload.update(measured_at="2026-09-21T13:45:31+00:00", temperature_c=22, humidity_pct=40)
    model = CanonicalMeasurement.from_dict(payload)
    assert model.to_dict()["measured_at"] == "2026-09-21T13:45:31Z"
    assert model.temperature_c == 22


@pytest.mark.parametrize("extra", ["request_id", "timestamp", "record_id", "cloud_received_at"])
def test_noncanonical_fields_rejected(payload, extra):
    payload[extra] = "not-canonical"
    with pytest.raises(MeasurementSchemaError):
        CanonicalMeasurement.from_dict(payload)


@pytest.mark.parametrize("value", [None, [], "{}", 1])
def test_nonobject_payload(value):
    with pytest.raises(MeasurementSchemaError):
        CanonicalMeasurement.from_dict(value)


def test_direct_construction_checks_schema(payload):
    values = CanonicalMeasurement.from_dict(payload).to_dict()
    values["measured_at"] = datetime(2026, 9, 21)
    values["received_at"] = datetime(2026, 9, 21, tzinfo=timezone.utc)
    with pytest.raises(MeasurementSchemaError, match="measured_at"):
        CanonicalMeasurement(**values)
