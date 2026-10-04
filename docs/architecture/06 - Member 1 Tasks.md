# Member 1 — Legacy Device Owner

## Overall mission

Member 1 is responsible for delivering a complete, tested, documented, configurable **Legacy Device simulator** that can operate both in normal mode and in controlled failure-simulation modes.

The component must eventually support this path:

```text
┌──────────────────────┐
│    Legacy Device     │
│                      │
│ Sensor generation    │
│ Failure injection    │
│ HTTP client          │
│ Retry handling       │
│ Logging              │
└──────────┬───────────┘
           │
           │ HTTP + JSON
           │
           ▼
┌──────────────────────┐
│    Edge Gateway      │
└──────────────────────┘
```

Member 1 does **not** own:

```text
ML-KEM
Gateway → Cloud encryption
Cloud storage
Cloud API
Gateway metrics
Cloud metrics
Session management
```

However, Member 1 should help verify that the Legacy Device behaves correctly against the real Gateway.

---

# Member 1 final deliverables

By the end of the project, Member 1 should have contributed these concrete artifacts:

|Deliverable|Expected result|
|---|---|
|Legacy configuration|validated runtime configuration|
|Measurement model|stable Legacy→Gateway schema|
|Sensor simulator|valid temperature/humidity generation|
|Sequence management|predictable monotonically increasing numbers|
|Failure injector|configurable invalid/anomalous data generation|
|Gateway HTTP client|timeout + bounded retry behavior|
|Device runtime loop|periodic sending + graceful shutdown|
|Logging|useful and safe operational events|
|Dockerfile|reproducible Legacy Device container|
|Unit tests|complete component-level coverage|
|Integration tests|real Device→Gateway scenarios|
|Baseline measurements|evidence for initial system|
|AI-history records|prompts, outputs, review, revisions|
|Technical documentation|design and implementation notes|
|Peer review|review at least relevant teammate changes|

The course explicitly requires AI-generated artifacts to be manually evaluated for correctness, security, maintainability, testability, performance, and operational suitability, with significant prompts and decisions documented.

---

# Task M1-00 — Review and freeze the Legacy Device contract

**Priority:** Critical  
**Dependency:** Architecture documentation must exist.  
**Coding:** No application implementation yet.

Member 1 should first verify that the implementation will follow the agreed contract exactly.

### Required contract

Endpoint:

```http
POST /api/v1/measurements
Content-Type: application/json
```

Payload:

```json
{
  "device_id": "sensor-001",
  "temperature_c": 21.7,
  "humidity_pct": 42.5,
  "timestamp": "2026-09-21T13:45:31Z",
  "sequence_number": 184
}
```

Rules:

|Field|Rule|
|---|---|
|`device_id`|non-empty string|
|`temperature_c`|normal generation around 15–30°C|
|`humidity_pct`|normal generation around 30–70%|
|`timestamp`|ISO-8601 UTC|
|`sequence_number`|integer `0 <= value <= 9223372036854775807`|

Member 1 must verify that these match:

```text
docs/architecture/legacy-device.md
docs/architecture/protocol-specification.md
```

### Acceptance criteria

- Schema is understood.
    
- Field names are frozen.
    
- No camelCase variants are introduced.
    
- Gateway endpoint is agreed with Member 2.
    
- Response semantics are agreed.
    
- Retry semantics are agreed.
    
- Member 1 does not independently change the protocol afterward.
    

### Definition of Done

```text
[ ] Reviewed protocol specification
[ ] Confirmed endpoint with Gateway owner
[ ] Confirmed field names
[ ] Confirmed status-code behavior
[ ] Confirmed `400` vs `422` validation boundary
[ ] Open questions resolved with team
```

---

# Task M1-01 — Implement Legacy Device configuration

**Primary files:**

```text
legacy_system/
└── src/
    └── legacy_system/
        └── config.py
```

Potential configuration:

```text
DEVICE_ID=sensor-001
GATEWAY_URL=http://edge-gateway:8000

SEND_INTERVAL_SECONDS=5
REQUEST_TIMEOUT_SECONDS=3
MAX_RETRIES=2

FAILURE_MODE=none
FAILURE_RATE=0.0
FAILURE_SEED=

LOG_LEVEL=INFO
```

### Responsibilities

`config.py` should:

```text
read environment variables
        ↓
apply defaults
        ↓
convert types
        ↓
validate values
        ↓
produce one validated Config object
```

Do not scatter:

```python
os.getenv(...)
```

through the rest of the application.

### Validation rules

Member 1 should verify at least:

```text
DEVICE_ID
→ non-empty

GATEWAY_URL
→ non-empty / valid enough for HTTP client

SEND_INTERVAL_SECONDS
→ > 0

REQUEST_TIMEOUT_SECONDS
→ > 0

MAX_RETRIES
→ >= 0

FAILURE_RATE
→ 0.0 <= value <= 1.0

FAILURE_MODE
→ known enum value

LOG_LEVEL
→ supported value
```

### Invalid configuration behavior

Example:

```text
SEND_INTERVAL_SECONDS=-10
```

Expected:

```text
startup
 ↓
configuration validation fails
 ↓
clear safe error
 ↓
process exits non-zero
```

Do not start the device with invalid configuration.

### Tests

Member 1 should implement:

```text
test_default_configuration
test_valid_environment_configuration
test_empty_device_id
test_negative_interval
test_zero_interval
test_zero_timeout
test_negative_timeout
test_negative_retry_count
test_failure_rate_below_zero
test_failure_rate_above_one
test_unknown_failure_mode
```

### Definition of Done

