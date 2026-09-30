"""Validated session handshake; no secure-message processing."""

import base64
from json import JSONDecodeError
import logging
import re

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from cloud_service.config import SecurityMode
from cloud_service.crypto.kdf import derive_session_key
from cloud_service.crypto.session import SessionAccessError, SessionState

router = APIRouter()
logger = logging.getLogger("cloud_service")
_FIELDS = {"protocol_version", "gateway_id", "key_id", "encapsulation_ciphertext"}


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


async def session_access_error_handler(request: Request, exc: SessionAccessError) -> JSONResponse:
    return _error(exc.status_code, exc.code, str(exc))


def _decode_ciphertext(value: object) -> bytes:
    # 1088 raw bytes have 1451 unpadded or 1452 padded Base64URL characters.
    if not isinstance(value, str) or len(value) not in (1451, 1452):
        raise ValueError
    if re.fullmatch(r"[A-Za-z0-9_-]+=?", value) is None:
        raise ValueError
    decoded = base64.b64decode(value + "=" * (-len(value) % 4), altchars=b"-_", validate=True)
    if len(decoded) != 1088 or base64.urlsafe_b64encode(decoded).decode().rstrip("=") != value.rstrip("="):
        raise ValueError
    return decoded


def _establish(keys, manager, gateway_id: str, ciphertext: bytes) -> JSONResponse:
    session = None
    try:
        secret = keys.decapsulate(ciphertext)
        key = derive_session_key(secret)
        session = manager.create(gateway_id, keys.key_id, key)
        response = JSONResponse(session.response(), headers={"Cache-Control": "no-store"})
    except Exception:
        if session is not None:
            manager.invalidate(session.session_id, SessionState.FAILED)
        logger.warning("session_establishment_failed")
        return _error(503, "SERVICE_UNAVAILABLE", "session establishment unavailable")
    logger.info("session_established")
    return response


@router.post("/api/v1/crypto/sessions")
async def establish_session(request: Request) -> JSONResponse:
    keys, manager = request.app.state.keys, request.app.state.sessions
    if (request.app.state.config.security_mode != SecurityMode.MLKEM
            or not request.app.state.running or keys is None or keys.closed or manager is None):
        return _error(503, "SERVICE_UNAVAILABLE", "session establishment unavailable")
    try:
        payload = await request.json()
    except (JSONDecodeError, UnicodeDecodeError):
        return _error(400, "INVALID_SESSION_REQUEST", "invalid session request")
    if not isinstance(payload, dict) or set(payload) != _FIELDS:
        return _error(400, "INVALID_SESSION_REQUEST", "invalid session request")
    if payload["protocol_version"] != "1":
        return _error(400, "UNSUPPORTED_PROTOCOL_VERSION", "unsupported protocol version")
    gateway_id = payload["gateway_id"]
    if (not isinstance(gateway_id, str) or not gateway_id or gateway_id != gateway_id.strip()
            or payload["key_id"] != keys.key_id):
        return _error(400, "INVALID_SESSION_REQUEST", "invalid session request")
    try:
        ciphertext = _decode_ciphertext(payload["encapsulation_ciphertext"])
    except ValueError:
        return _error(400, "INVALID_SESSION_REQUEST", "invalid session request")
    return await run_in_threadpool(_establish, keys, manager, gateway_id, ciphertext)
