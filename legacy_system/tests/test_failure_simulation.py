"""M1-17 failure simulation validation test suite.

Demonstrates that every failure mode in the Legacy Device failure injector matrix
has the expected wire shape and retry behavior against a strict loopback
contract receiver:
- Normal (none) -> synthetic 202 acknowledgement
- Syntax error -> 400 Bad Request (0 retries)
- Domain / schema errors -> 422 Unprocessable Entity (0 retries)
- Sequence collisions / reversals -> 409 Conflict (0 retries)
- Zero retries triggered for all 4xx rejection codes
"""

from __future__ import annotations

from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import math
import threading
from typing import Any
import urllib.request

import pytest

from legacy_system.client import ErrorCategory, GatewayClient
from legacy_system.config import Config, FailureMode
from legacy_system.device import DeviceController
from legacy_system.failure import FailureInjector
from legacy_system.sensor import Sensor


class _LegacyContractReceiver(BaseHTTPRequestHandler):
    """Loopback receiver enforcing the frozen Legacy request contract.

    This test double exercises the Legacy client's wire and retry behavior only.
    Its synthetic 202 acknowledgement is not evidence of Gateway-to-Cloud
    forwarding or Cloud persistence; those behaviors belong to integration tests.
    """

    server: _LegacyContractServer

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/v1/measurements":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        self.server.total_attempts += 1

        # 1. Syntax check -> 400 Bad Request
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except Exception:
            self.server.rejections_400 += 1
            self._respond(400, {"detail": "Malformed JSON syntax"})
            return

        # 2. Schema check -> 422 Unprocessable Entity
        required_fields = {
            "device_id",
            "temperature_c",
            "humidity_pct",
            "timestamp",
            "sequence_number",
        }
        if not isinstance(payload, dict) or set(payload) != required_fields:
            self.server.rejections_422 += 1
            self._respond(422, {"detail": "Legacy request schema mismatch"})
            return

        # 3. Domain value validation -> 422 Unprocessable Entity
        try:
            device_id = payload["device_id"]
            if not isinstance(device_id, str) or not device_id.strip():
                raise ValueError("Empty device_id")
            temp = payload["temperature_c"]
            if (
                isinstance(temp, bool)
                or not isinstance(temp, (int, float))
                or not math.isfinite(temp)
                or not (-40.0 <= temp <= 85.0)
            ):
                raise ValueError("Temperature out of range")
            humidity = payload["humidity_pct"]
            if (
                isinstance(humidity, bool)
                or not isinstance(humidity, (int, float))
                or not math.isfinite(humidity)
                or not (0.0 <= humidity <= 100.0)
            ):
                raise ValueError("Humidity out of range")
            timestamp = payload["timestamp"]
            if not isinstance(timestamp, str):
                raise ValueError("Timestamp must be a string")
            parsed_timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if parsed_timestamp.utcoffset() != timedelta(0):
                raise ValueError("Timestamp must be UTC")
            seq = payload["sequence_number"]
            if (
                isinstance(seq, bool)
                or not isinstance(seq, int)
                or not 0 <= seq <= 9223372036854775807
            ):
                raise ValueError("Invalid sequence number")
        except Exception as exc:
            self.server.rejections_422 += 1
            self._respond(422, {"detail": f"Domain validation error: {exc}"})
            return

        # 4. Sequence state tracking -> 409 Conflict
        last_seq = self.server.last_sequences.get(device_id)
        if last_seq is not None:
            if seq == last_seq:
                self.server.rejections_409 += 1
                self._respond(409, {"detail": f"Duplicate sequence number: {seq}"})
                return
            if seq < last_seq:
                self.server.rejections_409 += 1
                self._respond(
                    409, {"detail": f"Out of order sequence number: {seq} < {last_seq}"}
                )
                return

        self.server.last_sequences[device_id] = seq
        self.server.accepted_payloads.append(payload)
        self._respond(202, {"status": "loopback_acknowledged"})

    def _respond(self, status: int, data: dict[str, Any]) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        pass


class _LegacyContractServer(HTTPServer):
    def __init__(self, server_address: tuple[str, int]) -> None:
        super().__init__(server_address, _LegacyContractReceiver)
        self.total_attempts: int = 0
        self.rejections_400: int = 0
        self.rejections_422: int = 0
        self.rejections_409: int = 0
        self.accepted_payloads: list[dict[str, Any]] = []
        self.last_sequences: dict[str, int] = {}


def _start_contract_receiver() -> tuple[_LegacyContractServer, str, threading.Thread]:
    server = _LegacyContractServer(("127.0.0.1", 0))
    host, port = server.server_address
    url = f"http://{host}:{port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, url, thread


