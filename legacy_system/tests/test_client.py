import logging
import socket
from http.client import HTTPException
from urllib.error import HTTPError, URLError

import pytest

from legacy_system.client import ErrorCategory, GatewayClient


class FakeResponse:
    def __init__(self, status: int) -> None:
        self.status = status

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None


class ScriptedOpener:
    def __init__(self, outcomes: list[FakeResponse | BaseException]) -> None:
        self._outcomes = outcomes
        self.calls = 0

    def __call__(self, *_args: object, **_kwargs: object) -> FakeResponse:
        if self.calls >= len(self._outcomes):
            raise AssertionError("the opener was called more than expected")
        outcome = self._outcomes[self.calls]
        self.calls += 1
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


def test_send_posts_prepared_payload_to_gateway() -> None:
    calls: list[tuple[object, float]] = []

    def opener(request: object, *, timeout: float) -> FakeResponse:
        calls.append((request, timeout))
        return FakeResponse(202)

    client = GatewayClient(
        "http://gateway.example.test/",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=0,
    )
    payload = {
        "device_id": "sensor-001",
        "temperature_c": 21.7,
        "humidity_pct": 42.5,
        "timestamp": "2026-09-21T13:45:31Z",
        "sequence_number": 184,
    }

    result = client.send(payload)

    request, timeout = calls[0]
    assert request.full_url == (
        "http://gateway.example.test/api/v1/measurements"
    )
    assert request.get_method() == "POST"
    assert request.get_header("Content-type") == "application/json"
    assert request.data == (
        b'{"device_id": "sensor-001", "temperature_c": 21.7, '
        b'"humidity_pct": 42.5, "timestamp": "2026-09-21T13:45:31Z", '
        b'"sequence_number": 184}'
    )
    assert timeout == 3
    assert len(calls) == 1
    assert result.success is True
    assert result.status_code == 202
    assert result.attempt_count == 1
    assert result.error_category is None
    assert result.retryable is False


@pytest.mark.parametrize(
    ("status_code", "retryable"),
    [
        (400, False),
        (409, False),
        (422, False),
        (500, True),
        (502, True),
        (503, True),
        (504, True),
    ],
)
def test_http_statuses_are_classified_by_retryability(
    status_code: int, retryable: bool
) -> None:
    calls = 0

    def opener(*_args: object, **_kwargs: object) -> FakeResponse:
        nonlocal calls
        calls += 1
        return FakeResponse(status_code)

    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=0,
    )

    result = client.send({"sequence_number": 1})

    assert result.success is False
    assert calls == 1
    assert result.status_code == status_code
    assert result.attempt_count == 1
    assert result.error_category is ErrorCategory.HTTP
    assert result.retryable is retryable


@pytest.mark.parametrize(
    ("exception", "category"),
    [
        (socket.timeout(), ErrorCategory.TIMEOUT),
        (TimeoutError(), ErrorCategory.TIMEOUT),
        (URLError(socket.timeout()), ErrorCategory.TIMEOUT),
        (URLError("connection refused"), ErrorCategory.CONNECTION),
        (ConnectionError(), ErrorCategory.CONNECTION),
        (HTTPException("invalid response"), ErrorCategory.CONNECTION),
    ],
)
def test_transport_failures_are_stable_and_retryable(
    exception: Exception, category: ErrorCategory
) -> None:
    calls = 0

    def opener(*_args: object, **_kwargs: object) -> FakeResponse:
        nonlocal calls
        calls += 1
        raise exception

    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=0,
    )

    result = client.send({"sequence_number": 1})

    assert calls == 1
    assert result.success is False
    assert result.status_code is None
    assert result.attempt_count == 1
    assert result.error_category is category
    assert result.retryable is True


def test_http_error_is_classified_without_leaking_exception() -> None:
    error = HTTPError(
        "http://gateway.example.test/api/v1/measurements",
        503,
        "unavailable",
        hdrs=None,
        fp=None,
    )

    def opener(*_args: object, **_kwargs: object) -> FakeResponse:
        raise error

    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=0,
    )

    result = client.send({"sequence_number": 1})

    assert result.status_code == 503
    assert result.error_category is ErrorCategory.HTTP
    assert result.retryable is True


def test_unserializable_payload_is_non_retryable() -> None:
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=lambda *_args, **_kwargs: pytest.fail("request was sent"),
    )

    result = client.send({"invalid": object()})

    assert result.success is False
    assert result.status_code is None
    assert result.attempt_count == 1
    assert result.error_category is ErrorCategory.PAYLOAD
    assert result.retryable is False


