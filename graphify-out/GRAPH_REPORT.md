# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2119 nodes · 5256 edges · 111 communities (74 shown, 37 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 747 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- pytest
- test_secure_message_tamper.py
- test_gateway_cloud_secure.py
- test_legacy_compatibility.py
- cli.py
- LegacyMeasurement
- test_baseline_client.py
- GatewayClient
- edge_gateway/app.py
- FailureMode
- GatewayErrorCode
- load_config
- pathlib
- MeasurementRepository
- test_gateway_crypto_image.py
- test_gateway_validation.py
- create_app
- test_cloud_mlkem.py
- make_config
- cloud_service/app.py
- test_session.py
- FailureMode
- test_cloud_secure.py
- secure_transport.py
- test_public_key_client.py
- test_dispatch.py
- CanonicalMeasurement
- measure_baseline.py
- SessionManager
- secure.py
- PqcMetrics
- load_config
- test_mode_evaluation.py
- test_security_logging.py
- test_device.py
- SecureTransport
- edge_gateway/crypto/session.py
- SecureEnvelope
- test_cloud_failure_injection.py
- encapsulate
- validate_measurement
- public_key.py
- load_config
- StoredMeasurement
- encode_binary
- derive_session_key
- CloudMetrics
- test_cloud_baseline.py
- test_gateway_measurements.py
- test_secure_transport.py
- test_full_path_integration.py
- test_cloud_queries.py
- plaintext.py
- DeviceController
- test_cloud_session_api.py
- edge_gateway/crypto/encoding.py
- Config
- test_cloud_public_key.py
- CryptoFailureInjector
- test_session_recovery_is_counted
- test_crypto_failures.py
- normalize
- test_gateway_errors.py
- _Sessions
- test_secure_shutdown.py
- envelope_validation.py
- clean_container_crypto.py
- .__init__
- test_corrupt_ciphertext_mutates_only_the_outgoing_copy
- _Clock
- _HandshakeHandler
- queries.py
- _DroppedResponse
- KdfError
- test_refresh_graphify.py
- StartupError
- FakeResponse
- test_repository_hygiene.py
- test_injected_handshake_failure_leaves_no_session_and_skips_baseline
- _Handler
- _Handler
- test_client_exception_is_logged_then_loop_continues_and_closes
- KeyService
- public_key
- baseline_measurement
- .shutdown
- test_session_missing_and_expired_force_a_new_handshake
- _Handler
- _Handler
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 53 edges
2. `load_config()` - 50 edges
3. `load_config()` - 48 edges
4. `create_app()` - 48 edges
5. `FailureMode` - 46 edges
6. `SecureTransport` - 46 edges
7. `SessionManager` - 40 edges
8. `SecureTransportError` - 38 edges
9. `FailureMode` - 35 edges
10. `CloudHarness` - 34 edges

## Surprising Connections (you probably didn't know these)
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/aad.py

## Import Cycles
- None detected.

## Communities (111 total, 37 thin omitted)

### Community 0 - "pytest"
Cohesion: 0.05
Nodes (50): test_harness_rejects_invalid_sample_count(), fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor() (+42 more)

### Community 1 - "test_secure_message_tamper.py"
Cohesion: 0.05
Nodes (27): decapsulate(), generate_keypair(), MlKemError, PrivateKey, SecureSession, SessionAccessError, SessionManager, SessionState (+19 more)

### Community 2 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (33): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+25 more)

### Community 3 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (33): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+25 more)

### Community 4 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 5 - "LegacyMeasurement"
Cohesion: 0.09
Nodes (27): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values() (+19 more)

### Community 6 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (25): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+17 more)

### Community 7 - "GatewayClient"
Cohesion: 0.09
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 8 - "edge_gateway/app.py"
Cohesion: 0.08
Nodes (19): _baseline_transport(), create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready() (+11 more)

### Community 9 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 10 - "GatewayErrorCode"
Cohesion: 0.10
Nodes (14): GatewayError, GatewayErrorCode, UnavailableBaseline, SequenceTracker, test_committed_sequence_survives_later_cloud_failure(), test_concurrent_different_sequences_leave_highest_accepted_state(), test_concurrent_same_sequence_is_accepted_only_once(), submit() (+6 more)

### Community 11 - "load_config"
Cohesion: 0.10
Nodes (27): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), load_config(), _non_negative_int(), _positive_float() (+19 more)

### Community 12 - "pathlib"
Cohesion: 0.05
Nodes (3): test_quality_workflow_names_the_gateway_crypto_suites(), _fixture(), test_shared_fixtures_match_the_frozen_legacy_and_canonical_shapes()

### Community 13 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 14 - "test_gateway_crypto_image.py"
Cohesion: 0.08
Nodes (11): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version() (+3 more)

### Community 15 - "test_gateway_validation.py"
Cohesion: 0.10
Nodes (21): measurements(), LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), validate_legacy_measurement(), assert_rejection(), client() (+13 more)

### Community 16 - "create_app"
Cohesion: 0.09
Nodes (20): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+12 more)

### Community 17 - "test_cloud_mlkem.py"
Cohesion: 0.08
Nodes (10): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized(), test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent() (+2 more)

