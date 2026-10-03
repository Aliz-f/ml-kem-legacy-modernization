"""M5-37: three live Legacy messages reuse one ML-KEM session."""

from __future__ import annotations
import threading
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path
import uvicorn
from fastapi import Request
from cloud_service.app import create_app as cloud_app
from cloud_service.config import load_config as cloud_config
from edge_gateway.app import create_app as gateway_app
from edge_gateway.config import load_config as gateway_config
from legacy_system.client import GatewayClient


@contextmanager
def serve(app, name: str):
    server = uvicorn.Server(
        uvicorn.Config(
            app, host="127.0.0.1", port=0, log_level="warning", access_log=False
        )
    )
    thread = threading.Thread(target=server.run, name=name, daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            raise RuntimeError(f"{name} did not start")
        time.sleep(0.02)
    try:
        yield f"http://127.0.0.1:{server.servers[0].sockets[0].getsockname()[1]}"
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def _metric(text: str, name: str) -> int:
    return int(
        next(line for line in text.splitlines() if line.startswith(name + " ")).rsplit(
            " ", 1
        )[1]
    )


def test_three_legacy_messages_use_one_handshake_and_three_secure_deliveries(
    tmp_path: Path,
) -> None:
    cloud = cloud_app(
        cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{tmp_path / 'reuse.db'}",
                "SECURITY_MODE": "mlkem",
                "FAILURE_MODE": "none",
            }
        )
    )
    paths = []

    @cloud.middleware("http")
    async def capture(request: Request, call_next):
        response = await call_next(request)
        if request.url.path in {
            "/api/v1/crypto/sessions",
            "/api/v1/secure/measurements",
        }:
            paths.append(request.url.path)
        return response

    with serve(cloud, "m5-37-cloud") as cloud_url:
        gateway = gateway_app(
            gateway_config(
                {
                    "GATEWAY_ID": "gateway-reuse",
                    "CLOUD_URL": cloud_url,
                    "SECURITY_MODE": "mlkem",
                    "CLOUD_MAX_RETRIES": "0",
                    "FAILURE_MODE": "none",
                }
            )
        )
        with serve(gateway, "m5-37-gateway") as gateway_url:
            client = GatewayClient(
                gateway_url, request_timeout_seconds=5, max_retries=0
            )
            for sequence in (1, 2, 3):
                assert client.send(
                    {
                        "device_id": "sensor-reuse",
                        "temperature_c": 22.5,
                        "humidity_pct": 44.0,
                        "timestamp": "2026-09-21T12:00:00Z",
                        "sequence_number": sequence,
                    }
                ).success
            with urllib.request.urlopen(
                f"{gateway_url}/metrics", timeout=5
            ) as response:
                metrics = response.read().decode()
    assert paths == ["/api/v1/crypto/sessions"] + ["/api/v1/secure/measurements"] * 3
    assert _metric(metrics, 'gateway_mlkem_handshakes_total{result="success"}') == 1
    assert (
        _metric(metrics, 'gateway_secure_message_duration_seconds_count{phase="first"}')
        == 1
    )
    assert (
        _metric(
            metrics, 'gateway_secure_message_duration_seconds_count{phase="steady"}'
        )
        == 2
    )
