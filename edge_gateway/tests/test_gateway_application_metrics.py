"""PR9 counters follow local acceptance, rejection, and bounded series contracts."""

from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from edge_gateway.metrics import GatewayMetrics


PAYLOAD = {
    "device_id": "private-device-marker", "temperature_c": 21.7, "humidity_pct": 42.5,
    "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 10,
}
PATH = "/api/v1/measurements"


class Transport:
    async def send(self, **fields):
        if fields["sequence_number"] == 12:
            raise TimeoutError("private-transport-marker")
        return SimpleNamespace(status="accepted", record_id="private-record-marker")


@pytest.mark.parametrize("mode", ["classical", "mlkem"])
def test_metrics_distinguish_local_acceptance_from_cloud_delivery(mode):
    app = create_app(load_config({"SECURITY_MODE": mode}),
                     baseline_transport=Transport(), secure_transport=Transport())
    with TestClient(app) as client:
        assert client.post(PATH, content=b"{").status_code == 400
        assert client.post(PATH, json={**PAYLOAD, "humidity_pct": 101}).status_code == 422
        assert client.post(PATH, json=PAYLOAD).status_code == 202
        assert client.post(PATH, json=PAYLOAD).status_code == 409
        assert client.post(PATH, json={**PAYLOAD, "sequence_number": 9}).status_code == 409
        assert client.post(PATH, json={**PAYLOAD, "sequence_number": 12}).status_code == 503
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        text = response.text
        for name, value in {
            "measurements_received": 6, "measurements_accepted": 2,
            "measurements_rejected": 4, "duplicate_measurements": 1,
            "out_of_order_measurements": 1, "sequence_gaps": 1,
        }.items():
            assert f"gateway_{name}_total {value}\n" in text
        assert "private-" not in text
        # Export each metric family once, including the shared injection family.
        families = [line.split()[2] for line in text.splitlines() if line.startswith("# TYPE")]
        assert len(families) == len(set(families))
        assert "gateway_pqc_fallback_total 0\n" in text
        assert client.get("/metrics").text == text


def test_registry_updates_are_thread_safe_and_instances_are_isolated():
    metrics = GatewayMetrics()

    def attempt(_):
        with metrics.cloud_attempt():
            metrics.increment("measurements_received")

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(attempt, range(1000)))
    text = metrics.render()
    assert "gateway_cloud_requests_total 1000\n" in text
    assert "gateway_cloud_request_duration_seconds_count 1000\n" in text
    assert "gateway_measurements_received_total 1000\n" in text
    assert "gateway_cloud_requests_total 0\n" in GatewayMetrics().render()
    with pytest.raises(ValueError, match="Unknown Gateway metric"):
        metrics.increment("private-request-marker")
    assert "private-request-marker" not in metrics.render()


@pytest.mark.parametrize("mode", ["classical", "mlkem"])
def test_untrusted_values_do_not_create_metric_labels(mode):
    app = create_app(load_config({"SECURITY_MODE": mode}),
                     baseline_transport=Transport(), secure_transport=Transport())
    with TestClient(app) as client:
        before = client.get("/metrics").text
        for i in range(20):
            assert client.post(PATH, json={**PAYLOAD, "device_id": f"private-device-{i}"},
                               headers={"X-Request-ID": f"private-request-{i}"}).status_code == 202
        after = client.get("/metrics").text
    def series(text):
        return {line.rsplit(" ", 1)[0] for line in text.splitlines() if not line.startswith("#")}
    assert series(before) == series(after)
    for marker in ("private-", "request_id", "session_id", "device_id", "record_id", "timestamp"):
        assert marker not in after


@pytest.mark.parametrize("failure, status, attempts", [
    ("processing_error", 500, 0), ("drop_message", 503, 0),
    ("cloud_timeout", 503, 1), ("cloud_unavailable", 503, 1),
])
def test_injected_failures_are_exported_once_and_attempts_are_not_invented(failure, status, attempts):
    app = create_app(load_config({
        "SECURITY_MODE": "classical", "FAILURE_MODE": failure, "FAILURE_RATE": "1",
        "CLOUD_MAX_RETRIES": "0", "CLOUD_URL": "http://cloud.invalid",
    }))
    with TestClient(app) as client:
        assert client.post(PATH, json=PAYLOAD).status_code == status
        text = client.get("/metrics").text
        assert f'gateway_injected_failures_total{{failure_type="{failure}"}} 1\n' in text
        assert f"gateway_cloud_requests_total {attempts}\n" in text
        assert f"gateway_cloud_failures_total {attempts}\n" in text
        assert "gateway_measurements_accepted_total 1\n" in text
        assert "gateway_measurements_rejected_total 0\n" in text
