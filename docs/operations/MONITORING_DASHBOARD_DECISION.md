# Monitoring dashboard decision

This record implements Member 5 task M5-56.

## Decision

Do not add Grafana, a Prometheus server, or another dashboard service for this
course-scale system. The existing Gateway and Cloud `GET /metrics` endpoints
are sufficient for the current demonstrations, integration tests, failure
analysis, and final evaluation evidence.

This preserves the course requirement for meaningful metrics while following
the explicit scope constraint that a dashboard is optional and the project
should stay small. It adds no extra containers, persistent monitoring data,
credentials, network surface, or operational lifecycle to maintain.

## Evidence

- The frozen metric contract defines bounded application, secure-session,
  failure, retry, and storage metrics in
  [`METRICS_CONVENTIONS.md`](METRICS_CONVENTIONS.md).
- M5-51 queries both services' endpoints from the live test environment in
  `tests/integration/test_observability_integration.py` and the Docker Compose
  test in `tests/integration/test_gateway_compose_e2e.py`.
- The M5-65–M5-70 evaluation harness captures the same bounded session and
  delivery metrics for reproducible comparison evidence.
- Correlation remains in logs; `request_id`, `session_id`, and other
  identifiers are not dashboard or metrics labels.

## Operating procedure

For a local Gateway/Cloud test environment, query the two endpoints directly:

```bash
curl --fail http://127.0.0.1:${GATEWAY_HOST_PORT:-8000}/metrics
curl --fail http://127.0.0.1:${CLOUD_HOST_PORT:-9000}/metrics
```

Use the documented metric families to inspect accepted/rejected measurements,
Cloud attempts and retries, ML-KEM handshakes, active sessions, decryptions,
and storage outcomes. Do not treat a scrape as a replacement for the
integration and E2E tests that establish their semantics.

## Revisit conditions

Reconsider a dashboard only if it materially helps a scheduled demonstration
or a documented test deployment and the team has time to operate it. Any later
proposal must preserve bounded labels, avoid secret/identifier exposure, define
container lifecycle and persistence, and justify its scope before adding
monitoring infrastructure.
