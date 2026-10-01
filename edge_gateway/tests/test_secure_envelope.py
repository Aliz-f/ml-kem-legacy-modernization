"""SecureEnvelope fields, nonce, and absence of plaintext."""

from __future__ import annotations

import json
import logging

import pytest

from edge_gateway.crypto.aad import AadError, build_aad
from edge_gateway.crypto.encoding import decode_binary
from edge_gateway.crypto.envelope import build_secure_envelope
from edge_gateway.crypto.plaintext import PlaintextError, serialize_canonical_measurement
from edge_gateway.crypto.symmetric import NONCE_LENGTH, AeadError, decrypt


def _key() -> bytes:
    return bytes(range(32))


def _build(**overrides: object):
    fields: dict[str, object] = {
        "key": _key(),
        "session_id": "sess-123",
        "request_id": "req-8fb2",
        "device_id": "sensor-plaintext-marker",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z",
        "sequence_number": 184,
        "received_at": "2026-09-21T13:45:31.218Z",
        "gateway_id": "gateway-001",
    }
    fields.update(overrides)
    return build_secure_envelope(**fields)  # type: ignore[arg-type]


def test_envelope_has_exactly_the_protocol_fields():
    envelope = _build()
    payload = envelope.as_dict()
    assert list(payload) == [
        "protocol_version",
        "gateway_id",
        "session_id",
        "request_id",
        "nonce",
        "ciphertext",
    ]
    assert payload["protocol_version"] == "1"
    assert payload["gateway_id"] == "gateway-001"
    assert payload["session_id"] == "sess-123"
    assert payload["request_id"] == "req-8fb2"
    assert "message_counter" not in payload


def test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement():
    envelope = _build()
    nonce = decode_binary(envelope.nonce)
    ciphertext = decode_binary(envelope.ciphertext)
    plaintext = serialize_canonical_measurement(
        device_id="sensor-plaintext-marker",
        temperature_c=21.7,
        humidity_pct=42.5,
        measured_at="2026-09-21T13:45:31Z",
        sequence_number=184,
        received_at="2026-09-21T13:45:31.218Z",
        gateway_id="gateway-001",
    )
    associated_data = build_aad(
        protocol_version="1",
        gateway_id="gateway-001",
        session_id="sess-123",
        request_id="req-8fb2",
    )
    assert len(nonce) == NONCE_LENGTH
    assert decrypt(_key(), nonce, ciphertext, associated_data) == plaintext


def test_plaintext_measurement_does_not_appear_in_the_envelope():
    envelope = _build()
    rendered = json.dumps(envelope.as_dict(), separators=(",", ":"))
    assert "sensor-plaintext-marker" not in rendered
    assert "temperature_c" not in rendered
    assert "humidity_pct" not in rendered
    assert "measured_at" not in rendered
    assert "sequence_number" not in rendered
    assert "message_counter" not in rendered


def test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id():
    first = _build()
    second = _build()
    assert first.nonce != second.nonce
    assert first.ciphertext != second.ciphertext
    assert first.request_id == second.request_id == "req-8fb2"


def test_invalid_measurement_identity_and_key_build_no_envelope():
    with pytest.raises(PlaintextError):
        _build(measured_at="2026-09-21T13:45:31")
    with pytest.raises(AadError):
        _build(session_id=" sess-123")
    with pytest.raises(AeadError):
        _build(key=b"\x00" * 16)


def test_envelope_does_not_log_the_key_or_plaintext(caplog: pytest.LogCaptureFixture):
    key = _key()
    with caplog.at_level(logging.DEBUG):
        envelope = _build(key=key)
    rendered = caplog.text.encode()
    assert key not in rendered
    assert b"sensor-plaintext-marker" not in rendered
    assert envelope.ciphertext.encode() not in rendered