```text
[ ] Configuration centralized
[ ] Defaults documented
[ ] Invalid values rejected
[ ] Environment values correctly parsed
[ ] Tests pass
[ ] No secrets logged
[ ] Human review completed
```

---

# Task M1-02 — Implement measurement data model


**Primary location:**

Either:

```text
sensor.py
```

or, if justified:

```text
models.py
```

Do not create `models.py` merely for architectural decoration.

### Valid domain model

```text
Measurement
├── device_id
├── temperature_c
├── humidity_pct
├── timestamp
└── sequence_number
```

Conceptually:

```python
Measurement(
    device_id="sensor-001",
    temperature_c=21.7,
    humidity_pct=42.5,
    timestamp=...,
    sequence_number=42,
)
```

### Important invariant

`Measurement` represents a **valid internal measurement only**.

It should not be used to represent deliberately malformed test payloads such as:

```text
missing timestamp
invalid timestamp string
humidity > 100
temperature outside protocol range
```

Those faults are introduced later, after serialization.

### Requirements

The model should:

- serialize cleanly to the agreed Legacy→Gateway JSON schema;
- preserve numeric types;
- represent timestamps consistently;
- reject or prevent impossible internal state where practical;
- remain independent from HTTP logic;
- remain independent from fault-injection logic.

### Serialization boundary

Provide one explicit conversion to a wire payload, conceptually:

```python
payload = measurement.to_payload()
```

or an equivalent serializer function.

The result should be a plain outgoing representation such as:

```python
dict[str, object]
```

or a small `LegacyPayload` representation that can be deliberately mutated by the failure injector.

The intended pipeline is:

```text
Valid Measurement
      ↓
serialize
      ↓
LegacyPayload / dict
      ↓
optional failure injection
      ↓
GatewayClient
```

### Do not put into the domain model

```text
gateway URL
HTTP status
retry counter
Cloud fields
gateway_id
request_id
ML-KEM fields
simulation metadata
```

### Tests

```text
measurement creation
valid field constraints
serialization
field names
numeric preservation
timestamp serialization
sequence serialization
serializer returns independent outgoing representation
```

### Definition of Done

```text
[ ] Model matches protocol exactly
[ ] Model represents valid internal state only
[ ] Explicit serialization boundary exists
[ ] No Gateway/Cloud fields added
[ ] JSON representation verified
[ ] Tests pass
```

---

# Task M1-03 — Implement sensor simulator

**Primary file:**

```text
sensor.py
```

The sensor generator must always produce **valid data**.

Failure simulation belongs elsewhere.

### Normal simulation

Recommended generation:

```text
temperature:
15°C – 30°C

humidity:
30% – 70%
```

Protocol-valid limits remain wider:

```text
temperature:
-40°C – 85°C

humidity:
0% – 100%
```

### Sensor API

Conceptually:

```python
measurement = sensor.read()
```

### Responsibilities

The sensor should generate:

```text
temperature
humidity
timestamp
sequence_number
device_id
```

### Sequence-number rule

Increment when the measurement is **created**, regardless of whether delivery succeeds.

Example:

```text
generate seq=5
→ delivery succeeds

generate seq=6
→ delivery fails

generate seq=7
→ delivery succeeds
```

The Gateway should therefore see:

```text
5
7
```

and can detect the missing sequence.

### Timestamp rule

Generate at measurement time:

```text
UTC
ISO-8601
```

Example:

```text
2026-09-21T15:22:13.125Z
```

### Deterministic testing

Random generation must be controllable.

The design should allow:

```text
seeded random source
```

or dependency injection.

Tests should never randomly fail.

### Tests

```text
temperature within normal range
humidity within normal range
timestamp is UTC
sequence begins correctly
sequence increments
sequence increments even after unsuccessful send
configured device ID is used
seeded generation reproducible
```

### Definition of Done

```text
[ ] Always produces valid normal measurements
[ ] No failure simulation inside sensor
[ ] Sequence behavior tested
[ ] Time behavior tested
[ ] Random behavior deterministic in tests
```

---

# Task M1-04 — Implement failure-injection subsystem


**Primary file:**

```text
failure.py
```

This is one of Member 1's most important tasks.

### Correct architecture

Failure injection must operate on the **serialized outgoing payload**, not on the validated `Measurement` domain object.

```text
Sensor
  ↓
Valid Measurement
  ↓
Serializer
  ↓
LegacyPayload / dict
  ↓
Failure Injector
  ├── unchanged
  └── deliberately mutated payload
  ↓
Gateway Client
```

This separation is necessary because test scenarios such as:

```text
missing_field
invalid_timestamp
```

cannot cleanly exist inside a strictly valid `Measurement` object.

Conceptually:

```python
measurement = sensor.read()
payload = measurement.to_payload()
outgoing = failure_injector.apply(payload)
client.send(outgoing)
```

The injector should preferably return a mutated **copy** or otherwise have clearly documented mutation semantics, so normal valid state is not corrupted unexpectedly.

### Initial modes

Implement the agreed initial set:

```text
none
invalid_temperature
invalid_humidity
missing_field
invalid_timestamp
duplicate_sequence
out_of_order_sequence
random
```

### `none`

```text
Input serialized payload
→ unchanged logical contents
```

### `invalid_temperature`

Example:

```text
21.3
↓
500.0
```

### `invalid_humidity`

Example:

```text
42.0
↓
145.0
```

### `missing_field`

Remove one required field according to deterministic design.

Prefer a documented field rather than unpredictable removal unless `random` is requested.

Recommended deterministic example:

```text
remove timestamp
```

Expected Gateway result:

```text
JSON syntax remains valid
but a required field is absent
→ 422 Unprocessable Entity
```

