# PQC observability demonstration

This note records one local run of the existing Gateway PQC metrics. It does not add a metric.

The Gateway is in `SECURITY_MODE=mlkem`. One `PqcMetrics` registry is shared by the session manager, the secure transport, and `GET /metrics`. Cloud serves the production public-key, session, and secure-measurement routes. The Legacy route accepts four measurements for device `sensor-001`, temperature 22.5, humidity 44.0, and sequence numbers 1 through 4.

After the first measurement the scrape shows one successful handshake and no reused delivery:

```text
gateway_mlkem_handshakes_total{result="success"} 1
gateway_mlkem_handshakes_total{result="failure"} 0
gateway_active_session 1
gateway_pqc_fallback_total 0
gateway_session_reestablishments_total{result="success"} 0
gateway_secure_message_duration_seconds_count{phase="first"} 1
gateway_secure_message_duration_seconds_count{phase="steady"} 0
```

Measurements 2 and 3 reuse that session. The handshake counter stays at 1, and those two deliveries are steady-state:

```text
gateway_mlkem_handshakes_total{result="success"} 1
gateway_active_session 1
gateway_secure_message_duration_seconds_count{phase="first"} 1
gateway_secure_message_duration_seconds_count{phase="steady"} 2
```

The Gateway clock is then set to the held session `expires_at`. Measurement 4 establishes a new handshake. That increment is `gateway_mlkem_handshakes_total`, not `gateway_session_reestablishments_total`, because the session expired locally before delivery. The delivery phase is chosen before the session is opened, so this measurement is counted as steady while the handshake counter moves to 2:

```text
gateway_mlkem_handshakes_total{result="success"} 2
gateway_mlkem_handshakes_total{result="failure"} 0
gateway_session_reestablishments_total{result="success"} 0
gateway_session_reestablishments_total{result="failure"} 0
gateway_active_session 1
gateway_pqc_fallback_total 0
gateway_secure_message_duration_seconds_count{phase="first"} 1
gateway_secure_message_duration_seconds_count{phase="steady"} 3
```

The scrape has no session identifier and no request identifier. Duration samples are present and are not a performance limit. `gateway_pqc_fallback_total` stays 0.

The collector is `test_handshake_counter_shows_reuse_then_expiry` in `tests/integration/test_pqc_observability.py`.
