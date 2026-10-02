"""Legacy application pipeline, independent of Cloud retry and crypto internals."""

from collections.abc import Awaitable, Callable
from contextlib import nullcontext
from datetime import datetime

from edge_gateway.application_log import log_application
from edge_gateway.correlation import create_request_id
from edge_gateway.errors import GatewayError, GatewayErrorCode
from edge_gateway.failure.runtime import ApplicationFailures
from edge_gateway.models import CanonicalMeasurement, LegacyMeasurement
from edge_gateway.normalization import normalize
from edge_gateway.sequence import SequenceTracker
from edge_gateway.transport import CloudDeliveryError, CloudTransport


ProcessingHook = Callable[[CanonicalMeasurement, str], Awaitable[None]]


class UnavailableBaseline:
    """Fail closed until the M2-13 baseline client is supplied at composition."""

    async def send(self, **measurement: object) -> object:
        raise GatewayError(GatewayErrorCode.CLOUD_UNAVAILABLE)


class MeasurementProcessor:
    """One processor and sequence tracker per application/process.

    Input must already have passed schema and domain validation. Delivery never
    rolls sequence state back; the hook runs after normalization and correlation.
    Transports own bounded retries and return an acceptance with status/record_id
    only after Cloud confirmation, or raise a classified error.
    """

    def __init__(
        self, *, gateway_id: str, dispatch: CloudTransport | None,
        processing_hook: ProcessingHook | None = None,
        failures: ApplicationFailures | None = None,
    ) -> None:
        self._failures = failures
        self._gateway_id = gateway_id
        self._dispatch = dispatch
        self._processing_hook = processing_hook
        self._sequences = SequenceTracker()

    async def process(self, measurement: LegacyMeasurement, *, received_at: datetime) -> None:
        self._sequences.check_and_update(measurement.device_id, measurement.sequence_number)
        canonical = normalize(measurement, gateway_id=self._gateway_id, received_at=received_at)
        request_id = create_request_id()
        log_application(
            "canonical_measurement_created",
            request_id=request_id,
            device_id=canonical.device_id,
            sequence_number=canonical.sequence_number,
            gateway_id=canonical.gateway_id,
        )
        scope = self._failures.request(request_id) if self._failures else nullcontext()
        async with scope:
            if self._processing_hook is not None:
                await self._processing_hook(canonical, request_id)
            if self._dispatch is None:
                raise GatewayError(GatewayErrorCode.CLOUD_UNAVAILABLE)
            fields = canonical.to_dict()
            # Dispatch supplies the configured Gateway ID; correlation stays separate.
            fields.pop("gateway_id")
            try:
                result = await self._dispatch.send(request_id=request_id, **fields)
            except (CloudDeliveryError, TimeoutError, ConnectionError):
                raise GatewayError(GatewayErrorCode.CLOUD_UNAVAILABLE) from None
            if (
                getattr(result, "status", None) not in ("accepted", "already_accepted")
                or not isinstance(getattr(result, "record_id", None), str)
                or not result.record_id.strip()
            ):
                raise GatewayError(GatewayErrorCode.CLOUD_UNAVAILABLE)
