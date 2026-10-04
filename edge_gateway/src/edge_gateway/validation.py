"""Separate Legacy JSON/schema parsing and domain validation stages."""

import json

from edge_gateway.models import LegacyMeasurement

MAX_SEQUENCE_NUMBER = 2**63 - 1


class LegacyJSONError(ValueError):
    """The request body cannot be parsed as JSON."""


class LegacyMeasurementDomainError(ValueError):
    """Invalid measurement values; messages omit supplied payload values."""


def validate_legacy_measurement(measurement: LegacyMeasurement) -> LegacyMeasurement:
    """Check domain bounds on a schema-validated model without changing it.

    The model already guarantees finite numbers and a timezone-aware UTC timestamp.
    Sequence ordering, normalization, and delivery belong to later stages.
    """
    if not measurement.device_id.strip():
        raise LegacyMeasurementDomainError("device_id must be non-empty")
    if not -40 <= measurement.temperature_c <= 85:
        raise LegacyMeasurementDomainError("temperature_c must be between -40 and 85")
    if not 0 <= measurement.humidity_pct <= 100:
        raise LegacyMeasurementDomainError("humidity_pct must be between 0 and 100")
    if not 0 <= measurement.sequence_number <= MAX_SEQUENCE_NUMBER:
        raise LegacyMeasurementDomainError("sequence_number must be between 0 and 9223372036854775807")
    return measurement


def _reject_constant(value: str) -> None:
    # Python accepts NaN/Infinity by default, but they are not JSON syntax.
    raise ValueError("non-JSON numeric constant")


def parse_legacy_measurement(body: bytes) -> LegacyMeasurement:
    """Distinguish unparseable syntax from errors in a decoded request schema.

    Domain validation is a separate call after parsing; this function checks schema only.
    Neither parser errors nor schema errors contain supplied payload values.
    """
    try:
        payload = json.loads(body, parse_constant=_reject_constant)
    except (ValueError, RecursionError):
        raise LegacyJSONError("request body must be valid JSON") from None
    return LegacyMeasurement.from_dict(payload)
