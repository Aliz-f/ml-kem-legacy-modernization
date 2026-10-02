"""M5-26 real Legacy Device-to-Gateway HTTP boundary coverage."""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
import uvicorn

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from legacy_system.client import GatewayClient
from legacy_system.sensor import Measurement


PATH = "/api/v1/measurements"
FIXTURES = Path(__file__).parents[1] / "fixtures"


@dataclass
class AcceptedBaseline:
    """Boundary-only Cloud substitute; Cloud integration remains M5-27."""

    calls: list[dict[str, object]] = field(default_factory=list)

    async def send(self, **fields: object) -> object:
        self.calls.append(fields)
        return SimpleNamespace(status="accepted", record_id="rec-m5-26")


@contextmanager
def live_gateway():
    """Serve the production Gateway app on loopback with an accepted baseline stub."""
    transport = AcceptedBaseline()
    app = create_app(
        load_config({"SECURITY_MODE": "classical", "GATEWAY_ID": "gateway-m5-26"}),
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
