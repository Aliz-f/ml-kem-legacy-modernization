# Edge Gateway

## Configuration

The Gateway loads environment variables once at application startup through
`edge_gateway.config.load_config()`. Invalid configuration raises
`ConfigurationError` and must prevent startup. No other Gateway module should
read its configuration directly from the environment.

| Variable | Default | Validation |
| --- | --- | --- |
| `GATEWAY_ID` | `gateway-001` | Non-empty |
| `HOST` | `0.0.0.0` | Non-empty |
| `PORT` | `8000` | TCP port, 1–65535 |
| `CLOUD_URL` | `http://cloud-service:9000` | Absolute HTTP(S) URL |
| `CLOUD_TIMEOUT_SECONDS` | `3` | Positive number |
| `CLOUD_MAX_RETRIES` | `2` | Integer greater than or equal to zero |
| `SECURITY_MODE` | `classical` | `classical` or `mlkem` |
| `SESSION_TTL_SECONDS` | `300` | Exactly `300` for protocol v1 |
| `PQC_FAILURE_POLICY` | `fail_closed` | `fail_closed` only for protocol v1 |
| `FAILURE_MODE` | `none` | A documented Gateway failure mode |
| `FAILURE_RATE` | `0.0` | Number from 0.0 to 1.0 inclusive |
| `FAILURE_SEED` | empty | Optional deterministic-test seed; empty means unset |
| `LOG_LEVEL` | `INFO` | Non-empty |

`SECURITY_MODE=classical` is the explicitly selected baseline mode. The
`mlkem` setting supports later secure transport work; it does not provide a
plaintext fallback.
