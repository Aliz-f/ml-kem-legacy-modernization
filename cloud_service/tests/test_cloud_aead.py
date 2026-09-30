"""Cloud/Gateway AEAD interoperability and authenticated metadata tampering."""

import json
import logging
import traceback

import pytest

from cloud_service.crypto import aad, symmetric
from edge_gateway.crypto.aad import build_aad as gateway_aad
from edge_gateway.crypto.symmetric import encrypt, generate_nonce


def fields():
    return dict(protocol_version="1", gateway_id="gateway-1", session_id="sess-1", request_id="req-1")


@pytest.mark.parametrize("identifier", ["gateway-1", "sensor-\u00e4", 'id"\\\nvalue'])
def test_aad_is_byte_identical(identifier):
    metadata = fields()
    metadata["gateway_id"] = identifier
    encoded = aad.build_aad(**metadata)
    assert encoded == gateway_aad(**metadata)
    assert encoded == json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert set(json.loads(encoded)) == set(fields())


@pytest.mark.parametrize("field", ["gateway_id", "session_id", "request_id"])
@pytest.mark.parametrize("value", ["", " x ", None, 123])
def test_invalid_identifiers(field, value):
    metadata = fields()
    metadata[field] = value
    with pytest.raises(aad.AadError):
        aad.build_aad(**metadata)


@pytest.mark.parametrize("version", ["2", 1, None])
def test_unsupported_version(version):
    with pytest.raises(aad.AadError):
        aad.build_aad(**(fields() | {"protocol_version": version}))


@pytest.mark.parametrize("plaintext", [b"", b"canonical measurement bytes", b"\x00\xff\x80"])
def test_gateway_encryption_cloud_decryption(plaintext, caplog):
    key = bytes(range(32))  # Synthetic test key only.
    nonce = generate_nonce()
    with caplog.at_level(logging.DEBUG):
        ciphertext = encrypt(key, nonce, plaintext, gateway_aad(**fields()))
        actual = symmetric.decrypt(bytearray(key), bytearray(nonce), bytearray(ciphertext), aad.build_aad(**fields()))
    assert actual == plaintext
    assert caplog.text == ""


@pytest.mark.parametrize("field", list(fields()))
def test_each_modified_aad_field_fails_authentication(field):
    key, nonce = bytes(range(32)), generate_nonce()
    ciphertext = encrypt(key, nonce, b"private plaintext", gateway_aad(**fields()))
    changed = fields() | {field: "2" if field == "protocol_version" else "different"}
    # Build altered version bytes explicitly: production builders reject v2 first.
    altered_aad = json.dumps(changed, sort_keys=True, separators=(",", ":")).encode()
    with pytest.raises(symmetric.AeadError, match="authentication failed"):
        symmetric.decrypt(key, nonce, ciphertext, altered_aad)


@pytest.mark.parametrize("part", ["key", "nonce", "ciphertext", "tag"])
def test_crypto_tampering_rejected(part, caplog):
    values = {"key": bytes(range(32)), "nonce": generate_nonce(), "associated_data": aad.build_aad(**fields())}
    values["ciphertext"] = encrypt(values["key"], values["nonce"], b"private plaintext", values["associated_data"])
    target = "ciphertext" if part == "tag" else part
    modified = bytearray(values[target])
    modified[-1 if part == "tag" else 0] ^= 1
    values[target] = modified
    with pytest.raises(symmetric.AeadError):
        symmetric.decrypt(**values)
    assert caplog.text == ""


@pytest.mark.parametrize(("field", "value"), [
    ("key", b"x" * 16), ("key", b"x" * 31), ("key", "x" * 32),
    ("nonce", b"x" * 11), ("nonce", b"x" * 13), ("nonce", None),
    ("ciphertext", b""), ("ciphertext", b"x" * 15), ("ciphertext", "x" * 32),
    ("associated_data", None), ("associated_data", "metadata"),
])
def test_invalid_inputs_before_vendor(field, value, monkeypatch):
    def unexpected(*args):
        pytest.fail("Invalid input reached AESGCM")
    monkeypatch.setattr(symmetric, "AESGCM", unexpected)
    values = dict(key=b"x" * 32, nonce=b"x" * 12, ciphertext=b"x" * 16, associated_data=b"aad")
    values[field] = value
    with pytest.raises(symmetric.AeadError):
        symmetric.decrypt(**values)


def test_vendor_error_diagnostics_are_suppressed(monkeypatch, caplog):
    def fail(*args):
        raise RuntimeError("sensitive-vendor-marker")
    monkeypatch.setattr(symmetric, "AESGCM", fail)
    with pytest.raises(symmetric.AeadError) as caught:
        symmetric.decrypt(b"x" * 32, b"x" * 12, b"x" * 16, b"aad")
    assert "sensitive-vendor-marker" not in "".join(traceback.format_exception(caught.value)) + caplog.text
