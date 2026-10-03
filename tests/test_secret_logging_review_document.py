"""Regression checks for the Member 5 secret-logging review record."""

from pathlib import Path


REVIEW = Path(__file__).parents[1] / "docs/operations/SECRET_LOGGING_REVIEW.md"


def test_secret_logging_review_covers_required_prohibited_data() -> None:
    document = REVIEW.read_text(encoding="utf-8")

    for term in (
        "private-key bytes", "shared secret", "session key", "passwords",
        "tokens", "credentials", ".env", "full request/response bodies",
    ):
        assert term in document


def test_secret_logging_review_indexes_component_owned_marker_tests() -> None:
    document = REVIEW.read_text(encoding="utf-8")

    for test in (
        "test_shared_secret_is_not_logged",
        "test_session_key_is_not_logged",
        "test_handshake_and_delivery_omit_secrets_and_separate_timings",
        "test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged",
        "test_vendor_error_diagnostics_are_suppressed",
    ):
        assert test in document
    assert "uv run pytest" in document


def test_secret_logging_review_records_the_m5_50_system_regression() -> None:
    document = REVIEW.read_text(encoding="utf-8")

    assert "M5-50" in document
    assert "tests/integration/test_observability_integration.py" in document
    assert "shared secret and derived session key" in document
