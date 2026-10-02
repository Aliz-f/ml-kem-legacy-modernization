# Cloud SQLite persistence strategy

This document implements Member 5 task M5-11. It describes how the existing
Cloud-owned SQLite configuration is used in a future container deployment; it
does not add Docker Compose services, volumes, migrations, or a database
server.

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

The future Compose service should mount the same named volume at `/data` on
each normal start. As a result, restarting or recreating only the Cloud
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
- Once Docker Compose is introduced, use a fresh temporary volume for each
  test run; remove it after the run. `docker compose down -v` will be
  documented with the one-command environment task, not treated as an existing
  command in this repository.

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
