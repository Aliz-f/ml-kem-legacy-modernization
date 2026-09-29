"""Application lifecycle with storage, before ingestion and secure processing."""

import logging

from fastapi.testclient import TestClient
import pytest

from cloud_service.app import StartupError, create_app, main
from cloud_service.config import ConfigurationError, load_config
from cloud_service.storage.database import StorageError


def test_lifecycle_liveness_and_unready_storage(tmp_path, monkeypatch, caplog):
    monkeypatch.chdir(tmp_path)
    app = create_app(load_config({}))
    assert not app.state.running
    with caplog.at_level(logging.INFO, logger="cloud_service"):
        with TestClient(app) as client:
            assert app.state.running
            database = app.state.database
            assert app.state.repository.list() == []
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
            response = client.get("/ready")
            assert response.status_code == 503
            assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
        assert not app.state.running
        assert database.closed
        assert app.state.repository is None
    assert "cloud_starting security_mode=classical" in caplog.text
    assert "cloud_shutting_down" in caplog.text
    assert "cloud_ready" not in caplog.text
    assert (tmp_path / "cloud.db").is_file()


def test_metrics_exposes_only_bounded_service_information():
    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain; version=0.0.4")
    assert response.text == (
        "# HELP cloud_service_info Cloud Service process information.\n"
        "# TYPE cloud_service_info gauge\n"
        'cloud_service_info{security_mode="classical"} 1\n'
    )


def test_unsupported_secure_mode_fails_startup(caplog):
    app = create_app(load_config({"SECURITY_MODE": "mlkem"}))
    with pytest.raises(StartupError, match="Modernized Mode"):
        with TestClient(app):
            pytest.fail("Secure startup must fail before serving requests")
    assert not app.state.running
    assert app.state.config.security_mode == "mlkem"
    assert "cloud_startup_failed" in caplog.text


@pytest.mark.parametrize(("method", "path"), [
    ("POST", "/api/v1/secure/measurements"),
    ("POST", "/api/v1/crypto/sessions"),
    ("GET", "/api/v1/crypto/public-key"),
    ("GET", "/api/v1/measurements"),
    ("GET", "/api/v1/measurements/record-1"),
])
def test_future_routes_do_not_claim_success(method, path):
    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        assert client.request(method, path).status_code == 404


def test_factory_validates_process_config(monkeypatch):
    monkeypatch.setenv("PORT", "0")
    with pytest.raises(ConfigurationError, match="PORT"):
        create_app()


def test_invalid_config_exits_without_server_start(monkeypatch, caplog):
    monkeypatch.setenv("PORT", "invalid-private-marker")
    assert main() == 1
    assert "invalid-private-marker" not in caplog.text
    assert "invalid configuration" in caplog.text


def test_cli_uses_configured_server_settings(monkeypatch):
    import uvicorn

    from cloud_service import app as module

    config = load_config({"HOST": "127.0.0.1", "PORT": "9101", "LOG_LEVEL": "WARNING"})
    monkeypatch.setattr(module, "load_config", lambda: config)
    calls = []
    monkeypatch.setattr(uvicorn, "run", lambda app, **kwargs: calls.append((app, kwargs)))
    assert main() == 0
    assert calls[0][0].state.config == config
    assert calls[0][1] == {
        "host": "127.0.0.1", "port": 9101, "log_level": "warning",
        "access_log": False, "timeout_graceful_shutdown": 5,
    }


def test_apps_have_independent_lifecycle_state():
    first = create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))
    second = create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))
    with TestClient(first):
        assert first.state.running
        assert not second.state.running
    assert not first.state.running


def test_shutdown_runs_when_context_exits_with_error():
    app = create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))
    with pytest.raises(RuntimeError, match="test exit"):
        with TestClient(app):
            database = app.state.database
            repository = app.state.repository
            raise RuntimeError("test exit")
    assert not app.state.running
    assert database.closed
    with pytest.raises(StorageError, match="closed"):
        repository.list()


def test_storage_initialization_failure_stops_startup(tmp_path, caplog):
    target = tmp_path / "missing-parent" / "private-path-marker.db"
    app = create_app(load_config({"DATABASE_URL": f"sqlite:///{target.as_posix()}"}))
    with pytest.raises(StartupError, match="storage initialization") as error:
        with TestClient(app):
            pytest.fail("Storage failure must prevent startup")
    assert not app.state.running
    assert app.state.database is None
    assert app.state.repository is None
    assert "private-path-marker" not in str(error.value) + caplog.text


def test_unsupported_secure_startup_does_not_create_database(tmp_path):
    target = tmp_path / "secure.db"
    config = load_config({"SECURITY_MODE": "mlkem", "DATABASE_URL": f"sqlite:///{target.as_posix()}"})
    with pytest.raises(StartupError):
        with TestClient(create_app(config)):
            pytest.fail("Secure processing is not implemented")
    assert not target.exists()
