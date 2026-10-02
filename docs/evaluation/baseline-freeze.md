# Classical baseline freeze

This record implements Member 5 task M5-30. It freezes the verified
classical-mode reference point used for later modernized-mode comparison. It
does not claim that the system has been deployed or that a cryptographic
modernization benchmark has been completed.

## Freeze designation

The designated local Git tag is `baseline-classical-complete`. It must name the
reviewed commit containing this record and the completed baseline integration
work. The tag is created only after the required human review and final
verification; it is not a replacement for a reviewed commit.

## Frozen baseline contract

| Item | Baseline value |
| --- | --- |
| Gateway security mode | `SECURITY_MODE=classical` |
| Legacy endpoint | `POST /api/v1/measurements` |
| Gateway-to-Cloud endpoint | `POST /api/v1/baseline/measurements` |
| Correlation | Gateway-generated ID in `X-Request-ID`; not in canonical JSON |
| Persistence identity | `UNIQUE(device_id, sequence_number)` |
| Success timing | Gateway returns Legacy `202` only after Cloud acceptance/persistence |

The baseline exists for comparison. It does not activate ML-KEM, sessions,
AES-GCM, a plaintext fallback, or a separate cryptographic replay mechanism.

## Verified baseline evidence

The root integration suite now separates and composes the three actual
boundaries:

- `tests/integration/test_legacy_gateway.py` verifies the Legacy serializer and
  HTTP client against a live Gateway, including the frozen `400`, `422`, and
  `409` rejection behavior.
- `tests/integration/test_gateway_cloud_baseline.py` verifies the real Gateway
  baseline client against a live Cloud service, including canonical JSON,
  header-only correlation, idempotency, and storage mapping.
- `tests/integration/test_end_to_end.py` verifies the deterministic Legacy
  measurement flows through live Gateway and Cloud services to a queried SQLite
  row, including the received-time, Cloud-time, gateway identity, record ID,
  and Cloud correlation assertions.

Before this record, the full repository suite passed with **1,288 tests**.
The root baseline E2E test uses the frozen fixture `sensor-test`, 22.5 °C,
44.0 %, `2026-09-21T12:00:00Z`, sequence 1, and a fresh file-backed SQLite
database.

## Existing measurement evidence

The measured Gateway-route baseline is retained in
[`edge_gateway/docs/baseline-measurements.md`](../../edge_gateway/docs/baseline-measurements.md).
Its recorded local healthy workload used 100 sequential classical-mode Legacy
requests, accepted all 100, persisted 100 rows, and observed a 2.212 ms mean
Gateway accepted-request duration and 1.905 ms mean Cloud-delivery duration.
The same record documents its machine, workload, instrumentation, and failure
control. These numbers are observations, not performance requirements or a
production capacity claim.

## Known limitations at freeze

- Measurements use local loopback services and disposable SQLite files; Docker
  Compose and a deployed test environment are not yet part of this milestone.
- The Gateway `/ready` endpoint remains a known later operational task; the
  baseline test verifies synchronous delivery rather than deployment readiness.
- Results are a classical reference only. A valid ML-KEM comparison must use an
  equivalent workload and separately report first-message/session-establishment
  overhead.
- Business idempotency prevents duplicate logical rows but is not dedicated
  cryptographic replay protection.

## Reproduce the freeze checks

```bash
uv run pytest tests/integration/test_legacy_gateway.py
uv run pytest tests/integration/test_gateway_cloud_baseline.py
uv run pytest tests/integration/test_end_to_end.py
uv run pytest
uv run ruff check .
uv run ai-history check
```

The commit/tag action follows the required human review and final-verification
workflow. It must not tag an earlier commit that omits the reviewed baseline
artifacts.
