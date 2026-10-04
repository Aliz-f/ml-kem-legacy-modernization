# Developer testing guide

This M5-59 guide maps the repository's current test evidence to commands that
developers can run from the repository root. Start with the smallest relevant
selection, then run the repository checks before review. Test results are
evidence, not a substitute for the required human AI-history review.

## Setup and repository checks

```bash
uv sync --frozen
uv run ruff check .
uv run pytest
uv run ai-history check
```

Use the committed lockfile. Do not add `requirements.txt` or record secrets,
keys, `.env` values, session keys, or private data in test output or history.

## Unit and component tests

Run the relevant component suite while changing that component:

```bash
uv run pytest legacy_system/tests
uv run pytest edge_gateway/tests
uv run pytest cloud_service/tests
uv run pytest tests/ai_history
```

## Contract and integration tests

The CI workflow's named contract selection protects frozen wire and crypto
contracts. For the main live integration paths, run:

```bash
uv run pytest \
  tests/integration/test_legacy_gateway.py \
  tests/integration/test_gateway_cloud_baseline.py \
  tests/integration/test_mlkem_session_orchestration.py \
  tests/integration/test_gateway_cloud_secure_session.py \
  tests/integration/test_gateway_cloud_secure.py
```

These tests use production application boundaries and verify the frozen
versioned ML-KEM, HKDF, AES-GCM, AAD, session-recovery, retransmission, and
idempotency behavior. Do not change a protocol assertion merely to match an
implementation; resolve any mismatch against the architecture documents.

## End-to-end tests

The full in-process E2E evidence uses the real Legacy client, Gateway, Cloud,
and SQLite paths in both explicit modes:

```bash
uv run pytest \
  tests/integration/test_end_to_end.py \
  tests/integration/test_modernized_end_to_end.py \
  tests/integration/test_legacy_mode_success_compatibility.py
```

Modernized mode remains `SECURITY_MODE=mlkem` with
`PQC_FAILURE_POLICY=fail_closed`. It does not automatically downgrade to the
baseline endpoint.

## Failure, security, and metrics tests

```bash
uv run pytest tests/integration/test_failure_paths.py
uv run pytest tests/integration/test_gateway_cloud_secure.py
uv run pytest tests/integration/test_secure_message_tamper.py
uv run pytest tests/integration/test_metrics_sanity.py
uv run pytest tests/integration/test_observability_integration.py
```

The security tests intentionally do not require every valid-length mutated
ML-KEM ciphertext to raise: ML-KEM may use implicit rejection. For ordinary
ambiguous-response retry, the same already-built SecureEnvelope is resent;
business idempotency ensures one logical stored row. See
[M5 security regression evidence](M5_SECURITY_REGRESSION_SUITE.md), the
[failure matrix](FAILURE_TEST_MATRIX.md), and the
[metrics conventions](../operations/METRICS_CONVENTIONS.md).

## Baseline and modernized measurements

These are small reproducible evidence harnesses, not a performance benchmark
platform:

```bash
uv run python scripts/measure_baseline_e2e.py
uv run python scripts/measure_modernized_e2e.py
uv run python scripts/measure_mode_comparison.py
```

Read the matching files under `docs/evaluation/` before comparing results;
match workload, mode, and failure configuration.

## Docker and Compose checks

The current Compose topology contains `cloud-service` and `edge-gateway`.
The Legacy container remains a separate Member 1 prerequisite, so do not call
the two-service Compose stack a full three-container deployment.

```bash
docker compose config --quiet
uv run pytest tests/integration/test_gateway_compose_e2e.py
```

The Compose regression covers classical and ML-KEM delivery, health,
readiness, metrics, graceful Gateway shutdown, Cloud outage/restart recovery,
Gateway session loss after restart, and Cloud stale-session recovery. See the
[M5 deployment recovery evidence](M5_DEPLOYMENT_RECOVERY.md) for the frozen
fail-closed and idempotency assertions. For persistent versus clean SQLite
behavior, see [the SQLite persistence strategy](../deployment/sqlite-persistence.md).

## CI separation and clean-environment verification

The repository workflow keeps fast feedback and container validation distinct:
`quality` runs formatting and AI-history validation; `unit-tests` runs component,
repository, contract, and crypto tests; `integration-tests` covers live
cross-component paths; and `secure-e2e` covers the full classical and ML-KEM
flows. `docker-build` independently builds the Legacy Device, Gateway, and
Cloud images from the committed workspace lockfile.

The `clean-environment` job is intentionally a new GitHub-hosted runner. It
performs a frozen `uv sync`, validates the Compose configuration, and runs the
real Compose regression, which builds and starts the documented Gateway and
Cloud stack. The Legacy Device image is build-validated separately because it
is a client runtime rather than a Compose service. Each Python job enables the
`setup-uv` dependency cache keyed from the committed dependency inputs; a cache
is an optimization only and every job still uses `uv sync --frozen`.

## CI and review

`.github/workflows/ai-history.yml` runs frozen installation, Ruff, the full
suite, explicit observability/metrics, contract, crypto, Cloud, integration,
E2E, AI-history, Docker-readiness, and Compose-recovery stages. Before asking
for human review, run the focused checks for the change plus:

```bash
uv run ruff check .
uv run pytest
uv run python scripts/refresh_graphify.py
uv run ai-history check
git diff --check
```

Then use the lifecycle in [the development workflow](../DEVELOPMENT_WORKFLOW.md):
record AI output, wait for human review, record any revision, and wait for
explicit final verification. Never fill human review fields yourself.
