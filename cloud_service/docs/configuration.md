# Cloud configuration (M4-01)

`cloud_service.config.load_config()` reads the process environment;
`load_config(mapping)` and `Config.from_env(mapping)` accept an explicit mapping
for tests. An empty mapping uses defaults, not the process environment.
The returned frozen dataclass contains parsed settings. Use these loaders for
validation rather than constructing `Config` directly.

| Variable | Default | Validation |
|---|---|---|
| CLOUD_ID | cloud-001 | Non-empty local identifier |
| HOST | 0.0.0.0 | Non-empty bind host; actual binding belongs to the app |
| PORT | 9000 | Integer, 1 through 65535 |
| DATABASE_URL | sqlite:///cloud.db | SQLite file URL or sqlite:///:memory: |
| SECURITY_MODE | classical | classical or mlkem |
| SESSION_TTL_SECONDS | 300 | Must equal 300 for protocol v1 |
| FAILURE_MODE | none | Cloud mode listed below |
| FAILURE_RATE | 0.0 | Finite number, 0 through 1 |
| FAILURE_SEED | empty | Optional integer; empty/whitespace means None |
| FAILURE_DELAY_SECONDS | 2 | Finite, non-negative number of seconds |
| LOG_LEVEL | INFO | DEBUG, INFO, WARNING, ERROR, CRITICAL; case-insensitive |

Failure modes: `none`, `public_key_unavailable`, `mlkem_decapsulation_failure`,
`session_not_found`, `session_expired`, `decryption_failure`, `storage_failure`,
`processing_delay`, `service_unavailable`, `drop_response`, `random`.
Recognizing a mode does not implement fault injection or crypto behavior.

SQLite paths use forward slashes: `sqlite:///data/cloud.db` is relative to the
working directory; `sqlite:////absolute/cloud.db` and
`sqlite:///C:/data/cloud.db` express absolute paths on their respective platforms.
Query parameters, fragments, remote authorities and empty/directory-only paths
are unsupported. Loading configuration does not open/create a database or check
filesystem permissions; storage initialization is a later task.

The accepted M4-00 review and shared protocol section 30 fix the normal session
TTL at 300 seconds. Non-positive and other non-300 environment values are
rejected. Future session tests can use a controlled clock; this loader adds no
production TTL override. The crypto suite is not configurable. Baseline is the
current roadmap phase, so the default is `classical`. Selecting `mlkem` only
parses that explicit setting; no session, crypto, fallback or app is initialized.

Invalid settings raise `ConfigurationError` naming the setting without echoing
its supplied value. No settings are logged. App startup/exit handling belongs to
M4-02. No `.env` file is read automatically.

Run `uv run pytest cloud_service/tests` from the repository root. Cloud-local
`tests/conftest.py` exposes the source package for these tests because the root
development dependency group does not currently install Cloud. Shared manifests
and the lockfile are unchanged. On Windows use `PYTHONUTF8=1` for the full suite
to avoid the existing AI-history test's locale-dependent file decoding.
