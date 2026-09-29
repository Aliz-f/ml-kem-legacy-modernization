"""Cloud canonical schema, domain, and Gateway identity validation."""

from cloud_service.models import CanonicalMeasurement, MeasurementSchemaError


class MeasurementValidationError(ValueError):
    """Invalid measurement, with no payload values in the error message."""


def validate_measurement(
    payload: object, *, expected_gateway_id: str | None = None,
) -> CanonicalMeasurement:
    """Validate decoded canonical JSON before persistence.

    Secure callers must supply the Gateway ID already verified against the
    envelope/session. Baseline callers omit it. This function does not perform
    authentication, session lookup, HTTP error mapping, or database writes.
    """
    try:
        measurement = CanonicalMeasurement.from_dict(payload)
    except MeasurementSchemaError as error:
        raise MeasurementValidationError(str(error)) from None

    for name in ("device_id", "gateway_id"):
        if not getattr(measurement, name).strip():
            raise MeasurementValidationError(f"{name} must be non-empty")
    if not -40 <= measurement.temperature_c <= 85:
        raise MeasurementValidationError("temperature_c must be between -40 and 85")
    if not 0 <= measurement.humidity_pct <= 100:
        raise MeasurementValidationError("humidity_pct must be between 0 and 100")
    if measurement.sequence_number < 0:
        raise MeasurementValidationError("sequence_number must be non-negative")

    if expected_gateway_id is not None:
        if not isinstance(expected_gateway_id, str) or not expected_gateway_id.strip():
            raise MeasurementValidationError("expected_gateway_id must be a non-empty string")
        if measurement.gateway_id != expected_gateway_id:
            raise MeasurementValidationError("gateway_id does not match the verified Gateway identity")
    return measurement
