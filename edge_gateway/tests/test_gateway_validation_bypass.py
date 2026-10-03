"""M2-48 configured failure paths remain strictly after Legacy validation."""

from fastapi.testclient import TestClient
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import KNOWN_FAILURE_MODES, load_config


PATH = "/api/v1/measurements"
INVALID = {
    "device_id": "sensor-invalid", "temperature_c": 22.5, "humidity_pct": 100.1,
    "timestamp": "2026-09-21T12:00:00Z", "sequence_number": 10,
}


class TransportSpy:
    def __init__(self) -> None:
        self.calls = 0

    async def send(self, **_fields: object) -> object:
        self.calls += 1
        raise AssertionError("invalid input reached Cloud transport")


@pytest.mark.parametrize("security_mode", ["classical", "mlkem"])
@pytest.mark.parametrize("failure_mode", sorted(KNOWN_FAILURE_MODES - {"none"}))
def test_configured_failure_never_bypasses_domain_validation(security_mode, failure_mode) -> None:
    baseline, secure = TransportSpy(), TransportSpy()
    app = create_app(
        load_config({
            "SECURITY_MODE": security_mode, "FAILURE_MODE": failure_mode,
            "FAILURE_RATE": "1", "FAILURE_DELAY_SECONDS": "0",
        }),
        baseline_transport=baseline, secure_transport=secure,  # type: ignore[arg-type]
    )
    with TestClient(app) as client:
        response = client.post(PATH, json=INVALID)
        metrics = client.get("/metrics").text

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_MEASUREMENT"
    assert baseline.calls == secure.calls == 0
    for line in metrics.splitlines():
        if line.startswith("gateway_injected_failures_total{"):
            assert line.endswith(" 0")


@pytest.mark.parametrize("body, status", [(b"{", 400), (b"{}", 422)])
def test_random_failure_does_not_consume_or_forward_syntax_and_schema_rejections(body, status) -> None:
    transport = TransportSpy()
    app = create_app(
        load_config({"FAILURE_MODE": "random", "FAILURE_RATE": "1"}),
        baseline_transport=transport,  # type: ignore[arg-type]
    )
    with TestClient(app) as client:
        response = client.post(PATH, content=body)
        metrics = client.get("/metrics").text
    assert response.status_code == status
    assert transport.calls == 0
    assert all(
        line.endswith(" 0") for line in metrics.splitlines()
        if line.startswith("gateway_injected_failures_total{")
    )
