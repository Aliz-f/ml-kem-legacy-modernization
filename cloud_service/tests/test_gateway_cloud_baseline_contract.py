"""M4-69 Cloud-side Gateway baseline contract, using the shared fixture only."""

import json
import logging
from pathlib import Path

from fastapi.testclient import TestClient

from cloud_service.app import create_app
from cloud_service.config import load_config


FIXTURE = Path(__file__).parents[2] / "tests" / "fixtures" / "canonical_measurement.json"
ENDPOINT = "/api/v1/baseline/measurements"


def test_shared_canonical_fixture_is_accepted_and_preserves_the_baseline_contract(caplog) -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    request_id = "req-m4-69-contract"
    expected_fields = {
        "device_id", "temperature_c", "humidity_pct", "measured_at",
        "sequence_number", "received_at", "gateway_id",
    }
    assert set(payload) == expected_fields
    assert "request_id" not in payload
    assert payload["gateway_id"]

    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        with caplog.at_level(logging.INFO, logger="cloud_service"):
            first = client.post(ENDPOINT, json=payload, headers={"X-Request-ID": request_id})
            duplicate = client.post(ENDPOINT, json=payload, headers={"X-Request-ID": request_id})
        assert first.status_code == duplicate.status_code == 202
        record_id = first.json()["record_id"]
        assert first.json() == {"status": "accepted", "record_id": record_id}
        assert duplicate.json() == {"status": "already_accepted", "record_id": record_id}
        stored = client.app.state.repository.get(record_id)

    assert stored is not None
    assert stored.gateway_id == payload["gateway_id"]
    assert stored.device_id == payload["device_id"]
    assert stored.sequence_number == payload["sequence_number"]
    assert stored.measured_at.isoformat().replace("+00:00", "Z") == payload["measured_at"]
    assert stored.gateway_received_at.isoformat().replace("+00:00", "Z") == payload["received_at"]
    assert request_id in caplog.text