This is not a `400` case because the JSON itself is still parseable.

### `invalid_timestamp`

Example:

```text
timestamp = "not-a-valid-timestamp"
```

Expected Gateway result:

```text
422 Unprocessable Entity
```

because the JSON is parseable but the field value violates the contract.

### `duplicate_sequence`

Mutate only the outgoing payload's `sequence_number` to a previously used value.

Do **not** roll back the sensor's internal sequence counter.

### `out_of_order_sequence`

Example:

```text
current internal sequence = 40
outgoing payload sequence = 38
```

Again, the sensor's internal sequence progression remains monotonic.

### `random`

Select from supported data-failure scenarios.

Do not include:

```text
none
random
```

inside the random candidate pool.

### Failure rate

Configuration:

```text
FAILURE_RATE=0.2
```

Interpretation:

```text
roughly 20% of outgoing serialized payloads
receive the selected mutation
```

### Failure seed

```text
FAILURE_SEED=42
```

should permit reproducible testing/demonstration.

The seeded PRNG is only for **fault simulation**. It must never be reused for cryptographic randomness elsewhere in the project.

### Important protocol rule

Do **not** send:

```json
{
  "simulated_failure": true
}
```

to the Gateway.

The Gateway should evaluate malformed data exactly as if it originated from a faulty real device.

### Logging

When failure injection occurs:

```text
WARNING
event=simulated_failure_injected
mode=invalid_humidity
sequence_number=42
```

Logging may describe the selected simulation mode locally, but the outgoing wire payload must not include simulation-only metadata.

### Tests

Member 1 should implement at minimum:

```text
none preserves outgoing contents

invalid temperature becomes invalid
invalid humidity becomes invalid
missing field actually absent
timestamp becomes malformed

duplicate sequence mutates outgoing payload only
out-of-order sequence mutates outgoing payload only
sensor/internal sequence state remains monotonic

failure rate 0.0 → never inject
failure rate 1.0 → always inject

seeded random behavior deterministic
random only chooses allowed scenarios

valid Measurement object remains valid/unmodified
```

### Definition of Done

```text
[ ] Failure injection occurs after serialization
[ ] Valid Measurement domain object is not used for malformed state
[ ] Failure injection remains separate from sensor generation
[ ] All agreed modes implemented
[ ] Duplicate/out-of-order faults do not rewind internal sequence state
[ ] Failure rate works
[ ] Seed works
[ ] Failure events logged
[ ] No test marker sent to Gateway
[ ] Tests cover every mode
```

---

# Task M1-05 — Implement Gateway HTTP client


**Primary file:**

```text
client.py
```

Member 1 owns outgoing Legacy→Gateway communication.

### Endpoint

```text
{GATEWAY_URL}/api/v1/measurements
```

### Input boundary

The HTTP client receives the already prepared outgoing payload:

```text
LegacyPayload / dict
```

It should **not** own sensor-domain serialization or failure injection.

Conceptually:

```python
result = client.send(outgoing_payload)
```

### Responsibilities

```text
accept outgoing payload
encode payload as JSON
send HTTP request
enforce timeout
interpret HTTP status
classify retryability
perform bounded retry
return structured result
```

### Structured result

Possible result information:

```text
success
status_code
attempt_count
error category
```

Do not expose HTTP-library-specific exceptions throughout the application.

### Important status semantics

Success:

```text
202
```

Non-retryable Legacy application responses:

```text
400
→ malformed/unparseable JSON or body syntax

409
→ duplicate/out-of-order sequence

422
→ parsed JSON with missing, wrongly typed, or domain-invalid required fields
```

Retryable:

```text
network failure
timeout
500
502
503
504
```

`409` is expected for duplicate/out-of-order sequence rejection and must not be retried by the Legacy client.

### Tests

```text
prepared payload is sent unchanged except JSON encoding
correct endpoint used
correct content type
202 succeeds
400/409/422 are non-retryable
500/502/503/504 are retryable
network error classified safely
timeout classified safely
library exceptions do not leak through public client interface
```

---

# Task M1-06 — Implement retry policy

This may be part of `client.py`, but should be independently reviewable.

### Retry

```text
network connection failure
timeout
500
502
503
504
```

### Do not retry

```text
400
409
422
```

Rationale:

```text
422
→ sending exactly the same malformed payload again
  will not repair it.
```

### Default

```text
MAX_RETRIES=2
```

Meaning:

```text
1 original attempt
+
2 retry attempts
=
3 maximum requests
```

### Frozen initial backoff

```text
Attempt 1
failure
↓
wait 1 second

Attempt 2
failure
↓
wait 2 seconds

Attempt 3
failure
↓
give up
```

No infinite loop.

### Important testing rule

Tests must not really wait several seconds.

Inject/mock sleep or backoff behavior.

### Tests

```text
202 → success, no retry

400 → failure, no retry
409 → failure, no retry
422 → failure, no retry

500 → retry
502 → retry
503 → retry
504 → retry

timeout → retry
connection error → retry

failure then success
→ correct attempt count

all attempts fail
→ bounded failure

max retries zero
→ exactly one request
```

### Definition of Done

```text
[ ] Timeout explicit
[ ] Retry classifications documented
[ ] Retry bounded
[ ] Backoff deterministic
[ ] Tests do not sleep in real time
[ ] No infinite retry path
```

---

# Task M1-07 — Implement device controller/runtime loop


**Primary file:**

```text
device.py
```

Keep this module deliberately simple.

### Expected runtime

