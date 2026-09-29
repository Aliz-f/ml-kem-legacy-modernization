"""Valid measurement data for the Legacy Device."""

from dataclasses import dataclass
from datetime import datetime, timezone
import math
from numbers import Real


@dataclass(frozen=True, slots=True)
class Measurement:
    """A valid internal measurement ready for Legacy protocol serialization."""

    device_id: str
    temperature_c: float
    humidity_pct: float
    timestamp: datetime
    sequence_number: int

    def __post_init__(self) -> None:
        if not isinstance(self.device_id, str) or not self.device_id.strip():
            raise ValueError("device_id must be a non-empty string")
        _validate_number("temperature_c", self.temperature_c, -40.0, 85.0)
        _validate_number("humidity_pct", self.humidity_pct, 0.0, 100.0)

        if not isinstance(self.timestamp, datetime):
            raise TypeError("timestamp must be a datetime")
        if self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must be timezone-aware")
        object.__setattr__(
            self, "timestamp", self.timestamp.astimezone(timezone.utc)
        )

        if isinstance(self.sequence_number, bool) or not isinstance(
            self.sequence_number, int
        ):
            raise TypeError("sequence_number must be an integer")
        if self.sequence_number < 0:
            raise ValueError("sequence_number must be non-negative")

    def to_payload(self) -> dict[str, object]:
        """Return an independent JSON-compatible Legacy Gateway payload."""
        return {
            "device_id": self.device_id,
            "temperature_c": self.temperature_c,
            "humidity_pct": self.humidity_pct,
            "timestamp": self.timestamp.isoformat().replace("+00:00", "Z"),
            "sequence_number": self.sequence_number,
        }


def _validate_number(name: str, value: object, minimum: float, maximum: float) -> None:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a number")
    numeric_value = float(value)
    if not math.isfinite(numeric_value) or not minimum <= numeric_value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")