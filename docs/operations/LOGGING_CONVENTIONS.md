# Project-wide logging conventions

This is the Member 5 coordination convention for M5-46. Members 1–4 retain
ownership of their component log implementations. This document does not by
itself require a logging refactor or establish end-to-end correlation; those
are addressed by later component and M5-47 work.

## Event format

Emit one concise, structured-text event per significant outcome. The preferred
shape is space-separated `key=value` fields, beginning with a stable,
lowercase `event` name such as `event=session_established`. Values derived
from requests must be safely quoted or bounded; do not concatenate raw request
bodies, headers, or exception text into an event.

Every new event includes:

| Field | Meaning |
|---|---|
| `event` | Stable snake_case action or outcome name. |
| `component` | `legacy_system`, `edge_gateway`, or `cloud_service`. |
| `request_id` | Include when the component has one; omit when none exists. |
| `device_id` | Include when a measurement/device is known. |
| `gateway_id` | Include when a Gateway identity is known. |
| `sequence_number` | Include when a measurement sequence is known. |

For the current application logs, the logger name may supply the component
identity while components are incrementally aligned to this convention. New
events should include the explicit `component` field so log aggregation does
not depend on logger configuration.

Include these only when relevant and available:

| Field | Appropriate use |
|---|---|
| `session_id` | Session lifecycle, secure delivery, or session rejection. |
| `key_id` | Public-key selection, rotation, or session establishment metadata. |
| `record_id` | Cloud persistence and query outcomes. |
| `status` | HTTP/application outcome, never a raw response body. |
| `attempt` | A bounded retry or recovery attempt number. |
| `failure_type` | Stable, safe operational category such as `storage_failure`. |

`request_id` and `session_id` are log correlation fields, not metric labels.
They must never be introduced as unbounded Prometheus labels.

## Levels

| Level | Use |
|---|---|
| `DEBUG` | Safe diagnostic metadata useful during development; never values that are prohibited below. |
| `INFO` | Lifecycle, accepted processing, session establishment, and normal state transitions. |
| `WARNING` | Validation rejection, retry, expected injected fault, session rejection, or recoverable dependency failure. |
| `ERROR` | Startup failure, internal service fault, or an operation that cannot be completed safely. |

Legacy-facing failures must remain safe and structured at the HTTP boundary.
Logging an event must not change the frozen response code, retry policy, or
fail-closed behavior.

## Prohibited material

Never log, serialize into event fields, or include in exception messages:

- ML-KEM private keys, public-key byte material, encapsulation ciphertexts, or
  raw cryptographic nonces/ciphertexts;
- ML-KEM shared secrets, AES-GCM session keys, derived keys, or key buffers;
- passwords, tokens, credentials, `.env` contents, or connection secrets;
- full request/response bodies or unbounded user-supplied headers;
- raw stack traces or vendor exception text when it could reveal the material
  above.

Use a stable safe category (`failure_type`, `status`, or application error
code) rather than sensitive diagnostic data. Automated secret-marker tests
belong to M5-49/M5-50 and component-owned crypto tests.

## Review checklist

- Event names are stable snake_case and describe outcomes, not implementation
  details.
- Available common correlation fields are present and safely formatted.
- Retry and recovery entries include a bounded `attempt` when applicable.
- No event introduces request/session identifiers as metric labels.
- Logs contain no prohibited material, raw payload, or raw exception text.
