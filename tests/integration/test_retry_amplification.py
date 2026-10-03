"""M2-46/47 bounded retry propagation and amplification evidence."""

from __future__ import annotations

from contextlib import contextmanager
from io import BytesIO
import socket
from threading import Thread
from time import monotonic, sleep
from urllib.error import HTTPError
from urllib.request import urlopen

import uvicorn

from edge_gateway.app import create_app
from edge_gateway.cloud.baseline import BaselineCloudClient, BaselineCloudError
from edge_gateway.config import load_config
from legacy_system.client import GatewayClient


PAYLOAD = {
    "device_id": "sensor-retry", "temperature_c": 22.5, "humidity_pct": 44.0,
    "timestamp": "2026-09-21T12:00:00Z", "sequence_number": 10,
}


@contextmanager
def _live_gateway(transport: BaselineCloudClient):
    app = create_app(load_config({"SECURITY_MODE": "classical"}), baseline_transport=transport)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        server = uvicorn.Server(uvicorn.Config(
            app, log_config=None, access_log=False, lifespan="on",
            timeout_graceful_shutdown=5,
        ))
        thread = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            deadline = monotonic() + 10
            while not server.started and thread.is_alive() and monotonic() < deadline:
                sleep(0.01)
            assert server.started
            yield f"http://127.0.0.1:{listener.getsockname()[1]}"
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            assert not thread.is_alive()


def test_real_gateway_failure_chain_is_bounded_by_committed_sequence_state() -> None:
    cloud_attempts: list[bytes] = []
    cloud_backoffs: list[float] = []
    legacy_backoffs: list[float] = []
    gateway_statuses: list[int] = []
    transport = BaselineCloudClient(
        cloud_url="http://cloud.invalid", timeout_seconds=1, max_retries=2,
        sleep=cloud_backoffs.append,
    )

    def unavailable(body: bytes, request_id: str):
        cloud_attempts.append(body)
        raise BaselineCloudError("storage unavailable", retryable=True, code="STORAGE_UNAVAILABLE")

    transport._post_request = unavailable  # type: ignore[method-assign]

    def observe_gateway(request, timeout):
        try:
            return urlopen(request, timeout=timeout)
        except HTTPError as error:
            gateway_statuses.append(error.code)
            raise

    with _live_gateway(transport) as gateway_url:
        result = GatewayClient(
            gateway_url, request_timeout_seconds=5, opener=observe_gateway, max_retries=2,
            sleeper=legacy_backoffs.append,
        ).send(PAYLOAD)

    # Gateway exhausts its 3 Cloud attempts and returns 503. The Legacy retry
    # then receives frozen 409 DUPLICATE_SEQUENCE, so it must stop immediately.
    assert result.success is False
    assert result.status_code == 409
    assert result.retryable is False
    assert result.attempt_count == 2
    assert gateway_statuses == [503, 409]
    assert cloud_backoffs == [1.0, 2.0]
    assert legacy_backoffs == [1]
    assert len(cloud_attempts) == 3
    assert cloud_attempts[0] == cloud_attempts[1] == cloud_attempts[2]
    metrics = transport.metrics.render()
    assert "gateway_cloud_requests_total 3" in metrics
    assert "gateway_cloud_failures_total 3" in metrics
    assert "gateway_cloud_retries_total 2" in metrics


def test_theoretical_retry_amplification_product_is_explicit_and_bounded() -> None:
    legacy_attempts = 0
    simulated_cloud_attempts = 0
    delays: list[float] = []

    def gateway_503(_request, timeout):
        nonlocal legacy_attempts, simulated_cloud_attempts
        assert timeout == 1
        legacy_attempts += 1
        simulated_cloud_attempts += 3  # initial Cloud send + two bounded retries
        raise HTTPError("", 503, "unavailable", {}, BytesIO(b""))

    result = GatewayClient(
        "http://gateway.invalid", 1, opener=gateway_503,
        max_retries=2, sleeper=delays.append,
    ).send(PAYLOAD)

    assert result.status_code == 503 and result.retryable is True
    assert result.attempt_count == legacy_attempts == 3
    assert simulated_cloud_attempts == 9
    assert delays == [1, 2]
