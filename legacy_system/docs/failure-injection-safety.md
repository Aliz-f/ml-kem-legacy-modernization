# Failure injection safety safeguards (M1-19)

This record implements Member 1 task **M1-19: Verify that failure injection cannot
accidentally become normal behavior**. It provides an architectural and
operational safety review of the Legacy Device's failure injection subsystem.

---

## 1. How to reproduce

From the repository root with the locked development environment installed:

```bash
uv run pytest legacy_system/tests/test_failure_safety.py -v
```

This suite verifies safe configuration defaults, startup warning logging, domain
model immutability, sequence monotonicity, wire protocol purity, and PRNG isolation.

---

## 2. Core architectural safeguards

### A. Safe defaults
- `FAILURE_MODE` defaults strictly to `none`.
- `FAILURE_RATE` defaults strictly to `0.0`.
- `FAILURE_SEED` defaults to `None`.
- Unless an operator explicitly configures both a non-`none` mode and a non-zero rate, the simulator runs in 100% healthy, clean sensor mode.

### B. Startup visibility
- When failure simulation is enabled (`mode != none` and `rate > 0.0`), `DeviceController.run()` emits a prominent structured warning log during startup:
  ```text
  WARNING event=failure_injection_enabled component=legacy_system device_id=sensor-001 mode=invalid_humidity rate=0.25
  ```
- When simulation is disabled, this warning is completely absent.

### C. Domain model immutability
- Sensor readings are instantiated into validated `Measurement` domain dataclasses (`device_id`, `temperature_c`, `humidity_pct`, `timestamp`, `sequence_number`).
- Fault injection is applied strictly to **serialized outgoing dictionary copies** returned by `measurement.to_payload()`.
- The domain `Measurement` instance is never mutated, relaxed, or bypassed. Faulty representations (e.g., missing timestamps or negative humidity) exist only on the wire.

### D. Sequence state monotonicity
- For `duplicate_sequence` and `out_of_order_sequence` fault modes, the injector alters only the outgoing payload dictionary.
- The `Sensor` object's internal sequence counter increments strictly monotonically ($0, 1, 2, 3\dots$) with every reading.
- Downstream rejections or sequence mutations never rewind or corrupt internal device sequence state.

### E. Wire protocol purity
- Outgoing payloads contain only the five legitimate protocol fields (`device_id`, `temperature_c`, `humidity_pct`, `timestamp`, `sequence_number`), or a subset when `missing_field` is active.
- No synthetic simulation markers (such as `is_simulated`, `mock`, `test_mode`, or `failure_mode`) are added to the wire format.
- The Gateway evaluates incoming requests purely on their byte representation and protocol rules, unaware of whether an anomaly was simulated.

### F. PRNG isolation
- `FailureInjector` encapsulates its own dedicated `random.Random(failure_seed)` instance.
- It does not mutate or depend on the global Python `random` state.
- Simulation seeds never influence cryptographic randomness elsewhere in the system.
