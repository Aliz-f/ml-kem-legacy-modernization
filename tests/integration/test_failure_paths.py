"""M5-40 live Legacy fault scenarios against the production Gateway boundary."""

from __future__ import annotations

import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass, field
from types import SimpleNamespace

import pytest
import uvicorn

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from legacy_system.client import GatewayClient
from legacy_system.config import FailureMode
from legacy_system.failure import FailureInjector


@dataclass
class AcceptedCloud:
    """Boundary-only accepted Cloud transport for Legacy-to-Gateway tests."""

    calls: list[dict[str, object]] = field(default_factory=list)

    async def send(self, **fields: object) -> object:
        self.calls.append(fields)
        return SimpleNamespace(status="accepted", record_id="rec-m5-40")


@contextmanager
def _gateway():
    transport = AcceptedCloud()
    app = create_app(
        load_config({"SECURITY_MODE": "classical", "GATEWAY_ID": "gateway-m5-40"}),
        baseline_transport=transport,
    )
    server = uvicorn.Server(
        uvicorn.Config(
            app, host="127.0.0.1", port=0, log_level="warning", access_log=False
        )
    )
    thread = threading.Thread(target=server.run, name="m5-40-gateway", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            raise RuntimeError("Gateway did not start")
        time.sleep(0.02)
    try:
        socket = server.servers[0].sockets[0]
        yield f"http://127.0.0.1:{socket.getsockname()[1]}", transport
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def _payload(sequence: int) -> dict[str, object]:
    return {
        "device_id": "sensor-failure-paths",
        "temperature_c": 22.5,
        "humidity_pct": 44.0,
        "timestamp": "2026-09-21T12:00:00Z",
        "sequence_number": sequence,
    }


@pytest.mark.parametrize(
    "mode",
    (
        FailureMode.INVALID_TEMPERATURE,
        FailureMode.INVALID_HUMIDITY,
        FailureMode.INVALID_TIMESTAMP,
        FailureMode.MISSING_FIELD,
    ),
)
def test_legacy_injected_parsed_faults_are_422_without_retry_or_cloud_delivery(
    mode: FailureMode,
) -> None:
    outgoing = FailureInjector(mode, 1.0, failure_seed=1).apply(_payload(1))
    with _gateway() as (url, cloud):
        result = GatewayClient(url, request_timeout_seconds=5, max_retries=2).send(
            outgoing
        )

    assert (result.status_code, result.attempt_count, result.retryable) == (
        422,
        1,
        False,
    )
    assert cloud.calls == []


@pytest.mark.parametrize(
    "mode",
    (FailureMode.DUPLICATE_SEQUENCE, FailureMode.OUT_OF_ORDER_SEQUENCE),
)
def test_legacy_injected_sequence_faults_are_409_without_retry(
    mode: FailureMode,
) -> None:
    injector = FailureInjector(mode, 1.0, failure_seed=1)
    # Feed the injector's private history just as the DeviceController does,
    # while the Gateway receives a monotonic starting sequence.
    injector.apply(_payload(1))
    injector.apply(_payload(2))
    outgoing = injector.apply(_payload(3))
    with _gateway() as (url, cloud):
        client = GatewayClient(url, request_timeout_seconds=5, max_retries=2)
        assert client.send(_payload(1)).success
        assert client.send(_payload(2)).success
        result = client.send(outgoing)

    assert (result.status_code, result.attempt_count, result.retryable) == (
        409,
        1,
        False,
    )
    assert len(cloud.calls) == 2


def test_malformed_legacy_wire_body_is_400_without_cloud_delivery() -> None:
    with _gateway() as (url, cloud):
        request = urllib.request.Request(
            f"{url}/api/v1/measurements",
            data=b'{"device_id":',
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request, timeout=5)

    assert caught.value.code == 400
    assert cloud.calls == []
