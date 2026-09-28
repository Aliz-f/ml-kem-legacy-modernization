"""Frozen Cloud public-key response parsing."""

import pytest
from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from edge_gateway.crypto.encoding import encode_binary
from edge_gateway.crypto.mlkem import PUBLIC_KEY_LENGTH
from edge_gateway.crypto.public_key import PublicKeyRejected, parse_public_key_response


def _public_key() -> bytes:
    private_key = MLKEM768PrivateKey.generate()
    return private_key.public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )


def _payload(public_key: bytes) -> dict[str, str]:
    return {
        "protocol_version": "1",
        "algorithm": "ML-KEM-768",
        "key_id": "cloud-key-001",
        "public_key": encode_binary(public_key),
    }


def test_valid_response_returns_raw_public_key():
    public_key = _public_key()
    parsed = parse_public_key_response(_payload(public_key))
    assert parsed.protocol_version == "1"
    assert parsed.algorithm == "ML-KEM-768"
    assert parsed.key_id == "cloud-key-001"
    assert parsed.public_key == public_key
    assert len(parsed.public_key) == PUBLIC_KEY_LENGTH


@pytest.mark.parametrize(
    "changes",
    [
        {"protocol_version": "2"},
        {"algorithm": "ML-KEM-512"},
        {"key_id": ""},
        {"key_id": " cloud-key-001"},
        {"public_key": "ab+c"},
        {"public_key": encode_binary(b"\xff" * PUBLIC_KEY_LENGTH)},
        {"public_key": encode_binary(b"\x00" * 10)},
    ],
)
def test_contract_violations_are_rejected(changes: dict[str, str]):
    payload = _payload(_public_key())
    payload.update(changes)
    with pytest.raises(PublicKeyRejected):
        parse_public_key_response(payload)


def test_missing_fields_and_non_object_are_rejected():
    with pytest.raises(PublicKeyRejected):
        parse_public_key_response([])
    with pytest.raises(PublicKeyRejected):
        parse_public_key_response({"algorithm": "ML-KEM-768"})
