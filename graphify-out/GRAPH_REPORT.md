# Graph Report - ml-kem-legacy-modernization  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 723 nodes · 1657 edges · 41 communities (25 shown, 16 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 187 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_symmetric.py
- load_config
- CanonicalMeasurement
- cli.py
- test_sensor.py
- session_client.py
- load_config
- test_gateway_models.py
- load_config
- test_session.py
- test_cloud_storage.py
- MlKemError
- cloud_service/app.py
- SessionManager
- StorageError
- ConfigurationError
- session.py
- fetch_public_key
- StoredMeasurement
- test_kdf.py
- test_public_key_client.py
- parse_public_key_response
- test_cli.py
- refresh_graphify.py
- test_crypto_failure_is_classified_and_recorded
- SessionState
- SessionMetrics
- _Handler
- _Handler
- cloud-service
- edge-gateway
- legacy-system
- ml-kem-legacy-modernization

## God Nodes (most connected - your core abstractions)
1. `load_config()` - 33 edges
2. `MeasurementRepository` - 25 edges
3. `load_config()` - 25 edges
4. `load_config()` - 23 edges
5. `create_app()` - 23 edges
6. `CanonicalMeasurement` - 22 edges
7. `SessionManager` - 19 edges
8. `create_app()` - 19 edges
9. `StorageError` - 18 edges
10. `fetch_public_key()` - 18 edges

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

## Communities (41 total, 16 thin omitted)

### Community 0 - "test_symmetric.py"
Cohesion: 0.05
Nodes (47): AadError, build_aad(), _require_id(), build_secure_envelope(), SecureEnvelope, PlaintextError, _require_id(), _require_number() (+39 more)

### Community 1 - "load_config"
Cohesion: 0.07
Nodes (32): create_app(), health(), measurements(), ready(), get_config(), _logging_level(), main(), _unavailable() (+24 more)

### Community 2 - "CanonicalMeasurement"
Cohesion: 0.07
Nodes (25): CanonicalMeasurement, MeasurementSchemaError, _timestamp(), MeasurementValidationError, validate_measurement(), payload(), test_direct_construction_checks_schema(), test_invalid_timestamps() (+17 more)

### Community 3 - "cli.py"
Cohesion: 0.14
Nodes (31): main(), parser(), record_work(), recorded_changes(), require_active(), resolve_merge_conflict(), details(), review() (+23 more)

### Community 4 - "test_sensor.py"
Cohesion: 0.08
Nodes (18): Measurement, Sensor, _validate_number(), FalseyClock, FalseyRandomSource, make_measurement(), test_measurement_accepts_valid_internal_state(), test_measurement_rejects_invalid_domain_values() (+10 more)

### Community 5 - "session_client.py"
Cohesion: 0.10
Nodes (16): decode_binary(), encode_binary(), EncodingError, _endpoint(), _parse_expires_at(), parse_session_response(), post_session(), _RejectRedirect (+8 more)

### Community 6 - "load_config"
Cohesion: 0.12
Nodes (21): Config, ConfigurationError, FailureMode, _integer(), load_config(), _number(), _required_text(), _value() (+13 more)

### Community 7 - "test_gateway_models.py"
Cohesion: 0.15
Nodes (16): LegacyMeasurement, LegacyMeasurementSchemaError, _timestamp(), payload(), test_canonical_field_name_cannot_replace_legacy_timestamp(), test_direct_construction_checks_types_and_model_is_immutable(), test_domain_validation_is_a_separate_stage(), test_each_required_field_is_required() (+8 more)

### Community 8 - "load_config"
Cohesion: 0.16
Nodes (16): create_app(), lifespan(), main(), StartupError, load_config(), test_apps_have_independent_lifecycle_state(), test_cli_uses_configured_server_settings(), test_factory_validates_process_config() (+8 more)

### Community 9 - "test_session.py"
Cohesion: 0.13
Nodes (10): _Clock, _Cloud, cloud_url(), _manager(), _stamp(), test_close_wipes_the_session_key(), test_concurrent_callers_share_one_handshake(), test_establishment_stores_one_active_session_with_matching_key() (+2 more)

### Community 10 - "test_cloud_storage.py"
Cohesion: 0.17
Nodes (17): MeasurementRepository, database(), test_closed_database_errors_are_safe(), test_concurrent_repository_access(), test_corrupted_stored_row_is_translated(), test_database_uniqueness_is_a_conflict_not_idempotent_success(), test_invalid_repository_limits(), test_list_limit_filter_and_order() (+9 more)

