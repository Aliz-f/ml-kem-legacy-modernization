from datetime import datetime, timedelta, timezone

import pytest

from legacy_system.sensor import Measurement


def make_measurement(**overrides: object) -> Measurement:
    values: dict[str, object] = {
        "device_id": "sensor-001",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "timestamp": datetime(2026, 9, 21, 13, 45, 31, tzinfo=timezone.utc),
        "sequence_number": 184,
    }
    values.update(overrides)
    return Measurement(**values)  # type: ignore[arg-type]


def test_measurement_accepts_valid_internal_state() -> None:
    measurement = make_measurement()

    assert measurement.device_id == "sensor-001"
    assert measurement.temperature_c == 21.7
    assert measurement.humidity_pct == 42.5
    assert measurement.sequence_number == 184


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("device_id", ""),
        ("device_id", "   "),
        ("temperature_c", -40.1),
        ("temperature_c", 85.1),
        ("humidity_pct", -0.1),
        ("humidity_pct", 100.1),
        ("sequence_number", -1),
    ],
)
def test_measurement_rejects_invalid_domain_values(field: str, value: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        make_measurement(**{field: value})


def test_measurement_rejects_naive_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        make_measurement(timestamp=datetime(2026, 9, 21, 13, 45, 31))


def test_payload_has_exact_field_names_and_serialized_values() -> None:
    measurement = make_measurement()

    assert measurement.to_payload() == {
        "device_id": "sensor-001",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "timestamp": "2026-09-21T13:45:31Z",
        "sequence_number": 184,
    }


def test_payload_converts_non_utc_timestamp_to_utc() -> None:
    measurement = make_measurement(
        timestamp=datetime(
            2026, 9, 21, 13, 45, 31, tzinfo=timezone(timedelta(hours=2))
        )
    )

    assert measurement.to_payload()["timestamp"] == "2026-09-21T11:45:31Z"


def test_payload_preserves_numeric_types() -> None:
    measurement = make_measurement(temperature_c=21, humidity_pct=42)

    payload = measurement.to_payload()

    assert payload["temperature_c"] == 21
    assert type(payload["temperature_c"]) is int
    assert payload["humidity_pct"] == 42
    assert type(payload["humidity_pct"]) is int
    assert type(payload["sequence_number"]) is int


def test_payload_is_independent_from_model_and_other_payloads() -> None:
    measurement = make_measurement()
    first_payload = measurement.to_payload()
    first_payload["device_id"] = "changed"
    first_payload["sequence_number"] = 999

    second_payload = measurement.to_payload()

    assert second_payload["device_id"] == "sensor-001"
    assert second_payload["sequence_number"] == 184