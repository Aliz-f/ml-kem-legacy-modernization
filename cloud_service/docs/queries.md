# Measurement queries (M4-12 through M4-13)

`GET /api/v1/measurements` returns `200 {"items": [...]}` using the authoritative
shared protocol section 50. The older bare-array example in Cloud design
section 30 is not used. Items contain exactly the nine stored-model fields,
including `gateway_received_at` and `cloud_received_at`, with explicit UTC
timestamps. Queries never write data or expose request IDs or crypto material.

Optional parameters:

- `device_id`: exact device filter, passed as a bound SQLite parameter.
- `limit`: decimal integer, default 100, minimum 1, maximum 1000. Invalid,
  empty, non-integer or out-of-range input returns structured
  `422 INVALID_QUERY`; oversized requests are rejected rather than clamped.

Results preserve the repository's insertion order. The SQL query applies the
limit; it does not first load an unbounded set. The maximum of 1000 is the
course-sized implementation choice requested by M4-13. There is no offset,
cursor, arbitrary sorting, or analytics API.

`GET /api/v1/measurements/{record_id}` returns the stored object directly with
`200`, or structured `404 MEASUREMENT_NOT_FOUND` when absent. Empty list/filter
results return `{"items": []}`. Storage failures return `503 STORAGE_UNAVAILABLE`,
and unexpected query failures return `500 INTERNAL_ERROR`; neither is reported
as an empty result. Errors use the common `error.code`/`error.message` shape
without exposing exception details. The query-specific 422/404 codes document
implementation choices where the task did not prescribe a code.

Both routes reuse the repository via a worker thread. Tests seed the repository
directly and cover the full response shape, missing records, filtering, bounds,
parameterization and safe failures. This task does not implement M4-14
Gateway-to-Cloud integration or any later feature. Full readiness remains
separate work; existing health, metrics and security behavior are unchanged.

Run `uv run --frozen --all-packages --all-extras pytest cloud_service/tests`.
