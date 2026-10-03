# Gateway contract and failure hardening — M2-42 through M2-48

This Member 2 PR11 work completes the application-side contract, failure, and
retry checks after the M2-38 through M2-41 unit-suite audit. It adds tests around
the production HTTP boundaries without importing one component's internal model
into another component. It does not change endpoints, status codes, sequence
timing, retries, secure envelopes, sessions, cryptography, or storage mappings.

## M2-42 — Frozen sequence-state timing

The Gateway already implements and documents the required order:

```text
syntax/schema/domain validation
→ sequence-policy acceptance and state commit
→ normalization and request ID
→ selected Cloud transport
```

`test_gateway_measurements.py`, `test_gateway_sequence.py`, and
`test_gateway_routes.py` verify that invalid input does not change state,
sequence conflicts do not move it backward, and downstream failure never rolls
it back. The M2-46 live retry-chain test adds cross-component evidence: after
Cloud delivery exhausts its retries and Gateway returns `503`, the Legacy retry
of the same sequence receives `409 DUPLICATE_SEQUENCE`.

This timing describes Gateway acceptance, not Cloud persistence. It is a frozen
course contract and a documented delivery limitation rather than a reason to add
rollback or a queue.

## M2-43 — Legacy Device ↔ Gateway contract

`tests/integration/test_legacy_gateway.py` now starts the production Gateway
route on loopback and uses Member 1's `GatewayClient`. It verifies:

- a valid five-field fixture receives `202` after downstream acceptance;
- malformed JSON is `400 INVALID_JSON`;
- invalid temperature, humidity, timestamp, and missing fields are
  `422 INVALID_MEASUREMENT`;
- duplicate and older sequences are non-retryable `409` responses;
- a gap is accepted, forwarded once, logged, and counted;
- `400`, `409`, and `422` stop Member 1 retries after one attempt; and
- Legacy and Gateway production packages do not import each other.

## M2-44 — Gateway ↔ Cloud baseline contract

`tests/integration/test_gateway_cloud_baseline.py` sends Gateway's canonical JSON
through `BaselineCloudClient` to Cloud's production baseline route. It checks the
exact seven wire fields, UTC timestamp compatibility, `gateway_id`, absence of
`request_id` from JSON, presence of `X-Request-ID`, and Cloud's mapping of
`received_at` to `gateway_received_at`. Cloud rejects missing and unknown fields
with `422`. A source-level boundary check confirms Cloud does not import Gateway
application models.

## M2-45 — Secure Gateway ↔ Cloud contract

The existing production integration suite in
`tests/integration/test_gateway_cloud_secure.py` already covers secure success,
business-value preservation, one bounded recovery for both `SESSION_INVALID`
and `SESSION_EXPIRED`, refusal of a second recovery, permanent rejection without
blind retry, bounded retry of 500/502/503/504-style failure, byte-identical
ambiguous retry, session-establishment failure, and fail-closed behavior without
a baseline call. `test_gateway_transport_interface.py` verifies application data
and request correlation cross the transport boundary separately without mutating
the canonical model. PR11 reuses these Member 3/4 integration tests rather than
duplicating crypto internals in Member 2 files.

## M2-46 — Failure propagation

`tests/integration/test_retry_amplification.py` exercises the real Legacy client,
Gateway route, and baseline retry implementation with deterministic Cloud
storage-unavailable responses. Gateway performs three Cloud attempts (initial
plus two retries), returns `503`, and the Legacy client performs its permitted
retry. The frozen sequence commit makes that retry a non-retryable `409`, so the
chain stops. The test checks statuses `[503, 409]`, backoffs, byte-identical Cloud
bodies, and Cloud request/failure/retry metrics.

## M2-47 — Retry amplification

The independent retry-loop upper bound is multiplicative:

```text
(Legacy retries + 1) × (Gateway Cloud retries + 1)
3 Gateway attempts × 3 Cloud attempts = 9 Cloud attempts
```

One test makes this theoretical bound executable with deterministic `503`
responses. The production-chain test also records the current practical result:
because sequence state commits before Cloud delivery, a repeated logical
measurement normally stops at `409` after the first Gateway request has already
made three Cloud attempts. The upper bound remains relevant for requests that
can enter both retry loops, configuration changes, or future protocol evolution.
No queue, rollback, or distributed retry coordinator is introduced.

## M2-48 — Validation cannot be bypassed

`test_gateway_validation_bypass.py` enables every configured Gateway failure
mode at rate one in both classical and ML-KEM modes. Domain-invalid input remains
`422`, neither transport is called, and no injected-failure metric increments.
Additional malformed and missing-field cases remain `400`/`422` under random
failure selection. This proves syntax, schema, and domain validation finish
before application or cryptographic failure hooks can run.

## Verification

Run the focused PR11 contract/failure scope from the repository root:

```bash
uv run pytest \
  edge_gateway/tests/test_gateway_sequence.py \
  edge_gateway/tests/test_gateway_measurements.py \
  edge_gateway/tests/test_gateway_routes.py \
  edge_gateway/tests/test_gateway_transport_interface.py \
  edge_gateway/tests/test_gateway_validation_bypass.py \
  edge_gateway/tests/test_secure_transport.py \
  tests/integration/test_legacy_gateway.py \
  tests/integration/test_gateway_cloud_baseline.py \
  tests/integration/test_gateway_cloud_secure.py \
  tests/integration/test_retry_amplification.py
```

The full repository suite, Ruff, AI-history validation, Graphify refresh, and
human review remain required before completion.
