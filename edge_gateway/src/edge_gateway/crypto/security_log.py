"""Secret-safe Gateway security logs.

Each record is one line: ``event`` plus a fixed set of correlation fields.
Values that are not single tokens are omitted so a log call cannot break the
handshake or emit key material.
"""

from __future__ import annotations

import logging
import math
import re

logger = logging.getLogger(__name__)

SECURITY_EVENTS = frozenset(
    {
        "mlkem_public_key_received",
        "mlkem_handshake_started",
        "mlkem_handshake_succeeded",
        "mlkem_handshake_failed",
        "session_created",
        "session_reused",
        "session_expired",
        "session_invalidated",
        "session_reestablishment_started",
        "session_reestablishment_succeeded",
        "session_reestablishment_failed",
        "encryption_succeeded",
        "encryption_failed",
        "secure_delivery_started",
        "secure_delivery_rejected",
        "pqc_fail_closed",
    }
)

_FIELDS = (
    "request_id",
    "device_id",
    "gateway_id",
    "sequence_number",
    "session_id",
    "key_id",
    "result",
    "duration",
    "reason",
)
_TOKEN = re.compile(r"[A-Za-z0-9_.:-]{1,128}\Z")


def log_security(event: str, level: int = logging.INFO, **fields: object) -> None:
    """Log one security event. Unknown events and unsafe values are dropped."""
    if event not in SECURITY_EVENTS:
        return
    parts = [f"event={event}", "component=edge_gateway"]
    for name in _FIELDS:
        if name not in fields:
            continue
        token = _token(fields[name])
        if token is not None:
            parts.append(f"{name}={token}")
    logger.log(level, " ".join(parts))


def _token(value: object) -> str | None:
    if isinstance(value, bool) or isinstance(value, bytes):
        return None
    if isinstance(value, float):
        if not math.isfinite(value) or value < 0:
            return None
        value = format(value, ".6f")
    elif isinstance(value, int):
        value = str(value)
    if not isinstance(value, str) or _TOKEN.fullmatch(value) is None:
        return None
    return value