### Community 18 - "make_config"
Cohesion: 0.11
Nodes (14): FakeSensor, make_config(), RecordingClient, test_permanent_gateway_failures_are_logged_without_retry(), test_retry_and_final_failure_logging_are_visible(), test_retry_eventual_success_logs_delivery_without_final_failure(), test_runtime_logs_lifecycle_and_delivery_events(), stop_after_first_measurement() (+6 more)

### Community 19 - "cloud_service/app.py"
Cohesion: 0.14
Nodes (8): _crypto_dependencies_ready(), SecurityMode, derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 20 - "test_session.py"
Cohesion: 0.11
Nodes (14): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_refuses_a_later_handshake(), test_close_wipes_the_session_key() (+6 more)

### Community 21 - "FailureMode"
Cohesion: 0.12
Nodes (10): Config, FailureMode, FailureInjector, FailureSelection, test_custom_environment(), test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects() (+2 more)

### Community 22 - "test_cloud_secure.py"
Cohesion: 0.17
Nodes (24): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+16 more)

### Community 23 - "secure_transport.py"
Cohesion: 0.11
Nodes (7): build_secure_envelope(), SecureEnvelope, corrupt_ciphertext_copy(), _dump(), _error_code(), _RejectRedirect, _token()

### Community 24 - "test_public_key_client.py"
Cohesion: 0.13
Nodes (15): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, _body(), _public_key(), test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable() (+7 more)

### Community 25 - "test_dispatch.py"
Cohesion: 0.15
Nodes (14): _Baseline, cloud(), _config(), _Handler, _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport() (+6 more)

### Community 26 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 27 - "measure_baseline.py"
Cohesion: 0.12
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 28 - "SessionManager"
Cohesion: 0.11
Nodes (5): SecureSession, SessionEstablishmentError, SessionManager, _session(), get_or_establish()

### Community 29 - "secure.py"
Cohesion: 0.12
Nodes (9): AadError, build_aad(), AeadError, decrypt(), _error(), _ingest(), _NoMetrics, secure_measurement() (+1 more)

### Community 31 - "load_config"
Cohesion: 0.18
Nodes (19): ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration(), test_empty_device_id() (+11 more)

### Community 32 - "test_mode_evaluation.py"
Cohesion: 0.13
Nodes (10): _Baseline, _Calls, _dispatch(), measure_modes(), _serve(), _Server, _Sizes, test_equivalent_workload_keeps_the_modes_separate() (+2 more)

### Community 33 - "test_security_logging.py"
Cohesion: 0.12
Nodes (12): _Baseline, _Clock, _Cloud, cloud_url(), _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send() (+4 more)

### Community 34 - "test_device.py"
Cohesion: 0.12
Nodes (8): FakeMeasurement, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor, RecordingFailureInjector, test_delivery_failure_does_not_stop_loop_or_roll_back_sequence(), test_falsey_injected_dependencies_are_preserved()

### Community 35 - "SecureTransport"
Cohesion: 0.19
Nodes (6): _Measurement, _parse_acceptance(), SecureAcceptance, SecureTransport, SecureTransportError, log_security()

### Community 36 - "edge_gateway/crypto/session.py"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 37 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 38 - "test_cloud_failure_injection.py"
Cohesion: 0.19
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 39 - "encapsulate"
Cohesion: 0.15
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 40 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 41 - "public_key.py"
Cohesion: 0.15
Nodes (10): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key() (+2 more)

### Community 42 - "load_config"
Cohesion: 0.20
Nodes (15): ConfigurationError, load_config(), integer(), number(), text(), value(), test_unrelated_record_id_collision_is_not_idempotent_success(), test_defaults_do_not_create_database() (+7 more)

### Community 43 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 44 - "encode_binary"
Cohesion: 0.18
Nodes (8): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet(), test_published_public_key_round_trip_and_handshake()

### Community 45 - "derive_session_key"
Cohesion: 0.15
Nodes (8): KdfError, derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 46 - "CloudMetrics"
Cohesion: 0.12
Nodes (5): CloudMetrics, _labels(), _render_labels(), test_baseline_metrics_count_requests_storage_and_idempotent_duplicates(), test_metrics_reject_unbounded_or_unsupported_labels()

### Community 47 - "test_cloud_baseline.py"
Cohesion: 0.12
Nodes (9): client(), payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline() (+1 more)

### Community 48 - "test_gateway_measurements.py"
Cohesion: 0.17
Nodes (12): test_failed_delivery_returns_503_and_retains_sequence(), test_internal_failure_returns_safe_500_and_does_not_rollback(), test_invalid_input_has_no_sequence_hook_or_delivery_effect(), test_pending_delivery_does_not_return_success_or_hold_sequence_lock(), scenario(), test_secure_unavailability_never_calls_baseline(), test_selected_transport_receives_canonical_values_and_separate_id(), hook() (+4 more)

