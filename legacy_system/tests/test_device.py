import threading
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
import random

import pytest

from legacy_system.config import Config, FailureMode
from legacy_system.device import DeviceController
from legacy_system.sensor import Sensor


@dataclass
class FakeMeasurement:
    sequence_number: int
    events: list[tuple[str, object]] | None = None

    def to_payload(self) -> dict[str, object]:
        if self.events is not None:
            self.events.append(("serialize", self.sequence_number))
        return {"sequence_number": self.sequence_number}


class FakeSensor:
    def __init__(self, events: list[tuple[str, object]] | None = None) -> None:
        self.read_count = 0
        self.events = events

    def read(self) -> FakeMeasurement:
        if self.events is not None:
            self.events.append(("read", self.read_count))
        measurement = FakeMeasurement(self.read_count)
        measurement.events = self.events
        self.read_count += 1
        return measurement


class RecordingFailureInjector:
    def __init__(self, events: list[tuple[str, object]]) -> None:
        self.events = events

    def apply(self, payload: Mapping[str, object]) -> dict[str, object]:
        self.events.append(("inject", dict(payload)))
        return {**payload, "prepared": True}


class RecordingClient:
    def __init__(self, events: list[tuple[str, object]]) -> None:
        self.events = events
        self.results: list[bool] = []
        self.closed = False

    def send(self, payload: Mapping[str, object]) -> bool:
        self.events.append(("send", dict(payload)))
        return self.results.pop(0) if self.results else True

    def close(self) -> None:
        self.closed = True


class FalseySensor(FakeSensor):
    def __bool__(self) -> bool:
        return False


class FalseyFailureInjector(RecordingFailureInjector):
    def __bool__(self) -> bool:
        return False


class FalseyClient(RecordingClient):
    def __bool__(self) -> bool:
        return False


class FalseyEvent(threading.Event):
    def __bool__(self) -> bool:
        return False


class RaisingClient(RecordingClient):
    def send(self, payload: Mapping[str, object]) -> bool:
        super().send(payload)
        raise RuntimeError("delivery failed")


def make_config() -> Config:
    return Config(
        device_id="sensor-001",
        gateway_url="http://gateway.example.test",
        send_interval_seconds=5,
        request_timeout_seconds=3,
        max_retries=2,
        failure_mode=FailureMode.NONE,
        failure_rate=0.0,
        failure_seed=None,
        log_level="INFO",
    )


def test_runtime_pipeline_serializes_before_failure_injection_and_sends() -> None:
    events: list[tuple[str, object]] = []
    sensor = FakeSensor(events)
    client = RecordingClient(events)
    stop_event = threading.Event()

    def stop_after_first_wait(interval: float) -> None:
        events.append(("wait", interval))
        stop_event.set()

    controller = DeviceController(
        make_config(),
        sensor=sensor,
        failure_injector=RecordingFailureInjector(events),
        client=client,
        sleeper=stop_after_first_wait,
        stop_event=stop_event,
    )

    controller.run()

    assert events == [
        ("read", 0),
        ("serialize", 0),
        ("inject", {"sequence_number": 0}),
        ("send", {"sequence_number": 0, "prepared": True}),
        ("wait", 5),
    ]
    assert client.closed is True


def test_delivery_failure_does_not_stop_loop_or_roll_back_sequence() -> None:
    sensor = Sensor(
        "sensor-001",
        random_source=random.Random(7),
        clock=lambda: datetime(2026, 9, 30, tzinfo=timezone.utc),
    )
    client = RecordingClient([])
    client.results = [False, False]
    stop_event = threading.Event()
    waits: list[float] = []

    def wait_and_stop(interval: float) -> None:
        waits.append(interval)
        if len(waits) == 2:
            stop_event.set()

    controller = DeviceController(
        make_config(),
        sensor=sensor,
        failure_injector=RecordingFailureInjector([]),
        client=client,
        sleeper=wait_and_stop,
        stop_event=stop_event,
    )

    controller.run()

    assert [payload["sequence_number"] for _, payload in client.events] == [0, 1]
    assert waits == [5, 5]
    assert client.closed is True


def test_stop_prevents_work_and_closes_client() -> None:
    sensor = FakeSensor()
    client = RecordingClient([])
    controller = DeviceController(
        make_config(),
        sensor=sensor,
        client=client,
        stop_event=threading.Event(),
    )

    controller.stop()
    controller.run()

    assert sensor.read_count == 0
    assert client.closed is True


def test_falsey_injected_dependencies_are_preserved() -> None:
    events: list[tuple[str, object]] = []
    sensor = FalseySensor(events)
    failure_injector = FalseyFailureInjector(events)
    client = FalseyClient(events)
    stop_event = FalseyEvent()

    controller = DeviceController(
        make_config(),
        sensor=sensor,
        failure_injector=failure_injector,
        client=client,
        sleeper=lambda _interval: stop_event.set(),
        stop_event=stop_event,
    )

    controller.run()

    assert sensor.read_count == 1
    assert events == [
        ("read", 0),
        ("serialize", 0),
        ("inject", {"sequence_number": 0}),
        ("send", {"sequence_number": 0, "prepared": True}),
    ]
    assert client.closed is True


def test_client_is_closed_when_send_raises() -> None:
    client = RaisingClient([])
    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=lambda _interval: pytest.fail("sleep should not be called"),
    )

    with pytest.raises(RuntimeError, match="delivery failed"):
        controller.run()

    assert client.closed is True