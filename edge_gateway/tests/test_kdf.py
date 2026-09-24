"""Frozen HKDF-SHA-256 session-key contract."""

from __future__ import annotations

import logging

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from edge_gateway.crypto.kdf import SESSION_KEY_INFO, SESSION_KEY_LENGTH, KdfError, derive_session_key


def _independent(shared_secret: bytes, info: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=SESSION_KEY_LENGTH,
        salt=None,
        info=info,
    ).derive(shared_secret)


def test_same_secret_derives_the_same_session_key():
    shared_secret = bytes(range(32))
    assert derive_session_key(shared_secret) == derive_session_key(shared_secret)
    assert derive_session_key(shared_secret) == _independent(shared_secret, SESSION_KEY_INFO)


def test_session_key_is_32_bytes_and_info_is_exact():
    shared_secret = b"\x11" * 32
    session_key = derive_session_key(shared_secret)
    assert len(session_key) == 32
    assert SESSION_KEY_INFO == b"ml-kem-project:v1:gateway-cloud-session"
    assert session_key != _independent(shared_secret, b"ml-kem-project:v1:other")


def test_different_secret_derives_a_different_session_key():
    first = derive_session_key(b"\x01" * 32)
    second = derive_session_key(b"\x02" * 32)
    assert first != second


def test_shared_secret_length_is_rejected():
    with pytest.raises(KdfError):
        derive_session_key(b"")
    with pytest.raises(KdfError):
        derive_session_key(b"\x00" * 31)
    with pytest.raises(KdfError):
        derive_session_key(b"not-bytes")  # type: ignore[arg-type]


def test_session_key_is_not_logged(caplog: pytest.LogCaptureFixture):
    shared_secret = b"\x22" * 32
    with caplog.at_level(logging.DEBUG):
        session_key = derive_session_key(shared_secret)
    rendered = caplog.text.encode()
    assert shared_secret not in rendered
    assert session_key not in rendered
