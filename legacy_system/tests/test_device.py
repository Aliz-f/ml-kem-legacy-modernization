import threading
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
import logging
import random
import signal

import pytest

from legacy_system.config import Config, FailureMode
from legacy_system.client import GatewayClient
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


class FakeResponse:
    def __init__(self, status: int) -> None:
        self.status = status

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None


class ScriptedOpener:
    def __init__(self, statuses: list[int]) -> None:
        self._responses = [FakeResponse(status) for status in statuses]
        self.calls = 0

    def __call__(self, *_args: object, **_kwargs: object) -> FakeResponse:
        if self.calls >= len(self._responses):
            raise AssertionError("the opener was called more than expected")
        response = self._responses[self.calls]
        self.calls += 1
        return response


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


def test_client_exception_is_logged_then_loop_continues_and_closes() -> None:
    client = RaisingClient([])
    stop_event = threading.Event()
    waits: list[float] = []

    def wait_then_stop(interval: float) -> None:
        waits.append(interval)
        stop_event.set()

    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=wait_then_stop,
        stop_event=stop_event,
    )

    controller.run()

    assert len(client.events) == 1
    assert waits == [5]
    assert client.closed is True


def test_stop_during_delivery_skips_interval_wait() -> None:
    stop_event = threading.Event()

    class StoppingClient(RecordingClient):
        def send(self, payload: Mapping[str, object]) -> bool:
            result = super().send(payload)
            stop_event.set()
            return result

    client = StoppingClient([])
    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=lambda _interval: pytest.fail("shutdown must skip interval wait"),
        stop_event=stop_event,
    )

    controller.run()

    assert len(client.events) == 1
    assert client.closed is True


def test_runtime_logs_lifecycle_and_delivery_events(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO, logger="legacy_system.device")
    sensor = FakeSensor()
    client = RecordingClient([])
    stop_event = threading.Event()

    def stop_after_first_measurement(_interval: float) -> None:
        stop_event.set()

    controller = DeviceController(
        make_config(),
        sensor=sensor,
        failure_injector=RecordingFailureInjector([]),
        client=client,
        sleeper=stop_after_first_measurement,
        stop_event=stop_event,
    )

    controller.run()

    messages = [record.getMessage() for record in caplog.records]
    assert "event=device_starting component=legacy_system device_id=sensor-001" in messages
    assert "event=device_ready component=legacy_system device_id=sensor-001" in messages
    assert (
        "event=measurement_generated component=legacy_system device_id=sensor-001 sequence_number=0"
        in messages
    )
    assert (
        "event=measurement_delivered component=legacy_system device_id=sensor-001 sequence_number=0 "
        "status_code=202 attempt=1"
    ) in messages
    assert "event=device_shutting_down component=legacy_system device_id=sensor-001" in messages
    assert all(record.levelno == logging.INFO for record in caplog.records)


def test_retry_and_final_failure_logging_are_visible(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)

    stop_event = threading.Event()

    def stop_after_first_measurement(_interval: float) -> None:
        stop_event.set()

    opener = ScriptedOpener([503, 503, 503])
    client = GatewayClient(
        make_config().gateway_url,
        request_timeout_seconds=3,
        opener=opener,
        max_retries=2,
        sleeper=lambda _delay: None,
    )
    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=stop_after_first_measurement,
        stop_event=stop_event,
    )

    controller.run()

    retry_messages = [
        record.getMessage()
        for record in caplog.records
        if "event=gateway_retry" in record.getMessage()
    ]
    request_failure_messages = [
        record.getMessage()
        for record in caplog.records
        if "event=gateway_request_failed" in record.getMessage()
    ]
    delivery_failure_messages = [
        record.getMessage()
        for record in caplog.records
        if "event=measurement_delivery_failed" in record.getMessage()
    ]

    assert opener.calls == 3
    assert retry_messages == [
        "event=gateway_retry component=legacy_system device_id=None sequence_number=0 attempt=1 "
        "status_code=503 error_category=http",
        "event=gateway_retry component=legacy_system device_id=None sequence_number=0 attempt=2 "
        "status_code=503 error_category=http",
    ]
    assert request_failure_messages == [
        "event=gateway_request_failed component=legacy_system device_id=None sequence_number=0 "
        "status_code=503 attempt=3 error_category=http"
    ]
    assert delivery_failure_messages == [
        "event=measurement_delivery_failed component=legacy_system device_id=sensor-001 "
        "sequence_number=0 status_code=503 attempt=3 error_category=http"
    ]
    assert all(
        record.levelno == logging.WARNING
        for record in caplog.records
        if "event=gateway_" in record.getMessage()
        or "event=measurement_delivery_failed" in record.getMessage()
    )


