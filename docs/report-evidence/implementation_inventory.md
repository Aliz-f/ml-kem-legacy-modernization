# Implementation inventory (audited 2026-10-09)

| Area | Status | Evidence |
| --- | --- | --- |
| Legacy API, validation, sequencing, and 202-after-Cloud acceptance | IMPLEMENTED | `edge_gateway/src/edge_gateway/app.py`, `tests/integration/test_end_to_end.py` |
| Explicit classical and ML-KEM dispatch | IMPLEMENTED | `edge_gateway/src/edge_gateway/dispatch.py`, `docs/architecture/04 - Shared Cross-Component Protocol Specification.md` |
| ML-KEM-768 / HKDF-SHA-256 / AES-256-GCM secure path | IMPLEMENTED | `edge_gateway/src/edge_gateway/crypto/`, `cloud_service/src/cloud_service/crypto/` |
| Fail-closed security policy and bounded retry/recovery | IMPLEMENTED | `edge_gateway/src/edge_gateway/crypto/secure_transport.py`, `tests/integration/test_mlkem_handshake_failure_demo.py` |
| SQLite idempotency and query API | IMPLEMENTED | `cloud_service/src/cloud_service/storage/`, `tests/integration/test_modernized_end_to_end.py` |
| Metrics, health, readiness | IMPLEMENTED | component `app.py` and `metrics.py`; `tests/integration/test_metrics_sanity.py` |
| Fault injection | IMPLEMENTED | `edge_gateway/src/edge_gateway/failure/`, `cloud_service/src/cloud_service/failure.py`, integration tests |
| CPU/memory measurement | NOT IMPLEMENTED | No resource sampler in existing or added harness |
| 20 cold-session observations | PARTIALLY IMPLEMENTED | Collector produced three; target not met |
| TLS/mTLS/pinning/signed Cloud-key distribution | NOT IMPLEMENTED | Frozen-design limitation: `docs/technical-debt.md` TD-6/TD-7 |
| Dedicated cryptographic replay protection | NOT IMPLEMENTED | Frozen v1 limitation: `docs/technical-debt.md` TD-11 |
