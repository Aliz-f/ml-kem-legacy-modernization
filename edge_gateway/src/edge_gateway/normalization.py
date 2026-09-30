"""Translate validated Legacy measurements into the Gateway canonical model."""

from datetime import datetime

from edge_gateway.models import CanonicalMeasurement, LegacyMeasurement


def normalize(
    legacy_measurement: LegacyMeasurement, *, gateway_id: str, received_at: datetime
) -> CanonicalMeasurement:
    """Preserve measurement values and attach caller-supplied Gateway metadata.

    Call after Legacy schema/domain validation and sequence-policy acceptance.
    The caller supplies the configured Gateway ID and current UTC receipt time;
    this mapping performs no clock reads, configuration loading, or delivery.
    """
    return CanonicalMeasurement(
        device_id=legacy_measurement.device_id,
        temperature_c=legacy_measurement.temperature_c,
        humidity_pct=legacy_measurement.humidity_pct,
        measured_at=legacy_measurement.timestamp,
        sequence_number=legacy_measurement.sequence_number,
        received_at=received_at,
        gateway_id=gateway_id,
    )