```text
startup
 ↓
load validated configuration
 ↓
create Sensor
 ↓
create FailureInjector
 ↓
create GatewayClient
 ↓
generate valid Measurement
 ↓
serialize to outgoing payload
 ↓
apply optional failure injection to payload
 ↓
send payload
 ↓
log outcome
 ↓
wait
 ↓
repeat
```

Conceptually:

```python
while running:
    measurement = sensor.read()
    payload = measurement.to_payload()
    outgoing = failure_injector.apply(payload)
    result = client.send(outgoing)
    sleep(interval)
```

### Controller must not

```text
implement HTTP internals
generate random sensor values directly
mutate the valid Measurement into malformed state
perform Gateway validation
implement Cloud behavior
implement ML-KEM
```

### Tests

```text
sensor called
serializer called
failure injector receives serialized payload
Gateway client receives outgoing payload
configured interval respected
delivery failure does not terminate loop unexpectedly
loop can stop
resources closed
```

Also verify:

```text
sensor sequence increments when Measurement is created
delivery failure does not roll sequence back
```

---

# Task M1-08 — Graceful shutdown

Member 1 should explicitly support:

```text
Ctrl+C
SIGTERM
Docker stop
```

Expected:

```text
signal
 ↓
stop accepting/generating new work
 ↓
end runtime loop
 ↓
close HTTP client
 ↓
log shutdown
 ↓
exit
```

### Important cases

Test shutdown:

```text
during normal waiting
after delivery
when Gateway unavailable
```

You do not need complex cancellation architecture, but the process should not require force-killing under ordinary conditions.

### Definition of Done

```text
[ ] Ctrl+C clean
[ ] SIGTERM clean
[ ] Client closed
[ ] No traceback on normal shutdown
[ ] Shutdown logged
```

---

# Task M1-09 — Implement logging

Member 1 should produce simple structured or consistently formatted logs.

Recommended events:

```text
device_starting
device_ready

measurement_generated

simulated_failure_injected

gateway_request_failed
gateway_retry
measurement_delivered
measurement_delivery_failed

device_shutting_down
```

### Useful fields

```text
event
device_id
sequence_number
attempt
status_code
failure_mode
```

### Do not log

```text
full environment
future credentials
tokens
passwords
private keys
shared secrets
```

Even though the Legacy Device currently has no ML-KEM secrets, use project-wide safe logging practices.

### Example

```text
INFO
event=measurement_delivered
device_id=sensor-001
sequence_number=42
status_code=202
attempt=1
```

### Failure simulation

```text
WARNING
event=simulated_failure_injected
device_id=sensor-001
sequence_number=43
mode=invalid_humidity
```

### Definition of Done

```text
[ ] Major lifecycle events logged
[ ] Retry visible
[ ] Final delivery failures visible
[ ] Failure injection clearly identifiable locally
[ ] No secret-sensitive output
```

---

# Task M1-10 — Complete Legacy Device unit-test suite


Member 1 should treat the tests as a deliverable, not an afterthought.

The assignment explicitly says that important generated artifacts should be verified through tests, code review, static analysis, documentation, and where relevant failure/security testing.

Recommended structure:

```text
legacy_system/
└── tests/
    ├── test_config.py
    ├── test_models.py          # or serializer tests near sensor tests
    ├── test_sensor.py
    ├── test_failure.py
    ├── test_client.py
    └── test_device.py
```

### Required categories

**Configuration**

```text
defaults
valid values
invalid values
failure modes
failure rate
```

**Measurement + serialization**

```text
valid model creation
field names
timestamp encoding
numeric preservation
payload independence
```

**Sensor**

```text
ranges
timestamps
sequence numbers
deterministic randomness
```

**Failure injector**

```text
all modes
probabilities
seeded behavior
payload-only mutation
domain Measurement remains valid
duplicate/out-of-order faults do not rewind sensor sequence
```

**Gateway client**

```text
success

400 malformed/unparseable body
→ non-retryable

409 duplicate/out-of-order
→ non-retryable

422 parsed-but-invalid measurement
→ non-retryable

500/502/503/504 retryable
timeouts
connection failure
retry exhaustion
prepared payload transmitted correctly
```

**Controller**

```text
orchestration
serialization before fault injection
loop
delivery failure continuation
shutdown
```

### Test-quality requirements

Tests must not:

```text
call real internet services
depend on Cloud Service
wait 5 seconds repeatedly
depend on uncontrolled randomness
depend on test execution order
```

---

# Task M1-11 — Build test fixtures for integration

Member 1 should provide a small set of deterministic example payloads shared with Member 2.

Suggested fixtures:

```text
valid_legacy_measurement.json

invalid_temperature_measurement.json

invalid_humidity_measurement.json

invalid_timestamp_measurement.json

missing_field_measurement.json
```

Example valid fixture:

```json
{
  "device_id": "sensor-test",
  "temperature_c": 22.5,
  "humidity_pct": 44.0,
  "timestamp": "2026-09-21T12:00:00Z",
  "sequence_number": 1
}
```

These become part of the Device↔Gateway contract tests.

### Definition of Done

Member 1 and Member 2 both agree that:

```text
valid fixture
→ Gateway accepts

invalid fixtures
→ Gateway rejects appropriately
```

---

# Task M1-12 — Legacy Device ↔ Gateway integration testing


**Shared with:** Member 2  
**Member 1 responsibility:** Device side and scenario definitions.

Do not rely only on mocks once the real Gateway exists.

Required scenarios:

### Scenario 1 — Normal data

```text
Legacy
 ↓
valid measurement
 ↓
Gateway
 ↓
downstream Cloud path succeeds
 ↓
202 Accepted
```

### Scenario 2 — Invalid humidity

