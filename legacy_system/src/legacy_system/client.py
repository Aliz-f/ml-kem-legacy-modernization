"""HTTP client for sending prepared Legacy Device payloads to the Gateway."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from enum import StrEnum
from http.client import HTTPException
import json
import socket
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ErrorCategory(StrEnum):
    """Stable failure categories exposed by the Gateway client."""

    HTTP = "http"
    TIMEOUT = "timeout"
    CONNECTION = "connection"
    PAYLOAD = "payload"


@dataclass(frozen=True, slots=True)
class GatewayResult:
    """Outcome of one request to the Edge Gateway."""

    success: bool
    status_code: int | None
    attempt_count: int
    error_category: ErrorCategory | None
    retryable: bool


class GatewayClient:
    """Send one prepared Legacy payload to the configured Gateway endpoint."""

    def __init__(
        self,
        gateway_url: str,
        request_timeout_seconds: float,
        opener: Callable[..., Any] = urlopen,
        max_retries: int = 2,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        if isinstance(max_retries, bool) or not isinstance(max_retries, int):
            raise ValueError("max_retries must be a non-negative integer")
        if max_retries < 0:
            raise ValueError("max_retries must be a non-negative integer")
        self._endpoint = f"{gateway_url.rstrip('/')}/api/v1/measurements"
        self._request_timeout_seconds = request_timeout_seconds
        self._opener = opener
        self._max_retries = max_retries
        self._sleeper = sleeper

    def send(self, payload: Mapping[str, object]) -> GatewayResult:
        """Send a payload with bounded retries for retryable outcomes."""
        result = self._send_once(payload)
        attempt_count = 1

        while result.retryable and attempt_count <= self._max_retries:
            self._sleeper(2 ** (attempt_count - 1))
            result = self._send_once(payload)
            attempt_count += 1
            result = replace(result, attempt_count=attempt_count)

        return result

    def _send_once(self, payload: Mapping[str, object]) -> GatewayResult:
        """Send one request and classify its outcome without retrying."""
        try:
            encoded_payload = json.dumps(payload).encode("utf-8")
        except (TypeError, ValueError):
            return GatewayResult(
                success=False,
                status_code=None,
                attempt_count=1,
                error_category=ErrorCategory.PAYLOAD,
                retryable=False,
            )

        request = Request(
            self._endpoint,
            data=encoded_payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with self._opener(
                request, timeout=self._request_timeout_seconds
            ) as response:
                return self._result_for_status(response.status)
        except HTTPError as error:
            return self._result_for_status(error.code)
        except (socket.timeout, TimeoutError):
            return GatewayResult(
                success=False,
                status_code=None,
                attempt_count=1,
                error_category=ErrorCategory.TIMEOUT,
                retryable=True,
            )
        except URLError as error:
            category = (
                ErrorCategory.TIMEOUT
                if isinstance(error.reason, (socket.timeout, TimeoutError))
                else ErrorCategory.CONNECTION
            )
            return GatewayResult(
                success=False,
                status_code=None,
                attempt_count=1,
                error_category=category,
                retryable=True,
            )
        except HTTPException:
            return GatewayResult(
                success=False,
                status_code=None,
                attempt_count=1,
                error_category=ErrorCategory.CONNECTION,
                retryable=True,
            )
        except OSError:
            return GatewayResult(
                success=False,
                status_code=None,
                attempt_count=1,
                error_category=ErrorCategory.CONNECTION,
                retryable=True,
            )

    @staticmethod
    def _result_for_status(status_code: int) -> GatewayResult:
        return GatewayResult(
            success=status_code == 202,
            status_code=status_code,
            attempt_count=1,
            error_category=None if status_code == 202 else ErrorCategory.HTTP,
            retryable=status_code in {500, 502, 503, 504},
        )