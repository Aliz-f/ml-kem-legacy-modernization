"""Gateway schema tests using the documented Legacy wire contract."""

from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timezone
import json

import pytest

from edge_gateway.models import LegacyMeasurement, LegacyMeasurementSchemaError


@pytest.fixture
def payload():
    return {
        "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
        "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 184,
    }


def test_protocol_example_and_independent_round_trip(payload):
    original = payload.copy()
    model = LegacyMeasurement.from_dict(payload)
    assert model.device_id == "sensor-001"
    assert model.temperature_c == 21.7
    assert model.humidity_pct == 42.5
    assert model.timestamp == datetime(2026, 9, 21, 13, 45, 31, tzinfo=timezone.utc)
    assert model.sequence_number == 184
    assert {field.name for field in fields(model)} == set(payload)
    serialized = json.loads(json.dumps(model.to_dict(), allow_nan=False))
    assert serialized == original
    assert LegacyMeasurement.from_dict(serialized) == model
    serialized["device_id"] = "changed"
    assert model.device_id == "sensor-001"
    assert payload == original


@pytest.mark.parametrize("field", [
    "device_id", "temperature_c", "humidity_pct", "timestamp", "sequence_number",
])
def test_each_required_field_is_required(payload, field):
    del payload[field]
    with pytest.raises(LegacyMeasurementSchemaError):
        LegacyMeasurement.from_dict(payload)


@pytest.mark.parametrize(("field", "value"), [
    ("device_id", None), ("device_id", 1), ("device_id", []),
    ("temperature_c", "21.7"), ("temperature_c", True), ("temperature_c", None),
    ("humidity_pct", "42.5"), ("humidity_pct", False), ("humidity_pct", {}),
    ("sequence_number", True), ("sequence_number", 1.0), ("sequence_number", "184"),
    ("sequence_number", None), ("timestamp", 0), ("timestamp", None),
    ("timestamp", datetime(2026, 9, 21, tzinfo=timezone.utc)),
])
def test_wrong_types_are_not_coerced(payload, field, value):
    payload[field] = value
    with pytest.raises(LegacyMeasurementSchemaError):
        LegacyMeasurement.from_dict(payload)


@pytest.mark.parametrize("field", ["temperature_c", "humidity_pct"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), 10**400])
def test_nonfinite_or_unrepresentable_sensor_numbers(payload, field, value):
    payload[field] = value
    with pytest.raises(LegacyMeasurementSchemaError):
        LegacyMeasurement.from_dict(payload)


@pytest.mark.parametrize("value", [None, [], "{}", 1, True])
def test_payload_must_be_a_decoded_object(value):
    with pytest.raises(LegacyMeasurementSchemaError):
        LegacyMeasurement.from_dict(value)


@pytest.mark.parametrize("value", [
    "", "not-a-date", "2026-09-21", "2026-02-30T13:45:31Z",
    "2026-09-21T13:45:31", "2026-09-21T13:45:31+03:00",
])
def test_invalid_or_non_utc_timestamps(payload, value):
    payload["timestamp"] = value
    with pytest.raises(LegacyMeasurementSchemaError, match="timestamp"):
        LegacyMeasurement.from_dict(payload)


def test_utc_offset_fractional_seconds_and_integer_numbers(payload):
    payload.update(timestamp="2026-09-21T13:45:31.123456+00:00", temperature_c=22, humidity_pct=40)
    model = LegacyMeasurement.from_dict(payload)
    assert model.timestamp.microsecond == 123456
    assert model.to_dict()["timestamp"] == "2026-09-21T13:45:31.123456Z"
    assert model.temperature_c == 22
    assert model.humidity_pct == 40


def test_domain_validation_is_a_separate_stage(payload):
    payload.update(device_id="", temperature_c=86, humidity_pct=-1, sequence_number=-1)
    model = LegacyMeasurement.from_dict(payload)
    assert model.to_dict() == payload


def test_direct_construction_checks_types_and_model_is_immutable(payload):
    values = dict(payload, timestamp=datetime(2026, 9, 21, tzinfo=timezone.utc))
    model = LegacyMeasurement(**values)
    with pytest.raises(FrozenInstanceError):
        model.sequence_number = 2
    with pytest.raises(LegacyMeasurementSchemaError):
        LegacyMeasurement(**dict(values, timestamp=datetime(2026, 9, 21)))
    with pytest.raises(LegacyMeasurementSchemaError):
        LegacyMeasurement(**dict(values, temperature_c=True))


def test_error_does_not_echo_payload_values(payload):
    payload["temperature_c"] = "private-payload-marker"
    with pytest.raises(LegacyMeasurementSchemaError) as error:
        LegacyMeasurement.from_dict(payload)
    assert "private-payload-marker" not in str(error.value)


@pytest.mark.parametrize("extra", ["battery_level", "request_id", "gateway_id", "measured_at", "received_at"])
def test_extra_fields_are_rejected(payload, extra):
    payload[extra] = "private-extra-marker"
    with pytest.raises(LegacyMeasurementSchemaError) as error:
        LegacyMeasurement.from_dict(payload)
    assert "private-extra-marker" not in str(error.value)


def test_canonical_field_name_cannot_replace_legacy_timestamp(payload):
    payload["measured_at"] = payload.pop("timestamp")
    with pytest.raises(LegacyMeasurementSchemaError):
        LegacyMeasurement.from_dict(payload)
