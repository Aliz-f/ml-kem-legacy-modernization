"""M2-20 through M2-25 executable application fault contracts."""

from fastapi.testclient import TestClient
import pytest

from edge_gateway.app import create_app
from edge_gateway.config import load_config
from test_gateway_measurements import PATH, PAYLOAD, Transport


@pytest.mark.parametrize("security_mode", ["classical", "mlkem"])
@pytest.mark.parametrize(("fault", "status", "code"), [
    ("processing_error", 500, "INTERNAL_ERROR"),
    ("drop_message", 503, "CLOUD_UNAVAILABLE"),
])
def test_processing_fault_is_visible_and_preserves_sequence(security_mode, fault, status, code, caplog):
    baseline, secure = Transport(), Transport()
    config = load_config({
        "SECURITY_MODE": security_mode, "FAILURE_MODE": fault, "FAILURE_RATE": "1",
    })
    with TestClient(create_app(config, baseline_transport=baseline, secure_transport=secure)) as client:
        assert client.post(PATH, content=b"{").status_code == 400
        assert client.post(PATH, json={**PAYLOAD, "humidity_pct": 101}).status_code == 422
        response = client.post(PATH, json=PAYLOAD)
        assert response.status_code == status
        assert response.json()["error"]["code"] == code
        assert client.post(PATH, json=PAYLOAD).status_code == 409
        assert client.post(PATH, json={**PAYLOAD, "sequence_number": 9}).status_code == 409
        assert client.get("/health").status_code == 200
        assert client.post(PATH, json={**PAYLOAD, "sequence_number": 11}).status_code == status
        assert f'gateway_injected_failures_total{{failure_type="{fault}"}} 2' in client.get("/metrics").text
    assert baseline.calls == secure.calls == []
    injected = [
        record for record in caplog.records
        if record.getMessage().startswith("event=failure_injected ")
    ]
    assert len(injected) == 2
    assert all(record.failure_type == fault for record in injected)
    assert all(record.request_id.startswith("req-") for record in injected)


@pytest.mark.parametrize("value", ["-1", "30.01", "nan", "inf", "bad", ""])
def test_delay_configuration_rejects_unbounded_or_invalid_values(value):
    from edge_gateway.config import ConfigurationError

    with pytest.raises(ConfigurationError, match="FAILURE_DELAY_SECONDS"):
        load_config({"FAILURE_DELAY_SECONDS": value})


@pytest.mark.parametrize("value", ["0", "0.01", "2", "30"])
def test_delay_configuration_accepts_bounded_values(value):
    assert load_config({"FAILURE_DELAY_SECONDS": value}).failure_delay_seconds == float(value)


def test_processing_delay_yields_and_waits_before_delivery(monkeypatch):
    import asyncio
    import httpx
    from edge_gateway.failure import runtime

    async def scenario():
        entered, release = asyncio.Event(), asyncio.Event()
        delays = []

        async def sleep(seconds):
            delays.append(seconds)
            entered.set()
            await release.wait()

        monkeypatch.setattr(runtime.asyncio, "sleep", sleep)
        transport = Transport()
        app = create_app(load_config({
            "FAILURE_MODE": "processing_delay", "FAILURE_RATE": "1", "FAILURE_DELAY_SECONDS": "2",
        }), baseline_transport=transport)
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url="http://test") as client:
            pending = asyncio.create_task(client.post(PATH, json=PAYLOAD))
            try:
                await asyncio.wait_for(entered.wait(), 2)
                assert transport.calls == []
                assert not pending.done()
                assert (await client.post(PATH, json=PAYLOAD)).status_code == 409
                assert (await client.post(PATH, content=b"{")).status_code == 400
            finally:
                release.set()
                response = await asyncio.wait_for(pending, 2)
            assert response.status_code == 202
            assert len(transport.calls) == 1
            assert delays == [2]

    asyncio.run(scenario())


