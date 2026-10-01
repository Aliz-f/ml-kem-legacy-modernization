# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2010 nodes · 5021 edges · 93 communities (67 shown, 26 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 725 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FailureMode
- test_device.py
- create_app
- test_legacy_compatibility.py
- test_gateway_cloud_secure.py
- test_session.py
- GatewayErrorCode
- secure_transport.py
- test_crypto_failures.py
- test_baseline_client.py
- GatewayClient
- cli.py
- MeasurementRepository
- SecureTransport
- test_public_key_client.py
- test_security_logging.py
- pathlib
- CloudDispatch
- cloud_service/app.py
- create_app
- load_config
- edge_gateway/crypto/symmetric.py
- PqcMetrics
- CanonicalMeasurement
- test_cloud_secure.py
- LegacyMeasurement
- encapsulate
- SessionManager
- test_cloud_session_api.py
- datetime
- secure.py
- SecureEnvelope
- CryptoFailureInjector
- test_secure_transport.py
- test_secure_message_tamper.py
- measure_baseline.py
- validate_measurement
- encode_binary
- test_gateway_crypto_image.py
- FailureMode
- derive_session_key
- test_cloud_failure_injection.py
- CanonicalMeasurement
- test_secure_shutdown.py
- validate_legacy_measurement
- cloud_service/crypto/mlkem.py
- refresh_graphify.py
- decode_binary
- fields
- test_cloud_baseline.py
- test_cloud_queries.py
- plaintext.py
- test_gateway_validation.py
- test_cloud_kdf.py
- build_aad
- pytest
- parse_public_key_response
- SessionState
- SessionManager
- sessions.py
- test_cloud_mlkem.py
- test_cloud_public_key.py
- edge_gateway/validation.py
- validate
- envelope_validation.py
- test_secure_envelope.py
- keys.py
- _Clock
- cloud_service/crypto/session.py
- main
- test_refresh_graphify.py
- _Cloud
- test_repository_hygiene.py
- _Handler
- _DroppedResponse
- edge_gateway/models.py
- _Handler
- KdfError
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `create_app()` - 52 edges
2. `load_config()` - 48 edges
3. `load_config()` - 47 edges
4. `SecureTransport` - 44 edges
5. `FailureMode` - 44 edges
6. `create_app()` - 42 edges
7. `SessionManager` - 37 edges
8. `SecureTransportError` - 36 edges
9. `FailureMode` - 35 edges
10. `FailureInjector` - 34 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `settings()` --indirect_call--> `config()`  [INFERRED]
  edge_gateway/tests/test_gateway_app.py → cloud_service/tests/test_cloud_failure_injection.py
- `_send()` --uses--> `GatewayClient`  [INFERRED]
  tests/integration/test_legacy_compatibility.py → legacy_system/src/legacy_system/client.py

## Import Cycles
- None detected.

## Communities (93 total, 26 thin omitted)

### Community 0 - "FailureMode"
Cohesion: 0.06
Nodes (53): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+45 more)

### Community 1 - "test_device.py"
Cohesion: 0.05
Nodes (29): DeviceController, FakeMeasurement, FakeResponse, FakeSensor, FalseyClient, FalseyEvent, FalseyFailureInjector, FalseySensor (+21 more)

### Community 2 - "create_app"
Cohesion: 0.06
Nodes (48): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), ready(), _error_response() (+40 more)

### Community 3 - "test_legacy_compatibility.py"
Cohesion: 0.05
Nodes (33): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+25 more)

### Community 4 - "test_gateway_cloud_secure.py"
Cohesion: 0.05
Nodes (32): BaselineSpy, Clock, cloud(), CloudHarness, _deliver(), _flip(), _install_trace(), _measurement() (+24 more)

### Community 5 - "test_session.py"
Cohesion: 0.06
Nodes (25): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+17 more)

### Community 6 - "GatewayErrorCode"
Cohesion: 0.07
Nodes (21): GatewayError, GatewayErrorCode, MeasurementProcessor, UnavailableBaseline, SequenceTracker, client(), test_application_errors_have_stable_http_contract(), fail() (+13 more)

### Community 7 - "secure_transport.py"
Cohesion: 0.08
Nodes (8): _baseline_transport(), get_config(), GatewayConfig, baseline_headers(), corrupt_ciphertext_copy(), _error_code(), _token(), BaselineTransport

