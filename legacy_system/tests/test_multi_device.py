"""M1-15 multiple device simulation check test suite.

Verifies that the Legacy Device simulator supports concurrent/multiple device
instances (e.g. sensor-001, sensor-002, sensor-003) using the exact same codebase
and image with zero source modifications, driven purely by configuration.
"""

from typing import Any
from unittest.mock import MagicMock

import random
import threading

from legacy_system.client import GatewayResult
from legacy_system.config import FailureMode, load_config
from legacy_system.device import DeviceController
from legacy_system.failure import FailureInjector
from legacy_system.sensor import Sensor


def test_multiple_devices_configured_via_environment_without_code_changes() -> None:
    """Distinct device instances can be instantiated from independent environments."""
    env_1 = {
        "DEVICE_ID": "sensor-001",
        "GATEWAY_URL": "http://edge-gateway:8000",
        "SEND_INTERVAL_SECONDS": "5",
        "REQUEST_TIMEOUT_SECONDS": "3",
        "MAX_RETRIES": "2",
        "FAILURE_MODE": "none",
        "FAILURE_RATE": "0.0",
        "LOG_LEVEL": "INFO",
    }
    env_2 = {
        "DEVICE_ID": "sensor-002",
        "GATEWAY_URL": "http://edge-gateway:8000",
        "SEND_INTERVAL_SECONDS": "10",
        "REQUEST_TIMEOUT_SECONDS": "4",
        "MAX_RETRIES": "3",
        "FAILURE_MODE": "invalid_temperature",
        "FAILURE_RATE": "0.25",
        "FAILURE_SEED": "42",
        "LOG_LEVEL": "DEBUG",
    }
    env_3 = {
        "DEVICE_ID": "sensor-003",
        "GATEWAY_URL": "http://edge-gateway:8000",
        "SEND_INTERVAL_SECONDS": "15",
        "REQUEST_TIMEOUT_SECONDS": "5",
        "MAX_RETRIES": "1",
        "FAILURE_MODE": "duplicate_sequence",
        "FAILURE_RATE": "0.5",
        "FAILURE_SEED": "99",
        "LOG_LEVEL": "WARNING",
    }

    config_1 = load_config(environ=env_1)
    config_2 = load_config(environ=env_2)
    config_3 = load_config(environ=env_3)

    assert config_1.device_id == "sensor-001"
    assert config_1.send_interval_seconds == 5
    assert config_1.failure_mode == FailureMode.NONE

    assert config_2.device_id == "sensor-002"
    assert config_2.send_interval_seconds == 10
    assert config_2.failure_mode == FailureMode.INVALID_TEMPERATURE
    assert config_2.failure_seed == 42

    assert config_3.device_id == "sensor-003"
    assert config_3.send_interval_seconds == 15
    assert config_3.failure_mode == FailureMode.DUPLICATE_SEQUENCE
    assert config_3.failure_seed == 99


def test_multiple_sensor_instances_maintain_independent_monotonic_sequences() -> None:
    """Each sensor simulator advances its sequence counter independently."""
    sensor_a = Sensor("sensor-001", random_source=random.Random(10))
    sensor_b = Sensor("sensor-002", random_source=random.Random(20))

    # Sensor A produces 4 measurements: 0, 1, 2, 3
    measurements_a = [sensor_a.read() for _ in range(4)]
    assert [m.sequence_number for m in measurements_a] == [0, 1, 2, 3]
    assert all(m.device_id == "sensor-001" for m in measurements_a)

    # Sensor B produces 2 measurements: 0, 1 (independent from sensor A)
    measurements_b = [sensor_b.read() for _ in range(2)]
    assert [m.sequence_number for m in measurements_b] == [0, 1]
    assert all(m.device_id == "sensor-002" for m in measurements_b)

    # Subsequent reads continue from each sensor's independent counter
    next_a = sensor_a.read()
    next_b = sensor_b.read()
    assert next_a.sequence_number == 4
    assert next_a.device_id == "sensor-001"
    assert next_b.sequence_number == 2
    assert next_b.device_id == "sensor-002"