@pytest.mark.parametrize("security_mode", ["classical", "mlkem"])
@pytest.mark.parametrize("retries", [0, 2])
@pytest.mark.parametrize("fault", ["cloud_timeout", "cloud_unavailable"])
def test_cloud_fault_uses_existing_retries(security_mode, retries, fault, monkeypatch):
    from edge_gateway.cloud.baseline import BaselineCloudClient
    from edge_gateway.crypto.secure_transport import SecureTransport
    from edge_gateway.crypto.session import SessionManager
    from test_secure_transport import _session

    transport_class = BaselineCloudClient if security_mode == "classical" else SecureTransport
    original_init, original_post = transport_class.__init__, transport_class._post
    waits, attempts = [], []

    def initialize(self, *args, **kwargs):
        original_init(self, *args, **kwargs, sleep=waits.append)

    def post(self, *args):
        attempts.append(args)
        return original_post(self, *args)

    async def session(self):
        return _session("sess-test")

    monkeypatch.setattr(transport_class, "__init__", initialize)
    monkeypatch.setattr(transport_class, "_post", post)
    monkeypatch.setattr(SessionManager, "get_or_establish", session)
    config = load_config({
        "SECURITY_MODE": security_mode, "FAILURE_MODE": fault,
        "FAILURE_RATE": "1", "CLOUD_MAX_RETRIES": str(retries),
    })
    with TestClient(create_app(config)) as client:
        assert client.post(PATH, json=PAYLOAD).status_code == 503
        assert client.post(PATH, json=PAYLOAD).status_code == 409
        assert f'gateway_injected_failures_total{{failure_type="{fault}"}} {retries + 1}' in client.get("/metrics").text
    assert len(attempts) == retries + 1
    assert all(attempt == attempts[0] for attempt in attempts)
    assert waits == ([1, 2] if retries == 2 else [])


@pytest.mark.parametrize("security_mode", ["classical", "mlkem"])
@pytest.mark.parametrize(("mode", "rate"), [
    ("none", "1"), ("random", "0"), ("processing_error", "0"),
    ("processing_delay", "0"), ("cloud_timeout", "0"),
    ("cloud_unavailable", "0"), ("drop_message", "0"),
])
def test_disabled_faults_leave_valid_requests_unchanged(security_mode, mode, rate, caplog):
    baseline, secure = Transport(), Transport()
    config = load_config({"SECURITY_MODE": security_mode, "FAILURE_MODE": mode, "FAILURE_RATE": rate})
    with TestClient(create_app(config, baseline_transport=baseline, secure_transport=secure)) as client:
        assert client.post(PATH, json=PAYLOAD).status_code == 202
        assert client.post(PATH, json=PAYLOAD).status_code == 409
        text = client.get("/metrics").text
        for line in text.splitlines():
            if line.startswith("gateway_injected_failures_total{"):
                assert line.endswith(" 0")
    assert len(baseline.calls if security_mode == "classical" else secure.calls) == 1
    assert not (secure.calls if security_mode == "classical" else baseline.calls)
    assert "failure_injection_enabled" not in caplog.text
    assert "failure_injected" not in caplog.text


def test_enabled_warning_is_emitted_at_startup_without_seed_or_payload(caplog):
    import logging

    config = load_config({
        "FAILURE_MODE": "processing_error", "FAILURE_RATE": "1",
        "FAILURE_SEED": "private-seed-marker",
    })
    app = create_app(config, baseline_transport=Transport())
    caplog.clear()
    with TestClient(app) as client:
        response = client.post(PATH, json={**PAYLOAD, "temperature_c": 23.456789})
    warnings = [r for r in caplog.records if "event=failure_injection_enabled" in r.getMessage()]
    assert len(warnings) == 1 and warnings[0].levelno == logging.WARNING
    assert "private-seed-marker" not in caplog.text + response.text
    assert "23.456789" not in caplog.text + response.text


def test_request_context_is_isolated_in_threads_and_cleared_after_failure(monkeypatch):
    import asyncio
    from edge_gateway.crypto.metrics import PqcMetrics
    from edge_gateway.failure.runtime import ApplicationFailures

    async def scenario():
        runtime = ApplicationFailures(load_config({}), PqcMetrics())
        decisions = iter(["cloud_timeout", None, None])
        monkeypatch.setattr(runtime._injector, "select", lambda: next(decisions))
        entered, release = asyncio.Event(), asyncio.Event()

        async def failing():
            async with runtime.request("req-failing"):
                entered.set()
                await release.wait()
                await asyncio.to_thread(runtime.before_cloud_attempt, "req-failing")

        pending = asyncio.create_task(failing())
        try:
            await asyncio.wait_for(entered.wait(), 2)
            async with runtime.request("req-healthy"):
                await asyncio.to_thread(runtime.before_cloud_attempt, "req-healthy")
            release.set()
            with pytest.raises(TimeoutError):
                await asyncio.wait_for(pending, 2)
            # Same ID outside its failed scope must not retain the injected fault.
            await asyncio.to_thread(runtime.before_cloud_attempt, "req-failing")
            async with runtime.request("req-next"):
                await asyncio.to_thread(runtime.before_cloud_attempt, "req-next")
        finally:
            release.set()
            if not pending.done():
                pending.cancel()
                await asyncio.gather(pending, return_exceptions=True)

    asyncio.run(scenario())
