# Gateway test-suite hardening — M2-38 through M2-41

This Member 2 PR11 audit maps the frozen test requirements to maintained tests.
It extends the existing suite rather than renaming or duplicating established
files. Files use the repository's `test_gateway_*` convention where the shorter
names suggested by M2-38 would be ambiguous with Cloud or Member 3 tests.

## M2-38 — Unit-test suite

| Area | Maintained tests |
| --- | --- |
| Configuration | `test_gateway_config.py` |
| Legacy and canonical models | `test_gateway_models.py`, `test_gateway_canonical_model.py` |
| Syntax, schema, and domain validation | `test_gateway_validation.py` |
| Normalization | `test_gateway_normalization.py` |
| Sequence policy and concurrency | `test_gateway_sequence.py`, `test_gateway_measurements.py` |
| Legacy HTTP route | `test_gateway_routes.py`, `test_gateway_measurements.py` |
| Baseline Cloud client | `test_baseline_client.py` |
| Failure injection | `test_gateway_failure_injector.py`, `test_gateway_application_failures.py` |
| Health, readiness, logging | `test_gateway_app.py`, `test_gateway_operations.py` |
| Metrics and request limits | `test_gateway_application_metrics.py`, `test_gateway_request_size.py` |
| Lifecycle | `test_gateway_shutdown.py`, `test_secure_shutdown.py` |

Member 3's crypto/session/envelope tests remain in their existing focused files.
PR11 does not change ownership or cryptographic behavior.

## M2-39 — Route contract

`test_gateway_routes.py` provides one reviewable matrix for valid delivery,
malformed JSON, a missing field, invalid temperature, humidity, timestamp and
negative sequence, duplicate and out-of-order sequences, Cloud acceptance, and
Cloud failure. Its injected transport makes outbound behavior explicit: invalid
or sequence-rejected requests never reach Cloud, and `202` follows a valid
acceptance only. The Cloud-failure case also verifies the frozen sequence commit
timing by showing that the repeated sequence becomes a `409` duplicate.

The broader `test_gateway_measurements.py` suite covers both security modes,
canonical values, request-ID creation, malformed/unconfirmed responses, internal
failures, pending delivery, and fail-closed secure unavailability.

## M2-40 — Exact validation boundaries

`test_gateway_validation.py` exercises the named inclusive boundaries exactly:

```text
temperature: -40 and 85 valid; -40.01 and 85.01 invalid
humidity:       0 and 100 valid;   -0.1 and 100.1 invalid
```

It also checks nearby decimal values, device IDs, UTC timestamps, non-negative
sequences, syntax versus parsed-schema errors, absence of outbound network calls,
and secret-safe errors. The tests assert that valid values are not normalized or
mutated by validation.

## M2-41 — Sequence policy and state timing

`test_gateway_sequence.py` covers first values, increment by one, gaps,
duplicates, older values, independent devices, rejected-state stability,
process-local restart behavior, concurrent equal values, concurrent different
values, Cloud failure after commit, and a pending failure alongside a newer
sequence. `test_gateway_measurements.py` verifies the same policy through the
HTTP application: schema/domain-invalid input does not poison state; duplicate
and out-of-order requests do not move it backward; gaps advance it; Cloud
failure does not roll it back; and same-device requests remain responsive while
one delivery is pending.

The frozen order remains:

```text
schema/domain validation
→ sequence check and commit
→ normalization and request ID
→ Cloud delivery
```

No test requires or introduces sequence rollback after a Cloud failure.

## Verification

Run the Member 2 PR11 scope from the repository root:

```bash
uv run pytest \
  edge_gateway/tests/test_gateway_config.py \
  edge_gateway/tests/test_gateway_models.py \
  edge_gateway/tests/test_gateway_canonical_model.py \
  edge_gateway/tests/test_gateway_validation.py \
  edge_gateway/tests/test_gateway_normalization.py \
  edge_gateway/tests/test_gateway_sequence.py \
  edge_gateway/tests/test_gateway_routes.py \
  edge_gateway/tests/test_gateway_measurements.py \
  edge_gateway/tests/test_baseline_client.py \
  edge_gateway/tests/test_gateway_failure_injector.py \
  edge_gateway/tests/test_gateway_application_failures.py \
  edge_gateway/tests/test_gateway_app.py \
  edge_gateway/tests/test_gateway_operations.py \
  edge_gateway/tests/test_gateway_application_metrics.py \
  edge_gateway/tests/test_gateway_request_size.py \
  edge_gateway/tests/test_gateway_shutdown.py
```

The full repository suite, Ruff, AI-history validation, Graphify refresh, and
human review remain required before completion.
