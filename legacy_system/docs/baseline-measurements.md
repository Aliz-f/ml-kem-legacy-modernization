# Baseline Legacy Device measurements (M1-16)

This record implements Member 1 task **M1-16: Baseline data collection**. It
establishes and freezes the Legacy-side baseline observations before cryptographic
modernization. It complements Member 2's Gateway-route baseline
([`edge_gateway/docs/baseline-measurements.md`](../../edge_gateway/docs/baseline-measurements.md))
and Member 5's E2E baseline harness
([`docs/evaluation/baseline-measurement-method.md`](../../docs/evaluation/baseline-measurement-method.md)).

No production runtime code or protocol contracts are modified.

---

## 1. How to reproduce

From the repository root with the locked development environment installed:

```bash
uv run pytest legacy_system/tests/test_baseline_measurements.py -q -s
```

The test runs a 100-sample healthy workload over a loopback HTTP socket, checks
client acknowledgements, payload sizes, latencies, and monotonic sequence order,
and runs controlled failure scenarios. It does not run the Gateway or Cloud and
therefore is not evidence of forwarding or Cloud persistence.

---

## 2. Workload and configuration

| Parameter | Healthy baseline workload | Controlled failure scenarios |
| --- | --- | --- |
| Number of messages | 100 sequential client requests | 1 request per failure scenario |
| Device ID | `sensor-001` | `sensor-001` / `sensor-test` |
| Failure mode | `none` | `none` (server-side faults tested) |
| Sequence numbers | 0 through 99 (monotonic) | Increments monotonically across client failures |
| Client timeout | 3.0 seconds | 0.5 – 1.0 seconds |
| Client max retries | 2 retries | 2 retries (exponential backoff 1s, 2s) |
| Transport | HTTP/1.1 POST over loopback | HTTP/1.1 POST over loopback |
| Endpoint | `POST /api/v1/measurements` | `POST /api/v1/measurements` |

---

## 3. Measurement boundaries

| Metric | Boundary & calculation |
| --- | --- |
| **Legacy JSON payload size** | Exact serialized UTF-8 bytes (`len(json.dumps(payload).encode("utf-8"))`). Excludes HTTP headers. |
| **Legacy client → loopback receiver latency** | Client-side round-trip duration from `GatewayClient.send()` invocation until a synthetic loopback acknowledgement is parsed. Measured with `time.perf_counter()`. It is not Gateway-to-Cloud latency. |
| **Loopback acknowledgement rate** | Ratio of synthetic HTTP `202` loopback acknowledgements to total generated messages. It does not establish Cloud acceptance or persistence. |
| **Retry count** | Additional HTTP attempts beyond the initial attempt (`attempt_count - 1`). |
| **Sequence continuity** | Monotonic increment of `sequence_number` in `Sensor` across successful and failed delivery attempts. |

---

## 4. Recorded local sample

Collected on 2026-10-04 using the locked repository environment.
- **Environment:** Windows (`win32`), Python 3.12.14, pytest 9.1.1, loopback network socket.
- **Legacy component test suite:** 159 passed tests in `legacy_system/tests`.

### A. Healthy baseline summary (100 sequential messages)

| Observation | Value |
| --- | --- |
| Messages generated | 100 |
| Loopback acknowledgements (synthetic `202`) | 100 |
| Loopback acknowledgement rate | **100.0%** |
| Total retries triggered | 0 |
| Sequence progression | Monotonic (0 through 99 received in order) |

### B. Payload size distribution (bytes)

| Count | Minimum | Mean | Median | P95 | Maximum |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 162.0 B | 165.67 B | 166.0 B | 167.0 B | 167.0 B |

*Note: Payload sizes vary slightly (162–167 B) due to floating-point precision of generated sensor readings and sequence number digit width.*

### C. Client round-trip latency (milliseconds)

| Count | Minimum | Mean | Median | P95 | Maximum (first-request warm-up) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 0.51 ms | 1.10 ms | 0.58 ms | 0.84 ms | 20.35 ms |

*Note: Latency includes local loopback TCP socket connection, JSON serialization, HTTP request transmission, receiver handling, and HTTP response parsing. It does not include real Gateway validation/forwarding or Cloud persistence. The maximum latency reflects one-time first-request connection setup.*

---

## 5. Controlled failure observations

| Scenario | Injected condition | Observed client behavior | Retries | Sequence outcome |
| --- | --- | --- | ---: | --- |
| **Receiver unavailable** | Port closed / connection refused | 3 attempts (`attempt_count=3`), exponential backoff (1s, 2s), `error_category in {connection, timeout}` | 2 | Monotonic sequence continues (`seq=0` -> `seq=1`) |
| **Receiver 503 error** | Loopback server returns `503 Service Unavailable` | 3 attempts, `result.status_code=503`, `retryable=True` | 2 | Bounded retries exhausted; device continues |
| **Synthetic 422 response** | Loopback server returns `422 Unprocessable Entity` | 1 attempt, `result.status_code=422`, `retryable=False` | 0 | Non-retryable per protocol; no retry storm |
| **Device controller loop** | Persistent loopback `500 Internal Server Error` | Bounded retries per cycle; controller loop does not crash; graceful shutdown on stop event | 1 per cycle | Monotonic sequence increments each cycle |

---

## 6. Component test suite status

At the completion of Task M1-16, the Legacy Device test suite contains **159 automated tests**:

- `legacy_system/tests/test_config.py`: 22 tests (configuration loading and validation)
- `legacy_system/tests/test_sensor.py`: 31 tests (sensor generation, precision, sequence monotonicity)
- `legacy_system/tests/test_failure.py`: 24 tests (fault injection modes and deterministic seeds)
- `legacy_system/tests/test_client.py`: 35 tests (HTTP client, retry policy, error categories)
- `legacy_system/tests/test_device.py`: 17 tests (runtime loop, signal handling, graceful shutdown)
- `legacy_system/tests/test_main.py`: 2 tests (CLI entry point)
- `legacy_system/tests/test_docker_assets.py`: 13 tests (Dockerfile validation and container assets)
- `legacy_system/tests/test_multi_device.py`: 5 tests (multi-device configuration and concurrency)
- `legacy_system/tests/test_fixtures.py`: 5 tests (integration fixture validation)
- `legacy_system/tests/test_baseline_measurements.py`: 5 tests (baseline collection and failure verification)
