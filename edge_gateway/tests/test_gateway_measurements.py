"""M2-12 HTTP pipeline, acceptance timing, and sequence retention contracts."""

import asyncio
from datetime import UTC, datetime
import json
import logging
from types import SimpleNamespace

from fastapi.testclient import TestClient
import httpx
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from edge_gateway.crypto.secure_transport import SecureTransportError
from edge_gateway.errors import GatewayError, GatewayErrorCode


PATH = "/api/v1/measurements"
PAYLOAD = {
    "device_id": "sensor-001", "temperature_c": 21.7, "humidity_pct": 42.5,
    "timestamp": "2026-09-21T13:45:31Z", "sequence_number": 10,
}


class Transport:
    def __init__(self, *, result=None, error=None):
        self.calls = []
        self.result = result or SimpleNamespace(status="accepted", record_id="rec-1")
        self.error = error

    async def send(self, **fields):
        self.calls.append(fields)
        if self.error is not None:
            raise self.error
        return self.result


@pytest.mark.parametrize("mode", ["classical", "mlkem"])
@pytest.mark.parametrize("status", ["accepted", "already_accepted"])
def test_selected_transport_receives_canonical_values_and_separate_id(mode, status, caplog):
    baseline = Transport(result=SimpleNamespace(status=status, record_id="rec-1"))
    secure = Transport(result=SimpleNamespace(status=status, record_id="rec-1"))
    hook_calls = []

    async def hook(canonical, request_id):
        assert baseline.calls == secure.calls == []
        hook_calls.append((canonical, request_id))

    config = load_config({"SECURITY_MODE": mode, "GATEWAY_ID": "gateway-test"})
    before = datetime.now(UTC)
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        with TestClient(create_app(
            config, baseline_transport=baseline, secure_transport=secure, processing_hook=hook,
        )) as client:
            response = client.post(PATH, json=PAYLOAD, headers={"X-Request-ID": "untrusted"})
    assert response.status_code == 202
    assert response.json() == {"status": "accepted"}
    canonical, request_id = hook_calls[0]
    fields = canonical.to_dict()
    assert fields == {
        "device_id": PAYLOAD["device_id"], "temperature_c": PAYLOAD["temperature_c"],
        "humidity_pct": PAYLOAD["humidity_pct"], "measured_at": PAYLOAD["timestamp"],
        "sequence_number": 10, "received_at": fields["received_at"], "gateway_id": "gateway-test",
    }
    assert before <= canonical.received_at <= datetime.now(UTC)
    assert request_id.startswith("req-") and request_id != "untrusted"
    assert request_id in caplog.text
    if mode == "mlkem":
        fields.pop("gateway_id")
    selected, unused = (baseline, secure) if mode == "classical" else (secure, baseline)
    assert selected.calls == [{**fields, "request_id": request_id}]
    assert unused.calls == []


@pytest.mark.parametrize(("body", "status", "code"), [
    (b"{", 400, "INVALID_JSON"),
    (json.dumps({**PAYLOAD, "extra": 1}).encode(), 422, "INVALID_MEASUREMENT"),
    (json.dumps({**PAYLOAD, "humidity_pct": "bad"}).encode(), 422, "INVALID_MEASUREMENT"),
    (json.dumps({**PAYLOAD, "humidity_pct": 101}).encode(), 422, "INVALID_MEASUREMENT"),
])
def test_invalid_input_has_no_sequence_hook_or_delivery_effect(body, status, code):
    transport = Transport()
    hooks = []

    async def hook(*args):
        hooks.append(args)

    with TestClient(create_app(
        load_config({}), baseline_transport=transport, processing_hook=hook,
    )) as client:
        response = client.post(PATH, content=body)
        assert response.status_code == status
        assert response.json()["error"]["code"] == code
        assert transport.calls == hooks == []
        # Invalid input must not poison the sequence number.
        assert client.post(PATH, json=PAYLOAD).status_code == 202


def test_sequence_rejections_gaps_independence_and_unique_ids(caplog):
    transport = Transport()
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        with TestClient(create_app(load_config({}), baseline_transport=transport)) as client:
            assert client.post(PATH, json=PAYLOAD).status_code == 202
            for sequence, code in [(10, "DUPLICATE_SEQUENCE"), (9, "OUT_OF_ORDER_SEQUENCE")]:
                response = client.post(PATH, json={**PAYLOAD, "sequence_number": sequence})
                assert response.status_code == 409
                assert response.json()["error"]["code"] == code
            assert len(transport.calls) == 1
            assert client.post(PATH, json={**PAYLOAD, "sequence_number": 12}).status_code == 202
            assert client.post(PATH, json={**PAYLOAD, "device_id": "sensor-002"}).status_code == 202
    assert "sequence_gap_detected" in caplog.text
    assert len({call["request_id"] for call in transport.calls}) == 3


