"""POST /api/v1/secure/measurements.

An ordinary transport retry resends the same SecureEnvelope. HTTP 409
SESSION_INVALID or SESSION_EXPIRED invalidates the local session, establishes
one replacement, rebuilds the envelope for the same request ID, and retries
that logical request once. This client does not call the baseline endpoint.
"""

from __future__ import annotations

import asyncio
import http.client
import json
import logging
import math
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, replace
from collections.abc import Callable
from typing import Protocol
from urllib.parse import urljoin, urlparse

from edge_gateway.crypto.aad import AadError
from edge_gateway.crypto.encoding import EncodingError, decode_binary, encode_binary
from edge_gateway.crypto.envelope import SecureEnvelope, build_secure_envelope
from edge_gateway.crypto.failure import CryptoFailureInjector, corrupt_ciphertext_copy
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.plaintext import PlaintextError
from edge_gateway.crypto.security_log import log_security
from edge_gateway.crypto.session import SecureSession, SessionEstablishmentError
from edge_gateway.crypto.symmetric import AeadError
from edge_gateway.transport import CloudDeliveryError

logger = logging.getLogger(__name__)

_PATH = "api/v1/secure/measurements"
_MAX_BODY_BYTES = 16 * 1024
_RETRYABLE_STATUS = frozenset({500, 502, 503, 504})
_SESSION_CODES = frozenset({"SESSION_INVALID", "SESSION_EXPIRED"})
_ACCEPTED_STATUS = frozenset({"accepted", "already_accepted"})


class SecureTransportError(CloudDeliveryError):
    """The secure measurement was not accepted."""

    def __init__(self, message: str, *, retryable: bool, code: str | None = None) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.code = code


class _RetryableTransport(Exception):
    """One delivery attempt failed and the same envelope may be resent."""


class _SessionRecovery(Exception):
    """The Cloud rejected the session and one replacement may be tried."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class _RejectRedirect(urllib.request.HTTPRedirectHandler):
    """The configured Cloud URL is the only accepted measurement endpoint."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        log_security("secure_delivery_rejected", logging.WARNING, reason="redirect")
        raise SecureTransportError(
            "Cloud secure measurement endpoint redirected.",
            retryable=False,
        )


class _Sessions(Protocol):
    async def get_or_establish(self) -> SecureSession:
        """Return the active session, or establish one."""

    def invalidate(self) -> None:
        """Drop the current session and wipe its key."""


@dataclass(frozen=True, slots=True)
class SecureAcceptance:
    """Cloud accepted the logical measurement."""

    status: str
    record_id: str


@dataclass(frozen=True, slots=True)
class _Measurement:
    device_id: str
    temperature_c: float
    humidity_pct: float
    measured_at: str
    sequence_number: int
    received_at: str


