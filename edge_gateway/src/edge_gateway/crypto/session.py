"""In-memory Gateway session for protocol version 1.

The session key stays in process memory. Establishment uses the public-key
client, ML-KEM encapsulation, and HKDF, then POST /api/v1/crypto/sessions.
This module does not send measurements or perform AES-GCM.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum

from edge_gateway.crypto.failure import CryptoFailureInjector
from edge_gateway.crypto.kdf import KdfError, derive_session_key
from edge_gateway.crypto.mlkem import MlKemError, encapsulate
from edge_gateway.crypto.public_key import PublicKeyRejected
from edge_gateway.crypto.public_key_client import (
    PublicKeyTransportError,
    fetch_public_key,
)
from edge_gateway.crypto.session_client import (
    SessionRejected,
    SessionTransportError,
    post_session,
)

logger = logging.getLogger(__name__)

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
class SessionMetrics:
    """In-memory counters for Gateway session establishment.

    Exporting these counters is owned by the later Gateway observability work.
    Keeping the counter here ensures every failed handshake is recorded without
    attaching request or session identifiers as metric labels.
    """

    mlkem_handshake_failures_total: int = 0

    def record_establishment_failure(self) -> None:
        """Record one failed ML-KEM session-establishment attempt."""
        self.mlkem_handshake_failures_total += 1


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

    async def get_or_establish(self) -> SecureSession:
        """Return the active session, establishing one handshake if needed."""
        async with self._lock:
            self._apply_session_fault()
            current = self._usable_session()
            if current is not None:
                return current
            try:
                session = await asyncio.to_thread(self._establish)
            except SessionEstablishmentError:
                self._fail_current()
                raise
            self._session = session
            return session

    def invalidate(self) -> None:
        """Drop the current session and wipe its key."""
        if self._session is not None:
            self._session.clear(SessionState.EXPIRED)
            self._session = None

    def close(self) -> None:
        """Drop the current session and wipe its key."""
        if self._session is not None:
            self._session.clear(SessionState.CLOSED)
            self._session = None

    @property
    def metrics(self) -> SessionMetrics:
        """Expose aggregate, secret-free session-establishment metrics."""
        return self._metrics

    def _usable_session(self) -> SecureSession | None:
        session = self._session
        if session is None or session.state is not SessionState.ACTIVE:
            return None
        if session.expires_at <= self._clock():
            session.clear(SessionState.EXPIRED)
            self._session = None
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
            logger.warning("event=session_missing_injected")
            session.clear(SessionState.FAILED)
            self._session = None
            return
        if self._injector.session_expired():
            logger.warning("event=session_expired_injected")
            session.clear(SessionState.EXPIRED)
            self._session = None

    def _establish(self) -> SecureSession:
        """Run the handshake. The caller holds the establishment lock."""
        if self._injector.handshake_failure():
            logger.warning("event=mlkem_handshake_failed reason=injected")
            self._metrics.record_establishment_failure()
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
        try:
            cloud_key = fetch_public_key(self._cloud_url, self._timeout_seconds)
            ciphertext, shared_secret = encapsulate(cloud_key.public_key)
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
            )
        except (PublicKeyRejected, SessionRejected) as exc:
            self._fail_establishment(
                provisional,
                "session establishment rejected",
                retryable=False,
                cause=exc,
            )
        except (MlKemError, KdfError) as exc:
            self._fail_establishment(
                provisional,
                "ML-KEM session establishment failed",
                retryable=False,
                cause=exc,
            )
        except Exception as exc:
            self._fail_establishment(
                provisional,
                "unexpected session establishment failure",
                retryable=False,
                cause=exc,
            )
        provisional.session_id = response.session_id
        provisional.created_at = self._clock()
        provisional.expires_at = response.expires_at
        provisional.state = SessionState.ACTIVE
        return provisional

    def _fail_establishment(
        self,
        provisional: SecureSession,
        message: str,
        *,
        retryable: bool,
        cause: Exception,
    ) -> None:
        """Clear provisional key material and raise a classified failure."""
        provisional.clear(SessionState.FAILED)
        self._session = None
        self._metrics.record_establishment_failure()
        logger.warning(message)
        raise SessionEstablishmentError(message, retryable=retryable) from cause
