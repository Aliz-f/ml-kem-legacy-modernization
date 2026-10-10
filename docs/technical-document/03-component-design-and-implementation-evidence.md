# Chapter 3 — Component Design and Implementation Evidence

## 3.1 Implementation approach and ownership

The implementation is divided into three deployable Python services.  The
division is architectural rather than cosmetic: each service owns a distinct
part of the data path and must not absorb another component's responsibilities.

| Component | Implemented responsibility | Deliberate exclusion |
| --- | --- | --- |
| `legacy_system` | Simulate readings, serialize the legacy payload, make bounded HTTP delivery attempts, inject controlled device faults, and shut down cleanly. | No ML-KEM, Cloud API, encryption, session, or storage code. |
| `edge_gateway` | Provide Legacy API validation, normalization, sequence tracking, correlation, mode-specific Cloud dispatch, and Gateway-side PQC sessions/envelopes. | No durable business-record store and no direct sharing of internal models with Cloud. |
| `cloud_service` | Provide baseline and secure APIs, own Cloud ML-KEM/session behavior, decrypt and validate, enforce idempotency, store/query records, and expose health/metrics. | No Legacy Device wire-protocol support and no direct device communication. |

Each application is assembled through a `create_app(...)` factory or an
equivalent controller.  Dependencies are injected in tests and composition;
importing a module does not bind a server port, establish a remote session, or
write data.  This makes unit testing practical and isolates the boundary
between application logic, transport, cryptography, and storage.

```text
legacy_system/                         edge_gateway/                    cloud_service/
Sensor → DeviceController              FastAPI ingress                   FastAPI API routers
          ↓                            ↓                                  ↓
FailureInjector → GatewayClient        validation → normalize → dispatch  baseline OR crypto/session
                                       ↓                                  ↓
                                       classical client OR PQC transport    validate/decrypt → repository
```

## 3.2 Legacy Device implementation

The Legacy Device is intentionally a valid-data producer first and a
failure-simulation client second.  `Sensor` creates immutable `Measurement`
objects with a configured device ID, UTC timestamp, increasing sequence number,
and plausible environmental ranges (15–30 °C and 30–70% humidity during normal
simulation).  Its model-level validation uses the broader protocol domain:
temperature from -40 to 85 °C, humidity from 0 to 100%, and a non-negative
signed 64-bit sequence number.

The following excerpt from `legacy_system/src/legacy_system/sensor.py`
shows that normal sensor generation remains independent of delivery:

```python
def read(self) -> "Measurement":
    measurement = Measurement(
        device_id=self._device_id,
        temperature_c=self._random_source.uniform(15.0, 30.0),
        humidity_pct=self._random_source.uniform(30.0, 70.0),
        timestamp=self._clock(),
        sequence_number=self._next_sequence_number,
    )
    self._next_sequence_number += 1
    return measurement
```

`Measurement.to_payload()` converts the valid domain value into the five-field
Legacy JSON representation and formats the UTC offset as `Z`.  The
`FailureInjector` acts *after* serialization.  This is important because test
cases such as a missing field or invalid timestamp must be represented on the
wire without polluting the normal typed sensor model with invalid state.

`DeviceController` coordinates configuration, sensor reads, optional payload
mutation, client delivery, structured events, the send interval, and graceful
SIGINT/SIGTERM shutdown.  Its main loop has no Cloud or PQC dependency:

```python
while not self._stop_event.is_set():
    measurement = self._sensor.read()
    payload = measurement.to_payload()
    outgoing = self._failure_injector.apply(payload)
    self._send_with_logging(outgoing, measurement.sequence_number)
    if not self._stop_event.is_set():
        self._sleeper(self._config.send_interval_seconds)
```

The HTTP client classifies retryable network/server outcomes separately from
non-retryable protocol responses.  The controller logs identifiers, sequence
numbers, result status, and attempt count, but no credentials or cryptographic
material.  This preserves the behavior expected of a constrained legacy client
while still making delivery failures observable.

## 3.3 Edge Gateway implementation

### 3.3.1 Legacy ingress and application pipeline

