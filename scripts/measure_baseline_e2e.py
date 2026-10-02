"""Measure the real classical Legacy -> Gateway -> Cloud path.

This deliberately small M5-31 harness is evidence gathering, not a benchmark
platform.  It starts disposable local services, sends sequential measurements
through the production Legacy client, and prints one JSON report.

Example: ``uv run python scripts/measure_baseline_e2e.py --samples 10``.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import UTC, datetime
from importlib.metadata import version
import json
import math
from pathlib import Path
import platform
import sqlite3
from statistics import median
from tempfile import TemporaryDirectory
from threading import Thread
from time import perf_counter, sleep
from typing import Iterator
from urllib.request import urlopen

import uvicorn
from fastapi import Request

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import load_config as load_cloud_config
from cloud_service.storage.repository import MeasurementRepository
from edge_gateway.app import create_app as create_gateway_app
from edge_gateway.config import load_config as load_gateway_config
from legacy_system.client import GatewayClient
from legacy_system.sensor import Measurement


class TimedRepository(MeasurementRepository):
    """Record the Cloud's actual SQLite save operation for this harness only."""

    def __init__(self, database: object) -> None:
        super().__init__(database)  # type: ignore[arg-type]
        self.storage_ms: list[float] = []

    def save_idempotent(self, measurement: object) -> object:
        started = perf_counter()
        try:
            return super().save_idempotent(measurement)  # type: ignore[arg-type]
        finally:
            self.storage_ms.append((perf_counter() - started) * 1000)


@contextmanager
def serve(app: object, name: str) -> Iterator[str]:
    """Run one ASGI application on a disposable loopback port."""
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = Thread(target=server.run, name=name, daemon=True)
    thread.start()
    deadline = perf_counter() + 10
    while not server.started:
        if not thread.is_alive() or perf_counter() > deadline:
            server.should_exit = True
            thread.join(timeout=5)
            raise RuntimeError(f"{name} did not start")
        sleep(0.02)
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


def distribution(samples: list[float] | list[int]) -> dict[str, float | int]:
    """Return a small, stable summary without introducing benchmark targets."""
    if not samples:
        raise ValueError("cannot summarize no samples")
    ordered = sorted(samples)
    return {
        "count": len(samples),
        "min": ordered[0],
        "median": median(ordered),
        "p95": ordered[math.ceil(len(ordered) * 0.95) - 1],
        "max": ordered[-1],
    }


def _persisted_rows(cloud_url: str) -> list[dict[str, object]]:
    with urlopen(f"{cloud_url}/api/v1/measurements?limit=100", timeout=5) as response:
        payload = json.loads(response.read())
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise RuntimeError("Cloud query response did not contain items")
    return payload["items"]


def run(samples: int = 10) -> dict[str, object]:
    """Execute sequential successful baseline messages and return their observations."""
    if type(samples) is not int or not 1 <= samples <= 100:
        raise ValueError("samples must be an integer from 1 to 100")

    gateway_request_ms: list[float] = []
    cloud_request_ms: list[float] = []
    canonical_payload_bytes: list[int] = []
    end_to_end_ms: list[float] = []
    cloud_requests = 0

    with TemporaryDirectory(prefix="baseline-e2e-") as directory:
        database_url = f"sqlite:///{(Path(directory) / 'measurements.db').as_posix()}"
        cloud = create_cloud_app(
            load_cloud_config(
                {
                    "DATABASE_URL": database_url,
                    "SECURITY_MODE": "classical",
                    "FAILURE_MODE": "none",
                }
            )
        )

        @cloud.middleware("http")
        async def observe_cloud(request: Request, call_next):
            nonlocal cloud_requests
            started = perf_counter()
            if request.method == "POST" and request.url.path == "/api/v1/baseline/measurements":
                canonical_payload_bytes.append(len(await request.body()))
                cloud_requests += 1
            response = await call_next(request)
            if request.method == "POST" and request.url.path == "/api/v1/baseline/measurements":
                cloud_request_ms.append((perf_counter() - started) * 1000)
            return response

        with serve(cloud, "baseline-harness-cloud") as cloud_url:
            repository = TimedRepository(cloud.state.database)
            cloud.state.repository = repository
            gateway = create_gateway_app(
                load_gateway_config(
                    {
                        "GATEWAY_ID": "gateway-baseline-harness",
                        "CLOUD_URL": cloud_url,
                        "SECURITY_MODE": "classical",
                        "CLOUD_TIMEOUT_SECONDS": "5",
                        "CLOUD_MAX_RETRIES": "0",
                        "FAILURE_MODE": "none",
                    }
                )
            )

            @gateway.middleware("http")
            async def observe_gateway(request: Request, call_next):
                started = perf_counter()
                response = await call_next(request)
                if request.method == "POST" and request.url.path == "/api/v1/measurements":
                    gateway_request_ms.append((perf_counter() - started) * 1000)
                return response

            with serve(gateway, "baseline-harness-gateway") as gateway_url:
                legacy = GatewayClient(gateway_url, request_timeout_seconds=5, max_retries=0)
                for sequence in range(samples):
                    measurement = Measurement(
                        device_id="sensor-baseline-harness",
                        temperature_c=22.5,
                        humidity_pct=44.0,
                        timestamp=datetime(2026, 10, 2, 12, 0, tzinfo=UTC),
                        sequence_number=sequence,
                    )
                    started = perf_counter()
                    result = legacy.send(measurement.to_payload())
                    end_to_end_ms.append((perf_counter() - started) * 1000)
                    if not result.success or result.status_code != 202:
                        raise RuntimeError(f"Legacy delivery failed for sequence {sequence}")

            rows = _persisted_rows(cloud_url)

    if len(rows) != samples or len(repository.storage_ms) != samples:
        raise RuntimeError("successful messages were not persisted exactly once")
    if not all(row.get("sequence_number") == sequence for sequence, row in enumerate(rows)):
        raise RuntimeError("Cloud rows did not preserve sequence numbers")
    if not (
        len(end_to_end_ms)
        == len(gateway_request_ms)
        == len(cloud_request_ms)
        == len(canonical_payload_bytes)
        == cloud_requests
        == samples
    ):
        raise RuntimeError("measurement observations were incomplete")

    return {
        "scope": "Legacy client -> Gateway HTTP -> baseline Cloud HTTP -> SQLite",
        "environment": {
            "python": platform.python_version(),
            "os": platform.system(),
            "machine": platform.machine(),
            "sqlite": sqlite3.sqlite_version,
            "fastapi": version("fastapi"),
            "httpx": version("httpx"),
            "uvicorn": version("uvicorn"),
        },
        "security_mode": "classical",
        "configuration": {
            "failure_mode": "none",
            "legacy_request_timeout_seconds": 5,
            "legacy_max_retries": 0,
            "gateway_cloud_timeout_seconds": 5,
            "gateway_cloud_max_retries": 0,
            "workload": "sequential requests with no warmup or concurrent load",
        },
        "samples": samples,
        "successful_messages": samples,
        "persisted_rows": len(rows),
        "legacy_gateway_end_to_end_ms": distribution(end_to_end_ms),
        "gateway_request_ms": distribution(gateway_request_ms),
        "gateway_cloud_request_ms": distribution(cloud_request_ms),
        "cloud_storage_ms": distribution(repository.storage_ms),
        "canonical_payload_bytes": distribution(canonical_payload_bytes),
        "cloud_requests": cloud_requests,
        "gateway_cloud_retry_count": cloud_requests - samples,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=10)
    print(json.dumps(run(parser.parse_args().samples), indent=2, sort_keys=True))
