"""Legacy Device contract stays the same in classical and mlkem modes.

These tests start the production route without Cloud transport dependencies.
They check that switching SECURITY_MODE does not change
the Legacy JSON schema, response, or retry behavior, and that the Legacy
Device does not learn Gateway-to-Cloud cryptography.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import random
import threading
import time
from datetime import datetime, timezone
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest
import uvicorn

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from legacy_system import __file__ as legacy_package_file
from legacy_system.client import GatewayClient
from legacy_system.sensor import Sensor


LEGACY_FIELDS = (
    "device_id",
    "temperature_c",
    "humidity_pct",
    "timestamp",
    "sequence_number",
)
CRYPTO_TERMS = ("ML-KEM", "mlkem", "session_id", "nonce", "public_key", "AES-GCM")
FIXTURES = Path(__file__).parents[1] / "fixtures"


@dataclass(frozen=True)
class PostedRequest:
    """One Legacy HTTP request captured before the Gateway answers."""

    url: str
    method: str
    content_type: str | None
    body: bytes


class _Gateway:
    """One real Gateway process bound to an ephemeral local port."""

    def __init__(self, security_mode: str) -> None:
        self.security_mode = security_mode
        app = create_app(
            load_config(
                {
                    "SECURITY_MODE": security_mode,
                    "CLOUD_URL": "http://127.0.0.1:9",
                    "LOG_LEVEL": "WARNING",
                }
            )
        )
        self._server = uvicorn.Server(
            uvicorn.Config(
                app, host="127.0.0.1", port=0, log_level="warning", access_log=False
            )
        )
        self._thread = threading.Thread(
            target=self._server.run,
            name=f"gateway-{security_mode}",
            daemon=True,
        )
        self._thread.start()
        deadline = time.monotonic() + 10
        while not self._server.started:
            if not self._thread.is_alive():
                raise RuntimeError(
                    f"{security_mode} gateway exited before it accepted connections"
                )
            if time.monotonic() > deadline:
                self._server.should_exit = True
                raise RuntimeError(f"{security_mode} gateway did not start")
            time.sleep(0.02)
        sockets = self._server.servers[0].sockets
        if not sockets:
            self._server.should_exit = True
            raise RuntimeError(f"{security_mode} gateway has no socket")
        port = sockets[0].getsockname()[1]
        self.base_url = f"http://127.0.0.1:{port}"

    def close(self) -> None:
        self._server.should_exit = True
        self._thread.join(timeout=5)


@pytest.fixture
def gateways():
    servers = (_Gateway("classical"), _Gateway("mlkem"))
    try:
        yield {server.security_mode: server for server in servers}
    finally:
        for server in servers:
            server.close()


def _recording_opener(posted: list[PostedRequest]):
    def opener(request: Request, timeout: float | None = None):
        posted.append(
            PostedRequest(
                url=request.full_url,
                method=request.get_method(),
                content_type=request.get_header("Content-type"),
                body=request.data,
            )
        )
        return urlopen(request, timeout=timeout)

    return opener


def _send(base_url: str, payload: dict[str, object]):
    posted: list[PostedRequest] = []
    delays: list[float] = []
    client = GatewayClient(
        base_url,
        5.0,
        opener=_recording_opener(posted),
        max_retries=2,
        sleeper=delays.append,
    )
    return client.send(payload), posted, delays


def _exchange(base_url: str, body: bytes, *, method: str = "POST", path: str = "/api/v1/measurements"):
    request = Request(
        base_url + path,
        data=body if method == "POST" else None,
        headers={"Content-Type": "application/json"} if method == "POST" else {},
        method=method,
    )
    try:
        with urlopen(request, timeout=15) as response:
            return response.status, response.read()
    except HTTPError as error:
        return error.code, error.read()


def _fixture(name: str) -> dict[str, object]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def _assert_legacy_post(posted: list[PostedRequest], payload: dict[str, object]) -> None:
    encoded = json.dumps(payload).encode("utf-8")
    assert posted
    for request in posted:
        assert request.method == "POST"
        assert request.url.endswith("/api/v1/measurements")
        assert request.content_type == "application/json"
        assert request.body == encoded
        assert tuple(json.loads(request.body)) == LEGACY_FIELDS


def _assert_no_crypto_terms(body: bytes) -> None:
    text = body.decode("utf-8")
    leaked = [term for term in CRYPTO_TERMS if term in text]
    assert leaked == []


def test_security_mode_preserves_the_legacy_measurement_contract(gateways) -> None:
    """The same Legacy client and payload behave the same in both modes.

    A later delivery that returns the same Legacy result in both modes still
    passes. Divergent status, body, retry delay, or payload fields fail.
    """
    sensor = Sensor(
        "sensor-001",
        random.Random(7),
        clock=lambda: datetime(2026, 9, 21, 12, 5, tzinfo=timezone.utc),
    )
    payloads = (_fixture("valid_legacy_measurement.json"), sensor.read().to_payload())

    for payload in payloads:
        classical = _send(gateways["classical"].base_url, payload)
        mlkem = _send(gateways["mlkem"].base_url, payload)
        assert classical[0] == mlkem[0]
        assert classical[2] == mlkem[2]
        _assert_legacy_post(classical[1], payload)
        _assert_legacy_post(mlkem[1], payload)
        encoded = json.dumps(payload).encode("utf-8")
        classical_status, classical_body = _exchange(gateways["classical"].base_url, encoded)
        mlkem_status, mlkem_body = _exchange(gateways["mlkem"].base_url, encoded)
        assert classical_status == mlkem_status
        assert classical_body == mlkem_body
        _assert_no_crypto_terms(classical_body)
        _assert_no_crypto_terms(mlkem_body)


def test_domain_invalid_measurement_is_not_retried_in_either_mode(gateways) -> None:
    """Parsed JSON with a domain-invalid field stays a non-retryable 422."""
    payload = _fixture("invalid_humidity_measurement.json")
    encoded = json.dumps(payload).encode("utf-8")
    outcomes = {
        mode: _send(server.base_url, payload) for mode, server in gateways.items()
    }
    bodies = {
        mode: _exchange(server.base_url, encoded) for mode, server in gateways.items()
    }

    assert outcomes["classical"][0] == outcomes["mlkem"][0]
    assert outcomes["classical"][2] == []
    assert outcomes["mlkem"][2] == []
    result = outcomes["classical"][0]
    assert result.success is False
    assert result.status_code == 422
    assert result.attempt_count == 1
    assert result.retryable is False
    assert bodies["classical"] == bodies["mlkem"]
    status, body = bodies["classical"]
    assert status == 422
    assert json.loads(body) == {
        "error": {"code": "INVALID_MEASUREMENT", "message": "measurement validation failed"}
    }
    _assert_no_crypto_terms(body)
    _assert_legacy_post(outcomes["classical"][1], payload)
    _assert_legacy_post(outcomes["mlkem"][1], payload)


def test_malformed_json_is_rejected_the_same_way_in_either_mode(gateways) -> None:
    """Unparseable syntax stays 400 and does not depend on security mode."""
    bodies = {
        mode: _exchange(server.base_url, b"{") for mode, server in gateways.items()
    }
    assert bodies["classical"] == bodies["mlkem"]
    status, body = bodies["classical"]
    assert status == 400
    assert json.loads(body) == {
        "error": {"code": "INVALID_JSON", "message": "request body must be valid JSON"}
    }
    _assert_no_crypto_terms(body)


def test_metrics_label_changes_without_changing_the_legacy_response(gateways) -> None:
    """The security-mode label may differ. The Legacy response may not."""
    payload = json.dumps(_fixture("valid_legacy_measurement.json")).encode("utf-8")
    classical_status, classical_body = _exchange(gateways["classical"].base_url, payload)
    mlkem_status, mlkem_body = _exchange(gateways["mlkem"].base_url, payload)
    classical_metrics = _exchange(
        gateways["classical"].base_url, b"", method="GET", path="/metrics"
    )
    mlkem_metrics = _exchange(
        gateways["mlkem"].base_url, b"", method="GET", path="/metrics"
    )

    assert (classical_status, classical_body) == (mlkem_status, mlkem_body)
    _assert_no_crypto_terms(classical_body)
    assert classical_metrics[0] == 200
    assert mlkem_metrics[0] == 200
    classical_text = classical_metrics[1].decode("utf-8")
    mlkem_text = mlkem_metrics[1].decode("utf-8")
    assert 'gateway_service_info{security_mode="classical"} 1' in classical_text
    assert 'gateway_service_info{security_mode="mlkem"} 1' in mlkem_text
    assert classical_text.replace(
        'security_mode="classical"', 'security_mode="mlkem"'
    ) == mlkem_text


def test_legacy_sources_do_not_learn_gateway_crypto() -> None:
    """Member 1's Legacy Device sources stay free of Gateway cryptography."""
    root = Path(legacy_package_file).parent
    sources = sorted(root.glob("*.py"))
    assert {path.name for path in sources} >= {
        "__init__.py",
        "client.py",
        "config.py",
        "failure.py",
        "sensor.py",
    }
    for path in sources:
        text = path.read_text(encoding="utf-8")
        leaked = [term for term in CRYPTO_TERMS if term in text]
        assert leaked == [], path.name