```text
FAILURE_MODE=invalid_humidity
FAILURE_RATE=1.0
```

Expected:

```text
Legacy sends humidity > 100
Gateway returns 422
Legacy does not retry
Cloud receives nothing
```

### Scenario 3 — Invalid temperature

Expected:

```text
Gateway returns 422
Legacy does not retry
Cloud receives nothing
```

### Scenario 4 — Missing field

Expected:

```text
Legacy sends syntactically valid JSON
with one required field absent
↓
Gateway returns 422
↓
Legacy does not retry
↓
Cloud receives nothing
```

### Scenario 5 — Invalid timestamp

Expected:

```text
Gateway returns 422
Legacy does not retry
```

### Scenario 6 — Duplicate sequence

Expected:

```text
Gateway detects duplicate
Gateway returns 409
Legacy does not retry
```

### Scenario 7 — Out-of-order sequence

Expected:

```text
Gateway detects older sequence
Gateway returns 409
Legacy does not retry
```

### Scenario 8 — Sequence gap

Example:

```text
10
11
13
```

Expected:

```text
Gateway accepts 13
Gateway records/logs sequence gap
downstream processing continues
```

### Scenario 9 — Gateway unavailable

Stop Gateway.

Expected:

```text
Legacy attempts bounded retries
logs final failure
does not crash
continues with next newly generated measurement
sequence number continues increasing
```

### Sequence-state timing awareness

Member 1 should understand the Gateway's frozen policy:

```text
Gateway sequence state tracks the last valid sequence observed
```

not the last sequence successfully delivered to Cloud.

Therefore retries of a previously accepted Legacy sequence can legitimately receive `409` from the Gateway.

---

# Task M1-13 — Dockerize Legacy Device

**Primary file:**

```text
legacy_system/Dockerfile
```

Member 1 owns the component Docker image; Member 5 may review/integrate it into Compose.

### Requirements

Container should:

```text
use repository's chosen Python version
install through uv-compatible workflow
start Legacy Device
receive config through environment
support SIGTERM
```

### Important design

Legacy Device does **not** expose a network port.

It is an outbound client:

```text
Legacy container
      │
      └──────> Edge Gateway
```

### Do not add

```text
EXPOSE 8000
```

unless there is a real service requiring it.

### Verification

Member 1 should be able to run the device against a local/test Gateway.

---

# Task M1-14 — Support Docker Compose integration


**Shared with:** Member 5.

Inside the Legacy container, Member 1 should verify this configuration works:

```text
DEVICE_ID=sensor-001
GATEWAY_URL=http://edge-gateway:8000
SEND_INTERVAL_SECONDS=5
REQUEST_TIMEOUT_SECONDS=3
MAX_RETRIES=2
FAILURE_MODE=none
FAILURE_RATE=0.0
FAILURE_SEED=
LOG_LEVEL=INFO
```

At the repository root, Member 5 may expose service-scoped Compose source variables such as:

```text
LEGACY_FAILURE_MODE
LEGACY_FAILURE_RATE
LEGACY_FAILURE_SEED
```

and map them into the Legacy process's internal generic variables:

```text
FAILURE_MODE
FAILURE_RATE
FAILURE_SEED
```

This avoids collisions with Gateway and Cloud failure settings.

Required behaviors:

```text
docker compose up
       ↓
Legacy starts
       ↓
resolves edge-gateway hostname
       ↓
starts generating data
```

And:

```text
docker compose stop
       ↓
SIGTERM
       ↓
Legacy shuts down cleanly
```

Member 1 should not introduce Gateway/Cloud configuration into Legacy code merely because Compose manages all services.

---

# Task M1-15 — Multiple device simulation check

The component should be configurable enough to run:

```text
sensor-001
sensor-002
sensor-003
```

using the same image/code.

Only configuration should change.

Example:

```text
DEVICE_ID=sensor-001
```

versus:

```text
DEVICE_ID=sensor-002
```

No source-code modification.

Member 1 does **not** need to build fleet management.

### Acceptance

Two Legacy Device processes/containers should be able to send measurements independently to the same Gateway.

---

# Task M1-16 — Baseline data collection

The course asks the group to understand the initial architecture, run it, and establish baseline tests and measurements.

Member 1 should help collect Legacy-side baseline evidence once the baseline path works.

Useful observations:

```text
Legacy JSON payload size

Legacy → Gateway request latency

delivery success rate

retry behavior while Gateway unavailable

test count

possibly test coverage
```

Do not over-engineer benchmarking.

Suggested test:

```text
100 measurements
normal failure mode
working Gateway
```

Record:

```text
messages generated
messages delivered
request latency summary
retry count
```

Then run one controlled failure scenario.

---

# Task M1-17 — Validate failure simulation in real system


Once Gateway exists, Member 1 should demonstrate failure injection rather than merely unit-test it.

Example demonstration matrix:

| Failure mode | Expected Gateway result |
|---|---|
| `none` | normal processing |
| `invalid_temperature` | `422` |
| `invalid_humidity` | `422` |
| `missing_field` | `422` |
| `invalid_timestamp` | `422` |
| `duplicate_sequence` | `409` |
| `out_of_order_sequence` | `409` |
| `random` | mixed controlled failures |

For every validation/sequence rejection, verify that the Legacy client's retry behavior follows the protocol.

The boundary is:

```text
malformed/unparseable JSON/body syntax
→ 400

parsed JSON with missing/wrongly typed/domain-invalid required fields
→ 422
```

The current Legacy fault injector creates parsed-but-invalid payloads such as `missing_field`; it does not need to create malformed JSON unless a separate explicit test is added.

Verify:

