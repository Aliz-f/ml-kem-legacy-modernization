"""ML-KEM-768 encapsulation for the Gateway.

The Cloud public key is raw FIPS 203 bytes. Base64URL decoding belongs to
the protocol client, not this wrapper.
"""

from __future__ import annotations

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PublicKey

PUBLIC_KEY_LENGTH = 1184
CIPHERTEXT_LENGTH = 1088
SHARED_SECRET_LENGTH = 32


class MlKemError(Exception):
    """The Gateway could not encapsulate to the supplied public key."""


def validate_public_key(public_key: bytes) -> None:
    """Accept only a raw ML-KEM-768 public key. Does not encapsulate or log it."""
    if not isinstance(public_key, bytes) or len(public_key) != PUBLIC_KEY_LENGTH:
        raise MlKemError("ML-KEM-768 public key must be 1184 bytes.")
    try:
        MLKEM768PublicKey.from_public_bytes(public_key)
    except (ValueError, UnsupportedAlgorithm) as exc:
        raise MlKemError("ML-KEM-768 public key was rejected.") from exc


def encapsulate(public_key: bytes) -> tuple[bytes, bytes]:
    """Return `(ciphertext, shared_secret)` for an ML-KEM-768 public key.

    The shared secret stays with the caller. This function does not log it.
    """
    validate_public_key(public_key)
    try:
        key = MLKEM768PublicKey.from_public_bytes(public_key)
        shared_secret, ciphertext = key.encapsulate()
    except (ValueError, UnsupportedAlgorithm) as exc:
        raise MlKemError("ML-KEM-768 encapsulation failed.") from exc
    if (
        len(shared_secret) != SHARED_SECRET_LENGTH
        or len(ciphertext) != CIPHERTEXT_LENGTH
    ):
        raise MlKemError("ML-KEM-768 encapsulation returned unexpected lengths.")
    return ciphertext, shared_secret
