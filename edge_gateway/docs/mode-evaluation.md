# Baseline versus modernized evaluation

This note records one local sample. It does not rank the modes, and it does not set a performance limit.

The production Legacy route still stops before delivery, so the sample calls `CloudDispatch` rather than that route. Both modes send the same four measurements: device `sensor-001`, temperature 22.5, humidity 44.0, and sequence numbers 1 through 4. Classical mode posts the canonical JSON to Cloud's baseline route. Modernized mode uses `SecureTransport` against Cloud's production public-key, session, and secure-measurement routes. The first secure request is reported separately because it includes session establishment.

The Gateway does not yet have its own baseline HTTP client. The classical timing is the `CloudDispatch` call that posts the canonical measurement. A fifth modernized measurement is sent only after Cloud invalidates the session, so the re-establishment count is separate from the four-message workload.

## One local sample

| Measurement | Value |
| --- | --- |
| Classical first request | 13.012 ms |
| Classical steady-state mean, requests 2-4 | 1.390 ms |
| Classical canonical JSON size | 192 bytes |
| ML-KEM handshake duration | 13.542 ms |
| ML-KEM encapsulation duration | 0.259 ms |
| First secure-message latency | 15.871 ms |
| Steady-state secure-message mean, requests 2-4 | 1.253 ms |
| SecureEnvelope size | 455 bytes |
| Session reuse count | 3 |
| Session re-establishment count | 1 |
| Handshakes in the four-message workload | 1 |
| Handshakes after the invalidation retry | 2 |
| Plaintext fallback count | 0 |
| Baseline calls during mlkem delivery | 0 |

Session reuse count 3 means requests 2, 3, and 4 used the session from request 1. The re-establishment count is the one replacement handshake after Cloud returned `409 SESSION_INVALID`. That replacement is not included in the steady-state mean.

## Injected failures

`FAILURE_MODE=mlkem_handshake_failure` with `FAILURE_RATE=1.0` raises `SecureTransportError` before a session exists. `FAILURE_MODE=corrupt_ciphertext` with `FAILURE_RATE=1.0` mutates the ciphertext copy and Cloud rejects the envelope. In both cases the baseline transport is not called, `pqc_fallback_total` stays 0, and `secure_failures_total` is 1.

The collector is `measure_modes` in `tests/integration/test_mode_evaluation.py`.