@pytest.mark.parametrize("status_code", [400, 409, 422])
def test_permanent_gateway_failures_are_logged_without_retry(
    status_code: int,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.WARNING)
    opener = ScriptedOpener([status_code])
    delays: list[float] = []
    stop_event = threading.Event()

    def stop_after_first_measurement(_interval: float) -> None:
        stop_event.set()

    client = GatewayClient(
        make_config().gateway_url,
        request_timeout_seconds=3,
        opener=opener,
        max_retries=2,
        sleeper=delays.append,
    )
    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=stop_after_first_measurement,
        stop_event=stop_event,
    )

    controller.run()

    messages = [record.getMessage() for record in caplog.records]
    assert opener.calls == 1
    assert delays == []
    assert sum("event=gateway_retry" in message for message in messages) == 0
    assert messages.count(
        "event=gateway_request_failed component=legacy_system device_id=None sequence_number=0 "
        f"status_code={status_code} attempt=1 error_category=http"
    ) == 1
    assert messages.count(
        "event=measurement_delivery_failed component=legacy_system device_id=sensor-001 "
        f"sequence_number=0 status_code={status_code} attempt=1 "
        "error_category=http"
    ) == 1
    assert all(record.levelno == logging.WARNING for record in caplog.records)


def test_retry_eventual_success_logs_delivery_without_final_failure(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    opener = ScriptedOpener([503, 202])
    stop_event = threading.Event()

    def stop_after_first_measurement(_interval: float) -> None:
        stop_event.set()

    client = GatewayClient(
        make_config().gateway_url,
        request_timeout_seconds=3,
        opener=opener,
        max_retries=1,
        sleeper=lambda _delay: None,
    )
    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=stop_after_first_measurement,
        stop_event=stop_event,
    )

    controller.run()

    messages = [record.getMessage() for record in caplog.records]
    assert opener.calls == 2
    assert (
        "event=gateway_retry component=legacy_system device_id=None sequence_number=0 attempt=1 "
        "status_code=503 error_category=http"
    ) in messages
    assert not any("event=gateway_request_failed" in message for message in messages)
    assert (
        "event=measurement_delivered component=legacy_system device_id=sensor-001 sequence_number=0 "
        "status_code=202 attempt=2"
    ) in messages
    assert not any(
        "event=measurement_delivery_failed" in message for message in messages
    )


def test_sigterm_stops_during_wait_and_logs_shutdown(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    installed_handlers: dict[signal.Signals, object] = {}

    def fake_signal(signum: signal.Signals, handler: object) -> object:
        previous = installed_handlers.get(signum, signal.SIG_DFL)
        installed_handlers[signum] = handler
        return previous

    monkeypatch.setattr(signal, "signal", fake_signal)
    caplog.set_level(logging.INFO, logger="legacy_system.device")
    client = RecordingClient([])
    controller: DeviceController

    def stop_during_wait(_interval: float) -> None:
        handler = installed_handlers[signal.SIGTERM]
        assert callable(handler)
        handler(signal.SIGTERM, None)

    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=stop_during_wait,
    )

    controller.run()

    assert client.closed is True
    assert "device_shutting_down component=legacy_system device_id=sensor-001" in caplog.text


def test_sigint_stops_after_delivery_and_restores_handlers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    installed_handlers: dict[signal.Signals, object] = {}
    restored_handlers: dict[signal.Signals, object] = {}

    def fake_signal(signum: signal.Signals, handler: object) -> object:
        if signum in installed_handlers:
            restored_handlers[signum] = handler
        else:
            installed_handlers[signum] = handler
        return signal.SIG_DFL

    monkeypatch.setattr(signal, "signal", fake_signal)
    client = RecordingClient([])

    def stop_after_delivery(_interval: float) -> None:
        handler = installed_handlers[signal.SIGINT]
        assert callable(handler)
        handler(signal.SIGINT, None)

    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=stop_after_delivery,
    )

    controller.run()

    assert len(client.events) == 1
    assert client.closed is True
    assert restored_handlers == {
        signal.SIGINT: signal.SIG_DFL,
        signal.SIGTERM: signal.SIG_DFL,
    }


def test_shutdown_after_gateway_unavailable_delivery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    installed_handlers: dict[signal.Signals, object] = {}

    def fake_signal(signum: signal.Signals, handler: object) -> object:
        installed_handlers[signum] = handler
        return signal.SIG_DFL

    monkeypatch.setattr(signal, "signal", fake_signal)
    retry_delays: list[float] = []
    opener_calls = 0

    def unavailable_opener(*_args: object, **_kwargs: object) -> object:
        nonlocal opener_calls
        opener_calls += 1
        raise ConnectionError("Gateway unavailable")

    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=unavailable_opener,
        max_retries=2,
        sleeper=retry_delays.append,
    )

    def stop_after_failed_delivery(_interval: float) -> None:
        handler = installed_handlers[signal.SIGTERM]
        assert callable(handler)
        handler(signal.SIGTERM, None)

    controller = DeviceController(
        make_config(),
        sensor=FakeSensor(),
        client=client,
        sleeper=stop_after_failed_delivery,
    )

    controller.run()

    assert opener_calls == 3
    assert retry_delays == [1, 2]
