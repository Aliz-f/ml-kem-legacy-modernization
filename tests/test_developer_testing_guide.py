"""Regression checks for the M5-59 developer testing guide."""

from pathlib import Path


ROOT = Path(__file__).parents[1]
GUIDE = ROOT / "docs/testing/DEVELOPER_TESTING_GUIDE.md"
WORKFLOW = ROOT / "docs/DEVELOPMENT_WORKFLOW.md"


def test_developer_testing_guide_covers_current_test_layers_and_commands() -> None:
    document = GUIDE.read_text(encoding="utf-8")

    for command in (
        "uv sync --frozen",
        "uv run ruff check .",
        "uv run pytest legacy_system/tests",
        "uv run pytest edge_gateway/tests",
        "uv run pytest cloud_service/tests",
        "tests/integration/test_gateway_cloud_secure.py",
        "tests/integration/test_modernized_end_to_end.py",
        "tests/integration/test_failure_paths.py",
        "tests/integration/test_metrics_sanity.py",
        "uv run python scripts/measure_baseline_e2e.py",
        "docker compose config --quiet",
        "uv run ai-history check",
    ):
        assert command in document

    assert "PQC_FAILURE_POLICY=fail_closed" in document
    assert "same already-built SecureEnvelope" in document
    assert "two-service Compose stack" in document


def test_workflow_refers_to_current_ci_stages_and_testing_guide() -> None:
    document = WORKFLOW.read_text(encoding="utf-8")

    assert "cross-component integration" in document
    assert "full E2E tests" in document
    assert "AI-history CLI" in document
    assert "testing/DEVELOPER_TESTING_GUIDE.md" in document
