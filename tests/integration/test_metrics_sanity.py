"""M5-54 live Gateway and Cloud metrics sanity checks."""

from __future__ import annotations

import threading
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path

import uvicorn
from fastapi import Request

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import FailureMode, load_config as load_cloud_config
from cloud_service.failure import FailureInjector
from edge_gateway.app import create_app as create_gateway_app
from edge_gateway.config import load_config as load_gateway_config
from legacy_system.client import GatewayClient


@contextmanager
def _serve(app, name: str):
    """Run one production ASGI application on an isolated loopback port."""
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name=name, daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            server.should_exit = True
            thread.join(timeout=5)
            raise RuntimeError(f"{name} did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError(f"{name} has no listening socket")
    try:
        yield f"http://127.0.0.1:{sockets[0].getsockname()[1]}"
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        if thread.is_alive():
            raise RuntimeError(f"{name} did not stop")


def _metrics(base_url: str) -> str:
    with urllib.request.urlopen(f"{base_url}/metrics", timeout=5) as response:
        assert response.status == 200
        assert response.headers["Content-Type"].startswith("text/plain")
        return response.read().decode("utf-8")


def _payload(sequence_number: int) -> dict[str, object]:
    return {
        "device_id": "sensor-metrics",
        "temperature_c": 22.5,
        "humidity_pct": 44.0,
        "timestamp": "2026-09-21T12:00:00Z",
        "sequence_number": sequence_number,
    }


def test_five_valid_measurements_increment_gateway_and_cloud_counters(tmp_path: Path) -> None:
    cloud = create_cloud_app(load_cloud_config({
        "DATABASE_URL": f"sqlite:///{tmp_path / 'classical.db'}",
        "SECURITY_MODE": "classical",
    }))
    with _serve(cloud, "m5-54-classical-cloud") as cloud_url:
        gateway = create_gateway_app(load_gateway_config({
            "CLOUD_URL": cloud_url,
            "SECURITY_MODE": "classical",
            "CLOUD_TIMEOUT_SECONDS": "5",
            "CLOUD_MAX_RETRIES": "0",
        }))
        with _serve(gateway, "m5-54-classical-gateway") as gateway_url:
            client = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0)
            for sequence_number in range(5):
                result = client.send(_payload(sequence_number))
                assert result.success and result.status_code == 202
            gateway_metrics = _metrics(gateway_url)
            cloud_metrics = _metrics(cloud_url)

    for sample in (
        "gateway_measurements_received_total 5",
        "gateway_measurements_accepted_total 5",
        "gateway_cloud_requests_total 5",
        "gateway_cloud_request_duration_seconds_count 5",
    ):
        assert sample in gateway_metrics
    for sample in (
        "cloud_baseline_requests_total 5",
        "cloud_measurements_stored_total 5",
        "cloud_secure_requests_total 0",
        "cloud_request_duration_seconds_count 5",
    ):
        assert sample in cloud_metrics


def test_corrupted_secure_ciphertext_increments_decryption_failure_without_storage(tmp_path: Path) -> None:
    cloud = create_cloud_app(load_cloud_config({
        "DATABASE_URL": f"sqlite:///{tmp_path / 'corrupt.db'}",
        "SECURITY_MODE": "mlkem",
    }))
    with _serve(cloud, "m5-54-corrupt-cloud") as cloud_url:
        gateway = create_gateway_app(load_gateway_config({
            "CLOUD_URL": cloud_url,
            "SECURITY_MODE": "mlkem",
            "PQC_FAILURE_POLICY": "fail_closed",
            "CLOUD_TIMEOUT_SECONDS": "5",
            "CLOUD_MAX_RETRIES": "0",
            "FAILURE_MODE": "corrupt_ciphertext",
            "FAILURE_RATE": "1.0",
        }))
        with _serve(gateway, "m5-54-corrupt-gateway") as gateway_url:
            result = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0).send(
                _payload(1)
            )
            gateway_metrics = _metrics(gateway_url)
            cloud_metrics = _metrics(cloud_url)

    assert not result.success and result.status_code == 503
    assert 'gateway_injected_failures_total{failure_type="corrupt_ciphertext"} 1' in gateway_metrics
    assert "gateway_pqc_fallback_total 0" in gateway_metrics
    assert "cloud_secure_requests_total 1" in cloud_metrics
    assert "cloud_secure_requests_rejected_total 1" in cloud_metrics
    assert "cloud_decryption_failures_total 1" in cloud_metrics
    assert "cloud_measurements_stored_total 0" in cloud_metrics


def test_ambiguous_secure_retry_increments_retry_metric_and_keeps_one_row(tmp_path: Path) -> None:
    cloud = create_cloud_app(load_cloud_config({
        "DATABASE_URL": f"sqlite:///{tmp_path / 'retry.db'}",
        "SECURITY_MODE": "mlkem",
        "FAILURE_MODE": "drop_response",
        "FAILURE_RATE": "1.0",
    }))
    secure_requests = 0

    @cloud.middleware("http")
    async def clear_drop_after_first_secure_response(request: Request, call_next):
        nonlocal secure_requests
        response = await call_next(request)
        if request.url.path == "/api/v1/secure/measurements":
            secure_requests += 1
            if secure_requests == 1:
                cloud.state.failure_injector = FailureInjector(FailureMode.NONE, 0.0, None, 0)
        return response

    with _serve(cloud, "m5-54-retry-cloud") as cloud_url:
        gateway = create_gateway_app(load_gateway_config({
            "CLOUD_URL": cloud_url,
            "SECURITY_MODE": "mlkem",
            "PQC_FAILURE_POLICY": "fail_closed",
            "CLOUD_TIMEOUT_SECONDS": "5",
            "CLOUD_MAX_RETRIES": "1",
        }))
        with _serve(gateway, "m5-54-retry-gateway") as gateway_url:
            result = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0).send(
                _payload(2)
            )
            gateway_metrics = _metrics(gateway_url)
            cloud_metrics = _metrics(cloud_url)
            rows = cloud.state.repository.list()

    assert result.success and result.status_code == 202
    assert secure_requests == 2
    assert len(rows) == 1
    assert "gateway_cloud_requests_total 2" in gateway_metrics
    assert "gateway_cloud_retries_total 1" in gateway_metrics
    assert "cloud_secure_requests_total 2" in cloud_metrics
    assert "cloud_measurements_stored_total 1" in cloud_metrics
    assert "cloud_duplicate_measurements_total 1" in cloud_metrics
