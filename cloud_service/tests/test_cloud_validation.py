"""M4-04 application validation, independently of HTTP and persistence."""

import copy
import traceback

import pytest

from cloud_service.validation import MeasurementValidationError, validate_measurement


@pytest.fixture
def payload():
    return {
        "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z", "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218Z", "gateway_id": "gateway-001",
    }


def test_valid_baseline_and_secure_measurement_preserve_input(payload):
    original = copy.deepcopy(payload)
    baseline = validate_measurement(payload)
    secure = validate_measurement(payload, expected_gateway_id="gateway-001")
    assert baseline == secure
    assert secure.temperature_c == payload["temperature_c"]
    assert secure.humidity_pct == payload["humidity_pct"]
    assert secure.sequence_number == payload["sequence_number"]
    assert secure.device_id == payload["device_id"]
    assert secure.gateway_id == payload["gateway_id"]
    assert payload == original


@pytest.mark.parametrize("temperature", [-40, 85])
@pytest.mark.parametrize("humidity", [0, 100])
@pytest.mark.parametrize("sequence", [0, 2**63 - 1])
def test_inclusive_domain_boundaries(payload, temperature, humidity, sequence):
    payload.update(temperature_c=temperature, humidity_pct=humidity, sequence_number=sequence)
    result = validate_measurement(payload)
    assert result.temperature_c == temperature
    assert result.humidity_pct == humidity
    assert result.sequence_number == sequence


@pytest.mark.parametrize(("field", "value"), [
    ("temperature_c", -40.001), ("temperature_c", 85.001),
    ("humidity_pct", -0.001), ("humidity_pct", 100.001),
    ("sequence_number", -1), ("device_id", ""), ("device_id", " \t"),
    ("sequence_number", 2**63), ("sequence_number", 10**100),
    ("gateway_id", ""), ("gateway_id", "\n "),
    ("temperature_c", float("nan")), ("humidity_pct", float("inf")),
    ("sequence_number", True), ("temperature_c", "21.7"),
])
def test_invalid_domains_and_schema(payload, field, value):
    payload[field] = value
    with pytest.raises(MeasurementValidationError, match=field):
        validate_measurement(payload)


@pytest.mark.parametrize("field", ["measured_at", "received_at"])
@pytest.mark.parametrize("value", ["bad", "2026-09-21T13:45:31",
    "2026-09-21T13:45:31+03:00", "2026-02-30T13:45:31Z", None])
def test_invalid_timestamps_through_validator(payload, field, value):
    payload[field] = value
    with pytest.raises(MeasurementValidationError, match=field):
        validate_measurement(payload)


@pytest.mark.parametrize("expected", ["other-gateway", "GATEWAY-001", " gateway-001"])
def test_gateway_identity_requires_exact_match(payload, expected):
    with pytest.raises(MeasurementValidationError, match="verified Gateway identity"):
        validate_measurement(payload, expected_gateway_id=expected)


@pytest.mark.parametrize("expected", ["", " ", 1, False])
def test_invalid_trusted_identity_is_not_ignored(payload, expected):
    with pytest.raises(MeasurementValidationError, match="expected_gateway_id"):
        validate_measurement(payload, expected_gateway_id=expected)


def test_missing_fields_and_nonobjects_use_validation_error(payload):
    del payload["device_id"]
    for value in (payload, None, [], "{}"):
        with pytest.raises(MeasurementValidationError):
            validate_measurement(value)


def test_validation_does_not_normalize_identifiers(payload):
    payload["device_id"] = " sensor-001 "
    assert validate_measurement(payload).device_id == " sensor-001 "


def test_errors_and_logs_do_not_echo_payload(payload, caplog):
    marker = "private-payload-marker"
    payload["measured_at"] = marker
    with pytest.raises(MeasurementValidationError) as error:
        validate_measurement(payload)
    assert marker not in "".join(traceback.format_exception(error.value))
    assert caplog.text == ""
