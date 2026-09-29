# Cloud canonical validation (M4-04)

Use `cloud_service.validation.validate_measurement(payload)` for an already-
decoded canonical JSON object. It returns a `CanonicalMeasurement` only after
schema and domain validation. It does not mutate input or normalize identifiers.

The M4-03 parser enforces the exact fields, strict scalar types, finite numbers,
and valid timezone-aware UTC timestamps. M4-04 additionally requires non-empty
device/Gateway IDs (whitespace-only is empty), temperature from -40 through 85,
humidity from 0 through 100, and a sequence number of at least zero. Boundary
values are inclusive. No freshness window, sequence ordering, or extra timestamp
ordering rule is introduced.

Secure callers must supply `expected_gateway_id` obtained from the verified
envelope/session identity. The payload Gateway ID must match exactly; case and
whitespace are not normalized. An empty or non-string expected ID is rejected.
Baseline callers omit this argument. This optional baseline entry point does
not authenticate a Gateway or perform secure processing: future secure routes
must check session lookup, ownership, expiry and AEAD authentication first, then
invoke this validator with the trusted identity. Never derive the expected ID
from the decrypted measurement itself.

Schema and domain failures raise `MeasurementValidationError` with safe messages
that do not echo payload values. HTTP status mapping belongs to future routes;
this function neither assigns status codes nor writes records. No routes,
storage, cryptographic behavior, or dependencies change in M4-04.

Run `uv run --frozen --all-packages --all-extras pytest cloud_service/tests`.