```text
400 → no retry
409 → no retry
422 → no retry
```

For each scenario, record:

```text
Legacy log
Gateway response
retry behavior
expected result
actual result
whether Cloud was contacted
```

This becomes useful evidence for the technical documentation and presentation.

---

# Task M1-18 — Review network-failure behavior

Network-failure simulation does not initially belong inside `failure.py`.

Member 1 should test these by manipulating the environment or using test doubles:

```text
Gateway stopped
Gateway slow
Gateway returns 500
Gateway returns 503
connection refused
timeout
```

The objective is to prove the client distinguishes:

```text
data failure
vs
network/transient failure
```

---

# Task M1-19 — Verify that failure injection cannot accidentally become normal behavior


Because fault injection deliberately creates bad **wire payloads**, Member 1 must review it carefully.

Required safeguards:

```text
FAILURE_MODE default = none

FAILURE_RATE default = 0.0

startup logs when failure injection enabled

normal Sensor always creates valid Measurement objects

mode=none preserves the serialized payload

fault injection never mutates the internal valid Measurement

duplicate/out-of-order modes alter only outgoing payload state

simulation PRNG never becomes cryptographic RNG
```

Strongly recommended startup warning:

```text
WARNING event=failure_injection_enabled
mode=invalid_humidity
rate=0.2
```

when failure simulation is active.

No simulation marker is added to the wire protocol.

---

# Task M1-20 — Static quality review

Before a Legacy Device PR is considered finished, Member 1 should run the repository's agreed checks, for example:

```bash
uv run pytest legacy_system/tests
uv run ruff check legacy_system
uv run ai-history check
```

Use the actual repository commands if they differ.

Member 1 should manually inspect:

```bash
git status
git diff
```

and verify:

```text
no generated junk
no .env
no .venv
no unrelated files
no debug code
no accidental secrets
```

---

# Task M1-21 — AI-history workflow for every meaningful implementation task

The course explicitly requires the group to use AI for code, manually evaluate AI-generated code continuously, include prompts in technical documentation, and report how AI was used.

Member 1 therefore must follow the repository workflow for AI-assisted tasks.

For example:

```bash
uv run ai-history start
```

Task:

```text
Implement deterministic sensor generation and sequence handling
```

During significant follow-ups:

```bash
uv run ai-history interaction
```

if your updated CLI contains that command.

When implementation is complete:

```bash
uv run ai-history output
```

Then human review:

```bash
uv run ai-history review
```

If modified:

```text
AI revision
↓
uv run ai-history revision
↓
human review again
```

Finally:

```bash
uv run ai-history verify
```

### Member 1 must record

For significant tasks:

```text
task
prompt
relevant output/summary
problems discovered
decision
requested changes
verification
```

### Important

The LLM is explicitly to be treated as an **untrusted assistant**, not as an authority.

Member 1 cannot write:

```text
AI generated it and tests passed, so accepted.
```

Review must actually assess the implementation.

---

# Task M1-22 — Manual review checklist for Legacy AI-generated code


Member 1 should manually inspect AI-generated work for:

### Correctness

```text
correct field names
correct timestamp behavior
correct sequence behavior
correct retry classification
correct failure injection
serialization happens before failure injection
400 = malformed/unparseable body
422 = parsed-but-invalid measurement
missing_field → 422
400/409/422 are not retried
```

### Domain/payload separation

```text
Measurement remains valid
malformed scenarios exist only in outgoing payload representation
missing_field does not require invalid domain object
invalid_timestamp does not corrupt domain model
duplicate/out-of-order simulation does not rewind internal sequence state
```

### Maintainability

```text
clear modules
no unnecessary abstraction
no giant classes
no duplicated configuration
simple interfaces
```

### Testability

```text
randomness injectable
sleep mockable
network mockable
serializer testable independently
failure injector testable with plain payloads
no hardcoded global state preventing tests
```

### Operations

```text
timeouts present
bounded retries
graceful shutdown
useful logs
clear startup failure
```

### Security

```text
no hidden credentials
no unsafe debug output
no protocol-changing hidden fields
no simulation marker on wire
no uncontrolled payload sizes if relevant
simulation seed never affects cryptographic randomness elsewhere
```

### Scope

```text
no Cloud logic
no ML-KEM
no database
no unrelated refactors
```

---

# Task M1-23 — Documentation contribution

Member 1 should maintain:

```text
docs/architecture/legacy-device.md
```

and help update:

```text
docs/architecture/protocol-specification.md
```

only when interface changes are team-approved.

Documentation should cover:

```text
purpose
architecture
data model
configuration
normal behavior
retry behavior
failure modes
logging
testing
Docker behavior
known limitations
technical debt
```

---

# Task M1-24 — Document accepted, modified, and rejected AI decisions


The course requires the team to explain what AI-generated artifacts were accepted, modified, or rejected, why, how problems were identified, and what risks remain.

Member 1 should preserve meaningful examples such as:

```text
AI proposed infinite retry
→ Rejected
Reason:
could block the Legacy Device indefinitely.
```

```text
AI proposed retrying HTTP 422
→ Rejected/Modified
Reason:
sending the same malformed payload again will not repair it.
```

```text
AI proposed retrying HTTP 409
→ Rejected
Reason:
duplicate/out-of-order sequence rejection is a permanent Legacy application result for that request.
```

```text
AI proposed embedding failure_simulation=true in payload
→ Rejected
Reason:
Gateway must not know whether malformed data is simulated.
```

```text
AI proposed mutating the validated Measurement object to remove timestamp
→ Rejected/Modified
Reason:
malformed test state belongs in the serialized outgoing payload, while the domain Measurement remains valid.
```

