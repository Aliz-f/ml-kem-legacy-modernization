"""Real Legacy Device-to-Gateway HTTP boundary and integration scenario coverage."""

from __future__ import annotations

import json
import logging
import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
import uvicorn

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from legacy_system.client import GatewayClient
from legacy_system.config import Config, FailureMode
from legacy_system.device import DeviceController
from legacy_system.failure import FailureInjector
from legacy_system.sensor import Measurement, Sensor


PATH = "/api/v1/measurements"
FIXTURES = Path(__file__).parents[1] / "fixtures"


@dataclass
class AcceptedBaseline:
    """Boundary-only Cloud substitute; Cloud integration remains M5-27."""

    calls: list[dict[str, object]] = field(default_factory=list)

    async def send(self, **fields: object) -> object:
        self.calls.append(fields)
        return SimpleNamespace(status="accepted", record_id="rec-m5-26")


@dataclass
class FailingBaseline:
    """Boundary-only Cloud substitute that fails to test resilience and state."""

    async def send(self, **fields: object) -> object:
        raise ConnectionError("downstream Cloud connection refused")


@contextmanager
def live_gateway(transport: object | None = None):
    """Serve the production Gateway app on loopback with an accepted baseline stub."""
    if transport is None:
        transport = AcceptedBaseline()
    app = create_app(
        load_config({
            "SECURITY_MODE": "classical",
            "GATEWAY_ID": "gateway-m5-26",
            "LOG_LEVEL": "INFO",
        }),
        baseline_transport=transport,
    )
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name="legacy-gateway-test", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            server.should_exit = True
            thread.join(timeout=5)
            raise RuntimeError("Gateway did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("Gateway has no listening socket")
    url = f"http://127.0.0.1:{sockets[0].getsockname()[1]}"
    try:
        yield url, transport
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def fixture_payload(name: str) -> dict[str, object]:
    payload = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def post_raw(gateway_url: str, body: bytes) -> tuple[int, dict[str, object]]:
    request = urllib.request.Request(
        gateway_url + PATH,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            status, raw = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, raw = error.code, error.read()
    parsed = json.loads(raw)
    assert isinstance(parsed, dict)
    return status, parsed


def test_legacy_serializer_and_client_reach_live_gateway() -> None:
    fixture = fixture_payload("valid_legacy_measurement.json")
    measurement = Measurement(
        device_id=str(fixture["device_id"]),
        temperature_c=float(fixture["temperature_c"]),
        humidity_pct=float(fixture["humidity_pct"]),
        timestamp=datetime.fromisoformat(str(fixture["timestamp"])),
        sequence_number=int(fixture["sequence_number"]),
    )

    with live_gateway() as (gateway_url, transport):
        result = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0).send(
            measurement.to_payload()
        )

    assert result.success is True
    assert result.status_code == 202
    assert result.attempt_count == 1
    assert len(transport.calls) == 1
    assert transport.calls[0]["device_id"] == fixture["device_id"]
    assert transport.calls[0]["sequence_number"] == fixture["sequence_number"]


@pytest.mark.parametrize(
    ("payload", "expected_code"),
    [
        ({"temperature_c": 85.1}, "INVALID_MEASUREMENT"),
        (fixture_payload("invalid_humidity_measurement.json"), "INVALID_MEASUREMENT"),
        ({"timestamp": None}, "INVALID_MEASUREMENT"),
        ({"humidity_pct": "44.0"}, "INVALID_MEASUREMENT"),
        ({"timestamp": "not-a-timestamp"}, "INVALID_MEASUREMENT"),
    ],
    ids=("invalid-temperature", "invalid-humidity", "missing-field", "wrong-type", "invalid-timestamp"),
)
def test_parsed_invalid_legacy_payload_is_rejected_without_delivery(
    payload: dict[str, object], expected_code: str
) -> None:
    body = fixture_payload("valid_legacy_measurement.json") | payload
    with live_gateway() as (gateway_url, transport):
        status, response = post_raw(gateway_url, json.dumps(body).encode("utf-8"))

    assert (status, response) == (
        422,
        {"error": {"code": expected_code, "message": "measurement validation failed"}},
    )
    assert transport.calls == []


@pytest.mark.parametrize(
    "fixture_name",
    [
        "invalid_temperature_measurement.json",
        "invalid_humidity_measurement.json",
        "invalid_timestamp_measurement.json",
        "missing_field_measurement.json",
    ],
    ids=("invalid-temperature", "invalid-humidity", "invalid-timestamp", "missing-field"),
)
def test_all_invalid_integration_fixtures_are_rejected_without_delivery(fixture_name: str) -> None:
    body = fixture_payload(fixture_name)
    with live_gateway() as (gateway_url, transport):
        status, response = post_raw(gateway_url, json.dumps(body).encode("utf-8"))

    assert (status, response) == (
        422,
        {"error": {"code": "INVALID_MEASUREMENT", "message": "measurement validation failed"}},
    )
    assert transport.calls == []


def test_malformed_legacy_json_is_rejected_without_delivery() -> None:
    with live_gateway() as (gateway_url, transport):
        status, response = post_raw(gateway_url, b'{"device_id":')

    assert (status, response) == (
        400,
        {"error": {"code": "INVALID_JSON", "message": "request body must be valid JSON"}},
    )
    assert transport.calls == []


def test_duplicate_and_out_of_order_sequences_are_rejected_without_delivery() -> None:
    payload = fixture_payload("valid_legacy_measurement.json")
    with live_gateway() as (gateway_url, transport):
        first_status, _ = post_raw(gateway_url, json.dumps(payload).encode("utf-8"))
        duplicate_status, duplicate = post_raw(gateway_url, json.dumps(payload).encode("utf-8"))
        older_status, older = post_raw(
            gateway_url,
            json.dumps(payload | {"sequence_number": 0}).encode("utf-8"),
        )

    assert first_status == 202
    assert (duplicate_status, duplicate["error"]["code"]) == (409, "DUPLICATE_SEQUENCE")
    assert (older_status, older["error"]["code"]) == (409, "OUT_OF_ORDER_SEQUENCE")
    assert len(transport.calls) == 1


@pytest.mark.parametrize(
    "mode",
    [
        FailureMode.INVALID_HUMIDITY,
        FailureMode.INVALID_TEMPERATURE,
        FailureMode.MISSING_FIELD,
        FailureMode.INVALID_TIMESTAMP,
    ],
    ids=(
        "invalid-humidity",
        "invalid-temperature",
        "missing-field",
        "invalid-timestamp",
    ),
)
def test_injected_payload_faults_are_rejected_without_retry_or_cloud_delivery(
    mode: FailureMode,
) -> None:
    """Injected payload faults return 422, do not retry, and are not delivered to Cloud."""
    base = fixture_payload("valid_legacy_measurement.json")
    outgoing = FailureInjector(mode, failure_rate=1.0, failure_seed=42).apply(base)
    with live_gateway() as (gateway_url, transport):
        result = GatewayClient(
            gateway_url, request_timeout_seconds=5, max_retries=2
        ).send(outgoing)

    assert result.status_code == 422
    assert result.success is False
    assert result.attempt_count == 1
    assert result.retryable is False
    assert transport.calls == []


def test_injected_duplicate_sequence_is_rejected_without_retry() -> None:
    """Injected duplicate sequence is rejected as 409 without retry."""
    base = fixture_payload("valid_legacy_measurement.json")
    injector = FailureInjector(
        FailureMode.DUPLICATE_SEQUENCE, failure_rate=1.0, failure_seed=42
    )
    # Feed base payload sequence 1 to injector history
    injector.apply(base)
    # Next payload with sequence 2 is mutated to duplicate sequence 1
    second_payload = dict(base)
    second_payload["sequence_number"] = 2
    outgoing = injector.apply(second_payload)
    assert outgoing["sequence_number"] == 1

    with live_gateway() as (gateway_url, transport):
        client = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=2)
        first_result = client.send(base)
        assert first_result.success and first_result.status_code == 202

        second_result = client.send(outgoing)
        assert second_result.status_code == 409
        assert second_result.attempt_count == 1
        assert second_result.retryable is False
        assert len(transport.calls) == 1


