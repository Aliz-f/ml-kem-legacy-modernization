"""Regression coverage for the M5-31 full baseline measurement harness."""

import importlib.util
from pathlib import Path

import pytest


spec = importlib.util.spec_from_file_location(
    "measure_baseline_e2e", Path(__file__).parents[1] / "scripts" / "measure_baseline_e2e.py"
)
harness = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(harness)


def test_harness_observes_real_classical_end_to_end_path() -> None:
    report = harness.run(samples=2)

    assert report["security_mode"] == "classical"
    assert report["configuration"] == {
        "failure_mode": "none",
        "legacy_request_timeout_seconds": 5,
        "legacy_max_retries": 0,
        "gateway_cloud_timeout_seconds": 5,
        "gateway_cloud_max_retries": 0,
        "workload": "sequential requests with no warmup or concurrent load",
    }
    assert set(report["environment"]) == {
        "python", "os", "machine", "sqlite", "fastapi", "httpx", "uvicorn"
    }
    assert report["successful_messages"] == report["persisted_rows"] == 2
    assert report["cloud_requests"] == 2
    assert report["gateway_cloud_retry_count"] == 0
    for field in (
        "legacy_gateway_end_to_end_ms",
        "gateway_request_ms",
        "gateway_cloud_request_ms",
        "cloud_storage_ms",
        "canonical_payload_bytes",
    ):
        assert report[field]["count"] == 2


@pytest.mark.parametrize("samples", [0, 101, True])
def test_harness_rejects_invalid_sample_counts(samples: object) -> None:
    with pytest.raises(ValueError):
        harness.run(samples)
