"""M2-07 Gateway canonical schema and outbound serialization contract."""

from dataclasses import FrozenInstanceError, fields
from datetime import datetime, timedelta, timezone
import json

import pytest

from edge_gateway.models import CanonicalMeasurement, CanonicalMeasurementSchemaError


@pytest.fixture
def values():
    return {
        "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
        "measured_at": datetime(2026, 9, 21, 13, 45, 31, tzinfo=timezone.utc),
        "sequence_number": 184,
        "received_at": datetime(2026, 9, 21, 13, 45, 31, 218000, tzinfo=timezone.utc),
        "gateway_id": "gateway-001",
    }


def test_exact_protocol_fields_and_json_serialization(values):
    model = CanonicalMeasurement(**values)
    assert {field.name for field in fields(model)} == {
        "device_id", "temperature_c", "humidity_pct", "measured_at",
        "sequence_number", "received_at", "gateway_id",
    }
    assert json.loads(json.dumps(model.to_dict(), allow_nan=False)) == {
        "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z", "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218000Z", "gateway_id": "gateway-001",
    }


def test_values_are_preserved_and_serialized_dict_is_independent(values):
    values.update(temperature_c=-25, humidity_pct=100, sequence_number=0)
    model = CanonicalMeasurement(**values)
    for name, value in values.items():
        assert getattr(model, name) == value
        assert type(getattr(model, name)) is type(value)
    serialized = model.to_dict()
    serialized["device_id"] = "changed"
    assert model.device_id == "sensor-001"
    with pytest.raises(FrozenInstanceError):
        model.sequence_number = 9


@pytest.mark.parametrize("field", [
    "device_id", "temperature_c", "humidity_pct", "measured_at",
    "sequence_number", "received_at", "gateway_id",
])
def test_all_fields_are_required(values, field):
    del values[field]
    with pytest.raises(TypeError):
        CanonicalMeasurement(**values)


@pytest.mark.parametrize("extra", [
    "timestamp", "request_id", "session_id", "nonce", "ciphertext", "public_key",
    "record_id", "cloud_received_at", "gateway_received_at",
])
def test_noncanonical_fields_cannot_be_added(values, extra):
    with pytest.raises(TypeError):
        CanonicalMeasurement(**values, **{extra: "extra"})


@pytest.mark.parametrize(("field", "value"), [
    ("device_id", None), ("gateway_id", 1),
    ("temperature_c", True), ("temperature_c", "21.7"),
    ("humidity_pct", None), ("humidity_pct", False),
    ("sequence_number", True), ("sequence_number", 1.0), ("sequence_number", "184"),
])
def test_invalid_types_are_not_coerced(values, field, value):
    values[field] = value
    with pytest.raises(CanonicalMeasurementSchemaError):
        CanonicalMeasurement(**values)


@pytest.mark.parametrize("field", ["temperature_c", "humidity_pct"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), 10**400])
def test_nonfinite_or_unrepresentable_numbers_are_rejected(values, field, value):
    values[field] = value
    with pytest.raises(CanonicalMeasurementSchemaError):
        CanonicalMeasurement(**values)


@pytest.mark.parametrize("field", ["measured_at", "received_at"])
@pytest.mark.parametrize("value", [
    "2026-09-21T13:45:31Z", None, datetime(2026, 9, 21),
    datetime(2026, 9, 21, tzinfo=timezone(timedelta(hours=3))),
])
def test_timestamps_require_explicit_utc_datetimes(values, field, value):
    values[field] = value
    with pytest.raises(CanonicalMeasurementSchemaError):
        CanonicalMeasurement(**values)


def test_internal_error_does_not_echo_supplied_values(values):
    values["temperature_c"] = "private-payload-marker"
    with pytest.raises(CanonicalMeasurementSchemaError) as error:
        CanonicalMeasurement(**values)
    assert "private-payload-marker" not in str(error.value)
