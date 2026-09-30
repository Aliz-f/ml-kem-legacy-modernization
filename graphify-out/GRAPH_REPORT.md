# Graph Report - ml-kem-legacy-modernization

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1678 nodes · 4065 edges · 95 communities (54 shown, 41 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 533 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- LegacyMeasurement
- decrypt
- FailureMode
- test_session.py
- cli.py
- load_config
- GatewayClient
- test_gateway_cloud_secure.py
- secure_transport.py
- measure_baseline.py
- MeasurementRepository
- SessionManager
- SecureTransport
- test_sensor.py
- test_crypto_failures.py
- SessionManager
- derive_session_key
- cloud_service/app.py
- CanonicalMeasurement
- test_legacy_compatibility.py
- test_secure_message_tamper.py
- PqcMetrics
- SecureSession
- test_dispatch.py
- GatewayErrorCode
- test_secure_shutdown.py
- validate_measurement
- CryptoFailureInjector
- encapsulate
- test_secure_transport.py
- StoredMeasurement
- _accept
- load_config
- create_app
- public_key.py
- test_cloud_kdf.py
- test_cloud_baseline.py
- fetch_public_key
- test_cloud_queries.py
- CloudDispatch
- test_cloud_mlkem.py
- edge_gateway/config.py
- decode_binary
- refresh_graphify.py
- MlKemError
- test_clean_container_crypto.py
- test_cloud_public_key.py
- test_public_key_client.py
- test_gateway_crypto_image.py
- sessions.py
- handshake
- KeyService
- _install
- _HandshakeHandler
- cloud_service/crypto/symmetric.py
- crypto.py
- queries.py
- StartupError
- pytest
- test_repository_hygiene.py
- AadError
- _Handler
- test_refresh_graphify.py
- test_shared_integration_assets.py
- BaselineTransport
- _Handler
- client
- _Handler
- _Handler
- test_gateway_security_components_share_the_metrics_registry_by_default
- KdfError
- .shutdown
- get_config
- _Cloud
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `SecureTransport` - 42 edges
2. `load_config()` - 42 edges
3. `load_config()` - 38 edges
4. `SessionManager` - 37 edges
5. `create_app()` - 37 edges
6. `create_app()` - 36 edges
7. `SecureTransportError` - 33 edges
8. `FailureMode` - 33 edges
9. `MeasurementRepository` - 32 edges
10. `PqcMetrics` - 32 edges

## Surprising Connections (you probably didn't know these)
- `test_device_filter_and_limit_preserve_insertion_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_filter_is_parameterized()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_limits_default_and_maximum_are_applied()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_queries.py → edge_gateway/tests/test_session.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `AadError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/aad.py
- `test_protocol_version_999_is_rejected_before_secure_processing()` --uses--> `SessionEstablishmentError`  [INFERRED]
  tests/integration/test_secure_message_tamper.py → edge_gateway/src/edge_gateway/crypto/session.py

## Import Cycles
- None detected.

## Communities (95 total, 41 thin omitted)

### Community 0 - "LegacyMeasurement"
Cohesion: 0.05
Nodes (50): CanonicalMeasurement, CanonicalMeasurementSchemaError, LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), normalize(), LegacyJSONError, LegacyMeasurementDomainError (+42 more)

### Community 1 - "decrypt"
Cohesion: 0.05
Nodes (52): fields(), test_aad_is_byte_identical(), test_crypto_tampering_rejected(), test_each_modified_aad_field_fails_authentication(), test_gateway_encryption_cloud_decryption(), test_invalid_identifiers(), test_invalid_inputs_before_vendor(), test_unsupported_version() (+44 more)

### Community 2 - "FailureMode"
Cohesion: 0.07
Nodes (46): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+38 more)

### Community 3 - "test_session.py"
Cohesion: 0.06
Nodes (25): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+17 more)

### Community 4 - "cli.py"
Cohesion: 0.14
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 5 - "load_config"
Cohesion: 0.08
Nodes (34): create_app(), health(), ready(), main(), _unavailable(), ConfigurationError, load_config(), integer() (+26 more)

### Community 6 - "GatewayClient"
Cohesion: 0.09
Nodes (20): ErrorCategory, GatewayClient, GatewayResult, FakeResponse, ScriptedOpener, test_default_retry_count_allows_two_retries(), test_http_error_is_classified_without_leaking_exception(), test_http_statuses_are_classified_by_retryability() (+12 more)

