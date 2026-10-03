"""M5-36 successful Legacy compatibility in classical and ML-KEM modes."""

from __future__ import annotations

import json
import threading
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path

import uvicorn

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import load_config as load_cloud_config
from edge_gateway.app import create_app as create_gateway_app
from edge_gateway.config import load_config as load_gateway_config
from legacy_system.client import GatewayClient


@contextmanager
def serve(app, name: str):
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


def _deliver(tmp_path: Path, mode: str, payload: dict[str, object]) -> dict[str, object]:
    cloud = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{(tmp_path / f'{mode}.db').as_posix()}",
                "SECURITY_MODE": mode,
                "FAILURE_MODE": "none",
            }
        )
    )
    with serve(cloud, f"m5-36-{mode}-cloud") as cloud_url:
        gateway = create_gateway_app(
            load_gateway_config(
                {
                    "GATEWAY_ID": "gateway-compatibility",
                    "CLOUD_URL": cloud_url,
                    "SECURITY_MODE": mode,
                    "CLOUD_TIMEOUT_SECONDS": "5",
                    "CLOUD_MAX_RETRIES": "0",
                    "FAILURE_MODE": "none",
                }
            )
        )
        with serve(gateway, f"m5-36-{mode}-gateway") as gateway_url:
            result = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0).send(payload)
            with urllib.request.urlopen(f"{cloud_url}/api/v1/measurements", timeout=5) as response:
                rows = json.loads(response.read())["items"]
    assert result.success and result.status_code == 202 and result.attempt_count == 1
    assert isinstance(rows, list) and len(rows) == 1 and isinstance(rows[0], dict)
    return rows[0]


def test_same_legacy_client_payload_succeeds_in_both_security_modes(tmp_path: Path) -> None:
    payload = {
        "device_id": "sensor-compatibility",
        "temperature_c": 22.5,
        "humidity_pct": 44.0,
        "timestamp": "2026-09-21T12:00:00Z",
        "sequence_number": 1,
    }
    classical = _deliver(tmp_path, "classical", payload)
    mlkem = _deliver(tmp_path, "mlkem", payload)

    for row in (classical, mlkem):
        assert row["device_id"] == payload["device_id"]
        assert row["temperature_c"] == payload["temperature_c"]
        assert row["humidity_pct"] == payload["humidity_pct"]
        assert row["sequence_number"] == payload["sequence_number"]
        assert row["gateway_id"] == "gateway-compatibility"
    assert set(payload) == {"device_id", "temperature_c", "humidity_pct", "timestamp", "sequence_number"}
