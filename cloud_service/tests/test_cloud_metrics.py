"""M4-55/M4-56 bounded Cloud metrics and observability tests."""

from fastapi.testclient import TestClient
import pytest

from cloud_service.app import create_app
from cloud_service.config import FailureMode, load_config
from cloud_service.failure import FailureInjector
from cloud_service.metrics import CloudMetrics


PAYLOAD = {
    "device_id": "sensor-metrics",
    "gateway_id": "gateway-metrics",
    "temperature_c": 22.5,
    "humidity_pct": 44.0,
    "sequence_number": 1,
    "measured_at": "2026-09-21T12:00:00Z",
    "received_at": "2026-09-21T12:00:01Z",
}


def test_baseline_metrics_count_requests_storage_and_idempotent_duplicates() -> None:
    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        assert client.post("/api/v1/baseline/measurements", json=PAYLOAD).status_code == 202
        assert client.post("/api/v1/baseline/measurements", json=PAYLOAD).json()["status"] == "already_accepted"
        rendered = client.get("/metrics").text

    assert "cloud_baseline_requests_total 2" in rendered
    assert "cloud_measurements_stored_total 1" in rendered
    assert "cloud_duplicate_measurements_total 1" in rendered
    assert "cloud_request_duration_seconds_count 2" in rendered
    for metric in (
        "cloud_secure_requests_total", "cloud_secure_requests_rejected_total",
        "cloud_mlkem_sessions_created_total", "cloud_mlkem_session_failures_total",
        "cloud_expired_sessions_total", "cloud_authenticated_messages_total",
        "cloud_decryption_failures_total", "cloud_storage_failures_total",
        "cloud_injected_failures_total",
    ):
        assert metric in rendered
    for forbidden in ("request_id", "session_id", "record_id", "device_id", "gateway_id", "key_id"):
        assert forbidden not in rendered


def test_metrics_reject_unbounded_or_unsupported_labels() -> None:
    metrics = CloudMetrics()

    with pytest.raises(ValueError, match="bounded Cloud vocabulary"):
        metrics.increment("cloud_baseline_requests_total", request_id="req-1")
    with pytest.raises(ValueError, match="bounded Cloud vocabulary"):
        metrics.increment("cloud_injected_failures_total", failure_type="not-a-mode")
    with pytest.raises(ValueError, match="frozen Cloud counter family"):
        metrics.increment("cloud_measurement_by_device_total")


def test_injected_fault_is_counted_only_when_its_boundary_applies() -> None:
    applied: list[str] = []
    injector = FailureInjector(
        FailureMode.DECRYPTION_FAILURE, 1.0, 7, 0,
        on_applied=applied.append,
    )
    selection = injector.select((FailureMode.DECRYPTION_FAILURE,))

    assert applied == []
    assert selection.apply(FailureMode.DECRYPTION_FAILURE)
    assert selection.apply(FailureMode.DECRYPTION_FAILURE)
    assert applied == ["decryption_failure"]
