"""Stable Legacy-facing error definitions, independent of the HTTP framework."""

from enum import Enum


class GatewayErrorCode(Enum):
    """Fixed HTTP status and public message for each application error code."""

    INVALID_JSON = (400, "request body must be valid JSON")
    INVALID_MEASUREMENT = (422, "measurement validation failed")
    DUPLICATE_SEQUENCE = (409, "duplicate sequence number")
    OUT_OF_ORDER_SEQUENCE = (409, "out-of-order sequence number")
    CLOUD_UNAVAILABLE = (503, "cloud service is unavailable")
    INTERNAL_ERROR = (500, "internal gateway error")
    SERVICE_UNAVAILABLE = (503, "service is not ready")

    @property
    def status_code(self) -> int:
        return self.value[0]

    def to_dict(self) -> dict[str, dict[str, str]]:
        """Build a fresh response body using only fixed public text."""
        return {"error": {"code": self.name, "message": self.value[1]}}


class GatewayError(Exception):
    """An expected application failure selected by its stable error code.

    Sequence and transport stages can raise this after applying their policies;
    this exception does not implement sequencing, retries, or session recovery.
    """

    def __init__(self, code: GatewayErrorCode):
        self.code = code
        super().__init__(code.name)