class SecureTransport:
    """Send one canonical measurement as a SecureEnvelope."""

    def __init__(
        self,
        sessions: _Sessions,
        *,
        cloud_url: str,
        timeout_seconds: float,
        max_retries: int,
        injector: CryptoFailureInjector | None = None,
        metrics: PqcMetrics | None = None,
        sleep: Callable[[float], None] = time.sleep,
        before_attempt: Callable[[str], None] | None = None,
    ) -> None:
        if isinstance(max_retries, bool) or not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("max_retries must be a non-negative integer.")
        if (
            isinstance(timeout_seconds, bool)
            or not isinstance(timeout_seconds, (int, float))
            or not math.isfinite(timeout_seconds)
            or timeout_seconds <= 0
        ):
            raise ValueError("timeout_seconds must be greater than zero.")
        self._sessions = sessions
        self._endpoint = _endpoint(cloud_url)
        self._timeout_seconds = float(timeout_seconds)
        self._max_retries = max_retries
        self._injector = injector or CryptoFailureInjector.disabled()
        session_metrics = getattr(sessions, "metrics", None)
        self._metrics = metrics or (
            session_metrics if isinstance(session_metrics, PqcMetrics) else PqcMetrics()
        )
        self._before_attempt = before_attempt
        self._sleep = sleep
        self._opener = urllib.request.build_opener(_RejectRedirect)
        self._closed = False

    def shutdown(self) -> None:
        """Stop secure work, close the HTTP client, then clear the session.

        Gateway design section 53 orders the client close before the session
        is destroyed. A second call does nothing. No key material is logged.
        """
        if self._closed:
            return
        self._closed = True
        opener = self._opener
        self._opener = None
        if opener is not None:
            opener.close()
        close = getattr(self._sessions, "close", None)
        if close is not None:
            close()

    @property
    def metrics(self) -> PqcMetrics:
        """Return the process registry used by this secure transport."""
        return self._metrics

    async def send(
        self,
        *,
        request_id: str,
        device_id: str,
        temperature_c: float,
        humidity_pct: float,
        measured_at: str,
        sequence_number: int,
        received_at: str,
    ) -> SecureAcceptance:
        """Encrypt and deliver one measurement. Does not call the baseline API."""
        if self._closed:
            log_security(
                "secure_delivery_rejected",
                logging.WARNING,
                request_id=request_id,
                reason="closed",
            )
            raise SecureTransportError("Secure transport is closed.", retryable=False)
        measurement = _Measurement(
            device_id=device_id,
            temperature_c=temperature_c,
            humidity_pct=humidity_pct,
            measured_at=measured_at,
            sequence_number=sequence_number,
            received_at=received_at,
        )
        phase = "steady" if self._session_is_active() else "first"
        started = time.perf_counter()
        session = await self._open_session(request_id)
        log_security(
            "secure_delivery_started",
            request_id=request_id,
            gateway_id=session.gateway_id,
            session_id=session.session_id,
        )
        envelope = self._seal(session, request_id, measurement)
        try:
            acceptance = await asyncio.to_thread(self._deliver, envelope)
        except _SessionRecovery as recovery:
            acceptance = await self._recover(measurement, request_id, recovery.code)
        self._metrics.record_secure_message(phase, time.perf_counter() - started)
        return acceptance

    def _session_is_active(self) -> bool:
        for metrics in (self._metrics, getattr(self._sessions, "metrics", None)):
            if getattr(metrics, "active_session", 0):
                return True
        return False

    async def _open_session(self, request_id: str) -> SecureSession:
        try:
            return await self._sessions.get_or_establish()
        except SessionEstablishmentError as exc:
            log_security(
                "secure_delivery_rejected",
                logging.WARNING,
                request_id=request_id,
                reason="session_unavailable",
            )
            raise SecureTransportError(
                "Cloud secure session is unavailable.",
                retryable=exc.retryable,
            ) from exc

    async def _recover(
        self,
        measurement: _Measurement,
        request_id: str,
        code: str,
    ) -> SecureAcceptance:
        log_security(
            "session_reestablishment_started",
            logging.WARNING,
            request_id=request_id,
            reason=code,
        )
        self._sessions.invalidate()
        try:
            session = await self._sessions.get_or_establish()
        except SessionEstablishmentError as exc:
            self._metrics.record_reestablishment("failure")
            log_security(
                "session_reestablishment_failed",
                logging.WARNING,
                request_id=request_id,
                reason="session_unavailable",
            )
            raise SecureTransportError(
                "Cloud secure session recovery failed.",
                retryable=exc.retryable,
                code=code,
            ) from exc
        self._metrics.record_reestablishment("success")
        log_security(
            "session_reestablishment_succeeded",
            request_id=request_id,
            gateway_id=session.gateway_id,
            session_id=session.session_id,
            result="success",
        )
        envelope = self._seal(session, request_id, measurement)
        try:
            return await asyncio.to_thread(
                self._post,
                _dump(envelope),
                envelope.request_id,
                envelope.session_id,
            )
        except _SessionRecovery as exc:
            log_security(
                "secure_delivery_rejected",
                logging.WARNING,
                request_id=request_id,
                session_id=envelope.session_id,
                gateway_id=envelope.gateway_id,
                reason="session_rejected",
            )
            raise SecureTransportError(
                "Cloud secure session was rejected.",
                retryable=False,
                code=exc.code,
            ) from exc
        except _RetryableTransport as exc:
            log_security(
                "secure_delivery_rejected",
                logging.WARNING,
                request_id=request_id,
                session_id=envelope.session_id,
                gateway_id=envelope.gateway_id,
                reason="transport",
            )
            raise SecureTransportError(
                "Cloud secure measurement request failed.",
                retryable=True,
                code=code,
            ) from exc

    def _seal(
        self,
        session: SecureSession,
        request_id: str,
        measurement: _Measurement,
    ) -> SecureEnvelope:
        try:
            envelope = build_secure_envelope(
                key=bytes(session.session_key),
                session_id=session.session_id,
                request_id=request_id,
                gateway_id=session.gateway_id,
                device_id=measurement.device_id,
                temperature_c=measurement.temperature_c,
                humidity_pct=measurement.humidity_pct,
                measured_at=measurement.measured_at,
                sequence_number=measurement.sequence_number,
                received_at=measurement.received_at,
            )
            log_security(
                "encryption_succeeded",
                request_id=request_id,
                gateway_id=session.gateway_id,
                session_id=session.session_id,
                result="success",
            )
            if self._injector.corrupt_ciphertext():
                self._metrics.record_injected("corrupt_ciphertext")
                logger.warning(
                    "event=corrupt_ciphertext_injected component=edge_gateway request_id=%s",
                    request_id,
                )
                mutated = corrupt_ciphertext_copy(decode_binary(envelope.ciphertext))
                envelope = replace(envelope, ciphertext=encode_binary(mutated))
            return envelope
        except (AadError, PlaintextError, AeadError, EncodingError) as exc:
            self._metrics.record_encryption_failure()
            log_security(
                "encryption_failed",
                logging.WARNING,
                request_id=request_id,
                gateway_id=session.gateway_id,
                session_id=session.session_id,
                reason="seal",
            )
            raise SecureTransportError(
                "Cloud secure measurement could not be sealed.",
                retryable=False,
            ) from exc

    def _deliver(self, envelope: SecureEnvelope) -> SecureAcceptance:
        body = _dump(envelope)
        failure: _RetryableTransport | None = None
        for attempt in range(self._max_retries + 1):
            try:
                return self._post(body, envelope.request_id, envelope.session_id)
            except _RetryableTransport as exc:
                failure = exc
                if attempt < self._max_retries:
                    # The frozen Gateway policy waits 1s before retry two and
                    # 2s before retry three. The body remains byte-identical.
                    self._sleep(2.0**attempt)
        log_security(
            "secure_delivery_rejected",
            logging.WARNING,
            request_id=envelope.request_id,
            gateway_id=envelope.gateway_id,
            session_id=envelope.session_id,
            reason="transport",
        )
        raise SecureTransportError(
            "Cloud secure measurement request failed.",
            retryable=True,
        ) from failure

    def _post(self, body: bytes, request_id: str, session_id: str) -> SecureAcceptance:
        request = urllib.request.Request(
            self._endpoint,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Request-ID": request_id,
            },
        )
        try:
            if self._before_attempt is not None:
                self._before_attempt(request_id)
            with self._opener.open(request, timeout=self._timeout_seconds) as response:
                payload = response.read(_MAX_BODY_BYTES + 1)
                status = response.status
        except SecureTransportError:
            raise
        except TimeoutError as exc:
            raise _RetryableTransport("timeout") from exc
        except urllib.error.HTTPError as exc:
            return self._raise_http(exc, request_id, session_id)
        except urllib.error.URLError as exc:
            raise _RetryableTransport("connection") from exc
        except http.client.HTTPException as exc:
            # A Cloud response may be lost after persistence.  In particular,
            # an incomplete HTTP body must be retried using this exact wire
            # envelope, not re-encrypted.
            raise _RetryableTransport("incomplete response") from exc
        if status != 202:
            log_security(
                "secure_delivery_rejected",
                logging.WARNING,
                request_id=request_id,
                session_id=session_id,
                reason="rejected",
            )
            raise SecureTransportError(
                "Cloud secure measurement was not accepted.",
                retryable=False,
            )
        if not payload:
            # Some HTTP stacks surface a deliberately truncated 202 body as
            # empty bytes instead of an IncompleteRead.  The accepted response
            # schema is non-empty JSON, so retry the same envelope.
            raise _RetryableTransport("incomplete response")
        return _parse_acceptance(payload)

    def _raise_http(self, exc: urllib.error.HTTPError, request_id: str, session_id: str) -> SecureAcceptance:
        raw = exc.read(_MAX_BODY_BYTES + 1)
        code = _error_code(raw)
        if exc.code in _RETRYABLE_STATUS:
            raise _RetryableTransport(f"HTTP {exc.code}") from exc
        if exc.code == 409 and code in _SESSION_CODES:
            raise _SessionRecovery(code) from exc
        log_security(
            "secure_delivery_rejected",
            logging.WARNING,
            request_id=request_id,
            session_id=session_id,
            reason="rejected",
        )
        raise SecureTransportError(
            "Cloud secure measurement was rejected.",
            retryable=False,
            code=code,
        ) from exc


