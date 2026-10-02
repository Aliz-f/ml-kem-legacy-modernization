"""Regression checks for the reviewed M5-30 classical baseline record."""

from pathlib import Path


FREEZE = Path(__file__).parents[1] / "docs/evaluation/baseline-freeze.md"


def test_baseline_freeze_record_preserves_the_classical_contract() -> None:
    document = FREEZE.read_text(encoding="utf-8")

    for value in (
        "baseline-classical-complete",
        "SECURITY_MODE=classical",
        "POST /api/v1/measurements",
        "POST /api/v1/baseline/measurements",
        "X-Request-ID",
        "UNIQUE(device_id, sequence_number)",
        "1,288 tests",
    ):
        assert value in document
    assert "not in canonical JSON" in document


def test_baseline_freeze_record_retains_measurement_and_limitation_boundaries() -> None:
    document = FREEZE.read_text(encoding="utf-8")
    normalized = " ".join(document.split())

    assert "baseline-measurements.md" in document
    for limitation in (
        "Docker Compose",
        "first-message/session-establishment",
        "cryptographic replay protection",
    ):
        assert limitation in normalized