def test_multiple_failure_injectors_operate_independently() -> None:
    """Fault injectors bound to different devices do not cross-contaminate."""
    injector_none = FailureInjector(FailureMode.NONE, failure_rate=0.0)
    injector_temp = FailureInjector(FailureMode.INVALID_TEMPERATURE, failure_rate=1.0)
    injector_field = FailureInjector(FailureMode.MISSING_FIELD, failure_rate=1.0)

    payload_a = {
        "device_id": "sensor-001",
        "temperature_c": 21.5,
        "humidity_pct": 45.0,
        "timestamp": "2026-09-21T12:00:00Z",
        "sequence_number": 0,
    }
    payload_b = {
        "device_id": "sensor-002",
        "temperature_c": 22.0,
        "humidity_pct": 50.0,
        "timestamp": "2026-09-21T12:00:01Z",
        "sequence_number": 0,
    }
    payload_c = {
        "device_id": "sensor-003",
        "temperature_c": 23.0,
        "humidity_pct": 55.0,
        "timestamp": "2026-09-21T12:00:02Z",
        "sequence_number": 0,
    }

    out_a = injector_none.apply(payload_a)
    out_b = injector_temp.apply(payload_b)
    out_c = injector_field.apply(payload_c)

    # A remains unmodified
    assert out_a["temperature_c"] == 21.5
    assert out_a["device_id"] == "sensor-001"
    assert "timestamp" in out_a

    # B has invalid temperature outside [-40.0, 85.0]
    assert out_b["temperature_c"] < -40.0 or out_b["temperature_c"] > 85.0
    assert out_b["device_id"] == "sensor-002"
    assert "timestamp" in out_b

    # C has missing timestamp field
    assert "timestamp" not in out_c
    assert out_c["device_id"] == "sensor-003"
    assert out_c["temperature_c"] == 23.0


def test_multiple_device_controllers_deliver_independently_to_gateway_interface() -> None:
    """Multiple DeviceController runtimes deliver independent streams to the Gateway."""
    delivered_payloads: list[dict[str, Any]] = []

    mock_client = MagicMock()
    mock_client.send.side_effect = lambda payload: (
        delivered_payloads.append(dict(payload)),
        GatewayResult(
            success=True,
            status_code=202,
            attempt_count=1,
            error_category=None,
            retryable=False,
        ),
    )[1]

    env_a = {
        "DEVICE_ID": "sensor-001",
        "GATEWAY_URL": "http://edge-gateway:8000",
        "SEND_INTERVAL_SECONDS": "5",
        "REQUEST_TIMEOUT_SECONDS": "3",
        "MAX_RETRIES": "2",
        "FAILURE_MODE": "none",
        "FAILURE_RATE": "0.0",
        "LOG_LEVEL": "INFO",
    }
    env_b = {
        "DEVICE_ID": "sensor-002",
        "GATEWAY_URL": "http://edge-gateway:8000",
        "SEND_INTERVAL_SECONDS": "5",
        "REQUEST_TIMEOUT_SECONDS": "3",
        "MAX_RETRIES": "2",
        "FAILURE_MODE": "none",
        "FAILURE_RATE": "0.0",
        "LOG_LEVEL": "INFO",
    }

    config_a = load_config(environ=env_a)
    config_b = load_config(environ=env_b)

    # Controller A stops after 2 sends
    a_sends = 0
    stop_event_a = threading.Event()

    def sleeper_a(interval: float) -> None:
        nonlocal a_sends
        a_sends += 1
        if a_sends >= 2:
            stop_event_a.set()

    # Controller B stops after 2 sends
    b_sends = 0
    stop_event_b = threading.Event()

    def sleeper_b(interval: float) -> None:
        nonlocal b_sends
        b_sends += 1
        if b_sends >= 2:
            stop_event_b.set()

    controller_a = DeviceController(
        config_a, client=mock_client, sleeper=sleeper_a, stop_event=stop_event_a
    )
    controller_b = DeviceController(
        config_b, client=mock_client, sleeper=sleeper_b, stop_event=stop_event_b
    )

    controller_a.run()
    controller_b.run()

    assert len(delivered_payloads) == 4

    payloads_a = [p for p in delivered_payloads if p["device_id"] == "sensor-001"]
    assert [p["sequence_number"] for p in payloads_a] == [0, 1]

    payloads_b = [p for p in delivered_payloads if p["device_id"] == "sensor-002"]
    assert [p["sequence_number"] for p in payloads_b] == [0, 1]


def test_multiple_device_controllers_have_independent_lifecycle_state() -> None:
    """Stopping one DeviceController does not affect another controller's running state."""
    config_a = load_config(
        environ={
            "DEVICE_ID": "sensor-001",
            "GATEWAY_URL": "http://edge-gateway:8000",
            "SEND_INTERVAL_SECONDS": "5",
            "REQUEST_TIMEOUT_SECONDS": "3",
            "MAX_RETRIES": "2",
        }
    )
    config_b = load_config(
        environ={
            "DEVICE_ID": "sensor-002",
            "GATEWAY_URL": "http://edge-gateway:8000",
            "SEND_INTERVAL_SECONDS": "5",
            "REQUEST_TIMEOUT_SECONDS": "3",
            "MAX_RETRIES": "2",
        }
    )

    controller_a = DeviceController(config_a, client=MagicMock())
    controller_b = DeviceController(config_b, client=MagicMock())

    assert not controller_a._stop_event.is_set()
    assert not controller_b._stop_event.is_set()

    # Stop controller A
    controller_a.stop()
    assert controller_a._stop_event.is_set()
    assert not controller_b._stop_event.is_set()

    # Stop controller B
    controller_b.stop()
    assert controller_b._stop_event.is_set()
