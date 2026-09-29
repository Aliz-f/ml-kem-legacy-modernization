# Cloud application skeleton (M4-02)

The next step after M4-01 is a runnable baseline HTTP shell. `create_app()` in
`cloud_service.app` validates environment configuration and returns a new app.
Tests may pass a `Config` returned by `load_config(mapping)`. Module import has
no database, network, or crypto initialization side effects.

From the repository root, run the shell with:

```text
uv run --frozen --package cloud-service cloud-service
```

Defaults bind to `0.0.0.0:9000`. Set `HOST=127.0.0.1` for local-only access.
Stop with Ctrl+C. `python -m cloud_service.app` is also supported inside the
installed environment. No measurement can be persisted at this stage.

For the full workspace test suite:

```text
uv sync --frozen --all-packages --all-extras
uv run --frozen --all-packages --all-extras pytest
uv run --frozen --all-packages --all-extras ruff check .
```

On Windows set `PYTHONUTF8=1` for the existing AI-history tests. FastAPI and
Uvicorn are Cloud runtime dependencies; HTTPX is in Cloud's `test` extra.
The root development group does not install Cloud, so select all packages and
extras for testing rather than relying on a plain root environment sync.
The locked Starlette version warns that HTTPX TestClient support is deprecated;
the current tests pass, and migration can be handled as a separate dependency
maintenance task.

The shell uses FastAPI's [lifespan context](https://fastapi.tiangolo.com/advanced/events/)
for startup/shutdown and Uvicorn as the server. Startup records the selected
security mode; shutdown clears the running state and logs a shutdown event.
The CLI applies `HOST`, `PORT`, and `LOG_LEVEL`, disables access logging, and
uses a five-second graceful request-shutdown timeout. Uvicorn owns signal
handling. Configuration failures return a nonzero exit code without echoing
configuration values. Logging includes no configuration dump or request body.

| Route | Current behavior |
|---|---|
| `GET /health` | `200 {"status":"ok"}` while the lifespan is running |
| `GET /ready` | `503` with structured `SERVICE_UNAVAILABLE` error |
| `GET /metrics` | Prometheus text exposition containing only bounded `cloud_service_info`; request, storage, session, and crypto metrics require their later features |

Readiness intentionally stays unavailable: storage, validation, and persistence
have not been implemented. Liveness is not a claim that Cloud can accept a
measurement. There is no active-session requirement for readiness.

`SECURITY_MODE=mlkem` fails startup because the secure subsystems do not yet
exist; it never switches to classical mode. No crypto is initialized in baseline
mode. Failure-injection settings are parsed configuration only at this stage.

Measurement, query, crypto, and session routes are not registered yet and return
the framework's `404`. No stub returns `202` or pretends to persist data. M4-02's
eventual endpoint list is a target, not evidence those features
already exist. Storage initialization and cleanup will be added with M4-06/07;
baseline acceptance follows M4-03 through M4-11; query, crypto, sessions, metrics,
and complete readiness remain their designated later tasks. The app contains
no SQL or crypto internals and does not alter any frozen wire contract.

M4-00 and M4-01 are complete prerequisites. This skeleton does not complete
the roadmap baseline Cloud gate or baseline E2E gate. Future lifecycle changes
must initialize required subsystems before reporting readiness, close resources
on shutdown/failure, and preserve lookup → ownership → expiry session validation.