The Edge Gateway is a FastAPI application constructed in `edge_gateway/src/edge_gateway/app.py`.
It composes one configuration object, application and PQC metric registries,
failure hooks, a `CloudDispatch`, and a `MeasurementProcessor`.  It maps
exceptions at the HTTP boundary, preserving the frozen distinction between
syntax and semantic validation:

```python
@app.exception_handler(LegacyJSONError)
async def invalid_json(request: Request, error: LegacyJSONError):
    return _error_response(GatewayErrorCode.INVALID_JSON)       # HTTP 400

@app.exception_handler(LegacyMeasurementSchemaError)
@app.exception_handler(LegacyMeasurementDomainError)
async def invalid_measurement(request: Request, error: ValueError):
    return _error_response(GatewayErrorCode.INVALID_MEASUREMENT) # HTTP 422
```

The measurement endpoint limits the received body to 16 KiB, parses and
validates the five legacy fields, captures a Gateway receipt time, and delegates
processing.  A successful endpoint response is produced only after the
processor's Cloud dispatch succeeds:

```python
measurement = parse_legacy_measurement(bytes(body))
validate_legacy_measurement(measurement)
await processor.process(measurement, received_at=received_at)
return JSONResponse(status_code=202, content={"status": "accepted"})
```

`MeasurementProcessor` separates business flow from transport details.  It
normalizes a `LegacyMeasurement`, asks `SequenceTracker` to apply per-device
policy, creates the request ID, and calls mode-specific dispatch.  The sequence
tracker holds the last valid value per device; it accepts first/increasing
values, records but accepts gaps, and rejects duplicates or lower values.  Its
state is intentionally committed before downstream delivery and remains
in-memory.

### 3.3.2 Classical and secure dispatch

`CloudDispatch` is the Gateway's explicit mode selector.  With
`SECURITY_MODE=classical`, the baseline client sends canonical JSON and
`X-Request-ID` to the Cloud baseline endpoint.  With `SECURITY_MODE=mlkem`, it
uses `SecureTransport`.  The application factory illustrates fail-closed
composition: no secure transport is constructed implicitly in a classical
process, and the baseline transport is unavailable in an ML-KEM process.

```python
if settings.security_mode == "mlkem" and secure_transport is None:
    secure_transport = _secure_transport(settings, registry, failures, application_registry)
baseline = baseline_transport or _baseline_transport(settings, failures, application_registry)
dispatch = CloudDispatch(settings, baseline=baseline, secure=secure_transport,
                         pqc_metrics=registry)
```

The secure implementation is kept in `edge_gateway/crypto/` as small focused
modules: `mlkem.py`, `kdf.py`, `symmetric.py`, `encoding.py`, `aad.py`,
`envelope.py`, `public_key_client.py`, `session_client.py`, `session.py`, and
`secure_transport.py`.  This gives testable boundaries for maintained-library
calls, binary encoding, deterministic AAD construction, session state, and
transport behavior.

The envelope builder makes all required operations explicit:

```python
aad = build_aad(protocol_version=PROTOCOL_VERSION, gateway_id=gateway_id,
                session_id=session_id, request_id=request_id)
nonce = generate_nonce()
ciphertext = encrypt(session_key, nonce, plaintext, aad)
return SecureEnvelope(protocol_version=PROTOCOL_VERSION, gateway_id=gateway_id,
                      session_id=session_id, request_id=request_id,
                      nonce=encode_binary(nonce), ciphertext=encode_binary(ciphertext))
```

This implementation evidence matters for the retry rule: `SecureTransport`
retains one already-built envelope for ordinary transport retries instead of
creating a nonce/ciphertext pair per attempt.  A `SESSION_INVALID` or
`SESSION_EXPIRED` response takes a different bounded path: it invalidates the
local session, establishes one replacement, rebuilds under the new key, and
preserves the logical request ID.  No branch falls back automatically to the
baseline endpoint.

## 3.4 Cloud Service implementation

### 3.4.1 Application lifecycle and API composition

`cloud_service/src/cloud_service/app.py` builds the Cloud FastAPI application.
Its lifespan initializes SQLite storage, and only in ML-KEM mode creates the
process-local key and session services.  Shutdown reverses that lifecycle,
closes sessions and key service, then closes the database.  This avoids
carrying secure runtime state across a process restart.

