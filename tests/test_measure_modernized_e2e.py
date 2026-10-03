"""Regression coverage for the M5-65 through M5-69 ML-KEM measurement harness."""

import importlib.util
from pathlib import Path

import pytest


def _load(name: str):
    path = Path(__file__).parents[1] / "scripts" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


modernized = _load("measure_modernized_e2e.py")
comparison = _load("measure_mode_comparison.py")


def test_harness_separates_first_secure_message_and_reused_session_messages() -> None:
    report = modernized.run(samples=3)

    assert report["security_mode"] == "mlkem"
    assert report["configuration"] == {
        "failure_mode": "none",
        "log_level": "WARNING",
        "legacy_request_timeout_seconds": 5,
        "legacy_max_retries": 0,
        "gateway_cloud_timeout_seconds": 5,
        "gateway_cloud_max_retries": 0,
        "pqc_failure_policy": "fail_closed",
        "workload": "sequential requests with no warmup or concurrent load",
    }
    assert report["successful_messages"] == report["persisted_rows"] == 3
    assert report["cloud_requests"] == report["samples"] == 3
    assert report["gateway_cloud_retry_count"] == 0
    assert report["first_message"]["legacy_gateway_end_to_end_ms"]["count"] == 1
    assert report["steady_state"]["legacy_gateway_end_to_end_ms"]["count"] == 2
    assert report["secure_envelope_bytes"]["count"] == 3
    assert report["cloud_storage_ms"]["count"] == 3
    assert report["secure_envelope_bytes"]["median"] > 0
    session = report["session_establishment"]
    assert session["gateway_handshakes"] == 1
    assert session["gateway_handshake_failures"] == 0
    assert session["gateway_active_session"] == 1
    assert session["gateway_session_reestablishments"] == 0
    assert session["gateway_encryption_failures"] == 0
    assert session["gateway_pqc_fallbacks"] == 0
    assert session["cloud_sessions_created"] == 1
    assert session["cloud_session_failures"] == 0
    assert session["cloud_active_sessions"] == 1
    assert session["cloud_decryption_failures"] == 0
    for field in (
        "gateway_handshake_ms",
        "gateway_public_key_ms",
        "gateway_encapsulation_ms",
        "cloud_decapsulation_ms",
    ):
        assert session[field]["count"] == 1


def test_matched_comparison_uses_reports_from_one_equivalent_workload() -> None:
    report = comparison.run(samples=2)

    assert report["samples"] == 2
    values = report["comparison"]
    assert values["first_message_latency_ms"]["classical"]["count"] == 1
    assert values["first_message_latency_ms"]["mlkem"]["count"] == 1
    assert values["steady_state_latency_ms"]["classical"]["count"] == 1
    assert values["steady_state_latency_ms"]["mlkem"]["count"] == 1
    assert values["gateway_to_cloud_payload_bytes"]["mlkem"]["median"] > values[
        "gateway_to_cloud_payload_bytes"
    ]["classical"]["median"]
    assert values["session_setup"]["classical"] == "not_applicable"
    assert values["session_setup"]["mlkem"]["gateway_handshakes"] == 1
    assert values["successful_messages"] == {"classical": 2, "mlkem": 2}
    assert values["failed_messages"] == {
        "classical": 2 - values["successful_messages"]["classical"],
        "mlkem": 2 - values["successful_messages"]["mlkem"],
    }
    assert values["failed_messages"] == {"classical": 0, "mlkem": 0}
    assert values["storage_success"] == {"classical": 2, "mlkem": 2}


@pytest.mark.parametrize("samples", [0, 1, 101, True])
def test_modernized_harness_and_comparison_reject_uncomparable_workloads(samples: object) -> None:
    with pytest.raises(ValueError):
        modernized.run(samples)
    with pytest.raises(ValueError):
        comparison.run(samples)
