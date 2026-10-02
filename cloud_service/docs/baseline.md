# Baseline ingestion (M4-08 through M4-11)

With explicit `SECURITY_MODE=classical`, send canonical JSON to
`POST /api/v1/baseline/measurements` with `Content-Type: application/json` and
the Gateway-generated `X-Request-ID` header. The body has only the seven fields
defined by the shared canonical contract; no request ID is added to it.

Processing is parse, schema/domain validation, atomic idempotent persistence,
then response. The stored mapping preserves measurement fields, renames
`received_at` to `gateway_received_at`, and adds `record_id` and
`cloud_received_at`. Routes contain no SQL and perform no ML-KEM or AEAD.

| Outcome | Response |
|---|---|
| New measurement committed | `202 {"status":"accepted","record_id":"rec-..."}` |
| Existing device/sequence pair | `202 {"status":"already_accepted","record_id":"rec-existing"}` |
| Malformed JSON or text encoding | `400`, `INVALID_JSON` |
| Parsed but invalid canonical measurement | `422`, `INVALID_MEASUREMENT` |
| Storage unavailable or write failure | `503`, `STORAGE_UNAVAILABLE` |
| Unexpected repository failure | `500`, `INTERNAL_ERROR` |

Errors have the shared `{"error":{"code":...,"message":...}}` shape and
do not expose library exceptions or payloads. Duplicate bodies must still pass
validation. Identity is `(device_id, sequence_number)`, not request ID or
Gateway ID. Retries preserve the existing row and its metadata rather than
overwriting it. If a response is lost after commit, repeating the request
returns the existing record. Distinct sequences or devices create distinct rows.

The request header is diagnostic metadata only. Logs contain its escaped text
(bounded to 256 characters), result and record ID, never the request body.
Missing headers are logged as `None`; Cloud does not generate a replacement
Gateway request ID or use it for idempotency. No correlation value is persisted
in the canonical or stored model.

The route-level mode check prevents baseline acceptance outside classical mode.
In `mlkem` mode, secure ingestion is handled only by the separate secure
endpoint; there is no runtime plaintext fallback. Query, secure-protocol,
readiness, metrics, and failure-injection behavior remain separate concerns
from this baseline route.

Run `uv run --frozen --all-packages --all-extras pytest cloud_service/tests`.
Tests cover committed visibility, lost-response retry semantics, concurrent
duplicates across connections, distinct logical identities, malformed/invalid
input, storage failure and retry, safe internal failures, correlation, and mode
separation. Local HTTP-to-SQLite verification is not full Legacy/Gateway E2E.
