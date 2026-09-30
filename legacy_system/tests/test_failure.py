from datetime import datetime, timezone
import logging
import math

import pytest

from legacy_system.config import FailureMode
from legacy_system.failure import FailureInjector
from legacy_system.sensor import Measurement


def make_measurement(sequence_number: int = 184) -> Measurement:
    return Measurement(
        device_id="sensor-001",
        temperature_c=21.7,
        humidity_pct=42.5,
        timestamp=datetime(2026, 9, 21, 13, 45, 31, tzinfo=timezone.utc),
        sequence_number=sequence_number,
    )


def make_payload(sequence_number: int = 184) -> dict[str, object]:
    return make_measurement(sequence_number).to_payload()


def test_none_returns_independent_unchanged_payload() -> None:
    payload = make_payload()
    outgoing = FailureInjector(FailureMode.NONE, 1.0).apply(payload)

    assert outgoing == payload
    assert outgoing is not payload


@pytest.mark.parametrize(
    ("mode", "field"),
    [
        (FailureMode.INVALID_TEMPERATURE, "temperature_c"),
        (FailureMode.INVALID_HUMIDITY, "humidity_pct"),
    ],
)
def test_value_modes_mutate_only_outgoing_payload(
    mode: FailureMode, field: str
) -> None:
    payload = make_payload()
    outgoing = FailureInjector(mode, 1.0).apply(payload)

    assert outgoing[field] != payload[field]
    assert isinstance(outgoing[field], float)
    assert math.isfinite(outgoing[field])
    if mode is FailureMode.INVALID_TEMPERATURE:
        assert not -40.0 <= outgoing[field] <= 85.0
    else:
        assert not 0.0 <= outgoing[field] <= 100.0
    assert payload[field] in {21.7, 42.5}


def test_invalid_timestamp_is_malformed_and_varies_by_seed() -> None:
    first = FailureInjector(FailureMode.INVALID_TIMESTAMP, 1.0, failure_seed=1)
    second = FailureInjector(FailureMode.INVALID_TIMESTAMP, 1.0, failure_seed=2)

    first_timestamps = [
        first.apply(make_payload(sequence))["timestamp"] for sequence in range(3)
    ]
    second_timestamps = [
        second.apply(make_payload(sequence))["timestamp"] for sequence in range(3)
    ]

    assert first_timestamps != second_timestamps
    assert all(
        isinstance(timestamp, str) and timestamp.startswith("not-a-valid-timestamp-")
        for timestamp in first_timestamps + second_timestamps
    )


@pytest.mark.parametrize(
    "mode", [FailureMode.INVALID_TEMPERATURE, FailureMode.INVALID_HUMIDITY]
)
def test_value_mutations_vary_by_seed(mode: FailureMode) -> None:
    first_injector = FailureInjector(mode, 1.0, failure_seed=1)
    second_injector = FailureInjector(mode, 1.0, failure_seed=2)

    first_outputs = [
        first_injector.apply(make_payload(sequence)) for sequence in range(3)
    ]
    second_outputs = [
        second_injector.apply(make_payload(sequence)) for sequence in range(3)
    ]

    assert first_outputs != second_outputs


def test_missing_field_removes_timestamp_from_copy() -> None:
    payload = make_payload()

    outgoing = FailureInjector(FailureMode.MISSING_FIELD, 1.0).apply(payload)

    assert "timestamp" not in outgoing
    assert "timestamp" in payload


def test_duplicate_sequence_uses_previous_sequence_without_rewinding_input() -> None:
    injector = FailureInjector(FailureMode.DUPLICATE_SEQUENCE, 1.0)
    first = make_payload(40)
    second = make_payload(41)

    assert injector.apply(first) == first
    outgoing = injector.apply(second)

    assert outgoing["sequence_number"] == 40
    assert first["sequence_number"] == 40
    assert second["sequence_number"] == 41


def test_first_duplicate_sequence_leaves_payload_unchanged_without_failure_log(
    caplog: pytest.LogCaptureFixture,
) -> None:
    payload = make_payload(0)

    with caplog.at_level(logging.WARNING):
        outgoing = FailureInjector(FailureMode.DUPLICATE_SEQUENCE, 1.0).apply(payload)

    assert outgoing == payload
    assert "event=simulated_failure_injected" not in caplog.text


def test_duplicate_sequence_selection_varies_by_seed() -> None:
    first = FailureInjector(FailureMode.DUPLICATE_SEQUENCE, 1.0, failure_seed=1)
    second = FailureInjector(FailureMode.DUPLICATE_SEQUENCE, 1.0, failure_seed=2)
    for sequence in (10, 20, 30):
        payload = make_payload(sequence)
        first.apply(payload)
        second.apply(payload)

    first_output = first.apply(make_payload(40))
    second_output = second.apply(make_payload(40))

    assert first_output["sequence_number"] in {10, 20, 30}
    assert second_output["sequence_number"] in {10, 20, 30}
    assert first_output != second_output


def test_out_of_order_sequence_is_schema_valid_and_lower_than_current_sequence() -> (
    None
):
    injector = FailureInjector(FailureMode.OUT_OF_ORDER_SEQUENCE, 1.0)
    first = make_payload(0)
    second = make_payload(1)

    assert injector.apply(first) == first
    outgoing = injector.apply(second)

    assert isinstance(outgoing["sequence_number"], int)
    assert 0 <= outgoing["sequence_number"] < 1
    assert second["sequence_number"] == 1


