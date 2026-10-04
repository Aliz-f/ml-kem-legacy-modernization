"""Regression checks for the M5-96 AI-assisted decision record."""

from pathlib import Path


REGISTER = Path(__file__).parents[1] / "docs" / "AI_DECISION_REGISTER.md"


def test_register_records_all_required_decision_outcomes() -> None:
    document = REGISTER.read_text(encoding="utf-8")

    assert "M5-96" in document
    for decision in ("Accepted", "Modified", "Rejected"):
        assert decision in document


def test_register_preserves_course_scope_and_ci_safety_decisions() -> None:
    document = REGISTER.read_text(encoding="utf-8")

    for required_text in (
        "uv sync --frozen",
        "continue-on-error",
        "Kubernetes",
        "Kafka",
        "Docker/Compose",
        "human review",
    ):
        assert required_text in document