@pytest.mark.parametrize(
    ("mode", "expected_status"),
    [
        (FailureMode.NONE, 202),
        (FailureMode.INVALID_TEMPERATURE, 422),
        (FailureMode.INVALID_HUMIDITY, 422),
        (FailureMode.MISSING_FIELD, 422),
        (FailureMode.INVALID_TIMESTAMP, 422),
    ],
)
def test_data_failure_modes_rejected_or_accepted_without_retry(
    mode: FailureMode, expected_status: int
) -> None:
    """Verify each data failure mode produces the expected status and no retries."""
    server, gateway_url, _ = _start_contract_receiver()
    try:
        sleeps: list[float] = []
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=2.0,
            max_retries=2,
            sleeper=sleeps.append,
        )
        injector = FailureInjector(mode=mode, failure_rate=1.0, failure_seed=42)
        sensor = Sensor(device_id="sensor-001")

        measurement = sensor.read()
        payload = measurement.to_payload()
        outgoing = injector.apply(payload)

        result = client.send(outgoing)

        assert result.status_code == expected_status
        assert result.attempt_count == 1  # No retries on 202 or 422
        assert result.retryable is False
        assert len(sleeps) == 0
        assert server.total_attempts == 1

        if expected_status == 202:
            assert result.success is True
            assert len(server.accepted_payloads) == 1
        else:
            assert result.success is False
            assert result.error_category == ErrorCategory.HTTP
            assert server.rejections_422 == 1
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("device_id", 1),
        ("temperature_c", "21.5"),
        ("humidity_pct", True),
        ("timestamp", "2026-10-04T12:00:00"),
        ("timestamp", "2026-10-04T12:00:00+03:00"),
        ("sequence_number", 1.0),
        ("sequence_number", 9223372036854775808),
    ],
)
def test_contract_receiver_rejects_wrong_types_and_domains_without_retry(
    field: str, value: object
) -> None:
    """Lock the loopback receiver to the frozen Legacy schema and domain rules."""
    server, gateway_url, _ = _start_contract_receiver()
    try:
        client = GatewayClient(gateway_url, request_timeout_seconds=2.0, max_retries=2)
        payload = Sensor(device_id="sensor-001").read().to_payload()
        payload[field] = value

        result = client.send(payload)

        assert result.status_code == 422
        assert result.attempt_count == 1
        assert result.retryable is False
    finally:
        server.shutdown()
        server.server_close()


def test_contract_receiver_rejects_extra_fields_without_retry() -> None:
    """The Legacy request schema has exactly five fields; extras are a 422."""
    server, gateway_url, _ = _start_contract_receiver()
    try:
        client = GatewayClient(gateway_url, request_timeout_seconds=2.0, max_retries=2)
        payload = Sensor(device_id="sensor-001").read().to_payload()
        payload["unexpected"] = "field"

        result = client.send(payload)

        assert result.status_code == 422
        assert result.attempt_count == 1
        assert result.retryable is False
    finally:
        server.shutdown()
        server.server_close()


def test_sequence_failure_modes_trigger_409_without_retry() -> None:
    """Verify duplicate and out-of-order sequence faults trigger 409 with zero retries."""
    server, gateway_url, _ = _start_contract_receiver()
    try:
        sleeps: list[float] = []
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=2.0,
            max_retries=2,
            sleeper=sleeps.append,
        )

        # Baseline: send two valid measurements (seq 0 and seq 1)
        sensor = Sensor(device_id="sensor-001")
        m0 = sensor.read()
        m1 = sensor.read()
        assert client.send(m0.to_payload()).status_code == 202
        assert client.send(m1.to_payload()).status_code == 202
        assert server.total_attempts == 2

        # 1. Duplicate sequence mode
        injector_dup = FailureInjector(
            mode=FailureMode.DUPLICATE_SEQUENCE,
            failure_rate=1.0,
            failure_seed=1,
        )
        # Populate injector state with previous payloads
        injector_dup.apply(m0.to_payload())
        outgoing_dup = injector_dup.apply(m1.to_payload())

        result_dup = client.send(outgoing_dup)
        assert result_dup.status_code == 409
        assert result_dup.attempt_count == 1
        assert result_dup.retryable is False
        assert len(sleeps) == 0

        # 2. Out-of-order sequence mode
        m2 = sensor.read()
        m3 = sensor.read()
        injector_ooo = FailureInjector(
            mode=FailureMode.OUT_OF_ORDER_SEQUENCE,
            failure_rate=1.0,
            failure_seed=1,
        )
        injector_ooo.apply(m0.to_payload())
        injector_ooo.apply(m1.to_payload())
        injector_ooo.apply(m2.to_payload())
        outgoing_ooo = injector_ooo.apply(m3.to_payload())

        result_ooo = client.send(outgoing_ooo)
        assert result_ooo.status_code == 409
        assert result_ooo.attempt_count == 1
        assert result_ooo.retryable is False
        assert len(sleeps) == 0
        assert server.rejections_409 == 2
    finally:
        server.shutdown()
        server.server_close()


