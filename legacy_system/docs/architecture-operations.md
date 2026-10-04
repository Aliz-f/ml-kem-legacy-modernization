# Legacy Device Architecture and Operations Guide

This document provides the canonical architectural and operational reference for the **Legacy Device simulator** (`legacy_system/`). It documents the design, internal modules, wire protocol, configuration, failure injection, operational lifecycle, testing architecture, and known limitations.

---

## 1. Purpose and Architectural Role

The Legacy Device simulates an environmental IoT sensor appliance deployed at the physical edge. In this modernization project, it represents the **legacy domain**:
- It transmits periodic environmental measurements (temperature and humidity) to the Edge Gateway using an unencrypted, unauthenticated HTTP/JSON protocol.
- It is intentionally **outside the Post-Quantum Cryptography (PQC) perimeter**. The Legacy Device does not implement or interface with ML-KEM, HKDF, or AES-GCM.
- It serves as a pure outbound HTTP client; it does not listen on any incoming ports or run an HTTP server.
- The component ownership boundary is strictly contained within `legacy_system/` (source under `src/legacy_system/` and tests under `tests/`).

```text
┌─────────────────────────────────┐
│          Legacy Device          │
│  (Simulated IoT Sensor Appliance)│
│                                 │
│  • Config & Fail-fast Startup   │
│  • Deterministic Sensor Sim     │
│  • Safe Failure Injector        │
│  • Bounded HTTP Retrying Client │
│  • Graceful Signal Shutdown     │
└────────────────┬────────────────┘
                 │
                 │ HTTP POST /api/v1/measurements
                 │ (Unauthenticated JSON, Content-Type: application/json)
                 ▼
┌─────────────────────────────────┐
│          Edge Gateway           │
│   (PQC Modernization Boundary)  │
└─────────────────────────────────┘
```

---

## 2. Module Architecture

The component source code resides in `legacy_system/src/legacy_system/` and follows a clean separation of concerns without heavyweight framework dependencies:

```text
legacy_system/src/legacy_system/
├── __init__.py      # Package definition
├── config.py        # Validated runtime configuration dataclass and fail-fast loader
├── sensor.py        # Domain Measurement model and deterministic/stochastic generator
├── failure.py       # FailureInjector producing wire-level anomalies
├── client.py        # GatewayClient HTTP transport using standard library urllib
├── device.py        # DeviceController coordinating the periodic lifecycle loop
└── main.py          # Composition root CLI entry point with logging setup
```

### Module Responsibilities

1. **`config.py` (`Config`, `load_config`, `FailureMode`)**:
   Reads environment variables, validates ranges and types, and produces an immutable, frozen dataclass. Any missing or invalid configuration terminates initialization immediately (`ConfigurationError`).
2. **`sensor.py` (`Sensor`, `Measurement`)**:
   Generates simulated measurements. Maintains the internal monotonic `sequence_number` (starting at 0). Formats UTC ISO-8601 timestamps and serializes valid measurements to dictionaries.
3. **`failure.py` (`FailureInjector`)**:
   Applies test-time corruptions (e.g. invalid fields, corrupt timestamps, sequence tampering) to outbound payloads. **Domain/Payload Separation**: mutates only the outgoing dictionary/JSON string, leaving the underlying domain `Measurement` and `Sensor` state untouched.
4. **`client.py` (`GatewayClient`, `GatewayResult`, `ErrorCategory`)**:
   Wraps `urllib.request.urlopen` with configurable timeouts and bounded exponential retries. Classifies HTTP status codes and socket exceptions into stable outcome structures without leaking exception internals.
5. **`device.py` (`DeviceController`)**:
   Orchestrates the periodic loop. Coordinates sensor reading, optional fault injection, network dispatch, structured logging, and signal handling (`SIGINT`, `SIGTERM`) for zero-data-loss graceful shutdowns.
6. **`main.py` (`main`)**:
   Configures standard library logging formatters, loads settings from `os.environ`, instantiates `DeviceController`, and blocks on the runtime loop. Exits cleanly with status code 0 on termination signals, or non-zero (1) on configuration errors.

---

## 3. Data Model and Wire Contract

### Wire Contract
- **Target Endpoint**: `POST /api/v1/measurements`
- **Headers**: `Content-Type: application/json`
- **Success Status**: `202 Accepted`
- **Encoding**: UTF-8 encoded JSON

### JSON Schema

```json
{
  "device_id": "sensor-001",
  "temperature_c": 21.7,
  "humidity_pct": 42.5,
  "timestamp": "2026-10-04T15:30:00Z",
  "sequence_number": 0
}
```

### Field Definitions

