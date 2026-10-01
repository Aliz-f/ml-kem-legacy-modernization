"""Show an injected ML-KEM handshake failure with no session and no fallback.

FAILURE_MODE=mlkem_handshake_failure stops session establishment before a
public key is fetched. The Gateway returns failure, the handshake-failure
counter increments, and the baseline endpoint is not called.
This module does not add a metric.
"""

from __future__ import annotations

import sqlite3
import threading
import time
import urllib.request
from pathlib import Path

import uvicorn
from fastapi.testclient import TestClient

from cloud_service.app import create_app as create_cloud_app
from cloud_service.config import load_config as load_cloud_config
from edge_gateway.app import create_app
from edge_gateway.config import load_config
from edge_gateway.crypto.failure import CryptoFailureInjector
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.secure_transport import SecureTransport
from edge_gateway.crypto.session import SessionManager


PATH = "/api/v1/measurements"
HANDSHAKE_FAILURE = 'gateway_mlkem_handshakes_total{result="failure"}'
HANDSHAKE_SUCCESS = 'gateway_mlkem_handshakes_total{result="success"}'
INJECTED_REASON = 'gateway_mlkem_handshake_failures_total{reason="injected"}'
INJECTED_FAULT = 'gateway_injected_failures_total{failure_type="mlkem_handshake_failure"}'


class _Baseline:
    def __init__(self) -> None:
        self.calls = 0

    async def send(self, **_fields: object) -> dict[str, str]:
        self.calls += 1
        return {"status": "accepted", "record_id": "rec-baseline"}


class _Cloud:
    def __init__(
        self, server: uvicorn.Server, thread: threading.Thread, url: str, database: Path
    ) -> None:
        self._server = server
        self._thread = thread
        self.url = url
        self.database = database

    def stop(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5)

    def metrics(self) -> str:
        with urllib.request.urlopen(f"{self.url}/metrics", timeout=5) as response:
            assert response.status == 200
            return response.read().decode("utf-8")

    def stored_rows(self) -> int:
        with sqlite3.connect(self.database) as connection:
            return int(connection.execute("SELECT COUNT(*) FROM measurements").fetchone()[0])


def _serve(tmp_path: Path) -> _Cloud:
    database = tmp_path / "cloud.db"
    app = create_cloud_app(
        load_cloud_config(
            {
                "DATABASE_URL": f"sqlite:///{database}",
                "SECURITY_MODE": "mlkem",
                "LOG_LEVEL": "WARNING",
            }
        )
    )
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name="handshake-failure-cloud", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            server.should_exit = True
            raise RuntimeError("Cloud did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        raise RuntimeError("Cloud has no socket")
    return _Cloud(server, thread, f"http://127.0.0.1:{sockets[0].getsockname()[1]}", database)


def _count(scrape: str, sample: str) -> int:
    matches = [line for line in scrape.splitlines() if line.startswith(sample + " ")]
    assert len(matches) == 1, sample
    return int(matches[0].rsplit(" ", 1)[1])


def test_handshake_failure_stays_closed_without_a_session(tmp_path: Path) -> None:
    """One injected handshake failure increments the failure counter and skips baseline."""
    cloud = _serve(tmp_path)
    metrics = PqcMetrics()
    baseline = _Baseline()
    try:
        config = load_config(
            {
                "SECURITY_MODE": "mlkem",
                "CLOUD_URL": cloud.url,
                "GATEWAY_ID": "gateway-001",
                "LOG_LEVEL": "WARNING",
                "CLOUD_MAX_RETRIES": "0",
                "FAILURE_MODE": "mlkem_handshake_failure",
                "FAILURE_RATE": "1.0",
            }
        )
        injector = CryptoFailureInjector.from_config(config)
        sessions = SessionManager(
            config.gateway_id,
            cloud.url,
            config.cloud_timeout_seconds,
            metrics=metrics,
            injector=injector,
        )
        secure = SecureTransport(
            sessions,
            cloud_url=cloud.url,
            timeout_seconds=config.cloud_timeout_seconds,
            max_retries=0,
            metrics=metrics,
            injector=injector,
            sleep=lambda _delay: None,
        )
        with TestClient(
            create_app(
                config,
                pqc_metrics=metrics,
                secure_transport=secure,
                baseline_transport=baseline,
            )
        ) as client:
            response = client.post(
                PATH,
                json={
                    "device_id": "sensor-001",
                    "temperature_c": 22.5,
                    "humidity_pct": 44.0,
                    "timestamp": "2026-09-21T13:45:31Z",
                    "sequence_number": 1,
                },
            )
            gateway = client.get("/metrics")
        assert response.status_code == 503
        assert response.json() == {
            "error": {"code": "CLOUD_UNAVAILABLE", "message": "cloud service is unavailable"}
        }
        assert "session_id" not in response.text
        assert gateway.status_code == 200
        gateway_scrape = gateway.text
        cloud_scrape = cloud.metrics()
        stored = cloud.stored_rows()
        held = sessions._session
    finally:
        cloud.stop()

    assert held is None
    assert baseline.calls == 0
    assert stored == 0
    assert _count(gateway_scrape, HANDSHAKE_SUCCESS) == 0
    assert _count(gateway_scrape, HANDSHAKE_FAILURE) == 1
    assert _count(gateway_scrape, INJECTED_REASON) == 1
    assert _count(gateway_scrape, INJECTED_FAULT) == 1
    assert _count(gateway_scrape, "gateway_active_session") == 0
    assert _count(gateway_scrape, "gateway_encryption_failures_total") == 0
    assert _count(gateway_scrape, "gateway_pqc_fallback_total") == 0
    assert "session_id" not in gateway_scrape
    assert _count(cloud_scrape, "cloud_mlkem_sessions_created_total") == 0
    assert _count(cloud_scrape, "cloud_measurements_stored_total") == 0
    assert _count(cloud_scrape, "cloud_decryption_failures_total") == 0


def test_recorded_handshake_failure_matches_the_note() -> None:
    document = (
        Path(__file__).parents[2] / "edge_gateway" / "docs" / "mlkem-handshake-failure.md"
    ).read_text(encoding="utf-8")
    readme = (Path(__file__).parents[2] / "edge_gateway" / "README.md").read_text(
        encoding="utf-8"
    )

    assert "It does not add a metric." in document
    assert f"{HANDSHAKE_FAILURE} 1" in document
    assert f"{INJECTED_REASON} 1" in document
    assert "gateway_active_session 0" in document
    assert "gateway_pqc_fallback_total 0" in document
    assert "cloud_mlkem_sessions_created_total 0" in document
    assert "It does not call the baseline endpoint." in readme
