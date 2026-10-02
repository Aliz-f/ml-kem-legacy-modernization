"""Keep the M5-32 baseline measurement record reproducible and bounded."""

from pathlib import Path


METHOD = Path(__file__).parents[1] / "docs/evaluation/baseline-measurement-method.md"


def test_baseline_measurement_method_records_required_reproducibility_inputs() -> None:
    document = METHOD.read_text(encoding="utf-8")

    for value in (
        "--samples 10",
        "SECURITY_MODE=classical",
        "FAILURE_MODE=none",
        "zero retries",
        "5 s timeout",
        "loopback HTTP",
        "temporary file-backed SQLite",
        "sequential",
    ):
        assert value in document


def test_baseline_measurement_method_preserves_metric_boundaries_and_scope() -> None:
    document = METHOD.read_text(encoding="utf-8")
    normalized = " ".join(document.split())

    for field in (
        "legacy_gateway_end_to_end_ms",
        "gateway_request_ms",
        "gateway_cloud_request_ms",
        "cloud_storage_ms",
        "canonical_payload_bytes",
        "gateway_cloud_retry_count",
    ):
        assert field in document
    assert "not a comparison with Modernized Mode" in normalized
