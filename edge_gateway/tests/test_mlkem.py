"""Gateway ML-KEM-768 wrapper tests.

A valid-length ciphertext bit flip is not required to raise. ML-KEM may
implicitly reject it. Incorrect public-key length must raise.
"""

from __future__ import annotations

import logging

import pytest
from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from edge_gateway.crypto.mlkem import (
    CIPHERTEXT_LENGTH,
    PUBLIC_KEY_LENGTH,
    SHARED_SECRET_LENGTH,
    MlKemError,
    encapsulate,
)


def _raw_public_key() -> tuple[MLKEM768PrivateKey, bytes]:
    private_key = MLKEM768PrivateKey.generate()
    public_key = private_key.public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )
    return private_key, public_key


def test_valid_public_key_round_trip_matches_decapsulation():
    private_key, public_key = _raw_public_key()
    ciphertext, shared_secret = encapsulate(public_key)
    assert len(public_key) == PUBLIC_KEY_LENGTH
    assert len(ciphertext) == CIPHERTEXT_LENGTH
    assert len(shared_secret) == SHARED_SECRET_LENGTH
    assert private_key.decapsulate(ciphertext) == shared_secret


def test_encapsulation_is_fresh():
    _, public_key = _raw_public_key()
    first_ciphertext, first_secret = encapsulate(public_key)
    second_ciphertext, second_secret = encapsulate(public_key)
    assert first_ciphertext != second_ciphertext
    assert first_secret != second_secret


def test_invalid_public_key_length_is_rejected():
    with pytest.raises(MlKemError):
        encapsulate(b"")
    with pytest.raises(MlKemError):
        encapsulate(b"\x00" * (PUBLIC_KEY_LENGTH - 1))
    with pytest.raises(MlKemError):
        encapsulate(b"\x00" * (PUBLIC_KEY_LENGTH + 1))


def test_wrong_type_is_rejected():
    with pytest.raises(MlKemError):
        encapsulate("not-bytes")  # type: ignore[arg-type]


def test_library_rejected_public_key_is_translated():
    # 1184 0xff bytes are rejected by the library. Other 1184-byte strings,
    # including all zeros, are not. Do not require every bit flip to raise.
    with pytest.raises(MlKemError):
        encapsulate(b"\xff" * PUBLIC_KEY_LENGTH)


def test_shared_secret_is_not_logged(caplog: pytest.LogCaptureFixture):
    _, public_key = _raw_public_key()
    with caplog.at_level(logging.DEBUG):
        _, shared_secret = encapsulate(public_key)
    assert shared_secret.hex() not in caplog.text
    assert shared_secret not in caplog.text.encode()
