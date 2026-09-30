# Graph Report - ml-kem-legacy-modernization  (2026-10-01)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1595 nodes · 3904 edges · 94 communities (60 shown, 34 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 523 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- decrypt
- FailureMode
- load_config
- SessionManager
- test_client.py
- SecureTransport
- secure_transport.py
- test_sensor.py
- test_public_key_client.py
- MeasurementRepository
- load_config
- test_session.py
- derive_session_key
- LegacyMeasurement
- test_dispatch.py
- measure_baseline.py
- create_app
- PqcMetrics
- test_session_recovery_is_counted
- StoredMeasurement
- cli.py
- CanonicalMeasurement
- encapsulate
- GatewayErrorCode
- test_secure_message_tamper.py
- session_client.py
- edge_gateway/validation.py
- test_cloud_mlkem.py
- validate_measurement
- edge_gateway/config.py
- decode_binary
- SecureSession
- test_gateway_canonical_model.py
- test_secure_shutdown.py
- test_secure_transport.py
- test_gateway_cloud_secure.py
- Policy
- test_cloud_queries.py
- public_key.py
- _fixture
- plaintext.py
- test_gateway_validation.py
- cloud_service/crypto/mlkem.py
- routes.py
- test_cloud_baseline.py
- test_security_logging.py
- test_cloud_kdf.py
- CryptoFailureInjector
- pytest
- SessionManager
- test_crypto_failures.py
- refresh_graphify.py
- test_legacy_values_survive_secure_delivery
- test_cloud_public_key.py
- validate
- cloud_service/app.py
- sessions.py
- HistoryError
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- .__init__
- _Clock
- _HandshakeHandler
- record_work
- cloud_service/crypto/symmetric.py
- _seal
- StartupError
- test_repository_hygiene.py
- AadError
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- _Handler
- _Handler
- Clock
- _measurement
- .shutdown
- _Handler
- _RejectRedirect
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `SecureTransport` - 41 edges
2. `load_config()` - 41 edges
3. `load_config()` - 37 edges
4. `SessionManager` - 36 edges
5. `create_app()` - 36 edges
6. `create_app()` - 35 edges
7. `FailureMode` - 33 edges
8. `SecureTransportError` - 33 edges
9. `PqcMetrics` - 32 edges
10. `MeasurementRepository` - 32 edges

## Surprising Connections (you probably didn't know these)
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/aad.py
- `test_valid_encapsulation_matches_shared_secret_and_hkdf()` --uses--> `SessionState`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/crypto/session.py
- `test_legacy_values_survive_secure_delivery()` --uses--> `CloudDispatch`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/dispatch.py
- `test_secure_failure_does_not_call_baseline()` --uses--> `CloudDispatch`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → edge_gateway/src/edge_gateway/dispatch.py
- `CloudHarness` --uses--> `StoredMeasurement`  [INFERRED]
  tests/integration/test_gateway_cloud_secure.py → cloud_service/src/cloud_service/storage/models.py

## Import Cycles
- None detected.

## Communities (94 total, 34 thin omitted)

### Community 0 - "decrypt"
Cohesion: 0.06
Nodes (49): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+41 more)

### Community 1 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 2 - "load_config"
Cohesion: 0.08
Nodes (29): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+21 more)

### Community 3 - "SessionManager"
Cohesion: 0.08
Nodes (19): SecureSession, SessionAccessError, SessionManager, SessionState, handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak() (+11 more)

### Community 4 - "test_client.py"
Cohesion: 0.10
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 5 - "SecureTransport"
Cohesion: 0.10
Nodes (14): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport (+6 more)

### Community 7 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 8 - "test_public_key_client.py"
Cohesion: 0.10
Nodes (18): _endpoint(), fetch_public_key(), PublicKeyTransportError, PublicKeyRejected, _body(), cloud_server(), _Handler, _public_key() (+10 more)

### Community 9 - "MeasurementRepository"
Cohesion: 0.12
Nodes (20): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), test_closed_database_errors_are_safe(), test_concurrent_repository_access() (+12 more)

