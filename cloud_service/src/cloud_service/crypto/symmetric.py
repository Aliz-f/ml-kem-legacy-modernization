"""Authenticated decryption only; no parsing, persistence or plaintext logs."""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KEY_LENGTH = 32
NONCE_LENGTH = 12
TAG_LENGTH = 16


class AeadError(Exception):
    """Safe secure-message rejection without vendor or secret diagnostics."""


def decrypt(key: bytes | bytearray, nonce: bytes | bytearray,
            ciphertext: bytes | bytearray, associated_data: bytes | bytearray) -> bytes:
    """Return plaintext only after library authentication succeeds."""
    if not isinstance(key, (bytes, bytearray)) or len(key) != KEY_LENGTH:
        raise AeadError("AES-256-GCM key must be 32 bytes")
    if not isinstance(nonce, (bytes, bytearray)) or len(nonce) != NONCE_LENGTH:
        raise AeadError("AES-256-GCM nonce must be 12 bytes")
    if not isinstance(ciphertext, (bytes, bytearray)) or len(ciphertext) < TAG_LENGTH:
        raise AeadError("AES-256-GCM ciphertext must include an authentication tag")
    if not isinstance(associated_data, (bytes, bytearray)):
        raise AeadError("Associated data must be bytes")
    try:
        plaintext = AESGCM(bytes(key)).decrypt(bytes(nonce), bytes(ciphertext), bytes(associated_data))
        if not isinstance(plaintext, bytes):
            raise ValueError
    except Exception:
        raise AeadError("AES-256-GCM authentication failed") from None
    return plaintext
