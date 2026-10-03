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
| `GET /ready` | `200 {"status":"ready","security_mode":"..."}` when the configured transport is initialized; otherwise `503 SERVICE_UNAVAILABLE` |
| `POST /api/v1/measurements` | Invalid JSON → `400`; invalid schema/domain values → `422`; duplicate/out-of-order → `409`; `202` only after confirmed Cloud acceptance; unavailable delivery → `503` |
| `GET /metrics` | Prometheus text with application, Cloud-attempt, injection, and PQC metrics. `gateway_pqc_fallback_total` stays 0 |

M2-12 connects validation, sequence tracking, normalization, correlation, and
selected transport delivery for roadmap Phase 3 / Member 2 Gate A. M2-13 now
constructs the baseline HTTP client automatically for explicit
`SECURITY_MODE=classical`; M2-14 adds its bounded retry loop. `create_app` still
accepts transport dependencies for tests and secure-mode composition. M2-29
through M2-31 provide liveness and local transport readiness. Secure readiness
does not establish or require an active session and does not probe Cloud. There
is no plaintext fallback.

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
| `SERVICE_UNAVAILABLE` | 503 | Gateway is not running or its configured transport is not initialized |

Later sequence and transport stages can raise `GatewayError(code)` once their
own policies determine a failure. M2-06 defines their error contracts only;
it does not add sequence tracking, retries, or Cloud delivery. Existing parser
and domain exceptions map to their fixed validation responses. Unexpected
exceptions receive a generic JSON `500`; the application handler logs only
`gateway_internal_error`, without exception text or traceback.

```bash
uv run pytest edge_gateway/tests/test_gateway_errors.py edge_gateway/tests/test_gateway_validation.py
```

## Gateway response mapping (M2-15)

The Legacy endpoint has one frozen outcome-to-response mapping. It does not
pass through Cloud HTTP statuses, Cloud error codes, secure-session details, or
Python exception text. Cloud and secure delivery failures are intentionally
reduced to the same Legacy-safe unavailable result.

| Gateway outcome | Legacy HTTP response | Stable code |
| --- | ---: | --- |
| Confirmed Cloud acceptance, including Cloud idempotent acceptance | `202` | `{"status":"accepted"}` |
| Malformed or unparseable Legacy body | `400` | `INVALID_JSON` |
| Parsed Legacy schema/domain failure | `422` | `INVALID_MEASUREMENT` |
| Duplicate sequence | `409` | `DUPLICATE_SEQUENCE` |
| Lower sequence | `409` | `OUT_OF_ORDER_SEQUENCE` |
| Baseline retry exhaustion, baseline rejection, timeout, connection failure, secure session/PQC failure | `503` | `CLOUD_UNAVAILABLE` |
| Unexpected Gateway error | `500` | `INTERNAL_ERROR` |

The route returns `202` only after its selected Cloud transport confirms either
`accepted` or `already_accepted` with a record ID. `already_accepted` remains a
Cloud idempotency detail; Legacy receives the unchanged accepted response.
Baseline and secure errors both become `503` because the Legacy interface does
not expose the Gateway-to-Cloud transport or cryptographic boundary. Secure
mode remains fail closed: this mapping does not send a baseline request after a
secure failure. Tests exercise the complete table with transport doubles.

```bash
uv run pytest edge_gateway/tests/test_gateway_response_mapping.py
```

## Baseline Gateway–Cloud integration (M2-16)

The integration test sends the M2-16 canonical fixture through the production
`BaselineCloudClient` to a live loopback Cloud server in `SECURITY_MODE=classical`
with a temporary file-backed SQLite database. It verifies the exact seven-field
JSON body, `X-Request-ID: req-test-001` in the received request and Cloud logs,
unchanged measurement values, `received_at` mapping to `gateway_received_at`,
and Cloud-generated `cloud_received_at` and `record_id`. List/detail queries and
a fresh SQLite connection after Cloud shutdown confirm persistence.