### Community 49 - "test_secure_transport.py"
Cohesion: 0.32
Nodes (16): _error(), _send(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post(), test_keys_and_plaintext_are_not_logged() (+8 more)

### Community 50 - "test_full_path_integration.py"
Cohesion: 0.17
Nodes (3): _serve(), test_cloud_runtime_only_accepts_gateway_canonical_fields(), test_legacy_gateway_cloud_http_path_persists_canonical_measurement()

### Community 51 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 52 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 54 - "test_cloud_session_api.py"
Cohesion: 0.20
Nodes (9): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_synthetic_secret_markers_never_appear_in_cloud_logs() (+1 more)

### Community 55 - "edge_gateway/crypto/encoding.py"
Cohesion: 0.23
Nodes (8): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _different_nonce(), _tamper()

### Community 56 - "Config"
Cohesion: 0.21
Nodes (8): Config, main(), make_config(), RecordingController, test_main_loads_configuration_and_runs_controller(), factory(), test_main_logs_invalid_configuration_and_returns_nonzero(), invalid_config()

### Community 57 - "test_cloud_public_key.py"
Cohesion: 0.22
Nodes (9): secure_app(), test_classical_does_not_generate_keys(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized() (+1 more)

### Community 59 - "test_session_recovery_is_counted"
Cohesion: 0.14
Nodes (3): _Sessions, test_session_recovery_is_counted(), get_or_establish()

### Community 60 - "test_crypto_failures.py"
Cohesion: 0.20
Nodes (8): _injector(), measurement_url(), _MeasurementCloud, test_disabled_injection_reuses_one_handshake(), test_disabled_modes_never_select_a_crypto_fault(), test_invalid_failure_rate_is_rejected(), test_rate_one_selects_only_the_configured_mode(), test_same_seed_makes_the_same_decisions()

### Community 61 - "normalize"
Cohesion: 0.22
Nodes (5): normalize(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract()

### Community 62 - "test_gateway_errors.py"
Cohesion: 0.21
Nodes (6): client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 63 - "_Sessions"
Cohesion: 0.18
Nodes (4): _Opener, _Sessions, test_shutdown_closes_the_client_before_clearing_the_session(), _transport()

### Community 64 - "test_secure_shutdown.py"
Cohesion: 0.24
Nodes (4): _Baseline, _measurement(), test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_send_fails_closed_without_a_new_handshake()

### Community 65 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 66 - "clean_container_crypto.py"
Cohesion: 0.25
Nodes (3): _install(), main(), _serve()

### Community 67 - ".__init__"
Cohesion: 0.18
Nodes (3): _endpoint(), _RetryableTransport, _SessionRecovery

### Community 68 - "test_corrupt_ciphertext_mutates_only_the_outgoing_copy"
Cohesion: 0.24
Nodes (5): _aad(), _plaintext(), _Sessions, test_corrupt_ciphertext_mutates_only_the_outgoing_copy(), test_disabled_ciphertext_injection_still_authenticates()

### Community 69 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, handshake_url(), _HandshakeCloud

### Community 71 - "queries.py"
Cohesion: 0.46
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 72 - "_DroppedResponse"
Cohesion: 0.25
Nodes (3): _DroppedResponse, cloud_server(), _Response

### Community 73 - "KdfError"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 74 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

### Community 75 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 82 - "test_client_exception_is_logged_then_loop_continues_and_closes"
Cohesion: 0.33
Nodes (4): RaisingClient, test_client_exception_is_logged_then_loop_continues_and_closes(), test_stop_during_delivery_skips_interval_wait(), send()

### Community 93 - "test_session_missing_and_expired_force_a_new_handshake"
Cohesion: 0.50
Nodes (3): clock(), test_session_missing_and_expired_force_a_new_handshake(), _run()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 722 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FailureMode` connect `FailureMode` to `test_gateway_cloud_secure.py`, `test_cloud_failure_injection.py`, `load_config`, `cloud_service/app.py`, `public_key`, `baseline_measurement`, `secure.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `SecureTransport` connect `SecureTransport` to `pytest`, `test_gateway_cloud_secure.py`, `edge_gateway/app.py`, `secure_transport.py`, `test_dispatch.py`, `SessionManager`, `PqcMetrics`, `test_mode_evaluation.py`, `test_security_logging.py`, `test_secure_transport.py`, `plaintext.py`, `edge_gateway/crypto/encoding.py`, `CryptoFailureInjector`, `test_session_recovery_is_counted`, `_Sessions`, `clean_container_crypto.py`, `.__init__`, `test_corrupt_ciphertext_mutates_only_the_outgoing_copy`, `test_injected_handshake_failure_leaves_no_session_and_skips_baseline`, `.shutdown`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `PqcMetrics` connect `PqcMetrics` to `test_mode_evaluation.py`, `test_security_logging.py`, `.__init__`, `SecureTransport`, `edge_gateway/crypto/session.py`, `edge_gateway/app.py`, `load_config`, `.__init__`, `secure_transport.py`, `test_session_recovery_is_counted`, `SessionManager`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `pytest` be split into smaller, more focused modules?**
  _Cohesion score 0.054136874361593465 - nodes in this community are weakly interconnected._
- **Should `test_secure_message_tamper.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05242566510172144 - nodes in this community are weakly interconnected._