| Field | Type | Rules & Generation Bounds |
|---|---|---|
| `device_id` | `string` | Non-empty ASCII string identifier (e.g. `sensor-001`). |
| `temperature_c` | `float` | Ambient temperature in Celsius. Generated in normal range `[15.0, 30.0]`, rounded to 1 decimal place. |
| `humidity_pct` | `float` | Relative humidity percentage. Generated in normal range `[30.0, 70.0]`, rounded to 1 decimal place. |
| `timestamp` | `string` | ISO-8601 UTC timestamp format `YYYY-MM-DDTHH:MM:SSZ` (e.g. `2026-10-04T12:00:00Z`). |
| `sequence_number` | `integer` | Monotonically increasing counter `>= 0`. Increments by 1 on every generated measurement. |

---

## 4. Configuration Management

The Legacy Device is entirely configured via environment variables.

| Environment Variable | Type | Default | Validation Constraints |
|---|---|---|---|
| `DEVICE_ID` | `str` | `sensor-001` | Must be a non-empty string. |
| `GATEWAY_URL` | `str` | `http://edge-gateway:8000` | Must include an `http://` or `https://` scheme and valid netloc. |
| `SEND_INTERVAL_SECONDS` | `float` | `5.0` | Must be strictly positive (`> 0`). |
| `REQUEST_TIMEOUT_SECONDS` | `float` | `3.0` | Must be strictly positive (`> 0`). |
| `MAX_RETRIES` | `int` | `2` | Must be an integer `>= 0`. |
| `FAILURE_MODE` | `str` | `none` | Must match one of the supported `FailureMode` enum values. |
| `FAILURE_RATE` | `float` | `0.0` | Floating point value bounded within `[0.0, 1.0]`. |
| `FAILURE_SEED` | `int` | `None` (empty) | Optional integer seed for reproducible PRNG sequences. |
| `LOG_LEVEL` | `str` | `INFO` | Must be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |

### Fail-Fast Startup Behavior
If any configuration variable fails validation (e.g. negative timeout, invalid URL scheme, unrecognized failure mode), `load_config()` raises `ConfigurationError`. The application outputs a clear, safe diagnostic to stderr and terminates immediately with exit code 1. It never starts up in a half-configured or degenerate state.

---

## 5. Normal Operation Cycle

When started in normal operational mode (`FAILURE_MODE=none`), the device lifecycle follows a deterministic loop:

1. **Initialization**:
   - Parses configuration.
   - Sets root logger to `LOG_LEVEL` with structured formatting.
   - Instantiates `DeviceController`, initializing `Sensor(sequence_number=0)`.
   - Registers OS signal handlers for `SIGINT` and `SIGTERM`.
   - Emits `event=device_starting` and `event=device_ready`.
2. **Periodic Cycle**:
   - `Sensor.read()` generates a new reading with current UTC timestamp and increments `sequence_number`.
   - Emits `event=measurement_generated` with `device_id` and `sequence_number`.
   - Serializes reading to payload dict and passes through `FailureInjector` (no-op in `none` mode).
   - Dispatches payload via `GatewayClient.send()`.
   - Upon receiving `202 Accepted`, emits `event=measurement_delivered`.
   - Sleeps for `SEND_INTERVAL_SECONDS` using interruptible event waiting (`threading.Event.wait()`).
3. **Shutdown**:
   - Receipt of `SIGINT` or `SIGTERM` trips the stop event.
   - If the controller is sleeping between cycles, it wakes up immediately without waiting for the sleep duration to expire.
   - Emits `event=device_shutting_down`, closes client resources, restores original signal handlers, and exits with code 0.

---

## 6. Retry Semantics and Error Classification

The Gateway HTTP client (`GatewayClient`) enforces strict bounded retries to prevent retry storms while guaranteeing prompt failure propagation.

### Response Classification

| Response / Outcome | Retryable? | Behavior |
|---|---|---|
| `202 Accepted` | No | Request succeeded. Emits `measurement_delivered`. Returns immediately. |
| `400 Bad Request` | No | Malformed JSON syntax on wire. Permanent client error. Does not retry. |
| `409 Conflict` | No | Duplicate or out-of-order sequence rejected by Gateway. Permanent application result. Does not retry. |
| `422 Unprocessable Entity` | No | Schema or domain constraint violation (e.g. missing field, out-of-range value). Permanent validation error. Does not retry. |
| `500 Internal Server Error` | Yes | Server internal fault. Retries up to `MAX_RETRIES`. |
| `502 Bad Gateway` | Yes | Upstream delivery failure at Gateway. Retries up to `MAX_RETRIES`. |
| `503 Service Unavailable` | Yes | Gateway or downstream Cloud temporarily unavailable. Retries up to `MAX_RETRIES`. |
| `504 Gateway Timeout` | Yes | Upstream timeout. Retries up to `MAX_RETRIES`. |
| Connection Refused / URLError | Yes | Network partition or Gateway process offline. Retries up to `MAX_RETRIES`. |
| Socket / Read Timeout | Yes | Gateway failed to respond within `REQUEST_TIMEOUT_SECONDS`. Retries up to `MAX_RETRIES`. |

