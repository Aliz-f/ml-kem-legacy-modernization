"""Recorded Gateway crypto decisions stay aligned with the frozen protocol."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
DOCUMENT = ROOT / "edge_gateway" / "docs" / "ai-decisions.md"
README = ROOT / "edge_gateway" / "README.md"
DECISIONS = (
    (
        "AI proposed encrypting sensor JSON directly with ML-KEM.",
        "Rejected.",
        "ML-KEM is a KEM for shared-secret establishment, not bulk message encryption.",
    ),
    (
        "AI proposed SHA-256(shared_secret) as session-key derivation.",
        "Rejected/Modified.",
        "use the frozen HKDF-SHA-256 contract.",
    ),
    (
        "AI proposed HKDF with gateway_id/Cloud identity/key_id.",
        "Rejected/Modified.",
        'protocol v1 deliberately uses the simpler fixed info string: "ml-kem-project:v1:gateway-cloud-session".',
    ),
    (
        "AI proposed a separate key-confirmation key and session response.",
        "Rejected.",
        "protocol v1 does not include a key-confirmation exchange.",
    ),
    (
        "AI proposed adding message counter and a replay window.",
        "Rejected for protocol v1.",
        "dedicated cryptographic anti-replay remains documented technical debt.",
    ),
    (
        "AI proposed logging shared_secret.hex() for debugging.",
        "Rejected.",
        "secret leakage.",
    ),
    (
        "AI proposed automatic plaintext fallback after ML-KEM failure.",
        "Rejected.",
        "silent downgrade violates our fail-closed migration design.",
    ),
    (
        "AI proposed creating a new ML-KEM handshake for every measurement.",
        "Modified.",
        "reuse bounded sessions to reduce overhead.",
    ),
    (
        "AI proposed re-encrypting the same request with a fresh nonce after an ambiguous HTTP timeout.",
        "Rejected/Modified.",
        "ordinary protocol-v1 transport retry retransmits the same already-built SecureEnvelope. Re-encryption happens only after a new session is established.",
    ),
)


def test_ai_decisions_record_each_proposal_outcome_and_reason() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "accepted, modified, and rejected" in document
    assert "salt=None" in document
    assert "ml-kem-project:v1:gateway-cloud-session" in document
    assert "PQC_FAILURE_POLICY=fail_closed" in document
    for proposal, decision, reason in DECISIONS:
        assert f"Proposal: {proposal}" in document
        assert f"Decision: {decision}" in document
        assert f"Reason: {reason}" in document


def test_readme_points_at_the_ai_decisions() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "docs/ai-decisions.md" in readme
    assert "accepted, modified, and rejected" in readme


def test_recorded_decisions_still_match_the_gateway() -> None:
    kdf = (ROOT / "edge_gateway/src/edge_gateway/crypto/kdf.py").read_text(
        encoding="utf-8"
    )
    assert "salt=None" in kdf
    assert 'b"ml-kem-project:v1:gateway-cloud-session"' in kdf

    envelope = (
        ROOT / "edge_gateway/src/edge_gateway/crypto/envelope.py"
    ).read_text(encoding="utf-8")
    assert "message_counter" not in envelope

    dispatch = (ROOT / "edge_gateway/src/edge_gateway/dispatch.py").read_text(
        encoding="utf-8"
    )
    assert "not send the measurement to the baseline endpoint" in dispatch
