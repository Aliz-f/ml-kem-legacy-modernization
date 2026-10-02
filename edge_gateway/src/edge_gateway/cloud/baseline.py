"""Classical Gateway-to-Cloud delivery for the frozen baseline endpoint."""

from __future__ import annotations

import asyncio
import http.client
import json
import math
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

from edge_gateway.correlation import baseline_headers
from edge_gateway.transport import CloudDeliveryError


_PATH = "api/v1/baseline/measurements"
_MAX_BODY_BYTES = 16 * 1024
_RETRYABLE_STATUS = frozenset({500, 502, 503, 504})
_ACCEPTED_STATUS = frozenset({"accepted", "already_accepted"})


class BaselineCloudError(CloudDeliveryError):
    """A classified baseline delivery failure without remote error details."""

    def __init__(self, message: str, *, retryable: bool, code: str | None = None) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.code = code


class _RejectRedirect(urllib.request.HTTPRedirectHandler):
    """Keep delivery bound to the configured Cloud endpoint."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise BaselineCloudError("Cloud baseline endpoint redirected.", retryable=False)


@dataclass(frozen=True, slots=True)
class BaselineAcceptance:
    """Normalized response after Cloud accepted a canonical measurement."""

    status: str
    record_id: str


class BaselineCloudClient:
    """Send one canonical measurement with bounded ordinary transport retries."""

    def __init__(
        self, *, cloud_url: str, timeout_seconds: float, max_retries: int,
        sleep: Callable[[float], None] = time.sleep,
        before_attempt: Callable[[str], None] | None = None,
    ) -> None:
        if (
            isinstance(timeout_seconds, bool)
            or not isinstance(timeout_seconds, (int, float))
            or not math.isfinite(timeout_seconds)
            or timeout_seconds <= 0
        ):
            raise ValueError("timeout_seconds must be greater than zero.")
        if isinstance(max_retries, bool) or not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("max_retries must be a non-negative integer.")
        self._endpoint = _endpoint(cloud_url)
        self._timeout_seconds = float(timeout_seconds)
        self._max_retries = max_retries
        self._before_attempt = before_attempt
        self._sleep = sleep
        self._opener = urllib.request.build_opener(_RejectRedirect)

    async def send(
        self,
        *,
        request_id: str,
        gateway_id: str,
        device_id: str,
        temperature_c: float,
        humidity_pct: float,
        measured_at: str,
        sequence_number: int,
        received_at: str,
    ) -> BaselineAcceptance:
        """Serialize once, then retry only classified transient delivery failures."""
        body = _dump(
            gateway_id=gateway_id,
            device_id=device_id,
            temperature_c=temperature_c,
            humidity_pct=humidity_pct,
            measured_at=measured_at,
            sequence_number=sequence_number,
            received_at=received_at,
        )
        return await asyncio.to_thread(self._deliver, body, request_id)

    def _deliver(self, body: bytes, request_id: str) -> BaselineAcceptance:
        """Retry the same logical baseline request at most ``max_retries`` times."""
        failure: BaselineCloudError | None = None
        for attempt in range(self._max_retries + 1):
            try:
                return self._post(body, request_id)
            except BaselineCloudError as exc:
                if not exc.retryable:
                    raise
                failure = exc
                if attempt < self._max_retries:
                    # Frozen Gateway backoff: 1 second before retry two, then 2.
                    self._sleep(2.0**attempt)
        if failure is None:  # Defensive: every exhausted iteration is retryable.
            raise RuntimeError("baseline delivery exhausted without a failure")
        raise failure

    def _post(self, body: bytes, request_id: str) -> BaselineAcceptance:
        request = urllib.request.Request(
            self._endpoint,
            data=body,
            method="POST",
            headers={"Content-Type": "application/json", **baseline_headers(request_id)},
        )
        try:
            if self._before_attempt is not None:
                self._before_attempt(request_id)
            with self._opener.open(request, timeout=self._timeout_seconds) as response:
                payload = response.read(_MAX_BODY_BYTES + 1)
                status = response.status
        except BaselineCloudError:
            raise
        except TimeoutError as exc:
            raise BaselineCloudError("Cloud baseline request timed out.", retryable=True) from exc
        except urllib.error.HTTPError as exc:
            payload = exc.read(_MAX_BODY_BYTES + 1)
            code = _error_code(payload)
            raise BaselineCloudError(
                "Cloud baseline request was rejected.",
                retryable=exc.code in _RETRYABLE_STATUS,
                code=code,
            ) from exc
        except (urllib.error.URLError, http.client.HTTPException) as exc:
            raise BaselineCloudError("Cloud baseline connection failed.", retryable=True) from exc
        if status != 202:
            raise BaselineCloudError("Cloud baseline request was not accepted.", retryable=False)
        return _parse_acceptance(payload)


def _dump(**measurement: object) -> bytes:
    return json.dumps(measurement, separators=(",", ":")).encode("utf-8")


def _parse_acceptance(body: bytes) -> BaselineAcceptance:
    if len(body) > _MAX_BODY_BYTES:
        raise BaselineCloudError("Cloud baseline response exceeds 16 KiB.", retryable=False)
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise BaselineCloudError("Cloud baseline response is not JSON.", retryable=False) from exc
    if not isinstance(payload, dict):
        raise BaselineCloudError("Cloud baseline response must be a JSON object.", retryable=False)
    status = payload.get("status")
    record_id = payload.get("record_id")
    if status not in _ACCEPTED_STATUS:
        raise BaselineCloudError("Cloud baseline response status is not accepted.", retryable=False)
    if not isinstance(record_id, str) or not record_id.strip() or record_id != record_id.strip():
        raise BaselineCloudError("Cloud baseline response record_id is missing.", retryable=False)
    return BaselineAcceptance(status=status, record_id=record_id)


def _error_code(body: bytes) -> str | None:
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("error"), dict):
        return None
    code = payload["error"].get("code")
    return code if isinstance(code, str) and code and code.strip() == code else None


def _endpoint(cloud_url: str) -> str:
    if not isinstance(cloud_url, str):
        raise ValueError("cloud_url must be an HTTP or HTTPS URL.")
    parsed = urlparse(cloud_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("cloud_url must be an HTTP or HTTPS URL.")
    return urljoin(cloud_url.rstrip("/") + "/", _PATH)
