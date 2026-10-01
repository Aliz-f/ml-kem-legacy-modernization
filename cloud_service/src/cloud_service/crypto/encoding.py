"""Protocol v1 Base64URL: emit unpadded; accept canonical padded or unpadded."""

import base64
import re


class EncodingError(ValueError):
    """Safe encoding failure without input material."""


def encode_binary(value: bytes) -> str:
    """Encode non-empty binary protocol material using the URL-safe alphabet."""
    if not isinstance(value, bytes) or not value:
        raise EncodingError("invalid binary encoding")
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def decode_binary(value: str) -> bytes:
    """Reject whitespace, alternate alphabets, bad padding and unused pad bits."""
    try:
        if not isinstance(value, str) or re.fullmatch(r"[A-Za-z0-9_-]+={0,2}", value) is None:
            raise ValueError
        padded = value if "=" in value else value + "=" * (-len(value) % 4)
        if len(padded) % 4:
            raise ValueError
        decoded = base64.b64decode(padded, altchars=b"-_", validate=True)
        if encode_binary(decoded) != value.rstrip("="):
            raise ValueError
        return decoded
    except ValueError:
        raise EncodingError("invalid binary encoding") from None
