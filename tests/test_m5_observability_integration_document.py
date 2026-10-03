"""Regression checks for the M5-47 through M5-51 evidence runbook."""

from pathlib import Path


DOCUMENT = Path(__file__).parents[1] / "docs/testing/M5_OBSERVABILITY_INTEGRATION.md"


def test_observability_runbook_references_live_trace_metrics_and_log_safety() -> None:
    document = DOCUMENT.read_text(encoding="utf-8")

    for value in (
        "M5-47 through M5-51",
        "sequence_number=42",
        "X-Request-ID",
        "SecureEnvelope.request_id",
        "record_id",
        "/metrics",
        "shared secret",
        "derived session key",
        "test_gateway_compose_e2e.py",
    ):
        assert value in document
