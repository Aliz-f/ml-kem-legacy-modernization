"""M2-37 lifecycle cleanup and real Uvicorn signal handling."""

import os
import signal
import socket
import subprocess
import sys
import time

from fastapi.testclient import TestClient
import httpx
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import load_config


def test_lifespan_closes_baseline_and_rejects_late_requests():
    events = []

    class Baseline:
        def shutdown(self):
            assert not app.state.running
            assert app.state.stopping
            events.append("baseline_closed")

        async def send(self, **fields):
            raise AssertionError("Delivery after shutdown")

    app = create_app(load_config({}), baseline_transport=Baseline())
    with TestClient(app) as client:
        assert client.get("/ready").status_code == 200
    assert events == ["baseline_closed"]
    assert client.post("/api/v1/measurements", content=b"{}").status_code == 503
    assert client.get("/ready").status_code == 503


@pytest.mark.parametrize("mode", ["classical", "mlkem"])
@pytest.mark.parametrize("stop_signal", [signal.SIGINT, signal.SIGTERM])
def test_gateway_process_exits_cleanly_on_signal(mode, stop_signal):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    env = {
        **os.environ, "HOST": "127.0.0.1", "PORT": str(port), "SECURITY_MODE": mode,
        "CLOUD_URL": "http://127.0.0.1:9", "PQC_FAILURE_POLICY": "fail_closed",
        "FAILURE_MODE": "none", "FAILURE_RATE": "0", "LOG_LEVEL": "INFO",
    }
    process = subprocess.Popen([sys.executable, "-m", "edge_gateway.app"], env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        with httpx.Client(base_url=f"http://127.0.0.1:{port}", trust_env=False, timeout=0.5) as client:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                assert process.poll() is None, "Gateway exited before becoming ready"
                try:
                    if client.get("/ready").status_code == 200:
                        break
                except httpx.TransportError:
                    pass
                time.sleep(0.02)
            else:
                pytest.fail("Gateway did not become ready")
            assert client.get("/health").status_code == 200
            assert "gateway_cloud_requests_total 0" in client.get("/metrics").text
        process.send_signal(stop_signal)
        output, _ = process.communicate(timeout=10)
        # Uvicorn may re-raise the handled signal after its clean shutdown.
        assert process.returncode in (0, -stop_signal, 128 + stop_signal)
        assert "gateway_shutting_down" in output
        assert "Application shutdown complete" in output
        assert "Traceback" not in output
        assert "ERROR" not in output
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=5)