### Community 8 - "test_crypto_failures.py"
Cohesion: 0.06
Nodes (22): clock(), _aad(), _Clock, handshake_url(), _HandshakeCloud, _HandshakeHandler, _injector(), measurement_url() (+14 more)

### Community 9 - "test_baseline_client.py"
Cohesion: 0.09
Nodes (25): BaselineAcceptance, BaselineCloudClient, BaselineCloudError, _dump(), _endpoint(), _error_code(), _parse_acceptance(), _RejectRedirect (+17 more)

### Community 10 - "GatewayClient"
Cohesion: 0.10
Nodes (21): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+13 more)

### Community 11 - "cli.py"
Cohesion: 0.18
Nodes (30): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+22 more)

### Community 12 - "MeasurementRepository"
Cohesion: 0.10
Nodes (26): lifespan(), StartupError, Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save() (+18 more)

### Community 13 - "SecureTransport"
Cohesion: 0.10
Nodes (12): SecureEnvelope, _dump(), _endpoint(), _Measurement, _parse_acceptance(), _RejectRedirect, _RetryableTransport, SecureAcceptance (+4 more)

### Community 14 - "test_public_key_client.py"
Cohesion: 0.09
Nodes (19): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, CloudPublicKey, PublicKeyRejected, _body(), cloud_server() (+11 more)

### Community 15 - "test_security_logging.py"
Cohesion: 0.08
Nodes (15): _Sessions, SecureSession, _Baseline, _measurement(), test_gateway_security_components_share_the_metrics_registry_by_default(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed() (+7 more)

### Community 17 - "CloudDispatch"
Cohesion: 0.13
Nodes (15): CloudDispatch, _Baseline, cloud(), _config(), _Handler, _measurement(), _Secure, _Sessions (+7 more)

### Community 18 - "cloud_service/app.py"
Cohesion: 0.11
Nodes (7): public_key(), _unavailable(), _error(), get_measurement(), list_measurements(), baseline_measurement(), _error()

### Community 19 - "create_app"
Cohesion: 0.09
Nodes (18): create_app(), health(), ready(), main(), _unavailable(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+10 more)

### Community 20 - "load_config"
Cohesion: 0.14
Nodes (17): Config, ConfigurationError, load_config(), integer(), number(), text(), value(), SecurityMode (+9 more)

### Community 21 - "edge_gateway/crypto/symmetric.py"
Cohesion: 0.20
Nodes (18): main(), AeadError, decrypt(), encrypt(), _require_bytes(), _require_key(), _require_nonce(), _aad() (+10 more)

### Community 22 - "PqcMetrics"
Cohesion: 0.08
Nodes (3): _Duration, PqcMetrics, DispatchMetrics

### Community 23 - "CanonicalMeasurement"
Cohesion: 0.14
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 24 - "test_cloud_secure.py"
Cohesion: 0.18
Nodes (24): canonical(), envelope(), establish(), forbid(), test_authenticated_invalid_measurement_is_not_stored(), test_authentication_failure_never_parses_or_stores(), test_classical_accepts_only_baseline_and_secure_unavailable(), test_correctly_padded_base64url_is_accepted() (+16 more)

### Community 25 - "LegacyMeasurement"
Cohesion: 0.19
Nodes (15): LegacyMeasurement, LegacyMeasurementSchemaError, payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required(), test_error_does_not_echo_payload_values() (+7 more)

### Community 26 - "encapsulate"
Cohesion: 0.13
Nodes (12): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+4 more)

### Community 27 - "SessionManager"
Cohesion: 0.11
Nodes (3): lifespan(), SessionEstablishmentError, SessionManager

### Community 28 - "test_cloud_session_api.py"
Cohesion: 0.12
Nodes (12): client(), handshake(), test_existing_gateway_session_client_over_real_http(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session() (+4 more)

### Community 29 - "datetime"
Cohesion: 0.13
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 30 - "secure.py"
Cohesion: 0.14
Nodes (8): AadError, build_aad(), AeadError, decrypt(), _error(), _ingest(), secure_measurement(), fail()

### Community 31 - "SecureEnvelope"
Cohesion: 0.17
Nodes (10): EnvelopeSchemaError, SecureEnvelope, payload(), test_exact_fields_immutable_and_independent_dictionary(), test_existing_gateway_builder_wire_round_trip(), test_extra_fields_rejected_without_echo(), test_missing_field_rejected(), test_model_preserves_strings_without_claiming_security_validation() (+2 more)

### Community 32 - "CryptoFailureInjector"
Cohesion: 0.11
Nodes (3): CryptoFailureInjector, test_from_config_uses_gateway_failure_settings(), test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 33 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (17): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+9 more)

