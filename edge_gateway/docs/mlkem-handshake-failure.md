# ML-KEM handshake failure demonstration

This note records one local run of the existing handshake fault. It does not add a metric.

The Gateway is in `SECURITY_MODE=mlkem` with `FAILURE_MODE=mlkem_handshake_failure` and `FAILURE_RATE=1.0`. Cloud is running, and a baseline transport is available to the process. The Legacy route posts one measurement for device `sensor-001`, temperature 22.5, humidity 44.0, and sequence number 1.

The fault is applied before the Gateway fetches Cloud's public key. No session is created, and the measurement is not sealed. The Legacy response is `503 CLOUD_UNAVAILABLE` and does not contain a session identifier.

The Gateway scrape:

```text
gateway_mlkem_handshakes_total{result="success"} 0
gateway_mlkem_handshakes_total{result="failure"} 1
gateway_mlkem_handshake_failures_total{reason="injected"} 1
gateway_injected_failures_total{failure_type="mlkem_handshake_failure"} 1
gateway_active_session 0
gateway_encryption_failures_total 0
gateway_pqc_fallback_total 0
```

Cloud received no session request and stored no measurement:

```text
cloud_mlkem_sessions_created_total 0
cloud_measurements_stored_total 0
cloud_decryption_failures_total 0
```

The measurement table contains 0 rows. The baseline transport was not called.

The collector is `test_handshake_failure_stays_closed_without_a_session` in `tests/integration/test_mlkem_handshake_failure_demo.py`.
