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
installed environment. The baseline endpoint now persists canonical measurements.

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
| `GET /api/v1/crypto/public-key` | `200` with protocol v1 ML-KEM-768 public metadata in `mlkem` mode; `503` if unavailable or in `classical` mode |
| `POST /api/v1/crypto/sessions` | `200` with versioned session metadata after validated ML-KEM/HKDF establishment in `mlkem` mode; see [sessions](sessions.md) |
| `POST /api/v1/secure/measurements` | Authenticated ingestion in `mlkem` mode; see [secure ingestion](secure-ingestion.md) |
| `POST /api/v1/baseline/measurements` | `202 accepted` or `202 already_accepted` after committed persistence |
| `GET /api/v1/measurements` | Bounded `200 {"items": [...]}` with optional device filter |
| `GET /api/v1/measurements/{record_id}` | Stored record with `200`, or structured `404` |
| `GET /metrics` | Prometheus text exposition containing only bounded `cloud_service_info`; request, storage, session, and crypto metrics require their later features |

Full readiness checks remain later work; this PR leaves `/ready` unchanged.
M4-05 through M4-07 initialize SQLite and expose a repository on app state;
M4-08 through M4-11 add baseline ingestion. There is no active-session
requirement for readiness.

M4-16–M4-20 allow `SECURITY_MODE=mlkem` to start the ephemeral
[key service](mlkem-key-service.md). Storage and key initialization must succeed
before liveness is reported. Key failure aborts startup and closes storage;
there is no switch to classical mode. Baseline ingestion is rejected in `mlkem`
mode. No key is generated in baseline mode. Readiness remains `503`. Failure-injection settings are still
parsed configuration only.

M4-34–M4-36 register secure measurement ingestion. Baseline ingestion returns `202` only after
the storage transaction commits. See [baseline ingestion](baseline.md).
Storage initialization and cleanup are implemented by M4-06/07. Request, storage, session, and
crypto metrics remain their designated later work. The app contains
no SQL or crypto internals and does not alter any frozen wire contract.

M4-00 and M4-01 are complete prerequisites. This skeleton does not complete
the roadmap baseline Cloud gate or baseline E2E gate. SQLite initializes before
the app becomes live; initialization failure aborts startup with a safe error.
Shutdown closes storage and clears the database/repository references even when
the lifespan exits through an exception. The configured database's parent
directory must already exist. Future secure work must preserve
lookup → ownership → expiry session validation.

M4-12/M4-13 add the [measurement query API](queries.md), using the existing
repository with bounded list results. Gateway-to-Cloud integration remains
M4-14 and is not implemented by these query tasks.

M4-23–M4-29 add the in-memory session manager and establishment API. Shutdown
clears session keys before releasing Cloud keys/storage. Session validation
uses lookup, ownership, then expiry; TTL is 300 seconds without extension.
See [session behavior and tests](sessions.md) for the current integration scope.
