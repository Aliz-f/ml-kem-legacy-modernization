"""Regression checks for the M5-74 through M5-76 coordination index."""

from pathlib import Path


DOCUMENT = Path(__file__).parents[1] / "docs/testing/M5_SECURITY_REGRESSION_SUITE.md"


def test_security_suite_indexes_each_required_m5_74_boundary() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    for requirement in (
        "Tampered AEAD ciphertext",
        "Tampered AAD",
        "Wrong session, expired session, and unknown session",
        "Malformed ML-KEM session input",
        "Simulated ML-KEM decapsulation/application failure",
        "ML-KEM implicit-rejection caveat",
        "No secret logging",
        "No plaintext on the secure endpoint",
        "No automatic baseline fallback",
        "Ambiguous-response retry uses the same built envelope",
        "Retry remains business-idempotent",
        "No dedicated cryptographic anti-replay counter/window",
    ):
        assert requirement in document


def test_security_suite_preserves_fail_closed_and_no_fallback_claims() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "M5-75 — system-wide fail-closed verification" in document
    assert "PQC_FAILURE_POLICY=fail_closed" in document
    assert "mlkem_handshake_failure" in document
    assert "visible Legacy-facing `503`" in document
    assert "zero baseline calls" in document
    assert "gateway_pqc_fallback_total 0" in document
    assert "PQC_FAILURE_POLICY=fallback" in document
    assert "SECURITY_MODE=classical" in document


def test_security_suite_retains_implicit_rejection_scope_limit() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    assert "does not assert that every\nvalid-length bit flip raises" in document
    assert "business idempotency from cryptographic replay protection" in document
