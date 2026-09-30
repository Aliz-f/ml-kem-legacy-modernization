"""One ephemeral key pair per Cloud application lifespan."""

from uuid import uuid4

from cloud_service.crypto import mlkem
from cloud_service.crypto.encoding import encode_binary


class KeyService:
    def __init__(self):
        self.key_id = f"cloud-key-{uuid4()}"
        self.public_key, self._private_key = mlkem.generate_keypair()
        self.closed = False

    def public_response(self) -> dict[str, str]:
        if self.closed:
            raise mlkem.MlKemError("Cloud key is unavailable")
        return {
            "protocol_version": "1",
            "algorithm": "ML-KEM-768",
            "key_id": self.key_id,
            "public_key": encode_binary(self.public_key),
        }

    def decapsulate(self, ciphertext: bytes) -> bytes:
        return mlkem.decapsulate(ciphertext, self._private_key)

    def close(self) -> None:
        self._private_key.close()
        self.closed = True
