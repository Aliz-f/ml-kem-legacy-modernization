"""Measure one equivalent workload in classical mode and in mlkem mode.

The production Legacy route still stops before delivery, so this evaluation
calls CloudDispatch. Classical mode posts the canonical measurement to Cloud's
baseline route. Modernized mode uses the real secure transport. The first
secure request is timed separately because it includes session establishment.
This module records measurements. It does not rank the modes.
"""

from __future__ import annotations

import asyncio
import json
import threading
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import pytest
import uvicorn

from cloud_service.app import create_app
from cloud_service.config import load_config
from edge_gateway.config import load_config as load_gateway_config
from edge_gateway.crypto.failure import CryptoFailureInjector
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.secure_transport import SecureTransport, SecureTransportError
from edge_gateway.crypto.session import SessionManager
from edge_gateway.dispatch import CloudDispatch

_ROWS = tuple(
    {
        "request_id": f"req-eval-{sequence}",
        "device_id": "sensor-001",
        "temperature_c": 22.5,
        "humidity_pct": 44.0,
        "measured_at": "2026-09-21T13:45:31Z",
        "sequence_number": sequence,
        "received_at": "2026-09-21T13:45:31.218Z",
    }
    for sequence in range(1, 5)
)


@dataclass
class _Server:
    server: uvicorn.Server
    thread: threading.Thread
    url: str

    def stop(self) -> None:
        self.server.should_exit = True
        self.thread.join(timeout=5)


class _Baseline:
    def __init__(self, cloud_url: str) -> None:
        self._url = f"{cloud_url}/api/v1/baseline/measurements"
        self.sizes: list[int] = []

    async def send(self, **fields: object) -> int:
        request_id = str(fields.pop("request_id"))
        body = json.dumps(fields, separators=(",", ":")).encode()
        self.sizes.append(len(body))
        request = urllib.request.Request(
            self._url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-Request-ID": request_id,
            },
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status


class _Calls:
    def __init__(self) -> None:
        self.count = 0

    async def send(self, **_fields: object) -> None:
        self.count += 1


class _Sizes:
    def __init__(self, inner: urllib.request.OpenerDirector) -> None:
        self._inner = inner
        self.sizes: list[int] = []

    def open(self, request: urllib.request.Request, timeout: float | None = None):
        data = request.data
        if isinstance(data, bytes) and request.full_url.endswith(
            "/api/v1/secure/measurements"
        ):
            self.sizes.append(len(data))
        if timeout is None:
            return self._inner.open(request)
        return self._inner.open(request, timeout=timeout)

    def close(self) -> None:
        self._inner.close()


def _serve(tmp_path: Path, mode: str) -> _Server:
    app = create_app(
        load_config(
            {
                "DATABASE_URL": f"sqlite:///{tmp_path / f'{mode}.db'}",
                "SECURITY_MODE": mode,
                "LOG_LEVEL": "WARNING",
            }
        )
    )
    server = uvicorn.Server(
        uvicorn.Config(
            app, host="127.0.0.1", port=0, log_level="warning", access_log=False
        )
    )
    thread = threading.Thread(target=server.run, name=f"{mode}-eval", daemon=True)
    thread.start()
    deadline = time.monotonic() + 10
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            server.should_exit = True
            raise RuntimeError(f"{mode} Cloud did not start")
        time.sleep(0.02)
    sockets = server.servers[0].sockets
    if not sockets:
        server.should_exit = True
        raise RuntimeError(f"{mode} Cloud has no socket")
    return _Server(server, thread, f"http://127.0.0.1:{sockets[0].getsockname()[1]}")


def _dispatch(
    cloud_url: str,
    mode: str,
    *,
    baseline: _Baseline | _Calls,
    failure_mode: str = "none",
) -> tuple[CloudDispatch, SecureTransport | None, PqcMetrics]:
    config = load_gateway_config(
        {
            "SECURITY_MODE": mode,
            "CLOUD_URL": cloud_url,
            "LOG_LEVEL": "WARNING",
            "FAILURE_MODE": failure_mode,
            "FAILURE_RATE": "1.0" if failure_mode != "none" else "0.0",
        }
    )
    metrics = PqcMetrics()
    secure = None
    if mode == "mlkem":
        injector = CryptoFailureInjector(
            failure_mode, 1.0 if failure_mode != "none" else 0.0, None
        )
        sessions = SessionManager(
            config.gateway_id,
            cloud_url,
            config.cloud_timeout_seconds,
            metrics=metrics,
            injector=injector,
        )
        secure = SecureTransport(
            sessions,
            cloud_url=cloud_url,
            timeout_seconds=config.cloud_timeout_seconds,
            max_retries=config.cloud_max_retries,
            injector=injector,
            metrics=metrics,
            sleep=lambda _delay: None,
        )
    return (
        CloudDispatch(config, baseline=baseline, secure=secure, pqc_metrics=metrics),
        secure,
        metrics,
    )


async def _time_sends(dispatch: CloudDispatch, rows: tuple[dict[str, object], ...]) -> list[float]:
    timings: list[float] = []
    for row in rows:
        started = time.perf_counter()
        await dispatch.send(**row)
        timings.append(time.perf_counter() - started)
    return timings


