"""Measure the real ML-KEM Legacy -> Gateway -> Cloud path.

This small M5-65 through M5-69 harness mirrors ``measure_baseline_e2e.py``.
It reports the first secure request separately from reused-session requests and
prints observations only; it is not a capacity benchmark.

Example: ``uv run python scripts/measure_modernized_e2e.py --samples 10``.
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
from edge_gateway.crypto.metrics import PqcMetrics
from legacy_system.client import GatewayClient
from legacy_system.sensor import Measurement


class TimedRepository(MeasurementRepository):
    """Record Cloud SQLite saves for this harness without altering production code."""

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
    """Run one production ASGI app on a disposable loopback port."""
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
    """Return a small, stable summary without creating performance targets."""
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


def _metrics(url: str) -> str:
    with urlopen(f"{url}/metrics", timeout=5) as response:
        return response.read().decode("utf-8")


def _sample(metrics: str, name: str) -> float:
    values = [line for line in metrics.splitlines() if line.startswith(name + " ")]
    if len(values) != 1:
        raise RuntimeError(f"expected one metrics sample for {name}")
    return float(values[0].rsplit(" ", 1)[1])


def run(samples: int = 10) -> dict[str, object]:
    """Run equivalent successful secure messages and return measured observations."""
    if type(samples) is not int or not 2 <= samples <= 100:
        raise ValueError("samples must be an integer from 2 to 100")

    gateway_request_ms: list[float] = []
    cloud_request_ms: list[float] = []
    envelope_payload_bytes: list[int] = []
    end_to_end_ms: list[float] = []
    cloud_requests = 0
    session_establishment: dict[str, object] = {}

    with TemporaryDirectory(prefix="modernized-e2e-") as directory:
        database_url = f"sqlite:///{(Path(directory) / 'measurements.db').as_posix()}"
        cloud = create_cloud_app(
            load_cloud_config(
                {
                    "DATABASE_URL": database_url,
                    "SECURITY_MODE": "mlkem",
                    "FAILURE_MODE": "none",
                    "LOG_LEVEL": "WARNING",
                }
            )
        )

        @cloud.middleware("http")
        async def observe_cloud(request: Request, call_next):
            nonlocal cloud_requests
            started = perf_counter()
            if request.method == "POST" and request.url.path == "/api/v1/secure/measurements":
                envelope_payload_bytes.append(len(await request.body()))
                cloud_requests += 1
            response = await call_next(request)
            if request.method == "POST" and request.url.path == "/api/v1/secure/measurements":
                cloud_request_ms.append((perf_counter() - started) * 1000)
            return response

        with serve(cloud, "modernized-harness-cloud") as cloud_url:
            repository = TimedRepository(cloud.state.database)
            cloud.state.repository = repository
            pqc_metrics = PqcMetrics()
            gateway = create_gateway_app(
                load_gateway_config(
                    {
                        "GATEWAY_ID": "gateway-baseline-harness",
                        "CLOUD_URL": cloud_url,
                        "SECURITY_MODE": "mlkem",
                        "PQC_FAILURE_POLICY": "fail_closed",
                        "CLOUD_TIMEOUT_SECONDS": "5",
                        "CLOUD_MAX_RETRIES": "0",
                        "FAILURE_MODE": "none",
                        "LOG_LEVEL": "WARNING",
                    }
                ),
                pqc_metrics=pqc_metrics,
            )

            @gateway.middleware("http")
            async def observe_gateway(request: Request, call_next):
                started = perf_counter()
                response = await call_next(request)
                if request.method == "POST" and request.url.path == "/api/v1/measurements":
                    gateway_request_ms.append((perf_counter() - started) * 1000)
                return response

            with serve(gateway, "modernized-harness-gateway") as gateway_url:
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
                gateway_metrics = _metrics(gateway_url)
                cloud_metrics = _metrics(cloud_url)
                # Snapshot while the Gateway and Cloud still hold their active session.
                session_establishment = {
                    "gateway_handshakes": pqc_metrics.handshakes_succeeded,
                    "gateway_handshake_failures": pqc_metrics.mlkem_handshake_failures_total,
                    "gateway_handshake_ms": distribution(
                        [pqc_metrics.handshake_duration.total_seconds * 1000]
                    ),
                    "gateway_public_key_ms": distribution(
                        [pqc_metrics.public_key_duration.total_seconds * 1000]
                    ),
                    "gateway_encapsulation_ms": distribution(
                        [pqc_metrics.encapsulation_duration.total_seconds * 1000]
                    ),
                    "gateway_active_session": pqc_metrics.active_session,
                    "gateway_session_reestablishments": pqc_metrics.reestablishments["success"],
                    "gateway_encryption_failures": pqc_metrics.encryption_failures_total,
                    "gateway_pqc_fallbacks": pqc_metrics.pqc_fallback_total,
                    "cloud_sessions_created": int(
                        _sample(cloud_metrics, "cloud_mlkem_sessions_created_total")
                    ),
                    "cloud_session_failures": int(
                        _sample(cloud_metrics, "cloud_mlkem_session_failures_total")
                    ),
                    "cloud_decapsulation_ms": distribution(
                        [
                            _sample(
                                cloud_metrics,
                                "cloud_mlkem_decapsulation_duration_seconds_sum",
                            )
                            * 1000
                        ]
                    ),
                    "cloud_active_sessions": int(_sample(cloud_metrics, "cloud_active_sessions")),
                    "cloud_decryption_failures": int(
                        _sample(cloud_metrics, "cloud_decryption_failures_total")
                    ),
                }

            rows = _persisted_rows(cloud_url)

    if len(rows) != samples or len(repository.storage_ms) != samples:
        raise RuntimeError("successful messages were not persisted exactly once")
    if not all(row.get("sequence_number") == sequence for sequence, row in enumerate(rows)):
        raise RuntimeError("Cloud rows did not preserve sequence numbers")
    if not (
        len(end_to_end_ms)
        == len(gateway_request_ms)
        == len(cloud_request_ms)
        == len(envelope_payload_bytes)
        == cloud_requests
        == samples
    ):
        raise RuntimeError("measurement observations were incomplete")
    if pqc_metrics.handshakes_succeeded != 1 or pqc_metrics.handshake_duration.count != 1:
        raise RuntimeError("workload did not establish exactly one initial ML-KEM session")
    if pqc_metrics.message_duration["first"].count != 1:
        raise RuntimeError("first secure message was not recorded separately")
    if pqc_metrics.message_duration["steady"].count != samples - 1:
        raise RuntimeError("later secure messages did not reuse the active session")

    return {
        "scope": "Legacy client -> Gateway HTTP -> ML-KEM Cloud HTTP -> SQLite",
        "environment": {
            "python": platform.python_version(),
            "os": platform.system(),
            "machine": platform.machine(),
            "sqlite": sqlite3.sqlite_version,
            "fastapi": version("fastapi"),
            "httpx": version("httpx"),
            "uvicorn": version("uvicorn"),
        },
        "security_mode": "mlkem",
        "configuration": {
            "failure_mode": "none",
            "log_level": "WARNING",
            "legacy_request_timeout_seconds": 5,
            "legacy_max_retries": 0,
            "gateway_cloud_timeout_seconds": 5,
            "gateway_cloud_max_retries": 0,
            "pqc_failure_policy": "fail_closed",
            "workload": "sequential requests with no warmup or concurrent load",
        },
        "samples": samples,
        "successful_messages": samples,
        "persisted_rows": len(rows),
        "first_message": {
            "legacy_gateway_end_to_end_ms": distribution(end_to_end_ms[:1]),
            "gateway_request_ms": distribution(gateway_request_ms[:1]),
            "gateway_cloud_request_ms": distribution(cloud_request_ms[:1]),
        },
        "steady_state": {
            "legacy_gateway_end_to_end_ms": distribution(end_to_end_ms[1:]),
            "gateway_request_ms": distribution(gateway_request_ms[1:]),
            "gateway_cloud_request_ms": distribution(cloud_request_ms[1:]),
            "cloud_storage_ms": distribution(repository.storage_ms[1:]),
        },
        "secure_envelope_bytes": distribution(envelope_payload_bytes),
        "cloud_storage_ms": distribution(repository.storage_ms),
        "cloud_requests": cloud_requests,
        "gateway_cloud_retry_count": int(_sample(gateway_metrics, "gateway_cloud_retries_total")),
        "session_establishment": session_establishment,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=10)
    print(json.dumps(run(parser.parse_args().samples), indent=2, sort_keys=True))
