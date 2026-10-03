"""M5-38: live Cloud and proactive Gateway session-expiry recovery."""

from __future__ import annotations

import json
import threading
import time
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

import uvicorn
from fastapi import Request

from cloud_service.app import create_app as cloud_app
from cloud_service.config import load_config as cloud_config
from edge_gateway.app import create_app as gateway_app
from edge_gateway.config import load_config as gateway_config
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.secure_transport import SecureTransport
from edge_gateway.crypto.session import SessionManager
from legacy_system.client import GatewayClient


@dataclass
class Clock:
    """A UTC clock deliberately advanced by this system test."""

    now: datetime

    def __call__(self) -> datetime:
        return self.now

    def advance(self, seconds: int) -> None:
        self.now += timedelta(seconds=seconds)


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


def _measurement(sequence: int) -> dict[str, object]:
    return {
        "device_id": "sensor-expiry",
        "temperature_c": 22.5,
        "humidity_pct": 44.0,
        "timestamp": "2026-09-21T12:00:00Z",
        "sequence_number": sequence,
    }


def test_session_expiry_recovers_once_and_local_expiry_rekeys_proactively(
    tmp_path: Path,
) -> None:
    initial = datetime(2026, 9, 21, 12, tzinfo=UTC)
    cloud_clock = Clock(initial)
    gateway_clock = Clock(initial)
    cloud = cloud_app(
        cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{tmp_path / 'expiry.db'}",
                "SECURITY_MODE": "mlkem",
                "FAILURE_MODE": "none",
            }
        )
    )
    protocol_requests: list[tuple[str, int, dict[str, object] | None]] = []

    @cloud.middleware("http")
    async def capture_protocol(request: Request, call_next):
        body = await request.body()
        response = await call_next(request)
        if request.url.path in {
            "/api/v1/crypto/public-key",
            "/api/v1/crypto/sessions",
            "/api/v1/secure/measurements",
        }:
            payload = json.loads(body) if body else None
            protocol_requests.append((request.url.path, response.status_code, payload))
        return response

    with serve(cloud, "m5-38-cloud") as cloud_url:
        # The live app owns its SessionManager; replace only its clock to keep
        # protocol-v1's fixed 300-second TTL while controlling elapsed time.
        assert cloud.state.sessions is not None
        cloud.state.sessions._clock = cloud_clock  # noqa: SLF001

        metrics = PqcMetrics()
        sessions = SessionManager(
            "gateway-expiry", cloud_url, 5, clock=gateway_clock, metrics=metrics
        )
        transport = SecureTransport(
            sessions,
            cloud_url=cloud_url,
            timeout_seconds=5,
            max_retries=0,
            metrics=metrics,
        )
        gateway = gateway_app(
            gateway_config(
                {
                    "GATEWAY_ID": "gateway-expiry",
                    "CLOUD_URL": cloud_url,
                    "SECURITY_MODE": "mlkem",
                    "CLOUD_MAX_RETRIES": "0",
                    "FAILURE_MODE": "none",
                }
            ),
            pqc_metrics=metrics,
            secure_transport=transport,
        )
        with serve(gateway, "m5-38-gateway") as gateway_url:
            client = GatewayClient(
                gateway_url, request_timeout_seconds=5, max_retries=0
            )
            assert client.send(_measurement(1)).success

            # Only Cloud time advances: Gateway sends session A, Cloud returns
            # the frozen 409 SESSION_EXPIRED, and recovery creates session B.
            cloud_clock.advance(301)
            assert client.send(_measurement(2)).success

            # Advance both clocks so the Gateway observes B expired before it
            # sends. It establishes C directly; no second 409 recovery occurs.
            cloud_clock.advance(301)
            gateway_clock.advance(602)
            assert client.send(_measurement(3)).success
            with urllib.request.urlopen(
                f"{gateway_url}/metrics", timeout=5
            ) as response:
                gateway_metrics = response.read().decode()

    secure = [
        (status, payload)
        for path, status, payload in protocol_requests
        if path == "/api/v1/secure/measurements"
    ]
    assert [status for status, _ in secure] == [202, 409, 202, 202]
    assert secure[1][1] is not None and secure[2][1] is not None
    assert secure[1][1]["request_id"] == secure[2][1]["request_id"]
    assert secure[1][1]["session_id"] != secure[2][1]["session_id"]
    assert [path for path, _, _ in protocol_requests] == [
        "/api/v1/crypto/public-key",
        "/api/v1/crypto/sessions",
        "/api/v1/secure/measurements",
        "/api/v1/secure/measurements",
        "/api/v1/crypto/public-key",
        "/api/v1/crypto/sessions",
        "/api/v1/secure/measurements",
        "/api/v1/crypto/public-key",
        "/api/v1/crypto/sessions",
        "/api/v1/secure/measurements",
    ]
    assert (
        _metric(gateway_metrics, 'gateway_mlkem_handshakes_total{result="success"}')
        == 3
    )
    assert (
        _metric(
            gateway_metrics, 'gateway_session_reestablishments_total{result="success"}'
        )
        == 1
    )
    assert (
        _metric(
            gateway_metrics, 'gateway_session_reestablishments_total{result="failure"}'
        )
        == 0
    )
