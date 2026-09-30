"""Regression checks for the repository's foundational CI workflow."""

from pathlib import Path


WORKFLOW = Path(__file__).parents[1] / ".github/workflows/ai-history.yml"


def test_repository_quality_workflow_runs_required_foundation_checks() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "name: Repository quality" in workflow
    assert "on: [push, pull_request]" in workflow
    assert "actions/checkout@v4" in workflow
    assert "actions/setup-python@v5" in workflow
    assert 'python-version: "3.12"' in workflow
    assert "astral-sh/setup-uv@v5" in workflow

    commands = (
        "uv sync --frozen",
        "uv run ruff check .",
        "uv run pytest",
        "uv run ai-history check",
    )
    positions = [workflow.index(command) for command in commands]
    assert positions == sorted(positions)
