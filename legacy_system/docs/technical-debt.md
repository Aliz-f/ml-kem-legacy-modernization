# Legacy Device Technical Debt

This register records the known, accepted architectural and operational limitations of the **Legacy Device simulator** (`legacy_system/`) under Task M1-25.

The Legacy Device intentionally models an unmodernized, constrained edge IoT appliance. Rather than introducing complex enterprise middleware or hiding limitations, these trade-offs are explicitly documented, analyzed for operational risk, and mapped to future production improvements.

This component register coordinates directly with the project-wide technical debt register ([`docs/technical-debt.md`](../../docs/technical-debt.md)) and the Edge Gateway register ([`edge_gateway/docs/technical-debt.md`](../../edge_gateway/docs/technical-debt.md)).

---

## 1. Technical Debt Summary

| ID | Technical Debt | Consequence / Operational Risk | Why Accepted for Course Scope | Future Production Improvement |
|---|---|---|---|---|
| **LTD-1** | No persistent store-and-forward queue | Measurements dropped if Gateway is unreachable beyond retry limit; loss of unsent telemetry on power loss or crash. | Keeps component simple, lightweight, and course-sized without requiring non-volatile embedded database or disk queue. | Implement a disk-backed SQLite or append-only log store-and-forward buffer with persistent queueing. |
| **LTD-2** | No strong device authentication | An unauthorized device or on-path client can spoof `device_id` and send unauthorized measurements. | Models a legacy unauthenticated sensor environment in a controlled local testbed. | Provision cryptographic credentials (e.g. client certificates, API keys, or mTLS) for device identity verification. |
| **LTD-3** | Legacy hop is not PQC-protected | Traffic between Legacy Device and Edge Gateway is plain JSON over HTTP without ML-KEM or encryption. | Intentional modernization boundary: demonstrates retrofitting PQC at the Gateway without modifying legacy edge sensors. | Upgrade edge sensor firmware or hardware to support PQC encapsulation directly when device constraints allow. |
| **LTD-4** | Deterministic retry backoff without jitter | Multiple simultaneous devices recovering from a network outage could synchronize retries, potentially causing a retry storm at the Gateway. | Bounded backoff ($2^{\text{attempt}-1}$) is deterministic, predictable, and easily testable without stochastic timing. | Introduce full-jitter or truncated exponential backoff (e.g. decorrelated jitter) to disperse retry concurrency. |
| **LTD-5** | In-memory sequence counter resets on restart | Device restart resets `sequence_number` to 0, causing Gateway sequence tracker to reject initial readings as `409 Conflict`. | In-memory counter avoids disk I/O on edge hardware simulation; aligns with frozen protocol version 1. | Persist high-water sequence marks to non-volatile edge storage (e.g. EEPROM, flash, or persistent state file). |
| **LTD-6** | Simulated pseudo-sensor | Readings are synthetic pseudo-random values generated in software, not physical transducer signals. | Enables fully automated, hardware-independent CI testing and reproducible benchmark runs without physical lab gear. | Interface with physical hardware sensors (e.g. I2C/SPI temperature and humidity transducers). |
| **LTD-7** | No dedicated health / metrics endpoint | Device health must be inferred from container process status or Gateway receipt logs; no internal telemetry scrape endpoint. | Preserves pure outbound client profile; running an HTTP server on the sensor mismodels edge appliance topology. | Implement lightweight push telemetry (e.g. periodic heartbeat or metrics reporting over outbound HTTP/UDP). |
| **LTD-8** | Unencrypted cleartext HTTP transport | Plaintext HTTP/1.1 exposes measurement payload data (temperature, humidity, sequence) to local eavesdroppers. | Controlled course demonstration of application-level Gateway-to-Cloud security rather than edge link security. | Deploy TLS 1.3 or authenticated link-layer encryption (e.g. IEEE 802.15.4 security or WireGuard) on local edge network. |

---

## 2. In-Depth Debt Analysis

### LTD-1: No Persistent Store-and-Forward Buffer
- **Current Behavior**: The `DeviceController` reads the sensor and calls `GatewayClient.send()`. If the Gateway is unreachable, the client retries up to `MAX_RETRIES` (default 2) with exponential backoff. If all attempts fail, the client logs `event=gateway_request_failed` and drops the measurement. The controller then sleeps until the next cycle.
- **Risk & Consequence**: Any telemetry generated during sustained Gateway downtime or network partitions is permanently lost. Unsent measurements are not spooled to disk.
- **Accepted Rationale**: Incorporating a transactional embedded store (such as SQLite, RocksDB, or a spool file) adds significant complexity, disk write wear considerations on flash storage, and recovery logic that falls outside the core modernization scope.
- **Future Modernization**: Implement a lightweight local queue that buffers unsent payloads to disk during outages and flushes them in order upon network restoration.

### LTD-2: No Strong Device Authentication on Legacy Link
- **Current Behavior**: The device sends `{"device_id": "sensor-001", ...}` in plain JSON. The Gateway validates syntax and sequence order, but does not authenticate whether the HTTP connection originates from the legitimate device.
- **Risk & Consequence**: Any attacker on the local network capable of reaching the Gateway's HTTP port can inject arbitrary measurements claiming to be `sensor-001`.
- **Accepted Rationale**: The project's stated mission is **legacy modernization**. Legacy industrial and IoT devices commonly lack cryptographic co-processors, PKI identity, or credentials. The Edge Gateway serves precisely to ingest such legacy data and bridge it into a modern, authenticated, post-quantum cloud channel.
- **Future Modernization**: Provision unique pre-shared keys, X.509 client certificates, or token-based authentication on modern device replacements.

