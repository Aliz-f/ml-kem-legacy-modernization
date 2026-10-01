"""Run ML-KEM-768, HKDF-SHA-256, and AES-256-GCM in an installed Gateway image.

The script prints one success line. It does not print keys or shared secrets.
"""

from cryptography.hazmat.primitives.asymmetric.mlkem import MLKEM768PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from edge_gateway.crypto.kdf import derive_session_key
from edge_gateway.crypto.mlkem import encapsulate
from edge_gateway.crypto.symmetric import decrypt, encrypt, generate_nonce


def main() -> None:
    private_key = MLKEM768PrivateKey.generate()
    public_key = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    ciphertext, shared_secret = encapsulate(public_key)
    other_secret = private_key.decapsulate(ciphertext)
    same_secret = shared_secret == other_secret
    if (
        not same_secret
        or len(public_key) != 1184
        or len(ciphertext) != 1088
        or len(shared_secret) != 32
    ):
        raise SystemExit("ML-KEM-768 install check failed")

    session_key = derive_session_key(shared_secret)
    nonce = generate_nonce()
    associated_data = b'{"gateway_id":"gateway-001","protocol_version":"1","request_id":"req-image","session_id":"session-image"}'
    plaintext = b"measurement"
    token = encrypt(session_key, nonce, plaintext, associated_data)
    recovered = decrypt(session_key, nonce, token, associated_data)
    if recovered != plaintext or len(session_key) != 32 or len(nonce) != 12:
        raise SystemExit("AES-256-GCM install check failed")
    print("crypto-install-ok")


if __name__ == "__main__":
    main()
