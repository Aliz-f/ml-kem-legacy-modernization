# M5 deployment and restart recovery evidence

This document records the Compose-level evidence for M5-77, M5-78, and M5-79.
It does not alter the frozen Gateway--Cloud protocol or introduce a persistence
mechanism for cryptographic state.

## Scenarios

`tests/integration/test_gateway_compose_e2e.py` exercises the operational
failures using fresh Compose projects and volumes:

| Task | Scenario | Expected and asserted recovery |
|---|---|---|
| M5-77 | Gateway or Cloud container is stopped during normal deployment. | The stopped service becomes unavailable; after restart, readiness returns and delivery can continue. |
| M5-78 | Gateway restarts after a successful ML-KEM delivery. | Its process-local session is lost. The next measurement creates one new ML-KEM session; the old Cloud session can remain until its normal expiry. |
| M5-79 | Cloud restarts after a successful ML-KEM delivery. | A new Cloud key ID is exposed and old sessions disappear. The Gateway receives `409 SESSION_INVALID`, invalidates its local session, gets the new public key, establishes one replacement session, rebuilds the same logical request under that key, and succeeds. |

The Cloud restart regression also confirms the secure path remains fail closed:
`gateway_pqc_fallback_total` and `cloud_baseline_requests_total` stay zero.
The named SQLite volume survives a Cloud-only restart, so the query result has
exactly one row for each logical `(device_id, sequence_number)` measurement.

## Intentional operational boundaries

Gateway sequence and session state, plus Cloud ML-KEM identity and session
state, are process-local. A Gateway restart therefore loses its sequence
tracker as well as its secure session; a Cloud restart loses its key pair and
all secure sessions. These are accepted course-system technical debts, not
signals to fall back to plaintext. The current Compose stack has no Legacy
service, so legacy-start ordering and direct SQLite-file corruption remain
outside this two-service deployment regression.

Run the evidence locally with:

```bash
uv run pytest tests/integration/test_gateway_compose_e2e.py
```
