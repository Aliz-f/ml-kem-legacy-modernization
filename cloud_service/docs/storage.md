# Cloud storage (M4-05 through M4-07)

The Cloud-owned `storage` package uses Python's standard `sqlite3` module. It
adds no dependencies or shared application models.

`StoredMeasurement.from_canonical(measurement)` adds a UUID-based `rec-` ID
and a UTC Cloud timestamp. It preserves device/Gateway IDs, sensor values,
measurement time, and sequence, mapping canonical `received_at` to
`gateway_received_at`. Its nine fields match the frozen storage contract;
there are no request IDs, keys, sessions, envelopes or extra timestamps.
Domain/schema checks run before saving, including for directly constructed
canonical objects. Secure caller identity verification remains a caller duty.

`Database(database_url)` opens SQLite and creates the table if absent.
The primary key is `record_id`; `UNIQUE(device_id, sequence_number)` enforces
the frozen logical identity. Reopening does not delete existing data. File
paths follow the configuration documentation; parent directories must exist.
`:memory:` is local to one connection and disappears when closed. Datetimes
are stored as explicit UTC ISO-8601 text with microsecond precision. SQLite
stores sequences as signed 64-bit integers; larger schema-valid integers cause
a safe storage failure rather than truncation or a protocol-validation change.

`MeasurementRepository` provides:

- `save(canonical)` validates and commits a new record before returning it.
- `save_idempotent(canonical)` returns `SaveResult(measurement, created)` after
  commit; duplicates return the original row with `created=False`.
- `get(record_id)` returns a stored model or `None`.
- `find_by_device_sequence(device_id, sequence_number)` returns a model or `None`.
- `list(limit=100, device_id=None)` returns at most the requested positive
  integer limit, in stable insertion order, optionally filtered by device.

Queries use bound SQL parameters. One process-local reentrant lock serializes
connection use across application threads. Each repository operation owns its
transaction; write failure rolls it back. Call `Database.close()` to release
the connection; repeated close is harmless and later operations fail safely.
The app lifespan initializes storage before liveness and closes it on shutdown;
it exposes `app.state.database` and `app.state.repository` while running.

SQLite operational errors become `StorageError`; constraint violations become
`StorageConflictError`. Neither exposes database paths, SQL or payload values.
Invalid stored data is also translated to a safe storage error. These are
internal exceptions, not new HTTP status contracts. Schema evolution/migrations
and external modifications of the database are not supported by this initial
table initializer.

M4-08 adds idempotent insertion with a conflict clause targeted only at
`(device_id, sequence_number)`. Insert and lookup run in the same transaction,
including across separate connections; the returned result is released after
commit. The first valid accepted data and Cloud metadata are preserved even if
a repeated logical identity carries different valid values. Unrelated record-ID
collisions still raise a storage conflict. The original `save` remains a strict
insert API; baseline ingestion uses `save_idempotent`.

This is business idempotency, not cryptographic replay protection. M4-10 adds
the baseline ingestion route; query routes and complete readiness remain later
tasks. PR 2 storage alone does not satisfy baseline E2E.

Run `uv run --frozen --all-packages --all-extras pytest cloud_service/tests`.
Tests use temporary files or private in-memory databases and cover schema,
mapping, file reopen, lookup, list/filter/limit, rollback, uniqueness conflicts,
parameter binding, concurrent use, startup failure and shutdown cleanup.
