"""Baseline canonical ingestion; no secure processing or plaintext fallback."""

from json import JSONDecodeError
import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from cloud_service.config import SecurityMode
from cloud_service.storage.database import StorageError
from cloud_service.validation import MeasurementValidationError, validate_measurement

router = APIRouter()
logger = logging.getLogger("cloud_service")


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@router.post("/api/v1/baseline/measurements")
async def baseline_measurement(request: Request) -> JSONResponse:
    # A future secure runtime must never activate baseline delivery implicitly.
    if request.app.state.config.security_mode != SecurityMode.CLASSICAL:
        return _error(503, "SERVICE_UNAVAILABLE", "baseline service is unavailable")
    repository = request.app.state.repository
    if not request.app.state.running or repository is None:
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")

    # Bound diagnostic text and use repr formatting to escape control characters.
    request_id = request.headers.get("X-Request-ID")
    correlation = None if request_id is None else request_id[:256]
    try:
        payload = await request.json()
    except (JSONDecodeError, UnicodeDecodeError):
        logger.info("baseline_invalid_json request_id=%r", correlation)
        return _error(400, "INVALID_JSON", "invalid JSON body")
    try:
        measurement = validate_measurement(payload)
    except MeasurementValidationError:
        logger.info("measurement_validation_failed request_id=%r", correlation)
        return _error(422, "INVALID_MEASUREMENT", "measurement validation failed")

    try:
        result = await run_in_threadpool(repository.save_idempotent, measurement)
    except StorageError:
        logger.warning("storage_failed request_id=%r", correlation)
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    except Exception:
        logger.error("baseline_internal_error request_id=%r", correlation)
        return _error(500, "INTERNAL_ERROR", "internal error")

    status = "accepted" if result.created else "already_accepted"
    logger.info("measurement_%s request_id=%r record_id=%s", status, correlation, result.measurement.record_id)
    return JSONResponse(status_code=202, content={"status": status, "record_id": result.measurement.record_id})
