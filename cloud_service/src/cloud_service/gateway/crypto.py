"""Public-key distribution for the Cloud secure-ingestion protocol."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from cloud_service.config import FailureMode, SecurityMode

router = APIRouter()
logger = logging.getLogger("cloud_service")


@router.get("/api/v1/crypto/public-key")
async def public_key(request: Request) -> JSONResponse:
    keys = request.app.state.keys
    if (request.app.state.config.security_mode != SecurityMode.MLKEM
            or not request.app.state.running or keys is None or keys.closed):
        return _unavailable()
    failure = request.app.state.failure_injector.select(
        (FailureMode.SERVICE_UNAVAILABLE, FailureMode.PUBLIC_KEY_UNAVAILABLE)
    )
    if failure.apply(FailureMode.SERVICE_UNAVAILABLE):
        return _unavailable()
    if failure.apply(FailureMode.PUBLIC_KEY_UNAVAILABLE):
        return _unavailable()
    try:
        payload = keys.public_response()
    except Exception:
        logger.error("event=public_key_unavailable component=cloud_service")
        return _unavailable()
    logger.info("event=public_key_requested component=cloud_service key_id=%s", keys.key_id)
    return JSONResponse(payload, headers={"Cache-Control": "no-store"})


def _unavailable() -> JSONResponse:
    return JSONResponse(status_code=503, content={
        "error": {"code": "SERVICE_UNAVAILABLE", "message": "public key is unavailable"},
    })
