"""Base64URL helpers for protocol JSON."""

import pytest

from edge_gateway.crypto.encoding import EncodingError, decode_binary, encode_binary


def test_round_trip_omits_padding():
    raw = b"\x00\xff public-key"
    encoded = encode_binary(raw)
    assert "=" not in encoded
    assert "+" not in encoded
    assert "/" not in encoded
    assert decode_binary(encoded) == raw


def test_padded_and_unpadded_forms_decode_equally():
    raw = b"a"
    padded = encode_binary(raw) + "=" * (-len(encode_binary(raw)) % 4)
    assert decode_binary(padded) == raw
    assert decode_binary(encode_binary(raw)) == raw


def test_invalid_alphabet_whitespace_and_empty_are_rejected():
    with pytest.raises(EncodingError):
        decode_binary("")
    with pytest.raises(EncodingError):
        decode_binary("ab cd")
    with pytest.raises(EncodingError):
        decode_binary("ab+c")
    with pytest.raises(EncodingError):
        decode_binary("ab/c")
    with pytest.raises(EncodingError):
        encode_binary(b"")