### Community 10 - "load_config"
Cohesion: 0.14
Nodes (18): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+10 more)

### Community 11 - "test_session.py"
Cohesion: 0.12
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+6 more)

### Community 12 - "derive_session_key"
Cohesion: 0.11
Nodes (12): KdfError, derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged() (+4 more)

### Community 13 - "LegacyMeasurement"
Cohesion: 0.18
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 14 - "test_dispatch.py"
Cohesion: 0.13
Nodes (11): CloudDispatch, _Baseline, _Handler, _measurement(), _Secure, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline(), test_failure_log_omits_the_measurement() (+3 more)

### Community 15 - "measure_baseline.py"
Cohesion: 0.11
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 16 - "create_app"
Cohesion: 0.11
Nodes (18): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+10 more)

### Community 18 - "test_session_recovery_is_counted"
Cohesion: 0.09
Nodes (10): _Sessions, _Baseline, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+2 more)

### Community 19 - "StoredMeasurement"
Cohesion: 0.13
Nodes (6): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 21 - "cli.py"
Cohesion: 0.28
Nodes (16): start(), state_name(), Status, active_task(), atomic_write(), find_task(), git_changes(), load_state() (+8 more)

### Community 22 - "CanonicalMeasurement"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 23 - "encapsulate"
Cohesion: 0.15
Nodes (12): test_gateway_cloud_mlkem_and_kdf_interoperability(), test_key_services_are_independent_and_close_is_idempotent(), encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected() (+4 more)

### Community 24 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 25 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 26 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 27 - "edge_gateway/validation.py"
Cohesion: 0.13
Nodes (9): normalize(), LegacyJSONError, LegacyMeasurementDomainError, _reject_constant(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input() (+1 more)

### Community 28 - "test_cloud_mlkem.py"
Cohesion: 0.11
Nodes (5): KeyService, test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 29 - "validate_measurement"
Cohesion: 0.20
Nodes (12): MeasurementValidationError, validate_measurement(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator(), test_invalid_trusted_identity_is_not_ignored() (+4 more)

### Community 30 - "edge_gateway/config.py"
Cohesion: 0.18
Nodes (14): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+6 more)

### Community 31 - "decode_binary"
Cohesion: 0.17
Nodes (10): decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip() (+2 more)

### Community 32 - "SecureSession"
Cohesion: 0.14
Nodes (4): SecureSession, SessionEstablishmentError, _Sessions, _session()

### Community 33 - "test_gateway_canonical_model.py"
Cohesion: 0.18
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 34 - "test_secure_shutdown.py"
Cohesion: 0.16
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 35 - "test_secure_transport.py"
Cohesion: 0.33
Nodes (15): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+7 more)

### Community 36 - "test_gateway_cloud_secure.py"
Cohesion: 0.20
Nodes (12): CloudHarness, _deliver(), test_a_second_session_rejection_is_not_recovered(), test_ambiguous_transport_retries_the_same_envelope(), test_expired_session_returns_409_and_recovers_once(), test_invalid_session_returns_409_and_recovers_once(), test_local_session_expiry_reestablishes_before_the_next_send(), test_secure_envelope_round_trip_stores_canonical_measurement() (+4 more)

### Community 37 - "Policy"
Cohesion: 0.13
Nodes (8): cloud(), _install(), secure_measurements(), Policy, _reject(), _require_envelope(), SecureRejection, test_production_cloud_app_has_no_secure_measurement_route()

### Community 38 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (12): test_unrelated_record_id_collision_is_not_idempotent_success(), client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail() (+4 more)

### Community 39 - "public_key.py"
Cohesion: 0.17
Nodes (9): CloudPublicKey, parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing() (+1 more)

### Community 40 - "_fixture"
Cohesion: 0.12
Nodes (12): client(), payload(), payload(), database(), measurement(), payload(), cloud(), payload() (+4 more)

