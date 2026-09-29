# Canonical Cloud measurement (M4-03)

`cloud_service.models.CanonicalMeasurement.from_dict(payload)` parses an
already-decoded JSON object into a frozen dataclass. Cloud owns this model and
does not import Gateway models. It requires the seven shared canonical fields:
`device_id`, `temperature_c`, `humidity_pct`, `measured_at`, `sequence_number`,
`received_at`, and `gateway_id`. Missing and extra fields are rejected.

IDs must be strings, sensor values finite JSON numbers, and sequence numbers
integers. Booleans and numeric strings are not coerced. Timestamps must be
ISO-8601 date/time strings with a `T` separator and an explicit zero UTC offset
(`Z` or `+00:00`). Invalid dates, naive timestamps, and non-UTC offsets are
rejected. Internally timestamps are Python datetimes, with microsecond precision.
`to_dict()` produces JSON-compatible fields and UTC timestamps ending in `Z`.
The input dictionary is not mutated. Direct construction checks field types
and requires UTC datetime objects as well.

`MeasurementSchemaError` identifies schema failures without echoing payload
values. Parsing does not assign an HTTP status; endpoint syntax/error handling
is a later task. Request IDs, Legacy `timestamp`, and Cloud storage metadata do
not belong in this model. Storage will map `received_at` to
`gateway_received_at` in M4-05; M4-03 does not rename it.

This completes the schema prerequisite for PR 2, not persistence validation.
M4-04 remains responsible for non-empty IDs, temperature/humidity ranges,
non-negative sequences, and envelope/session Gateway identity consistency.
Successful schema parsing alone must not authorize persistence. There are no
new routes, database operations, dependency changes, or shared-model imports.