@pytest.mark.parametrize("error", [
    TimeoutError("private-marker"), ConnectionError("private-marker"),
    SecureTransportError("private-marker", retryable=False),
    GatewayError(GatewayErrorCode.CLOUD_UNAVAILABLE),
])
def test_failed_delivery_returns_503_and_retains_sequence(error, caplog):
    transport = Transport(error=error)
    with TestClient(create_app(load_config({}), baseline_transport=transport)) as client:
        failed = client.post(PATH, json=PAYLOAD)
        assert failed.status_code == 503
        assert failed.json()["error"]["code"] == "CLOUD_UNAVAILABLE"
        retry = client.post(PATH, json=PAYLOAD)
        assert retry.status_code == 409
        assert retry.json()["error"]["code"] == "DUPLICATE_SEQUENCE"
    assert len(transport.calls) == 1
    assert "private-marker" not in failed.text + caplog.text


@pytest.mark.parametrize("result", [
    object(), SimpleNamespace(status="pending", record_id="rec-1"),
    SimpleNamespace(status="accepted", record_id=""),
    SimpleNamespace(status="accepted", record_id=None),
])
def test_unconfirmed_delivery_never_returns_202(result):
    with TestClient(create_app(load_config({}), baseline_transport=Transport(result=result))) as client:
        response = client.post(PATH, json=PAYLOAD)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "CLOUD_UNAVAILABLE"


@pytest.mark.parametrize("where", ["hook", "transport"])
def test_internal_failure_returns_safe_500_and_does_not_rollback(where, caplog):
    async def hook(*args):
        raise RuntimeError("private-marker")

    transport = Transport(error=RuntimeError("private-marker") if where == "transport" else None)
    with TestClient(create_app(
        load_config({}), baseline_transport=transport,
        processing_hook=hook if where == "hook" else None,
    ), raise_server_exceptions=False) as client:
        response = client.post(PATH, json=PAYLOAD)
        assert response.status_code == 500
        assert response.json()["error"]["code"] == "INTERNAL_ERROR"
        assert client.post(PATH, json=PAYLOAD).status_code == 409
    assert len(transport.calls) == (1 if where == "transport" else 0)
    assert "private-marker" not in response.text + caplog.text


@pytest.mark.parametrize("with_secure", [False, True])
def test_secure_unavailability_never_calls_baseline(with_secure):
    baseline = Transport()
    secure = Transport(error=SecureTransportError("unavailable", retryable=True))
    with TestClient(create_app(
        load_config({"SECURITY_MODE": "mlkem"}), baseline_transport=baseline,
        secure_transport=secure if with_secure else None,
    )) as client:
        response = client.post(PATH, json=PAYLOAD)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "CLOUD_UNAVAILABLE"
    assert baseline.calls == []


def test_pending_delivery_does_not_return_success_or_hold_sequence_lock():
    async def scenario():
        entered = asyncio.Event()
        release = asyncio.Event()

        class PendingTransport(Transport):
            async def send(self, **fields):
                self.calls.append(fields)
                if fields["sequence_number"] == 10:
                    entered.set()
                    await release.wait()
                    raise TimeoutError()
                return self.result

        transport = PendingTransport()
        app = create_app(load_config({}), baseline_transport=transport)
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url="http://test") as client:
            pending = asyncio.create_task(client.post(PATH, json=PAYLOAD))
            try:
                await asyncio.wait_for(entered.wait(), timeout=2)
                assert not pending.done()
                duplicate = await client.post(PATH, json=PAYLOAD)
                assert duplicate.status_code == 409
                newer = await client.post(PATH, json={**PAYLOAD, "sequence_number": 11})
                assert newer.status_code == 202
            finally:
                release.set()
                failed = await asyncio.wait_for(pending, timeout=2)
            assert failed.status_code == 503
            assert (await client.post(PATH, json={**PAYLOAD, "sequence_number": 11})).status_code == 409
            assert len(transport.calls) == 2

    asyncio.run(scenario())


def test_sequence_state_is_isolated_between_app_instances():
    for _ in range(2):
        with TestClient(create_app(load_config({}), baseline_transport=Transport())) as client:
            assert client.post(PATH, json=PAYLOAD).status_code == 202
            assert client.post(PATH, json=PAYLOAD).status_code == 409
