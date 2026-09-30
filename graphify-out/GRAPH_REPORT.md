# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 775 nodes · 1794 edges · 47 communities (24 shown, 23 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 231 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_symmetric.py
- cli.py
- load_config
- CanonicalMeasurement
- FailureMode
- test_sensor.py
- test_gateway_models.py
- load_config
- load_config
- create_app
- test_session.py
- cloud_service/app.py
- SessionManager
- session_client.py
- MlKemError
- json
- test_cloud_storage.py
- test_kdf.py
- fetch_public_key
- public_key.py
- encoding.py
- test_public_key_client.py
- StoredMeasurement
- test_crypto_failure_is_classified_and_recorded
- public_key_client.py
- _Handler
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `FailureMode` - 33 edges
2. `load_config()` - 33 edges
3. `FailureInjector` - 31 edges
4. `MeasurementRepository` - 25 edges
5. `load_config()` - 25 edges
6. `load_config()` - 23 edges
7. `create_app()` - 23 edges
8. `CanonicalMeasurement` - 22 edges
9. `SessionManager` - 19 edges
10. `create_app()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `test_concurrent_repository_access()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_database_uniqueness_is_a_conflict_not_idempotent_success()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_invalid_metadata_and_domain_are_rejected()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_list_limit_filter_and_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_parameterized_identifiers()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py

## Import Cycles
- None detected.

## Communities (47 total, 23 thin omitted)

### Community 0 - "test_symmetric.py"
Cohesion: 0.06
Nodes (46): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number() (+38 more)

### Community 1 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 2 - "load_config"
Cohesion: 0.08
Nodes (32): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+24 more)

### Community 3 - "CanonicalMeasurement"
Cohesion: 0.08
Nodes (25): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), MeasurementValidationError, validate_measurement(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps() (+17 more)

### Community 4 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 5 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 6 - "test_gateway_models.py"
Cohesion: 0.15
Nodes (16): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required() (+8 more)

### Community 7 - "load_config"
Cohesion: 0.14
Nodes (18): Config, ConfigurationError, FailureMode, load_config(), integer(), number(), text(), value() (+10 more)

### Community 8 - "load_config"
Cohesion: 0.15
Nodes (20): Config, ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration() (+12 more)

### Community 9 - "create_app"
Cohesion: 0.11
Nodes (18): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), test_apps_have_independent_lifecycle_state() (+10 more)

### Community 10 - "test_session.py"
Cohesion: 0.11
Nodes (12): SessionState, _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake() (+4 more)

### Community 11 - "cloud_service/app.py"
Cohesion: 0.12
Nodes (6): Database, StorageConflictError, StorageError, database(), test_missing_parent_and_invalid_file_errors_are_safe(), test_relative_path()

### Community 12 - "SessionManager"
Cohesion: 0.12
Nodes (3): SecureSession, SessionEstablishmentError, SessionManager

### Community 13 - "session_client.py"
Cohesion: 0.17
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 14 - "MlKemError"
Cohesion: 0.16
Nodes (9): encapsulate(), MlKemError, _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged(), test_valid_public_key_round_trip_matches_decapsulation() (+1 more)

### Community 15 - "json"
Cohesion: 0.13
Nodes (7): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section(), test_clear_incremental_state_preserves_only_shared_artifacts(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

### Community 16 - "test_cloud_storage.py"
Cohesion: 0.20
Nodes (15): MeasurementRepository, test_closed_database_errors_are_safe(), test_concurrent_repository_access(), test_corrupted_stored_row_is_translated(), test_database_uniqueness_is_a_conflict_not_idempotent_success(), test_invalid_metadata_and_domain_are_rejected(), test_invalid_repository_limits(), test_list_limit_filter_and_order() (+7 more)

### Community 17 - "test_kdf.py"
Cohesion: 0.17
Nodes (9): derive_session_key(), KdfError, _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected() (+1 more)

### Community 18 - "fetch_public_key"
Cohesion: 0.17
Nodes (10): fetch_public_key(), PublicKeyTransportError, PublicKeyRejected, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable(), test_http_status_is_classified(), test_invalid_json_is_not_a_transport_retry(), test_oversized_body_is_rejected() (+2 more)

### Community 19 - "public_key.py"
Cohesion: 0.20
Nodes (8): validate_public_key(), CloudPublicKey, parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 20 - "encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 21 - "test_public_key_client.py"
Cohesion: 0.18
Nodes (6): _body(), cloud_server(), _public_key(), _Response, test_fetch_does_not_encapsulate(), test_fetch_returns_validated_public_key()

### Community 22 - "StoredMeasurement"
Cohesion: 0.21
Nodes (4): StoredMeasurement, _stored(), test_exact_stored_model_mapping(), test_generated_metadata()

### Community 23 - "test_crypto_failure_is_classified_and_recorded"
Cohesion: 0.20
Nodes (3): SessionMetrics, test_crypto_failure_is_classified_and_recorded(), fail_encapsulation()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 240 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `test_session.py`, `session_client.py`, `MlKemError`, `test_kdf.py`, `fetch_public_key`, `test_crypto_failure_is_classified_and_recorded`, `session.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `create_app`, `cloud_service/app.py`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `FailureMode` connect `FailureMode` to `load_config`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `FailureInjector` (e.g. with `FailureMode` and `test_duplicate_sequence_selection_varies_by_seed()`) actually correct?**
  _`FailureInjector` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `MeasurementRepository` (e.g. with `CanonicalMeasurement` and `Database`) actually correct?**
  _`MeasurementRepository` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._