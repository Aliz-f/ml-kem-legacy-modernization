# Gateway and Cloud metrics contract

This Member 5 contract implements M5-52, M5-53, and M5-55. It defines the
minimum metric families that component owners implement and Member 5 validates.
It does not claim that every family is already emitted: the current Gateway
endpoint has service/PQC metrics and the current Cloud endpoint has service
information; remaining families are component-owned follow-up work.

Metrics use Prometheus naming conventions. A `_total` family is a counter,
`_duration_seconds` is a histogram/summary duration family, and active-session
families are gauges. Metrics must never contain secret material.

## Gateway minimum families

| Metric | Type | Meaning |
|---|---|---|
| `gateway_measurements_received_total` | Counter | Legacy measurements received at the Gateway boundary. |
| `gateway_measurements_accepted_total` | Counter | Measurements accepted for Cloud delivery. |
| `gateway_measurements_rejected_total` | Counter | Measurements rejected by validation or sequence policy. |
| `gateway_duplicate_measurements_total` | Counter | Equal per-device sequence rejections. |
| `gateway_out_of_order_measurements_total` | Counter | Lower per-device sequence rejections. |
| `gateway_sequence_gaps_total` | Counter | Accepted higher sequence values that reveal a gap. |
| `gateway_cloud_requests_total` | Counter | Gateway-to-Cloud send attempts. |
| `gateway_cloud_failures_total` | Counter | Failed Gateway-to-Cloud attempts. |
| `gateway_cloud_retries_total` | Counter | Bounded ordinary transport retry attempts. |
| `gateway_cloud_request_duration_seconds` | Duration | Gateway-to-Cloud request duration. |
| `gateway_mlkem_handshakes_total` | Counter | Successful or attempted ML-KEM handshakes, with a bounded result label if needed. |
| `gateway_mlkem_handshake_failures_total` | Counter | Failed ML-KEM handshake attempts. |
| `gateway_mlkem_handshake_duration_seconds` | Duration | ML-KEM session-establishment duration. |
| `gateway_session_reestablishments_total` | Counter | Bounded replacement-session attempts after session recovery. |
| `gateway_encryption_failures_total` | Counter | Secure-envelope encryption failures. |
| `gateway_active_session` | Gauge | Whether one active Gateway secure session exists. |
| `gateway_pqc_fallback_total` | Counter | Must remain `0` in protocol v1: runtime plaintext fallback is prohibited. |
| `gateway_injected_failures_total` | Counter | Local Gateway fault-injection events. |

## Cloud minimum families

| Metric | Type | Meaning |
|---|---|---|
| `cloud_baseline_requests_total` | Counter | Baseline measurement requests received. |
| `cloud_secure_requests_total` | Counter | Secure-envelope requests received. |
| `cloud_secure_requests_rejected_total` | Counter | Secure requests rejected before acceptance/storage. |
| `cloud_request_duration_seconds` | Duration | Cloud request-processing duration. |
| `cloud_mlkem_sessions_created_total` | Counter | Secure sessions successfully created. |
| `cloud_mlkem_session_failures_total` | Counter | Failed session-establishment attempts. |
| `cloud_mlkem_decapsulation_duration_seconds` | Duration | ML-KEM decapsulation duration. |
| `cloud_active_sessions` | Gauge | Number of currently active in-memory secure sessions. |
| `cloud_expired_sessions_total` | Counter | Sessions expired by access or cleanup. |
| `cloud_authenticated_messages_total` | Counter | Secure envelopes authenticated and decrypted. |
| `cloud_decryption_failures_total` | Counter | Secure-envelope authentication/decryption failures. |
| `cloud_measurements_stored_total` | Counter | Newly stored logical measurements. |
| `cloud_storage_failures_total` | Counter | Storage operation failures. |
| `cloud_duplicate_measurements_total` | Counter | Idempotent duplicate logical measurements. |
| `cloud_injected_failures_total` | Counter | Local Cloud fault-injection events. |

## Cardinality and label review

Labels are optional and must be finite, low-cardinality enumerations. Accepted
examples are `result`, `failure_type`, `security_mode`, and `phase`; a bounded
handshake `reason` may be used only when its values are an explicit finite
application enum. Labels must not change the semantic meaning of the metric.

Reject any label that contains an identifier, per-request value, timestamp,
payload value, or secret. In particular, do not use `request_id`, `session_id`,
`record_id`, `device_id`, `gateway_id`, `key_id`, nonce, ciphertext, or message
contents as labels. Correlation belongs in logs, not metrics.

Before adding a label, the component owner documents its finite value set and
Member 5 reviews whether its cardinality remains bounded. M5-54 verifies metric
changes under real request/failure flows; this contract alone does not do so.
