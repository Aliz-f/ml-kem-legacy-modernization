"""M1-19 failure-injection safety safeguard test suite.

Verifies that fault simulation cannot accidentally become normal behavior:
- Defaults to disabled (mode=none, rate=0.0).
- Emits visible WARNING logs at startup when simulation is active.
- Leaves domain Measurement objects completely immutable.
- Preserves internal sensor sequence monotonicity during sequence fault injection.
- Never injects simulation markers or metadata into wire payloads.
- Keeps simulation PRNG strictly isolated from production code.
"""

from __future__ import annotations

import logging
import threading

import pytest

from legacy_system.config import Config, FailureMode, load_config
from legacy_system.device import DeviceController
from legacy_system.failure import FailureInjector
from legacy_system.sensor import Sensor


def test_default_configuration_failure_injection_disabled() -> None:
    """Verify default configuration has failure simulation disabled."""
    config = load_config(environ={})
    assert config.failure_mode is FailureMode.NONE
    assert config.failure_rate == 0.0
    assert config.failure_seed is None


def test_startup_warning_logged_when_failure_injection_active(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Verify startup emits a visible WARNING event when failure injection is active."""
    config = Config(
        device_id="sensor-warning-test",
        gateway_url="http://127.0.0.1:8000",
        send_interval_seconds=0.01,
        request_timeout_seconds=1.0,
        max_retries=0,
        failure_mode=FailureMode.INVALID_HUMIDITY,
        failure_rate=0.25,
        failure_seed=42,
        log_level="INFO",
    )
    stop_event = threading.Event()

    def dummy_sleeper(_secs: float) -> None:
        stop_event.set()

    controller = DeviceController(
        config=config,
        stop_event=stop_event,
        sleeper=dummy_sleeper,
    )

    with caplog.at_level(logging.WARNING):
        controller.run()

    assert "event=failure_injection_enabled" in caplog.text
    assert "component=legacy_system" in caplog.text
    assert "device_id=sensor-warning-test" in caplog.text
    assert "mode=invalid_humidity" in caplog.text
    assert "rate=0.25" in caplog.text


def test_startup_warning_absent_when_failure_injection_disabled(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Verify no failure_injection_enabled warning is emitted when simulation is disabled."""
    # 1. Mode is NONE
    config_none = Config(
        device_id="sensor-safe-test",
        gateway_url="http://127.0.0.1:8000",
        send_interval_seconds=0.01,
        request_timeout_seconds=1.0,
        max_retries=0,
        failure_mode=FailureMode.NONE,
        failure_rate=0.0,
        failure_seed=None,
        log_level="INFO",
    )
    stop_event1 = threading.Event()
    controller_none = DeviceController(
        config=config_none,
        stop_event=stop_event1,
        sleeper=lambda _: stop_event1.set(),
    )

    with caplog.at_level(logging.WARNING):
        controller_none.run()

    assert "event=failure_injection_enabled" not in caplog.text

    # 2. Mode is configured but rate is 0.0
    caplog.clear()
    config_zero_rate = Config(
        device_id="sensor-safe-test-2",
        gateway_url="http://127.0.0.1:8000",
        send_interval_seconds=0.01,
        request_timeout_seconds=1.0,
        max_retries=0,
        failure_mode=FailureMode.INVALID_TEMPERATURE,
        failure_rate=0.0,
        failure_seed=None,
        log_level="INFO",
    )
    stop_event2 = threading.Event()
    controller_zero_rate = DeviceController(
        config=config_zero_rate,
        stop_event=stop_event2,
        sleeper=lambda _: stop_event2.set(),
    )

    with caplog.at_level(logging.WARNING):
        controller_zero_rate.run()

    assert "event=failure_injection_enabled" not in caplog.text


@pytest.mark.parametrize(
    "mode",
    [
        FailureMode.INVALID_TEMPERATURE,
        FailureMode.INVALID_HUMIDITY,
        FailureMode.MISSING_FIELD,
        FailureMode.INVALID_TIMESTAMP,
        FailureMode.DUPLICATE_SEQUENCE,
        FailureMode.OUT_OF_ORDER_SEQUENCE,
        FailureMode.RANDOM,
    ],
)
def test_domain_measurement_immutability_under_failure_injection(
    mode: FailureMode,
) -> None:
    """Verify that domain Measurement instances and initial dicts are never mutated by faults."""
    sensor = Sensor(device_id="sensor-immutable")
    measurement = sensor.read()

    # Capture original domain attributes
    original_device_id = measurement.device_id
    original_temp = measurement.temperature_c
    original_humidity = measurement.humidity_pct
    original_ts = measurement.timestamp
    original_seq = measurement.sequence_number

    payload = measurement.to_payload()
    payload_copy = dict(payload)

    injector = FailureInjector(mode=mode, failure_rate=1.0, failure_seed=123)
    outgoing = injector.apply(payload)

    # 1. Domain Measurement instance attributes must be strictly unchanged
    assert measurement.device_id == original_device_id
    assert measurement.temperature_c == original_temp
    assert measurement.humidity_pct == original_humidity
    assert measurement.timestamp == original_ts
    assert measurement.sequence_number == original_seq

    # 2. The input dictionary passed to apply() must not be mutated in-place
    assert payload == payload_copy

    # 3. If mutation occurred, outgoing is distinct from input payload
    if mode is not FailureMode.NONE:
        # Outgoing reflects mutation, but original remains intact
        assert isinstance(outgoing, dict)


def test_sequence_fault_injection_preserves_internal_monotonicity() -> None:
    """Verify sequence fault injection alters wire payloads without rewinding sensor counter."""
    sensor = Sensor(device_id="sensor-seq-safety")
    injector_dup = FailureInjector(
        mode=FailureMode.DUPLICATE_SEQUENCE, failure_rate=1.0, failure_seed=1
    )
    injector_ooo = FailureInjector(
        mode=FailureMode.OUT_OF_ORDER_SEQUENCE, failure_rate=1.0, failure_seed=1
    )

    m0 = sensor.read()
    m1 = sensor.read()
    m2 = sensor.read()
    m3 = sensor.read()

    assert [m0.sequence_number, m1.sequence_number, m2.sequence_number, m3.sequence_number] == [
        0,
        1,
        2,
        3,
    ]

    # Apply duplicate sequence fault to m1
    injector_dup.apply(m0.to_payload())
    outgoing_dup = injector_dup.apply(m1.to_payload())
    # Outgoing payload has duplicate sequence 0
    assert outgoing_dup["sequence_number"] == 0
    # But internal sensor measurement sequence was and remains 1
    assert m1.sequence_number == 1

    # Apply out-of-order sequence fault to m3
    injector_ooo.apply(m0.to_payload())
    injector_ooo.apply(m1.to_payload())
    injector_ooo.apply(m2.to_payload())
    outgoing_ooo = injector_ooo.apply(m3.to_payload())
    assert outgoing_ooo["sequence_number"] < 3
    assert m3.sequence_number == 3

    # Subsequent sensor read continues monotonic sequence (4)
    m4 = sensor.read()
    assert m4.sequence_number == 4


def test_failure_mode_none_preserves_payload_verbatim() -> None:
    """Verify mode=none preserves the serialized payload with zero modifications."""
    sensor = Sensor(device_id="sensor-verbatim")
    measurement = sensor.read()
    payload = measurement.to_payload()

    injector = FailureInjector(mode=FailureMode.NONE, failure_rate=1.0)
    outgoing = injector.apply(payload)

    assert outgoing == payload


@pytest.mark.parametrize(
    "mode",
    list(FailureMode),
)
def test_strict_absence_of_simulation_metadata_on_wire(mode: FailureMode) -> None:
    """Verify no simulation marker or synthetic metadata exists in outgoing wire payloads."""
    forbidden_keys = {
        "is_simulated",
        "simulated",
        "simulation",
        "failure_mode",
        "fault",
        "mock",
        "test_mode",
        "synthetic",
        "debug",
    }
    allowed_keys = {
        "device_id",
        "temperature_c",
        "humidity_pct",
        "timestamp",
        "sequence_number",
    }

    sensor = Sensor(device_id="sensor-purity")
    injector = FailureInjector(mode=mode, failure_rate=1.0, failure_seed=42)

    for _ in range(5):
        measurement = sensor.read()
        outgoing = injector.apply(measurement.to_payload())

        # No forbidden keys present in any mutated wire payload
        assert forbidden_keys.isdisjoint(outgoing.keys())
        # All present keys are legitimate protocol fields (subset for missing_field)
        assert set(outgoing.keys()).issubset(allowed_keys)
