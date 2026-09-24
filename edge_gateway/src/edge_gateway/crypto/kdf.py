"""Session-key derivation for protocol version 1.

Both Gateway and Cloud must call this contract. `salt=None` is the
`cryptography` HKDF default: RFC 5869 expands a missing salt to HashLen
zero bytes.
"""

from __future__ import annotations

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

SESSION_KEY_LENGTH = 32
SESSION_KEY_INFO = b"ml-kem-project:v1:gateway-cloud-session"
SHARED_SECRET_LENGTH = 32


class KdfError(Exception):
    """The shared secret cannot be used for session-key derivation."""


def derive_session_key(shared_secret: bytes) -> bytes:
    """Derive the 32-byte AES-256-GCM session key. Does not log key material."""
    if not isinstance(shared_secret, bytes) or len(shared_secret) != SHARED_SECRET_LENGTH:
        raise KdfError("ML-KEM shared secret must be 32 bytes.")
    return HKDF(
        algorithm=hashes.SHA256(),
        length=SESSION_KEY_LENGTH,
        salt=None,
        info=SESSION_KEY_INFO,
    ).derive(shared_secret)
