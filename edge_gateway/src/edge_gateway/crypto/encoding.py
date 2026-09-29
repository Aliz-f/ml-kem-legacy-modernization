"""Base64URL encoding for binary values carried in JSON.

Protocol version 1 uses Base64URL without whitespace. Padding is accepted
and is omitted when encoding.
"""

from __future__ import annotations

import base64
import re

_BASE64URL = re.compile(r"^[A-Za-z0-9_-]+={0,2}$")


class EncodingError(ValueError):
    """A binary JSON field is not valid Base64URL."""


def encode_binary(value: bytes) -> str:
    """Encode raw bytes as unpadded Base64URL."""
    if not isinstance(value, bytes) or value == b"":
        raise EncodingError("Binary value must be non-empty bytes.")
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def decode_binary(value: str) -> bytes:
    """Decode one Base64URL string into raw bytes."""
    if not isinstance(value, str) or value == "":
        raise EncodingError("Base64URL value must be a non-empty string.")
    if _BASE64URL.fullmatch(value) is None:
        raise EncodingError("Base64URL value contains invalid characters.")
    padded = value if "=" in value else value + "=" * (-len(value) % 4)
    if len(padded) % 4 != 0:
        raise EncodingError("Base64URL padding is invalid.")
    try:
        decoded = base64.urlsafe_b64decode(padded)
    except ValueError as exc:
        raise EncodingError("Base64URL value could not be decoded.") from exc
    if decoded == b"":
        raise EncodingError("Base64URL value must not decode to empty bytes.")
    return decoded