def test_injected_out_of_order_sequence_is_rejected_without_retry() -> None:
    """Injected out-of-order sequence is rejected as 409 without retry."""
    injector = FailureInjector(
        FailureMode.OUT_OF_ORDER_SEQUENCE, failure_rate=1.0, failure_seed=42
    )
    p1 = fixture_payload("valid_legacy_measurement.json") | {"sequence_number": 1}
    p2 = fixture_payload("valid_legacy_measurement.json") | {"sequence_number": 2}
    p3 = fixture_payload("valid_legacy_measurement.json") | {"sequence_number": 3}
    injector.apply(p1)
    injector.apply(p2)
    outgoing = injector.apply(p3)
    assert outgoing["sequence_number"] in (1, 2) and outgoing["sequence_number"] < 3

    with live_gateway() as (gateway_url, transport):
        client = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=2)
        assert client.send(p1).success
        assert client.send(p2).success

        result = client.send(outgoing)
        assert result.status_code == 409
        assert result.attempt_count == 1
        assert result.retryable is False
        assert len(transport.calls) == 2


def test_sequence_gap_is_accepted_and_logged(caplog: pytest.LogCaptureFixture) -> None:
    """Sequence gap (e.g. 10, 11, 13) is accepted by Gateway and logged."""
    with live_gateway() as (gateway_url, transport):
        client = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0)

        m10 = Measurement("sensor-gap", 20.0, 50.0, datetime.now(timezone.utc), 10)
        res10 = client.send(m10.to_payload())
        assert res10.success and res10.status_code == 202

        m11 = Measurement("sensor-gap", 20.5, 51.0, datetime.now(timezone.utc), 11)
        res11 = client.send(m11.to_payload())
        assert res11.success and res11.status_code == 202

        with caplog.at_level(logging.INFO, logger="edge_gateway"):
            m13 = Measurement("sensor-gap", 21.0, 52.0, datetime.now(timezone.utc), 13)
            res13 = client.send(m13.to_payload())
            assert res13.success and res13.status_code == 202

        assert len(transport.calls) == 3
        assert transport.calls[2]["sequence_number"] == 13
        assert "event=sequence_gap_detected" in caplog.text
        assert "sequence_number=13" in caplog.text


