"""Bounded measurement queries for verification and demonstration."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from cloud_service.storage.database import StorageError

router = APIRouter()
logger = logging.getLogger("cloud_service")
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@router.get("/api/v1/measurements")
async def list_measurements(request: Request, limit: str = str(DEFAULT_LIMIT), device_id: str | None = None) -> JSONResponse:
    # Bound the text before integer conversion, including attacker-sized values.
    if not (limit.isascii() and limit.isdecimal()) or len(limit) > 4 or not 1 <= int(limit) <= MAX_LIMIT:
        return _error(422, "INVALID_QUERY", "limit must be an integer between 1 and 1000")
    repository = request.app.state.repository
    if not request.app.state.running or repository is None:
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    try:
        records = await run_in_threadpool(repository.list, int(limit), device_id=device_id)
        return JSONResponse(content={"items": [record.to_dict() for record in records]})
    except StorageError:
        logger.warning(
            "event=measurement_query_storage_failed component=cloud_service device_id=%r",
            None if device_id is None else device_id[:256],
        )
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    except Exception:
        logger.error(
            "event=measurement_query_internal_error component=cloud_service device_id=%r",
            None if device_id is None else device_id[:256],
        )
        return _error(500, "INTERNAL_ERROR", "internal error")


@router.get("/api/v1/measurements/{record_id}")
async def get_measurement(request: Request, record_id: str) -> JSONResponse:
    repository = request.app.state.repository
    if not request.app.state.running or repository is None:
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    try:
        record = await run_in_threadpool(repository.get, record_id)
        if record is None:
            return _error(404, "MEASUREMENT_NOT_FOUND", "measurement not found")
        return JSONResponse(content=record.to_dict())
    except StorageError:
        logger.warning("event=measurement_query_storage_failed component=cloud_service record_id=%r", record_id[:256])
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    except Exception:
        logger.error("event=measurement_query_internal_error component=cloud_service record_id=%r", record_id[:256])
        return _error(500, "INTERNAL_ERROR", "internal error")
