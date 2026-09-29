"""Stored measurement metadata and canonical-to-storage mapping."""

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from cloud_service.models import CanonicalMeasurement
from cloud_service.validation import validate_measurement


@dataclass(frozen=True, slots=True)
class StoredMeasurement:
    record_id: str
    device_id: str
    gateway_id: str
    temperature_c: float
    humidity_pct: float
    measured_at: datetime
    gateway_received_at: datetime
    cloud_received_at: datetime
    sequence_number: int

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id.strip():
            raise ValueError("record_id must be a non-empty string")
        for name in ("measured_at", "gateway_received_at", "cloud_received_at"):
            value = getattr(self, name)
            if not isinstance(value, datetime) or value.utcoffset() != timedelta(0):
                raise ValueError(f"{name} must be a UTC datetime")
        validate_measurement({
            "device_id": self.device_id, "gateway_id": self.gateway_id,
            "temperature_c": self.temperature_c, "humidity_pct": self.humidity_pct,
            "measured_at": self.measured_at.isoformat(),
            "received_at": self.gateway_received_at.isoformat(),
            "sequence_number": self.sequence_number,
        })

    @classmethod
    def from_canonical(
        cls, measurement: CanonicalMeasurement, *, record_id: str | None = None,
        cloud_received_at: datetime | None = None,
    ) -> "StoredMeasurement":
        """Add Cloud metadata; explicit metadata supports deterministic tests."""
        return cls(
            record_id=f"rec-{uuid4()}" if record_id is None else record_id,
            device_id=measurement.device_id, gateway_id=measurement.gateway_id,
            temperature_c=measurement.temperature_c, humidity_pct=measurement.humidity_pct,
            measured_at=measurement.measured_at,
            gateway_received_at=measurement.received_at,
            cloud_received_at=datetime.now(timezone.utc) if cloud_received_at is None else cloud_received_at,
            sequence_number=measurement.sequence_number,
        )

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        for name in ("measured_at", "gateway_received_at", "cloud_received_at"):
            result[name] = getattr(self, name).isoformat(timespec="microseconds").replace("+00:00", "Z")
        return result