def test_gateway_unavailable_triggers_bounded_retries_and_monotonic_progression(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Gateway outage triggers bounded retries, logs failure, and preserves monotonic progression without crashing."""
    config = Config(
        device_id="sensor-unavailable-test",
        gateway_url="http://127.0.0.1:9",
        send_interval_seconds=0.01,
        request_timeout_seconds=0.05,
        max_retries=1,
        failure_mode=FailureMode.NONE,
        failure_rate=0.0,
        failure_seed=None,
        log_level="INFO",
    )
    stop_event = threading.Event()
    generated_sequences: list[int] = []

    class TrackingSensor(Sensor):
        def read(self) -> Measurement:
            m = super().read()
            generated_sequences.append(m.sequence_number)
            return m

    sensor = TrackingSensor(config.device_id)

    iterations = 0

    def sleeper_stop_after_two(_interval: float) -> None:
        nonlocal iterations
        iterations += 1
        if iterations >= 2:
            stop_event.set()

    with caplog.at_level(logging.WARNING, logger="legacy_system.device"):
        controller = DeviceController(
            config,
            sensor=sensor,
            sleeper=sleeper_stop_after_two,
            stop_event=stop_event,
        )
        controller.run()

    assert generated_sequences == [0, 1]
    assert "event=measurement_delivery_failed" in caplog.text


def test_sequence_state_timing_awareness_no_rollback_on_downstream_failure() -> None:
    """Gateway commits sequence state upon valid ingestion; state does not roll back on Cloud failure."""
    failing_transport = FailingBaseline()
    with live_gateway(transport=failing_transport) as (gateway_url, _):
        client = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0)
        measurement = Measurement(
            device_id="sensor-timing-test",
            temperature_c=22.0,
            humidity_pct=45.0,
            timestamp=datetime.now(timezone.utc),
            sequence_number=1,
        )
        # First send: passes Gateway validation and commits sequence 1, but downstream Cloud delivery fails -> 503
        first_result = client.send(measurement.to_payload())
        assert first_result.status_code == 503
        assert first_result.success is False

        # Resend same sequence: Gateway rejects as 409 DUPLICATE_SEQUENCE because state was NOT rolled back
        second_result = client.send(measurement.to_payload())
        assert second_result.status_code == 409
        assert second_result.success is False

