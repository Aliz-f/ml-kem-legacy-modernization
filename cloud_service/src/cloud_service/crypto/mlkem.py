"""ML-KEM-768 key generation and decapsulation using PyCA cryptography.

Only this module depends on the vendor ML-KEM API. Private keys are opaque
handles, never serialized. No input, key or shared secret is logged.
"""

from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

PUBLIC_KEY_LENGTH = 1184
CIPHERTEXT_LENGTH = 1088
SHARED_SECRET_LENGTH = 32


class MlKemError(Exception):
    """Safe error that contains no vendor diagnostics or input material."""


class PrivateKey:
    """Opaque process-local key handle with explicit reference release.

    Closing prevents further use. Python cannot guarantee memory zeroization.
    The default object repr deliberately includes no key fields.
    """

    __slots__ = ("_key",)

    def __init__(self, key: MLKEM768PrivateKey):
        self._key = key

    def close(self) -> None:
        self._key = None


def generate_keypair() -> tuple[bytes, PrivateKey]:
    """Return raw public bytes and an opaque private handle; use library RNG."""
    try:
        key = MLKEM768PrivateKey.generate()
        public_key = key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        if not isinstance(public_key, bytes) or len(public_key) != PUBLIC_KEY_LENGTH:
            raise ValueError
    except Exception:
        # Vendor exceptions may contain sensitive diagnostics. Suppress chaining.
        raise MlKemError("ML-KEM-768 key generation failed") from None
    return public_key, PrivateKey(key)


def decapsulate(ciphertext: bytes, private_key: PrivateKey) -> bytes:
    """Return the raw 32-byte secret. Correct-length tampering may not raise."""
    if not isinstance(ciphertext, bytes) or len(ciphertext) != CIPHERTEXT_LENGTH:
        raise MlKemError("ML-KEM-768 ciphertext must be 1088 bytes")
    if not isinstance(private_key, PrivateKey) or private_key._key is None:
        raise MlKemError("ML-KEM-768 private key is unavailable")
    try:
        shared_secret = private_key._key.decapsulate(ciphertext)
        if not isinstance(shared_secret, bytes) or len(shared_secret) != SHARED_SECRET_LENGTH:
            raise ValueError
    except Exception:
        raise MlKemError("ML-KEM-768 decapsulation failed") from None
    return shared_secret
