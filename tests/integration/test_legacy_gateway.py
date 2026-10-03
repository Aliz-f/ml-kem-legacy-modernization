"""M2-43 real Legacy Device-to-Gateway HTTP contract tests."""

from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import socket
from threading import Thread
from time import monotonic, sleep
from types import SimpleNamespace
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
import uvicorn

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from legacy_system.client import GatewayClient


PATH = "/api/v1/measurements"
VALID = {
    "device_id": "sensor-contract", "temperature_c": 22.5, "humidity_pct": 44.0,
    "timestamp": "2026-09-21T12:00:00Z", "sequence_number": 10,
}


class AcceptedCloud:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    async def send(self, **fields: object) -> object:
        self.calls.append(fields)
        return SimpleNamespace(status="accepted", record_id=f"record-{len(self.calls)}")


@contextmanager
def _live_gateway():
    cloud = AcceptedCloud()
    app = create_app(load_config({"SECURITY_MODE": "classical"}), baseline_transport=cloud)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        server = uvicorn.Server(uvicorn.Config(
            app, log_config=None, access_log=False, lifespan="on",
            timeout_graceful_shutdown=5,
        ))
        thread = Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
        thread.start()
        try:
            deadline = monotonic() + 10
            while not server.started and thread.is_alive() and monotonic() < deadline:
                sleep(0.01)
            assert server.started
            yield f"http://127.0.0.1:{listener.getsockname()[1]}", cloud
        finally:
            server.should_exit = True
            thread.join(timeout=10)
            assert not thread.is_alive()


@pytest.fixture
def gateway():
    with _live_gateway() as running:
        yield running


def _raw(base_url: str, body: bytes, *, path: str = PATH) -> tuple[int, dict[str, object]]:
    request = Request(
        base_url + path, data=body, method="POST", headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def _client(base_url: str) -> GatewayClient:
    return GatewayClient(base_url, request_timeout_seconds=5, max_retries=2, sleeper=lambda _: None)


def test_valid_legacy_fixture_is_accepted_only_after_downstream_success(gateway) -> None:
    base_url, cloud = gateway
    result = _client(base_url).send(VALID)

    assert result.success is True
    assert result.status_code == 202
    assert result.attempt_count == 1
    assert len(cloud.calls) == 1
    assert cloud.calls[0]["device_id"] == VALID["device_id"]
    assert cloud.calls[0]["sequence_number"] == VALID["sequence_number"]


@pytest.mark.parametrize(("payload", "code"), [
    ({**VALID, "temperature_c": 85.01}, "INVALID_MEASUREMENT"),
    ({**VALID, "humidity_pct": 100.1}, "INVALID_MEASUREMENT"),
    ({**VALID, "timestamp": "2026-09-21T12:00:00"}, "INVALID_MEASUREMENT"),
    ({key: value for key, value in VALID.items() if key != "device_id"}, "INVALID_MEASUREMENT"),
])
def test_parsed_invalid_legacy_fixtures_are_non_retryable_422(gateway, payload, code) -> None:
    base_url, cloud = gateway
    result = _client(base_url).send(payload)
    status, body = _raw(base_url, json.dumps(payload).encode())

    assert result.success is False
    assert result.status_code == status == 422
    assert result.attempt_count == 1
    assert result.retryable is False
    assert body["error"]["code"] == code
    assert cloud.calls == []


def test_invalid_json_is_400_and_non_retryable(gateway) -> None:
    base_url, cloud = gateway
    attempts = 0

    def opener(request, timeout):
        nonlocal attempts
        attempts += 1
        return urlopen(Request(
            request.full_url, data=b"{", method="POST",
            headers={"Content-Type": "application/json"},
        ), timeout=timeout)

    result = GatewayClient(base_url, 5, opener=opener, max_retries=2).send(VALID)
    status, body = _raw(base_url, b"{")

    assert result.status_code == status == 400
    assert result.retryable is False
    assert result.attempt_count == attempts == 1
    assert body["error"]["code"] == "INVALID_JSON"
    assert cloud.calls == []


def test_sequence_conflicts_are_non_retryable_and_gap_is_accepted_and_counted(
    gateway, caplog: pytest.LogCaptureFixture,
) -> None:
    base_url, cloud = gateway
    client = _client(base_url)

    assert client.send(VALID).status_code == 202
    duplicate = client.send(VALID)
    older = client.send({**VALID, "sequence_number": 9})
    gap = client.send({**VALID, "sequence_number": 12})
    with urlopen(base_url + "/metrics", timeout=5) as response:
        metrics = response.read().decode()

    assert duplicate.status_code == 409 and duplicate.retryable is False
    assert older.status_code == 409 and older.retryable is False
    assert duplicate.attempt_count == older.attempt_count == 1
    assert gap.status_code == 202
    assert len(cloud.calls) == 2
    assert "event=sequence_gap_detected" in caplog.text
    assert "gateway_sequence_gaps_total 1" in metrics


def test_component_sources_do_not_import_each_other() -> None:
    root = Path(__file__).parents[2]
    legacy = "\n".join(path.read_text(encoding="utf-8") for path in
                         (root / "legacy_system/src/legacy_system").rglob("*.py"))
    gateway = "\n".join(path.read_text(encoding="utf-8") for path in
                          (root / "edge_gateway/src/edge_gateway").rglob("*.py"))
    assert "from edge_gateway" not in legacy and "import edge_gateway" not in legacy
    assert "from legacy_system" not in gateway and "import legacy_system" not in gateway
