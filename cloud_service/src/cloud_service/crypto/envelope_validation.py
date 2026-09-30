"""Strict bounded wire validation before session lookup or cryptography."""

import base64
from dataclasses import dataclass, field
import json
import re

from cloud_service.crypto.envelope import EnvelopeSchemaError, SecureEnvelope

MAX_ENVELOPE_BYTES = 64 * 1024


class EnvelopeValidationError(ValueError):
    def __init__(self, code: str = "SECURE_MESSAGE_REJECTED"):
        super().__init__("secure message rejected")
        self.code = code


@dataclass(frozen=True, slots=True)
class ValidatedEnvelope:
    envelope: SecureEnvelope = field(repr=False)
    nonce: bytes = field(repr=False)
    ciphertext: bytes = field(repr=False)


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _constant(value):
    raise ValueError("non-JSON constant")


def parse_json(data: bytes) -> object:
    """Strict UTF-8 JSON; reject duplicate keys and non-finite constants."""
    return json.loads(data.decode("utf-8"), object_pairs_hook=_object, parse_constant=_constant)


def _binary(value: str) -> bytes:
    if not value or re.fullmatch(r"[A-Za-z0-9_-]+={0,2}", value) is None:
        raise ValueError
    padded = value if "=" in value else value + "=" * (-len(value) % 4)
    if len(padded) % 4:
        raise ValueError
    decoded = base64.b64decode(padded, altchars=b"-_", validate=True)
    if not decoded or base64.urlsafe_b64encode(decoded).decode().rstrip("=") != value.rstrip("="):
        raise ValueError
    return decoded


def validate_envelope(body: bytes) -> ValidatedEnvelope:
    if not isinstance(body, bytes) or len(body) > MAX_ENVELOPE_BYTES:
        raise EnvelopeValidationError()
    try:
        envelope = SecureEnvelope.from_dict(parse_json(body))
        if envelope.protocol_version != "1":
            raise EnvelopeValidationError("UNSUPPORTED_PROTOCOL_VERSION")
        for value in (envelope.gateway_id, envelope.session_id, envelope.request_id):
            if not value or value != value.strip():
                raise ValueError
        nonce, ciphertext = _binary(envelope.nonce), _binary(envelope.ciphertext)
        if len(nonce) != 12:
            raise ValueError
        return ValidatedEnvelope(envelope, nonce, ciphertext)
    except EnvelopeValidationError:
        raise
    except (ValueError, EnvelopeSchemaError, RecursionError):
        raise EnvelopeValidationError() from None
