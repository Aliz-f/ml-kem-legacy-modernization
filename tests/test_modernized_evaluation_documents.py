"""Keep the M5-65 through M5-70 evaluation guidance reproducible and bounded."""

from pathlib import Path


ROOT = Path(__file__).parents[1]
MODERNIZED = ROOT / "docs/evaluation/modernized-measurement-method.md"
COMPARISON = ROOT / "docs/evaluation/baseline-vs-modernized-comparison.md"


def test_modernized_method_preserves_the_matched_workload_and_session_boundaries() -> None:
    document = MODERNIZED.read_text(encoding="utf-8")

    for value in (
        "M5-65 through M5-69",
        "scripts/measure_modernized_e2e.py --samples 10",
        "sensor-baseline-harness",
        "PQC_FAILURE_POLICY=fail_closed",
        "first secure message",
        "steady-state",
        "SecureEnvelope JSON bytes",
        "Cloud decapsulation duration",
        "no secret value is printed or persisted",
    ):
        assert value in document


def test_comparison_table_is_generated_from_real_matched_measurements() -> None:
    document = COMPARISON.read_text(encoding="utf-8")

    for value in (
        "M5-70",
        "scripts/measure_mode_comparison.py --samples 10",
        "First-message latency",
        "Steady-state latency",
        "Gateway→Cloud payload size",
        "Session setup",
        "Successful messages",
        "Failed messages",
        "Storage success",
        "instead of copying fixed numbers",
    ):
        assert value in document