def test_out_of_order_mutation_varies_by_seed() -> None:
    first = FailureInjector(FailureMode.OUT_OF_ORDER_SEQUENCE, 1.0, failure_seed=1)
    second = FailureInjector(FailureMode.OUT_OF_ORDER_SEQUENCE, 1.0, failure_seed=2)

    first_outputs = [
        first.apply(make_payload(sequence)) for sequence in range(100, 104)
    ]
    second_outputs = [
        second.apply(make_payload(sequence)) for sequence in range(100, 104)
    ]

    assert first_outputs != second_outputs


def test_failure_rate_zero_never_injects() -> None:
    payload = make_payload()

    outgoing = FailureInjector(FailureMode.INVALID_HUMIDITY, 0.0).apply(payload)

    assert outgoing == payload


def test_failure_rate_one_always_injects() -> None:
    payload = make_payload()

    outgoing = FailureInjector(FailureMode.INVALID_HUMIDITY, 1.0).apply(payload)

    assert outgoing["humidity_pct"] != payload["humidity_pct"]
    assert not 0.0 <= outgoing["humidity_pct"] <= 100.0


def test_random_mode_uses_only_supported_faults() -> None:
    injector = FailureInjector(FailureMode.RANDOM, 1.0, failure_seed=42)

    outputs = [injector.apply(make_payload(sequence)) for sequence in range(20)]

    for sequence, output in enumerate(outputs):
        original = make_payload(sequence)
        changed_fields = {
            field
            for field in set(output) | set(original)
            if output.get(field) != original.get(field)
        }
        assert changed_fields
        assert changed_fields <= {
            "temperature_c",
            "humidity_pct",
            "timestamp",
            "sequence_number",
        }
        if "temperature_c" in changed_fields:
            assert not -40.0 <= output["temperature_c"] <= 85.0
        if "humidity_pct" in changed_fields:
            assert not 0.0 <= output["humidity_pct"] <= 100.0
        if "timestamp" in changed_fields:
            assert "timestamp" not in output or str(output["timestamp"]).startswith(
                "not-a-valid-timestamp-"
            )
        if "sequence_number" in changed_fields:
            assert output["sequence_number"] != sequence


def test_random_mode_varies_with_seed() -> None:
    first = FailureInjector(FailureMode.RANDOM, 1.0, failure_seed=1)
    second = FailureInjector(FailureMode.RANDOM, 1.0, failure_seed=2)

    first_outputs = [first.apply(make_payload(sequence)) for sequence in range(1, 10)]
    second_outputs = [second.apply(make_payload(sequence)) for sequence in range(1, 10)]

    assert first_outputs != second_outputs


def test_seeded_random_behavior_is_reproducible() -> None:
    first = FailureInjector(FailureMode.RANDOM, 0.5, failure_seed=42)
    second = FailureInjector(FailureMode.RANDOM, 0.5, failure_seed=42)

    first_outputs = [first.apply(make_payload(sequence)) for sequence in range(10, 30)]
    second_outputs = [
        second.apply(make_payload(sequence)) for sequence in range(10, 30)
    ]

    assert first_outputs == second_outputs


def test_injection_logs_local_event_without_wire_marker(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING):
        outgoing = FailureInjector(FailureMode.INVALID_HUMIDITY, 1.0).apply(
            make_payload()
        )

    assert "event=simulated_failure_injected" in caplog.text
    assert "simulated_failure" not in outgoing


def test_skipped_injection_does_not_log_failure(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING):
        FailureInjector(FailureMode.NONE, 1.0).apply(make_payload())
        FailureInjector(FailureMode.INVALID_HUMIDITY, 0.0).apply(make_payload())

    assert "event=simulated_failure_injected" not in caplog.text


def test_measurement_remains_valid_and_unmodified() -> None:
    measurement = make_measurement()
    original_payload = measurement.to_payload()

    FailureInjector(FailureMode.INVALID_HUMIDITY, 1.0).apply(original_payload)

    assert measurement.to_payload() == original_payload
    assert measurement.humidity_pct == 42.5


def test_sequence_mutations_do_not_change_measurements() -> None:
    injector = FailureInjector(FailureMode.OUT_OF_ORDER_SEQUENCE, 1.0, failure_seed=42)
    first = make_measurement(40)
    second = make_measurement(41)

    first_outgoing = injector.apply(first.to_payload())
    second_outgoing = injector.apply(second.to_payload())

    assert first_outgoing["sequence_number"] == first.sequence_number
    assert second_outgoing["sequence_number"] < second.sequence_number
    assert first.sequence_number == 40
    assert second.sequence_number == 41


def test_invalid_payload_sequence_is_rejected() -> None:
    with pytest.raises(ValueError, match="sequence_number"):
        FailureInjector(FailureMode.NONE, 0.0).apply({"sequence_number": "1"})


def test_invalid_failure_rate_is_rejected() -> None:
    with pytest.raises(ValueError, match="failure_rate"):
        FailureInjector(FailureMode.NONE, 1.1)
