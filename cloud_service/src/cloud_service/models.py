"""Cloud-owned canonical schema. Application domain rules follow in M4-04."""

from dataclasses import dataclass, fields
from datetime import datetime, timedelta
import math


class MeasurementSchemaError(ValueError):
    """Invalid canonical schema, without echoing supplied payload values."""


def _timestamp(value: object, name: str) -> datetime:
    if not isinstance(value, str) or "T" not in value:
        raise MeasurementSchemaError(f"{name} must be an ISO-8601 UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        raise MeasurementSchemaError(f"{name} must be an ISO-8601 UTC timestamp") from None
    if parsed.utcoffset() != timedelta(0):
        raise MeasurementSchemaError(f"{name} must have an explicit UTC timezone")
    return parsed


@dataclass(frozen=True, slots=True)
class CanonicalMeasurement:
    """Typed canonical data, not yet validated for persistence.

    Schema validity is separate from M4-04's domain and Gateway identity checks.
    Request IDs and Cloud storage metadata are not canonical measurement fields.
    """

    device_id: str
    temperature_c: float
    humidity_pct: float
    measured_at: datetime
    sequence_number: int
    received_at: datetime
    gateway_id: str

    def __post_init__(self) -> None:
        for name in ("device_id", "gateway_id"):
            if not isinstance(getattr(self, name), str):
                raise MeasurementSchemaError(f"{name} must be a string")
        for name in ("temperature_c", "humidity_pct"):
            value = getattr(self, name)
            if type(value) not in (int, float):
                raise MeasurementSchemaError(f"{name} must be a finite number")
            try:
                finite = math.isfinite(value)
            except OverflowError:
                finite = False
            if not finite:
                raise MeasurementSchemaError(f"{name} must be a finite number")
        if type(self.sequence_number) is not int:
            raise MeasurementSchemaError("sequence_number must be an integer")
        for name in ("measured_at", "received_at"):
            value = getattr(self, name)
            if not isinstance(value, datetime) or value.utcoffset() != timedelta(0):
                raise MeasurementSchemaError(f"{name} must be a UTC datetime")

    @classmethod
    def from_dict(cls, payload: object) -> "CanonicalMeasurement":
        """Parse an already-decoded JSON object, without scalar coercion."""
        if not isinstance(payload, dict):
            raise MeasurementSchemaError("measurement must be a JSON object")
        expected = {field.name for field in fields(cls)}
        if set(payload) != expected:
            raise MeasurementSchemaError("measurement must contain exactly the seven canonical fields")
        values = dict(payload)
        for name in ("measured_at", "received_at"):
            values[name] = _timestamp(values[name], name)
        return cls(**values)

    def to_dict(self) -> dict[str, object]:
        """Return the wire fields with explicit UTC timestamps, without metadata."""
        result = {field.name: getattr(self, field.name) for field in fields(self)}
        for name in ("measured_at", "received_at"):
            result[name] = getattr(self, name).isoformat().replace("+00:00", "Z")
        return result
