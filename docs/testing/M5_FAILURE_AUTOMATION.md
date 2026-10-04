# M5-40 through M5-45 failure automation evidence

This index records the Member 5 cross-component evidence without adding a
second failure protocol. All listed failure modes are local configuration and
are disabled by default.

| Task | Automated evidence | Frozen outcome checked |
|---|---|---|
| M5-40 | `tests/integration/test_failure_paths.py` | Actual Legacy wire payloads mutated by the Legacy injector receive `422` or `409` without a Legacy retry or Cloud delivery. A separate raw malformed body receives `400`. |
| M5-41 | `edge_gateway/tests/test_gateway_application_failures_integration.py` | `processing_error`, `cloud_timeout`, `cloud_unavailable`, and `drop_message` produce visible failure and never false Cloud acceptance. Cloud transport retries remain bounded. |
| M5-42 | `edge_gateway/tests/test_crypto_failures.py`, `tests/integration/test_mlkem_handshake_failure_demo.py`, and `tests/integration/test_session_expiry_system.py` | Handshake failure is fail closed with no baseline call; ciphertext rejection stores nothing; session faults re-establish once. |
| M5-43 | `cloud_service/tests/test_cloud_failure_injection.py` and `tests/integration/test_gateway_cloud_secure.py` | Each Cloud fault has its fixed result. The simulated decapsulation failure is an operational wrapper fault, not a claim about arbitrary valid-length ML-KEM ciphertext changes. |
| M5-44 | `tests/integration/test_modernized_end_to_end.py` and `tests/integration/test_gateway_cloud_secure.py::test_ambiguous_transport_retries_the_same_envelope` | A lost post-persistence response triggers an ordinary resend of byte-identical `request_id`, `session_id`, nonce, ciphertext, and AAD; exactly one `(device_id, sequence_number)` row remains. |
| M5-45 | `tests/integration/test_retry_amplification.py` | Three Legacy attempts times three Gateway Cloud attempts gives at most nine downstream attempts. The test also demonstrates that committed Gateway sequence state terminates a repeated Legacy retry with `409`. |

## Operational limitation

The `3 × 3 = 9` maximum is intentional, bounded course-scale behavior, not a
claim that retry layering is cost-free. It remains technical debt to revisit if
the system gains higher request rates or more retrying intermediaries.

## M5-80 Legacy continuity evidence

`tests/integration/test_end_to_end.py::test_legacy_controller_continues_after_bounded_cloud_delivery_failure`
starts production Legacy, Gateway, and Cloud application instances in
Classical Mode. It injects one Cloud storage failure, verifies the Legacy
client's retry is bounded, and then removes the injected Cloud failure before
the next controller iteration. The test proves that the Legacy controller
generates sequence `0` and later sequence `1`, logs the failed first delivery,
and persists only sequence `1` after recovery. It therefore documents the
intentional no-queue behavior: a delivery failure may discard a measurement,
but must not permanently stall future Legacy measurements.

## Scope limits

Protocol v1 has no cryptographic replay counter or window. M5-44 proves only
the frozen business-idempotency rule, `UNIQUE(device_id, sequence_number)`, for
the ordinary same-envelope retransmission path. Session recovery is separate:
it has one replacement handshake, a rebuilt envelope, and the same logical
request ID.
