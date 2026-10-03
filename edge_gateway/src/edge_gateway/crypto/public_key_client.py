"""HTTP client for GET /api/v1/crypto/public-key.

Networking stays in this module. Field validation and ML-KEM key checks stay
in the parser. The client does not encapsulate.
"""

from __future__ import annotations

import http.client
import json
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlparse

from edge_gateway.crypto.public_key import (
    CloudPublicKey,
    PublicKeyRejected,
    parse_public_key_response,
)

_PATH = "api/v1/crypto/public-key"
_MAX_BODY_BYTES = 16 * 1024
_RETRYABLE_STATUS = frozenset({500, 502, 503, 504})


class PublicKeyTransportError(Exception):
    """The public-key request did not return a usable response."""

    def __init__(self, message: str, *, retryable: bool) -> None:
        super().__init__(message)
        self.retryable = retryable


class _RejectRedirect(urllib.request.HTTPRedirectHandler):
    """The configured Cloud URL is the only accepted public-key source."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise PublicKeyTransportError(
            "Cloud public-key endpoint redirected.",
            retryable=False,
        )


def fetch_public_key(cloud_url: str, timeout_seconds: float) -> CloudPublicKey:
    """GET the Cloud public key and return the validated key."""
    if not isinstance(timeout_seconds, (int, float)) or timeout_seconds <= 0:
        raise PublicKeyTransportError(
            "Cloud public-key timeout must be greater than zero.",
            retryable=False,
        )
    request = urllib.request.Request(_endpoint(cloud_url), method="GET")
    opener = urllib.request.build_opener(_RejectRedirect)
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            body = response.read(_MAX_BODY_BYTES + 1)
            status = response.status
    except PublicKeyTransportError:
        raise
    except TimeoutError as exc:
        raise PublicKeyTransportError(
            "Cloud public-key request timed out.",
            retryable=True,
        ) from exc
    except urllib.error.HTTPError as exc:
        raise PublicKeyTransportError(
            f"Cloud public-key request failed with HTTP {exc.code}.",
            retryable=exc.code in _RETRYABLE_STATUS,
        ) from exc
    except urllib.error.URLError as exc:
        timed_out = isinstance(exc.reason, TimeoutError)
        message = (
            "Cloud public-key request timed out."
            if timed_out
            else "Cloud public-key request failed."
        )
        raise PublicKeyTransportError(message, retryable=True) from exc
    except (http.client.HTTPException, OSError) as exc:
        # A reset or truncated body while reading is not wrapped in URLError.
        raise PublicKeyTransportError(
            "Cloud public-key request failed.",
            retryable=True,
        ) from exc
    if status != 200:
        raise PublicKeyTransportError(
            f"Cloud public-key request failed with HTTP {status}.",
            retryable=status in _RETRYABLE_STATUS,
        )
    if len(body) > _MAX_BODY_BYTES:
        raise PublicKeyRejected("Public-key response exceeds 16 KiB.")
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise PublicKeyRejected("Public-key response is not JSON.") from exc
    return parse_public_key_response(payload)


def _endpoint(cloud_url: str) -> str:
    if not isinstance(cloud_url, str):
        raise PublicKeyTransportError(
            "CLOUD_URL must be an HTTP or HTTPS URL.",
            retryable=False,
        )
    parsed = urlparse(cloud_url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc == "":
        raise PublicKeyTransportError(
            "CLOUD_URL must be an HTTP or HTTPS URL.",
            retryable=False,
        )
    return urljoin(cloud_url.rstrip("/") + "/", _PATH)
