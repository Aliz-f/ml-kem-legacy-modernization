"""Cloud wrapper interoperability, safe failures and ephemeral key lifetime."""

from base64 import urlsafe_b64encode
import logging
from types import SimpleNamespace
import traceback

from cryptography.exceptions import UnsupportedAlgorithm
import pytest

from cloud_service.crypto import mlkem
from cloud_service.crypto.keys import KeyService
from edge_gateway.crypto.mlkem import encapsulate


def test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(caplog):
    with caplog.at_level(logging.DEBUG):
        public, private = mlkem.generate_keypair()
        assert len(public) == 1184
        ciphertext, expected = encapsulate(public)
        actual = mlkem.decapsulate(ciphertext, private)
        assert len(actual) == 32
        assert actual == expected
        # Serialization is test-only, for checking absence from logs/repr.
        private_bytes = private._key.private_bytes_raw()
        output = caplog.text + repr(private)
        for secret in (private_bytes, actual):
            assert all(text not in output for text in (
                repr(secret), secret.hex(), urlsafe_b64encode(secret).decode(),
            ))
    private.close()
    with pytest.raises(mlkem.MlKemError, match="unavailable"):
        mlkem.decapsulate(ciphertext, private)


@pytest.mark.parametrize("ciphertext", [b"", b"x" * 1087, b"x" * 1089, "x" * 1088, None])
def test_malformed_ciphertext_rejected(ciphertext):
    _, private = mlkem.generate_keypair()
    try:
        with pytest.raises(mlkem.MlKemError, match="1088 bytes"):
            mlkem.decapsulate(ciphertext, private)
    finally:
        private.close()


def test_wrong_private_handle_rejected():
    with pytest.raises(mlkem.MlKemError, match="unavailable"):
        mlkem.decapsulate(b"x" * 1088, object())


@pytest.mark.parametrize("error", [ValueError, UnsupportedAlgorithm, RuntimeError])
@pytest.mark.parametrize("operation", ["generate", "decapsulate"])
def test_vendor_failures_are_safe(monkeypatch, caplog, error, operation):
    def fail(*args):
        raise error("sensitive-vendor-marker")

    if operation == "generate":
        monkeypatch.setattr(mlkem, "MLKEM768PrivateKey", SimpleNamespace(generate=fail))
        call = mlkem.generate_keypair
    else:
        private = mlkem.PrivateKey(SimpleNamespace(decapsulate=fail))
        def call():
            return mlkem.decapsulate(b"x" * 1088, private)
    with pytest.raises(mlkem.MlKemError) as caught:
        call()
    output = "".join(traceback.format_exception(caught.value)) + caplog.text
    assert "sensitive-vendor-marker" not in output


@pytest.mark.parametrize("result", [b"short", "x" * 32, None])
def test_bad_vendor_secret_rejected(result):
    private = mlkem.PrivateKey(SimpleNamespace(decapsulate=lambda _: result))
    with pytest.raises(mlkem.MlKemError, match="decapsulation failed"):
        mlkem.decapsulate(b"x" * 1088, private)


def test_bad_vendor_public_key_rejected(monkeypatch):
    public = SimpleNamespace(public_bytes=lambda *args: b"short")
    private = SimpleNamespace(public_key=lambda: public)
    monkeypatch.setattr(mlkem, "MLKEM768PrivateKey", SimpleNamespace(generate=lambda: private))
    with pytest.raises(mlkem.MlKemError, match="key generation failed"):
        mlkem.generate_keypair()


def test_key_services_are_independent_and_close_is_idempotent():
    first, second = KeyService(), KeyService()
    try:
        assert first.key_id != second.key_id
        assert first.public_key != second.public_key
        ciphertext, expected = encapsulate(first.public_key)
        assert first.decapsulate(ciphertext) == expected
        first.close()
        first.close()
        with pytest.raises(mlkem.MlKemError):
            first.public_response()
        with pytest.raises(mlkem.MlKemError):
            first.decapsulate(ciphertext)
        assert not second.closed
    finally:
        first.close()
        second.close()
