"""Frozen protocol-v1 session-key derivation using maintained HKDF."""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

SESSION_KEY_LENGTH = 32
SESSION_KEY_INFO = b"ml-kem-project:v1:gateway-cloud-session"
SHARED_SECRET_LENGTH = 32


class KdfError(Exception):
    """Safe derivation failure without input or vendor diagnostics."""


def derive_session_key(shared_secret: bytes) -> bytes:
    """Derive one 32-byte key; never log or persist secret material."""
    if not isinstance(shared_secret, bytes) or len(shared_secret) != SHARED_SECRET_LENGTH:
        raise KdfError("ML-KEM shared secret must be 32 bytes")
    try:
        key = HKDF(
            algorithm=hashes.SHA256(),
            length=SESSION_KEY_LENGTH,
            salt=None,
            info=SESSION_KEY_INFO,
        ).derive(shared_secret)
        if not isinstance(key, bytes) or len(key) != SESSION_KEY_LENGTH:
            raise ValueError
    except Exception:
        raise KdfError("Session key derivation failed") from None
    return key