Repeated delivery returns `already_accepted` with the original record ID and
one row. Real Cloud validation rejection is non-retryable; a SQLite write failure
exhausts the configured two retries with identical requests and no stored row.
The test replaces only retry sleeping, so failures do not add backoff delays.

Run from the workspace root (requires permission to bind loopback sockets):

```bash
uv run pytest edge_gateway/tests/test_gateway_baseline_integration.py -q
```

This covers the Member 2 client boundary and complements the Cloud-local
serializer harness. The M2-17 tests below extend it through the Legacy boundary.
Cloud health and dependency readiness both return `200`. Gateway readiness
returns `200` after its configured local transport is initialized; it does not
probe Cloud connectivity.

## First full baseline E2E support (M2-17)

The same test module now sends a deterministic Legacy `Measurement` through its
production serializer and `GatewayClient`, a live Gateway configured with
`SECURITY_MODE=classical`, the production baseline Cloud client, and a live Cloud
with temporary file-backed SQLite. Both HTTP boundaries use loopback sockets;
the Gateway creates its own transport, sequence tracker, and request IDs.

The roadmap fixture (`sensor-test`, sequence `1`, `22.5` °C, `44.0` %,
`2026-09-21T12:00:00Z`) and domain-boundary cases verify unchanged values,
`timestamp` → `measured_at`, added Gateway ID and receipt time, and exact
`received_at` → `gateway_received_at` mapping. Fractional timestamp precision is
preserved. Correlation reaches Cloud through `X-Request-ID` and its acceptance
log, outside the seven-field canonical body. Cloud list/detail queries immediately
after Legacy `202`, plus a fresh SQLite connection after shutdown, verify storage.

Negative coverage verifies that invalid Legacy data returns `422` without
forwarding, a real SQLite write failure returns `503` rather than acceptance,
and duplicate/out-of-order sequences return `409` even after failed delivery.
A subsequent valid sequence gap succeeds. Retries are disabled in these E2E
cases to isolate the response and sequence policy; M2-14/M2-16 cover bounded
Cloud retries.

Run the M2-17 cases from the workspace root:

```bash
uv run pytest edge_gateway/tests/test_gateway_baseline_integration.py -k 'legacy_to_sqlite or baseline_e2e' -q
```

This is Member 2's transformation evidence for the Phase 5 baseline milestone.
Member 5 retains ownership of shared E2E orchestration, deployment, and baseline
freeze coordination. These tests use the deterministic send path, not the
continuous sensor loop or Docker Compose. Both services' `/health` endpoints
return `200`; both services' `/ready` endpoints also return `200` after their
local dependencies initialize. Compose currently has no service definitions,
so this does not establish container deployment readiness.

The current Gateway `/ready` response reports local application and transport
readiness. It deliberately does not establish an ML-KEM session or contact
Cloud, so a later measurement can still receive `503 CLOUD_UNAVAILABLE` if
Cloud cannot be reached. See [Gateway operations](docs/gateway-operations.md).

## Baseline Gateway measurements (M2-18)

A small collector in the existing live integration test records Legacy request
counts, accepted/rejected/failed outcomes, Gateway request duration, baseline
Cloud delivery and attempt latency, actual retries, and canonical HTTP body
size. Production behavior is unchanged. Run from the workspace root:

```bash
uv run pytest edge_gateway/tests/test_gateway_baseline_integration.py -k baseline_gateway_measurements -q -s
```

Each scenario prints an `M2-18` JSON report. See
[the measurement method and recorded sample](docs/baseline-measurements.md)
for timing boundaries, workload, configuration, and limitations. This supplies
Member 2 evidence for the Phase 5 baseline milestone; Member 5 retains ownership
of the shared benchmark harness, deployment, and baseline freeze.

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
integration is covered by M2-16/17; application metrics are documented in
[PR9 metrics and operations](docs/gateway-pr9.md).
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
Cloud delivery. Configured application faults run at this boundary before the
optional hook; faults are disabled by default. Exceptions use the existing safe
error mapping.

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

## Secure transport integration (M2-26 through M2-28)

