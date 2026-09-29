"""Four-field AES-GCM associated data for protocol version 1.

Gateway and Cloud must each produce these bytes. The object is exactly
`protocol_version`, `gateway_id`, `session_id`, and `request_id`.
"""

from __future__ import annotations

import json

PROTOCOL_VERSION = "1"


class AadError(Exception):
    """The AAD fields are not the frozen four-field object."""


def build_aad(
    *,
    protocol_version: str,
    gateway_id: str,
    session_id: str,
    request_id: str,
) -> bytes:
    """Return the canonical UTF-8 AAD object. Does not log the fields."""
    if not isinstance(protocol_version, str) or protocol_version != PROTOCOL_VERSION:
        raise AadError('protocol_version must be "1".')
    _require_id(gateway_id, "gateway_id")
    _require_id(session_id, "session_id")
    _require_id(request_id, "request_id")
    payload = {
        "protocol_version": protocol_version,
        "gateway_id": gateway_id,
        "session_id": session_id,
        "request_id": request_id,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _require_id(value: object, name: str) -> None:
    if not isinstance(value, str) or value == "" or value != value.strip():
        raise AadError(f"{name} must be a non-empty string.")
