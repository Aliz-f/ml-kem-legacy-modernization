"""Execute local application faults without altering measurement payloads."""

import asyncio
from contextlib import asynccontextmanager
from contextvars import ContextVar
import logging
from io import BytesIO
from urllib.error import HTTPError

from edge_gateway.config import GatewayConfig
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.errors import GatewayError, GatewayErrorCode
from edge_gateway.failure.injector import FailureInjector

logger = logging.getLogger(__name__)


class ApplicationFailures:
    """One selector per app; one decision after each valid sequence acceptance."""

    def __init__(self, config: GatewayConfig, metrics: PqcMetrics) -> None:
        self._injector = FailureInjector.from_config(config, announce=False)
        self._metrics = metrics
        self._delay = config.failure_delay_seconds
        self._selected: ContextVar[tuple[str | None, str]] = ContextVar(
            "gateway_application_fault", default=(None, ""),
        )

    def log_enabled(self) -> None:
        self._injector.log_enabled()

    @asynccontextmanager
    async def request(self, request_id: str):
        mode = self._injector.select()
        if mode == "processing_error":
            self._record(mode, request_id)
            raise GatewayError(GatewayErrorCode.INTERNAL_ERROR)
        if mode == "drop_message":
            self._record(mode, request_id)
            raise GatewayError(GatewayErrorCode.CLOUD_UNAVAILABLE)
        if mode == "processing_delay":
            self._record(mode, request_id)
            await asyncio.sleep(self._delay)
        token = self._selected.set((mode, request_id))
        try:
            yield
        finally:
            self._selected.reset(token)

    def before_cloud_attempt(self, request_id: str) -> None:
        """Run inside the existing retry loop, before a measurement HTTP call.

        asyncio.to_thread copies this request context to the delivery worker.
        Never reselect on retries or use this hook on session/key endpoints.
        """
        mode, selected_id = self._selected.get()
        if request_id != selected_id:
            return
        if mode == "cloud_timeout":
            self._record(mode, request_id)
            raise TimeoutError("Injected Cloud timeout")
        if mode == "cloud_unavailable":
            self._record(mode, request_id)
            raise HTTPError("", 503, "Injected Cloud unavailability", {}, BytesIO(b""))

    def _record(self, mode: str, request_id: str) -> None:
        self._metrics.record_injected(mode)
        logger.warning(
            "event=failure_injected failure_type=%s request_id=%s", mode, request_id,
        )
