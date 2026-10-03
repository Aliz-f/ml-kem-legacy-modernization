"""Gateway fault execution against a live Cloud and disposable SQLite database."""

from fastapi import Request
from fastapi.testclient import TestClient
import pytest

from cloud_service.app import create_app as create_cloud
from cloud_service.config import load_config as cloud_config
from edge_gateway.app import create_app
from edge_gateway.config import load_config
from test_gateway_baseline_integration import live_service
from test_gateway_measurements import PATH, PAYLOAD


@pytest.mark.parametrize("security_mode", ["classical", "mlkem"])
@pytest.mark.parametrize(("fault", "rate", "status", "stored"), [
    ("processing_error", "1", 500, False),
    ("processing_delay", "1", 202, True),
    ("cloud_timeout", "1", 503, False),
    ("cloud_unavailable", "1", 503, False),
    ("drop_message", "1", 503, False),
    ("none", "1", 202, True),
    ("random", "0", 202, True),
])
def test_faults_preserve_real_cloud_storage_and_mode_boundaries(
    tmp_path, security_mode, fault, rate, status, stored,
):
    cloud = create_cloud(cloud_config({
        "DATABASE_URL": f"sqlite:///{tmp_path / 'faults.db'}", "SECURITY_MODE": security_mode,
    }))
    posts = []

    @cloud.middleware("http")
    async def capture(request: Request, call_next):
        if request.method == "POST":
            posts.append(request.url.path)
        return await call_next(request)

    with live_service(cloud, "cloud_service") as (url, query):
        app = create_app(load_config({
            "CLOUD_URL": url, "SECURITY_MODE": security_mode,
            "FAILURE_MODE": fault, "FAILURE_RATE": rate,
            "FAILURE_DELAY_SECONDS": "0.001", "CLOUD_MAX_RETRIES": "0",
        }))
        with TestClient(app) as client:
            assert client.post(PATH, json=PAYLOAD).status_code == status
            assert client.post(PATH, json=PAYLOAD).status_code == 409
            assert client.get("/health").status_code == 200
        rows = query.get("/api/v1/measurements").json()["items"]
        assert len(rows) == int(stored)
        measurement_posts = [p for p in posts if p.endswith("/measurements")]
        expected_path = f"/api/v1/{'baseline' if security_mode == 'classical' else 'secure'}/measurements"
        assert measurement_posts == ([expected_path] if stored else [])
        if security_mode == "mlkem":
            assert "/api/v1/baseline/measurements" not in posts
        if fault in {"processing_error", "drop_message"}:
            assert posts == []  # No handshake or measurement forwarding.


def test_seeded_random_execution_repeats_without_leaking_to_later_requests(tmp_path):
    cloud = create_cloud(cloud_config({
        "DATABASE_URL": f"sqlite:///{tmp_path / 'random.db'}", "SECURITY_MODE": "classical",
    }))
    runs = []
    with live_service(cloud, "cloud_service") as (url, query):
        for run in range(2):
            app = create_app(load_config({
                "CLOUD_URL": url, "SECURITY_MODE": "classical",
                "FAILURE_MODE": "random", "FAILURE_RATE": "0.5",
                "FAILURE_SEED": "repeatable", "FAILURE_DELAY_SECONDS": "0",
                "CLOUD_MAX_RETRIES": "0",
            }))
            with TestClient(app) as client:
                results = []
                for sequence in range(1, 41):
                    if run == 1:
                        # Invalid requests must not consume the seeded sequence.
                        assert client.post(PATH, content=b"{").status_code == 400
                    results.append(client.post(PATH, json={
                        **PAYLOAD, "device_id": f"sensor-{run}", "sequence_number": sequence,
                    }).status_code)
                counters = [line for line in client.get("/metrics").text.splitlines()
                            if line.startswith("gateway_injected_failures_total{")]
                runs.append((results, counters))
        assert runs[0] == runs[1]
        assert set(runs[0][0]) == {202, 500, 503}
        assert len(query.get("/api/v1/measurements").json()["items"]) == 2 * runs[0][0].count(202)