def test_retry_logging_exposes_failed_attempts_and_retry_events(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.WARNING, logger="legacy_system.client")
    opener = ScriptedOpener([FakeResponse(503), FakeResponse(422)])
    delays: list[float] = []
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=2,
        sleeper=delays.append,
    )

    result = client.send({"device_id": "sensor-001", "sequence_number": 42})

    assert result.success is False
    assert result.status_code == 422
    assert "event=gateway_request_failed" in caplog.text
    assert "event=gateway_retry" in caplog.text
    assert "component=legacy_system" in caplog.text


@pytest.mark.parametrize("status_code", [500, 502, 503, 504])
def test_retryable_http_status_retries_then_succeeds(status_code: int) -> None:
    opener = ScriptedOpener([FakeResponse(status_code), FakeResponse(202)])
    delays: list[float] = []
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=2,
        sleeper=delays.append,
    )

    result = client.send({"sequence_number": 1})

    assert opener.calls == 2
    assert delays == [1]
    assert result.success is True
    assert result.status_code == 202
    assert result.attempt_count == 2


@pytest.mark.parametrize("status_code", [400, 409, 422])
def test_non_retryable_http_status_stops_immediately(status_code: int) -> None:
    opener = ScriptedOpener([FakeResponse(status_code)])
    delays: list[float] = []
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=2,
        sleeper=delays.append,
    )

    result = client.send({"sequence_number": 1})

    assert opener.calls == 1
    assert delays == []
    assert result.status_code == status_code
    assert result.attempt_count == 1


@pytest.mark.parametrize(
    "failure",
    [socket.timeout(), ConnectionError(), HTTPException("invalid response")],
)
def test_transport_failure_retries_then_succeeds(failure: BaseException) -> None:
    opener = ScriptedOpener([failure, FakeResponse(202)])
    delays: list[float] = []
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=2,
        sleeper=delays.append,
    )

    result = client.send({"sequence_number": 1})

    assert opener.calls == 2
    assert delays == [1]
    assert result.success is True
    assert result.attempt_count == 2


def test_retry_exhaustion_is_bounded_and_uses_deterministic_backoff() -> None:
    opener = ScriptedOpener(
        [FakeResponse(503), FakeResponse(503), FakeResponse(503)]
    )
    delays: list[float] = []
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=2,
        sleeper=delays.append,
    )

    result = client.send({"sequence_number": 1})

    assert opener.calls == 3
    assert len(delays) == opener.calls - 1
    assert delays == [1, 2]
    assert result.success is False
    assert result.status_code == 503
    assert result.attempt_count == 3


def test_default_retry_count_allows_two_retries() -> None:
    opener = ScriptedOpener(
        [FakeResponse(503), FakeResponse(503), FakeResponse(503)]
    )
    delays: list[float] = []
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        sleeper=delays.append,
    )

    result = client.send({"sequence_number": 1})

    assert opener.calls == 3
    assert delays == [1, 2]
    assert result.status_code == 503
    assert result.attempt_count == 3


def test_retry_stops_after_non_retryable_result() -> None:
    opener = ScriptedOpener([FakeResponse(503), FakeResponse(422)])
    delays: list[float] = []
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=2,
        sleeper=delays.append,
    )

    result = client.send({"sequence_number": 1})

    assert opener.calls == 2
    assert delays == [1]
    assert result.status_code == 422
    assert result.attempt_count == 2
    assert result.retryable is False


def test_zero_retries_makes_only_the_initial_request() -> None:
    opener = ScriptedOpener([FakeResponse(503)])
    delays: list[float] = []
    client = GatewayClient(
        "http://gateway.example.test",
        request_timeout_seconds=3,
        opener=opener,
        max_retries=0,
        sleeper=delays.append,
    )

    result = client.send({"sequence_number": 1})

    assert opener.calls == 1
    assert delays == []
    assert result.status_code == 503
    assert result.attempt_count == 1


@pytest.mark.parametrize("max_retries", [-1, 1.5, True])
def test_invalid_retry_counts_are_rejected(max_retries: object) -> None:
    with pytest.raises(ValueError, match="non-negative integer"):
        GatewayClient(
            "http://gateway.example.test",
            request_timeout_seconds=3,
            max_retries=max_retries,  # type: ignore[arg-type]
        )
