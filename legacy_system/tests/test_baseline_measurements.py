"""M1-16 baseline measurement test suite and data collection.

Measures the Legacy Device simulator performance, payload sizes, delivery
rates, and retry behaviors on the Legacy-to-Gateway boundary without
introducing benchmark targets or changing production runtime code.
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import math
from statistics import mean, median
import threading
from time import perf_counter
from typing import Any

from legacy_system.client import ErrorCategory, GatewayClient
from legacy_system.config import Config, FailureMode
from legacy_system.device import DeviceController
from legacy_system.sensor import Sensor


class _BaselineGatewayHandler(BaseHTTPRequestHandler):
    """Minimal loopback HTTP handler simulating the Edge Gateway endpoint."""

    server: _BaselineServer

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/v1/measurements":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        self.server.received_bytes.append(len(raw_body))

        if self.server.response_status != 202:
            self.server.attempts += 1
            self.send_response(self.server.response_status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"detail": "Simulated Gateway failure"}')
            return

        try:
            payload = json.loads(raw_body.decode("utf-8"))
            self.server.received_payloads.append(payload)
            self.server.attempts += 1
            self.send_response(202)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "accepted"}')
        except Exception:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"detail": "Invalid JSON"}')

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        # Suppress standard logging to keep pytest output clean
        pass


class _BaselineServer(HTTPServer):
    def __init__(self, server_address: tuple[str, int]) -> None:
        super().__init__(server_address, _BaselineGatewayHandler)
        self.received_payloads: list[dict[str, Any]] = []
        self.received_bytes: list[int] = []
        self.attempts: int = 0
        self.response_status: int = 202


def _start_loopback_gateway() -> tuple[_BaselineServer, str, threading.Thread]:
    server = _BaselineServer(("127.0.0.1", 0))
    host, port = server.server_address
    url = f"http://{host}:{port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, url, thread


def _calculate_distribution(values: list[float] | list[int]) -> dict[str, float]:
    if not values:
        raise ValueError("Cannot calculate distribution for empty values")
    ordered = sorted(values)
    n = len(ordered)
    p95_idx = max(0, math.ceil(n * 0.95) - 1)
    return {
        "count": float(n),
        "min": float(ordered[0]),
        "mean": float(mean(ordered)),
        "median": float(median(ordered)),
        "p95": float(ordered[p95_idx]),
        "max": float(ordered[-1]),
    }


def test_baseline_healthy_workload_100_measurements() -> None:
    """Collect baseline evidence across 100 sequential valid measurements."""
    server, gateway_url, _ = _start_loopback_gateway()
    try:
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=3.0,
            max_retries=2,
        )
        sensor = Sensor(device_id="sensor-001")

        payload_sizes: list[int] = []
        latencies_ms: list[float] = []
        delivery_successes: int = 0
        total_retries: int = 0

        for _ in range(100):
            measurement = sensor.read()
            payload = measurement.to_payload()
            encoded_bytes = json.dumps(payload).encode("utf-8")
            payload_sizes.append(len(encoded_bytes))

            start_time = perf_counter()
            result = client.send(payload)
            latency = (perf_counter() - start_time) * 1000.0

            latencies_ms.append(latency)
            if result.success and result.status_code == 202:
                delivery_successes += 1
            total_retries += (result.attempt_count - 1)

        # Basic assertions
        assert delivery_successes == 100
        assert total_retries == 0
        assert len(server.received_payloads) == 100
        assert server.attempts == 100

        payload_dist = _calculate_distribution(payload_sizes)
        latency_dist = _calculate_distribution(latencies_ms)

        report = {
            "task": "M1-16",
            "scenario": "healthy_baseline_100_sequential",
            "messages_generated": 100,
            "messages_delivered": delivery_successes,
            "delivery_success_rate_pct": (delivery_successes / 100.0) * 100.0,
            "total_retries": total_retries,
            "payload_bytes": payload_dist,
            "latency_ms": latency_dist,
        }
        assert report["messages_delivered"] == 100
        assert report["delivery_success_rate_pct"] == 100.0

        # Payload sizes: standard sensor payload is ~130-175 bytes depending on float precision
        assert 120 <= payload_dist["min"] <= 180
        assert 120 <= payload_dist["max"] <= 180

        # Verify sequential monotonic ordering in received payloads
        seqs = [int(p["sequence_number"]) for p in server.received_payloads]
        assert seqs == list(range(100))
    finally:
        server.shutdown()
        server.server_close()


def test_baseline_gateway_unavailable_bounded_retries() -> None:
    """Verify bounded retry count and non-crashing sequence progression when Gateway is down."""
    # Pick a port that is guaranteed not listening
    dummy_server = _BaselineServer(("127.0.0.1", 0))
    _, unused_port = dummy_server.server_address
    dummy_server.server_close()

    gateway_url = f"http://127.0.0.1:{unused_port}"

    sleeps: list[float] = []
    client = GatewayClient(
        gateway_url=gateway_url,
        request_timeout_seconds=0.5,
        max_retries=2,
        sleeper=sleeps.append,
    )

    sensor = Sensor(device_id="sensor-001")
    m1 = sensor.read()
    assert m1.sequence_number == 0

    result1 = client.send(m1.to_payload())
    assert not result1.success
    assert result1.status_code is None
    assert result1.error_category in {ErrorCategory.CONNECTION, ErrorCategory.TIMEOUT}
    assert result1.retryable is True
    assert result1.attempt_count == 3  # Initial attempt + 2 retries
    assert sleeps == [1, 2]  # Exponential backoff 2^0, 2^1

    # Verify sensor continues monotonic sequence generation despite network outage
    m2 = sensor.read()
    assert m2.sequence_number == 1
    result2 = client.send(m2.to_payload())
    assert not result2.success
    assert result2.attempt_count == 3


def test_baseline_gateway_http_503_controlled_failure() -> None:
    """Verify bounded retries when Gateway returns 503 Service Unavailable."""
    server, gateway_url, _ = _start_loopback_gateway()
    server.response_status = 503
    try:
        sleeps: list[float] = []
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=1.0,
            max_retries=2,
            sleeper=sleeps.append,
        )

        sensor = Sensor(device_id="sensor-001")
        m = sensor.read()

        result = client.send(m.to_payload())
        assert not result.success
        assert result.status_code == 503
        assert result.error_category == ErrorCategory.HTTP
        assert result.retryable is True
        assert result.attempt_count == 3
        assert server.attempts == 3
        assert sleeps == [1, 2]
    finally:
        server.shutdown()
        server.server_close()


def test_baseline_validation_failure_no_retries() -> None:
    """Verify validation failure (422) is not retried."""
    server, gateway_url, _ = _start_loopback_gateway()
    server.response_status = 422
    try:
        sleeps: list[float] = []
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=1.0,
            max_retries=2,
            sleeper=sleeps.append,
        )

        sensor = Sensor(device_id="sensor-001")
        m = sensor.read()

        result = client.send(m.to_payload())
        assert not result.success
        assert result.status_code == 422
        assert result.error_category == ErrorCategory.HTTP
        assert result.retryable is False
        assert result.attempt_count == 1
        assert server.attempts == 1
        assert len(sleeps) == 0
    finally:
        server.shutdown()
        server.server_close()


def test_baseline_device_controller_graceful_continuity_on_failure() -> None:
    """Verify DeviceController continues periodic execution through downstream failure."""
    server, gateway_url, _ = _start_loopback_gateway()
    server.response_status = 500  # Gateway failure
    try:
        config = Config(
            device_id="sensor-test",
            gateway_url=gateway_url,
            send_interval_seconds=0.01,
            request_timeout_seconds=0.5,
            max_retries=1,
            failure_mode=FailureMode.NONE,
            failure_rate=0.0,
            failure_seed=None,
            log_level="INFO",
        )
        stop_event = threading.Event()
        call_count = 0

        def sleeper_mock(_secs: float) -> None:
            nonlocal call_count
            call_count += 1
            if call_count >= 3:
                stop_event.set()

        controller = DeviceController(
            config=config,
            stop_event=stop_event,
            sleeper=sleeper_mock,
        )
        controller.run()

        # Controller completed 3 loop cycles despite all sends returning 500
        assert call_count >= 3
        assert server.attempts == 6  # 3 cycles * 2 attempts each (initial + 1 retry)
    finally:
        server.shutdown()
        server.server_close()