These are exactly the kinds of decisions that make the final technical documentation stronger.

---

# Task M1-25 — Document Legacy technical debt

Member 1 should maintain the Legacy-specific technical-debt section.

Expected items:

|Technical debt|Why accepted|Future improvement|
|---|---|---|
|No persistent failed-message queue|keeps project simple|disk-backed store-and-forward|
|No strong device authentication|legacy simulation|provisioned credentials|
|Legacy path not PQC-protected|intentional migration boundary|replace/update devices later|
|Simple retry strategy|course scope|jittered exponential backoff|
|Simulated sensor|no hardware requirement|real embedded device|
|No dedicated metrics endpoint|legacy-device simplicity|lightweight telemetry|

The final evaluation must identify remaining technical debt and risks.

---

# Task M1-26 — Support system-level end-to-end testing


Once Members 2–4 complete Gateway/Cloud functionality, Member 1 should help Member 5 with full E2E scenarios.

### Baseline Mode

```text
SECURITY_MODE=classical
```

Flow:

```text
Legacy
↓
Gateway
↓
Cloud baseline endpoint
↓
SQLite
```

Verify the original measurement survives.

### Modernized Mode

```text
SECURITY_MODE=mlkem
```

Flow:

```text
Legacy
↓
Gateway
↓
ML-KEM-768 / HKDF-SHA-256 / AES-256-GCM Cloud path
↓
Cloud
↓
SQLite
```

Legacy itself must behave identically.

This is important:

> The Legacy Device should not need to know whether Gateway→Cloud is running in Baseline Mode or Modernized Mode.

Expected test:

```text
Run 1:
Gateway/Cloud SECURITY_MODE=classical
→ Legacy works

Run 2:
Gateway/Cloud SECURITY_MODE=mlkem
→ same Legacy code/config protocol
→ Legacy works
```

No Legacy-side ML-KEM field, endpoint, or configuration is introduced.

---

# Task M1-27 — Verify Legacy compatibility across modernization


This should become a specific acceptance test.

Baseline:

```text
SAME Legacy v1
    ↓
Gateway Baseline Mode
SECURITY_MODE=classical
```

Modernized:

```text
SAME Legacy v1
    ↓
Gateway Modernized Mode
SECURITY_MODE=mlkem
```

There should be **zero protocol changes required on the Legacy Device**.

Member 1 should confirm:

```text
same POST /api/v1/measurements endpoint
same JSON schema
same response/retry semantics
same Legacy configuration semantics
same HTTP client
same valid Measurement model
same serializer
same sensor implementation
```

Only Gateway→Cloud internals change.

This compatibility proof is one of the strongest demonstrations that the Gateway is acting as the intended modernization boundary.

---

# Task M1-28 — Peer review responsibilities

Member 1 should not review only their own component.

At minimum, Member 1 should review relevant Gateway PRs affecting:

```text
POST /api/v1/measurements
validation
sequence handling
Legacy HTTP error semantics
integration fixtures
```

Questions to check:

```text
Does Gateway still follow our Legacy contract?

Did Member 2 rename fields?

Did status-code semantics change?

Does Gateway still use:
400 for malformed/unparseable JSON,
422 for parsed-but-invalid required fields,
and 409 for duplicate/out-of-order sequence?

Will Legacy incorrectly retry a new error response?

Did Gateway start expecting an extra undocumented field?
```

Any protocol mismatch must be resolved before merge.

---

# Task M1-29 — Integration regression after Gateway changes

Any Gateway PR that modifies:

```text
routes
schema
validation
status codes
```

should trigger the Legacy→Gateway integration suite.

Member 1 should help ensure this is automated in CI.

Goal:

```text
Gateway refactor
↓
Legacy integration tests
↓
contract break detected immediately
```

---

# Task M1-30 — Final component quality pass


Before project freeze, Member 1 should perform one final review of the Legacy component.

Check:

```text
Configuration
✓ clear

Measurement model
✓ valid-domain-only

Serialization boundary
✓ explicit

Sensor
✓ valid deterministic behavior

Sequence
✓ internal sequence monotonic

Timestamp
✓ UTC

Failure injection
✓ serialized payload only
✓ controlled
✓ disabled by default

HTTP client
✓ receives prepared payload
✓ bounded timeout/retry
✓ 400/409/422 non-retryable
✓ 400 = malformed/unparseable body
✓ 422 = parsed-but-invalid measurement

Runtime loop
✓ generate → serialize → inject → send

Shutdown
✓ clean

Logging
✓ useful

Tests
✓ meaningful

Docker
✓ reproducible

Documentation
✓ current

AI history
✓ complete
```

Also remove:

```text
temporary debug prints
TODOs that should have been completed
unused imports
unused configuration
unused dependencies
dead test helpers
accidental simulation metadata
```

---

# Member 1 dependency map

Member 1 can work largely independently initially:

```text
Protocol Specification
        ↓
   Member 1
        │
        ├── Config
        ├── Valid Measurement model
        ├── Sensor
        ├── Serializer / payload boundary
        ├── Failure injector
        ├── HTTP client
        └── Tests
```

Then Member 1 becomes dependent on Member 2:

```text
Legacy
  ↓
Gateway API
```

Later Member 1 has **no direct dependency on Cloud implementation**.

That is intentional.

```text
Legacy
knows Gateway

Legacy
does NOT know Cloud
```

---

# Recommended Member 1 task order

I would assign Member 1 the work in exactly this sequence:

