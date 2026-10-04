# Failure simulation validation in real system (M1-17)

This record implements Member 1 task **M1-17: Validate failure simulation in real
system**. It provides concrete evidence demonstrating that the Legacy Device's
failure simulation subsystem operates in accordance with the frozen protocol
specification and Edge Gateway validation contracts.

---

## 1. How to reproduce

From the repository root with the locked development environment installed:

```bash
uv run pytest legacy_system/tests/test_failure_simulation.py -v
```

This executes the automated failure simulation test suite covering every mode
in the demonstration matrix, wire syntax errors, deterministic random mode,
structured logging assertions, and continuous runtime loop execution under
fault injection.

---

## 2. Failure simulation demonstration matrix

| Failure mode | Injected fault condition | Gateway status | Client attempts | Client retries | Outcome | Cloud contacted? |
| --- | --- | :---: | :---: | :---: | --- | :---: |
| `none` | Clean, valid sensor measurement | `202 Accepted` | 1 | 0 | Accepted & forwarded | Yes (normal delivery) |
| `invalid_temperature` | `temperature_c = 150.0` (> 85.0 °C limit) | `422 Unprocessable` | 1 | 0 | Rejection without retry | No |
| `invalid_humidity` | `humidity_pct = -10.0` (< 0.0 % limit) | `422 Unprocessable` | 1 | 0 | Rejection without retry | No |
| `missing_field` | Removed `timestamp` field | `422 Unprocessable` | 1 | 0 | Rejection without retry | No |
| `invalid_timestamp` | Non-ISO timestamp string (`"invalid-iso"`) | `422 Unprocessable` | 1 | 0 | Rejection without retry | No |
| `duplicate_sequence` | Repeated previous `sequence_number` | `409 Conflict` | 1 | 0 | Rejection without retry | No |
| `out_of_order_sequence` | Lower `sequence_number` than seen | `409 Conflict` | 1 | 0 | Rejection without retry | No |
| `random` (seed `12345`) | Controlled mixture of valid and faulty | `202` / `409` / `422` | 1 per req | 0 | Mixed, deterministic | Only for `202` |
| *(Wire syntax control)* | Unparseable JSON body (`{"unclosed`) | `400 Bad Request` | 1 | 0 | Rejection without retry | No |

---

## 3. Key protocol boundaries verified

### A. HTTP status code distinction
- **Malformed / unparseable JSON syntax (`400 Bad Request`):** The body fails syntax parsing before schema validation.
- **Parsed JSON with missing, wrongly-typed, or domain-invalid fields (`422 Unprocessable Entity`):** The body is valid JSON syntax, but violates domain constraints (missing required field, out-of-range physical reading, non-ISO timestamp).
- **Sequence violations (`409 Conflict`):** The payload is valid, but the sequence number is a duplicate or lower than previously accepted values for that device ID.

### B. Client retry restraint
- For all `4xx` responses (`400`, `409`, `422`), `GatewayClient.send()` classifies the error as non-retryable (`retryable = False`).
- The client performs **exactly 1 attempt** and **0 retries**, preventing retry storms against deterministic rejections.
- Bounded retries are strictly reserved for transient/network errors (`500`, `502`, `503`, `504`, connection timeout, connection refused).

### C. Domain model separation
- Fault injection is applied strictly to the **serialized outgoing payload** (a Python `dict`), never to the internal validated `Measurement` dataclass.
- Faulty states (`missing_field`, `invalid_timestamp`, out-of-range sensor readings) cannot corrupt the domain object representation.

### D. Operational logging
- When a failure is rejected, the client logs a structured event at `WARNING` level:
  ```text
  event=gateway_request_failed component=legacy_system device_id=sensor-log-test sequence_number=0 status_code=422 attempt=1 error_category=http
  ```
- The Legacy Device runtime loop (`DeviceController`) handles rejections gracefully, logging the failure without crashing, and continues monotonic sequence generation for subsequent cycles.
