"""M5-28 full baseline Legacy-to-Gateway-to-Cloud happy-path coverage."""

from __future__ import annotations

import json
import logging
import threading
import time
import urllib.request
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import Request

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import FailureMode as CloudFailureMode
from cloud_service.config import load_config as load_cloud_config
from cloud_service.failure import FailureInjector as CloudFailureInjector
from edge_gateway.app import create_app as create_gateway_app
from edge_gateway.config import load_config as load_gateway_config
from legacy_system.client import GatewayClient
from legacy_system.config import Config as LegacyConfig
from legacy_system.config import FailureMode as LegacyFailureMode
from legacy_system.device import DeviceController
from legacy_system.sensor import Measurement


FIXTURE = Path(__file__).parents[1] / "fixtures" / "valid_legacy_measurement.json"


@contextmanager
def serve(app, name: str):
    """Run one production ASGI application on an isolated local port."""
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


def query_single_measurement(cloud_url: str) -> dict[str, object]:
    with urllib.request.urlopen(f"{cloud_url}/api/v1/measurements", timeout=5) as response:
        assert response.status == 200
        payload = json.loads(response.read())
    assert isinstance(payload, dict)
    items = payload["items"]
    assert isinstance(items, list) and len(items) == 1
    row = items[0]
    assert isinstance(row, dict)
    return row


def test_baseline_measurement_flows_from_legacy_to_persisted_cloud_row(
    tmp_path: Path, caplog
) -> None:
    original = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(original, dict)
    measurement = Measurement(
        device_id=str(original["device_id"]),
        temperature_c=float(original["temperature_c"]),
        humidity_pct=float(original["humidity_pct"]),
        timestamp=datetime.fromisoformat(str(original["timestamp"])),
        sequence_number=int(original["sequence_number"]),
    )
    cloud = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{(tmp_path / 'measurements.db').as_posix()}",
                "SECURITY_MODE": "classical",
            }
        )
    )
    gateway_requests: list[tuple[str | None, bytes]] = []

    @cloud.middleware("http")
    async def observe_baseline_gateway_request(request: Request, call_next):
        if request.method == "POST" and request.url.path == "/api/v1/baseline/measurements":
            gateway_requests.append((request.headers.get("X-Request-ID"), await request.body()))
        return await call_next(request)

    with caplog.at_level(logging.INFO, logger="cloud_service"):
        with serve(cloud, "baseline-e2e-cloud") as cloud_url:
            gateway = create_gateway_app(
                load_gateway_config(
                    {
                        "GATEWAY_ID": "gateway-baseline-e2e",
                        "CLOUD_URL": cloud_url,
                        "SECURITY_MODE": "classical",
                        "CLOUD_TIMEOUT_SECONDS": "5",
                        "CLOUD_MAX_RETRIES": "0",
                    }
                )
            )
            with serve(gateway, "baseline-e2e-gateway") as gateway_url:
                result = GatewayClient(
                    gateway_url, request_timeout_seconds=5, max_retries=0
                ).send(measurement.to_payload())
                stored = query_single_measurement(cloud_url)

    assert result.success is True
    assert result.status_code == 202
    assert stored["device_id"] == original["device_id"]
    assert stored["temperature_c"] == original["temperature_c"]
    assert stored["humidity_pct"] == original["humidity_pct"]
    assert stored["sequence_number"] == original["sequence_number"]
    assert datetime.fromisoformat(str(stored["measured_at"])) == datetime.fromisoformat(
        str(original["timestamp"])
    )
    assert len(gateway_requests) == 1
    request_id, body = gateway_requests[0]
    assert isinstance(request_id, str) and request_id.startswith("req-")
    canonical = json.loads(body)
    assert canonical == {
        "device_id": original["device_id"],
        "temperature_c": original["temperature_c"],
        "humidity_pct": original["humidity_pct"],
        "measured_at": original["timestamp"],
        "sequence_number": original["sequence_number"],
        "received_at": canonical["received_at"],
        "gateway_id": "gateway-baseline-e2e",
    }
    assert "request_id" not in canonical
    gateway_received_at = datetime.fromisoformat(str(canonical["received_at"]))
    assert gateway_received_at.utcoffset() is not None
    assert datetime.fromisoformat(str(stored["gateway_received_at"])) == gateway_received_at
    cloud_received_at = datetime.fromisoformat(str(stored["cloud_received_at"]))
    assert cloud_received_at.utcoffset() is not None
    assert stored["gateway_id"] == "gateway-baseline-e2e"
    assert stored["record_id"]
    assert any(
        record.name == "cloud_service"
        and "event=measurement_stored " in record.getMessage()
        and f"request_id={request_id!r} " in record.getMessage()
        for record in caplog.records
    )


