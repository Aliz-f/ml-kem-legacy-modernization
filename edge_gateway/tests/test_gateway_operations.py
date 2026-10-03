"""M2-29 through M2-33 health, readiness, application logs, and privacy."""

import logging
from types import SimpleNamespace

from fastapi.testclient import TestClient

from edge_gateway.app import create_app
from edge_gateway.application_log import log_application
from edge_gateway.config import load_config


PATH = "/api/v1/measurements"
PAYLOAD = {
    "device_id": "sensor-001",
    "temperature_c": 21.7,
    "humidity_pct": 42.5,
    "timestamp": "2026-09-21T13:45:31Z",
    "sequence_number": 10,
}


class _Transport:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.calls: list[dict[str, object]] = []

    async def send(self, **fields: object) -> object:
        self.calls.append(fields)
        if self.error is not None:
            raise self.error
        return SimpleNamespace(status="accepted", record_id="rec-1")


def test_application_events_cover_success_validation_and_sequence_paths(caplog) -> None:
    transport = _Transport()
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        with TestClient(create_app(load_config({}), baseline_transport=transport)) as client:
            assert client.post(PATH, content=b"{").status_code == 400
            assert client.post(PATH, json={**PAYLOAD, "humidity_pct": 101}).status_code == 422
            assert client.post(PATH, json=PAYLOAD).status_code == 202
            assert client.post(PATH, json=PAYLOAD).status_code == 409
            assert client.post(PATH, json={**PAYLOAD, "sequence_number": 9}).status_code == 409
            assert client.post(PATH, json={**PAYLOAD, "sequence_number": 12}).status_code == 202

    for event in (
        "gateway_starting",
        "gateway_ready",
        "legacy_validation_failed",
        "legacy_measurement_received",
        "gateway_request_created",
        "canonical_measurement_created",
        "cloud_delivery_started",
        "cloud_delivery_succeeded",
        "sequence_duplicate_detected",
        "sequence_out_of_order_detected",
        "sequence_gap_detected",
        "gateway_shutting_down",
    ):
        assert f"event={event} component=edge_gateway" in caplog.text
    assert "device_id=sensor-001" in caplog.text
    assert "sequence_number=10" in caplog.text
    assert "gateway_id=gateway-001" in caplog.text
    assert "request_id=req-" in caplog.text


def test_application_logs_drop_payload_secrets_and_exception_text(caplog) -> None:
    marker = "private-payload-marker"
    transport = _Transport(RuntimeError("private-exception-marker"))
    config = load_config({
        "GATEWAY_ID": "gateway-001",
        "CLOUD_URL": "http://private-config-marker.invalid",
        "FAILURE_SEED": "private-seed-marker",
    })
    payload = {
        **PAYLOAD,
        "device_id": f"sensor\n{marker}",
        "temperature_c": 23.456789,
    }
    with caplog.at_level(logging.DEBUG):
        with TestClient(
            create_app(config, baseline_transport=transport),
            raise_server_exceptions=False,
        ) as client:
            response = client.post(PATH, json=payload)
    assert response.status_code == 500
    combined = caplog.text + response.text
    for forbidden in (
        marker,
        "private-exception-marker",
        "private-config-marker",
        "private-seed-marker",
        "23.456789",
        "temperature_c",
        "humidity_pct",
        "timestamp",
    ):
        assert forbidden not in combined


def test_application_logger_rejects_unknown_events_and_unsafe_fields(caplog) -> None:
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        log_application("unknown_event", request_id="req-private-marker")
        log_application(
            "cloud_delivery_failed",
            request_id="req-safe",
            device_id="line\nbreak",
            gateway_id=b"raw-secret",
            reason="transport failure with details",
        )
    assert "unknown_event" not in caplog.text
    assert "req-private-marker" not in caplog.text
    assert "event=cloud_delivery_failed component=edge_gateway request_id=req-safe" in caplog.text
    assert "line" not in caplog.text
    assert "raw-secret" not in caplog.text
    assert "transport failure with details" not in caplog.text