def measure_modes(tmp_path: Path) -> dict[str, float | int]:
    """Run the equivalent workload and return the collected sample."""
    classical = _serve(tmp_path, "classical")
    modernized = _serve(tmp_path, "mlkem")
    try:
        baseline = _Baseline(classical.url)
        classical_dispatch, _, _ = _dispatch(
            classical.url, "classical", baseline=baseline
        )
        unused = _Calls()
        modern_dispatch, secure, metrics = _dispatch(
            modernized.url, "mlkem", baseline=unused
        )
        if secure is None:
            raise RuntimeError("mlkem dispatch has no secure transport")
        recorder = _Sizes(secure._opener)
        secure._opener = recorder
        classical_times = asyncio.run(_time_sends(classical_dispatch, _ROWS))
        modern_times = asyncio.run(_time_sends(modern_dispatch, _ROWS))
        if len(classical_times) != 4 or len(modern_times) != 4:
            raise RuntimeError("each mode must send four measurements")
        if metrics.handshake_duration.count != 1 or metrics.encapsulation_duration.count != 1:
            raise RuntimeError("the first four messages did not use one handshake")
        if metrics.message_duration["steady"].count != 3:
            raise RuntimeError("steady-state reuse count was not 3")
        reuse_count = metrics.message_duration["steady"].count
        steady = metrics.message_duration["steady"]
        secure_steady_ms = steady.total_seconds / steady.count * 1000
        secure_first_ms = metrics.message_duration["first"].total_seconds * 1000
        first_handshake_ms = (
            metrics.handshake_duration.total_seconds
            / metrics.handshake_duration.count
            * 1000
        )
        encapsulation_ms = (
            metrics.encapsulation_duration.total_seconds
            / metrics.encapsulation_duration.count
            * 1000
        )
        session = secure._sessions._session
        if session is None:
            raise RuntimeError("mlkem workload did not keep a session")
        modernized.server.config.app.state.sessions.invalidate(session.session_id)
        asyncio.run(
            modern_dispatch.send(
                request_id="req-eval-5",
                device_id="sensor-001",
                temperature_c=22.5,
                humidity_pct=44.0,
                measured_at="2026-09-21T13:45:31Z",
                sequence_number=5,
                received_at="2026-09-21T13:45:31.218Z",
            )
        )
        return {
            "classical_first_ms": classical_times[0] * 1000,
            "classical_steady_ms": sum(classical_times[1:]) / 3 * 1000,
            "classical_body_bytes": baseline.sizes[0],
            "handshake_ms": first_handshake_ms,
            "encapsulation_ms": encapsulation_ms,
            "secure_first_ms": secure_first_ms,
            "secure_steady_ms": secure_steady_ms,
            "envelope_bytes": recorder.sizes[0],
            "reuse_count": reuse_count,
            "reestablishment_count": metrics.reestablishments["success"],
            "handshake_count": metrics.handshakes_succeeded,
            "fallback_count": metrics.pqc_fallback_total,
            "baseline_calls_during_mlkem": unused.count,
        }
    finally:
        classical.stop()
        modernized.stop()


def test_recorded_sample_is_one_local_run_and_does_not_rank_modes() -> None:
    document = (
        Path(__file__).parents[2] / "edge_gateway" / "docs" / "mode-evaluation.md"
    ).read_text(encoding="utf-8")
    readme = (
        Path(__file__).parents[2] / "edge_gateway" / "README.md"
    ).read_text(encoding="utf-8")

    assert "It does not rank the modes" in document
    assert "The first secure request is reported separately" in document
    assert "| Classical first request | 13.012 ms |" in document
    assert "| First secure-message latency | 15.871 ms |" in document
    assert "| Steady-state secure-message mean, requests 2-4 | 1.253 ms |" in document
    assert "| SecureEnvelope size | 455 bytes |" in document
    assert "| Session reuse count | 3 |" in document
    assert "| Session re-establishment count | 1 |" in document
    assert "Baseline calls during mlkem delivery | 0 |" in document
    assert "does not rank the modes" in readme


def test_equivalent_workload_keeps_the_modes_separate(tmp_path: Path) -> None:
    sample = measure_modes(tmp_path)

    assert sample["reuse_count"] == 3
    assert sample["reestablishment_count"] == 1
    assert sample["handshake_count"] == 2
    assert sample["fallback_count"] == 0
    assert sample["baseline_calls_during_mlkem"] == 0
    assert sample["classical_body_bytes"] > 0
    assert sample["envelope_bytes"] > sample["classical_body_bytes"]
    assert sample["secure_first_ms"] > 0
    assert sample["secure_steady_ms"] > 0


@pytest.mark.parametrize(
    "failure_mode",
    ["mlkem_handshake_failure", "corrupt_ciphertext"],
)
def test_injected_crypto_failure_does_not_call_baseline(
    tmp_path: Path, failure_mode: str
) -> None:
    modernized = _serve(tmp_path, "mlkem")
    try:
        baseline = _Calls()
        dispatch, _, metrics = _dispatch(
            modernized.url,
            "mlkem",
            baseline=baseline,
            failure_mode=failure_mode,
        )
        with pytest.raises(SecureTransportError):
            asyncio.run(dispatch.send(**_ROWS[0]))
        assert baseline.count == 0
        assert metrics.pqc_fallback_total == 0
        assert dispatch.metrics.secure_failures_total == 1
        assert metrics.injected_failures[failure_mode] == 1
    finally:
        modernized.stop()
