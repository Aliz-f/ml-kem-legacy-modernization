"""The Gateway threat model matches the frozen failure behavior."""

from pathlib import Path


ROOT = Path(__file__).parents[2]
DOCUMENT = ROOT / "edge_gateway" / "docs" / "threat-model.md"
README = ROOT / "edge_gateway" / "README.md"
ENTRIES = (
    "Tampered ciphertext",
    "Wrong or expired session",
    "Malformed or modified ML-KEM ciphertext",
    "Public-key substitution",
    "Secret logging",
    "Replay of an authenticated secure envelope",
    "Downgrade",
    "Cloud unavailability",
    "Session race",
)


def test_each_threat_has_a_mitigation_and_a_remaining_limitation() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "does not add a replay window, TLS, or a plaintext downgrade path" in document
    assert (
        "business idempotency prevents duplicate rows, but protocol v1 has "
        "no dedicated cryptographic anti-replay counter/window."
    ) in document
    for name in ENTRIES:
        section = document.split(f"## {name}\n", 1)[1].split("\n## ", 1)[0]
        assert section.startswith("\nThreat: ")
        assert "\nMitigation: " in section
        assert "\nRemaining limitation: " in section


def test_readme_points_at_the_gateway_threat_model() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "docs/threat-model.md" in readme
    assert "does not add a replay window" in readme


def test_threat_mitigations_still_match_the_gateway() -> None:
    session = (ROOT / "edge_gateway/src/edge_gateway/crypto/session.py").read_text(
        encoding="utf-8"
    )
    dispatch = (ROOT / "edge_gateway/src/edge_gateway/dispatch.py").read_text(
        encoding="utf-8"
    )
    security_log = (
        ROOT / "edge_gateway/src/edge_gateway/crypto/security_log.py"
    ).read_text(encoding="utf-8")
    envelope = (ROOT / "edge_gateway/src/edge_gateway/crypto/envelope.py").read_text(
        encoding="utf-8"
    )

    assert "asyncio.Lock" in session
    assert "not send the measurement to the baseline endpoint" in dispatch
    assert "unsafe values are dropped" in security_log
    assert "message_counter" not in envelope
