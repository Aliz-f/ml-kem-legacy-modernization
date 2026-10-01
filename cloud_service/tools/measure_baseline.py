"""Cloud-local serializer/HTTP/SQLite integration and measurement harness.

Run from the workspace with all packages and test extras installed. This is
not the Gateway HTTP client and does not exercise Legacy or Gateway routing.
"""

import argparse
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timezone
from importlib.metadata import version
import json
import logging
import math
from pathlib import Path
import platform
import socket
import sqlite3
from statistics import median
from tempfile import TemporaryDirectory
from threading import Thread
from time import perf_counter, sleep

import httpx
import uvicorn

from cloud_service.app import create_app
from cloud_service.config import load_config
from cloud_service.storage.database import Database
from cloud_service.storage.repository import MeasurementRepository
from edge_gateway.crypto.plaintext import serialize_canonical_measurement


def canonical(sequence):
    return {
        "device_id": "sensor-baseline", "gateway_id": "gateway-baseline",
        "temperature_c": 21.7, "humidity_pct": 42.5,
        "measured_at": "2026-09-21T13:45:31Z",
        "received_at": "2026-09-21T13:45:31.218Z",
        "sequence_number": sequence,
    }


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def distribution(samples):
    ordered = sorted(samples)
    return {
        "count": len(samples), "min": min(samples), "median": median(samples),
        "p95": ordered[math.ceil(len(samples) * 0.95) - 1], "max": max(samples),
    }


class TimedRepository(MeasurementRepository):
    """Harness-only timing includes row mapping, locking, SQL and commit."""

    def __init__(self, database):
        super().__init__(database)
        self.elapsed_ms = []

    def save_idempotent(self, measurement):
        start = perf_counter()
        try:
            return super().save_idempotent(measurement)
        finally:
            self.elapsed_ms.append((perf_counter() - start) * 1000)


class Capture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.messages = []

    def emit(self, record):
        self.messages.append(record.getMessage())


@contextmanager
def live_cloud(database_url):
    app = create_app(load_config({"DATABASE_URL": database_url, "SECURITY_MODE": "classical"}))
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan(app):
        async with original_lifespan(app):
            app.state.repository = TimedRepository(app.state.database)
            yield

    app.router.lifespan_context = lifespan
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        server = uvicorn.Server(uvicorn.Config(
            app, log_config=None, access_log=False, lifespan="on",
            timeout_graceful_shutdown=5,
        ))
        thread = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            deadline = perf_counter() + 10
            while not server.started and thread.is_alive() and perf_counter() < deadline:
                sleep(0.01)
            require(server.started, "Cloud did not start")
            with httpx.Client(
                base_url=f"http://127.0.0.1:{listener.getsockname()[1]}",
                timeout=5, trust_env=False,
            ) as client:
                yield app, client
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            require(not thread.is_alive(), "Cloud did not stop")


