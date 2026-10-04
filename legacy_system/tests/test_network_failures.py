"""M1-18 network-failure and transient failure verification test suite.

Proves that the Legacy Device HTTP client cleanly distinguishes permanent data
failures (400/409/422, non-retryable) from transient network/server failures
(connection refused, timeout, 500, 502, 503, 504, retryable with exponential backoff).
"""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import threading
import time
from typing import Any

import pytest

from legacy_system.client import ErrorCategory, GatewayClient
from legacy_system.config import Config, FailureMode
from legacy_system.device import DeviceController
from legacy_system.sensor import Sensor


class _ScriptedNetworkHandler(BaseHTTPRequestHandler):
    """Loopback HTTP handler scripted with a sequence of status codes or delays."""

    server: _ScriptedNetworkServer

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/v1/measurements":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(content_length)
        with self.server.lock:
            self.server.attempts += 1

        # Check if delay is configured
        if self.server.delay_seconds > 0:
            time.sleep(self.server.delay_seconds)

        # Retrieve next status code from script
        with self.server.lock:
            if self.server.script:
                status = self.server.script.pop(0)
            else:
                status = self.server.default_status

        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if status == 202:
                self.wfile.write(b'{"status": "accepted"}')
            else:
                self.wfile.write(json.dumps({"detail": f"Status {status}"}).encode("utf-8"))
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        pass


class _ScriptedNetworkServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int]) -> None:
        super().__init__(server_address, _ScriptedNetworkHandler)
        self.daemon_threads = True
        self.lock = threading.Lock()
        self.attempts: int = 0
        self.delay_seconds: float = 0.0
        self.script: list[int] = []
        self.default_status: int = 202


def _start_scripted_server() -> tuple[_ScriptedNetworkServer, str, threading.Thread]:
    server = _ScriptedNetworkServer(("127.0.0.1", 0))
    host, port = server.server_address
    url = f"http://{host}:{port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, url, thread


def _sample_payload(seq: int = 0) -> dict[str, object]:
    return {
        "device_id": "sensor-001",
        "temperature_c": 21.5,
        "humidity_pct": 50.0,
        "timestamp": "2026-10-04T12:00:00Z",
        "sequence_number": seq,
    }


def test_gateway_stopped_or_connection_refused() -> None:
    """Verify stopped Gateway / connection refused triggers bounded retries with backoff."""
    # Create and immediately close server to get an unused, closed port
    server = _ScriptedNetworkServer(("127.0.0.1", 0))
    _, port = server.server_address
    server.server_close()

    sleeps: list[float] = []
    client = GatewayClient(
        gateway_url=f"http://127.0.0.1:{port}",
        request_timeout_seconds=0.5,
        max_retries=2,
        sleeper=sleeps.append,
    )

    result = client.send(_sample_payload())

    assert result.success is False
    assert result.status_code is None
    assert result.error_category in {ErrorCategory.CONNECTION, ErrorCategory.TIMEOUT}
    assert result.retryable is True
    assert result.attempt_count == 3  # 1 initial + 2 retries
    assert sleeps == [1, 2]  # 2^0, 2^1


def test_gateway_slow_request_timeout() -> None:
    """Verify slow Gateway responses exceeding timeout trigger retryable TIMEOUT results."""
    server, gateway_url, _ = _start_scripted_server()
    server.delay_seconds = 0.3  # Longer than client timeout (0.1s)
    try:
        sleeps: list[float] = []
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=0.1,
            max_retries=2,
            sleeper=sleeps.append,
        )

        result = client.send(_sample_payload())

        assert result.success is False
        assert result.status_code is None
        assert result.error_category == ErrorCategory.TIMEOUT
        assert result.retryable is True
        assert result.attempt_count == 3
        assert server.attempts == 3
        assert sleeps == [1, 2]
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize("status_code", [500, 502, 503, 504])
def test_gateway_server_errors_trigger_bounded_retries(status_code: int) -> None:
    """Verify 5xx server errors (500, 502, 503, 504) are retryable and exhaust retries."""
    server, gateway_url, _ = _start_scripted_server()
    server.default_status = status_code
    try:
        sleeps: list[float] = []
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=1.0,
            max_retries=2,
            sleeper=sleeps.append,
        )

        result = client.send(_sample_payload())

        assert result.success is False
        assert result.status_code == status_code
        assert result.error_category == ErrorCategory.HTTP
        assert result.retryable is True
        assert result.attempt_count == 3
        assert server.attempts == 3
        assert sleeps == [1, 2]
    finally:
        server.shutdown()
        server.server_close()


