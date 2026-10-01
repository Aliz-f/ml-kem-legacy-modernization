"""The frozen HTTP-plus-application-crypto trust decision stays documented."""

from pathlib import Path


DOCUMENT = Path(__file__).parents[1] / "docs" / "transport-trust.md"
README = Path(__file__).parents[1] / "README.md"


def test_transport_trust_records_the_frozen_http_decision() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "may use HTTP" in document
    assert "ML-KEM-768" in document
    assert "AES-256-GCM" in document
    assert "documented trust-model limitation" in document
    assert "not an unresolved implementation choice" in document
    assert "http://cloud-service:9000" in document


def test_transport_trust_states_what_is_demonstrated_and_what_is_outside() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "Application-layer post-quantum key establishment" in document
    assert "authenticated encrypted" in document
    for item in (
        "production TLS certificate lifecycle",
        "mTLS",
        "PKI",
        "public-key pinning",
        "signed key distribution",
    ):
        assert item in document
    assert "ML-KEM does not authenticate Cloud identity" in document


def test_key_confirmation_does_not_remove_public_key_substitution_risk() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "does not add a separate key-confirmation tag" in document
    assert "does not remove the risk of unauthenticated public-key substitution" in document


def test_readme_points_at_the_transport_trust_decision() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "docs/transport-trust.md" in readme
    assert "may use HTTP" in readme
    assert "ML-KEM does not authenticate the Cloud" in readme