def test_legacy_controller_continues_after_bounded_cloud_delivery_failure(
    tmp_path: Path, caplog
) -> None:
    """M5-80: a downstream failure drops one measurement but cannot stall Legacy."""
    cloud = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{(tmp_path / 'continuity.db').as_posix()}",
                "SECURITY_MODE": "classical",
                "FAILURE_MODE": "storage_failure",
                "FAILURE_RATE": "1.0",
                "FAILURE_DELAY_SECONDS": "0",
            }
        )
    )
    generated_sequences: list[int] = []
    stop_event = threading.Event()
    sleeps = 0

    class TrackingSensor:
        def __init__(self) -> None:
            self._next_sequence = 0

        def read(self) -> Measurement:
            sequence_number = self._next_sequence
            self._next_sequence += 1
            generated_sequences.append(sequence_number)
            return Measurement(
                device_id="sensor-m5-80",
                temperature_c=22.5,
                humidity_pct=44.0,
                timestamp=datetime.fromisoformat("2026-09-21T12:00:00+00:00"),
                sequence_number=sequence_number,
            )

    with caplog.at_level(logging.INFO):
        with serve(cloud, "m5-80-cloud") as cloud_url:
            gateway = create_gateway_app(
                load_gateway_config(
                    {
                        "GATEWAY_ID": "gateway-m5-80",
                        "CLOUD_URL": cloud_url,
                        "SECURITY_MODE": "classical",
                        "CLOUD_TIMEOUT_SECONDS": "5",
                        "CLOUD_MAX_RETRIES": "0",
                    }
                )
            )
            with serve(gateway, "m5-80-gateway") as gateway_url:
                config = LegacyConfig(
                    device_id="sensor-m5-80",
                    gateway_url=gateway_url,
                    send_interval_seconds=0.01,
                    request_timeout_seconds=5,
                    max_retries=1,
                    failure_mode=LegacyFailureMode.NONE,
                    failure_rate=0.0,
                    failure_seed=None,
                    log_level="INFO",
                )

                def advance_after_delivery_attempt(_interval: float) -> None:
                    nonlocal sleeps
                    sleeps += 1
                    if sleeps == 1:
                        # The first valid sequence reached Cloud and failed storage.
                        # Its Legacy retry is bounded and then rejected as a duplicate
                        # because Gateway sequence state is intentionally not rolled back.
                        cloud.state.failure_injector = CloudFailureInjector(
                            CloudFailureMode.NONE, 0.0, None, 0
                        )
                    else:
                        stop_event.set()

                controller = DeviceController(
                    config,
                    sensor=TrackingSensor(),
                    client=GatewayClient(
                        gateway_url,
                        request_timeout_seconds=5,
                        max_retries=1,
                        sleeper=lambda _delay: None,
                    ),
                    sleeper=advance_after_delivery_attempt,
                    stop_event=stop_event,
                )
                controller.run()
                stored = query_single_measurement(cloud_url)

    assert generated_sequences == [0, 1]
    assert stored["device_id"] == "sensor-m5-80"
    assert stored["sequence_number"] == 1
    assert "event=gateway_retry component=legacy_system" in caplog.text
    assert "event=measurement_delivery_failed component=legacy_system device_id=sensor-m5-80 sequence_number=0" in caplog.text
    assert "event=measurement_delivered component=legacy_system device_id=sensor-m5-80 sequence_number=1" in caplog.text
