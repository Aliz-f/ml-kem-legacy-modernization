"""M2-08 lossless Legacy-to-canonical mapping with deterministic metadata."""

from datetime import datetime, timedelta, timezone
import json

import pytest

from edge_gateway.config import load_config
from edge_gateway.models import CanonicalMeasurementSchemaError, LegacyMeasurement
from edge_gateway.normalization import normalize
from edge_gateway.validation import parse_legacy_measurement, validate_legacy_measurement


MEASURED_AT = datetime(2026, 9, 21, 13, 45, 31, 123456, tzinfo=timezone.utc)
RECEIVED_AT = datetime(2026, 9, 21, 13, 45, 32, 654321, tzinfo=timezone.utc)


@pytest.mark.parametrize(("temperature", "humidity", "sequence"), [
    (21.7123456789, 42.5123456789, 184),
    (-40, 0, 0),
    (85, 100, 2**53 + 1),
    (-0.0, -0.0, 1),
])
def test_normalization_preserves_values_and_input(temperature, humidity, sequence):
    legacy = LegacyMeasurement(" sensor-001 ", temperature, humidity, MEASURED_AT, sequence)
    original = legacy.to_dict()
    validated = validate_legacy_measurement(legacy)
    config = load_config({"GATEWAY_ID": "gateway-normalization-test"})

    canonical = normalize(validated, gateway_id=config.gateway_id, received_at=RECEIVED_AT)

    for field in ("device_id", "temperature_c", "humidity_pct", "sequence_number"):
        assert getattr(canonical, field) == getattr(legacy, field)
        assert type(getattr(canonical, field)) is type(getattr(legacy, field))
    assert canonical.measured_at is legacy.timestamp
    assert canonical.received_at is RECEIVED_AT
    assert canonical.gateway_id == config.gateway_id
    assert legacy.to_dict() == original
    assert canonical == normalize(validated, gateway_id=config.gateway_id, received_at=RECEIVED_AT)
    # JSON comparison also detects losing the sign of a floating-point zero.
    assert json.dumps(canonical.temperature_c) == json.dumps(legacy.temperature_c)
    assert json.dumps(canonical.humidity_pct) == json.dumps(legacy.humidity_pct)


def test_parsed_measurement_normalizes_to_exact_canonical_wire_contract():
    legacy = validate_legacy_measurement(parse_legacy_measurement(b'''
        {"device_id":"sensor-001","temperature_c":21.7,"humidity_pct":42.5,
         "timestamp":"2026-09-21T13:45:31.123456Z","sequence_number":184}
    '''))
    canonical = normalize(legacy, gateway_id="gateway-002", received_at=RECEIVED_AT)
    assert json.loads(json.dumps(canonical.to_dict(), allow_nan=False)) == {
        "device_id": "sensor-001",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31.123456Z",
        "sequence_number": 184,
        "received_at": "2026-09-21T13:45:32.654321Z",
        "gateway_id": "gateway-002",
    }


@pytest.mark.parametrize("received_at", [
    RECEIVED_AT.replace(tzinfo=None),
    RECEIVED_AT.astimezone(timezone(timedelta(hours=2))),
    "2026-09-21T13:45:32Z",
])
def test_invalid_receipt_time_is_rejected_by_canonical_model(received_at):
    legacy = LegacyMeasurement("sensor-001", 21.7, 42.5, MEASURED_AT, 184)
    with pytest.raises(CanonicalMeasurementSchemaError, match="received_at must be a UTC datetime"):
        normalize(legacy, gateway_id="gateway-001", received_at=received_at)
