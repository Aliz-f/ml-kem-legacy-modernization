# Gateway security technical debt

This register records the security limits Member 3 keeps for the course system. Each row names the debt, the risk, and a future improvement. These future improvements are recorded only. This course system does not add TLS, a persistent session store, an HSM, a replay window, or automated key rotation.

The canonical design already lists several of these limits in Edge Gateway design section 84 and in [security.md](security.md). This note is the Member 3 register. It does not change the protocol.

| Technical debt | Risk | Future improvement |
| --- | --- | --- |
| Simplified Cloud public-key trust | MITM/key substitution risk | TLS/PKI/key pinning |
| In-memory sessions | restart loses state | secure persistent session strategy |
| Ephemeral Cloud key | identity changes on restart | persistent secure key storage |
| No HSM | keys remain process-memory software keys | HSM/KMS |
| No dedicated cryptographic anti-replay counter/window | authenticated envelopes can be replayed at crypto layer | per-session counters / replay window |
| Application-level crypto over test HTTP | no transport identity | TLS/mTLS |
| Simple key rotation | limited lifecycle | automated rotation |
| Python memory cannot guarantee zeroization | residual key-memory risk | lower-level secure key handling |

Cloud business idempotency prevents duplicate logical rows, but it is not a replacement for cryptographic replay protection. Persistence is unique on `(device_id, sequence_number)`. Protocol version 1 has no message counter and no replay window.

## Where the limits are now

Simplified Cloud public-key trust is the configured `CLOUD_URL`. ML-KEM does not authenticate Cloud identity. `edge_gateway/docs/transport-trust.md` records the unauthenticated HTTP substitution risk.

In-memory sessions are the Gateway `SessionManager` in `edge_gateway/src/edge_gateway/crypto/session.py` and the Cloud `SessionManager` in `cloud_service/src/cloud_service/crypto/session.py`. A process restart drops both. The Cloud session module states that it has no persistence, counters, or replay window.

The ephemeral Cloud key is one ML-KEM-768 key pair per Cloud process. `cloud_service/src/cloud_service/crypto/keys.py` generates `key_id` with `uuid4` and keeps the private key in that process. A restart creates a new identity.

No HSM means the private key, the shared secret, and the session key are software keys in process memory.

No dedicated cryptographic anti-replay counter/window means a previously accepted SecureEnvelope can still authenticate. Business idempotency stops a duplicate measurement row. It does not reject the cryptographic replay. `edge_gateway/src/edge_gateway/crypto/envelope.py` has no `message_counter`.

Application-level crypto over test HTTP means AES-256-GCM protects the measurement body. The course test environment, including Docker, may use HTTP. TLS and mTLS are not part of this implementation.

Simple key rotation means the Cloud key lives for one process and sessions last 300 seconds. There is no automated rotation service.

Python memory cannot guarantee zeroization. Replacing or closing a session overwrites the session-key buffer and drops the object. `edge_gateway/src/edge_gateway/crypto/session.py` states that Python does not guarantee secure memory zeroization.
