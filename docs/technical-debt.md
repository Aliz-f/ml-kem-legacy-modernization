# Project-wide technical-debt register

This is the Member 5 coordination register for M5-81. It consolidates known,
accepted course-system limitations; it does not authorize changes to the frozen
protocol or implementation. Risk events and their current controls are tracked
separately in the [risk register](risk-register.md).

| ID | Debt | Component | Consequence / risk | Why accepted now | Future improvement |
|---|---|---|---|---|---|
| TD-1 | No authentication on the Legacy Device → Gateway HTTP/JSON boundary | Legacy Device, Gateway | A party able to reach the Gateway can spoof or alter legacy traffic. | The boundary intentionally represents a legacy protocol in the controlled course environment. | Define an authenticated migration path for devices. |
| TD-2 | No persistent Gateway queue or store-and-forward buffer | Gateway | A downstream outage can make an accepted sequence unavailable for later delivery; a process restart loses unsent work. | The frozen Gateway returns `202` only after Cloud acceptance and keeps the system course-sized. | Redesign delivery/acceptance semantics with durable buffering. |
| TD-3 | Gateway sequence state is in memory | Gateway | Restart loses duplicate/out-of-order history. | Frozen protocol explicitly accepts this for the course system. | Persist per-device sequence state with a recovery design. |
| TD-4 | Secure sessions are in memory | Gateway, Cloud | Restart invalidates active session state and requires a fresh handshake. | Short-lived 300-second sessions keep the implementation small. | Add a reviewed persistent session lifecycle or revised recovery architecture. |
| TD-5 | Cloud ML-KEM key pair is ephemeral | Cloud | Cloud restart changes `key_id` and removes existing sessions. | One process-local key pair is the frozen version-1 model. | Use managed persistent key lifecycle and authenticated distribution. |
| TD-6 | Simplified Cloud public-key trust | Gateway, Cloud | ML-KEM does not authenticate Cloud identity; a public-key substitution remains possible. | The Gateway trusts the configured Cloud URL in a controlled test environment. | Add authenticated transport and a production identity design (for example TLS/mTLS, PKI, pinning, or signed distribution). |
| TD-7 | HTTP-only controlled test environment | Gateway, Cloud, deployment | Transport identity and broader traffic metadata protections are outside the application AEAD scope. | The project demonstrates application payload protection, not production network identity. | Deploy authenticated encrypted transport under an approved architecture revision. |
| TD-8 | SQLite and single-instance services | Cloud, deployment | Availability, concurrency, and recovery capabilities are limited; there is no high availability. | SQLite and one instance match the small demonstration scope. | Select a production persistence and availability design after requirements analysis. |
| TD-9 | Simple bounded retry strategy | Legacy Device, Gateway | Retries can delay failure and amplify downstream attempts; they do not guarantee delivery. | Bounds make failure behavior observable and testable without extra infrastructure. | Reassess retry ownership, backoff, and durable delivery under production load. |
| TD-10 | Idempotency is only `UNIQUE(device_id, sequence_number)` | Cloud | Device sequence resets or identity reuse can conflict with prior logical measurements. | It is the frozen business identity needed for ordinary retransmission handling. | Define a device lifecycle/reset identity strategy. |
| TD-11 | No dedicated cryptographic anti-replay counter/window | Gateway, Cloud | A previously authenticated SecureEnvelope can be replayed at the cryptographic layer. | Protocol v1 intentionally excludes counters and replay windows. | Add a versioned per-session replay design only through a protocol revision. |
| TD-12 | Python cannot guarantee secure memory zeroization | Gateway, Cloud | Sensitive key material can remain in process memory beyond intended object lifetime. | The maintained libraries and best-effort lifecycle handling are appropriate for the course scope. | Use platform-supported key isolation and a runtime with stronger memory-control properties where required. |

## Required distinction

Cloud business idempotency prevents duplicate logical rows for
`(device_id, sequence_number)`. It is **not cryptographic replay protection**:
protocol version 1 has no dedicated cryptographic anti-replay counter or
window. TD-10 and TD-11 are deliberately separate entries.

## Evidence sources

The frozen cross-component specification documents in-memory sequence state,
the public-key trust assumption, session/key lifecycle, idempotency, replay
limits, and course-scale exclusions. The component records
[`edge_gateway/docs/technical-debt.md`](../edge_gateway/docs/technical-debt.md)
and [`edge_gateway/docs/threat-model.md`](../edge_gateway/docs/threat-model.md)
provide the Gateway-level evidence consolidated here.
