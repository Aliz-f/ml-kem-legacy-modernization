"""Cloud public-key response for protocol version 1.

The Gateway trusts this key because it came from the configured Cloud URL.
ML-KEM does not authenticate the Cloud. Unauthenticated HTTP does not
prevent substitution of the public key.
"""

from __future__ import annotations

from dataclasses import dataclass

from edge_gateway.crypto.encoding import EncodingError, decode_binary
from edge_gateway.crypto.mlkem import MlKemError, validate_public_key

PROTOCOL_VERSION = "1"
ALGORITHM = "ML-KEM-768"


class PublicKeyRejected(Exception):
    """The public-key response does not match the frozen contract."""


@dataclass(frozen=True, slots=True)
class CloudPublicKey:
    """A validated ML-KEM-768 Cloud encapsulation key."""

    protocol_version: str
    algorithm: str
    key_id: str
    public_key: bytes


def parse_public_key_response(payload: object) -> CloudPublicKey:
    """Validate a decoded JSON public-key response.

    This checks the key with the ML-KEM wrapper and does not encapsulate.
    """
    if not isinstance(payload, dict):
        raise PublicKeyRejected("Public-key response must be a JSON object.")
    if payload.get("protocol_version") != PROTOCOL_VERSION:
        raise PublicKeyRejected("Unsupported protocol_version.")
    if payload.get("algorithm") != ALGORITHM:
        raise PublicKeyRejected("Unsupported algorithm.")
    key_id = payload.get("key_id")
    if not isinstance(key_id, str) or key_id == "" or key_id != key_id.strip():
        raise PublicKeyRejected("key_id must be a non-empty string.")
    encoded = payload.get("public_key")
    if not isinstance(encoded, str):
        raise PublicKeyRejected("public_key must be a Base64URL string.")
    try:
        public_key = decode_binary(encoded)
    except EncodingError as exc:
        raise PublicKeyRejected("public_key is not valid Base64URL.") from exc
    try:
        validate_public_key(public_key)
    except MlKemError as exc:
        raise PublicKeyRejected("public_key is not a valid ML-KEM-768 key.") from exc
    return CloudPublicKey(
        protocol_version=PROTOCOL_VERSION,
        algorithm=ALGORITHM,
        key_id=key_id,
        public_key=public_key,
    )
