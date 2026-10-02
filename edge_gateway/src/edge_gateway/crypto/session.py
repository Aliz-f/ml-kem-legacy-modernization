"""In-memory Gateway session for protocol version 1.

The session key stays in process memory. Establishment uses the public-key
client, ML-KEM encapsulation, and HKDF, then POST /api/v1/crypto/sessions.
This module does not send measurements or perform AES-GCM. Python does not
guarantee secure memory zeroization.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum

from edge_gateway.crypto.failure import CryptoFailureInjector
from edge_gateway.crypto.kdf import KdfError, derive_session_key
from edge_gateway.crypto.metrics import PqcMetrics as SessionMetrics
from edge_gateway.crypto.mlkem import MlKemError, encapsulate
from edge_gateway.crypto.public_key import PublicKeyRejected
from edge_gateway.crypto.public_key_client import (
    PublicKeyTransportError,
    fetch_public_key,
)
from edge_gateway.crypto.security_log import log_security
from edge_gateway.crypto.session_client import (
    SessionRejected,
    SessionTransportError,
    post_session,
)

Clock = Callable[[], datetime]


class SessionState(StrEnum):
    """Local lifecycle of one Gateway session."""

    ESTABLISHING = "establishing"
    ACTIVE = "active"
    EXPIRED = "expired"
    FAILED = "failed"
    CLOSED = "closed"


class SessionEstablishmentError(Exception):
    """The Gateway could not store an active session."""

    def __init__(self, message: str, *, retryable: bool) -> None:
        super().__init__(message)
        self.retryable = retryable


@dataclass(slots=True)
class SecureSession:
    """One Cloud session owned by this Gateway.

    ``session_key`` is a mutable buffer so ``clear`` can wipe it. ``repr``
    omits that buffer.
    """

    session_id: str
    gateway_id: str
    cloud_key_id: str
    created_at: datetime
    expires_at: datetime
    session_key: bytearray
    state: SessionState

    def __repr__(self) -> str:
        return (
            "SecureSession("
            f"session_id={self.session_id!r}, "
            f"gateway_id={self.gateway_id!r}, "
            f"cloud_key_id={self.cloud_key_id!r}, "
            f"state={self.state.value!r})"
        )

    def clear(self, state: SessionState) -> None:
        """Overwrite the session key and record why the session ended."""
        self.session_key[:] = b"\x00" * len(self.session_key)
        self.state = state


class SessionManager:
    """Hold at most one active session and establish it under one lock."""

    def __init__(
        self,
        gateway_id: str,
        cloud_url: str,
        timeout_seconds: float,
        *,
        clock: Clock | None = None,
        metrics: SessionMetrics | None = None,
        injector: CryptoFailureInjector | None = None,
    ) -> None:
        if not isinstance(gateway_id, str) or gateway_id == "" or gateway_id != gateway_id.strip():
            raise ValueError("gateway_id must be a non-empty string.")
        self._gateway_id = gateway_id
        self._cloud_url = cloud_url
        self._timeout_seconds = timeout_seconds
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._metrics = metrics or SessionMetrics()
        self._injector = injector or CryptoFailureInjector.disabled()
        self._lock = asyncio.Lock()
        self._session: SecureSession | None = None
        self._closed = False

    async def get_or_establish(self) -> SecureSession:
        """Return the active session, establishing one handshake if needed."""
        async with self._lock:
            if self._closed:
                raise SessionEstablishmentError(
                    "Gateway session manager is closed.",
                    retryable=False,
                )
            self._apply_session_fault()
            current = self._usable_session()
            if current is not None:
                log_security(
                    "session_reused",
                    session_id=current.session_id,
                    gateway_id=current.gateway_id,
                    result="reused",
                )
                return current
            try:
                session = await asyncio.to_thread(self._establish)
            except SessionEstablishmentError:
                self._fail_current()
                raise
            if self._closed:
                session.clear(SessionState.CLOSED)
                if self._session is session:
                    self._session = None
                self._metrics.set_active_session(False)
                raise SessionEstablishmentError(
                    "Gateway session manager is closed.",
                    retryable=False,
                )
            self._session = session
            self._metrics.set_active_session(True)
            return session

    def invalidate(self, session_id: str | None = None) -> None:
        """Drop the current session only when it is the rejected session.

        ``None`` retains the explicit local-management behavior used outside a
        recovery. A 409 recovery supplies the envelope's session ID so a
        delayed concurrent recovery cannot clear a replacement session.
        """
        session = self._session
        if session is None or (session_id is not None and session.session_id != session_id):
            return
        log_security(
            "session_invalidated",
            session_id=session.session_id,
            gateway_id=session.gateway_id,
            reason="invalidated",
            level=logging.WARNING,
        )
        session.clear(SessionState.EXPIRED)
        self._session = None
        self._metrics.set_active_session(False)

    def close(self) -> None:
        """Drop the current session and wipe its key.

        Later handshakes are refused. Python does not guarantee that every
        copy of the key is gone from process memory.
        """
        self._closed = True
        session = self._session
        if session is not None:
            log_security(
                "session_invalidated",
                session_id=session.session_id,
                gateway_id=session.gateway_id,
                reason="closed",
                level=logging.WARNING,
            )
            session.clear(SessionState.CLOSED)
            self._session = None
            self._metrics.set_active_session(False)

    @property
    def metrics(self) -> SessionMetrics:
        """Expose aggregate, secret-free session-establishment metrics."""
        return self._metrics

    def _usable_session(self) -> SecureSession | None:
        session = self._session
        if session is None or session.state is not SessionState.ACTIVE:
            return None
        if session.expires_at <= self._clock():
            log_security(
                "session_expired",
                session_id=session.session_id,
                gateway_id=session.gateway_id,
                reason="expired",
                level=logging.WARNING,
            )
            session.clear(SessionState.EXPIRED)
            self._session = None
            self._metrics.set_active_session(False)
            return None
        return session

    def _fail_current(self) -> None:
        if self._session is not None:
            self._session.clear(SessionState.FAILED)
            self._session = None

    def _apply_session_fault(self) -> None:
        session = self._session
        if session is None or session.state is not SessionState.ACTIVE:
            return
        if self._injector.session_missing():
            self._metrics.record_injected("session_missing")
            log_security(
                "session_invalidated",
                session_id=session.session_id,
                gateway_id=session.gateway_id,
                reason="missing",
                level=logging.WARNING,
            )
            session.clear(SessionState.FAILED)
            self._session = None
            self._metrics.set_active_session(False)
            return
        if self._injector.session_expired():
            self._metrics.record_injected("session_expired")
            log_security(
                "session_expired",
                session_id=session.session_id,
                gateway_id=session.gateway_id,
                reason="injected",
                level=logging.WARNING,
            )
            session.clear(SessionState.EXPIRED)
            self._session = None
            self._metrics.set_active_session(False)

    def _clear_replaced_session(self) -> None:
        """Wipe a session that is still held when a new handshake starts."""
        session = self._session
        if session is None:
            return
        log_security(
            "session_invalidated",
            session_id=session.session_id,
            gateway_id=session.gateway_id,
            reason="replaced",
            level=logging.WARNING,
        )
        session.clear(SessionState.FAILED)
        self._session = None
        self._metrics.set_active_session(False)

    def _establish(self) -> SecureSession:
        """Run the handshake. The caller holds the establishment lock."""
        started = time.perf_counter()
        self._clear_replaced_session()
        log_security("mlkem_handshake_started", gateway_id=self._gateway_id)
        if self._injector.handshake_failure():
            duration = time.perf_counter() - started
            self._metrics.record_injected("mlkem_handshake_failure")
            self._metrics.record_handshake_failure("injected", duration)
            log_security(
                "mlkem_handshake_failed",
                logging.WARNING,
                gateway_id=self._gateway_id,
                reason="injected",
                duration=duration,
            )
            raise SessionEstablishmentError("ML-KEM handshake failed.", retryable=False)
        provisional = SecureSession(
            session_id="",
            gateway_id=self._gateway_id,
            cloud_key_id="",
            created_at=self._clock(),
            expires_at=self._clock(),
            session_key=bytearray(),
            state=SessionState.ESTABLISHING,
        )
        self._session = provisional
        public_key_seconds: float | None = None
        encapsulation_seconds: float | None = None
        try:
            fetched = time.perf_counter()
            cloud_key = fetch_public_key(self._cloud_url, self._timeout_seconds)
            public_key_seconds = time.perf_counter() - fetched
            log_security(
                "mlkem_public_key_received",
                gateway_id=self._gateway_id,
                key_id=cloud_key.key_id,
            )
            encapsulated = time.perf_counter()
            ciphertext, shared_secret = encapsulate(cloud_key.public_key)
            encapsulation_seconds = time.perf_counter() - encapsulated
            session_key = bytearray(derive_session_key(shared_secret))
            provisional.session_key = session_key
            provisional.cloud_key_id = cloud_key.key_id
            response = post_session(
                self._cloud_url,
                self._timeout_seconds,
                gateway_id=self._gateway_id,
                key_id=cloud_key.key_id,
                encapsulation_ciphertext=ciphertext,
                now=self._clock(),
            )
        except (PublicKeyTransportError, SessionTransportError) as exc:
            self._fail_establishment(
                provisional,
                "session establishment failed",
                retryable=exc.retryable,
                cause=exc,
                reason="transport",
                started=started,
                public_key_seconds=public_key_seconds,
                encapsulation_seconds=encapsulation_seconds,
            )
        except (PublicKeyRejected, SessionRejected) as exc:
            self._fail_establishment(
                provisional,
                "session establishment rejected",
                retryable=False,
                cause=exc,
                reason="rejected",
                started=started,
                public_key_seconds=public_key_seconds,
                encapsulation_seconds=encapsulation_seconds,
            )
        except (MlKemError, KdfError) as exc:
            self._fail_establishment(
                provisional,
                "ML-KEM session establishment failed",
                retryable=False,
                cause=exc,
                reason="cryptographic",
                started=started,
                public_key_seconds=public_key_seconds,
                encapsulation_seconds=encapsulation_seconds,
            )
        except Exception as exc:
            self._fail_establishment(
                provisional,
                "unexpected session establishment failure",
                retryable=False,
                cause=exc,
                reason="unexpected",
                started=started,
                public_key_seconds=public_key_seconds,
                encapsulation_seconds=encapsulation_seconds,
            )
        duration = time.perf_counter() - started
        self._metrics.record_handshake_success(duration, public_key_seconds or 0.0, encapsulation_seconds or 0.0)
        provisional.session_id = response.session_id
        provisional.created_at = self._clock()
        provisional.expires_at = response.expires_at
        provisional.state = SessionState.ACTIVE
        log_security(
            "mlkem_handshake_succeeded",
            gateway_id=self._gateway_id,
            session_id=response.session_id,
            key_id=provisional.cloud_key_id,
            result="success",
            duration=duration,
        )
        log_security(
            "session_created",
            gateway_id=self._gateway_id,
            session_id=response.session_id,
            key_id=provisional.cloud_key_id,
            result="created",
        )
        return provisional

    def _fail_establishment(
        self,
        provisional: SecureSession,
        message: str,
        *,
        retryable: bool,
        cause: Exception,
        reason: str,
        started: float,
        public_key_seconds: float | None,
        encapsulation_seconds: float | None,
    ) -> None:
        """Clear provisional key material and raise a classified failure."""
        provisional.clear(SessionState.FAILED)
        self._session = None
        duration = time.perf_counter() - started
        self._metrics.record_handshake_failure(
            reason,
            duration,
            public_key_seconds,
            encapsulation_seconds,
        )
        log_security(
            "mlkem_handshake_failed",
            logging.WARNING,
            gateway_id=self._gateway_id,
            reason=reason,
            duration=duration,
        )
        raise SessionEstablishmentError(message, retryable=retryable) from cause
