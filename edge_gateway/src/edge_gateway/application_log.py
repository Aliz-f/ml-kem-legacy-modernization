"""Bounded, secret-safe structured logging for Gateway application events."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger("edge_gateway")

APPLICATION_EVENTS = frozenset({
    "gateway_starting",
    "gateway_ready",
    "gateway_shutting_down",
    "gateway_startup_failed",
    "gateway_internal_error",
    "gateway_request_created",
    "legacy_measurement_received",
    "legacy_validation_failed",
    "sequence_duplicate_detected",
    "sequence_out_of_order_detected",
    "sequence_gap_detected",
    "canonical_measurement_created",
    "cloud_delivery_started",
    "cloud_delivery_retry",
    "cloud_delivery_succeeded",
    "cloud_delivery_failed",
    "failure_injected",
})
_FIELDS = (
    "request_id",
    "device_id",
    "gateway_id",
    "sequence_number",
    "previous_sequence_number",
    "security_mode",
    "status",
    "status_code",
    "attempt",
    "failure_type",
    "reason",
)
_TOKEN = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")


def log_application(event: str, level: int = logging.INFO, **fields: object) -> None:
    """Emit one allowlisted event and silently omit unsafe field values."""
    if event not in APPLICATION_EVENTS:
        return
    parts = [f"event={event}", "component=edge_gateway"]
    extra: dict[str, object] = {}
    for name in _FIELDS:
        value = fields.get(name)
        token = _token(value)
        if token is not None:
            parts.append(f"{name}={token}")
            extra[name] = value
    logger.log(level, " ".join(parts), extra=extra)


def _token(value: object) -> str | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        value = str(value)
    if not isinstance(value, str) or _TOKEN.fullmatch(value) is None:
        return None
    return value