### Backoff Algorithm
When an outcome is marked `retryable=True`, the client pauses before retrying using an exponential backoff schedule:
$$\text{delay} = 2^{\text{attempt} - 1} \quad \text{seconds}$$
For default `MAX_RETRIES=2`:
- Initial attempt (attempt 1): sends immediately.
- Attempt 2 (retry 1): waits 1 second ($2^0$).
- Attempt 3 (retry 2): waits 2 seconds ($2^1$).
- If attempt 3 fails, the retry budget is exhausted. The client logs `event=gateway_request_failed` and returns a failed `GatewayResult`.

### Sequence Number Preservation
When a measurement delivery fails (even after all retries are exhausted), **the device never rolls back its sequence number**. The sequence number advances monotonically on every generated measurement. This guarantees the Gateway sequence tracker never observes historical sequence numbers due to local transient network errors.

---

## 7. Failure Simulation and Safety Safeguards

To test downstream resilience (Edge Gateway and Cloud Service), the Legacy Device features a configurable failure injection engine (`FailureInjector`).

### Supported Failure Modes

| Mode | Wire Transformation | Expected Gateway Response |
|---|---|---|
| `none` | No modification. Normal measurement payload. | `202 Accepted` |
| `invalid_temperature` | Sets `temperature_c = 150.0` (outside domain bounds). | `422 Unprocessable Entity` |
| `invalid_humidity` | Sets `humidity_pct = -10.0` (outside domain bounds). | `422 Unprocessable Entity` |
| `missing_field` | Deletes a required key (`timestamp` or `temperature_c`). | `422 Unprocessable Entity` |
| `invalid_timestamp` | Replaces timestamp with malformed string `"not-a-timestamp"`. | `422 Unprocessable Entity` |
| `duplicate_sequence` | Repeats the previous measurement's sequence number. | `409 Conflict` |
| `out_of_order_sequence` | Decrements the sequence number (`sequence_number - 2`). | `409 Conflict` |
| `random` | Randomly chooses one of the active corruption modes per cycle. | `409` or `422` depending on choice |

### Architectural Safety Safeguards
1. **Wire Purity**: The failure injector never injects simulation flags, debug headers (e.g. `X-Simulation`), or query parameters into the wire request. Downstream components (Gateway and Cloud) treat every request purely on its payload merits without knowing if an error was simulated or organic.
2. **Domain/Payload Separation**: The underlying domain `Measurement` object remains valid. Mutations only occur on the serialized dictionary or wire representation during dispatch.
3. **Internal State Isolation**: Simulating a duplicate or out-of-order sequence does not alter the internal `Sensor._sequence_number` state. The sensor's actual generator continues incrementing monotonically.
4. **Isolated Pseudo-Randomness**: The failure injector uses an independent `random.Random` instance seeded via `FAILURE_SEED`. It never shares state with cryptographic PRNGs (`secrets` or OS entropy) used elsewhere in the modernization system.

---

## 8. Logging and Observability

The Legacy Device utilizes Python's standard `logging` library. All operational events use structured key-value formats for easy ingestion and parsing:

```text
event=device_starting component=legacy_system device_id=sensor-001
event=device_ready component=legacy_system device_id=sensor-001
event=measurement_generated component=legacy_system device_id=sensor-001 sequence_number=0
event=measurement_delivered component=legacy_system device_id=sensor-001 sequence_number=0 status_code=202 attempt=1
event=gateway_retry component=legacy_system device_id=sensor-001 sequence_number=1 attempt=1 status_code=503 error_category=http
event=device_shutting_down component=legacy_system device_id=sensor-001
```

### Privacy and Security Hygiene
- **Zero Secret Exposure**: The Legacy Device handles no cryptographic secrets, private keys, session tokens, or credentials.
- **Sanitized Values**: Measurements logged do not dump raw floating-point sensor values, private headers, or internal execution frames.
- **Safe Field Formatting**: Only bounded alphanumeric tokens and integers are logged.

---

## 9. Testing Strategy

The `legacy_system` test suite provides 100% component-level coverage across all functional areas:

| Test Module | Coverage Scope |
|---|---|
| [`test_config.py`](../tests/test_config.py) | Environment loading, default values, bounds validation, and fail-fast startup errors. |
| [`test_sensor.py`](../tests/test_sensor.py) | Reading bounds, precision rounding, UTC timestamp format, and monotonic sequence increments. |
| [`test_failure.py`](../tests/test_failure.py) | All `FailureMode` transformations, deterministic seed reproducibility, and rate gating. |
| [`test_failure_safety.py`](../tests/test_failure_safety.py) | Wire purity (no simulation flags), domain model immutability, and state sequence preservation. |
| [`test_failure_simulation.py`](../tests/test_failure_simulation.py) | Real HTTP client/server loop validation verifying Gateway-equivalent responses (409/422). |
| [`test_client.py`](../tests/test_client.py) | Timeout handling, socket exceptions, status code classification, and exponential backoff retry math. |
| [`test_network_failures.py`](../tests/test_network_failures.py) | Socket disconnects, connection refusal, half-open sockets, and transient server faults. |
| [`test_device.py`](../tests/test_device.py) | Controller lifecycle loop, signal interception (`SIGINT`/`SIGTERM`), and graceful resource release. |
| [`test_multi_device.py`](../tests/test_multi_device.py) | Concurrent multi-device simulation and independent sequence numbering. |
| [`test_docker_assets.py`](../tests/test_docker_assets.py) | Dockerfile instructions, non-root user verification, STOPSIGNAL compliance, and Compose service mapping. |
| [`test_static_quality.py`](../tests/test_static_quality.py) | AST-based static checks for zero `breakpoint()`/`pdb`/debug prints, no PEM keys, no `.env` files, and clean component boundaries. |
| [`test_baseline_measurements.py`](../tests/test_baseline_measurements.py) | 100-sample baseline benchmark measuring round-trip latency, payload sizes, and delivery rates. |

---

## 10. Docker Container Behavior

The Legacy Device is containerized using Docker and managed via Docker Compose:

- **Base Image**: `python:3.12-slim-bookworm` using pinned Astral `uv:0.12.19`.
- **Packaging**: Container build executes `uv sync --frozen --package legacy-system --no-dev --no-editable`.
- **Security**: Runs under non-root unprivileged user `USER 10001:10001`.
- **Network Profile**: Pure outbound client. **Zero exposed ports** (`EXPOSE` is absent). Does not bind or listen on network sockets.
- **Process Orchestration & Signals**:
  - `STOPSIGNAL SIGTERM` ensures Docker stop commands send `SIGTERM` directly to `python -m legacy_system.main`.
  - The process catches `SIGTERM` and shuts down within milliseconds, avoiding forceful `SIGKILL` timeouts.
- **Docker Compose Topology**:
  - Defined under service `legacy-device` in root `docker-compose.yml`.
  - Configured with `depends_on: edge-gateway: condition: service_healthy` so it only attempts delivery after the Gateway is ready.
  - Gateway destination configured via internal container DNS: `GATEWAY_URL: http://edge-gateway:8000`.

---

## 11. Known Limitations and Operational Boundaries

The Legacy Device simulation reflects realistic constraints of older embedded equipment:
1. **In-Memory Sequence State**: Sequence numbers are stored in process memory. A process restart resets the sequence counter back to `0`. (Downstream Gateways reject sequence `0` as out-of-order if higher sequences were previously recorded; see Gateway technical debt).
2. **No Persistent Store-and-Forward Buffer**: If the Edge Gateway is down for an extended period, failed measurements are dropped after `MAX_RETRIES` are exhausted. Unsent measurements are not persisted to local non-volatile storage.
3. **No Transport Encryption or Authentication**: The device sends cleartext HTTP payloads without TLS, mutual client certificates, or API tokens. This reflects an unmodernized legacy sensor environment.
4. **Fixed Simple Retry Backoff**: Retries use deterministic exponential backoff without jitter. In multi-device deployments experiencing a shared network outage, synchronized retries may occur.

---

## 12. Technical Debt and Decision Tracking

For full registers of architectural decisions and accepted technical debt:
- **AI Decision Register**: [`legacy_system/docs/ai-decisions.md`](ai-decisions.md) (Task M1-24) — tracks all accepted, modified, and rejected AI proposals.
- **Technical Debt Register**: [`legacy_system/docs/technical-debt.md`](technical-debt.md) (Task M1-25) — tracks accepted legacy limitations, operational risks, and future modernization improvements.
- **Project-Wide Technical Debt**: [`docs/technical-debt.md`](../../docs/technical-debt.md) — consolidates cross-component debt across Legacy, Gateway, and Cloud.
