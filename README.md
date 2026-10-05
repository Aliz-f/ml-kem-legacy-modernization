# ML-KEM Legacy Modernization

A Python 3.12 course project that modernizes a simulated Legacy Device → Edge Gateway → Cloud Service measurement system for post-quantum cryptography (PQC). The Legacy Device retains its HTTP/JSON interface; only the Gateway-to-Cloud path changes.

Two explicit modes are implemented:

- **Classical Baseline Mode**: SECURITY_MODE=classical uses the baseline Cloud endpoint.
- **Modernized ML-KEM Mode**: SECURITY_MODE=mlkem with PQC_FAILURE_POLICY=fail_closed uses ML-KEM-768 session establishment and AES-256-GCM payload protection. It never falls back to plaintext at runtime.

This is the project map and quick-start. The linked architecture documents are the source of truth.

## Start here

Choose one of these paths. Run every command from the repository root.

| I want to… | Run this | Then check this |
| --- | --- | --- |
| run the normal baseline system | `SECURITY_MODE=classical docker compose up --build --wait` | [check the stored measurements](#check-a-running-system) |
| run the PQC-protected system | `SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed docker compose up --build --wait` | [check metrics and stored measurements](#check-a-running-system) |
| run all automated checks | follow [run every repository check](#run-every-repository-check) | all commands exit with status 0 |
| compare baseline and ML-KEM locally | `uv run python scripts/measure_mode_comparison.py --samples 10` | keep the JSON output; see [evaluation](#tests-and-evaluations) |

The Legacy Device starts automatically in Compose, sends measurements through
the Gateway, and the Cloud persists accepted measurements. Stop the current
stack before switching modes:

```bash
docker compose down
```

## Contents

- [Start here](#start-here)
- [Architecture and assumptions](#architecture-and-assumptions)
- [Repository layout](#repository-layout)
- [Protocol and modes](#protocol-and-modes)
- [Development and AI agents](#development-and-ai-agents)
- [Tests and evaluations](#tests-and-evaluations)
- [Metrics and operations](#metrics-and-operations)
- [Docker deployment](#docker-deployment)
- [Risks and technical debt](#risks-and-technical-debt)
- [Graphify and GitHub Actions](#graphify-and-github-actions)
- [Complete command reference](#complete-command-reference)

## Architecture and assumptions

~~~text
Legacy Device                    Edge Gateway                         Cloud Service
sensor simulation --HTTP/JSON--> validation, normalization ----------> SQLite
                                 sequence tracking
                                 classical JSON, or
                                 ML-KEM-768 -> HKDF-SHA-256 -> AES-256-GCM
~~~

There are two deliberately separate boundaries. The Legacy Device sends a five-field measurement to POST /api/v1/measurements. The Gateway validates, normalizes, tracks per-device sequence state, and returns 202 only after Cloud acceptance. The Cloud owns persistence and the UNIQUE(device_id, sequence_number) idempotency constraint.

The authoritative designs are the [shared cross-component protocol](docs/architecture/04%20-%20Shared%20Cross-Component%20Protocol%20Specification.md), [Legacy Device](docs/architecture/01%20-%20Legacy%20Device.md), [Edge Gateway](docs/architecture/02%20-%20Edge%20Gateway.md), and [Cloud Service](docs/architecture/03%20-%20Cloud%20Service.md).

Key assumptions and frozen limits:

- Legacy-to-Gateway traffic intentionally remains HTTP/JSON and is not PQC-protected. Modernization is at the Gateway-to-Cloud boundary.
- Protocol v1 uses ML-KEM-768, HKDF-SHA-256 with salt=None and fixed project info, one 32-byte session key, AES-256-GCM, a 12-byte nonce, and four-field AAD. See the [protocol specification](docs/architecture/04%20-%20Shared%20Cross-Component%20Protocol%20Specification.md).
- Sessions have a 300-second lifetime and key/session state is process-local. Ordinary transport retry resends the identical built envelope. A 409 SESSION_INVALID or SESSION_EXPIRED triggers one replacement session and a rebuilt envelope with the same logical request ID.
- The test environment is single-instance, HTTP-only, and SQLite-based. Gateway sequence/session state and Cloud ML-KEM identity are intentionally in memory.
- Idempotency is business-level duplicate control, not cryptographic replay protection. Protocol v1 has no replay counter/window.

The intended delivery order is architecture and baseline first; then ML-KEM/session security, secure E2E, failure handling and observability, Docker/CI, and evaluation. Phase gates and owner responsibilities are in the [implementation roadmap](docs/architecture/05%20-%20Implementation%20roadmap.md) and [Member 1](docs/architecture/06%20-%20Member%201%20Tasks.md), [Member 2](docs/architecture/07%20-%20Member%202%20Tasks.md), [Member 3](docs/architecture/08%20-%20Member%203%20Tasks.md), [Member 4](docs/architecture/09%20-%20Member%204%20Tasks.md), and [Member 5](docs/architecture/10%20-%20Member%205%20Tasks.md) tasks.

## Repository layout

~~~text
.
├── legacy_system/             sensor simulator, serializer, HTTP client, faults
│   ├── src/legacy_system/     implementation
│   ├── tests/                 component tests
│   ├── docs/                  operations, measurements, faults, debt
│   └── Dockerfile
├── edge_gateway/              Legacy API, baseline/PQC transport, sessions
│   ├── src/edge_gateway/      validation, sequence, metrics, crypto
│   ├── tests/                 application and security tests
│   ├── docs/                  operations, reviews, security, debt
│   └── Dockerfile
├── cloud_service/             APIs, ML-KEM/session service, validation, SQLite
│   ├── src/cloud_service/     implementation
│   ├── tests/                 API, crypto, storage tests
│   ├── docs/                  secure ingestion, configuration, operations
│   └── Dockerfile
├── tests/                     repository, contract, and integration tests
│   ├── ai_history/            AI-history CLI tests
│   └── integration/           live, E2E, fault, and Compose tests
├── docs/                      architecture, operations, testing, deployment, evaluation
├── scripts/                   measurement and Graphify-refresh scripts
├── src/ai_history/            local AI-history command
├── graphify-out/              generated code graph and report
├── .github/workflows/         CI workflows
├── docker-compose.yml         three-service test topology
├── .env.example               non-secret configuration/fault map
├── pyproject.toml / uv.lock   workspace and locked dependencies
└── AGENTS.md                  binding AI-agent policy
~~~

Ownership is fixed: Legacy owns sensing/client behavior; Gateway owns the Legacy API, normalization, sequence policy, baseline delivery, and PQC transport; Cloud owns ML-KEM/session handling, decryption, validation, idempotency, and storage; repository-wide integration owns Docker, CI, E2E, and metrics coordination. See [AGENTS.md](AGENTS.md) and the [roadmap](docs/architecture/05%20-%20Implementation%20roadmap.md).

Component entry points: [Legacy Device README](legacy_system/README.md), [Edge Gateway README](edge_gateway/README.md), and [Cloud final operations](cloud_service/docs/final-integration-and-operations.md).

## Protocol and modes

| Area | Classical baseline | Modernized ML-KEM |
| --- | --- | --- |
| Configuration | SECURITY_MODE=classical | SECURITY_MODE=mlkem; PQC_FAILURE_POLICY=fail_closed |
| Cloud delivery | POST /api/v1/baseline/measurements | public key → session → POST /api/v1/secure/measurements |
| Correlation | X-Request-ID | request ID in authenticated envelope AAD |
| Failure handling | visible failure after bounded retry | fail closed, never automatic plaintext fallback |
| Legacy interface | unchanged | unchanged |

Secure binary JSON values are Base64URL. A SecureEnvelope contains exactly protocol_version, gateway_id, session_id, request_id, nonce, and ciphertext; AAD contains exactly protocol_version, gateway_id, session_id, and request_id. Any endpoint, schema, status code, crypto/KDF/nonce/AAD parameter, retry/session behavior, or storage-mapping change is an architecture change and must follow the update order in [AGENTS.md](AGENTS.md).

## Development and AI agents

All contributors and agents follow [AGENTS.md](AGENTS.md); [CLAUDE.md](CLAUDE.md), [GROK.md](GROK.md), and [Copilot instructions](.github/copilot-instructions.md) defer to it. Before making a change, identify affected components, read required frozen documents, inspect code/tests, and work only within the roadmap scope.

~~~text
task -> feature branch from develop -> AI-history task -> implement and test
     -> factual output -> human review -> revision if needed
     -> accepted final human verification -> PR to develop -> peer review -> merge
~~~

The detailed branching, review gate, and AI-history lifecycle are in the [development workflow](docs/DEVELOPMENT_WORKFLOW.md) and [AI-history guide](docs/ai/README.md). AI output remains untrusted until human review and verification. Never put secrets, key material, credentials, .env content, or invented human review text in the history.

Use maintained ML-KEM, HKDF, and AES-GCM libraries; never implement primitives or add plaintext fallback. Course scope and required AI evaluation are in [Group Explanation 01](Group-Explanation%2001.pdf) and [Group Explanation 02](Group-Explanation%2002.pdf).

## Tests and evaluations

The [project test matrix](docs/testing/PROJECT_TEST_MATRIX.md) records evidence by test layer rather than asserting a coverage percentage.

| Type | Purpose | Detail |
| --- | --- | --- |
| Unit/component | models, validation, config, crypto wrappers, storage, device runtime | [developer testing guide](docs/testing/DEVELOPER_TESTING_GUIDE.md) |
| Contract | frozen schemas, endpoints, KDF, AAD, envelope, sessions | [protocol regression detection](docs/testing/M5_PROTOCOL_REGRESSION_DETECTION.md) |
| Integration | live Legacy-Gateway and Gateway-Cloud boundaries | [developer testing guide](docs/testing/DEVELOPER_TESTING_GUIDE.md) |
| End-to-end | production client, Gateway, Cloud, and SQLite in both modes | [test matrix](docs/testing/PROJECT_TEST_MATRIX.md) |
| Failure/security | invalid data, outages, tampering, session recovery, bounded retry, fail-closed mode | [failure matrix](docs/testing/FAILURE_TEST_MATRIX.md), [security suite](docs/testing/M5_SECURITY_REGRESSION_SUITE.md) |
| Compose/recovery | image wiring, health/readiness, restart/session recovery | [deployment recovery evidence](docs/testing/M5_DEPLOYMENT_RECOVERY.md) |

Evaluation is reproducible local evidence, not a capacity or production benchmark. The matched baseline and secure harnesses run sequential data through loopback HTTP and temporary SQLite, with zero retries and no injected faults. Secure output separates first-message session establishment from steady-state delivery. Read the [baseline method](docs/evaluation/baseline-measurement-method.md), [modernized method](docs/evaluation/modernized-measurement-method.md), [comparison method](docs/evaluation/baseline-vs-modernized-comparison.md), and [final evaluation evidence](docs/evaluation/final-evaluation-evidence.md) before reporting results.

## Metrics and operations

Gateway and Cloud each expose Prometheus text at GET /metrics. The dashboard starts with the default Compose stack; open `http://127.0.0.1:${DASHBOARD_HOST_PORT:-8080}` after `docker compose up --build --wait`. It displays health/readiness, bounded metric charts, Cloud measurements, whitelisted runtime configuration, and recent container logs. It can also explicitly restart one selected service with temporary, allowlisted failure-injection or log-level overrides; it never edits `.env` or `docker-compose.yml`, and a later Compose recreate restores configured defaults. See the [metrics contract](docs/operations/METRICS_CONVENTIONS.md) and [monitoring decision](docs/operations/MONITORING_DASHBOARD_DECISION.md).

| Family | Representative metrics | Use |
| --- | --- | --- |
| Gateway intake/sequence | gateway_measurements_received_total, gateway_measurements_accepted_total, gateway_measurements_rejected_total, gateway_duplicate_measurements_total, gateway_sequence_gaps_total | validation and sequence results |
| Gateway delivery | gateway_cloud_requests_total, gateway_cloud_failures_total, gateway_cloud_retries_total, gateway_cloud_request_duration_seconds | delivery and retries |
| Gateway PQC | gateway_mlkem_handshakes_total, gateway_active_session, gateway_session_reestablishments_total, gateway_encryption_failures_total, gateway_pqc_fallback_total | session/security state; fallback is always zero in v1 |
| Cloud ingress/crypto | cloud_baseline_requests_total, cloud_secure_requests_total, cloud_authenticated_messages_total, cloud_decryption_failures_total, cloud_mlkem_sessions_created_total | mode and authentication results |
| Cloud storage | cloud_measurements_stored_total, cloud_duplicate_measurements_total, cloud_storage_failures_total, cloud_request_duration_seconds | persistence/idempotency outcomes |

Labels must remain finite and low-cardinality. Do not use IDs, timestamps, payloads, nonces, ciphertext, or secrets as labels; correlate with logs instead. The required safe event fields and prohibited material are documented in [logging conventions](docs/operations/LOGGING_CONVENTIONS.md) and [secret-logging review](docs/operations/SECRET_LOGGING_REVIEW.md).

For health, recovery, failure injection, and safe logs, use the [system runbook](docs/RUNBOOK.md) and [failure automation evidence](docs/testing/M5_FAILURE_AUTOMATION.md). Fault injection is local to the selected service and off by default.

## Docker deployment

docker-compose.yml provides the test topology:

~~~text
legacy-device --depends on Gateway health--> edge-gateway
edge-gateway  --depends on Cloud health----> cloud-service --> cloud-data volume
~~~

Gateway and Cloud bind to loopback by default on 8000 and 9000. Legacy has no inbound host port; service DNS uses edge-gateway:8000 and cloud-service:9000. The Cloud-owned cloud-data volume persists accepted SQLite measurements across normal restarts, never keys or sessions. Use the [Compose test-environment runbook](docs/deployment/compose-test-environment.md) for lifecycle commands and [SQLite persistence strategy](docs/deployment/sqlite-persistence.md) for persistence and clean-test rules.

Copy .env.example only for local non-secret configuration. Never commit a populated .env file.

## Risks and technical debt

The [technical-debt register](docs/technical-debt.md) records accepted course-system limits: unauthenticated Legacy traffic, no durable Gateway queue, in-memory sequence/session/key state, simplified public-key trust, HTTP-only test deployment, single-instance SQLite, bounded retry, business-only idempotency, no crypto replay defense, and Python memory-zeroization limits.

The [risk register](docs/risk-register.md) explains the corresponding events, controls, impact, and residual treatment: public-key substitution, Legacy spoofing, envelope replay, outages/loss, retry amplification, restart state loss, secret exposure, SQLite availability, and inappropriate classical-mode selection. Component evidence is in the [Gateway threat model](edge_gateway/docs/threat-model.md), [Gateway debt register](edge_gateway/docs/technical-debt.md), and [Legacy debt register](legacy_system/docs/technical-debt.md).

## Graphify and GitHub Actions

[Graphify](docs/development/graphify.md) is a local, code-only navigation aid. Its generated artifacts, graphify-out/graph.json and graphify-out/GRAPH_REPORT.md, are not runtime inputs or architecture authority. Refresh them after graph-relevant code changes; do not hand-edit artifacts or install Graphify hooks.

| Workflow | Purpose | Detail |
| --- | --- | --- |
| Repository quality | push/PR: frozen install, Ruff, AI history, unit/contract/crypto/integration/E2E tests, image builds, clean Compose recovery | [ai-history.yml](.github/workflows/ai-history.yml) |
| Graphify shared code graph | PRs to develop with code/config changes: refreshes and rejects stale graph artifacts | [graphify.yml](.github/workflows/graphify.yml) |

See the [developer testing guide](docs/testing/DEVELOPER_TESTING_GUIDE.md) and [development workflow](docs/DEVELOPMENT_WORKFLOW.md) for CI equivalence and release process.

## Complete command reference

Run commands from the repository root. Use uv sync --frozen before checks/evaluation. Docker is required for Compose commands. The clean reset below permanently removes the local named volume and its demo measurements.

### Run every repository check

Start with the first five lines below. They install the locked dependencies,
lint the repository, run the full test suite, validate AI history, and check
Markdown/code whitespace. A successful command prints no errors and exits with
status 0.

The commands after **Component suites** are alternatives for focused work; do
not run every focused selection unless you specifically want that extra detail.

~~~bash
uv sync --frozen
uv run ruff check .
uv run pytest
uv run ai-history check
git diff --check

# Component suites
uv run pytest legacy_system/tests
uv run pytest edge_gateway/tests
uv run pytest cloud_service/tests
uv run pytest tests/ai_history

# Frozen contracts and live integrations
uv run pytest \
  tests/integration/test_legacy_gateway.py \
  tests/integration/test_gateway_cloud_baseline.py \
  tests/integration/test_mlkem_session_orchestration.py \
  tests/integration/test_gateway_cloud_secure_session.py \
  tests/integration/test_gateway_cloud_secure.py

# Classical and ML-KEM end-to-end paths
uv run pytest \
  tests/integration/test_end_to_end.py \
  tests/integration/test_modernized_end_to_end.py \
  tests/integration/test_legacy_mode_success_compatibility.py

# Failure, tamper, metrics, observability, and Compose recovery
uv run pytest tests/integration/test_failure_paths.py
uv run pytest tests/integration/test_secure_message_tamper.py
uv run pytest tests/integration/test_metrics_sanity.py
uv run pytest tests/integration/test_observability_integration.py
uv run pytest tests/integration/test_gateway_compose_e2e.py
~~~

### Run one mode

Run **one** of the two start commands. Do not start both modes at once. If a
stack is already running, use `docker compose down` before changing mode.

~~~bash
docker compose config --quiet
SECURITY_MODE=classical docker compose up --build --wait
docker compose down
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed docker compose up --build --wait
~~~

### Check a running system

After either Compose start command completes, use these commands in order. The
first four confirm that both HTTP services are alive and ready; the next two
show operational counters; the last command shows measurements accepted by the
Cloud. An empty session count immediately after startup is normal in ML-KEM
mode because sessions are created lazily.

~~~bash
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/health
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/ready
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/health
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/ready
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/api/v1/measurements
~~~

Use `docker compose logs --follow legacy-device edge-gateway cloud-service` to
watch safe operational logs. Use `docker compose down` to stop the stack;
`docker compose down --volumes --remove-orphans` also deletes its local
database volume.

### Presentation scenarios

Reset with docker compose down --volumes --remove-orphans before each one. Outcomes are documented in [demo scenarios](docs/presentation/demo-scenarios.md).

~~~bash
# 1. Classical baseline
SECURITY_MODE=classical docker compose up --build --wait

# 2. Modernized ML-KEM
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed docker compose up --build --wait

# 3. Tampered ciphertext: reject and do not store
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed \
  GATEWAY_FAILURE_MODE=corrupt_ciphertext GATEWAY_FAILURE_RATE=1 \
  docker compose up --build --wait

# 4. Storage failure: bounded visible failure and no false acceptance
SECURITY_MODE=mlkem PQC_FAILURE_POLICY=fail_closed \
  CLOUD_FAILURE_MODE=storage_failure CLOUD_FAILURE_RATE=1 \
  docker compose up --build --wait
~~~

### Evaluations, Graphify, and AI-history inspection

~~~bash
uv run python scripts/measure_baseline_e2e.py --samples 10
uv run python scripts/measure_modernized_e2e.py --samples 10
uv run python scripts/measure_mode_comparison.py --samples 10

uv run pytest tests/integration/test_end_to_end.py tests/integration/test_modernized_end_to_end.py
uv run pytest tests/integration/test_secure_message_tamper.py tests/integration/test_mlkem_handshake_failure_demo.py

uv run graphify query "Which modules implement the Gateway-to-Cloud secure path?"
uv run graphify path "SessionManager" "SecureEnvelope"
uv run graphify explain "Measurement"
uv run python scripts/refresh_graphify.py

uv run ai-history status
uv run ai-history list
uv run ai-history check
~~~
