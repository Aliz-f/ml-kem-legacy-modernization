"""M5-35 full Legacy-to-ML-KEM-Cloud end-to-end coverage."""

from __future__ import annotations

import json
import threading
import time
import urllib.request
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import Request

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import FailureMode, load_config as load_cloud_config
from cloud_service.failure import FailureInjector
from edge_gateway.app import create_app as create_gateway_app
from edge_gateway.config import load_config as load_gateway_config
from legacy_system.client import GatewayClient
from legacy_system.sensor import Measurement


@contextmanager
def serve(app, name: str):
    """Run a production service on an isolated loopback port."""
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


def _query_one(cloud_url: str) -> dict[str, object]:
    with urllib.request.urlopen(f"{cloud_url}/api/v1/measurements", timeout=5) as response:
        assert response.status == 200
        payload = json.loads(response.read())
    assert isinstance(payload, dict)
    items = payload["items"]
    assert isinstance(items, list) and len(items) == 1
    row = items[0]
    assert isinstance(row, dict)
    return row


def test_legacy_client_reaches_one_persisted_row_through_mlkem_retry_path(tmp_path: Path) -> None:
    """One dropped Cloud response must resend the already-built envelope once."""
    measurement = Measurement(
        device_id="sensor-modernized-e2e",
        temperature_c=22.5,
        humidity_pct=44.0,
        timestamp=datetime.fromisoformat("2026-09-21T12:00:00Z"),
        sequence_number=1,
    )
    legacy_payload = measurement.to_payload()
    cloud = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{(tmp_path / 'modernized.db').as_posix()}",
                "SECURITY_MODE": "mlkem",
                "FAILURE_MODE": "drop_response",
                "FAILURE_RATE": "1.0",
            }
        )
    )
    secure_bodies: list[bytes] = []
    protocol_paths: list[str] = []

    @cloud.middleware("http")
    async def capture_and_clear_first_drop(request: Request, call_next):
        body = await request.body()
        response = await call_next(request)
        if request.url.path in {"/api/v1/crypto/public-key", "/api/v1/crypto/sessions"}:
            protocol_paths.append(request.url.path)
        if request.url.path == "/api/v1/secure/measurements":
            secure_bodies.append(body)
            if len(secure_bodies) == 1:
                cloud.state.failure_injector = FailureInjector(FailureMode.NONE, 0.0, None, 0)
        return response

    with serve(cloud, "m5-35-cloud") as cloud_url:
        gateway = create_gateway_app(
            load_gateway_config(
                {
                    "GATEWAY_ID": "gateway-modernized-e2e",
                    "CLOUD_URL": cloud_url,
                    "SECURITY_MODE": "mlkem",
                    "PQC_FAILURE_POLICY": "fail_closed",
                    "CLOUD_TIMEOUT_SECONDS": "5",
                    "CLOUD_MAX_RETRIES": "1",
                    "FAILURE_MODE": "none",
                }
            )
        )
        with serve(gateway, "m5-35-gateway") as gateway_url:
            result = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0).send(
                legacy_payload
            )
            stored = _query_one(cloud_url)

    assert result.success is True
    assert result.status_code == 202
    assert result.attempt_count == 1
    assert set(legacy_payload) == {
        "device_id", "temperature_c", "humidity_pct", "timestamp", "sequence_number"
    }
    assert protocol_paths == ["/api/v1/crypto/public-key", "/api/v1/crypto/sessions"]
    assert len(secure_bodies) == 2
    assert secure_bodies[0] == secure_bodies[1]
    envelope = json.loads(secure_bodies[0])
    assert set(envelope) == {
        "protocol_version", "gateway_id", "session_id", "request_id", "nonce", "ciphertext"
    }
    assert envelope["gateway_id"] == "gateway-modernized-e2e"
    assert "device_id" not in envelope and "message_counter" not in envelope

    assert stored["device_id"] == legacy_payload["device_id"]
    assert stored["temperature_c"] == legacy_payload["temperature_c"]
    assert stored["humidity_pct"] == legacy_payload["humidity_pct"]
    assert stored["sequence_number"] == legacy_payload["sequence_number"]
    assert stored["gateway_id"] == "gateway-modernized-e2e"
    assert datetime.fromisoformat(str(stored["measured_at"])) == datetime.fromisoformat(
        str(legacy_payload["timestamp"])
    )
    assert datetime.fromisoformat(str(stored["gateway_received_at"])).utcoffset() is not None
    assert datetime.fromisoformat(str(stored["cloud_received_at"])).utcoffset() is not None
    assert "request_id" not in stored
