from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
import random

import pytest

from legacy_system.sensor import Measurement, Sensor


class FalseyRandomSource(random.Random):
    def __bool__(self) -> bool:
        return False


class FalseyClock:
    def __init__(self, timestamp: datetime) -> None:
        self.timestamp = timestamp

    def __bool__(self) -> bool:
        return False

    def __call__(self) -> datetime:
        return self.timestamp


def test_sensor_generates_valid_normal_measurements() -> None:
    sensor = Sensor("sensor-007", random.Random(42))

    measurements = [sensor.read() for _ in range(20)]

    assert all(
        15.0 <= measurement.temperature_c <= 30.0
        for measurement in measurements
    )
    assert all(
        30.0 <= measurement.humidity_pct <= 70.0
        for measurement in measurements
    )
    assert all(measurement.device_id == "sensor-007" for measurement in measurements)


def test_sensor_assigns_utc_timestamp_at_creation() -> None:
    timestamp = datetime(2026, 9, 29, 12, 34, 56, tzinfo=timezone(timedelta(hours=2)))
    sensor = Sensor("sensor-007", clock=lambda: timestamp)

    measurement = sensor.read()

    assert measurement.timestamp == datetime(
        2026, 9, 29, 10, 34, 56, tzinfo=timezone.utc
    )
    assert measurement.timestamp.tzinfo is timezone.utc


def test_sensor_increments_sequence_for_each_created_measurement() -> None:
    sensor = Sensor("sensor-007", random.Random(42))

    first = sensor.read()
    second = sensor.read()
    third = sensor.read()

    assert [first.sequence_number, second.sequence_number, third.sequence_number] == [
        0,
        1,
        2,
    ]


def test_sensor_seeded_random_generation_is_reproducible() -> None:
    timestamp = datetime(2026, 9, 29, 12, 34, 56, tzinfo=timezone.utc)
    first_sensor = Sensor("sensor-007", random.Random(42), clock=lambda: timestamp)
    second_sensor = Sensor("sensor-007", random.Random(42), clock=lambda: timestamp)

    assert [first_sensor.read() for _ in range(3)] == [
        second_sensor.read() for _ in range(3)
    ]


def test_sensor_preserves_falsey_supplied_dependencies() -> None:
    timestamp = datetime(2026, 9, 29, 12, 34, 56, tzinfo=timezone.utc)
    random_source = FalseyRandomSource(42)
    clock = FalseyClock(timestamp)
    sensor = Sensor("sensor-007", random_source=random_source, clock=clock)

    measurement = sensor.read()

    expected_random = random.Random(42)
    assert measurement.temperature_c == expected_random.uniform(15.0, 30.0)
    assert measurement.humidity_pct == expected_random.uniform(30.0, 70.0)
    assert measurement.timestamp == timestamp


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
        ("device_id", None),
        ("temperature_c", -40.1),
        ("temperature_c", 85.1),
        ("temperature_c", float("nan")),
        ("temperature_c", float("inf")),
        ("temperature_c", True),
        ("humidity_pct", -0.1),
        ("humidity_pct", 100.1),
        ("humidity_pct", float("nan")),
        ("humidity_pct", float("inf")),
        ("humidity_pct", True),
        ("sequence_number", -1),
        ("sequence_number", 1.5),
        ("sequence_number", True),
        ("timestamp", "2026-09-21T13:45:31Z"),
    ],
)
def test_measurement_rejects_invalid_domain_values(field: str, value: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        make_measurement(**{field: value})


@pytest.mark.parametrize(
    ("temperature", "humidity", "sequence"),
    [
        (-40.0, 0.0, 0),
        (85.0, 100.0, 1000000),
    ],
)
def test_measurement_accepts_valid_boundary_values(
    temperature: float, humidity: float, sequence: int
) -> None:
    measurement = make_measurement(
        temperature_c=temperature,
        humidity_pct=humidity,
        sequence_number=sequence,
    )
    assert measurement.temperature_c == temperature
    assert measurement.humidity_pct == humidity
    assert measurement.sequence_number == sequence


def test_measurement_is_immutable() -> None:
    measurement = make_measurement()
    with pytest.raises(FrozenInstanceError):
        measurement.temperature_c = 25.0  # type: ignore[misc]


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