def test_transient_failure_eventual_recovery_succeeds() -> None:
    """Verify transient 503 errors that recover on retry return success and log delivery."""
    server, gateway_url, _ = _start_scripted_server()
    # First 2 attempts return 503; 3rd attempt succeeds with 202
    server.script = [503, 503, 202]
    try:
        sleeps: list[float] = []
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=1.0,
            max_retries=2,
            sleeper=sleeps.append,
        )

        result = client.send(_sample_payload())

        assert result.success is True
        assert result.status_code == 202
        assert result.attempt_count == 3
        assert result.retryable is False
        assert server.attempts == 3
        assert sleeps == [1, 2]
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize(
    ("status_code", "is_retryable", "expected_attempts"),
    [
        # Permanent data failures -> 0 retries
        (400, False, 1),
        (409, False, 1),
        (422, False, 1),
        # Transient server failures -> 2 retries (3 attempts total)
        (500, True, 3),
        (502, True, 3),
        (503, True, 3),
        (504, True, 3),
    ],
)
def test_data_vs_transient_failure_classification_matrix(
    status_code: int, is_retryable: bool, expected_attempts: int
) -> None:
    """Verify the clean separation between non-retryable 4xx and retryable 5xx responses."""
    server, gateway_url, _ = _start_scripted_server()
    server.default_status = status_code
    try:
        sleeps: list[float] = []
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=1.0,
            max_retries=2,
            sleeper=sleeps.append,
        )

        result = client.send(_sample_payload())

        assert result.retryable is is_retryable
        assert result.status_code == status_code
        assert result.attempt_count == expected_attempts
        assert server.attempts == expected_attempts
        assert len(sleeps) == (expected_attempts - 1)
    finally:
        server.shutdown()
        server.server_close()


def test_device_controller_discards_failed_measurement_and_advances_sequence(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Verify DeviceController discards failed measurements and monotonically advances sequence."""
    server, gateway_url, _ = _start_scripted_server()
    server.default_status = 503  # Gateway permanently failing
    try:
        config = Config(
            device_id="sensor-transient-test",
            gateway_url=gateway_url,
            send_interval_seconds=0.01,
            request_timeout_seconds=0.5,
            max_retries=1,  # 1 retry per measurement
            failure_mode=FailureMode.NONE,
            failure_rate=0.0,
            failure_seed=None,
            log_level="INFO",
        )
        sensor = Sensor(device_id="sensor-transient-test")
        stop_event = threading.Event()
        cycles = 0

        def sleeper_mock(_secs: float) -> None:
            nonlocal cycles
            cycles += 1
            if cycles >= 3:
                stop_event.set()

        controller = DeviceController(
            config=config,
            sensor=sensor,
            stop_event=stop_event,
            sleeper=sleeper_mock,
        )

        with caplog.at_level(logging.WARNING):
            controller.run()

        # Controller completed 3 cycles
        assert cycles >= 3
        # In each cycle: 1 initial attempt + 1 retry = 2 attempts * 3 cycles = 6 server attempts
        assert server.attempts == 6

        # Check that sequential logs reflect sequence advancement (seq 0, 1, 2) despite failures
        assert "sequence_number=0" in caplog.text
        assert "sequence_number=1" in caplog.text
        assert "sequence_number=2" in caplog.text
        assert "event=measurement_delivery_failed" in caplog.text

        # Next sensor read continues sequence monotonically (seq 3)
        m_next = sensor.read()
        assert m_next.sequence_number == 3
    finally:
        server.shutdown()
        server.server_close()
