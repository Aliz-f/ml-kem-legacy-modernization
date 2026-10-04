"""Runtime orchestration for the Legacy Device."""

from collections.abc import Callable, Mapping
import logging
import signal
import threading
from types import FrameType

from legacy_system.client import GatewayClient
from legacy_system.config import Config, FailureMode
from legacy_system.failure import FailureInjector
from legacy_system.sensor import Sensor

logger = logging.getLogger(__name__)


class DeviceController:
    """Generate, prepare, and deliver Legacy Device measurements."""

    def __init__(
        self,
        config: Config,
        sensor: Sensor | None = None,
        failure_injector: FailureInjector | None = None,
        client: GatewayClient | None = None,
        sleeper: Callable[[float], None] | None = None,
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
        self._stop_event = (
            stop_event if stop_event is not None else threading.Event()
        )
        self._sleeper = sleeper if sleeper is not None else self._stop_event.wait

    def run(self) -> None:
        """Run the device loop until :meth:`stop` is called."""
        logger.info(
            "event=device_starting component=legacy_system device_id=%s",
            self._config.device_id,
        )
        if (
            self._config.failure_mode != FailureMode.NONE
            and self._config.failure_rate > 0.0
        ):
            logger.warning(
                "event=failure_injection_enabled component=legacy_system device_id=%s mode=%s rate=%s",
                self._config.device_id,
                self._config.failure_mode.value,
                self._config.failure_rate,
            )
        previous_handlers = self._install_signal_handlers()
        try:
            logger.info(
                "event=device_ready component=legacy_system device_id=%s",
                self._config.device_id,
            )
            while not self._stop_event.is_set():
                measurement = self._sensor.read()
                logger.info(
                    "event=measurement_generated component=legacy_system device_id=%s sequence_number=%s",
                    self._config.device_id,
                    measurement.sequence_number,
                )
                payload = measurement.to_payload()
                outgoing = self._failure_injector.apply(payload)
                self._send_with_logging(outgoing, measurement.sequence_number)
                if not self._stop_event.is_set():
                    self._sleeper(self._config.send_interval_seconds)
        finally:
            self._restore_signal_handlers(previous_handlers)
            self._close_client()
            if self._stop_event.is_set():
                logger.info(
                    "event=device_shutting_down component=legacy_system device_id=%s",
                    self._config.device_id,
                )

    def _send_with_logging(
        self, payload: Mapping[str, object], sequence_number: int
    ) -> None:
        """Send payload and log success/failure outcomes."""
        try:
            result = self._client.send(payload)
        except Exception as exc:
            logger.warning(
                "event=measurement_delivery_failed component=legacy_system device_id=%s sequence_number=%s error=%s",
                self._config.device_id,
                sequence_number,
                type(exc).__name__,
            )
            return

        success = result if isinstance(result, bool) else bool(getattr(result, "success", False))
        status_code = 202 if result is True else (None if isinstance(result, bool) else getattr(result, "status_code", None))
        attempt_count = 1 if isinstance(result, bool) else getattr(result, "attempt_count", 1)
        error_category = None if result is True else (None if isinstance(result, bool) else getattr(result, "error_category", None))

        if success:
            logger.info(
                "event=measurement_delivered component=legacy_system device_id=%s sequence_number=%s status_code=%s attempt=%s",
                self._config.device_id,
                sequence_number,
                status_code,
                attempt_count,
            )
            return

        logger.warning(
            "event=measurement_delivery_failed component=legacy_system device_id=%s sequence_number=%s status_code=%s attempt=%s error_category=%s",
            self._config.device_id,
            sequence_number,
            status_code,
            attempt_count,
            error_category,
        )

    def stop(self) -> None:
        """Request that the loop stop before generating another measurement."""
        self._stop_event.set()

    def _close_client(self) -> None:
        close = getattr(self._client, "close", None)
        if callable(close):
            close()

    def _install_signal_handlers(self) -> dict[signal.Signals, object]:
        if threading.current_thread() is not threading.main_thread():
            return {}

        previous_handlers: dict[signal.Signals, object] = {}
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[signum] = signal.signal(signum, self._handle_signal)
        return previous_handlers

    def _restore_signal_handlers(
        self,
        previous_handlers: dict[signal.Signals, object],
    ) -> None:
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)

    def _handle_signal(self, _signum: int, _frame: FrameType | None) -> None:
        self.stop()