```text
M1-00  Review/freeze Legacy protocol

M1-01  Configuration

M1-02  Measurement model + serializer/payload boundary

M1-03  Sensor generation

M1-04  Serialized-payload failure injector

M1-05  Gateway HTTP client

M1-06  Retry/backoff behavior

M1-07  Main runtime loop

M1-08  Graceful shutdown

M1-09  Logging

M1-10  Complete unit tests

M1-11  Shared test fixtures

M1-12  Gateway integration tests

M1-13  Dockerfile

M1-14  Docker Compose integration

M1-15  Multiple-device verification

M1-16  Baseline measurements

M1-17  Real failure-mode demonstrations

M1-18  Network-failure verification

M1-19  Failure-injection safety review

M1-20  Static/code-quality review

M1-21  AI-history completion

M1-22  Human review of AI-generated artifacts

M1-23  Documentation

M1-24  AI decision documentation

M1-25  Technical-debt documentation

M1-26  Full E2E support

M1-27  Legacy compatibility test

M1-28  Gateway peer review

M1-29  Integration regression verification

M1-30  Final quality pass
```

---

# Suggested PR breakdown for Member 1

I would **not** put all 30 items into one branch. A better PR breakdown is:

|PR|Scope|
|---|---|
|PR 1|Legacy configuration + valid Measurement model + serializer|
|PR 2|Sensor generator + sequence behavior|
|PR 3|Gateway HTTP client + retry|
|PR 4|Serialized-payload failure-injection subsystem|
|PR 5|Device runtime + graceful shutdown + logging|
|PR 6|Legacy test-suite completion|
|PR 7|Docker packaging|
|PR 8|Legacy↔Gateway integration tests|
|PR 9|Baseline/failure evaluation + documentation|

This gives the team manageable human-review units.

---

# Member 1 milestone gates

### Gate A — Core simulation ready

Required:

```text
configuration
valid Measurement model
serializer / outgoing payload boundary
sensor
sequence
timestamps
```

No Gateway required yet.

### Gate B — Standalone Legacy complete

Required:

```text
HTTP client
retry
serialized-payload failure injection
runtime
shutdown
logging
unit tests
```

Can use mocked Gateway.

### Gate C — Real Gateway compatible

Required:

```text
valid data accepted
invalid data rejected
correct retry behavior
sequence scenarios work
```

### Gate D — Container ready

Required:

```text
Docker
Compose compatibility
clean shutdown
```

### Gate E — Project-ready Legacy component

Required:

```text
baseline evidence
failure scenarios
E2E compatibility
documentation
AI history
human review
technical debt
```

---

# Final Definition of Done for Member 1

Member 1's work is complete only when all of these are true:

```text
[ ] Legacy Device produces valid deterministic sensor measurements.

[ ] `Measurement` represents valid internal state only.

[ ] A separate serializer converts `Measurement` into the outgoing Legacy payload.

[ ] Failure injection operates on the serialized outgoing payload, not on the valid domain object.

[ ] `missing_field` and `invalid_timestamp` can be represented without corrupting `Measurement`.

[ ] Duplicate/out-of-order simulation mutates outgoing payload only; internal sequence state remains monotonic.

[ ] JSON exactly follows the frozen Legacy→Gateway contract.

[ ] UTC timestamp behavior is correct.

[ ] Sequence numbers behave as designed.

[ ] Failure injection supports all agreed initial modes.

[ ] Failure injection defaults to disabled.

[ ] Failure injection supports deterministic seeded testing.

[ ] Legacy Device does not send simulation metadata to Gateway.

[ ] Gateway communication uses explicit timeout.

[ ] Retry behavior is bounded.

[ ] Retryable/non-retryable failures are correctly distinguished, including `400/409/422` as non-retryable.

[ ] `400` is used for malformed/unparseable JSON/body syntax.

[ ] `422` is used for parsed JSON with missing, wrongly typed, or domain-invalid required fields.

[ ] `missing_field` integration tests expect `422`.

[ ] Failed measurements are deliberately discarded after retry exhaustion.

[ ] Device continues after normal delivery failures.

[ ] Graceful shutdown works.

[ ] Logging is useful and safe.

[ ] Unit tests cover configuration, valid domain model, serialization, sensor, payload failure injection, client and controller.

[ ] Real Device↔Gateway integration tests pass.

[ ] Invalid Legacy data is rejected by Gateway.

[ ] Network failure behavior is verified.

[ ] Docker image works.

[ ] No unnecessary inbound port is exposed.

[ ] Multiple device instances can be configured without source changes.

[ ] Legacy Device works unchanged in Baseline Mode (`SECURITY_MODE=classical`).

[ ] Legacy Device works unchanged in Modernized Mode (`SECURITY_MODE=mlkem`).

[ ] Baseline measurements have been recorded.

[ ] Technical debt is documented.

[ ] Architecture documentation is current.

[ ] Significant AI prompts and outputs are recorded.

[ ] AI-generated code has been manually reviewed.

[ ] Accepted/modified/rejected AI decisions are documented.

[ ] Relevant tests, Ruff/static checks and AI-history validation pass.

[ ] No secrets, .env files, virtual environments or unrelated artifacts are committed.

[ ] Relevant Gateway PRs have received Legacy-contract review.

[ ] CI passes.

[ ] Another teammate has reviewed the final PR.
```

This gives **Member 1 a clearly bounded but substantial role**: they own the complete legacy simulation from configuration and valid data generation through serialization, wire-payload fault injection, HTTP behavior, testing, Dockerization, baseline evidence, and the actual compatibility proof showing that the same old device continues to operate after the Gateway→Cloud path is modernized with ML-KEM. That last point is particularly important because preserving or explicitly addressing legacy compatibility is one of the stated project objectives.
