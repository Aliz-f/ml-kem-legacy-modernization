# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 799 nodes · 1855 edges · 50 communities (25 shown, 25 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 237 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_symmetric.py
- load_config
- cli.py
- load_config
- LegacyMeasurement
- FailureMode
- test_sensor.py
- load_config
- test_public_key_client.py
- session.py
- CanonicalMeasurement
- public_key.py
- SessionManager
- test_session.py
- validate_measurement
- StorageError
- test_cloud_storage.py
- MlKemError
- encoding.py
- StoredMeasurement
- test_kdf.py
- refresh_graphify.py
- dataclasses
- _Clock
- test_crypto_failure_is_classified_and_recorded
- public_key_client.py
- SessionMetrics
- test_refresh_graphify.py
- _Handler
- _Handler
- measurement
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `FailureMode` - 33 edges
2. `load_config()` - 33 edges
3. `FailureInjector` - 31 edges
4. `load_config()` - 26 edges
5. `MeasurementRepository` - 25 edges
6. `create_app()` - 23 edges
7. `create_app()` - 23 edges
8. `load_config()` - 23 edges
9. `CanonicalMeasurement` - 22 edges
10. `LegacyMeasurement` - 20 edges

## Surprising Connections (you probably didn't know these)
- `test_invalid_metadata_and_domain_are_rejected()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_relative_path()` --uses--> `Database`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → cloud_service/src/cloud_service/storage/database.py
- `test_concurrent_repository_access()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_database_uniqueness_is_a_conflict_not_idempotent_success()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py
- `test_list_limit_filter_and_order()` --calls--> `replace()`  [INFERRED]
  cloud_service/tests/test_cloud_storage.py → edge_gateway/tests/test_session.py

## Import Cycles
- None detected.

## Communities (50 total, 25 thin omitted)

### Community 0 - "test_symmetric.py"
Cohesion: 0.06
Nodes (46): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number() (+38 more)

### Community 1 - "load_config"
Cohesion: 0.07
Nodes (33): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+25 more)

### Community 2 - "cli.py"
Cohesion: 0.11
Nodes (40): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+32 more)

### Community 3 - "load_config"
Cohesion: 0.07
Nodes (36): create_app(), health(), lifespan(), ready(), main(), StartupError, _unavailable(), Config (+28 more)

### Community 4 - "LegacyMeasurement"
Cohesion: 0.08
Nodes (29): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), parse_legacy_measurement(), _reject_constant(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable() (+21 more)

### Community 5 - "FailureMode"
Cohesion: 0.13
Nodes (26): FailureMode, FailureInjector, _sequence_number(), make_measurement(), make_payload(), test_duplicate_sequence_selection_varies_by_seed(), test_duplicate_sequence_uses_previous_sequence_without_rewinding_input(), test_failure_rate_one_always_injects() (+18 more)

### Community 6 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 7 - "load_config"
Cohesion: 0.14
Nodes (20): Config, ConfigurationError, _integer(), load_config(), _number(), _required_text(), _value(), test_default_configuration() (+12 more)

### Community 8 - "test_public_key_client.py"
Cohesion: 0.13
Nodes (16): _endpoint(), fetch_public_key(), PublicKeyTransportError, _body(), cloud_server(), _public_key(), _Response, test_cloud_url_and_timeout_are_validated() (+8 more)

### Community 9 - "session.py"
Cohesion: 0.16
Nodes (10): _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect, _request(), SessionRejected, SessionResponse (+2 more)

### Community 10 - "CanonicalMeasurement"
Cohesion: 0.19
Nodes (11): CanonicalMeasurement, MeasurementSchemaError, payload(), test_direct_construction_checks_schema(), test_invalid_timestamps(), test_missing_fields(), test_noncanonical_fields_rejected(), test_nonobject_payload() (+3 more)

### Community 11 - "public_key.py"
Cohesion: 0.16
Nodes (8): CloudPublicKey, parse_public_key_response(), PublicKeyRejected, _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 12 - "SessionManager"
Cohesion: 0.13
Nodes (3): SecureSession, SessionEstablishmentError, SessionManager

### Community 13 - "test_session.py"
Cohesion: 0.15
Nodes (8): SessionState, _manager(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key(), test_expired_session_is_replaced(), test_rejected_response_does_not_become_active(), test_unavailable_cloud_is_retryable_and_leaves_no_session()

### Community 14 - "validate_measurement"
Cohesion: 0.19
Nodes (12): MeasurementValidationError, validate_measurement(), payload(), test_errors_and_logs_do_not_echo_payload(), test_gateway_identity_requires_exact_match(), test_inclusive_domain_boundaries(), test_invalid_domains_and_schema(), test_invalid_timestamps_through_validator() (+4 more)

### Community 15 - "StorageError"
Cohesion: 0.15
Nodes (4): Database, StorageConflictError, StorageError, test_reopen_preserves_schema_and_committed_data()

### Community 16 - "test_cloud_storage.py"
Cohesion: 0.19
Nodes (15): MeasurementRepository, test_closed_database_errors_are_safe(), test_concurrent_repository_access(), test_corrupted_stored_row_is_translated(), test_database_uniqueness_is_a_conflict_not_idempotent_success(), test_invalid_repository_limits(), test_list_limit_filter_and_order(), test_missing_parent_and_invalid_file_errors_are_safe() (+7 more)

### Community 17 - "MlKemError"
Cohesion: 0.18
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 18 - "encoding.py"
Cohesion: 0.22
Nodes (6): decode_binary(), encode_binary(), EncodingError, test_invalid_alphabet_whitespace_and_empty_are_rejected(), test_padded_and_unpadded_forms_decode_equally(), test_round_trip_omits_padding()

### Community 19 - "StoredMeasurement"
Cohesion: 0.20
Nodes (5): StoredMeasurement, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 20 - "test_kdf.py"
Cohesion: 0.22
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 21 - "refresh_graphify.py"
Cohesion: 0.22
Nodes (4): clear_incremental_state(), normalize_artifacts(), refresh_graph(), _without_section()

### Community 23 - "_Clock"
Cohesion: 0.22
Nodes (4): _Clock, _Cloud, cloud_url(), _stamp()

### Community 24 - "test_crypto_failure_is_classified_and_recorded"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

### Community 27 - "test_refresh_graphify.py"
Cohesion: 0.38
Nodes (3): test_clear_incremental_state_preserves_only_shared_artifacts(), test_normalize_artifacts_removes_checkout_specific_metadata(), test_refresh_uses_a_stable_hash_seed()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 245 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `test_public_key_client.py`, `session.py`, `public_key.py`, `test_session.py`, `MlKemError`, `test_crypto_failure_is_classified_and_recorded`, `SessionMetrics`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `StorageError`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Why does `FailureMode` connect `FailureMode` to `load_config`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `FailureMode` (e.g. with `FailureInjector` and `test_default_configuration()`) actually correct?**
  _`FailureMode` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `FailureInjector` (e.g. with `FailureMode` and `test_duplicate_sequence_selection_varies_by_seed()`) actually correct?**
  _`FailureInjector` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `MeasurementRepository` (e.g. with `CanonicalMeasurement` and `Database`) actually correct?**
  _`MeasurementRepository` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._