The application processor uses a mode-independent `CloudTransport` contract.
`CloudDispatch` selects the classical or ML-KEM path once from validated
configuration and never falls back to plaintext after a secure failure. The
Legacy endpoint and payload remain unchanged in both modes. See
[the integration note](docs/secure-transport-integration.md) for ownership,
behavior, and live compatibility evidence.

## Baseline Cloud client (M2-13)

`edge_gateway.cloud.baseline.BaselineCloudClient` is used only when
`SECURITY_MODE=classical` is explicitly configured. It serializes the exact
seven-field `CanonicalMeasurement` as compact JSON, posts it to
`{CLOUD_URL}/api/v1/baseline/measurements`, applies `CLOUD_TIMEOUT_SECONDS`, and
puts the separately created request ID only in `X-Request-ID`. A successful
Cloud `202` response is normalized to `BaselineAcceptance(status, record_id)`;
only `accepted` and `already_accepted` with a non-empty record ID qualify.

The M2-14 retry policy treats timeouts, connection/protocol errors, and `500`,
`502`, `503`, or `504` as retryable. Redirects, other HTTP responses, and
malformed/unexpected `202` payloads are permanent. `CLOUD_MAX_RETRIES` is the
number of additional ordinary transport attempts, defaulting to `2` for at most
three sends. The frozen backoff is one second before the second attempt and two
seconds before the third; no delay follows the final failure. Each retry uses
the exact same already-serialized body and `X-Request-ID`. The route converts
exhausted or permanent delivery failures to existing Legacy-safe `503
CLOUD_UNAVAILABLE`. ML-KEM mode never creates or calls this client after a
secure failure; its bounded session recovery remains separate.

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

## Crypto AI-history (M3-64)

Generated Gateway crypto code stays untrusted until a human security review.
Significant crypto changes follow the repository AI-history workflow: start,
implementation, tests, output, human review, and a separate final verification.
Details are in [docs/ai-history.md](docs/ai-history.md).

## Crypto review checklist (M3-65)

Generated Gateway crypto stays untrusted until a human reviews it. A passing
test suite does not replace this checklist. The checks cover the maintained
ML-KEM library, HKDF, sessions, AES-GCM, retry, the missing replay window,
fail-closed behavior, and the Legacy boundary. Details are in
[docs/crypto-review-checklist.md](docs/crypto-review-checklist.md).

## Crypto AI decisions (M3-66)

Generated crypto proposals are recorded as accepted, modified, and rejected.
ML-KEM stays a key-establishment step, the session key stays the frozen HKDF
call, and an ordinary timeout resends the envelope already built. Details are
in [docs/ai-decisions.md](docs/ai-decisions.md).

## Security documentation (M3-67)

The Gateway security facts stay in the frozen Edge Gateway design and the
shared protocol specification. This note points at those sections. It does not replace the frozen architecture. Details are in
[docs/security.md](docs/security.md).

## Security technical debt (M3-68)

The course system keeps simplified public-key trust, in-memory sessions, an
ephemeral Cloud key, and no cryptographic replay window. The register records
those limits and their future improvements. It does not add those future controls.
Details are in [docs/technical-debt.md](docs/technical-debt.md).

## Threat model (M3-69)

The Gateway threat model covers tampered ciphertext, a bad session, ML-KEM
ciphertext changes, public-key substitution, secret logging, envelope replay,
downgrade, Cloud unavailability, and a session race. It does not add a replay window.
Details are in [docs/threat-model.md](docs/threat-model.md).

## Mode evaluation (M3-70)

One local sample compares an equivalent four-measurement workload in classical
mode and in mlkem mode. The first secure request is reported separately. The
sample does not rank the modes. Details are in
[docs/mode-evaluation.md](docs/mode-evaluation.md).

## PQC observability (M3-71)

One local run shows the handshake counter move from 0 to 1, stay at 1 while
later measurements reuse the session, and move to 2 after the session expires.
The scrape does not include a session identifier. Details are in
[docs/pqc-observability.md](docs/pqc-observability.md).

## Corrupted ciphertext (M3-72)

