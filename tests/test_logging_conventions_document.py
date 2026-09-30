"""Regression checks for the project-wide logging convention."""

from pathlib import Path


CONVENTIONS = Path(__file__).parents[1] / "docs/operations/LOGGING_CONVENTIONS.md"


def test_logging_conventions_cover_common_and_conditional_fields() -> None:
    document = CONVENTIONS.read_text(encoding="utf-8")

    for field in (
        "event", "component", "request_id", "device_id", "gateway_id",
        "sequence_number", "session_id", "key_id", "record_id", "status",
        "attempt", "failure_type",
    ):
        assert f"`{field}`" in document


def test_logging_conventions_preserve_secret_safety_and_metric_boundaries() -> None:
    document = CONVENTIONS.read_text(encoding="utf-8")

    for forbidden in (
        "private keys", "shared secrets", "session keys", "passwords", "tokens",
        "credentials", "full request/response bodies", "raw stack traces",
    ):
        assert forbidden in document
    assert "not metric labels" in document


def test_logging_conventions_define_levels_and_component_ownership() -> None:
    document = CONVENTIONS.read_text(encoding="utf-8")

    for level in ("DEBUG", "INFO", "WARNING", "ERROR"):
        assert f"`{level}`" in document
    assert "retain\nownership" in document