### Community 7 - "test_gateway_cloud_secure.py"
Cohesion: 0.08
Nodes (24): BaselineSpy, Clock, CloudHarness, _deliver(), _measurement(), _seal(), test_a_second_session_rejection_is_not_recovered(), test_ambiguous_transport_retries_the_same_envelope() (+16 more)

### Community 9 - "measure_baseline.py"
Cohesion: 0.09
Nodes (19): canonical(), Capture, distribution(), live_cloud(), lifespan(), require(), run(), post() (+11 more)

### Community 10 - "MeasurementRepository"
Cohesion: 0.11
Nodes (24): Database, StorageConflictError, StorageError, MeasurementRepository, test_concurrent_duplicates_across_connections(), save(), database(), measurement() (+16 more)

### Community 11 - "SessionManager"
Cohesion: 0.08
Nodes (8): clock(), _RejectRedirect, log_security(), _token(), SessionEstablishmentError, SessionManager, test_session_missing_and_expired_force_a_new_handshake(), _run()

### Community 12 - "SecureTransport"
Cohesion: 0.11
Nodes (11): SecureEnvelope, _dump(), _endpoint(), _error_code(), _Measurement, _parse_acceptance(), _RetryableTransport, SecureAcceptance (+3 more)

### Community 13 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 14 - "test_crypto_failures.py"
Cohesion: 0.09
Nodes (16): _aad(), _Clock, handshake_url(), _HandshakeCloud, _injector(), measurement_url(), _MeasurementCloud, _plaintext() (+8 more)

### Community 15 - "SessionManager"
Cohesion: 0.11
Nodes (11): SecureSession, SessionAccessError, SessionManager, SessionState, test_clock_failure_never_publishes(), test_invalid_creation_never_publishes(), test_ownership_before_expiry_and_exact_boundary(), test_parallel_sessions_are_distinct_and_independent() (+3 more)

### Community 16 - "derive_session_key"
Cohesion: 0.09
Nodes (14): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+6 more)

### Community 17 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (7): Config, FailureMode, SecurityMode, baseline_measurement(), _error(), test_custom_environment(), test_defaults_do_not_create_database()

### Community 18 - "CanonicalMeasurement"
Cohesion: 0.13
Nodes (12): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected() (+4 more)

### Community 19 - "test_legacy_compatibility.py"
Cohesion: 0.13
Nodes (15): _assert_legacy_post(), _assert_no_crypto_terms(), _exchange(), _fixture(), _Gateway, gateways(), PostedRequest, _recording_opener() (+7 more)

### Community 20 - "test_secure_message_tamper.py"
Cohesion: 0.14
Nodes (13): DecryptSpy, _envelope(), _establish(), _receive(), _reject(), _require_envelope(), SecureRejection, test_authentic_envelope_is_stored_once() (+5 more)

### Community 21 - "PqcMetrics"
Cohesion: 0.09
Nodes (4): _Duration, PqcMetrics, test_metrics_endpoint_exposes_the_same_registry(), test_rendered_metrics_keep_bounded_labels_and_zero_fallback()

### Community 22 - "SecureSession"
Cohesion: 0.12
Nodes (11): _Sessions, SecureSession, _measurement(), test_handshake_and_delivery_omit_secrets_and_separate_timings(), _send(), test_injected_handshake_failure_stays_fail_closed(), test_seal_failure_is_counted_without_the_session_key(), get_or_establish() (+3 more)

### Community 23 - "test_dispatch.py"
Cohesion: 0.18
Nodes (13): _Baseline, cloud(), _config(), _measurement(), _Secure, _Sessions, test_classical_mode_uses_only_the_baseline_transport(), test_encryption_failure_does_not_call_baseline() (+5 more)

### Community 24 - "GatewayErrorCode"
Cohesion: 0.12
Nodes (8): GatewayError, GatewayErrorCode, client(), test_application_errors_have_stable_http_contract(), fail(), test_exception_details_are_not_exposed(), test_internal_failure_outside_measurement_route_is_sanitized(), test_public_error_bodies_are_independent()