### Community 34 - "test_secure_message_tamper.py"
Cohesion: 0.17
Nodes (11): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+3 more)

### Community 35 - "measure_baseline.py"
Cohesion: 0.13
Nodes (9): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+1 more)

### Community 36 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 37 - "encode_binary"
Cohesion: 0.16
Nodes (9): decode_binary(), encode_binary(), EncodingError, build_secure_envelope(), test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _different_nonce() (+1 more)

### Community 38 - "test_gateway_crypto_image.py"
Cohesion: 0.12
Nodes (7): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels(), test_verification_image_runs_when_docker_is_available()

### Community 39 - "FailureMode"
Cohesion: 0.16
Nodes (7): FailureMode, FailureInjector, FailureSelection, test_enabled_injection_logs_safe_warning(), test_random_rate_one_selects_one_applicable_fault_for_request(), test_random_rate_zero_never_injects(), test_random_seed_is_reproducible_and_selects_only_allowed_modes()

### Community 40 - "derive_session_key"
Cohesion: 0.15
Nodes (9): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+1 more)

### Community 41 - "test_cloud_failure_injection.py"
Cohesion: 0.21
Nodes (16): canonical(), config(), envelope(), handshake(), secure_client(), test_decryption_failure_prevents_plaintext_and_storage(), test_drop_response_commits_then_same_envelope_retries_idempotently(), test_injected_session_failures_are_frozen_409s() (+8 more)

### Community 42 - "CanonicalMeasurement"
Cohesion: 0.17
Nodes (11): CanonicalMeasurement, CanonicalMeasurementSchemaError, test_all_fields_are_required(), test_exact_protocol_fields_and_json_serialization(), test_internal_error_does_not_echo_supplied_values(), test_invalid_types_are_not_coerced(), test_noncanonical_fields_cannot_be_added(), test_nonfinite_or_unrepresentable_numbers_are_rejected() (+3 more)

### Community 43 - "test_secure_shutdown.py"
Cohesion: 0.15
Nodes (8): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake(), _transport()

### Community 44 - "validate_legacy_measurement"
Cohesion: 0.15
Nodes (8): measurements(), normalize(), validate_legacy_measurement(), canonical(), test_invalid_receipt_time_is_rejected_by_canonical_model(), test_normalization_preserves_values_and_input(), test_parsed_measurement_normalizes_to_exact_canonical_wire_contract(), test_legacy_values_survive_secure_delivery()

### Community 45 - "cloud_service/crypto/mlkem.py"
Cohesion: 0.14
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 46 - "refresh_graphify.py"
Cohesion: 0.14
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 47 - "decode_binary"
Cohesion: 0.22
Nodes (7): decode_binary(), encode_binary(), EncodingError, test_binary_round_trip_padded_and_unpadded(), test_encoding_requires_nonempty_bytes(), test_invalid_encoding_rejected_without_echo(), test_urlsafe_alphabet()

### Community 48 - "fields"
Cohesion: 0.22
Nodes (11): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+3 more)

### Community 49 - "test_cloud_baseline.py"
Cohesion: 0.14
Nodes (8): test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500(), test_unrelated_record_id_collision_is_not_idempotent_success()

### Community 50 - "test_cloud_queries.py"
Cohesion: 0.15
Nodes (10): client(), measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied() (+2 more)

### Community 51 - "plaintext.py"
Cohesion: 0.22
Nodes (10): PlaintextError, _require_id(), _require_number(), _require_sequence(), _require_utc_timestamp(), serialize_canonical_measurement(), _measurement(), test_explicit_utc_offsets_are_preserved() (+2 more)

### Community 52 - "test_gateway_validation.py"
Cohesion: 0.23
Nodes (12): assert_rejection(), client(), payload(), test_domain_invalid_values_are_422_before_cloud(), test_domain_timestamp_contract_is_enforced_by_model(), test_domain_valid_values_are_preserved(), test_extra_field_is_422(), test_malformed_json_is_400() (+4 more)