One local run seals a valid measurement, corrupts the outgoing ciphertext copy,
and records Cloud's authentication rejection. It does not store the rejected measurement.
Details are in [docs/corrupt-ciphertext.md](docs/corrupt-ciphertext.md).

## ML-KEM handshake failure (M3-73)

One local run stops session establishment before a public key is fetched.
The Gateway returns failure and the handshake-failure counter increments.
It does not call the baseline endpoint.
Details are in [docs/mlkem-handshake-failure.md](docs/mlkem-handshake-failure.md).

## Cloud crypto review (M3-74)

One review of Member 4's Cloud crypto compares the implementation with the
frozen session-key contract. It does not change the Cloud protocol.
Details are in [docs/cloud-crypto-review.md](docs/cloud-crypto-review.md).

## Member 2 integration review (M3-75)

One review of the Gateway integration checks modernized dispatch, request
correlation, fail-closed delivery, and session recovery. It does not change the Gateway protocol.
Details are in [docs/member2-integration-review.md](docs/member2-integration-review.md).

## Dependency and security review (M3-76)

One review of `uv.lock` and the crypto source checks for unnecessary,
unmaintained, or duplicate crypto packages and unsafe low-level use.
Details are in [docs/dependency-review.md](docs/dependency-review.md).

## Static and code-quality verification (M3-77)

Before a crypto pull request, run the Gateway tests, Ruff, the AI-history
check, and the secure integration tests, then inspect the diff for secret
logging, key files, debug prints, and `.env` values.
Details are in [docs/static-checks.md](docs/static-checks.md).

## Final secure-transport review (M3-78)

One review checks every item of the frozen M3-78 checklist against the
current Gateway and Cloud code, tests, and documentation before freeze.
Details are in [docs/final-secure-transport-review.md](docs/final-secure-transport-review.md).

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
| `FAILURE_DELAY_SECONDS` | `2` | Processing delay, finite and between 0 and 30 seconds |
| `FAILURE_RATE` | `0.0` | Number from 0.0 to 1.0 inclusive |
| `FAILURE_SEED` | empty | Optional deterministic-test seed; empty means unset |
| `LOG_LEVEL` | `INFO` | Non-empty |

`SECURITY_MODE=classical` is the explicitly selected baseline mode. The
`mlkem` setting selects only the supplied secure transport; missing or failed
secure delivery returns `503` without a plaintext fallback.

## Application failure injection (M2-19 through M2-25)

`edge_gateway.failure.FailureInjector.from_config(config)` builds a local
selector using `FAILURE_MODE`, `FAILURE_RATE`, and optional `FAILURE_SEED`.
Defaults (`none`, `0.0`, empty seed) disable selection. Rate zero never selects;
rate one always selects an eligible fault; intermediate rates use one probability
check per eligible call. A seed reproduces decisions for the same call order.
Concurrent request scheduling can change which request receives a decision.

`select()` returns one mode or `None`. Application modes are `processing_error`,
`processing_delay`, `cloud_timeout`, `cloud_unavailable`, and `drop_message`.
`random` chooses only from these modes, with a stable candidate order. Pass
`allowed` to restrict selection to implemented/applicable boundaries. Keep one
injector per application and select once after validation, sequence acceptance,
normalization, and request-ID creation; retain that decision across boundaries.
Failure selection must never bypass validation or roll back sequence state.

The application composes the selector and execution hooks in both security modes.
See [the task-by-task guide](docs/application-failure-injection.md) for behavior,
configuration, verification, and limitations. Enabled application simulation emits
`WARNING event=failure_injection_enabled` during startup. Applied faults emit
`event=failure_injected` with the request ID and increment the existing
`gateway_injected_failures_total{failure_type="..."}` counter.

Member 3's crypto injector remains separate; crypto modes select no application
fault. This framework does not generate keys/nonces/request IDs, mutate payloads,
or add network fields. Its private PRNG does not change global random state.

```bash
uv run pytest edge_gateway/tests/test_gateway_failure_injector.py
```
