"""M2-06 stable HTTP error contracts and safe application failure responses."""

from fastapi.testclient import TestClient
import pytest

from edge_gateway import app as app_module
from edge_gateway.config import load_config
from edge_gateway.errors import GatewayError, GatewayErrorCode
from edge_gateway.models import LegacyMeasurementSchemaError
from edge_gateway.validation import LegacyJSONError, LegacyMeasurementDomainError


PRIVATE_DETAIL = "private-marker /srv/private/file.py ValueError ML-KEM library internals"
PAYLOAD = {
    "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
    "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 184,
}


@pytest.fixture(params=["classical", "mlkem"])
def client(request):
    app = app_module.create_app(load_config({"SECURITY_MODE": request.param}))
    # Observe the actual HTTP 500 body rather than TestClient re-raising failures.
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client


@pytest.mark.parametrize(("code", "status", "message"), [
    ("INVALID_JSON", 400, "request body must be valid JSON"),
    ("INVALID_MEASUREMENT", 422, "measurement validation failed"),
    ("DUPLICATE_SEQUENCE", 409, "duplicate sequence number"),
    ("OUT_OF_ORDER_SEQUENCE", 409, "out-of-order sequence number"),
    ("CLOUD_UNAVAILABLE", 503, "cloud service is unavailable"),
    ("INTERNAL_ERROR", 500, "internal gateway error"),
    ("SERVICE_UNAVAILABLE", 503, "service is not ready"),
])
def test_application_errors_have_stable_http_contract(client, monkeypatch, code, status, message):
    def fail(measurement):
        # Simulate a later policy stage without implementing sequencing/transport.
        raise GatewayError(GatewayErrorCode[code]) from RuntimeError(PRIVATE_DETAIL)

    monkeypatch.setattr(app_module, "validate_legacy_measurement", fail)
    response = client.post("/api/v1/measurements", json=PAYLOAD)
    assert response.status_code == status
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"error": {"code": code, "message": message}}


@pytest.mark.parametrize(("error_type", "status", "code", "message"), [
    (LegacyJSONError, 400, "INVALID_JSON", "request body must be valid JSON"),
    (LegacyMeasurementSchemaError, 422, "INVALID_MEASUREMENT", "measurement validation failed"),
    (LegacyMeasurementDomainError, 422, "INVALID_MEASUREMENT", "measurement validation failed"),
    (RuntimeError, 500, "INTERNAL_ERROR", "internal gateway error"),
    (ValueError, 500, "INTERNAL_ERROR", "internal gateway error"),
])
def test_exception_details_are_not_exposed(
    client, monkeypatch, caplog, error_type, status, code, message,
):
    def fail(body):
        raise error_type(PRIVATE_DETAIL)

    monkeypatch.setattr(app_module, "parse_legacy_measurement", fail)
    response = client.post("/api/v1/measurements", json=PAYLOAD)
    assert response.status_code == status
    assert response.json() == {"error": {"code": code, "message": message}}
    assert "private-marker" not in caplog.text
    if status == 500:
        records = [r for r in caplog.records if r.name == "edge_gateway"]
        assert any(
            r.message == "event=gateway_internal_error component=edge_gateway"
            for r in records
        )
        assert all(r.exc_info is None for r in records)


def test_internal_failure_outside_measurement_route_is_sanitized(client, monkeypatch):
    def fail():
        raise RuntimeError(PRIVATE_DETAIL)

    client.app.dependency_overrides[app_module.get_config] = fail
    response = client.get("/metrics")
    assert response.status_code == 500
    assert response.json() == {
        "error": {"code": "INTERNAL_ERROR", "message": "internal gateway error"},
    }


def test_public_error_bodies_are_independent():
    first = GatewayErrorCode.INVALID_MEASUREMENT.to_dict()
    first["error"]["message"] = PRIVATE_DETAIL
    assert GatewayErrorCode.INVALID_MEASUREMENT.to_dict() == {
        "error": {"code": "INVALID_MEASUREMENT", "message": "measurement validation failed"},
    }
