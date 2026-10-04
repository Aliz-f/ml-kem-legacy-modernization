"""Regression checks for the M5 Compose test-environment runbook."""

from pathlib import Path


RUNBOOK = (
    Path(__file__).parents[1] / "docs" / "deployment" / "compose-test-environment.md"
)


def test_compose_test_environment_runbook_covers_lifecycle_and_verification() -> None:
    document = RUNBOOK.read_text(encoding="utf-8")

    for command in (
        "docker compose config --quiet",
        "docker compose build",
        "SECURITY_MODE=classical docker compose up --build --wait",
        "SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed docker compose up --build --wait",
        "docker compose ps",
        "docker compose logs --follow legacy-device edge-gateway cloud-service",
        "docker compose down",
        "docker compose down --volumes --remove-orphans",
    ):
        assert command in document

    for endpoint in ("/health", "/ready", "/metrics", "/api/v1/measurements"):
        assert endpoint in document


def test_compose_test_environment_runbook_preserves_operational_contracts() -> None:
    document = RUNBOOK.read_text(encoding="utf-8")

    assert "http://edge-gateway:8000" in document
    assert "http://cloud-service:9000" in document
    assert "fail-closed" in document
    assert "sessions are established lazily" in document
    assert "never cause a baseline request automatically" in document
    assert "ML-KEM private keys" in document
    assert "session keys" in document