### Community 53 - "test_cloud_kdf.py"
Cohesion: 0.14
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 54 - "build_aad"
Cohesion: 0.22
Nodes (7): AadError, build_aad(), _require_id(), _independent(), test_each_authenticated_field_changes_the_aad_bytes(), test_gateway_and_independent_aad_bytes_match_the_contract(), test_invalid_aad_fields_are_rejected()

### Community 55 - "pytest"
Cohesion: 0.18
Nodes (6): test_harness_rejects_invalid_sample_count(), create_request_id(), test_baseline_request_carries_id_in_header_and_keeps_body_unchanged(), test_existing_secure_envelope_authenticates_same_request_context(), test_gateway_logs_generated_id_without_measurement_data(), test_independent_requests_get_distinct_uuid4_ids()

### Community 56 - "parse_public_key_response"
Cohesion: 0.22
Nodes (8): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key(), test_protocol_version_999_is_rejected_before_secure_processing(), reject_public_key()

### Community 57 - "SessionState"
Cohesion: 0.19
Nodes (8): SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent(), test_production_ttl_is_fixed(), test_remove_expired_and_shutdown(), test_unknown_wrong_owner_and_invalidation()

### Community 59 - "sessions.py"
Cohesion: 0.32
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 60 - "test_cloud_mlkem.py"
Cohesion: 0.20
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 61 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 62 - "edge_gateway/validation.py"
Cohesion: 0.21
Nodes (6): LegacyJSONError, LegacyMeasurementDomainError, parse_legacy_measurement(), _reject_constant(), test_domain_bounds_remain_a_separate_stage(), test_valid_measurement_parses_but_is_not_accepted_before_delivery()

### Community 63 - "validate"
Cohesion: 0.39
Nodes (10): validate(), run(), start(), test_cannot_start_while_active_or_corrupt_state(), test_first_id_slug_and_multiline_prompt(), test_full_acceptance_lifecycle(), test_modified_requires_changes_and_revision_preserves_rounds(), test_rejection_and_second_task() (+2 more)

### Community 64 - "envelope_validation.py"
Cohesion: 0.27
Nodes (6): _constant(), EnvelopeValidationError, _object(), parse_json(), validate_envelope(), ValidatedEnvelope

### Community 65 - "test_secure_envelope.py"
Cohesion: 0.35
Nodes (8): _build(), _key(), test_each_logical_message_gets_a_new_nonce_and_keeps_the_request_id(), test_envelope_does_not_log_the_key_or_plaintext(), test_envelope_has_exactly_the_protocol_fields(), test_invalid_measurement_identity_and_key_build_no_envelope(), test_nonce_is_12_bytes_and_ciphertext_decrypts_to_the_measurement(), test_plaintext_measurement_does_not_appear_in_the_envelope()

### Community 67 - "_Clock"
Cohesion: 0.22
Nodes (3): _Clock, _Cloud, cloud_url()

### Community 69 - "main"
Cohesion: 0.29
Nodes (3): _install(), main(), _serve()

### Community 70 - "test_refresh_graphify.py"
Cohesion: 0.36
Nodes (4): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed(), test_report_is_identical_across_local_and_ci_dates()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 663 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SecureTransport` connect `SecureTransport` to `CryptoFailureInjector`, `test_secure_transport.py`, `create_app`, `test_gateway_cloud_secure.py`, `encode_binary`, `main`, `secure_transport.py`, `test_crypto_failures.py`, `test_secure_shutdown.py`, `test_security_logging.py`, `CloudDispatch`, `plaintext.py`, `edge_gateway/crypto/symmetric.py`, `build_aad`, `PqcMetrics`, `SessionManager`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `create_app()` connect `create_app` to `keys.py`, `measure_baseline.py`, `cloud_service/crypto/session.py`, `main`, `test_gateway_cloud_secure.py`, `test_cloud_failure_injection.py`, `MeasurementRepository`, `cloud_service/app.py`, `test_cloud_queries.py`, `load_config`, `test_cloud_secure.py`, `SessionManager`, `sessions.py`, `test_cloud_session_api.py`, `test_cloud_public_key.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `DeviceController` connect `test_device.py` to `FailureMode`, `GatewayClient`, `test_legacy_compatibility.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `GatewayConfig`) actually correct?**
  _`create_app()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FailureMode` be split into smaller, more focused modules?**
  _Cohesion score 0.055900621118012424 - nodes in this community are weakly interconnected._
- **Should `test_device.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._