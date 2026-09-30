"""Runtime orchestration for the Legacy Device."""

from collections.abc import Callable
import threading
import time

from legacy_system.client import GatewayClient
from legacy_system.config import Config
from legacy_system.failure import FailureInjector
from legacy_system.sensor import Sensor


class DeviceController:
    """Generate, prepare, and deliver Legacy Device measurements."""

    def __init__(
        self,
        config: Config,
        sensor: Sensor | None = None,
        failure_injector: FailureInjector | None = None,
        client: GatewayClient | None = None,
        sleeper: Callable[[float], None] = time.sleep,
        stop_event: threading.Event | None = None,
    ) -> None:
        self._config = config
        self._sensor = sensor if sensor is not None else Sensor(config.device_id)
        self._failure_injector = (
            failure_injector
            if failure_injector is not None
            else FailureInjector(
                config.failure_mode,
                config.failure_rate,
                config.failure_seed,
            )
        )
        self._client = (
            client
            if client is not None
            else GatewayClient(
                config.gateway_url,
                config.request_timeout_seconds,
                max_retries=config.max_retries,
            )
        )
        self._sleeper = sleeper
        self._stop_event = (
            stop_event if stop_event is not None else threading.Event()
        )

    def run(self) -> None:
        """Run the device loop until :meth:`stop` is called."""
        try:
            while not self._stop_event.is_set():
                measurement = self._sensor.read()
                payload = measurement.to_payload()
                outgoing = self._failure_injector.apply(payload)
                self._client.send(outgoing)
                self._sleeper(self._config.send_interval_seconds)
        finally:
            self._close_client()

    def stop(self) -> None:
        """Request that the loop stop before generating another measurement."""
        self._stop_event.set()

    def _close_client(self) -> None:
        close = getattr(self._client, "close", None)
        if callable(close):
            close()