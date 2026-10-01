"""Keep the Cloud crypto review anchored to the current implementation."""

from pathlib import Path

ROOT = Path(__file__).parents[2]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_review_matches_the_cloud_session_key_contract() -> None:
    review = _text("edge_gateway/docs/cloud-crypto-review.md")
    cloud_kdf = _text("cloud_service/src/cloud_service/crypto/kdf.py")
    gateway_kdf = _text("edge_gateway/src/edge_gateway/crypto/kdf.py")
    sessions = _text("cloud_service/src/cloud_service/gateway/sessions.py")
    info = 'b"ml-kem-project:v1:gateway-cloud-session"'

    assert "It does not change Cloud code." in review
    assert info in cloud_kdf
    assert info in gateway_kdf
    assert "salt=None" in cloud_kdf
    assert "salt=None" in gateway_kdf
    assert "length=SESSION_KEY_LENGTH" in cloud_kdf
    assert "SESSION_KEY_LENGTH = 32" in cloud_kdf
    assert "hashes.SHA256()" in cloud_kdf
    establish = sessions.split("def _establish", 1)[1].split("async def establish_session", 1)[0]
    assert establish.index("keys.decapsulate") < establish.index("derive_session_key")
    assert "session.response()" in establish


def test_review_matches_key_exposure_and_secure_ingestion() -> None:
    review = _text("edge_gateway/docs/cloud-crypto-review.md")
    keys = _text("cloud_service/src/cloud_service/crypto/keys.py")
    mlkem = _text("cloud_service/src/cloud_service/crypto/mlkem.py")
    session = _text("cloud_service/src/cloud_service/crypto/session.py")
    secure = _text("cloud_service/src/cloud_service/gateway/secure.py")
    envelope = _text("cloud_service/src/cloud_service/crypto/envelope.py")
    repository = _text("cloud_service/src/cloud_service/storage/repository.py")
    notes = _text("cloud_service/docs/secure-ingestion.md")

    public = keys.split("def public_response", 1)[1].split("def decapsulate", 1)[0]
    assert "private" not in public
    assert '"public_key"' in public
    response = session.split("def response", 1)[1].split("class SessionManager", 1)[0]
    assert "session_key" not in response
    assert "repr=False" in session
    assert "never serialized" in mlkem
    assert "Correct-length tampering may not raise." in mlkem
    assert "no persistence, counters or replay window." in session
    assert "session.gateway_id != gateway_id" in session

    ingest = secure.split("def _ingest", 1)[1].split("async def secure_measurement", 1)[0]
    assert ingest.index("validate_envelope") < ingest.index("sessions.get")
    assert ingest.index("plaintext = decrypt") < ingest.index("save_idempotent")
    rejected = ingest.split("except AeadError", 1)[1].split("except StorageError", 1)[0]
    assert "save_idempotent" not in rejected
    assert "exactly the six protocol fields" in envelope
    assert "ON CONFLICT(device_id, sequence_number) DO NOTHING" in repository
    assert "not cryptographic replay" in notes

    for sentence in (
        "salt=None",
        "private key",
        "400 SECURE_MESSAGE_REJECTED",
        "gateway_id",
        "already_accepted",
        "correct-length tampering may not raise",
    ):
        assert sentence.lower() in review.lower()
    readme = _text("edge_gateway/README.md")
    assert "It does not change the Cloud protocol." in readme
