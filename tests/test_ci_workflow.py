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


def test_repository_quality_workflow_runs_contract_stage_after_unit_tests() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    stage = "name: Run protocol contract tests"
    assert stage in workflow
    for path in (
        "edge_gateway/tests/test_gateway_models.py",
        "edge_gateway/tests/test_gateway_canonical_model.py",
        "edge_gateway/tests/test_gateway_correlation.py",
        "edge_gateway/tests/test_public_key_client.py",
        "edge_gateway/tests/test_session.py",
        "edge_gateway/tests/test_secure_envelope.py",
        "edge_gateway/tests/test_aad.py",
        "edge_gateway/tests/test_kdf.py",
        "cloud_service/tests/test_gateway_cloud_baseline_contract.py",
        "cloud_service/tests/test_cloud_public_key.py",
        "cloud_service/tests/test_cloud_session_api.py",
        "cloud_service/tests/test_cloud_envelope.py",
        "cloud_service/tests/test_cloud_kdf.py",
    ):
        assert path in workflow

    unit_tests = workflow.index("- run: uv run pytest")
    contract_tests = workflow.index(stage)
    crypto_tests = workflow.index("name: Run Gateway crypto checks")
    assert unit_tests < contract_tests < crypto_tests


def test_repository_quality_workflow_runs_the_compose_recovery_regression() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "name: Run Compose recovery regression" in workflow
    assert "uv run pytest tests/integration/test_gateway_compose_e2e.py" in workflow
