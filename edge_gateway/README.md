# Edge Gateway

## Application skeleton (M2-02)

From the repository root:

```bash
uv sync --frozen
uv run edge-gateway
```

The equivalent module command is `uv run python -m edge_gateway.app`.
The server uses configured `HOST`/`PORT` (default `0.0.0.0:8000`). Uvicorn
manages signals and runs the lifespan shutdown hook, with a five-second
graceful-shutdown timeout. Importing the module does not load configuration or
start a server. Invalid configuration prevents startup with a sanitized error.
`LOG_LEVEL` must be a recognized Python logging level at application startup.

| Route | Current behavior |
| --- | --- |
| `GET /health` | `200 {"status":"ok"}` while the application is running |
| `GET /ready` | `503 SERVICE_UNAVAILABLE` pending the operational readiness task |
| `POST /api/v1/measurements` | Invalid JSON → `400`; invalid schema/domain values → `422`; duplicate/out-of-order → `409`; `202` only after confirmed Cloud acceptance; unavailable delivery → `503` |
| `GET /metrics` | Prometheus text with bounded `gateway_service_info` and PQC counters. `gateway_pqc_fallback_total` stays 0 |

M2-12 connects validation, sequence tracking, normalization, correlation, and
selected transport delivery for roadmap Phase 3 / Member 2 Gate A. M2-13 now
constructs the baseline HTTP client automatically for explicit
`SECURITY_MODE=classical`; M2-14 adds its bounded retry loop. `create_app` still
accepts transport dependencies for tests and secure-mode composition. Readiness
remains unavailable pending M2-30/M2-31; it does not depend on an active secure
session. There is no plaintext fallback.

`create_app(load_config(mapping))` supports isolated test configuration.
Routes obtain settings through `get_config`, which tests can replace with
FastAPI's `app.dependency_overrides`. Lifespan initializes process state and
logging and clears the running flag on shutdown. Cloud clients and session
resources can be integrated into that lifecycle in their owning tasks.

Run application tests from the root with:

```bash
uv run pytest edge_gateway/tests/test_gateway_app.py
```

## Legacy request model (M2-03)

`edge_gateway.models.LegacyMeasurement.from_dict(payload)` parses an already
decoded JSON object containing exactly `device_id`, `temperature_c`,
`humidity_pct`, `timestamp`, and `sequence_number`. Missing or extra fields,
incorrect types, and nonfinite sensor numbers raise `LegacyMeasurementSchemaError`.
Numeric strings and booleans are not coerced into numbers. Timestamps must be
ISO-8601 strings with an explicit UTC timezone; internally they are datetimes.
`to_dict()` returns the five wire fields with a UTC `Z` timestamp.

The model is immutable and independently owned by Gateway, with no imports from
Legacy or Cloud. It checks schema only: non-empty device IDs, sensor ranges,
and nonnegative sequences are checked separately by M2-05 domain validation. Parsing a model does
not mean a measurement has been accepted. M2-04 integrates this schema at the
HTTP boundary; valid input proceeds through the M2-12 pipeline described below.
Timestamp serialization uses Python datetime microsecond precision.

## Schema validation (M2-04)

`edge_gateway.validation.parse_legacy_measurement(body)` decodes JSON and then
uses the M2-03 request model. Malformed or empty bodies, invalid encoding, and
non-JSON constants (`NaN`, `Infinity`) produce `400 INVALID_JSON`. Parsed JSON
with missing/extra fields, wrong types, or an invalid timestamp produces
`422 INVALID_MEASUREMENT`. Both responses use the shared structured error body
and omit payload values and parser details. Invalid requests make no Cloud calls.

Domain bounds are checked separately by M2-05; M2-12 then performs sequencing,
normalization, and delivery through the selected transport.

```bash
uv run pytest edge_gateway/tests/test_gateway_validation.py
```

## Domain validation (M2-05)

After parsing, `edge_gateway.validation.validate_legacy_measurement(measurement)`
checks temperature in `[-40, 85]`, humidity in `[0, 100]`, sequence number `>= 0`,
and a non-empty device ID (whitespace-only IDs are rejected). It returns the same
immutable model without trimming IDs or modifying values. These are protocol
bounds, so values outside the simulator's normal range, such as `-25` °C, are valid.

The existing model enforces ISO-8601 timestamps with an explicit UTC timezone;
invalid dates, timezone-less timestamps, and non-UTC offsets return `422`.
Domain failures raise `LegacyMeasurementDomainError` and map to the same sanitized
`422 INVALID_MEASUREMENT` response as schema failures, before any Cloud call.
Sequence ordering and duplicate detection use the M2-10 tracker shared across
requests by the M2-12 processor.

