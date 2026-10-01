"""Uniform protocol binary encoding, including padding and malformed inputs."""

import base64

import pytest

from cloud_service.crypto.encoding import EncodingError, decode_binary, encode_binary


@pytest.mark.parametrize("size", [1, 2, 3, 12, 16, 1088, 1184])
def test_binary_round_trip_padded_and_unpadded(size):
    data = bytes(index % 256 for index in range(size))
    encoded = encode_binary(data)
    assert "=" not in encoded
    assert encoded == base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")
    assert decode_binary(encoded) == data
    assert decode_binary(encoded + "=" * (-len(encoded) % 4)) == data


@pytest.mark.parametrize("value", ["", " ", "Y Q==", "YQ==\n", "YQ=", "YQ===", "A",
    "AB==", "AAB=", "YWJj=", "AA+_", "AA/_", "=YQ", "YQ==x", "é", None, b"YQ", 1])
def test_invalid_encoding_rejected_without_echo(value):
    with pytest.raises(EncodingError, match="^invalid binary encoding$"):
        decode_binary(value)


@pytest.mark.parametrize("value", [b"", "text", None, 1])
def test_encoding_requires_nonempty_bytes(value):
    with pytest.raises(EncodingError, match="^invalid binary encoding$"):
        encode_binary(value)


def test_urlsafe_alphabet():
    assert encode_binary(b"\xfb\xff") == "-_8"
    assert decode_binary("-_8=") == b"\xfb\xff"