### LTD-3: Legacy Link is not PQC-Protected
- **Current Behavior**: Post-Quantum Cryptography (ML-KEM-768, HKDF-SHA-256, AES-256-GCM) is implemented exclusively between the Edge Gateway and Cloud Service. The Legacy Device remains completely classical and unencrypted.
- **Risk & Consequence**: The physical edge link remains vulnerable to classical and quantum adversaries capable of capturing traffic on the local subnet.
- **Accepted Rationale**: This is the core architectural premise of the project: legacy field devices cannot be easily updated with heavy PQC libraries or key encapsulation algorithms due to memory, CPU, or firmware constraints. The modernization boundary is intentionally placed at the Gateway.
- **Future Modernization**: When next-generation edge microcontrollers become available, implement hardware-accelerated ML-KEM or hybrid post-quantum transport directly on the sensor.

### LTD-4: Deterministic Retry Backoff Without Jitter
- **Current Behavior**: `GatewayClient` applies deterministic exponential backoff: delay equals $2^{\text{attempt}-1}$ seconds (1s, 2s).
- **Risk & Consequence**: If a large fleet of simulated devices experiences a simultaneous network blip or Gateway restart, all devices will retry at identical time offsets, resulting in synchronized traffic spikes ("thundering herd").
- **Accepted Rationale**: Deterministic timing enables reproducible, fast, and stable unit and integration tests (`test_client.py`, `test_baseline_measurements.py`) without requiring flaky test tolerances or long random sleeps.
- **Future Modernization**: Implement randomized jitter (e.g. `delay = random.uniform(0.5, 1.5) * (2 ** attempt)`).

### LTD-5: In-Memory Sequence Counter Resets on Restart
- **Current Behavior**: `Sensor` initializes `self._sequence_number = 0` in memory. Restarting the process or container resets the counter back to 0.
- **Risk & Consequence**: If the Edge Gateway has already accepted sequence numbers (e.g. up to 150), a restarted device sending sequence 0 will be rejected with HTTP `409 Conflict` (out-of-order sequence) until its sequence counter exceeds the Gateway's recorded high-water mark.
- **Accepted Rationale**: Ephemeral in-memory state avoids persistent state management across container teardowns in automated test runners and CI pipelines.
- **Future Modernization**: Persist the current sequence number to non-volatile storage or negotiate a session/epoch identifier with the Gateway upon startup.

### LTD-6: Simulated Pseudo-Sensor
- **Current Behavior**: `Sensor.read()` generates synthetic temperature ($[15.0, 30.0]$ °C) and humidity ($[30.0, 70.0]$ %) using Python's `random.Random` module with optional seeding.
- **Risk & Consequence**: Does not capture real-world sensor noise, electrical faults, physical ADC drift, or hardware bus delays.
- **Accepted Rationale**: Software simulation enables fully reproducible, deterministic baseline measurements, failure injections, and CI runs without requiring specialized physical test benches.
- **Future Modernization**: Replace `Sensor` with a driver interacting with Linux `/sys/bus/iio` or hardware GPIO/I2C buses.

### LTD-7: No Ingress Health or Metrics Endpoint
- **Current Behavior**: The device has no HTTP server, no `/health` endpoint, and no Prometheus metrics exporter. Observability is limited to structured log events (`event=...`) and exit codes.
- **Risk & Consequence**: External monitoring systems cannot pull live health or telemetry stats directly from the device container via HTTP scraping.
- **Accepted Rationale**: The Legacy Device is purely an outbound client. Binding listening sockets on an IoT sensor expands attack surface and mismodels embedded edge devices.
- **Future Modernization**: Implement an outbound lightweight push telemetry protocol (e.g. periodic MQTT/UDP heartbeats) to report device health.

### LTD-8: Unencrypted Cleartext HTTP Transport
- **Current Behavior**: Communication uses plain HTTP/1.1 (`http://edge-gateway:8000/api/v1/measurements`).
- **Risk & Consequence**: Data in transit across the local physical segment is vulnerable to passive sniffing and tampering.
- **Accepted Rationale**: Replicates typical legacy fieldbus/industrial network environments where encryption was omitted. The modernization project addresses post-quantum security across the untrusted WAN (Gateway &rarr; Cloud) rather than retrofitting TLS onto constrained legacy field devices.
- **Future Modernization**: Introduce TLS 1.3 or MACsec / IPsec link encryption once network infrastructure permits.

---

## 3. Operational Risk Summary and Interactions

When operating the system under stress or in degraded conditions, these technical debt items interact in predictable ways:
1. **Restart After Failure**: If a power outage or restart occurs after 50 measurements have been sent, LTD-5 (sequence reset to 0) interacts with Gateway sequence tracking: the first 51 measurements from the restarted device will return `409 Conflict`.
2. **Gateway Downtime**: If the Gateway is offline for more than 3 seconds, LTD-1 (no local buffer) means unacknowledged readings are permanently dropped rather than queued.
3. **Network Recovery**: If network connectivity recovers simultaneously across multiple devices, LTD-4 (no jitter) may produce concurrent burst requests at the Gateway.

All of these interactions are consistent with the frozen architecture and provide concrete operational baselines against which future modernization phases can be measured.

---

## 4. Cross-References

- **Legacy Operations**: [`legacy_system/docs/architecture-operations.md`](architecture-operations.md) (Task M1-23)
- **AI Decision Register**: [`legacy_system/docs/ai-decisions.md`](ai-decisions.md) (Task M1-24)
- **Project-Wide Technical Debt**: [`docs/technical-debt.md`](../../docs/technical-debt.md) (Tasks M5-81, cross-component consolidation)
- **Edge Gateway Technical Debt**: [`edge_gateway/docs/technical-debt.md`](../../edge_gateway/docs/technical-debt.md)
- **Project Risk Register**: [`docs/risk-register.md`](../../docs/risk-register.md)
