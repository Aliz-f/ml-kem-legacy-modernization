# Corrupted ciphertext demonstration

This note records one local run of the existing ciphertext-corruption fault. It does not add a metric.

The Gateway is in `SECURITY_MODE=mlkem` with `FAILURE_MODE=corrupt_ciphertext` and `FAILURE_RATE=1.0`. Cloud serves the production public-key, session, and secure-measurement routes. The Legacy route posts one measurement for device `sensor-001`, temperature 22.5, humidity 44.0, and sequence number 1.

The Gateway establishes a session and seals that measurement. The seal succeeds, so the local encryption-failure counter stays 0. The injector then flips one bit in a copy of the ciphertext and sends that copy. Cloud authentication fails. The Legacy response is `503 CLOUD_UNAVAILABLE` and does not contain the session or the ciphertext.

Cloud's scrape after the rejection:

```text
cloud_decryption_failures_total 1
cloud_authenticated_messages_total 0
cloud_measurements_stored_total 0
```

The Gateway scrape shows the applied fault and no plaintext fallback:

```text
gateway_mlkem_handshakes_total{result="success"} 1
gateway_encryption_failures_total 0
gateway_injected_failures_total{failure_type="corrupt_ciphertext"} 1
gateway_pqc_fallback_total 0
```

The Cloud measurement table contains 0 rows. The session remains active because this rejection is not `409 SESSION_INVALID` or `409 SESSION_EXPIRED`.

The collector is `test_corrupted_ciphertext_is_rejected_and_not_stored` in `tests/integration/test_corrupt_ciphertext_demo.py`.
