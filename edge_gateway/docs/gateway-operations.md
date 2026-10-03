# Gateway health, readiness, and application logging — M2-29 through M2-33

This note defines Member 2 PR8 behavior. It does not change the frozen protocol
or move cryptographic logging from Member 3.

For application/Cloud metrics, the 16 KiB Legacy body limit, and lifecycle
cleanup, see [PR9 metrics and operations](gateway-pr9.md).

## M2-29 — Liveness

`GET /health` returns `200 {"status":"ok"}` while the application lifespan is
running. The check has no Cloud, session, or transport dependency. It therefore
answers whether the Gateway process can serve requests, rather than whether a
measurement can currently reach Cloud.

## M2-30 and M2-31 — Readiness

`GET /ready` checks local application and transport initialization. A ready
response is:

```json
{"status":"ready","security_mode":"mlkem"}
```

Classical mode requires an initialized baseline client. ML-KEM mode requires an
initialized, open `SecureTransport`. Readiness never requires an active ML-KEM
session because sessions are established lazily on the first delivery. It also
does not probe Cloud or establish a session as a side effect.

This local policy keeps readiness safe and deterministic. A ready Gateway can
still return `503 CLOUD_UNAVAILABLE` for a later measurement if Cloud is
unreachable. Responses expose only the status and configured security mode.

## M2-32 — Structured application events

The Gateway emits allowlisted event names and bounded correlation fields:

| Area | Events |
| --- | --- |
| Lifecycle | `gateway_starting`, `gateway_ready`, `gateway_shutting_down`, `gateway_startup_failed`, `gateway_internal_error` |
| Legacy input | `legacy_measurement_received`, `legacy_validation_failed` |
| Processing | `gateway_request_created`, `canonical_measurement_created` |
| Sequence policy | `sequence_duplicate_detected`, `sequence_out_of_order_detected`, `sequence_gap_detected` |
| Cloud delivery | `cloud_delivery_started`, `cloud_delivery_retry`, `cloud_delivery_succeeded`, `cloud_delivery_failed` |
| Failure simulation | `failure_injected` |

Useful safe fields include request, device, Gateway, and sequence identifiers;
security mode; status; delivery attempt; and stable failure reasons. Retry
events describe attempts already permitted by each transport's existing retry
policy. Cryptographic lifecycle events remain in Member 3's security logger.

## M2-33 — Privacy review

The application logger accepts only named fields whose values are bounded
integers or simple tokens. It omits unknown fields and values containing spaces,
line breaks, or other unsafe characters. Application logs do not contain
request bodies, temperature or humidity values, measurement timestamps, raw
headers, exception text, environment values, credentials, failure seeds, URLs,
keys, ciphertext, shared secrets, session keys, or nonces. A device identifier
that cannot be represented safely is omitted rather than normalized or logged.

IDs may appear in logs for request correlation. Metrics continue to use bounded
labels and do not use request, device, or session identifiers.

## Verification

Run the focused operational checks from the repository root:

```bash
uv run pytest edge_gateway/tests/test_gateway_app.py \
  edge_gateway/tests/test_gateway_operations.py \
  edge_gateway/tests/test_gateway_sequence.py \
  edge_gateway/tests/test_baseline_client.py \
  edge_gateway/tests/test_secure_transport.py
```
