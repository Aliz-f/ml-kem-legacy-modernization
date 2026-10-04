# Cloud SQLite persistence strategy

This document implements Member 5 task M5-11. It describes the Cloud-owned
SQLite configuration used by the current three-service Docker Compose test
deployment. It does not add database migrations or additional Docker Compose
services.

## Storage boundary

The Cloud Service owns `DATABASE_URL` and its SQLite initialization. It
accepts only `sqlite:///` URLs for either a database file or `:memory:`. The
measurement table provides the frozen logical idempotency constraint
`UNIQUE(device_id, sequence_number)`.

The database contains accepted measurement records and their Cloud metadata.
It must not persist ML-KEM private keys, ML-KEM shared secrets, derived session
keys, or secure-session state. Cloud keys and sessions remain process-local and
are intentionally lost when the Cloud process restarts.

## Development and demonstration mode

For a containerized demonstration, use a named Docker volume mounted at
`/data`, with the Cloud's existing container default:

```text
DATABASE_URL=sqlite:////data/cloud.db
```

The current Compose Cloud service mounts the named `cloud-data` volume at
`/data` on each normal start. As a result, restarting or recreating only the Cloud
container retains accepted measurement rows, allowing the query API to show
accumulated demo data. It does not retain Cloud cryptographic identity or an
active Gateway session, so a Gateway must establish a fresh secure session
after a Cloud restart.

The directory must be writable by the non-root Cloud container user. The
existing Cloud Dockerfile creates `/data` with the required ownership. No
separate database service is needed: SQLite remains inside the Cloud
container's mounted storage.

## Clean automated-test mode

Automated tests must not reuse a development/demo database volume. Use one of
these isolated modes:

- For a process-local unit test, set `DATABASE_URL=sqlite:///:memory:`. The
  database exists only for that connection and disappears when it closes.
- For tests that need reopen/persistence behavior, use a uniquely created
  temporary database file and remove its temporary directory through the test
  framework.
- For Compose tests, use a fresh temporary volume/project for each test run
  and remove it with `docker compose down -v` (or the equivalent `--volumes`
  command).

Do not bind automated tests to a developer's persisted demo volume. A clean
database ensures deterministic idempotency, query, and measurement-count
assertions.

## Operational limits

SQLite is deliberately course-sized storage. It is appropriate for the
single-Cloud-instance demonstration but is not a multi-writer distributed
database strategy. Schema migrations and externally modifying the database
file are unsupported. Database backups, access control, encryption at rest,
and a production database migration remain out of scope for protocol version
1 and should be recorded as future operational decisions if the project is
expanded.
