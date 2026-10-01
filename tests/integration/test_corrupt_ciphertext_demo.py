"""Show a corrupted ciphertext rejected by Cloud with no stored row.

FAILURE_MODE=corrupt_ciphertext and FAILURE_RATE=1.0 seal a valid measurement,
then flip one byte of the outgoing ciphertext copy. Cloud authentication fails,
the decryption-failure counter increments, and the measurement table stays empty.
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
INJECTED = 'gateway_injected_failures_total{failure_type="corrupt_ciphertext"}'


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
    thread = threading.Thread(target=server.run, name="corrupt-ciphertext-cloud", daemon=True)
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


def test_corrupted_ciphertext_is_rejected_and_not_stored(tmp_path: Path) -> None:
    """One injected corruption increments Cloud's decryption-failure counter."""
    cloud = _serve(tmp_path)
    metrics = PqcMetrics()
    try:
        config = load_config(
            {
                "SECURITY_MODE": "mlkem",
                "CLOUD_URL": cloud.url,
                "GATEWAY_ID": "gateway-001",
                "LOG_LEVEL": "WARNING",
                "CLOUD_MAX_RETRIES": "0",
                "FAILURE_MODE": "corrupt_ciphertext",
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
            create_app(config, pqc_metrics=metrics, secure_transport=secure)
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
        assert "ciphertext" not in response.text
        assert gateway.status_code == 200
        gateway_scrape = gateway.text
        cloud_scrape = cloud.metrics()
        stored = cloud.stored_rows()
    finally:
        cloud.stop()

    assert stored == 0
    assert _count(gateway_scrape, 'gateway_mlkem_handshakes_total{result="success"}') == 1
    assert _count(gateway_scrape, "gateway_encryption_failures_total") == 0
    assert _count(gateway_scrape, INJECTED) == 1
    assert _count(gateway_scrape, "gateway_pqc_fallback_total") == 0
    assert "session_id" not in gateway_scrape
    assert _count(cloud_scrape, "cloud_decryption_failures_total") == 1
    assert _count(cloud_scrape, "cloud_authenticated_messages_total") == 0
    assert _count(cloud_scrape, "cloud_measurements_stored_total") == 0
    assert "sensor-001" not in cloud_scrape


def test_recorded_rejection_matches_the_ciphertext_note() -> None:
    document = (
        Path(__file__).parents[2] / "edge_gateway" / "docs" / "corrupt-ciphertext.md"
    ).read_text(encoding="utf-8")
    readme = (Path(__file__).parents[2] / "edge_gateway" / "README.md").read_text(
        encoding="utf-8"
    )

    assert "It does not add a metric." in document
    assert "cloud_decryption_failures_total 1" in document
    assert "cloud_measurements_stored_total 0" in document
    assert f"{INJECTED} 1" in document
    assert "gateway_encryption_failures_total 0" in document
    assert "It does not store the rejected measurement." in readme
