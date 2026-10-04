# Network and transient failure behavior (M1-18)

This record implements Member 1 task **M1-18: Review network-failure behavior**.
It verifies that the Legacy Device HTTP client and runtime loop rigorously
distinguish between permanent **data failures** and transient **network or
server failures**, applying protocol-compliant bounded retry policies.

---

## 1. How to reproduce

From the repository root with the locked development environment installed:

```bash
uv run pytest legacy_system/tests/test_network_failures.py -v
```

This suite executes tests across connection refusal, timeouts, server errors
(`500`, `502`, `503`, `504`), eventual recovery, classification matrices, and
monotonic sequence progression through retry exhaustion.

---

## 2. Data failures vs. Network/transient failures

The Legacy Device architecture enforces a clear boundary between failure types:

| Failure category | Trigger conditions | Protocol status codes | Client retry policy | Max attempts | Backoff behavior |
| --- | --- | :---: | :---: | :---: | --- |
| **Data failure** | Malformed syntax, missing field, out-of-range sensor reading, duplicate/out-of-order sequence | `400`, `409`, `422` | **Non-retryable** (`retryable = False`) | 1 | None (immediate failure return) |
| **Network failure** | Gateway unreachable, connection refused, TCP reset, DNS failure | `None` (`ErrorCategory.CONNECTION`) | **Retryable** (`retryable = True`) | `1 + MAX_RETRIES` (3 default) | Exponential: $2^{\text{attempt}-1}$ (1s, 2s) |
| **Timeout failure** | Slow Gateway response exceeding `REQUEST_TIMEOUT_SECONDS` | `None` (`ErrorCategory.TIMEOUT`) | **Retryable** (`retryable = True`) | `1 + MAX_RETRIES` (3 default) | Exponential: $2^{\text{attempt}-1}$ (1s, 2s) |
| **Server failure** | Downstream failure, transient Gateway error, service restart | `500`, `502`, `503`, `504` | **Retryable** (`retryable = True`) | `1 + MAX_RETRIES` (3 default) | Exponential: $2^{\text{attempt}-1}$ (1s, 2s) |

---

## 3. Verified failure scenarios

### A. Gateway stopped / connection refused
- **Trigger:** Gateway process stopped or port closed.
- **Client Behavior:** Caught as socket / connection error (`ErrorCategory.CONNECTION` or `ErrorCategory.TIMEOUT`).
- **Retries:** Client performs up to `MAX_RETRIES` (default 2 retries, 3 total attempts) with exponential backoffs ($1\text{s}, 2\text{s}$).
- **Outcome:** `GatewayResult.success = False`, `retryable = True`.

### B. Gateway slow / request timeout
- **Trigger:** Gateway response delayed beyond `REQUEST_TIMEOUT_SECONDS`.
- **Client Behavior:** `TimeoutError` / `socket.timeout` caught and classified as `ErrorCategory.TIMEOUT`.
- **Retries:** Retried with exponential backoff up to `MAX_RETRIES`.
- **Outcome:** Protects client from unbounded blocking.

### C. Server-side failures (`500`, `502`, `503`, `504`)
- **Trigger:** Gateway returns standard transient 5xx HTTP response codes.
- **Client Behavior:** Classified as `ErrorCategory.HTTP` with `retryable = True`.
- **Retries:** Full retry sequence attempted up to `MAX_RETRIES`.

### D. Eventual recovery on retry
- **Trigger:** Gateway fails initial attempts (e.g., returns `503`), but recovers within retry limits (returns `202 Accepted` on attempt 3).
- **Client Behavior:** Logs intermediate warnings (`event=gateway_retry`), but ultimately logs success (`event=measurement_delivered`).
- **Outcome:** Clean delivery without declaring permanent failure.

### E. Retry exhaustion and sequence continuity
- **Trigger:** Gateway remains unreachable across all retry attempts.
- **Client Behavior:** Client logs `event=measurement_delivery_failed` at `WARNING` level with `attempt=3`.
- **Runtime Policy:** The failed measurement is discarded. The sensor does **not** rewind sequence numbers, nor does it block indefinitely. The next cycle reads a fresh measurement with monotonically incremented sequence number (`seq=0` $\rightarrow$ `seq=1`).