### Community 11 - "MlKemError"
Cohesion: 0.18
Nodes (10): encapsulate(), MlKemError, validate_public_key(), _raw_public_key(), test_encapsulation_is_fresh(), test_invalid_public_key_length_is_rejected(), test_library_rejected_public_key_is_translated(), test_shared_secret_is_not_logged() (+2 more)

### Community 12 - "cloud_service/app.py"
Cohesion: 0.15
Nodes (8): health(), ready(), _unavailable(), Config, FailureMode, SecurityMode, test_custom_environment(), test_defaults_do_not_create_database()

### Community 13 - "SessionManager"
Cohesion: 0.15
Nodes (3): SecureSession, SessionEstablishmentError, SessionManager

### Community 14 - "StorageError"
Cohesion: 0.16
Nodes (3): Database, StorageConflictError, StorageError

### Community 15 - "ConfigurationError"
Cohesion: 0.18
Nodes (12): ConfigurationError, integer(), number(), text(), value(), test_errors_do_not_echo_invalid_values(), test_inclusive_boundaries(), test_invalid_configuration() (+4 more)

### Community 16 - "session.py"
Cohesion: 0.14
Nodes (3): _endpoint(), _RejectRedirect, CloudPublicKey

### Community 17 - "fetch_public_key"
Cohesion: 0.17
Nodes (10): fetch_public_key(), PublicKeyTransportError, PublicKeyRejected, test_cloud_url_and_timeout_are_validated(), test_connection_failure_is_retryable(), test_http_status_is_classified(), test_invalid_json_is_not_a_transport_retry(), test_oversized_body_is_rejected() (+2 more)

### Community 18 - "StoredMeasurement"
Cohesion: 0.20
Nodes (5): StoredMeasurement, _stored(), test_exact_stored_model_mapping(), test_generated_metadata(), test_invalid_metadata_and_domain_are_rejected()

### Community 19 - "test_kdf.py"
Cohesion: 0.22
Nodes (7): derive_session_key(), _independent(), test_different_secret_derives_a_different_session_key(), test_same_secret_derives_the_same_session_key(), test_session_key_is_32_bytes_and_info_is_exact(), test_session_key_is_not_logged(), test_shared_secret_length_is_rejected()

### Community 20 - "test_public_key_client.py"
Cohesion: 0.18
Nodes (6): _body(), cloud_server(), _public_key(), _Response, test_fetch_does_not_encapsulate(), test_fetch_returns_validated_public_key()

### Community 21 - "parse_public_key_response"
Cohesion: 0.26
Nodes (6): parse_public_key_response(), _payload(), _public_key(), test_contract_violations_are_rejected(), test_missing_fields_and_non_object_are_rejected(), test_valid_response_returns_raw_public_key()

### Community 22 - "test_cli.py"
Cohesion: 0.42
Nodes (9): run(), start(), test_cannot_start_while_active_or_corrupt_state(), test_first_id_slug_and_multiline_prompt(), test_full_acceptance_lifecycle(), test_modified_requires_changes_and_revision_preserves_rounds(), test_rejection_and_second_task(), test_validation_rejects_duplicate_metadata_and_mismatched_filename() (+1 more)

### Community 23 - "refresh_graphify.py"
Cohesion: 0.31
Nodes (3): normalize_artifacts(), refresh_graph(), _without_section()

### Community 24 - "test_crypto_failure_is_classified_and_recorded"
Cohesion: 0.29
Nodes (4): KdfError, test_crypto_failure_is_classified_and_recorded(), fail_derivation(), fail_encapsulation()

## Knowledge Gaps
- **4 isolated node(s):** `cloud-service`, `edge-gateway`, `legacy-system`, `ml-kem-legacy-modernization`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 228 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SessionManager` connect `SessionManager` to `session_client.py`, `test_session.py`, `MlKemError`, `session.py`, `fetch_public_key`, `test_crypto_failure_is_classified_and_recorded`, `SessionMetrics`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `load_config()` connect `load_config` to `cloud_service/app.py`, `StorageError`, `ConfigurationError`?**
  _High betweenness centrality (0.023) - this node is a cross-community bridge._
- **Why does `CanonicalMeasurement` connect `CanonicalMeasurement` to `StoredMeasurement`, `test_cloud_storage.py`, `StorageError`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `MeasurementRepository` (e.g. with `CanonicalMeasurement` and `Database`) actually correct?**
  _`MeasurementRepository` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `create_app()` (e.g. with `lifespan()` and `Config`) actually correct?**
  _`create_app()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `cloud-service`, `edge-gateway`, `legacy-system` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `test_symmetric.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05183861082737487 - nodes in this community are weakly interconnected._