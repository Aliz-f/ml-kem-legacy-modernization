"""Regression checks for the repository's foundational CI workflow."""

from pathlib import Path


WORKFLOW = Path(__file__).parents[1] / ".github/workflows/ai-history.yml"
AI_HISTORY_README = Path(__file__).parents[1] / "docs/ai/README.md"


def test_repository_quality_workflow_separates_required_ci_jobs_and_caches_uv() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "name: Repository quality" in workflow
    assert "on: [push, pull_request]" in workflow
    assert "actions/checkout@v4" in workflow
    assert "actions/setup-python@v5" in workflow
    assert 'python-version: "3.12"' in workflow
    assert "astral-sh/setup-uv@v5" in workflow
    assert "enable-cache: true" in workflow
    for job in (
        "quality:", "unit-tests:", "integration-tests:", "secure-e2e:",
        "docker-build:", "clean-environment:",
    ):
        assert job in workflow

    quality = workflow[workflow.index("  quality:") : workflow.index("  unit-tests:")]
    assert "uv sync --frozen" in quality
    assert "uv run ruff check ." in quality
    assert "uv run ai-history check" in quality


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

    unit_tests = workflow.index("name: Run unit and repository tests")
    contract_tests = workflow.index(stage)
    crypto_tests = workflow.index("name: Run Gateway crypto checks")
    assert unit_tests < contract_tests < crypto_tests


def test_repository_quality_workflow_runs_the_compose_recovery_regression() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "name: Run Compose recovery regression" in workflow
    assert "uv run pytest tests/integration/test_gateway_compose_e2e.py" in workflow


def test_repository_quality_workflow_runs_observability_and_metrics_sanity() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "name: Run observability and metrics sanity regressions" in workflow
    assert "tests/integration/test_observability_integration.py" in workflow
    assert "tests/integration/test_metrics_sanity.py" in workflow


def test_repository_quality_workflow_runs_explicit_integration_and_e2e_stages() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    integration_stage = "name: Run cross-component integration tests"
    e2e_stage = "name: Run full end-to-end tests"
    assert integration_stage in workflow
    assert e2e_stage in workflow

    for path in (
        "tests/integration/test_legacy_gateway.py",
        "tests/integration/test_gateway_cloud_baseline.py",
        "tests/integration/test_mlkem_session_orchestration.py",
        "tests/integration/test_gateway_cloud_secure_session.py",
        "tests/integration/test_gateway_cloud_secure.py",
        "tests/integration/test_end_to_end.py",
        "tests/integration/test_modernized_end_to_end.py",
        "tests/integration/test_legacy_mode_success_compatibility.py",
    ):
        assert path in workflow

    assert workflow.index(integration_stage) < workflow.index(e2e_stage)
    assert "needs: [quality, unit-tests, integration-tests]" in workflow


def test_repository_quality_workflow_smoke_tests_ai_history_cli() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    stage = "name: Verify AI-history CLI compatibility"
    assert stage in workflow
    for command in (
        "uv run ai-history --help",
        "uv run ai-history status",
        "uv run ai-history list",
        "uv run ai-history check",
    ):
        assert command in workflow

    assert workflow.index("uv sync --frozen") < workflow.index(stage)


def test_repository_quality_workflow_builds_all_images_and_runs_clean_compose() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    for dockerfile in (
        "legacy_system/Dockerfile",
        "edge_gateway/Dockerfile",
        "cloud_service/Dockerfile",
    ):
        assert f"docker build --file {dockerfile}" in workflow

    clean_environment = workflow[workflow.index("  clean-environment:") :]
    assert "needs: [secure-e2e, docker-build]" in clean_environment
    assert "uv sync --frozen" in clean_environment
    assert "docker compose config --quiet" in clean_environment
    assert "uv run pytest tests/integration/test_gateway_compose_e2e.py" in clean_environment


def test_integration_job_keeps_the_complete_integration_suite() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    integration = workflow[
        workflow.index("  integration-tests:") : workflow.index("  secure-e2e:")
    ]

    assert "name: Run all integration tests" in integration
    assert "uv run pytest tests/integration" in integration


def test_ai_history_readme_documents_the_clean_ci_compatibility_commands() -> None:
    document = AI_HISTORY_README.read_text(encoding="utf-8")

    assert "## Clean-environment compatibility" in document
    for command in (
        "uv sync --frozen",
        "uv run ai-history --help",
        "uv run ai-history status",
        "uv run ai-history list",
        "uv run ai-history check",
    ):
        assert command in document
    assert "currently has no\n`interaction` command" in document
