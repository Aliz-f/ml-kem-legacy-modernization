"""Security-mode dispatch for one Gateway measurement.

``SECURITY_MODE=classical`` forwards to the injected baseline transport.
``SECURITY_MODE=mlkem`` uses only the secure transport. ``PQC_FAILURE_POLICY``
is ``fail_closed``: a secure failure is logged, counted, and returned. It does
not send the measurement to the baseline endpoint. Changing mode is an
operator configuration change, not a reaction to a failed request.

The baseline HTTP client and the Legacy route stay with Member 2. This module
only chooses which already-built transport handles the measurement.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

from edge_gateway.config import GatewayConfig
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.secure_transport import SecureAcceptance, SecureTransport, SecureTransportError
from edge_gateway.crypto.security_log import log_security


class BaselineTransport(Protocol):
    """Member 2's plaintext Cloud client. This module does not implement it."""

    async def send(
        self,
        *,
        request_id: str,
        gateway_id: str,
        device_id: str,
        temperature_c: float,
        humidity_pct: float,
        measured_at: str,
        sequence_number: int,
        received_at: str,
    ) -> object:
        """Deliver one canonical measurement in baseline mode."""


@dataclass(slots=True)
class DispatchMetrics:
    """Count secure deliveries that failed closed.

    Exporting the counter belongs to later observability work.
    """

    secure_failures_total: int = 0


class CloudDispatch:
    """Send one measurement through the transport selected at startup."""

    def __init__(
        self,
        config: GatewayConfig,
        *,
        baseline: BaselineTransport,
        secure: SecureTransport | None = None,
        metrics: DispatchMetrics | None = None,
        pqc_metrics: PqcMetrics | None = None,
    ) -> None:
        if config.pqc_failure_policy != "fail_closed":
            raise ValueError("PQC_FAILURE_POLICY must be fail_closed.")
        if config.security_mode not in {"classical", "mlkem"}:
            raise ValueError("SECURITY_MODE must be classical or mlkem.")
        if config.security_mode == "mlkem" and secure is None:
            raise ValueError("Secure transport must be initialized for mlkem mode.")
        self._mode = config.security_mode
        self._gateway_id = config.gateway_id
        self._baseline = baseline
        self._secure = secure
        self._metrics = metrics or DispatchMetrics()
        self._pqc_metrics = pqc_metrics or PqcMetrics()

    @property
    def metrics(self) -> DispatchMetrics:
        return self._metrics

    @property
    def pqc_metrics(self) -> PqcMetrics:
        """PQC counters. Fail-closed delivery does not increment the fallback counter."""
        return self._pqc_metrics

    async def send(
        self,
        *,
        request_id: str,
        device_id: str,
        temperature_c: float,
        humidity_pct: float,
        measured_at: str,
        sequence_number: int,
        received_at: str,
    ) -> object:
        """Deliver one measurement. A secure failure does not change mode."""
        if self._mode == "classical":
            return await self._baseline.send(
                request_id=request_id,
                gateway_id=self._gateway_id,
                device_id=device_id,
                temperature_c=temperature_c,
                humidity_pct=humidity_pct,
                measured_at=measured_at,
                sequence_number=sequence_number,
                received_at=received_at,
            )
        return await self._send_secure(
            request_id=request_id,
            device_id=device_id,
            temperature_c=temperature_c,
            humidity_pct=humidity_pct,
            measured_at=measured_at,
            sequence_number=sequence_number,
            received_at=received_at,
        )

    async def _send_secure(
        self,
        *,
        request_id: str,
        device_id: str,
        temperature_c: float,
        humidity_pct: float,
        measured_at: str,
        sequence_number: int,
        received_at: str,
    ) -> SecureAcceptance:
        secure = self._secure
        if secure is None:
            raise ValueError("Secure transport must be initialized for mlkem mode.")
        try:
            return await secure.send(
                request_id=request_id,
                device_id=device_id,
                temperature_c=temperature_c,
                humidity_pct=humidity_pct,
                measured_at=measured_at,
                sequence_number=sequence_number,
                received_at=received_at,
            )
        except SecureTransportError:
            self._metrics.secure_failures_total += 1
            log_security(
                "pqc_fail_closed",
                logging.WARNING,
                request_id=request_id,
                gateway_id=self._gateway_id,
                reason="secure_failure",
            )
            raise
