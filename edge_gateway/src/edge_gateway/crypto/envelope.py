"""SecureEnvelope builder for protocol version 1.

Each call is one new logical message: a new 12-byte nonce and a new
ciphertext. An ordinary transport retry resends the envelope already
returned by this function. The envelope has no message counter.
"""

from __future__ import annotations

from dataclasses import dataclass

from edge_gateway.crypto.aad import PROTOCOL_VERSION, build_aad
from edge_gateway.crypto.encoding import encode_binary
from edge_gateway.crypto.plaintext import serialize_canonical_measurement
from edge_gateway.crypto.symmetric import encrypt, generate_nonce


@dataclass(frozen=True, slots=True)
class SecureEnvelope:
    """The six protocol fields sent to the Cloud. Plaintext is not one of them."""

    protocol_version: str
    gateway_id: str
    session_id: str
    request_id: str
    nonce: str
    ciphertext: str

    def as_dict(self) -> dict[str, str]:
        """Return the envelope fields in protocol order."""
        return {
            "protocol_version": self.protocol_version,
            "gateway_id": self.gateway_id,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "nonce": self.nonce,
            "ciphertext": self.ciphertext,
        }


def build_secure_envelope(
    *,
    key: bytes,
    session_id: str,
    request_id: str,
    device_id: str,
    temperature_c: float,
    humidity_pct: float,
    measured_at: str,
    sequence_number: int,
    received_at: str,
    gateway_id: str,
) -> SecureEnvelope:
    """Encrypt one canonical measurement into a SecureEnvelope.

    The session key is used only for AES-256-GCM and is not retained.
    """
    plaintext = serialize_canonical_measurement(
        device_id=device_id,
        temperature_c=temperature_c,
        humidity_pct=humidity_pct,
        measured_at=measured_at,
        sequence_number=sequence_number,
        received_at=received_at,
        gateway_id=gateway_id,
    )
    nonce = generate_nonce()
    associated_data = build_aad(
        protocol_version=PROTOCOL_VERSION,
        gateway_id=gateway_id,
        session_id=session_id,
        request_id=request_id,
    )
    ciphertext = encrypt(key, nonce, plaintext, associated_data)
    return SecureEnvelope(
        protocol_version=PROTOCOL_VERSION,
        gateway_id=gateway_id,
        session_id=session_id,
        request_id=request_id,
        nonce=encode_binary(nonce),
        ciphertext=encode_binary(ciphertext),
    )
