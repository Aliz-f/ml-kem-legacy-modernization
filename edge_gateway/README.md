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

| Route | Current skeleton behavior |
| --- | --- |
| `GET /health` | `200 {"status":"ok"}` while the application is running |
| `GET /ready` | `503 SERVICE_UNAVAILABLE` until processing and transport exist |
| `POST /api/v1/measurements` | Invalid JSON → `400`; invalid schema/domain values → `422`; valid requests → `503` pending delivery |
| `GET /metrics` | Prometheus text with bounded `gateway_service_info` and PQC counters. `gateway_pqc_fallback_total` stays 0 |

This is roadmap Phase 3 / G2 scaffolding with G3 syntax/schema and domain validation.
Normalization and correlation helpers are available, but their route orchestration,
sequencing, Cloud delivery, and application metrics remain later tasks. This is not
the completed Legacy API; `202` will be returned only after Cloud acceptance.

Both configured security modes expose the skeleton. Neither performs Cloud
requests or establishes sessions. Readiness is unavailable because processing
and transport are absent, not because an active secure session is missing.
There is no plaintext fallback.

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
HTTP boundary; requests passing schema and domain validation still return `503` pending delivery.
Timestamp serialization uses Python datetime microsecond precision.

## Schema validation (M2-04)

`edge_gateway.validation.parse_legacy_measurement(body)` decodes JSON and then
uses the M2-03 request model. Malformed or empty bodies, invalid encoding, and
non-JSON constants (`NaN`, `Infinity`) produce `400 INVALID_JSON`. Parsed JSON
with missing/extra fields, wrong types, or an invalid timestamp produces
`422 INVALID_MEASUREMENT`. Both responses use the shared structured error body
and omit payload values and parser details. Invalid requests make no Cloud calls.

Domain bounds are checked separately by M2-05; sequencing, normalization, and
delivery remain later stages. No measurement is accepted or forwarded yet.

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
Sequence ordering and duplicate detection remain later tasks.

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
| `SERVICE_UNAVAILABLE` | 503 | Existing readiness/unfinished-delivery placeholder |

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
Call after schema/domain validation and sequence-policy acceptance. Route
orchestration remains M2-12; the existing route still returns `503` for valid
measurements until Cloud delivery is implemented.

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

These helpers are ready for M2-12 route orchestration and M2-13 Cloud forwarding;
the current placeholder route does not yet accept measurements or create IDs.
Tests construct baseline HTTP requests without sending them and exercise the
existing secure envelope to verify context propagation and authentication.

```bash
uv run pytest edge_gateway/tests/test_gateway_correlation.py
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
`mlkem` setting supports later secure transport work; it does not provide a
plaintext fallback.
