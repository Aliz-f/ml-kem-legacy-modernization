"""Frozen HKDF contract and real ML-KEM-to-HKDF interoperability."""

import logging
from types import SimpleNamespace
import traceback

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from cloud_service.crypto import kdf, mlkem
from edge_gateway.crypto import kdf as gateway_kdf
from edge_gateway.crypto.mlkem import encapsulate


def test_frozen_contract_and_determinism():
    secret = bytes(range(32))  # Synthetic test input, never a runtime RNG.
    expected = HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
                    info=b"ml-kem-project:v1:gateway-cloud-session").derive(secret)
    assert kdf.SESSION_KEY_INFO == gateway_kdf.SESSION_KEY_INFO == b"ml-kem-project:v1:gateway-cloud-session"
    assert kdf.SESSION_KEY_LENGTH == gateway_kdf.SESSION_KEY_LENGTH == 32
    assert kdf.derive_session_key(secret) == expected
    assert kdf.derive_session_key(secret) == kdf.derive_session_key(secret)


def test_exact_library_parameters(monkeypatch):
    calls = []
    original = kdf.HKDF
    def capture(**kwargs):
        calls.append(kwargs)
        return original(**kwargs)
    monkeypatch.setattr(kdf, "HKDF", capture)
    assert len(kdf.derive_session_key(bytes(range(32)))) == 32
    assert len(calls) == 1
    assert isinstance(calls[0]["algorithm"], hashes.SHA256)
    assert calls[0]["salt"] is None
    assert calls[0]["length"] == 32
    assert calls[0]["info"] == b"ml-kem-project:v1:gateway-cloud-session"


def test_gateway_cloud_mlkem_and_kdf_interoperability(caplog):
    public, private = mlkem.generate_keypair()
    try:
        with caplog.at_level(logging.DEBUG):
            ciphertext, gateway_secret = encapsulate(public)
            cloud_secret = mlkem.decapsulate(ciphertext, private)
            # Boolean assertions avoid rendering secret operands on failure.
            secrets_match = gateway_secret == cloud_secret
            assert secrets_match
            gateway_key = gateway_kdf.derive_session_key(gateway_secret)
            cloud_key = kdf.derive_session_key(cloud_secret)
            keys_match = gateway_key == cloud_key
            assert keys_match
            assert len(cloud_key) == 32
        assert caplog.text == ""
    finally:
        private.close()


@pytest.mark.parametrize("secret", [b"", b"x" * 31, b"x" * 33, "x" * 32, None, bytearray(32)])
def test_invalid_secret_rejected_before_hkdf(secret, monkeypatch):
    def unexpected(**kwargs):
        pytest.fail("Invalid input reached HKDF")
    monkeypatch.setattr(kdf, "HKDF", unexpected)
    with pytest.raises(kdf.KdfError, match="must be 32 bytes"):
        kdf.derive_session_key(secret)


@pytest.mark.parametrize("stage", ["construction", "derivation"])
def test_vendor_failures_are_sanitized(stage, monkeypatch, caplog):
    def fail(*args, **kwargs):
        raise RuntimeError("sensitive-vendor-marker")
    monkeypatch.setattr(kdf, "HKDF", fail if stage == "construction" else
                        lambda **kwargs: SimpleNamespace(derive=fail))
    with pytest.raises(kdf.KdfError) as caught:
        kdf.derive_session_key(bytes(range(32)))
    assert "sensitive-vendor-marker" not in "".join(traceback.format_exception(caught.value)) + caplog.text


@pytest.mark.parametrize("result", [b"short", "x" * 32, None])
def test_invalid_vendor_output_rejected(result, monkeypatch):
    monkeypatch.setattr(kdf, "HKDF", lambda **kwargs: SimpleNamespace(derive=lambda _: result))
    with pytest.raises(kdf.KdfError, match="derivation failed"):
        kdf.derive_session_key(bytes(range(32)))