def run(samples=100):
    if type(samples) is not int or not 1 <= samples <= 1000:
        raise ValueError("samples must be an integer from 1 to 1000")
    capture = Capture()
    logger = logging.getLogger("cloud_service")
    previous_level = logger.level
    logger.addHandler(capture)
    started = datetime.now(timezone.utc)
    try:
        with TemporaryDirectory(prefix="cloud-baseline-") as directory:
            database_url = f"sqlite:///{(Path(directory) / 'baseline.db').as_posix()}"
            with live_cloud(database_url) as (app, client):
                require(client.get("/health").status_code == 200, "health failed")
                require(client.get("/ready").status_code == 200, "readiness contract changed")
                request_ms, sizes, ids = [], [], []

                def post(sequence, request_id):
                    body = serialize_canonical_measurement(**canonical(sequence))
                    require("request_id" not in json.loads(body), "request ID leaked into body")
                    begin = perf_counter()
                    response = client.post(
                        "/api/v1/baseline/measurements", content=body,
                        headers={"Content-Type": "application/json", "X-Request-ID": request_id},
                    )
                    return response, (perf_counter() - begin) * 1000, len(body)

                for sequence in range(samples):
                    response, elapsed, size = post(sequence, f"baseline-{sequence}")
                    require(response.status_code == 202, "insert HTTP status failed")
                    require(response.json()["status"] == "accepted", "insert was not accepted")
                    ids.append(response.json()["record_id"])
                    request_ms.append(elapsed)
                    sizes.append(size)
                repository = app.state.repository
                insert_storage_ms = list(repository.elapsed_ms)
                require(len(set(ids)) == samples, "record IDs not unique")
                response, duplicate_ms, _ = post(0, "baseline-duplicate")
                require(response.status_code == 202 and response.json() == {
                    "status": "already_accepted", "record_id": ids[0],
                }, "duplicate response failed")
                duplicate_storage_ms = repository.elapsed_ms[-1]

                # Real SQLite write failure, confined to this disposable connection.
                with app.state.database.transaction() as connection:
                    connection.execute("PRAGMA query_only = ON")
                try:
                    response, failure_ms, _ = post(samples, "baseline-storage-failure")
                    require(response.status_code == 503 and response.json() == {
                        "error": {"code": "STORAGE_UNAVAILABLE", "message": "storage is unavailable"},
                    }, "storage failure was not safely reported")
                    failure_storage_ms = repository.elapsed_ms[-1]
                finally:
                    with app.state.database.transaction() as connection:
                        connection.execute("PRAGMA query_only = OFF")

                listing = client.get("/api/v1/measurements", params={"limit": samples})
                require(listing.status_code == 200, "query failed")
                rows = listing.json()["items"]
                require(len(rows) == samples, "unexpected row count")
                for sequence, row in enumerate(rows):
                    expected = canonical(sequence)
                    expected["gateway_received_at"] = expected.pop("received_at")
                    for field, value in expected.items():
                        actual = row[field]
                        if field in {"measured_at", "gateway_received_at"}:
                            require(datetime.fromisoformat(actual) == datetime.fromisoformat(value), "timestamp changed")
                        else:
                            require(actual == value, "canonical field changed")
                    require(set(row) == set(expected) | {"record_id", "cloud_received_at"}, "stored fields changed")
                    require(row["record_id"] == ids[sequence], "record ID changed")
                    require(started <= datetime.fromisoformat(row["cloud_received_at"]) <= datetime.now(timezone.utc), "Cloud timestamp invalid")
                    detail = client.get(f"/api/v1/measurements/{ids[sequence]}")
                    require(detail.status_code == 200 and detail.json() == row, "detail query mismatch")
                    require(any(
                        f"request_id='baseline-{sequence}' record_id={ids[sequence]}" in message
                        for message in capture.messages
                    ), "request correlation missing")
                require(any("request_id='baseline-duplicate'" in message for message in capture.messages), "duplicate correlation missing")
                require(any("event=storage_failed" in message and "request_id='baseline-storage-failure'" in message
                            for message in capture.messages), "failure correlation missing")
            reopened = Database(database_url)
            try:
                persisted = MeasurementRepository(reopened).list(limit=samples + 1)
                require([row.to_dict() for row in persisted] == rows, "persistence changed after restart")
                require(MeasurementRepository(reopened).find_by_device_sequence("sensor-baseline", samples) is None, "failed write persisted")
            finally:
                reopened.close()
    finally:
        logger.removeHandler(capture)
        logger.setLevel(previous_level)
    return {
        "measured_at": started.isoformat(),
        "scope": "Gateway canonical serializer -> harness HTTPX -> loopback Cloud HTTP -> SQLite -> query API",
        "environment": {
            "python": platform.python_version(), "os": platform.system(),
            "sqlite": sqlite3.sqlite_version,
            **{name: version(name) for name in ("fastapi", "uvicorn", "httpx")},
        },
        "samples": samples, "successful_inserts": len(ids), "persisted_rows_after_reopen": len(persisted),
        "insert_request_ms": distribution(request_ms),
        "insert_storage_ms": distribution(insert_storage_ms),
        "payload_bytes": distribution(sizes),
        "duplicate": {"http_status": 202, "status": "already_accepted", "same_record_id": True,
                      "request_ms": duplicate_ms, "storage_ms": duplicate_storage_ms},
        "storage_failure": {"http_status": 503, "code": "STORAGE_UNAVAILABLE", "persisted": False,
                            "request_ms": failure_ms, "storage_ms": failure_storage_ms},
        "verified": ["canonical fields", "request log correlation", "header-only request ID",
                     "timestamp mapping", "Cloud metadata", "list and detail queries", "persistence after reopen"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=100)
    args = parser.parse_args()
    print(json.dumps(run(args.samples), indent=2))
