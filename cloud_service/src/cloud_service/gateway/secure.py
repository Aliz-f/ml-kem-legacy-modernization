"""Secure-only ingestion; all validation/authentication precedes storage."""

import asyncio
import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from starlette.requests import ClientDisconnect

from cloud_service.config import FailureMode, SecurityMode
from cloud_service.crypto.aad import build_aad
from cloud_service.crypto.envelope_validation import (
    MAX_ENVELOPE_BYTES, EnvelopeValidationError, parse_json, validate_envelope,
)
from cloud_service.crypto.session import SessionAccessError, SessionState
from cloud_service.crypto.symmetric import AeadError, decrypt
from cloud_service.storage.database import StorageError
from cloud_service.validation import MeasurementValidationError, validate_measurement

router = APIRouter()
logger = logging.getLogger("cloud_service")


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


def _ingest(body: bytes, sessions, repository, failure) -> JSONResponse:
    try:
        validated = validate_envelope(body)
    except EnvelopeValidationError as exc:
        if exc.code == "UNSUPPORTED_PROTOCOL_VERSION":
            return _error(400, exc.code, "unsupported protocol version")
        return _error(400, exc.code, "secure message could not be processed")
    envelope = validated.envelope
    try:
        # Manager enforces lookup -> ownership -> expiry, with no extension.
        session = sessions.get(envelope.session_id, envelope.gateway_id)
        if failure.apply(FailureMode.SESSION_NOT_FOUND):
            sessions.invalidate(envelope.session_id, SessionState.INVALIDATED)
            raise SessionAccessError(409, "SESSION_INVALID", "secure session is invalid")
        if failure.apply(FailureMode.SESSION_EXPIRED):
            sessions.invalidate(envelope.session_id, SessionState.EXPIRED)
            raise SessionAccessError(409, "SESSION_EXPIRED", "secure session has expired")
        aad = build_aad(protocol_version=envelope.protocol_version, gateway_id=envelope.gateway_id,
                        session_id=envelope.session_id, request_id=envelope.request_id)
        if failure.apply(FailureMode.DECRYPTION_FAILURE):
            raise AeadError("injected decryption failure")
        plaintext = decrypt(session.session_key, validated.nonce, validated.ciphertext, aad)
        try:
            measurement = validate_measurement(parse_json(plaintext), expected_gateway_id=envelope.gateway_id)
        except (ValueError, MeasurementValidationError, RecursionError):
            return _error(422, "INVALID_MEASUREMENT", "measurement validation failed")
        if failure.apply(FailureMode.STORAGE_FAILURE):
            raise StorageError("injected storage failure")
        result = repository.save_idempotent(measurement)
    except SessionAccessError:
        raise  # Existing frozen HTTP handler handles 409/ownership errors.
    except AeadError:
        return _error(400, "SECURE_MESSAGE_REJECTED", "secure message could not be processed")
    except StorageError:
        logger.warning("event=secure_storage_failed component=cloud_service request_id=%r gateway_id=%r",
                       envelope.request_id[:256], envelope.gateway_id[:256])
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    except Exception:
        logger.error("event=secure_internal_error component=cloud_service request_id=%r gateway_id=%r",
                     envelope.request_id[:256], envelope.gateway_id[:256])
        return _error(500, "INTERNAL_ERROR", "internal error")
    status = "accepted" if result.created else "already_accepted"
    logger.info("event=secure_measurement_accepted component=cloud_service request_id=%r gateway_id=%r device_id=%r sequence_number=%s status=%s record_id=%s",
                envelope.request_id[:256], envelope.gateway_id[:256], measurement.device_id[:256],
                measurement.sequence_number, status, result.measurement.record_id)
    if failure.apply(FailureMode.DROP_RESPONSE):
        # The record is committed, but the caller receives a retryable outcome.
        # A retransmission must retain its already-built envelope and reaches
        # the repository's idempotency path. Transport-level connection loss is
        # exercised by Member 5's real-network E2E suite.
        return _error(503, "SERVICE_UNAVAILABLE", "secure response is unavailable")
    return JSONResponse(status_code=202, content={"status": status, "record_id": result.measurement.record_id})


@router.post("/api/v1/secure/measurements")
async def secure_measurement(request: Request) -> JSONResponse:
    if request.app.state.config.security_mode != SecurityMode.MLKEM or not request.app.state.running:
        return _error(503, "SERVICE_UNAVAILABLE", "secure service is unavailable")
    sessions, repository = request.app.state.sessions, request.app.state.repository
    if sessions is None:
        return _error(503, "SERVICE_UNAVAILABLE", "secure service is unavailable")
    if repository is None:
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    injector = request.app.state.failure_injector
    failure = injector.select((
        FailureMode.SERVICE_UNAVAILABLE, FailureMode.PROCESSING_DELAY,
        FailureMode.SESSION_NOT_FOUND, FailureMode.SESSION_EXPIRED,
        FailureMode.DECRYPTION_FAILURE, FailureMode.STORAGE_FAILURE,
        FailureMode.DROP_RESPONSE,
    ))
    if failure.apply(FailureMode.SERVICE_UNAVAILABLE):
        return _error(503, "SERVICE_UNAVAILABLE", "secure service is unavailable")
    if failure.apply(FailureMode.PROCESSING_DELAY):
        await asyncio.sleep(injector.delay_seconds)
    if request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
        return _error(400, "SECURE_MESSAGE_REJECTED", "secure message could not be processed")
    body = bytearray()
    try:
        length = request.headers.get("content-length")
        if length is not None and (not length.isascii() or not length.isdecimal() or int(length) > MAX_ENVELOPE_BYTES):
            raise ValueError
        async for chunk in request.stream():
            if len(body) + len(chunk) > MAX_ENVELOPE_BYTES:
                raise ValueError
            body.extend(chunk)
    except (ValueError, ClientDisconnect):
        return _error(400, "SECURE_MESSAGE_REJECTED", "secure message could not be processed")
    return await run_in_threadpool(_ingest, bytes(body), sessions, repository, failure)
