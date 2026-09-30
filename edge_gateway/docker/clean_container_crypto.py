"""Start Cloud and deliver one secure measurement from a clean install.

The secure measurement receiver is mounted only on this process. It is not a
Cloud production route. The script prints one success line and does not print
keys or shared secrets.
"""

from __future__ import annotations

import asyncio
import json
import tempfile
import threading
import time
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from cloud_service.app import create_app
from cloud_service.config import load_config
from cloud_service.crypto.aad import AadError
from cloud_service.crypto.aad import build_aad as cloud_build_aad
from cloud_service.crypto.session import SessionAccessError
from cloud_service.crypto.symmetric import AeadError as CloudAeadError
from cloud_service.crypto.symmetric import decrypt as cloud_decrypt
from cloud_service.validation import MeasurementValidationError, validate_measurement
from edge_gateway.crypto.encoding import EncodingError, decode_binary
from edge_gateway.crypto.secure_transport import SecureTransport
from edge_gateway.crypto.session import SessionManager


_ENVELOPE_FIELDS = (
    "protocol_version",
    "gateway_id",
    "session_id",
    "request_id",
    "nonce",
    "ciphertext",
)
_MEASUREMENT = {
    "device_id": "sensor-001",
    "temperature_c": 22.5,
    "humidity_pct": 44.0,
    "measured_at": "2026-09-21T13:45:31Z",
    "sequence_number": 1,
    "received_at": "2026-09-21T13:45:31.218Z",
}


def _install(app: FastAPI, counts: dict[str, int]) -> None:
    """Mount the test-only receiver. Production routers stay unchanged."""

    @app.middleware("http")
    async def count_posts(request: Request, call_next):
        response = await call_next(request)
        if request.method == "POST" and request.url.path == "/api/v1/crypto/sessions":
            if response.status_code == 200:
                counts["handshakes"] += 1
        if request.method == "POST" and request.url.path == "/api/v1/baseline/measurements":
            counts["baseline"] += 1
        return response

    @app.post("/api/v1/secure/measurements")
    async def secure_measurements(request: Request) -> JSONResponse:
        try:
            payload = json.loads(await request.body())
        except (json.JSONDecodeError, UnicodeError):
            return _rejected()
        if not isinstance(payload, dict) or set(payload) != set(_ENVELOPE_FIELDS):
            return _rejected()
        if any(not isinstance(payload[name], str) or payload[name] == "" for name in _ENVELOPE_FIELDS):
            return _rejected()
        if payload["protocol_version"] != "1":
            return _rejected()
        try:
            session = app.state.sessions.get(payload["session_id"], payload["gateway_id"])
            associated = cloud_build_aad(
                protocol_version=payload["protocol_version"],
                gateway_id=payload["gateway_id"],
                session_id=payload["session_id"],
                request_id=payload["request_id"],
            )
            plaintext = cloud_decrypt(
                session.session_key,
                decode_binary(payload["nonce"]),
                decode_binary(payload["ciphertext"]),
                associated,
            )
            measurement = validate_measurement(
                json.loads(plaintext),
                expected_gateway_id=payload["gateway_id"],
            )
        except (SessionAccessError, AadError, EncodingError, CloudAeadError, MeasurementValidationError, json.JSONDecodeError):
            return _rejected()
        saved = app.state.repository.save_idempotent(measurement)
        return JSONResponse(
            status_code=202,
            content={"status": "accepted", "record_id": saved.measurement.record_id},
        )


def _rejected() -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": {"code": "SECURE_MESSAGE_REJECTED", "message": "secure message rejected"}},
    )


def _serve(app: FastAPI) -> tuple[uvicorn.Server, threading.Thread, str]:
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_level="warning", access_log=False)
    )
    thread = threading.Thread(target=server.run, name="clean-container-cloud", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive():
            raise RuntimeError("Cloud exited before it accepted connections")
        if time.monotonic() > deadline:
            server.should_exit = True
            raise RuntimeError("Cloud did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        raise RuntimeError("Cloud has no socket")
    return server, thread, f"http://127.0.0.1:{sockets[0].getsockname()[1]}"


def main() -> None:
    directory = Path(tempfile.mkdtemp(prefix="clean-container-"))
    database = directory / "measurements.db"
    app = create_app(
        load_config(
            {
                "DATABASE_URL": f"sqlite:///{database}",
                "SECURITY_MODE": "mlkem",
                "LOG_LEVEL": "WARNING",
            }
        )
    )
    counts = {"handshakes": 0, "baseline": 0}
    _install(app, counts)
    server, thread, base_url = _serve(app)
    sessions = SessionManager("gateway-001", base_url, 5.0)
    transport = SecureTransport(
        sessions,
        cloud_url=base_url,
        timeout_seconds=5.0,
        max_retries=0,
        sleep=lambda _delay: None,
    )
    try:
        accepted = asyncio.run(
            transport.send(
                request_id="req-clean-container",
                device_id=str(_MEASUREMENT["device_id"]),
                temperature_c=float(_MEASUREMENT["temperature_c"]),
                humidity_pct=float(_MEASUREMENT["humidity_pct"]),
                measured_at=str(_MEASUREMENT["measured_at"]),
                sequence_number=int(_MEASUREMENT["sequence_number"]),
                received_at=str(_MEASUREMENT["received_at"]),
            )
        )
        stored = app.state.repository.find_by_device_sequence(
            str(_MEASUREMENT["device_id"]),
            int(_MEASUREMENT["sequence_number"]),
        )
        values_match = (
            stored is not None
            and stored.temperature_c == _MEASUREMENT["temperature_c"]
            and stored.humidity_pct == _MEASUREMENT["humidity_pct"]
            and stored.sequence_number == _MEASUREMENT["sequence_number"]
            and stored.device_id == _MEASUREMENT["device_id"]
        )
        if (
            accepted.status != "accepted"
            or not accepted.record_id
            or not values_match
            or counts["handshakes"] != 1
            or counts["baseline"] != 0
            or len(app.state.repository.list()) != 1
        ):
            raise SystemExit("clean container crypto check failed")
        print("clean-container-ok")
    finally:
        transport.shutdown()
        server.should_exit = True
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
