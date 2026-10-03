# Gateway application failure injection — M2-20 through M2-25

The production Gateway app now executes M2-19's selected application fault in
both `classical` and `mlkem` modes. Defaults remain `FAILURE_MODE=none` and
`FAILURE_RATE=0.0`. These tasks implement roadmap Phase 18's application faults
and contribute to Member 2 Gate D; they do not complete all operations tasks.

## Important change in each task

| Task | Change | Legacy result |
|---|---|---|
| M2-20 | `processing_error` raises a safe application error after valid input and sequence commit, before Cloud work. The process stays healthy. | `500 INTERNAL_ERROR` |
| M2-21 | `processing_delay` awaits an asynchronous timer, then continues normal delivery. `FAILURE_DELAY_SECONDS` defaults to 2 and accepts finite values from 0 to 30 seconds. | `202` only after Cloud acceptance; delivery errors keep their existing mapping |
| M2-22 | `cloud_timeout` raises a simulated timeout at each measurement HTTP attempt, inside the existing transport retry loop. | `503 CLOUD_UNAVAILABLE` after exhaustion |
| M2-23 | `cloud_unavailable` raises a simulated HTTP 503 at that same boundary. | `503 CLOUD_UNAVAILABLE` after exhaustion |
| M2-24 | `drop_message` skips all Cloud work, including session establishment, and reports failure. | `503 CLOUD_UNAVAILABLE`, never false `202` |
| M2-25 | Safety checks cover disabled defaults, rate limits, seeded selection, isolated concurrent requests, startup warnings, safe logs, retries, and real Cloud persistence. | Normal validation, sequence, and delivery semantics preserved |

## Configure a local demonstration

Set variables in the Gateway process only, for example:

```bash
SECURITY_MODE=classical FAILURE_MODE=processing_error FAILURE_RATE=1 uv run edge-gateway
```

Use the same settings with `SECURITY_MODE=mlkem` to exercise the secure path.
For a delay, set `FAILURE_MODE=processing_delay FAILURE_DELAY_SECONDS=2`.
To restore normal delivery, restart with `FAILURE_MODE=none` or `FAILURE_RATE=0`.
The Cloud must be running in the matching security mode for successful delivery.
These are process-level settings; Compose service mapping remains Member 5-owned.

## Selection and execution boundaries

Only a schema/domain-valid request with an accepted sequence consumes a selection.
Malformed JSON remains `400`, invalid fields remain `422`, and duplicate/lower
sequences remain `409`. After sequence commit, the Gateway normalizes, creates a
request ID, and selects at most one application fault. `random` chooses only among
the five application modes above. A seed reproduces decisions for the same call
order, but concurrent scheduling can assign those decisions to different requests.

A selected transport fault persists for all attempts of that logical request;
it is not selected again on retries. The default two retries mean three attempts,
with existing 1- and 2-second backoff. All attempts use identical serialized bytes
and request ID; secure attempts also preserve the envelope, nonce, session, and
AAD. The hook does not run on public-key or session requests. If the secure
handshake fails first, that existing failure takes precedence and no simulated
measurement transport fault is counted.

Request-local context carries the decision into the existing delivery worker and
is reset on exit. No fault flags enter headers, canonical JSON, or SecureEnvelope.
The seeded simulation PRNG is separate from cryptographic randomness. The secure
transport only gains an optional callback before a measurement HTTP attempt;
Member 3's crypto/session algorithms and retry/recovery ownership are unchanged.
Custom transports supplied to `create_app` own their delivery behavior; the
production composition installs the callback on its built-in clients.

Sequence state records the last valid sequence observed, even when processing,
delivery, or intentional dropping fails. Retrying that same Legacy sequence gets
`409`; a higher sequence can proceed. A delayed request does not hold the sequence
lock or block the event loop. Client timeout/disconnection does not guarantee
cancellation: a delayed request may still reach Cloud later.

## Logs and metrics

Startup logs `WARNING event=failure_injection_enabled mode=...` for enabled
application faults. Execution logs `event=failure_injected failure_type=...
request_id=...`. Seed, measurement body, credentials, keys, and secret material
are omitted. The existing `gateway_injected_failures_total` family adds five
bounded `failure_type` values: `processing_error`, `processing_delay`,
`cloud_timeout`, `cloud_unavailable`, and `drop_message`.

Processing error, delay, and drop increment once per execution. Timeout and
unavailability increment once per simulated attempt, so a request exhausting two
retries increments by three. Selection alone does not increment counters.
The metric family is rendered once through the existing Gateway registry.

## Verification and limits

```bash
uv run pytest edge_gateway/tests/test_gateway_failure_injector.py edge_gateway/tests/test_gateway_application_failures.py edge_gateway/tests/test_gateway_application_failures_integration.py
```

The tests cover both security modes, byte-identical retries and backoff, input
rejection before injection, retained sequence state, delay ordering, disabled
faults, startup logs, safe errors, and concurrent worker isolation. Live tests use
production Cloud routes and temporary SQLite to verify acceptance/persistence,
no measurement forwarding for selected failures, and no plaintext fallback.
Timeout/unavailability are local simulations before a network send; they do not
simulate a response lost after persistence. Existing transport tests cover real
HTTP failures and secure retry/recovery. No deployment performance is claimed.
