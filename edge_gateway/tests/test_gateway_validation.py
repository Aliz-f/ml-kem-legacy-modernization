"""M2-04 HTTP syntax/schema boundary and rejection before Cloud access."""

import json
import socket

from fastapi.testclient import TestClient
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from edge_gateway.models import LegacyMeasurement
from edge_gateway.validation import parse_legacy_measurement


@pytest.fixture
def payload():
    return {
        "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
        "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 184,
    }


@pytest.fixture(params=["classical", "mlkem"])
def client(request, monkeypatch):
    def forbidden_network(*args, **kwargs):
        pytest.fail("Schema validation attempted an outbound network connection")

    config = load_config({"SECURITY_MODE": request.param})
    with TestClient(create_app(config)) as client:
        monkeypatch.setattr(socket.socket, "connect", forbidden_network)
        monkeypatch.setattr(socket.socket, "connect_ex", forbidden_network)
        yield client


def assert_rejection(client, body, status, code):
    response = client.post(
        "/api/v1/measurements", content=body, headers={"Content-Type": "application/json"},
    )
    assert response.status_code == status
    message = (
        "request body must be valid JSON" if status == 400 else "measurement validation failed"
    )
    assert response.json() == {"error": {"code": code, "message": message}}


@pytest.mark.parametrize("body", [
    b"", b" ", b"{", b'{"device_id":', b'{"device_id":"private-marker",}',
    b"{'device_id': 'sensor-001'}", b'{} {}', b'{"device_id":"\xff"}',
    b'NaN', b'Infinity', b'-Infinity', pytest.param(b'[' * 2000, id="deep-incomplete-json"),
])
def test_malformed_json_is_400(client, body, caplog):
    assert_rejection(client, body, 400, "INVALID_JSON")
    assert "private-marker" not in caplog.text


@pytest.mark.parametrize("field", [
    "device_id", "temperature_c", "humidity_pct", "timestamp", "sequence_number",
])
def test_missing_required_fields_are_422(client, payload, field):
    del payload[field]
    assert_rejection(client, json.dumps(payload), 422, "INVALID_MEASUREMENT")


@pytest.mark.parametrize(("field", "value"), [
    ("device_id", None), ("device_id", 7),
    ("temperature_c", "hot"), ("temperature_c", True), ("temperature_c", None),
    ("humidity_pct", None), ("humidity_pct", "42.5"), ("humidity_pct", []),
    ("sequence_number", False), ("sequence_number", "184"), ("sequence_number", 1.0),
    ("timestamp", 123), ("timestamp", None), ("timestamp", "invalid-private-marker"),
])
def test_wrong_types_and_timestamp_are_422(client, payload, field, value, caplog):
    payload[field] = value
    assert_rejection(client, json.dumps(payload), 422, "INVALID_MEASUREMENT")
    assert "invalid-private-marker" not in caplog.text


@pytest.mark.parametrize("body", ["null", "[]", '"string"', "1", "true", "{}"])
def test_parsed_non_measurements_are_422(client, body):
    assert_rejection(client, body, 422, "INVALID_MEASUREMENT")


def test_extra_field_is_422(client, payload, caplog):
    payload["private-extra-name"] = "private-extra-value"
    assert_rejection(client, json.dumps(payload), 422, "INVALID_MEASUREMENT")
    assert "private-extra" not in caplog.text


def test_valid_json_number_overflow_is_schema_error(client, payload):
    body = json.dumps(payload).replace("21.7", "1e400")
    assert_rejection(client, body, 422, "INVALID_MEASUREMENT")


def test_valid_measurement_parses_but_is_not_accepted_before_delivery(client, payload):
    model = parse_legacy_measurement(json.dumps(payload).encode())
    assert isinstance(model, LegacyMeasurement)
    assert model.to_dict() == payload
    assert client.post("/api/v1/measurements", json=payload).status_code == 503


def test_domain_bounds_remain_a_separate_stage(payload):
    payload.update(device_id="", temperature_c=86, humidity_pct=-1, sequence_number=-1)
    assert parse_legacy_measurement(json.dumps(payload).encode()).to_dict() == payload
