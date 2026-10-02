"""HTTP client for POST /api/v1/crypto/sessions.

The request carries the ML-KEM ciphertext. The shared secret and session key
stay off the wire. Response validation does not create a local session.
"""

from __future__ import annotations

import http.client
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin, urlparse

from edge_gateway.crypto.encoding import encode_binary
from edge_gateway.crypto.mlkem import CIPHERTEXT_LENGTH
from edge_gateway.crypto.public_key import PROTOCOL_VERSION

_PATH = "api/v1/crypto/sessions"
_MAX_BODY_BYTES = 16 * 1024
_RETRYABLE_STATUS = frozenset({500, 502, 503, 504})


class SessionTransportError(Exception):
    """The session request did not return a usable response."""

    def __init__(self, message: str, *, retryable: bool) -> None:
        super().__init__(message)
        self.retryable = retryable


class SessionRejected(Exception):
    """The session response does not match the frozen contract."""


class _RejectRedirect(urllib.request.HTTPRedirectHandler):
    """The configured Cloud URL is the only accepted session endpoint."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise SessionTransportError(
            "Cloud session endpoint redirected.",
            retryable=False,
        )


@dataclass(frozen=True, slots=True)
class SessionResponse:
    """Validated fields from a successful session response."""

    protocol_version: str
    session_id: str
    expires_at: datetime


def post_session(
    cloud_url: str,
    timeout_seconds: float,
    *,
    gateway_id: str,
    key_id: str,
    encapsulation_ciphertext: bytes,
    now: datetime,
) -> SessionResponse:
    """POST one encapsulation ciphertext and validate the Cloud response."""
    if len(encapsulation_ciphertext) != CIPHERTEXT_LENGTH:
        raise SessionRejected("Encapsulation ciphertext must be 1088 bytes.")
    payload = {
        "protocol_version": PROTOCOL_VERSION,
        "gateway_id": gateway_id,
        "key_id": key_id,
        "encapsulation_ciphertext": encode_binary(encapsulation_ciphertext),
    }
    body = _request(cloud_url, timeout_seconds, payload)
    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise SessionRejected("Session response is not JSON.") from exc
    return parse_session_response(parsed, now=now)


def parse_session_response(payload: object, *, now: datetime) -> SessionResponse:
    """Validate a decoded session-establishment response."""
    if not isinstance(payload, dict):
        raise SessionRejected("Session response must be a JSON object.")
    if payload.get("protocol_version") != PROTOCOL_VERSION:
        raise SessionRejected("Unsupported protocol_version.")
    session_id = payload.get("session_id")
    if not isinstance(session_id, str) or session_id == "" or session_id != session_id.strip():
        raise SessionRejected("session_id must be a non-empty string.")
    if payload.get("status") != "established":
        raise SessionRejected("status must be established.")
    expires_at = _parse_expires_at(payload.get("expires_at"))
    if expires_at <= now:
        raise SessionRejected("expires_at must be in the future.")
    return SessionResponse(
        protocol_version=PROTOCOL_VERSION,
        session_id=session_id,
        expires_at=expires_at,
    )


def _parse_expires_at(value: object) -> datetime:
    if not isinstance(value, str) or value == "":
        raise SessionRejected("expires_at must be an explicit UTC timestamp.")
    if value.endswith("Z"):
        candidate = value[:-1] + "+00:00"
    else:
        candidate = value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise SessionRejected("expires_at must be an explicit UTC timestamp.") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise SessionRejected("expires_at must be an explicit UTC timestamp.")
    return parsed.astimezone(timezone.utc)


def _request(cloud_url: str, timeout_seconds: float, payload: dict[str, str]) -> bytes:
    if not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool):
        raise SessionTransportError(
            "Cloud session timeout must be greater than zero.",
            retryable=False,
        )
    if timeout_seconds <= 0:
        raise SessionTransportError(
            "Cloud session timeout must be greater than zero.",
            retryable=False,
        )
    raw = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        _endpoint(cloud_url),
        data=raw,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    opener = urllib.request.build_opener(_RejectRedirect)
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            body = response.read(_MAX_BODY_BYTES + 1)
            status = response.status
    except SessionTransportError:
        raise
    except TimeoutError as exc:
        raise SessionTransportError(
            "Cloud session request timed out.",
            retryable=True,
        ) from exc
    except urllib.error.HTTPError as exc:
        raise SessionTransportError(
            f"Cloud session request failed with HTTP {exc.code}.",
            retryable=exc.code in _RETRYABLE_STATUS,
        ) from exc
    except urllib.error.URLError as exc:
        timed_out = isinstance(exc.reason, TimeoutError)
        message = (
            "Cloud session request timed out."
            if timed_out
            else "Cloud session request failed."
        )
        raise SessionTransportError(message, retryable=True) from exc
    except (http.client.HTTPException, OSError) as exc:
        # A reset or truncated body while reading is not wrapped in URLError.
        raise SessionTransportError(
            "Cloud session request failed.",
            retryable=True,
        ) from exc
    if status != 200:
        raise SessionTransportError(
            f"Cloud session request failed with HTTP {status}.",
            retryable=status in _RETRYABLE_STATUS,
        )
    if len(body) > _MAX_BODY_BYTES:
        raise SessionRejected("Session response exceeds 16 KiB.")
    return body


def _endpoint(cloud_url: str) -> str:
    if not isinstance(cloud_url, str):
        raise SessionTransportError(
            "CLOUD_URL must be an HTTP or HTTPS URL.",
            retryable=False,
        )
    parsed = urlparse(cloud_url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc == "":
        raise SessionTransportError(
            "CLOUD_URL must be an HTTP or HTTPS URL.",
            retryable=False,
        )
    return urljoin(cloud_url.rstrip("/") + "/", _PATH)
