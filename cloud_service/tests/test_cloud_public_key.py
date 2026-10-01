"""Public-key wire contract and fail-closed application lifecycle."""

from base64 import urlsafe_b64decode, urlsafe_b64encode
import logging
import traceback

from fastapi.testclient import TestClient
import pytest

from cloud_service import app as app_module
from cloud_service.app import StartupError, create_app
from cloud_service.config import load_config
from cloud_service.crypto.keys import KeyService
from cloud_service.crypto.mlkem import MlKemError
from edge_gateway.crypto.mlkem import encapsulate
from edge_gateway.crypto.public_key import parse_public_key_response

PATH = "/api/v1/crypto/public-key"


def secure_app(database_url="sqlite:///:memory:"):
    return create_app(load_config({"DATABASE_URL": database_url, "SECURITY_MODE": "mlkem"}))


def test_public_key_contract_gateway_interop_and_secret_boundary(tmp_path, caplog):
    path = tmp_path / "cloud.db"
    app = secure_app(f"sqlite:///{path.as_posix()}")
    assert app.state.keys is None
    with caplog.at_level(logging.DEBUG, logger="cloud_service"):
        with TestClient(app) as client:
            keys = app.state.keys
            response = client.get(PATH)
            assert response.status_code == 200
            assert response.headers["cache-control"] == "no-store"
            payload = response.json()
            assert set(payload) == {"protocol_version", "algorithm", "key_id", "public_key"}
            parsed = parse_public_key_response(payload)
            assert parsed.protocol_version == "1"
            assert parsed.algorithm == "ML-KEM-768"
            assert parsed.key_id == keys.key_id
            assert parsed.public_key == keys.public_key
            assert urlsafe_b64encode(urlsafe_b64decode(payload["public_key"] + "==")).decode().rstrip("=") == payload["public_key"]
            ciphertext, expected = encapsulate(parsed.public_key)
            actual = keys.decapsulate(ciphertext)
            assert actual == expected
            seed = keys._private_key._key.private_bytes_raw()
            assert client.get(PATH).json() == payload
            assert client.get("/health").status_code == 200
            assert client.get("/ready").status_code == 503
            assert client.post("/api/v1/baseline/measurements", json={}).status_code == 503
            assert client.post("/api/v1/crypto/sessions", json={}).status_code == 400
            assert client.post("/api/v1/secure/measurements", json={}).status_code == 400
            assert app.state.repository.list() == []
            with app.state.database.transaction() as connection:
                tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                assert [row[0] for row in tables] == ["measurements"]
        assert keys.closed
        assert keys._private_key._key is None
        assert app.state.keys is app.state.database is app.state.repository is None
        assert not app.state.running
        output = caplog.text + response.text + repr(keys)
        for secret in (seed, actual):
            assert all(value not in output for value in (repr(secret), secret.hex(), urlsafe_b64encode(secret).decode()))
            assert secret not in path.read_bytes()


def test_restart_rotates_keys_and_id():
    app = secure_app()
    with TestClient(app) as client:
        first = client.get(PATH).json()
        previous = app.state.keys
    with TestClient(app) as client:
        second = client.get(PATH).json()
        assert first["key_id"] != second["key_id"]
        assert first["public_key"] != second["public_key"]
        assert previous.closed


def test_classical_does_not_generate_keys(monkeypatch):
    def unexpected():
        pytest.fail("Classical mode must not generate keys")
    monkeypatch.setattr(app_module, "KeyService", unexpected)
    app = create_app(load_config({"DATABASE_URL": "sqlite:///:memory:"}))
    with TestClient(app) as client:
        assert app.state.keys is None
        assert client.get(PATH).status_code == 503
        assert client.get("/health").status_code == 200


def test_endpoint_without_lifespan_is_unavailable():
    with TestClient(secure_app()) as client:
        client.app.state.keys.close()
        assert client.get(PATH).status_code == 503
    client = TestClient(secure_app())
    try:
        assert client.get(PATH).status_code == 503
    finally:
        client.close()


def test_key_failure_aborts_startup_and_closes_storage(monkeypatch, caplog):
    databases = []
    original = app_module.Database
    def database(url):
        result = original(url)
        databases.append(result)
        return result
    def fail():
        raise RuntimeError("private-key-marker")
    monkeypatch.setattr(app_module, "Database", database)
    monkeypatch.setattr(app_module, "KeyService", fail)
    app = secure_app()
    with pytest.raises(StartupError, match="key initialization failed") as caught:
        with TestClient(app):
            pytest.fail("Failed key generation must stop startup")
    assert databases[0].closed
    assert app.state.keys is app.state.database is app.state.repository is None
    assert not app.state.running
    assert app.state.config.security_mode == "mlkem"
    assert "private-key-marker" not in caplog.text + "".join(traceback.format_exception(caught.value))


def test_public_response_failure_is_sanitized(monkeypatch, caplog):
    def fail(self):
        raise RuntimeError("private-key-marker")
    with TestClient(secure_app()) as client:
        monkeypatch.setattr(KeyService, "public_response", fail)
        response = client.get(PATH)
        assert response.status_code == 503
        assert response.json() == {"error": {"code": "SERVICE_UNAVAILABLE", "message": "public key is unavailable"}}
        assert "private-key-marker" not in response.text + caplog.text


def test_exceptional_shutdown_releases_keys_and_storage():
    app = secure_app()
    with pytest.raises(RuntimeError, match="exit test"):
        with TestClient(app):
            keys, database = app.state.keys, app.state.database
            raise RuntimeError("exit test")
    assert database.closed and keys.closed
    with pytest.raises(MlKemError):
        keys.decapsulate(b"x" * 1088)
    assert app.state.keys is None
