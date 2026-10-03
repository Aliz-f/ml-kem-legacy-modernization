"""M2-36 measures bytes before parsing, sequencing, injection or forwarding."""

import asyncio
import json
from types import SimpleNamespace

from fastapi.testclient import TestClient
import httpx
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import load_config


PATH = "/api/v1/measurements"
PAYLOAD = {
    "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
    "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 10,
}


class Transport:
    def __init__(self):
        self.calls = 0

    async def send(self, **fields):
        self.calls += 1
        return SimpleNamespace(status="accepted", record_id="rec-1")


@pytest.mark.parametrize("mode", ["classical", "mlkem"])
@pytest.mark.parametrize("size", [1024, 16383, 16384, 16385])
def test_body_limit_before_sequence_and_delivery(mode, size):
    transport = Transport()
    app = create_app(load_config({"SECURITY_MODE": mode}),
                     baseline_transport=transport, secure_transport=transport)
    raw = json.dumps(PAYLOAD).encode()
    body = raw + b" " * (size - len(raw))
    with TestClient(app) as client:
        response = client.post(PATH, content=body)
        if size <= 16384:
            assert response.status_code == 202
            assert transport.calls == 1
        else:
            assert response.status_code == 413
            assert response.json()["error"]["code"] == "PAYLOAD_TOO_LARGE"
            assert transport.calls == 0
            assert "gateway_measurements_rejected_total 1\n" in client.get("/metrics").text
            assert client.post(PATH, json=PAYLOAD).status_code == 202


@pytest.mark.parametrize("headers", [{}, {"Content-Length": "1"}])
def test_streamed_body_stops_reading_as_soon_as_limit_is_exceeded(headers):
    async def scenario():
        transport = Transport()
        app = create_app(load_config({}), baseline_transport=transport)

        async def body():
            yield b" " * 16384
            yield b"x"
            raise AssertionError("Oversized stream was consumed past the limit")

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url="http://test") as client:
            response = await client.post(PATH, content=body(), headers=headers)
        assert response.status_code == 413
        assert transport.calls == 0

    asyncio.run(scenario())
