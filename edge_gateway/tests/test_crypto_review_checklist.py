"""The human review checklist keeps the frozen Gateway crypto checks."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
DOCUMENT = ROOT / "edge_gateway" / "docs" / "crypto-review-checklist.md"
README = ROOT / "edge_gateway" / "README.md"
CHECKS = (
    "correct maintained library API",
    "ML-KEM-768 parameter set",
    "public/private key roles correct",
    "shared secret handled internally only",
    "no handmade lattice/KEM implementation",
    "no brittle assumption that every modified valid-length ciphertext throws",
    "protocol_version / algorithm / key_id validated",
    "unauthenticated HTTP substitution risk documented",
    "ML-KEM not misrepresented as Cloud identity authentication",
    "HKDF-SHA-256",
    "salt=None",
    "info exactly:",
    '"ml-kem-project:v1:gateway-cloud-session"',
    "output length=32 bytes",
    "same fixed parameters as Cloud",
    "no extra transcript fields",
    "no extra confirmation key",
    "no ad hoc SHA256(shared_secret)",
    "TTL enforced",
    "session reuse",
    "gateway/session ownership",
    "409 SESSION_INVALID handling",
    "409 SESSION_EXPIRED handling",
    "maximum one re-establishment per send",
    "AES-256-GCM",
    "32-byte key",
    "12-byte nonce",
    "cryptographically secure nonce generation",
    "AAD contains exactly:",
    "protocol_version",
    "gateway_id",
    "session_id",
    "request_id",
    "canonical AAD encoding matches Cloud",
    "authentication failure stops processing",
    "transport retry bounded",
    "ordinary ambiguous retry reuses the same already-built SecureEnvelope",
    "same request_id / nonce / ciphertext / AAD for ordinary retransmission",
    "session recovery is separate from ordinary retry",
    "new-session recovery rebuilds encryption only because the session changed",
    "business idempotency handles already-stored measurement",
    "no message counter in protocol v1",
    "no dedicated cryptographic anti-replay counter/window",
    "limitation is documented as technical debt",
    "do not claim replay protection that is not implemented",
    "PQC_FAILURE_POLICY=fail_closed only",
    "no runtime plaintext fallback",
    "no baseline endpoint call after crypto/session failure",
    "timeouts",
    "logging safe",
    "metrics safe",
    "readiness does not require an active session",
    "shutdown clears session references",
    "crypto isolated",
    "no crypto code in Legacy route handler",
    "CanonicalMeasurement not modified",
    "request_id remains separate request/transport context",
    "no direct Legacy coupling",
)


def test_crypto_review_checklist_requires_a_human_pass() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert (
        "Generated Gateway crypto code is untrusted until a human "
        "completes this checklist."
    ) in document
    assert "A passing test suite does not replace this checklist." in document
    assert "Decision records are a later task." in document
    for item in CHECKS:
        assert f"\n- {item}\n" in document


def test_readme_points_at_the_crypto_review_checklist() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "docs/crypto-review-checklist.md" in readme
    assert "does not replace this checklist" in readme


def test_checklist_anchors_still_match_the_gateway() -> None:
    kdf = (ROOT / "edge_gateway/src/edge_gateway/crypto/kdf.py").read_text(
        encoding="utf-8"
    )
    assert "salt=None" in kdf
    assert 'b"ml-kem-project:v1:gateway-cloud-session"' in kdf
    assert "SESSION_KEY_LENGTH = 32" in kdf

    mlkem = (ROOT / "edge_gateway/src/edge_gateway/crypto/mlkem.py").read_text(
        encoding="utf-8"
    )
    assert "MLKEM768PublicKey" in mlkem
    assert "PUBLIC_KEY_LENGTH = 1184" in mlkem
    assert "CIPHERTEXT_LENGTH = 1088" in mlkem

    aad = (ROOT / "edge_gateway/src/edge_gateway/crypto/aad.py").read_text(
        encoding="utf-8"
    )
    assert "sort_keys=True" in aad
    assert 'separators=(",", ":")' in aad

    symmetric = (
        ROOT / "edge_gateway/src/edge_gateway/crypto/symmetric.py"
    ).read_text(encoding="utf-8")
    assert "NONCE_LENGTH = 12" in symmetric
    assert "KEY_LENGTH = 32" in symmetric
    assert "secrets.token_bytes" in symmetric

    transport = (
        ROOT / "edge_gateway/src/edge_gateway/crypto/secure_transport.py"
    ).read_text(encoding="utf-8")
    assert "one replacement" in transport
    assert "does not call the baseline endpoint" in transport

    config = (ROOT / "edge_gateway/src/edge_gateway/config.py").read_text(
        encoding="utf-8"
    )
    assert 'PQC_FAILURE_POLICIES = frozenset({"fail_closed"})' in config

    app = (ROOT / "edge_gateway/src/edge_gateway/app.py").read_text(encoding="utf-8")
    handler = app.split("async def measurements", 1)[1].split("@app.get", 1)[0]
    for term in ("encapsulate", "encrypt", "SecureEnvelope", "MLKEM"):
        assert term not in handler
    ready = app.split("async def ready", 1)[1].split("@app.post", 1)[0]
    assert "session" not in ready
    assert "dispatch.is_ready" in ready