def test_malformed_wire_body_is_400_without_retry() -> None:
    """Verify malformed JSON syntax is rejected with 400 Bad Request and not retried."""
    server, gateway_url, _ = _start_contract_receiver()
    try:
        # Directly post unparseable bytes to test the syntax boundary
        endpoint = f"{gateway_url}/api/v1/measurements"
        req = urllib.request.Request(
            endpoint,
            data=b'{"device_id": "sensor-001", "unclosed',
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(req, timeout=2.0)

        assert exc_info.value.code == 400
        assert server.total_attempts == 1
        assert server.rejections_400 == 1
    finally:
        server.shutdown()
        server.server_close()


def test_random_failure_mode_generates_mixed_controlled_outcomes() -> None:
    """Verify random mode injects mixed valid and faulty payloads deterministically."""
    server, gateway_url, _ = _start_contract_receiver()
    try:
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=2.0,
            max_retries=2,
        )
        # Rate 0.5 with fixed seed produces a mix of 202 and 4xx
        injector = FailureInjector(
            mode=FailureMode.RANDOM,
            failure_rate=0.5,
            failure_seed=12345,
        )
        sensor = Sensor(device_id="sensor-001")

        statuses: list[int] = []
        for _ in range(20):
            measurement = sensor.read()
            outgoing = injector.apply(measurement.to_payload())
            res = client.send(outgoing)
            assert res.attempt_count == 1  # No retries on any 202 or 4xx
            assert res.status_code in {202, 409, 422}
            assert res.status_code is not None
            statuses.append(res.status_code)

        # Must have both successful and failed outcomes
        assert 202 in statuses
        assert any(code in {409, 422} for code in statuses)
        assert server.total_attempts == 20
        # No 5xx or unhandled errors
        assert set(statuses).issubset({202, 409, 422})
    finally:
        server.shutdown()
        server.server_close()


def test_failure_rejections_logged_with_structured_attributes(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Verify structured log events for failure occurrences reflect error category and status."""
    server, gateway_url, _ = _start_contract_receiver()
    try:
        client = GatewayClient(
            gateway_url=gateway_url,
            request_timeout_seconds=2.0,
            max_retries=2,
        )
        injector = FailureInjector(
            mode=FailureMode.INVALID_TEMPERATURE,
            failure_rate=1.0,
            failure_seed=1,
        )
        sensor = Sensor(device_id="sensor-log-test")
        measurement = sensor.read()
        outgoing = injector.apply(measurement.to_payload())

        with caplog.at_level(logging.WARNING):
            result = client.send(outgoing)

        assert result.status_code == 422
        assert "event=gateway_request_failed" in caplog.text
        assert "status_code=422" in caplog.text
        assert "attempt=1" in caplog.text
        assert "error_category=http" in caplog.text
    finally:
        server.shutdown()
        server.server_close()


def test_device_controller_runs_through_fault_injections_without_crashing() -> None:
    """Verify DeviceController continues generating measurements when faults are injected."""
    server, gateway_url, _ = _start_contract_receiver()
    try:
        config = Config(
            device_id="sensor-fault-loop",
            gateway_url=gateway_url,
            send_interval_seconds=0.01,
            request_timeout_seconds=1.0,
            max_retries=2,
            failure_mode=FailureMode.INVALID_HUMIDITY,
            failure_rate=1.0,
            failure_seed=999,
            log_level="INFO",
        )
        stop_event = threading.Event()
        cycles = 0

        def sleeper_mock(_secs: float) -> None:
            nonlocal cycles
            cycles += 1
            if cycles >= 4:
                stop_event.set()

        controller = DeviceController(
            config=config,
            stop_event=stop_event,
            sleeper=sleeper_mock,
        )
        controller.run()

        # Controller completed 4 cycles without crashing, generating 4 invalid payloads
        assert cycles >= 4
        assert server.total_attempts == 4
        assert server.rejections_422 == 4
        assert len(server.accepted_payloads) == 0
    finally:
        server.shutdown()
        server.server_close()
