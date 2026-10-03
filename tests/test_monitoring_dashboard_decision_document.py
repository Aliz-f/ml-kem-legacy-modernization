"""Regression checks for the deliberately small M5-56 monitoring decision."""

from pathlib import Path


DECISION = Path(__file__).parents[1] / "docs/operations/MONITORING_DASHBOARD_DECISION.md"


def test_m5_56_declines_unneeded_monitoring_infrastructure_with_evidence() -> None:
    document = DECISION.read_text(encoding="utf-8")

    for value in (
        "M5-56",
        "Do not add Grafana",
        "Prometheus server",
        "GET /metrics",
        "METRICS_CONVENTIONS.md",
        "test_observability_integration.py",
        "test_gateway_compose_e2e.py",
        "request_id",
        "session_id",
        "Revisit conditions",
    ):
        assert value in document
