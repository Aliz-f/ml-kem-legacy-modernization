"""Gateway-owned Legacy request schema, independent of the Legacy package."""

from dataclasses import dataclass, fields
from datetime import datetime, timedelta
import math


class LegacyMeasurementSchemaError(ValueError):
    """Invalid request schema; messages never include supplied payload values."""


@dataclass(frozen=True, slots=True)
class LegacyMeasurement:
    """Typed Legacy data, not yet domain-validated or accepted for delivery.

    M2-05 owns domain bounds and non-empty device IDs. M2-04/M2-12 own
    JSON syntax and HTTP error mapping. No canonical metadata is added here.
    """

    device_id: str
    temperature_c: float
    humidity_pct: float
    timestamp: datetime
    sequence_number: int

    def __post_init__(self) -> None:
        if not isinstance(self.device_id, str):
            raise LegacyMeasurementSchemaError("device_id must be a string")
        for name in ("temperature_c", "humidity_pct"):
            value = getattr(self, name)
            if type(value) not in (int, float):
                raise LegacyMeasurementSchemaError(f"{name} must be a finite number")
            try:
                finite = math.isfinite(value)
            except OverflowError:
                finite = False
            if not finite:
                raise LegacyMeasurementSchemaError(f"{name} must be a finite number")
        if type(self.sequence_number) is not int:
            raise LegacyMeasurementSchemaError("sequence_number must be an integer")
        if not isinstance(self.timestamp, datetime) or self.timestamp.utcoffset() != timedelta(0):
            raise LegacyMeasurementSchemaError("timestamp must be a UTC datetime")

    @classmethod
    def from_dict(cls, payload: object) -> "LegacyMeasurement":
        """Parse a decoded JSON object without coercion or extra fields."""
        if not isinstance(payload, dict):
            raise LegacyMeasurementSchemaError("measurement must be a JSON object")
        expected = {field.name for field in fields(cls)}
        if set(payload) != expected:
            raise LegacyMeasurementSchemaError("measurement must contain exactly the five Legacy fields")
        values = dict(payload)
        values["timestamp"] = _timestamp(values["timestamp"])
        return cls(**values)

    def to_dict(self) -> dict[str, object]:
        """Return the five Legacy wire fields as an independent JSON object."""
        result = {field.name: getattr(self, field.name) for field in fields(self)}
        result["timestamp"] = self.timestamp.isoformat().replace("+00:00", "Z")
        return result


def _timestamp(value: object) -> datetime:
    if not isinstance(value, str) or "T" not in value:
        raise LegacyMeasurementSchemaError("timestamp must be an ISO-8601 UTC string")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        raise LegacyMeasurementSchemaError("timestamp must be an ISO-8601 UTC string") from None
    if parsed.utcoffset() != timedelta(0):
        raise LegacyMeasurementSchemaError("timestamp must have an explicit UTC timezone")
    return parsed
