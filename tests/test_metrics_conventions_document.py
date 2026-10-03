"""Regression checks for the frozen Member 5 metrics contract."""

from pathlib import Path


CONVENTIONS = Path(__file__).parents[1] / "docs/operations/METRICS_CONVENTIONS.md"


GATEWAY_METRICS = (
    "gateway_measurements_received_total", "gateway_measurements_accepted_total",
    "gateway_measurements_rejected_total", "gateway_duplicate_measurements_total",
    "gateway_out_of_order_measurements_total", "gateway_sequence_gaps_total",
    "gateway_cloud_requests_total", "gateway_cloud_failures_total",
    "gateway_cloud_retries_total", "gateway_cloud_request_duration_seconds",
    "gateway_mlkem_handshakes_total", "gateway_mlkem_handshake_failures_total",
    "gateway_mlkem_handshake_duration_seconds", "gateway_session_reestablishments_total",
    "gateway_encryption_failures_total", "gateway_active_session",
    "gateway_pqc_fallback_total", "gateway_injected_failures_total",
)

CLOUD_METRICS = (
    "cloud_baseline_requests_total", "cloud_secure_requests_total",
    "cloud_secure_requests_rejected_total", "cloud_request_duration_seconds",
    "cloud_mlkem_sessions_created_total", "cloud_mlkem_session_failures_total",
    "cloud_mlkem_decapsulation_duration_seconds", "cloud_active_sessions",
    "cloud_expired_sessions_total", "cloud_authenticated_messages_total",
    "cloud_decryption_failures_total", "cloud_measurements_stored_total",
    "cloud_storage_failures_total", "cloud_duplicate_measurements_total",
    "cloud_injected_failures_total",
)


def test_metrics_conventions_include_every_frozen_minimum_family() -> None:
    document = CONVENTIONS.read_text(encoding="utf-8")

    for metric in GATEWAY_METRICS + CLOUD_METRICS:
        assert f"`{metric}`" in document


def test_metrics_conventions_preserve_fail_closed_and_cardinality_rules() -> None:
    document = CONVENTIONS.read_text(encoding="utf-8")

    assert "Must remain `0`" in document
    assert "runtime plaintext fallback is prohibited" in document
    for forbidden in (
        "request_id", "session_id", "record_id", "device_id", "gateway_id", "key_id",
    ):
        assert f"`{forbidden}`" in document
    for permitted in ("`result`", "`failure_type`", "`security_mode`", "`phase`"):
        assert permitted in document


def test_metrics_conventions_link_component_observation_points() -> None:
    document = CONVENTIONS.read_text(encoding="utf-8")

    assert "../../edge_gateway/docs/gateway-pr9.md" in document
    assert "Component\nimplementations and their tests" in document
    assert "M5-54" in document