## Application errors (M2-06)

`edge_gateway.errors.GatewayErrorCode` defines fixed public messages and status
codes. Application exception handlers always return
`{"error": {"code": "...", "message": "..."}}` without exception details.

| Error code | HTTP status | Meaning |
| --- | --- | --- |
| `INVALID_JSON` | 400 | Unparseable JSON/body syntax |
| `INVALID_MEASUREMENT` | 422 | Schema or domain validation failed |
| `DUPLICATE_SEQUENCE` | 409 | Duplicate sequence rejected |
| `OUT_OF_ORDER_SEQUENCE` | 409 | Older sequence rejected |
| `CLOUD_UNAVAILABLE` | 503 | Cloud/secure delivery unavailable after its retry policy |
| `INTERNAL_ERROR` | 500 | Unexpected application failure |
| `SERVICE_UNAVAILABLE` | 503 | Operational readiness placeholder |

Later sequence and transport stages can raise `GatewayError(code)` once their
own policies determine a failure. M2-06 defines their error contracts only;
it does not add sequence tracking, retries, or Cloud delivery. Existing parser
and domain exceptions map to their fixed validation responses. Unexpected
exceptions receive a generic JSON `500`; the application handler logs only
`gateway_internal_error`, without exception text or traceback.

```bash
uv run pytest edge_gateway/tests/test_gateway_errors.py edge_gateway/tests/test_gateway_validation.py
```

## Canonical measurement model (M2-07)

`edge_gateway.models.CanonicalMeasurement` is an immutable Gateway-owned model
with exactly seven fields: `device_id`, `temperature_c`, `humidity_pct`,
`measured_at`, `sequence_number`, `received_at`, and `gateway_id`.
Both timestamps must be explicit UTC datetimes. Numbers must be finite, and
booleans/numeric strings are not coerced. Invalid types raise
`CanonicalMeasurementSchemaError` with no supplied values in the message.
`to_dict()` returns an independent JSON-ready dictionary with UTC `Z` timestamps
at Python datetime microsecond precision.

The model requires all values explicitly. M2-08 constructs it from the
validated Legacy measurement, mapping `timestamp` to `measured_at` and supplying
the Gateway current UTC time as `received_at` plus configured `GATEWAY_ID`.
Domain rules remain in the existing validation stage. No request ID, session,
crypto, or Cloud storage metadata belongs in this model. It does not import the
Legacy or Cloud packages, read configuration, consult a clock, or perform delivery.

```bash
uv run pytest edge_gateway/tests/test_gateway_canonical_model.py
```

## Normalization (M2-08)

`edge_gateway.normalization.normalize(legacy_measurement, *, gateway_id, received_at)`
maps a validated Legacy measurement to `CanonicalMeasurement`. It preserves the
device ID, temperature, humidity, and sequence exactly, maps `timestamp` to
`measured_at`, and adds the supplied Gateway metadata. It does not trim IDs,
round numbers, convert units, or mutate the input.

The caller supplies `config.gateway_id` and the Gateway current UTC receipt time
as `received_at`. Explicit inputs keep the mapping deterministic and avoid
environment or clock access inside normalization. Canonical model validation
rejects invalid metadata types and timestamps without an explicit UTC timezone.
The M2-12 processor calls normalization after schema/domain validation and
sequence-policy acceptance, with the UTC receipt time captured by the route.

```bash
uv run pytest edge_gateway/tests/test_gateway_normalization.py
```

## Request/correlation IDs (M2-09)

`edge_gateway.correlation.create_request_id()` creates a fresh `req-<UUID4>`
and logs it through the Gateway logger, both in the message and as a structured
`request_id` attribute. It takes no measurement data or incoming header value.
Call once after validation and sequence-policy acceptance, then keep the same ID
for delivery retries and session recovery. IDs are public tracing context, not
secrets, key material, or metrics labels.

`baseline_headers(request_id)` returns `{"X-Request-ID": request_id}` for the
baseline Cloud request. Pass the same ID separately to the existing secure
envelope builder, which authenticates it through AAD. Canonical measurement
serialization remains unchanged and contains no request ID.

M2-12 now creates the ID once and passes it separately to the processing hook
and selected transport. The baseline HTTP header remains M2-13 responsibility.
Tests construct baseline HTTP requests without sending them and exercise the
existing secure envelope to verify context propagation and authentication.

```bash
uv run pytest edge_gateway/tests/test_gateway_correlation.py
```

## Sequence tracker (M2-10)

