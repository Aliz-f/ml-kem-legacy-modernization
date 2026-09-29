"""AES-256-GCM wrapper and 12-byte nonce."""

from __future__ import annotations

import json
import logging

import pytest

from edge_gateway.crypto.aad import build_aad
from edge_gateway.crypto.plaintext import serialize_canonical_measurement
from edge_gateway.crypto.symmetric import KEY_LENGTH, NONCE_LENGTH, AeadError, decrypt, encrypt, generate_nonce


def _key() -> bytes:
    return bytes(range(KEY_LENGTH))


def _aad(**overrides: str) -> bytes:
    fields = {
        "protocol_version": "1",
        "gateway_id": "gateway-001",
        "session_id": "sess-123",
        "request_id": "req-8fb2",
    }
    fields.update(overrides)
    return build_aad(**fields)


def _plaintext() -> bytes:
    return serialize_canonical_measurement(
        device_id="sensor-001",
        temperature_c=21.7,
        humidity_pct=42.5,
        measured_at="2026-09-21T13:45:31Z",
        sequence_number=184,
        received_at="2026-09-21T13:45:31.218Z",
        gateway_id="gateway-001",
    )


def test_round_trip_recovers_the_canonical_measurement():
    key = _key()
    nonce = generate_nonce()
    plaintext = _plaintext()
    associated_data = _aad()
    ciphertext = encrypt(key, nonce, plaintext, associated_data)
    assert ciphertext != plaintext
    assert decrypt(key, nonce, ciphertext, associated_data) == plaintext


def test_same_nonce_repeats_the_ciphertext_and_a_new_nonce_does_not():
    key = _key()
    nonce = b"\x10" * NONCE_LENGTH
    plaintext = _plaintext()
    associated_data = _aad()
    first = encrypt(key, nonce, plaintext, associated_data)
    second = encrypt(key, nonce, plaintext, associated_data)
    assert first == second
    assert encrypt(key, generate_nonce(), plaintext, associated_data) != first


def test_generate_nonce_returns_distinct_12_byte_values():
    nonces = {generate_nonce() for _ in range(8)}
    assert len(nonces) == 8
    assert all(len(nonce) == NONCE_LENGTH for nonce in nonces)


def test_wrong_key_modified_ciphertext_nonce_and_aad_fail():
    key = _key()
    nonce = b"\x22" * NONCE_LENGTH
    plaintext = _plaintext()
    associated_data = _aad()
    ciphertext = encrypt(key, nonce, plaintext, associated_data)
    tampered = bytearray(ciphertext)
    tampered[0] ^= 0x01
    other_nonce = bytearray(nonce)
    other_nonce[0] ^= 0x01
    with pytest.raises(AeadError):
        decrypt(bytes(range(1, KEY_LENGTH + 1)), nonce, ciphertext, associated_data)
    with pytest.raises(AeadError):
        decrypt(key, nonce, bytes(tampered), associated_data)
    with pytest.raises(AeadError):
        decrypt(key, bytes(other_nonce), ciphertext, associated_data)
    with pytest.raises(AeadError):
        decrypt(key, nonce, ciphertext, _aad(request_id="req-other"))


def test_authentication_failure_does_not_return_plaintext():
    key = _key()
    nonce = b"\x33" * NONCE_LENGTH
    plaintext = _plaintext()
    ciphertext = encrypt(key, nonce, plaintext, _aad())
    try:
        recovered = decrypt(key, nonce, ciphertext, _aad(gateway_id="gateway-002"))
    except AeadError as exc:
        assert plaintext not in str(exc).encode()
    else:
        assert recovered != plaintext
        raise AssertionError("tampered AAD returned plaintext")


def test_invalid_key_and_nonce_lengths_are_rejected():
    plaintext = b"{}"
    associated_data = _aad()
    nonce = b"\x01" * NONCE_LENGTH
    for key in (b"", b"\x00" * 16, b"\x00" * 31, b"\x00" * 33, "x" * KEY_LENGTH):
        with pytest.raises(AeadError):
            encrypt(key, nonce, plaintext, associated_data)  # type: ignore[arg-type]
    for bad_nonce in (b"", b"\x00" * 11, b"\x00" * 16):
        with pytest.raises(AeadError):
            encrypt(_key(), bad_nonce, plaintext, associated_data)
    with pytest.raises(AeadError):
        encrypt(_key(), nonce, "plaintext", associated_data)  # type: ignore[arg-type]
    with pytest.raises(AeadError):
        decrypt(_key(), nonce, b"", associated_data)


def test_session_bytearray_key_round_trips():
    key = bytearray(_key())
    nonce = bytearray(b"\x44" * NONCE_LENGTH)
    plaintext = bytearray(_plaintext())
    associated_data = bytearray(_aad())
    ciphertext = encrypt(key, nonce, plaintext, associated_data)
    assert decrypt(key, nonce, ciphertext, associated_data) == bytes(plaintext)


def test_keys_and_plaintext_are_not_logged(caplog: pytest.LogCaptureFixture):
    key = _key()
    plaintext = _plaintext()
    with caplog.at_level(logging.DEBUG):
        ciphertext = encrypt(key, b"\x55" * NONCE_LENGTH, plaintext, _aad())
        decrypt(key, b"\x55" * NONCE_LENGTH, ciphertext, _aad())
    rendered = caplog.text.encode()
    assert key not in rendered
    assert plaintext not in rendered
    assert b"sensor-001" not in rendered


def test_independent_cloud_aad_authenticates_and_each_field_change_fails():
    key = _key()
    nonce = b"\x66" * NONCE_LENGTH
    plaintext = _plaintext()
    fields = {
        "gateway_id": "gateway-001",
        "protocol_version": "1",
        "request_id": "req-8fb2",
        "session_id": "sess-123",
    }
    gateway_aad = build_aad(**fields)
    cloud_aad = json.dumps(dict(fields), sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert gateway_aad == cloud_aad
    ciphertext = encrypt(key, nonce, plaintext, gateway_aad)
    assert decrypt(key, nonce, ciphertext, cloud_aad) == plaintext
    for name, value in (
        ("gateway_id", "gateway-002"),
        ("protocol_version", "2"),
        ("request_id", "req-other"),
        ("session_id", "sess-other"),
    ):
        changed = dict(fields)
        changed[name] = value
        forged = json.dumps(changed, sort_keys=True, separators=(",", ":")).encode("utf-8")
        assert forged != gateway_aad
        with pytest.raises(AeadError):
            decrypt(key, nonce, ciphertext, forged)