def _dump(envelope: SecureEnvelope) -> bytes:
    return json.dumps(envelope.as_dict(), separators=(",", ":")).encode("utf-8")


def _parse_acceptance(body: bytes) -> SecureAcceptance:
    if len(body) > _MAX_BODY_BYTES:
        raise SecureTransportError(
            "Cloud secure measurement response exceeds 16 KiB.",
            retryable=False,
        )
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise SecureTransportError(
            "Cloud secure measurement response is not JSON.",
            retryable=False,
        ) from exc
    if not isinstance(payload, dict):
        raise SecureTransportError(
            "Cloud secure measurement response must be a JSON object.",
            retryable=False,
        )
    status = payload.get("status")
    record_id = payload.get("record_id")
    if status not in _ACCEPTED_STATUS:
        raise SecureTransportError(
            "Cloud secure measurement response status is not accepted.",
            retryable=False,
        )
    if not isinstance(record_id, str) or record_id == "" or record_id != record_id.strip():
        raise SecureTransportError(
            "Cloud secure measurement response record_id is missing.",
            retryable=False,
        )
    return SecureAcceptance(status=status, record_id=record_id)


def _error_code(body: bytes) -> str | None:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    error = payload.get("error")
    if not isinstance(error, dict):
        return None
    code = error.get("code")
    if not isinstance(code, str) or code == "" or code != code.strip():
        return None
    return code


def _endpoint(cloud_url: str) -> str:
    if not isinstance(cloud_url, str):
        raise ValueError("cloud_url must be an HTTP or HTTPS URL.")
    parsed = urlparse(cloud_url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc == "":
        raise ValueError("cloud_url must be an HTTP or HTTPS URL.")
    return urljoin(cloud_url.rstrip("/") + "/", _PATH)
