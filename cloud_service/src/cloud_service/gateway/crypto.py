"""Public-key distribution only; sessions and secure ingestion follow later."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from cloud_service.config import SecurityMode

router = APIRouter()
logger = logging.getLogger("cloud_service")


@router.get("/api/v1/crypto/public-key")
async def public_key(request: Request) -> JSONResponse:
    keys = request.app.state.keys
    if (request.app.state.config.security_mode != SecurityMode.MLKEM
            or not request.app.state.running or keys is None or keys.closed):
        return _unavailable()
    try:
        payload = keys.public_response()
    except Exception:
        logger.error("public_key_unavailable")
        return _unavailable()
    logger.info("public_key_requested")
    return JSONResponse(payload, headers={"Cache-Control": "no-store"})


def _unavailable() -> JSONResponse:
    return JSONResponse(status_code=503, content={
        "error": {"code": "SERVICE_UNAVAILABLE", "message": "public key is unavailable"},
    })
