# Project-wide test matrix

This is the Member 5 coordination artifact for M5-72.  It inventories
automated evidence present in this checkout; it is not a coverage report and a
marked cell is not proof of correctness.  The rows follow the test layers in
the shared protocol specification: unit, contract, integration, end-to-end,
and failure/security regression.

## Status key

- **Evidence** — one or more current tests exercise the stated layer.
- **N/A** — that layer does not apply independently to the area.
- **Gap** — a useful regression is not currently represented; the listed
  owner coordinates its resolution under M5-73.

## Current evidence

| Area | Unit | Contract | Integration | E2E | Failure / security | Evidence highlights |
|---|---|---|---|---|---|---|
| Legacy Device | Evidence | Evidence | Evidence | Evidence | Evidence | `legacy_system/tests/`; `tests/integration/test_legacy_gateway.py`; `tests/integration/test_end_to_end.py`; `tests/integration/test_failure_paths.py` |
| Gateway application | Evidence | Evidence | Evidence | Evidence | Evidence | `edge_gateway/tests/test_gateway_*.py`; `tests/integration/test_gateway_cloud_baseline.py`; `tests/integration/test_legacy_compatibility.py`; `edge_gateway/tests/test_gateway_application_failures_integration.py` |
| Gateway crypto and sessions | Evidence | Evidence | Evidence | Evidence | Evidence | `edge_gateway/tests/test_mlkem.py`, `test_kdf.py`, `test_secure_envelope.py`, and `test_aad.py`; `tests/integration/test_mlkem_session_orchestration.py`; `tests/integration/test_modernized_end_to_end.py`; `tests/integration/test_secure_message_tamper.py` |
| Cloud API and crypto | Evidence | Evidence | Evidence | Evidence | Evidence | `cloud_service/tests/test_cloud_*.py`; `cloud_service/tests/test_gateway_cloud_baseline_contract.py`; `tests/integration/test_gateway_cloud_secure.py`; `tests/integration/test_mlkem_handshake_failure_demo.py` |
| SQLite storage | Evidence | N/A | Evidence | Evidence | Evidence | `cloud_service/tests/test_cloud_storage.py`; `cloud_service/tests/test_baseline_integration.py`; `tests/integration/test_end_to_end.py`; `tests/integration/test_gateway_cloud_secure.py` |
| Cross-component protocol | N/A | Evidence | Evidence | Evidence | Evidence | CI runs the protocol-contract selection in `.github/workflows/ai-history.yml`; `tests/integration/test_gateway_cloud_secure_session.py`; `tests/integration/test_gateway_compose_e2e.py`; `docs/testing/M5_FAILURE_AUTOMATION.md` |
| Deployment and CI | N/A | N/A | Evidence | Evidence | Gap | `tests/test_ci_workflow.py`; `tests/integration/test_gateway_crypto_image.py`; `tests/integration/test_gateway_compose_e2e.py`; Docker readiness is also exercised in CI. |
| Observability | Evidence | Evidence | Evidence | Evidence | Evidence | `cloud_service/tests/test_cloud_metrics.py`; `tests/test_metrics_conventions_document.py`; `tests/integration/test_observability_integration.py`; `tests/integration/test_pqc_observability.py` |

Storage has no separate wire-level contract: its observable contract is the
Cloud API and the frozen `UNIQUE(device_id, sequence_number)` idempotency rule.
Likewise, deployment does not have an independent unit or protocol-contract
layer.

## Coordinated gap register

| ID | Gap | Owner | Resolution target | Completion evidence |
|---|---|---|---|---|
| TM-1 | No Compose-level regression simulates a Gateway or Cloud dependency outage/restart and verifies health/readiness recovery. Existing deployment tests cover image construction, crypto installation, normal Compose delivery, and Cloud readiness, but not this operational failure path. | Member 5 | M5-73 coordination | A deterministic Docker Compose test enters CI and asserts the documented health/readiness and delivery outcome. |

## Boundaries retained by this matrix

The failure/security column indexes the existing F1–F18 plan in
[`FAILURE_TEST_MATRIX.md`](FAILURE_TEST_MATRIX.md) and its automation evidence
in [`M5_FAILURE_AUTOMATION.md`](M5_FAILURE_AUTOMATION.md).  It does not add a
new failure protocol.

In particular, modernized-path tests retain the frozen boundaries: a secure
failure is fail closed without a baseline fallback; ordinary transport retry
resends the same already-built envelope; session recovery establishes one
replacement session and rebuilds the envelope while preserving the logical
request ID.  Protocol v1 has no cryptographic replay counter or window, so
business idempotency is not represented as cryptographic replay protection.

Coverage percentages are intentionally absent.  M5-71 permits coverage
aggregation if the team elects to use it, but this matrix records exercised
behaviours and remaining scope rather than inferring quality from a percentage.
