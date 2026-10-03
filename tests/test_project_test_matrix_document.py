"""Regression checks for the M5-72 project-wide test inventory."""

from pathlib import Path


MATRIX = Path(__file__).parents[1] / "docs/testing/PROJECT_TEST_MATRIX.md"


def test_project_matrix_covers_the_required_areas_and_test_layers() -> None:
    document = MATRIX.read_text(encoding="utf-8")

    for area in (
        "Legacy Device",
        "Gateway application",
        "Gateway crypto and sessions",
        "Cloud API and crypto",
        "SQLite storage",
        "Deployment and CI",
    ):
        assert area in document
    assert "| Unit | Contract | Integration | E2E | Failure / security |" in document


def test_project_matrix_indexes_real_evidence_and_the_resolved_compose_gap() -> None:
    document = MATRIX.read_text(encoding="utf-8")

    for path in (
        "legacy_system/tests/",
        "edge_gateway/tests/test_mlkem.py",
        "cloud_service/tests/test_cloud_storage.py",
        "tests/integration/test_gateway_compose_e2e.py",
        "docs/testing/M5_FAILURE_AUTOMATION.md",
    ):
        assert path in document
    assert "TM-1 was\nresolved" in document
    assert "test_compose_cloud_restart_recovers_readiness_and_delivery" in document
    assert "selected explicitly in CI" in document


def test_project_matrix_preserves_evaluation_and_protocol_scope_limits() -> None:
    document = MATRIX.read_text(encoding="utf-8")

    assert "not a coverage report" in document
    assert "Coverage percentages are intentionally absent" in document
    assert "fail closed without a baseline fallback" in document
    assert "same already-built envelope" in document
    assert "no cryptographic replay counter or window" in document