`edge_gateway.sequence.SequenceTracker.check_and_update(device_id, sequence_number)`
tracks the last valid sequence accepted per device in memory. Share one tracker
across requests and call it after schema/domain validation, before Cloud delivery.
The check and update use one lock. First values (including zero) and increments
are accepted; gaps advance state and emit `sequence_gap_detected` with device and
sequence context. Equal values raise `GatewayError(DUPLICATE_SEQUENCE)` and lower
values raise `GatewayError(OUT_OF_ORDER_SEQUENCE)`, using the existing `409`
error definitions. Rejections leave state unchanged.

State describes Gateway acceptance, not Cloud persistence. There is no rollback
operation; restarting the process loses history. M2-10 provides the standalone
tracker; M2-11 documents and tests its state lifetime and delivery boundary below.

```bash
uv run pytest edge_gateway/tests/test_gateway_sequence.py
```

## Sequence-state design (M2-11)

One Gateway process should own one `SequenceTracker`, shared across its requests.
Its private dictionary stores the last valid accepted sequence for each device;
creating a tracker for every request would lose duplicate protection. A fresh
process starts with empty history. There is no disk persistence or coordination
between workers, so this design assumes a single Gateway process.

The caller must apply this order:

1. Parse and validate the Legacy measurement's schema and domain values.
2. Call `check_and_update(device_id, sequence_number)` to check and commit state.
3. Continue processing and attempt Cloud delivery after the method returns.

For example, accepting sequence `10` immediately commits `10`. A later Cloud
timeout or connection failure leaves that value unchanged. A Legacy retry of
`10` then raises `409 DUPLICATE_SEQUENCE`. Gateway-to-Cloud retries and Cloud
idempotency are separate from this Legacy-side state.

The existing lock covers the lookup, comparison, and update as one operation.
It is released before downstream I/O. Concurrent equal values have exactly one
winner. For different values, scheduling can affect which requests are accepted,
but state never moves backward and finishes at the highest accepted value.
A pending Cloud request does not block another sequence update, and its failure
must not undo a newer accepted value.

The sequence tests cover restart-equivalent instance isolation, simulated Cloud
failures after commit, another update during pending delivery, and concurrent
equal/different sequences, alongside the M2-10 policy cases. These are component
tests using delivery stubs. M2-12 adds HTTP route tests with transport stubs that
verify commit timing, concurrent requests, and failure retention. Real Cloud
integration and application metrics remain separate tasks.
## Legacy measurement endpoint (M2-12)

`POST /api/v1/measurements` captures UTC receipt time, parses JSON, validates
schema and domain, then delegates to `MeasurementProcessor`. Each application
owns one processor and one in-memory `SequenceTracker`. Processing order is:

```text
validate → check/commit sequence → normalize → create request_id
→ optional processing hook → selected Cloud transport → interpret acceptance
```

Composition supplies `baseline_transport` and/or `secure_transport` to
`create_app`. The existing `CloudDispatch` selects using `SECURITY_MODE`.
Transports expose async `send` with the existing dispatch keyword arguments.
They own retries and return an object with `status` (`accepted` or
`already_accepted`) and a non-empty string `record_id` after confirmed Cloud
acceptance. The secure transport already returns this shape. Missing transport,
invalid acceptance, timeout/connection failures, and classified secure delivery
failures return `503 CLOUD_UNAVAILABLE`; baseline adapters can raise
`GatewayError(CLOUD_UNAVAILABLE)` after bounded retries. Unexpected errors return
sanitized `500 INTERNAL_ERROR`. The route performs no extra retry loop.

Only confirmed delivery returns `202 {"status":"accepted"}`. Cloud record IDs
and transport details are not exposed to Legacy. The optional async
`processing_hook(canonical, request_id)` runs after sequence commit and before
Cloud delivery; no hook is active by default. Concrete processing fault modes
remain M2-19 onward. Exceptions from the hook use the existing safe error mapping.

A failed delivery or processing hook never rolls sequence state back. For
example, sequence `10` followed by a Cloud failure returns `503`; resending `10`
returns `409 DUPLICATE_SEQUENCE` without another Cloud call. This can lose a
measurement during an outage because the Gateway has no delivery queue. Cloud
idempotency separately protects Gateway-to-Cloud retransmissions. Restart loses
Gateway sequence history. Pending Cloud I/O does not hold the sequence lock.

Tests use injected transports, including a blocked asynchronous delivery, and
verify both modes, exact canonical fields, separate unique IDs, invalid input
without side effects, sequence errors/gaps, safe failures, and no fallback.
They do not claim real baseline Cloud persistence or baseline E2E readiness.

```bash
uv run pytest edge_gateway/tests/test_gateway_measurements.py
```

## Baseline Cloud client (M2-13)

