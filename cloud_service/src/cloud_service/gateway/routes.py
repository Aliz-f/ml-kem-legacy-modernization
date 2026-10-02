"""Baseline canonical ingestion; no secure processing or plaintext fallback."""

import asyncio
from json import JSONDecodeError
import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from cloud_service.config import FailureMode, SecurityMode
from cloud_service.storage.database import StorageError
from cloud_service.validation import MeasurementValidationError, validate_measurement

router = APIRouter()
logger = logging.getLogger("cloud_service")


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@router.post("/api/v1/baseline/measurements")
async def baseline_measurement(request: Request) -> JSONResponse:
    # Secure operation must never activate baseline delivery implicitly.
    if request.app.state.config.security_mode != SecurityMode.CLASSICAL:
        return _error(503, "SERVICE_UNAVAILABLE", "baseline service is unavailable")
    repository = request.app.state.repository
    if not request.app.state.running or repository is None:
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    injector = request.app.state.failure_injector
    failure = injector.select(
        (FailureMode.SERVICE_UNAVAILABLE, FailureMode.PROCESSING_DELAY, FailureMode.STORAGE_FAILURE)
    )
    if failure.apply(FailureMode.SERVICE_UNAVAILABLE):
        return _error(503, "SERVICE_UNAVAILABLE", "baseline service is unavailable")
    if failure.apply(FailureMode.PROCESSING_DELAY):
        await asyncio.sleep(injector.delay_seconds)

    # Bound diagnostic text and use repr formatting to escape control characters.
    request_id = request.headers.get("X-Request-ID")
    correlation = None if request_id is None else request_id[:256]
    try:
        payload = await request.json()
    except (JSONDecodeError, UnicodeDecodeError):
        logger.info("event=measurement_validation_failed component=cloud_service request_id=%r", correlation)
        return _error(400, "INVALID_JSON", "invalid JSON body")
    try:
        measurement = validate_measurement(payload)
    except MeasurementValidationError:
        logger.info("event=measurement_validation_failed component=cloud_service request_id=%r", correlation)
        return _error(422, "INVALID_MEASUREMENT", "measurement validation failed")

    try:
        if failure.apply(FailureMode.STORAGE_FAILURE):
            raise StorageError("injected storage failure")
        result = await run_in_threadpool(repository.save_idempotent, measurement)
    except StorageError:
        request.app.state.metrics.increment("cloud_storage_failures_total")
        logger.warning("event=storage_failed component=cloud_service request_id=%r", correlation)
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    except Exception:
        logger.error("event=baseline_internal_error component=cloud_service request_id=%r", correlation)
        return _error(500, "INTERNAL_ERROR", "internal error")

    status = "accepted" if result.created else "already_accepted"
    metric = "cloud_measurements_stored_total" if result.created else "cloud_duplicate_measurements_total"
    request.app.state.metrics.increment(metric)
    event = "measurement_stored" if result.created else "measurement_duplicate"
    logger.info(
        "event=%s component=cloud_service request_id=%r gateway_id=%r device_id=%r "
        "sequence_number=%s record_id=%s status=%s",
        event, correlation, measurement.gateway_id[:256], measurement.device_id[:256],
        measurement.sequence_number, result.measurement.record_id, status,
    )
    return JSONResponse(status_code=202, content={"status": status, "record_id": result.measurement.record_id})
