"""Process-local Cloud sessions; no persistence, counters or replay window."""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from threading import RLock
from uuid import uuid4


class SessionState(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    INVALIDATED = "invalidated"
    CLOSED = "closed"
    FAILED = "failed"


class SessionAccessError(Exception):
    """Frozen secure-access error; contains no identifiers or key material."""

    def __init__(self, status_code: int, code: str, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


@dataclass(frozen=True, slots=True)
class SecureSession:
    session_id: str
    gateway_id: str
    cloud_key_id: str
    created_at: datetime
    expires_at: datetime
    session_key: bytearray = field(repr=False, compare=False)
    state: SessionState = SessionState.ACTIVE

    def clear(self, state: SessionState) -> None:
        self.session_key[:] = b"\x00" * len(self.session_key)
        object.__setattr__(self, "state", state)

    def response(self) -> dict[str, str]:
        """Explicit public metadata only; never serialize the session object."""
        return {
            "protocol_version": "1", "session_id": self.session_id,
            "status": "established",
            "expires_at": self.expires_at.isoformat().replace("+00:00", "Z"),
        }


class SessionManager:
    def __init__(self, ttl_seconds: int = 300, *, clock: Callable[[], datetime] | None = None):
        if type(ttl_seconds) is not int or ttl_seconds != 300:
            raise ValueError("Session TTL must be 300 seconds")
        self._ttl = timedelta(seconds=ttl_seconds)
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._sessions: dict[str, SecureSession] = {}
        self._lock = RLock()
        self._closed = False

    def _now(self) -> datetime:
        now = self._clock()
        if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() != timedelta(0):
            raise ValueError("Session clock must return UTC")
        return now.astimezone(timezone.utc)

    def create(self, gateway_id: str, cloud_key_id: str, session_key: bytes) -> SecureSession:
        """Construct fully before publication; errors leave no usable session."""
        for value in (gateway_id, cloud_key_id):
            if not isinstance(value, str) or not value or value != value.strip():
                raise ValueError("Session identifiers must be non-empty strings")
        if not isinstance(session_key, bytes) or len(session_key) != 32:
            raise ValueError("Session key must be 32 bytes")
        with self._lock:
            if self._closed:
                raise ValueError("Session manager is closed")
            now = self._now()
            session_id = f"sess-{uuid4()}"
            if session_id in self._sessions:
                raise ValueError("Session identifier collision")
            session = SecureSession(session_id, gateway_id, cloud_key_id, now,
                                    now + self._ttl, bytearray(session_key))
            self._sessions[session_id] = session
            return session

    def get(self, session_id: str, gateway_id: str) -> SecureSession:
        """Shared-protocol order: lookup, ownership, expiry. No TTL extension."""
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None or session.state != SessionState.ACTIVE:
                raise SessionAccessError(409, "SESSION_INVALID", "secure session is invalid")
            if session.gateway_id != gateway_id:
                raise SessionAccessError(400, "SECURE_MESSAGE_REJECTED", "secure message could not be processed")
            if self._now() >= session.expires_at:
                self.invalidate(session_id, SessionState.EXPIRED)
                raise SessionAccessError(409, "SESSION_EXPIRED", "secure session has expired")
            return session

    def invalidate(self, session_id: str, state: SessionState = SessionState.INVALIDATED) -> None:
        if state == SessionState.ACTIVE:
            raise ValueError("Invalidation requires a terminal state")
        with self._lock:
            session = self._sessions.pop(session_id, None)
            if session is not None:
                session.clear(state)

    def remove_expired(self) -> int:
        with self._lock:
            now = self._now()
            expired = [key for key, session in self._sessions.items() if now >= session.expires_at]
            for key in expired:
                self.invalidate(key, SessionState.EXPIRED)
            return len(expired)

    def close(self) -> None:
        with self._lock:
            self._closed = True
            for session_id in list(self._sessions):
                self.invalidate(session_id, SessionState.CLOSED)

    def __len__(self) -> int:
        with self._lock:
            return len(self._sessions)