### Community 41 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 42 - "test_gateway_validation.py"
Cohesion: 0.24
Nodes (13): parse_legacy_measurement(), assert_rejection(), test_domain_bounds_remain_a_separate_stage(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+5 more)

### Community 43 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.16
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 44 - "routes.py"
Cohesion: 0.20
Nodes (5): _error(), get_measurement(), list_measurements(), baseline_measurement(), _error()

### Community 45 - "test_cloud_baseline.py"
Cohesion: 0.15
Nodes (7): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 46 - "test_security_logging.py"
Cohesion: 0.16
Nodes (5): _Clock, _Cloud, cloud_url(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback(), test_unsafe_log_values_are_dropped()

### Community 47 - "test_cloud_kdf.py"
Cohesion: 0.15
Nodes (4): test_exact_library_parameters(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 49 - "pytest"
Cohesion: 0.18
Nodes (4): test_harness_rejects_invalid_sample_count(), test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 50 - "SessionManager"
Cohesion: 0.21
Nodes (4): clock(), SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run()

### Community 51 - "test_crypto_failures.py"
Cohesion: 0.22
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode(), test_same_seed_makes_the_same_decisions()

### Community 52 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 53 - "test_legacy_values_survive_secure_delivery"
Cohesion: 0.15
Nodes (4): BaselineSpy, test_legacy_values_survive_secure_delivery(), test_secure_failure_does_not_call_baseline(), test_valid_encapsulation_matches_shared_secret_and_hkdf()

### Community 54 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 55 - "validate"
Cohesion: 0.39
Nodes (10): validate(), run(), start(), test_cannot_start_while_active_or_corrupt_state(), test_first_id_slug_and_multiline_prompt(), test_full_acceptance_lifecycle(), test_modified_requires_changes_and_revision_preserves_rounds(), test_rejection_and_second_task() (+2 more)

### Community 57 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 58 - "HistoryError"
Cohesion: 0.29
Nodes (7): main(), parser(), resolve_merge_conflict(), details(), status(), HistoryError, root_from()

### Community 59 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 61 - "_Clock"
Cohesion: 0.25
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 63 - "record_work"
Cohesion: 0.50
Nodes (7): record_work(), recorded_changes(), require_active(), review(), verify(), append(), markdown_list()

### Community 65 - "_seal"
Cohesion: 0.25
Nodes (6): _seal(), test_malformed_mlkem_ciphertext_is_rejected(), test_tampered_secure_message_is_rejected(), test_unsupported_protocol_version_is_rejected(), unreachable(), test_wrong_gateway_ownership_is_rejected_before_decrypt()

### Community 66 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 74 - "_measurement"
Cohesion: 0.33
Nodes (5): _measurement(), test_duplicate_sequence_is_stored_once(), send_twice(), test_one_handshake_is_reused_for_three_measurements(), send_three()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 519 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `load_config`, `SecureTransport`, `secure_transport.py`, `.__init__`, `test_dispatch.py`, `test_security_logging.py`, `SessionManager`, `test_session_recovery_is_counted`, `.__init__`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `decrypt`, `SecureSession`, `test_secure_shutdown.py`, `test_secure_transport.py`, `load_config`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `secure_transport.py`, `test_gateway_cloud_secure.py`, `plaintext.py`, `.shutdown`, `test_dispatch.py`, `CryptoFailureInjector`, `PqcMetrics`, `test_session_recovery_is_counted`, `SessionManager`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `.__init__`, `decode_binary`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `load_config`, `SecureTransport`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `secure_transport.py`, `.__init__`, `SessionManager`, `test_crypto_failures.py`, `test_session_recovery_is_counted`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `SecureTransport` (e.g. with `AadError` and `EncodingError`) actually correct?**
  _`SecureTransport` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `SessionManager` (e.g. with `test_existing_gateway_session_client_over_real_http()` and `CryptoFailureInjector`) actually correct?**
  _`SessionManager` has 20 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `decrypt` be split into smaller, more focused modules?**
  _Cohesion score 0.05581395348837209 - nodes in this community are weakly interconnected._