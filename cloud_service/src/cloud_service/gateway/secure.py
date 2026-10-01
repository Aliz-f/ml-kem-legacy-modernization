"""Secure-only ingestion; all validation/authentication precedes storage."""

import asyncio
import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
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


class _DroppedResponse(Response):
    """Start an accepted response, then let the server close it unfinished.

    The deliberately incomplete response represents a lost acknowledgement:
    Uvicorn closes an ASGI response that starts but never completes, and the
    Gateway therefore receives a transport error rather than an HTTP result.
    """

    def __init__(self) -> None:
        # A non-zero length makes an empty body unambiguously incomplete to an
        # HTTP client.  Do not send a body event.
        super().__init__(status_code=202, headers={"Content-Length": "1"})

    async def __call__(self, scope, receive, send) -> None:
        await send({"type": "http.response.start", "status": self.status_code, "headers": self.raw_headers})


def _error(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


class _NoMetrics:
    """Compatibility no-op for direct internal test-harness calls."""

    def increment(self, _name: str, /, **_labels: str) -> None:
        return None


def _ingest(body: bytes, sessions, repository, failure, metrics=None) -> JSONResponse:
    if metrics is None:
        metrics = _NoMetrics()
    try:
        validated = validate_envelope(body)
    except EnvelopeValidationError as exc:
        logger.warning("event=secure_envelope_rejected component=cloud_service code=%s", exc.code)
        if exc.code == "UNSUPPORTED_PROTOCOL_VERSION":
            return _error(400, exc.code, "unsupported protocol version")
        return _error(400, exc.code, "secure message could not be processed")
    envelope = validated.envelope
    logger.info(
        "event=secure_measurement_received component=cloud_service request_id=%r gateway_id=%r session_id=%r",
        envelope.request_id[:256], envelope.gateway_id[:256], envelope.session_id[:256],
    )
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
        metrics.increment("cloud_authenticated_messages_total")
        logger.info(
            "event=decryption_succeeded component=cloud_service request_id=%r gateway_id=%r",
            envelope.request_id[:256], envelope.gateway_id[:256],
        )
        try:
            measurement = validate_measurement(parse_json(plaintext), expected_gateway_id=envelope.gateway_id)
        except (ValueError, MeasurementValidationError, RecursionError):
            logger.info(
                "event=measurement_validation_failed component=cloud_service request_id=%r gateway_id=%r",
                envelope.request_id[:256], envelope.gateway_id[:256],
            )
            return _error(422, "INVALID_MEASUREMENT", "measurement validation failed")
        if failure.apply(FailureMode.STORAGE_FAILURE):
            raise StorageError("injected storage failure")
        result = repository.save_idempotent(measurement)
    except SessionAccessError:
        raise  # Existing frozen HTTP handler handles 409/ownership errors.
    except AeadError:
        metrics.increment("cloud_decryption_failures_total")
        logger.warning(
            "event=decryption_failed component=cloud_service request_id=%r gateway_id=%r",
            envelope.request_id[:256], envelope.gateway_id[:256],
        )
        return _error(400, "SECURE_MESSAGE_REJECTED", "secure message could not be processed")
    except StorageError:
        metrics.increment("cloud_storage_failures_total")
        logger.warning("event=storage_failed component=cloud_service request_id=%r gateway_id=%r",
                       envelope.request_id[:256], envelope.gateway_id[:256])
        return _error(503, "STORAGE_UNAVAILABLE", "storage is unavailable")
    except Exception:
        logger.error("event=secure_internal_error component=cloud_service request_id=%r gateway_id=%r",
                     envelope.request_id[:256], envelope.gateway_id[:256])
        return _error(500, "INTERNAL_ERROR", "internal error")
    status = "accepted" if result.created else "already_accepted"
    metric = "cloud_measurements_stored_total" if result.created else "cloud_duplicate_measurements_total"
    metrics.increment(metric)
    event = "measurement_stored" if result.created else "measurement_duplicate"
    logger.info(
        "event=%s component=cloud_service request_id=%r gateway_id=%r device_id=%r sequence_number=%s status=%s record_id=%s",
        event, envelope.request_id[:256], envelope.gateway_id[:256], measurement.device_id[:256],
        measurement.sequence_number, status, result.measurement.record_id,
    )
    if failure.apply(FailureMode.DROP_RESPONSE):
        # The record is committed, but the Gateway receives no completed HTTP
        # response.  Its ordinary retry must retain the already-built envelope
        # and therefore reaches the repository's idempotency path.
        return _DroppedResponse()
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
        logger.warning("event=secure_envelope_rejected component=cloud_service code=INVALID_CONTENT_TYPE")
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
        logger.warning("event=secure_envelope_rejected component=cloud_service code=INVALID_ENVELOPE_BODY")
        return _error(400, "SECURE_MESSAGE_REJECTED", "secure message could not be processed")
    return await run_in_threadpool(_ingest, bytes(body), sessions, repository, failure, request.app.state.metrics)