### Community 25 - "test_secure_shutdown.py"
Cohesion: 0.13
Nodes (9): _Baseline, _measurement(), _Opener, _Sessions, test_dispatch_after_shutdown_does_not_call_baseline(), test_lifespan_runs_security_cleanup_after_stopping_work(), test_shutdown_closes_the_client_before_clearing_the_session(), test_shutdown_send_fails_closed_without_a_new_handshake() (+1 more)

### Community 26 - "validate_measurement"
Cohesion: 0.18
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 27 - "CryptoFailureInjector"
Cohesion: 0.12
Nodes (3): CryptoFailureInjector, test_enabled_warning_names_the_mode_and_not_the_seed(), test_from_config_uses_gateway_failure_settings()

### Community 28 - "encapsulate"
Cohesion: 0.14
Nodes (12): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+4 more)

### Community 29 - "test_secure_transport.py"
Cohesion: 0.26
Nodes (16): _error(), _send(), _session(), _Sessions, test_a_second_session_conflict_is_not_recovered_again(), test_application_rejection_is_not_retried(), test_exhausted_transport_retries_stay_retryable(), test_invalid_measurement_and_session_failure_do_not_post() (+8 more)

### Community 30 - "StoredMeasurement"
Cohesion: 0.14
Nodes (5): StoredMeasurement, SaveResult, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 31 - "_accept"
Cohesion: 0.13
Nodes (9): _accept(), cloud(), _install(), secure_measurements(), Policy, _reject(), _require_envelope(), SecureRejection (+1 more)

### Community 32 - "load_config"
Cohesion: 0.15
Nodes (12): load_config(), test_cli_uses_configured_server_settings_and_loads_once(), test_config_is_not_reloaded_for_requests(), test_invalid_configuration_prevents_startup(), test_lifecycle_and_health(), test_registered_routes_never_claim_readiness_or_acceptance(), test_responses_and_lifecycle_logs_do_not_expose_configuration(), test_settings_dependency_can_be_overridden_and_isolated() (+4 more)

### Community 33 - "create_app"
Cohesion: 0.18
Nodes (12): create_app(), application_error(), health(), internal_error(), invalid_json(), invalid_measurement(), measurements(), ready() (+4 more)

### Community 34 - "public_key.py"
Cohesion: 0.17
Nodes (10): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, test_invalid_json_is_not_a_transport_retry(), test_oversized_body_is_rejected(), _payload(), _public_key(), test_contract_violations_are_rejected() (+2 more)

### Community 35 - "test_cloud_kdf.py"
Cohesion: 0.13
Nodes (5): test_exact_library_parameters(), test_gateway_cloud_mlkem_and_kdf_interoperability(), test_invalid_secret_rejected_before_hkdf(), test_invalid_vendor_output_rejected(), test_vendor_failures_are_sanitized()

### Community 36 - "test_cloud_baseline.py"
Cohesion: 0.13
Nodes (8): payload(), test_acceptance_is_committed_and_correlated(), test_distinct_logical_identity_creates_second_row(), test_invalid_canonical_data_is_422(), test_malformed_body_is_400_and_not_stored(), test_missing_fields_and_wrong_json_shape(), test_secure_body_never_falls_back_to_baseline(), test_unexpected_repository_error_is_safe_500()

### Community 37 - "fetch_public_key"
Cohesion: 0.17
Nodes (9): _endpoint(), fetch_public_key(), PublicKeyTransportError, _RejectRedirect, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable(), test_http_status_is_classified(), test_redirect_is_not_followed() (+1 more)

### Community 38 - "test_cloud_queries.py"
Cohesion: 0.16
Nodes (9): measurement(), test_closed_storage_is_503_not_empty_or_not_found(), test_device_filter_and_limit_preserve_insertion_order(), test_filter_is_parameterized(), test_invalid_limits_rejected_before_storage(), fail(), test_limits_default_and_maximum_are_applied(), test_missing_repository_is_503() (+1 more)

### Community 39 - "CloudDispatch"
Cohesion: 0.16
Nodes (4): GatewayConfig, CloudDispatch, DispatchMetrics, test_injected_handshake_failure_leaves_no_session_and_skips_baseline()

### Community 40 - "test_cloud_mlkem.py"
Cohesion: 0.15
Nodes (5): test_bad_vendor_secret_rejected(), test_gateway_ciphertext_decapsulates_and_secrets_are_not_logged(), test_key_services_are_independent_and_close_is_idempotent(), test_malformed_ciphertext_rejected(), test_vendor_failures_are_safe()

