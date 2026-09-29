"""AES-256-GCM for protocol version 1.

`generate_nonce()` is only for a new logical encryption. An ordinary transport
retry resends the already-built envelope: the same nonce, ciphertext, and AAD
under the same session key. This module does not build that envelope.
"""

from __future__ import annotations

import secrets

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_LENGTH = 12
KEY_LENGTH = 32


class AeadError(Exception):
    """AES-256-GCM could not encrypt or authenticate the message."""


def generate_nonce() -> bytes:
    """Return a fresh 12-byte nonce from the operating-system CSPRNG."""
    return secrets.token_bytes(NONCE_LENGTH)


def encrypt(key: bytes, nonce: bytes, plaintext: bytes, associated_data: bytes) -> bytes:
    """Encrypt and authenticate. The result includes the GCM authentication tag."""
    key_bytes = _require_key(key)
    nonce_bytes = _require_nonce(nonce)
    plaintext_bytes = _require_bytes(plaintext, "Plaintext")
    aad_bytes = _require_bytes(associated_data, "Associated data")
    try:
        return AESGCM(key_bytes).encrypt(nonce_bytes, plaintext_bytes, aad_bytes)
    except ValueError as exc:
        raise AeadError("AES-256-GCM encryption failed.") from exc


def decrypt(key: bytes, nonce: bytes, ciphertext: bytes, associated_data: bytes) -> bytes:
    """Authenticate and decrypt. A failure does not return plaintext."""
    key_bytes = _require_key(key)
    nonce_bytes = _require_nonce(nonce)
    ciphertext_bytes = _require_bytes(ciphertext, "Ciphertext")
    aad_bytes = _require_bytes(associated_data, "Associated data")
    try:
        return AESGCM(key_bytes).decrypt(nonce_bytes, ciphertext_bytes, aad_bytes)
    except (InvalidTag, ValueError) as exc:
        raise AeadError("AES-256-GCM authentication failed.") from exc


def _require_key(key: object) -> bytes:
    if not isinstance(key, (bytes, bytearray)) or len(key) != KEY_LENGTH:
        raise AeadError("AES-256-GCM key must be 32 bytes.")
    return bytes(key)


def _require_nonce(nonce: object) -> bytes:
    if not isinstance(nonce, (bytes, bytearray)) or len(nonce) != NONCE_LENGTH:
        raise AeadError("AES-256-GCM nonce must be 12 bytes.")
    return bytes(nonce)


def _require_bytes(value: object, label: str) -> bytes:
    if not isinstance(value, (bytes, bytearray)):
        raise AeadError(f"{label} must be bytes.")
    return bytes(value)
