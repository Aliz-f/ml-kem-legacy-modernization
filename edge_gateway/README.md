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
| `POST /api/v1/measurements` | Registered, but unavailable (`503`); accepts no measurements |
| `GET /metrics` | Prometheus text with bounded `gateway_service_info` only |

This is roadmap Phase 3 / G2 scaffolding. Measurement parsing/validation,
normalization, sequencing, request IDs, Cloud delivery, and operational metrics
belong to later tasks. The measurement placeholder does not parse the body;
it is not the completed Legacy API. Later validation must preserve malformed
JSON → `400`, invalid parsed fields → `422`, and `202` only after Cloud acceptance.

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
not mean a measurement has been accepted. HTTP syntax/error mapping and route
integration remain later tasks; the skeleton route still returns `503`.
Timestamp serialization uses Python datetime microsecond precision.

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
