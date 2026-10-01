"""Cloud secure-envelope wire schema; security validation follows in M4-34."""

from dataclasses import dataclass, fields


class EnvelopeSchemaError(ValueError):
    """Invalid wire shape without echoing supplied payload values."""


@dataclass(frozen=True, slots=True)
class SecureEnvelope:
    """Six encoded string fields, not yet trusted for secure processing.

    Nonce/ciphertext remain Base64URL wire strings, with no decoding here.
    Construction does not establish protocol validity or authentication.
    """

    protocol_version: str
    gateway_id: str
    session_id: str
    request_id: str
    nonce: str
    ciphertext: str

    def __post_init__(self) -> None:
        for field in fields(self):
            if not isinstance(getattr(self, field.name), str):
                raise EnvelopeSchemaError(f"{field.name} must be a string")

    @classmethod
    def from_dict(cls, payload: object) -> "SecureEnvelope":
        """Read exactly the six wire fields, without coercion or cryptography."""
        if not isinstance(payload, dict):
            raise EnvelopeSchemaError("secure envelope must be a JSON object")
        if set(payload) != {field.name for field in fields(cls)}:
            raise EnvelopeSchemaError("secure envelope must contain exactly the six protocol fields")
        return cls(**payload)

    def to_dict(self) -> dict[str, str]:
        """Return a fresh dictionary preserving all encoded wire values."""
        return {field.name: getattr(self, field.name) for field in fields(self)}
