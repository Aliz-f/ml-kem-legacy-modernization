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
| `POST /api/v1/measurements` | Invalid JSON → `400`; invalid schema → `422`; schema-valid requests → `503` pending delivery |
| `GET /metrics` | Prometheus text with bounded `gateway_service_info` only |

This is roadmap Phase 3 / G2 scaffolding with G3 syntax/schema validation. Domain validation,
normalization, sequencing, request IDs, Cloud delivery, and operational metrics
belong to later tasks. This is not the completed Legacy API; `202` will be
returned only after Cloud acceptance.

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
and nonnegative sequences remain M2-05 domain validation. Parsing a model does
not mean a measurement has been accepted. M2-04 integrates this schema at the
HTTP boundary; schema-valid requests still return `503` pending later stages.
Timestamp serialization uses Python datetime microsecond precision.

## Schema validation (M2-04)

`edge_gateway.validation.parse_legacy_measurement(body)` decodes JSON and then
uses the M2-03 request model. Malformed or empty bodies, invalid encoding, and
non-JSON constants (`NaN`, `Infinity`) produce `400 INVALID_JSON`. Parsed JSON
with missing/extra fields, wrong types, or an invalid timestamp produces
`422 INVALID_MEASUREMENT`. Both responses use the shared structured error body
and omit payload values and parser details. Invalid requests make no Cloud calls.

Domain bounds remain M2-05; sequencing, normalization, and delivery also remain
separate later stages. No measurement is accepted or forwarded by this task.

```bash
uv run pytest edge_gateway/tests/test_gateway_validation.py
```

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