The application registers distinct routers for baseline ingestion, queries,
public-key publication, session establishment, and secure ingestion.  It also
exports `/health`, `/ready`, and `/metrics`.  Readiness checks storage and, in
ML-KEM mode, the availability of key/session and cryptographic dependencies;
it deliberately does not require an active Gateway session.

```python
app.include_router(gateway_router)
app.include_router(query_router)
app.include_router(crypto_router)
app.include_router(session_router)
app.include_router(secure_router)
```

### 3.4.2 Secure ingestion: validate, authenticate, validate again, then store

The secure route delegates its CPU/blocking pipeline to
`cloud_service.gateway.secure._ingest`.  Its ordering is security-critical:
the envelope is structurally validated; session existence, gateway ownership,
and expiry are checked; deterministic AAD is reconstructed; AES-GCM
authenticates/decrypts; the resulting canonical measurement is validated; only
then does the repository receive it.

```python
session = sessions.get(envelope.session_id, envelope.gateway_id)
aad = build_aad(protocol_version=envelope.protocol_version,
                gateway_id=envelope.gateway_id,
                session_id=envelope.session_id,
                request_id=envelope.request_id)
plaintext = decrypt(session.session_key, validated.nonce,
                    validated.ciphertext, aad)
measurement = validate_measurement(parse_json(plaintext),
                                   expected_gateway_id=envelope.gateway_id)
result = repository.save_idempotent(measurement)
```

The route converts malformed envelopes and cryptographic authentication failure
to the deliberately non-specific `400 SECURE_MESSAGE_REJECTED` response;
invalid decrypted business data is `422 INVALID_MEASUREMENT`; session errors
are served through the session handler as `409`; and storage failure is `503`.
The code also supports controlled failure modes, including a deliberately
dropped acknowledgement after a committed write.  That scenario tests that an
ordinary Gateway retry reuses its envelope and arrives at the idempotent
storage path.

### 3.4.3 SQLite storage and idempotency

The Cloud repository isolates parameterized SQLite work from HTTP and crypto
code.  `save_idempotent()` uses a targeted conflict clause on the frozen
business identity, then returns the existing or newly created record in the
same transaction:

```python
cursor = connection.execute(
    _INSERT + " ON CONFLICT(device_id, sequence_number) DO NOTHING",
    candidate.to_dict(),
)
created = cursor.rowcount == 1
row = connection.execute(
    "SELECT * FROM measurements WHERE device_id = ? AND sequence_number = ?",
    (measurement.device_id, measurement.sequence_number),
).fetchone()
```

This prevents a retry from adding a second logical record and returns a stable
record identity for either case.  It does not attempt to turn SQLite
idempotency into a cryptographic replay window; replay protection remains out
of scope for protocol v1.

## 3.5 Cross-component engineering decisions visible in the code

The selected implementation patterns provide direct evidence for several
project-wide requirements:

| Requirement | Implementation evidence |
| --- | --- |
| Legacy compatibility | Sensor/controller and HTTP client are isolated in `legacy_system`; no crypto imports are needed there. |
| Frozen validation semantics | Gateway exception handlers differentiate `400`, `422`, and `409`; Cloud repeats canonical validation after decryption. |
| No plaintext downgrade | Gateway composes separate baseline/secure transports and secure dispatch has no automatic baseline route. |
| Secret-safe operation | Session/key material is never returned by a route or written into normal application log fields; error messages are classified rather than diagnostic. |
| Correct retry behavior | Gateway separates ordinary envelope reuse from session-recovery rebuild; Cloud's dropped-response mode exercises persistence-before-response behavior. |
| Idempotent persistence | SQLite uses `ON CONFLICT(device_id, sequence_number) DO NOTHING` within the repository transaction. |
| Testability | Factories, dependency injection, focused crypto modules, repository isolation, injectable clocks/randomness, and controlled failure injectors support component and integration tests. |

These choices keep the codebase course-sized while retaining the boundaries
needed to inspect AI-generated changes critically.  The full protocol constants
and wire contracts are in Chapter 2; deployment, monitoring, and CI evidence
is in Chapter 4; and verification evidence is in Chapter 5.
