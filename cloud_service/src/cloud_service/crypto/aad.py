"""Frozen four-field protocol-v1 authenticated metadata."""

import json

PROTOCOL_VERSION = "1"


class AadError(Exception):
    """Metadata cannot be encoded under the frozen protocol."""


def build_aad(*, protocol_version: str, gateway_id: str, session_id: str, request_id: str) -> bytes:
    if not isinstance(protocol_version, str) or protocol_version != PROTOCOL_VERSION:
        raise AadError('protocol_version must be "1"')
    for value in (gateway_id, session_id, request_id):
        if not isinstance(value, str) or not value or value != value.strip():
            raise AadError("AAD identifiers must be non-empty strings")
    return json.dumps({
        "protocol_version": protocol_version, "gateway_id": gateway_id,
        "session_id": session_id, "request_id": request_id,
    }, sort_keys=True, separators=(",", ":")).encode("utf-8")
