"""Legacy JSON syntax and schema validation, before domain checks or delivery."""

import json

from edge_gateway.models import LegacyMeasurement


class LegacyJSONError(ValueError):
    """The request body cannot be parsed as JSON."""


def _reject_constant(value: str) -> None:
    # Python accepts NaN/Infinity by default, but they are not JSON syntax.
    raise ValueError("non-JSON numeric constant")


def parse_legacy_measurement(body: bytes) -> LegacyMeasurement:
    """Distinguish unparseable syntax from errors in a decoded request schema.

    Domain bounds, sequence policy, normalization, and delivery are later stages.
    Neither parser errors nor schema errors contain supplied payload values.
    """
    try:
        payload = json.loads(body, parse_constant=_reject_constant)
    except (ValueError, RecursionError):
        raise LegacyJSONError("request body must be valid JSON") from None
    return LegacyMeasurement.from_dict(payload)
