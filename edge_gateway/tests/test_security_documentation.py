"""Gateway security facts stay in the canonical architecture documents."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
DOCUMENT = ROOT / "edge_gateway" / "docs" / "security.md"
README = ROOT / "edge_gateway" / "README.md"
GATEWAY = ROOT / "docs/architecture/02 - Edge Gateway.md"
PROTOCOL = ROOT / "docs/architecture/04 - Shared Cross-Component Protocol Specification.md"
LIBRARY = ROOT / "docs/architecture/ml-kem-library-decision.md"
TOPICS = (
    "ML-KEM library decision",
    "ML-KEM-768 parameter set",
    "ML-KEM implicit-rejection caveat",
    "Public-key response",
    "Public-key trust limitation",
    "HKDF-SHA-256",
    "Session lifecycle",
    "409 session recovery",
    "AES-256-GCM",
    "AAD fields",
    "Canonical AAD serialization",
    "SecureEnvelope format",
    "Base64URL encoding",
    "Ordinary ambiguous retry",
    "Session-recovery encryption",
    "Business idempotency",
    "Replay window",
    "Fail-closed policy",
    "Failure injection",
    "Secret handling",
    "Python memory zeroization",
)
CANONICAL = (
    (GATEWAY, "ML-KEM-768"),
    (GATEWAY, "implicit-rejection"),
    (GATEWAY, '"algorithm": "ML-KEM-768"'),
    (GATEWAY, "does not by itself authenticate the identity of the Cloud"),
    (GATEWAY, "salt=None"),
    (GATEWAY, '"ml-kem-project:v1:gateway-cloud-session"'),
    (GATEWAY, "Python does not guarantee cryptographic memory zeroization"),
    (GATEWAY, "same already-built"),
    (GATEWAY, "409 SESSION_INVALID"),
    (GATEWAY, "12-byte / 96-bit nonce"),
    (GATEWAY, "sorted keys"),
    (GATEWAY, "PQC_FAILURE_POLICY=fail_closed"),
    (GATEWAY, "DO NOT send the measurement to the baseline plaintext endpoint"),
    (GATEWAY, "No dedicated cryptographic anti-replay counter/window"),
    (GATEWAY, "business idempotency is not cryptographic replay protection"),
    (GATEWAY, "(device_id, sequence_number)"),
    (GATEWAY, "ML-KEM private key"),
    (LIBRARY, "pyca/cryptography"),
    (PROTOCOL, "salt=None"),
    (PROTOCOL, "implicit-rejection"),
)


def test_security_note_points_at_the_canonical_documents() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "docs/architecture/02 - Edge Gateway.md" in document
    assert "docs/architecture/04 - Shared Cross-Component Protocol Specification.md" in document
    assert "docs/architecture/ml-kem-library-decision.md" in document
    assert "are not separate specifications" in document
    assert "does not change the protocol" in document
    assert "salt=None" in document
    assert 'info="ml-kem-project:v1:gateway-cloud-session"' in document
    assert "documented as technical debt" in document
    assert "no runtime plaintext fallback" in document
    for topic in TOPICS:
        assert topic in document
    for name in (
        "docs/architecture/edge-gateway.md",
        "docs/architecture/protocol-specification.md",
        "docs/architecture/security-design.md",
    ):
        assert name in document
        assert not (ROOT / name).exists()


def test_canonical_security_sections_keep_the_frozen_facts() -> None:
    for path, phrase in CANONICAL:
        assert phrase in path.read_text(encoding="utf-8")


def test_readme_points_at_the_security_documentation() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "docs/security.md" in readme
    assert "does not replace the frozen architecture" in readme
