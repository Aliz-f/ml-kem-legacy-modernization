"""Gateway lifecycle and route registration without configured Cloud transports."""

import logging

from fastapi.testclient import TestClient
import pytest

from edge_gateway.app import create_app, get_config, main
from edge_gateway.config import ConfigurationError, load_config


def test_lifecycle_and_health(caplog):
    app = create_app(load_config({}))
    assert not app.state.running
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        with TestClient(app) as client:
            assert app.state.running
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
        assert not app.state.running
    assert "event=gateway_starting component=edge_gateway security_mode=classical" in caplog.text
    assert "event=gateway_shutting_down component=edge_gateway" in caplog.text
    assert "gateway_ready" not in caplog.text


@pytest.mark.parametrize("mode", ["classical", "mlkem"])
def test_registered_routes_never_claim_readiness_or_acceptance(mode):
    config = load_config({
        "SECURITY_MODE": mode, "CLOUD_URL": "http://unreachable.invalid", "CLOUD_MAX_RETRIES": "0",
    })
    with TestClient(create_app(config)) as client:
        assert client.get("/health").status_code == 200
        for response, code, message in [
            (client.get("/ready"), "SERVICE_UNAVAILABLE", "service is not ready"),
            (client.post("/api/v1/measurements", json={
                "device_id": "sensor-001", "temperature_c": 21.7,
                "humidity_pct": 42.5, "timestamp": "2026-09-21T13:45:31Z",
                "sequence_number": 184,
            }), "CLOUD_UNAVAILABLE", "cloud service is unavailable"),
        ]:
            assert response.status_code == 503
            assert response.json() == {
                "error": {"code": code, "message": message},
            }
        metrics = client.get("/metrics")
        assert metrics.status_code == 200
        assert metrics.headers["content-type"].startswith("text/plain; version=0.0.4")
        assert f'gateway_service_info{{security_mode="{mode}"}} 1\n' in metrics.text


def test_settings_dependency_can_be_overridden_and_isolated():
    first = create_app(load_config({}))
    second = create_app(load_config({}))
    first.dependency_overrides[get_config] = lambda: load_config({"SECURITY_MODE": "mlkem"})
    with TestClient(first) as client:
        assert 'security_mode="mlkem"' in client.get("/metrics").text
        assert not second.state.running
        assert second.dependency_overrides == {}
    with TestClient(second) as client:
        assert 'security_mode="classical"' in client.get("/metrics").text
        assert not first.state.running


def test_shutdown_runs_on_exception():
    app = create_app(load_config({}))
    with pytest.raises(RuntimeError, match="test exit"):
        with TestClient(app):
            raise RuntimeError("test exit")
    assert not app.state.running


@pytest.mark.parametrize(("name", "value"), [
    ("PORT", "invalid-private-marker"),
    ("CLOUD_TIMEOUT_SECONDS", "0"),
    ("PQC_FAILURE_POLICY", "fallback"),
    ("LOG_LEVEL", "invalid-private-marker"),
])
def test_invalid_configuration_prevents_startup(name, value, monkeypatch, caplog):
    import uvicorn

    monkeypatch.setenv(name, value)
    monkeypatch.setattr(uvicorn, "run", lambda *args, **kwargs: pytest.fail("Server started"))
    with pytest.raises(ConfigurationError):
        create_app()
    assert main() == 1
    assert "reason=invalid_configuration" in caplog.text
    assert "invalid-private-marker" not in caplog.text


def test_cli_uses_configured_server_settings_and_loads_once(monkeypatch):
    import uvicorn

    from edge_gateway import app as module

    config = load_config({"HOST": "127.0.0.1", "PORT": "8101", "LOG_LEVEL": "WARN"})
    loads = []
    calls = []

    def settings():
        loads.append(True)
        return config

    monkeypatch.setattr(module, "load_config", settings)
    monkeypatch.setattr(uvicorn, "run", lambda app, **kwargs: calls.append((app, kwargs)))
    assert main() == 0
    assert loads == [True]
    assert calls[0][0].state.config is config
    assert calls[0][1] == {
        "host": "127.0.0.1", "port": 8101, "log_level": logging.WARNING,
        "access_log": False, "timeout_graceful_shutdown": 5,
    }


def test_config_is_not_reloaded_for_requests(monkeypatch):
    from edge_gateway import app as module

    app = create_app(load_config({}))
    monkeypatch.setattr(module, "load_config", lambda: pytest.fail("Config reloaded"))
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        assert client.get("/metrics").status_code == 200


def test_responses_and_lifecycle_logs_do_not_expose_configuration(caplog):
    config = load_config({
        "CLOUD_URL": "http://private-marker.invalid",
        "FAILURE_SEED": "private-marker",
        "GATEWAY_ID": "private-marker",
    })
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        with TestClient(create_app(config)) as client:
            responses = [client.get(path).text for path in ("/health", "/ready", "/metrics")]
            responses.append(client.post("/api/v1/measurements", json={}).text)
    assert "private-marker" not in caplog.text + "".join(responses)
