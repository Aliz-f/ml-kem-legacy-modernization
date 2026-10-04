"""Canonical measurement bytes that become AES-GCM plaintext.

The seven field names and their meaning belong to the Gateway canonical
measurement. This serializer only checks that they can be encoded as UTF-8
JSON: finite numbers, an integer sequence, and explicit UTC timestamp strings.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timedelta

_PLAINTEXT_FIELDS = (
    "device_id",
    "temperature_c",
    "humidity_pct",
    "measured_at",
    "sequence_number",
    "received_at",
    "gateway_id",
)


class PlaintextError(Exception):
    """The canonical measurement cannot be serialized."""


def serialize_canonical_measurement(
    *,
    device_id: str,
    temperature_c: float,
    humidity_pct: float,
    measured_at: str,
    sequence_number: int,
    received_at: str,
    gateway_id: str,
) -> bytes:
    """Return deterministic UTF-8 JSON for one canonical measurement."""
    # Device identity has already passed Legacy domain validation. Preserve
    # surrounding whitespace just as baseline delivery and Cloud validation do.
    if not isinstance(device_id, str) or not device_id.strip():
        raise PlaintextError("device_id must be a non-empty string.")
    payload = {
        "device_id": device_id,
        "temperature_c": _require_number(temperature_c, "temperature_c"),
        "humidity_pct": _require_number(humidity_pct, "humidity_pct"),
        "measured_at": _require_utc_timestamp(measured_at, "measured_at"),
        "sequence_number": _require_sequence(sequence_number),
        "received_at": _require_utc_timestamp(received_at, "received_at"),
        "gateway_id": _require_id(gateway_id, "gateway_id"),
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
    if list(json.loads(encoded)) != list(_PLAINTEXT_FIELDS):
        raise PlaintextError("Canonical measurement fields changed during encoding.")
    return encoded.encode("utf-8")


def _require_id(value: object, name: str) -> str:
    if not isinstance(value, str) or value == "" or value != value.strip():
        raise PlaintextError(f"{name} must be a non-empty string.")
    return value


def _require_number(value: object, name: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise PlaintextError(f"{name} must be a finite number.")
    return value


def _require_sequence(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise PlaintextError("sequence_number must be an integer.")
    return value


def _require_utc_timestamp(value: object, name: str) -> str:
    if not isinstance(value, str) or value == "" or value != value.strip():
        raise PlaintextError(f"{name} must be an explicit UTC timestamp.")
    text = f"{value[:-1]}+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise PlaintextError(f"{name} must be an explicit UTC timestamp.") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise PlaintextError(f"{name} must be an explicit UTC timestamp.")
    return value
