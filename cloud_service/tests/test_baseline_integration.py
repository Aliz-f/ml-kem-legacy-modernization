"""Exercise the real Gateway serializer through Cloud HTTP and file SQLite."""

import importlib.util
from pathlib import Path

import pytest


spec = importlib.util.spec_from_file_location(
    "measure_baseline", Path(__file__).resolve().parents[1] / "tools" / "measure_baseline.py",
)
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


def test_serializer_http_sqlite_query_integration():
    result = harness.run(samples=3)
    assert result["successful_inserts"] == result["persisted_rows_after_reopen"] == 3
    assert result["insert_request_ms"]["count"] == result["insert_storage_ms"]["count"] == 3
    assert result["duplicate"]["same_record_id"] is True
    assert result["storage_failure"]["persisted"] is False


@pytest.mark.parametrize("samples", [0, 1001, True])
def test_harness_rejects_invalid_sample_count(samples):
    with pytest.raises(ValueError):
        harness.run(samples)