### Community 41 - "edge_gateway/config.py"
Cohesion: 0.30
Nodes (11): _allowed_value(), ConfigurationError, _failure_rate(), _fixed_session_ttl(), _integer(), _non_negative_int(), _positive_float(), _positive_int() (+3 more)

### Community 42 - "decode_binary"
Cohesion: 0.23
Nodes (9): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding(), _flip(), _different_nonce() (+1 more)

### Community 43 - "refresh_graphify.py"
Cohesion: 0.21
Nodes (5): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_report_date(), _without_section()

### Community 44 - "MlKemError"
Cohesion: 0.18
Nodes (4): decapsulate(), generate_keypair(), MlKemError, PrivateKey

### Community 45 - "test_clean_container_crypto.py"
Cohesion: 0.17
Nodes (3): test_clean_container_image_runs_when_docker_is_available(), test_clean_container_script_stores_one_secure_measurement(), test_verification_image_runs_when_docker_is_available()

### Community 46 - "test_cloud_public_key.py"
Cohesion: 0.27
Nodes (8): secure_app(), test_endpoint_without_lifespan_is_unavailable(), test_exceptional_shutdown_releases_keys_and_storage(), test_key_failure_aborts_startup_and_closes_storage(), fail(), test_public_key_contract_gateway_interop_and_secret_boundary(), test_public_response_failure_is_sanitized(), test_restart_rotates_keys_and_id()

### Community 47 - "test_public_key_client.py"
Cohesion: 0.24
Nodes (6): _body(), cloud_server(), _public_key(), _Response, test_fetch_does_not_encapsulate(), test_fetch_returns_validated_public_key()

### Community 48 - "test_gateway_crypto_image.py"
Cohesion: 0.24
Nodes (4): _install(), _locked_version(), _site_packages(), test_frozen_gateway_install_uses_linux_wheels()

### Community 49 - "sessions.py"
Cohesion: 0.36
Nodes (6): derive_session_key(), _decode_ciphertext(), _error(), _establish(), establish_session(), session_access_error_handler()

### Community 50 - "handshake"
Cohesion: 0.22
Nodes (8): handshake(), test_expiry_http_mapping_and_replacement(), test_extra_field_and_malformed_json(), test_handshake_wire_contract_and_no_secret_leak(), test_missing_fields_or_nonobject(), test_operational_failure_never_leaves_usable_session(), fail(), test_validation_precedes_crypto()

### Community 53 - "_install"
Cohesion: 0.22
Nodes (5): _install(), secure_measurements(), main(), _rejected(), _serve()

### Community 58 - "queries.py"
Cohesion: 0.46
Nodes (3): _error(), get_measurement(), list_measurements()

### Community 59 - "StartupError"
Cohesion: 0.29
Nodes (3): lifespan(), StartupError, test_session_initialization_failure_releases_keys()

### Community 66 - "test_refresh_graphify.py"
Cohesion: 0.47
Nodes (3): test_clear_incremental_state_removes_all_prior_graphify_output(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 557 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PqcMetrics` connect `PqcMetrics` to `create_app`, `CloudDispatch`, `secure_transport.py`, `SessionManager`, `SecureTransport`, `SecureSession`, `CryptoFailureInjector`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `SessionManager` connect `SessionManager` to `public_key.py`, `test_session.py`, `load_config`, `fetch_public_key`, `CloudDispatch`, `secure_transport.py`, `test_gateway_cloud_secure.py`, `test_gateway_security_components_share_the_metrics_registry_by_default`, `test_crypto_failures.py`, `derive_session_key`, `test_secure_message_tamper.py`, `_install`, `PqcMetrics`, `SecureSession`, `CryptoFailureInjector`, `encapsulate`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `CryptoFailureInjector` connect `CryptoFailureInjector` to `CloudDispatch`, `secure_transport.py`, `SessionManager`, `SecureTransport`, `test_crypto_failures.py`, `SecureSession`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `SecureTransport` (e.g. with `main()` and `AadError`) actually correct?**
  _`SecureTransport` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `SessionManager` (e.g. with `test_existing_gateway_session_client_over_real_http()` and `main()`) actually correct?**
  _`SessionManager` has 21 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `LegacyMeasurement` be split into smaller, more focused modules?**
  _Cohesion score 0.050187265917602995 - nodes in this community are weakly interconnected._