`edge_gateway.cloud.baseline.BaselineCloudClient` is used only when
`SECURITY_MODE=classical` is explicitly configured. It serializes the exact
seven-field `CanonicalMeasurement` as compact JSON, posts it to
`{CLOUD_URL}/api/v1/baseline/measurements`, applies `CLOUD_TIMEOUT_SECONDS`, and
puts the separately created request ID only in `X-Request-ID`. A successful
Cloud `202` response is normalized to `BaselineAcceptance(status, record_id)`;
only `accepted` and `already_accepted` with a non-empty record ID qualify.

The client sends one attempt in M2-13 and classifies failures for M2-14:
timeouts, connection/protocol errors, and `500`, `502`, `503`, or `504` are
retryable; redirects, other HTTP responses, and malformed/unexpected `202`
payloads are not. It never follows redirects and never changes the request body
or inserts `request_id` into it. The route converts classified failures to the
existing Legacy-safe `503 CLOUD_UNAVAILABLE`; M2-14 will make retry exhaustion
the normal path to that result. ML-KEM mode never creates or calls this client
after a secure failure.

```bash
uv run pytest edge_gateway/tests/test_baseline_client.py
```

## Transport trust (M3-54)

Docker and the course test environment may use HTTP for Gateway-to-Cloud
communication. Modernized mode demonstrates application-layer ML-KEM-768 key
establishment and AES-256-GCM payload protection. That is a documented
trust-model limitation: ML-KEM does not authenticate the Cloud, and production
TLS, mTLS, PKI, public-key pinning, and signed key distribution are outside
this implementation. Details are in
[docs/transport-trust.md](docs/transport-trust.md).

## Session memory (M3-55)

The Gateway session key stays in process memory. Replacing a session clears the old key buffer and drops that object. Python does not guarantee secure memory zeroization, so that overwrite is not a claim that every copy is gone. Details are in
[docs/session-memory.md](docs/session-memory.md).

## Secure shutdown (M3-56)

When a secure transport is attached, Gateway shutdown stops accepting work, closes that transport's HTTP client, and then clears the in-memory session. The cleanup does not print key material. Process signals and Docker stop stay with the application lifecycle. Details are in
[docs/secure-shutdown.md](docs/secure-shutdown.md).

## Crypto image install (M3-61)

The Gateway crypto dependencies install from the frozen lock as Linux wheels.
`edge_gateway/docker/crypto-image.Dockerfile` is a Python 3.12 bookworm image
with no compiler. It runs `uv sync --frozen --package edge-gateway --no-dev`
and then checks ML-KEM-768, HKDF-SHA-256, and AES-256-GCM. The service image
`edge_gateway/Dockerfile` remains Member 2's task. Details are in
[docs/crypto-image.md](docs/crypto-image.md).

## Clean-container crypto test (M3-62)

`edge_gateway/docker/clean-container.Dockerfile` installs Gateway and Cloud
from the frozen lock, starts Cloud, establishes one ML-KEM session, and stores
one secure measurement. The receiver exists only in that container process.
Details are in [docs/clean-container.md](docs/clean-container.md).

## Configuration

The Gateway loads environment variables once at application startup through
`edge_gateway.config.load_config()`. Invalid configuration raises
`ConfigurationError` and must prevent startup. No other Gateway module should
read its configuration directly from the environment.

| Variable | Default | Validation |
| --- | --- | --- |
| `GATEWAY_ID` | `gateway-001` | Non-empty |
| `HOST` | `0.0.0.0` | Non-empty |
| `PORT` | `8000` | TCP port, 1–65535 |
| `CLOUD_URL` | `http://cloud-service:9000` | Absolute HTTP(S) URL |
| `CLOUD_TIMEOUT_SECONDS` | `3` | Positive number |
| `CLOUD_MAX_RETRIES` | `2` | Integer greater than or equal to zero |
| `SECURITY_MODE` | `classical` | `classical` or `mlkem` |
| `SESSION_TTL_SECONDS` | `300` | Exactly `300` for protocol v1 |
| `PQC_FAILURE_POLICY` | `fail_closed` | `fail_closed` only for protocol v1 |
| `FAILURE_MODE` | `none` | A documented Gateway failure mode |
| `FAILURE_RATE` | `0.0` | Number from 0.0 to 1.0 inclusive |
| `FAILURE_SEED` | empty | Optional deterministic-test seed; empty means unset |
| `LOG_LEVEL` | `INFO` | Non-empty |

`SECURITY_MODE=classical` is the explicitly selected baseline mode. The
`mlkem` setting selects only the supplied secure transport; missing or failed
secure delivery returns `503` without a plaintext fallback.
