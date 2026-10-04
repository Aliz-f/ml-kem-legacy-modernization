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
            assert response.status_code == 200
            assert response.json() == {"status": "ready", "storage": "ok"}
            database.close()
            assert client.get("/health").json() == {"status": "ok"}
            assert client.get("/ready").status_code == 503
        assert not app.state.running
        assert database.closed
        assert app.state.repository is None
    assert "event=cloud_starting component=cloud_service security_mode=classical" in caplog.text
    assert "event=cloud_shutting_down component=cloud_service" in caplog.text
    assert "event=cloud_ready component=cloud_service" in caplog.text
    assert (tmp_path / "cloud.db").is_file()


def test_readiness_requires_current_write_capability() -> None:
    app = create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))
    with TestClient(app) as client:
        connection = app.state.database._connection
        connection.execute("PRAGMA query_only = ON")
        try:
            response = client.get("/ready")
            assert response.status_code == 503
            assert response.json() == {
                "error": {"code": "SERVICE_UNAVAILABLE", "message": "service is not ready"}
            }
        finally:
            connection.execute("PRAGMA query_only = OFF")


def test_metrics_exposes_bounded_service_information_and_zero_value_cloud_metrics():
    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain; version=0.0.4")
    assert 'cloud_service_info{security_mode="classical"} 1' in response.text
    assert "cloud_request_duration_seconds_count 0" in response.text
    assert "cloud_mlkem_decapsulation_duration_seconds_count 0" in response.text
    assert "cloud_active_sessions 0" in response.text
    assert "request_id" not in response.text


def test_mlkem_readiness_requires_initialized_dependencies_not_an_active_session(monkeypatch):
    from cloud_service import app as module

    app = create_app(load_config({"SECURITY_MODE": "mlkem", "DATABASE_URL": "sqlite:///:memory:"}))
    with TestClient(app) as client:
        assert len(app.state.sessions) == 0
        assert client.get("/ready").json() == {"status": "ready", "storage": "ok", "mlkem": "available"}
        monkeypatch.setattr(module, "_crypto_dependencies_ready", lambda: False)
        response = client.get("/ready")
        assert response.status_code == 503
        assert response.json() == {"error": {"code": "SERVICE_UNAVAILABLE", "message": "service is not ready"}}


@pytest.mark.parametrize(("method", "path"), [
    ("POST", "/api/v1/secure/measurements"),
])
def test_secure_route_unavailable_in_classical_mode(method, path):
    with TestClient(create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))) as client:
        assert client.request(method, path).status_code == 503


def test_factory_validates_process_config(monkeypatch):
    monkeypatch.setenv("PORT", "0")
    with pytest.raises(ConfigurationError, match="PORT"):
        create_app()


def test_invalid_config_exits_without_server_start(monkeypatch, caplog):
    monkeypatch.setenv("PORT", "invalid-private-marker")
    assert main() == 1
    assert "invalid-private-marker" not in caplog.text
    assert "event=cloud_startup_failed component=cloud_service reason=invalid_configuration" in caplog.text


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
