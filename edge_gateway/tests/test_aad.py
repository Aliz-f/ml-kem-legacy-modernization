"""Frozen four-field AAD encoding."""

from __future__ import annotations

import json

import pytest

from edge_gateway.crypto.aad import AadError, build_aad


def _independent(
    *,
    protocol_version: str,
    gateway_id: str,
    session_id: str,
    request_id: str,
) -> bytes:
    """Stand-in for the Cloud encoder. It does not call the Gateway builder."""
    return json.dumps(
        {
            "session_id": session_id,
            "request_id": request_id,
            "protocol_version": protocol_version,
            "gateway_id": gateway_id,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def test_gateway_and_independent_aad_bytes_match_the_contract():
    fields = {
        "protocol_version": "1",
        "gateway_id": "gateway-001",
        "session_id": "sess-123",
        "request_id": "req-8fb2",
    }
    expected = (
        b'{"gateway_id":"gateway-001","protocol_version":"1",'
        b'"request_id":"req-8fb2","session_id":"sess-123"}'
    )
    assert build_aad(**fields) == expected
    assert build_aad(**fields) == _independent(**fields)


def test_each_authenticated_field_changes_the_aad_bytes():
    original = {
        "protocol_version": "1",
        "gateway_id": "gateway-001",
        "session_id": "sess-123",
        "request_id": "req-8fb2",
    }
    baseline = build_aad(**original)
    for name, value in (
        ("gateway_id", "gateway-002"),
        ("session_id", "sess-other"),
        ("request_id", "req-other"),
    ):
        changed = dict(original)
        changed[name] = value
        assert build_aad(**changed) != baseline
        assert _independent(**changed) != baseline


def test_invalid_aad_fields_are_rejected():
    valid = {
        "protocol_version": "1",
        "gateway_id": "gateway-001",
        "session_id": "sess-123",
        "request_id": "req-8fb2",
    }
    for name, value in (
        ("protocol_version", "2"),
        ("protocol_version", " 1"),
        ("gateway_id", ""),
        ("gateway_id", " gateway-001"),
        ("session_id", "sess-123 "),
        ("request_id", ""),
    ):
        fields = dict(valid)
        fields[name] = value
        with pytest.raises(AadError):
            build_aad(**fields)
