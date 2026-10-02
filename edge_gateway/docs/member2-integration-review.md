# Peer review of Member 2 integration

This note records Member 3's review of the current Gateway integration. It does not change Gateway code.

Reviewed areas: `SECURITY_MODE` dispatch, the transport boundary, `request_id` propagation, PQC failure mapping, readiness, and failure-injection boundaries.

## Legacy route and modernized mode

`POST /api/v1/measurements` parses and validates the Legacy body, then calls `MeasurementProcessor.process`. The handler does not choose a transport and does not read `FAILURE_MODE`. `CloudDispatch.send` calls the baseline transport only when `SECURITY_MODE` is `classical`. In `mlkem` it calls `SecureTransport`. If `mlkem` is configured without a secure transport, the application leaves dispatch unset and the processor returns `503 CLOUD_UNAVAILABLE`. `_baseline_transport` constructs `BaselineCloudClient` only for classical mode.

## Request correlation

`CanonicalMeasurement` holds `device_id`, `temperature_c`, `humidity_pct`, `measured_at`, `sequence_number`, `received_at`, and `gateway_id`. It has no `request_id`. The processor creates the request ID after normalization and passes it as its own argument. Baseline mode puts that ID in the `X-Request-ID` header. The baseline JSON body is the canonical measurement. Modernized mode passes the same ID into `SecureTransport.send`, which places it in the envelope and the four-field AAD and also sends it as `X-Request-ID`.

## Fail closed

`CloudDispatch` accepts only `PQC_FAILURE_POLICY=fail_closed`. A `SecureTransportError` increments `secure_failures_total`, logs `event=pqc_fail_closed`, and is raised again. That handler does not call the baseline transport, and the mode does not change. `SessionEstablishmentError` becomes `SecureTransportError` inside the secure transport before dispatch sees it.

## Session recovery

HTTP 409 `SESSION_INVALID` and `SESSION_EXPIRED` are handled inside `SecureTransport`. The transport invalidates the old session, establishes one replacement, rebuilds the envelope with the same `request_id`, and posts once. A second 409 during that recovery becomes `SecureTransportError` and is not recovered again. The Legacy route does not add its own retry loop.

## Readiness and error translation

`GET /ready` returns unavailable and does not read session state, so readiness does not require an already-active session. It is still the placeholder and does not report that the process is ready to deliver. Delivery failures of type `SecureTransportError`, `TimeoutError`, and `ConnectionError` become `GatewayError` `CLOUD_UNAVAILABLE` with the original exception detached. The HTTP handler returns the fixed error body. The catch-all logs `gateway_internal_error` and does not include the exception text.

## Failure injection

`FAILURE_MODE` is applied by the crypto injector while establishing a session or sealing a ciphertext. The Legacy handler and `CloudDispatch` do not select or suppress those faults, and a fault does not switch the process to baseline mode.

## Review result

The inspected integration keeps modernized delivery on `SecureTransport` and keeps baseline delivery on the explicit classical path. The recorded limits are the placeholder `/ready` response and the absence of a cryptographic replay window, which remains outside this integration.
