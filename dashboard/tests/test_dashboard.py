import importlib.util
from pathlib import Path

import pytest

MODULE = Path(__file__).parents[1] / "app.py"
SPEC = importlib.util.spec_from_file_location("dashboard_app", MODULE)
assert SPEC and SPEC.loader
dashboard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard)


def test_safe_environment_exposes_only_documented_settings() -> None:
    assert dashboard._safe_environment(
        ["GATEWAY_ID=gateway-001", "LOG_LEVEL=INFO", "API_TOKEN=not-visible"],
        "edge-gateway",
    ) == {"GATEWAY_ID": "gateway-001", "LOG_LEVEL": "INFO"}


def test_decode_docker_multiplexed_logs() -> None:
    payload = (
        b"\x01\x00\x00\x00\x00\x00\x00\x06first\n"
        + b"\x02\x00\x00\x00\x00\x00\x00\x07second\n"
    )
    assert dashboard._decode_logs(payload) == "first\nsecond\n"


def test_decode_chunked_docker_response() -> None:
    assert (
        dashboard._decode_chunks(b"5\r\nhello\r\n6\r\n world\r\n0\r\n\r\n")
        == b"hello world"
    )


def test_dashboard_ui_uses_cloud_measurement_timestamp_and_pagination() -> None:
    javascript = (Path(__file__).parents[1] / "static/app.js").read_text(
        encoding="utf-8"
    )

    for expected in (
        "item.measured_at",
        "pageSize = 10",
        "toFixed(2)",
        "Measurements received",
    ):
        assert expected in javascript


def test_dashboard_metric_display_distinguishes_durations_from_counts() -> None:
    javascript = (Path(__file__).parents[1] / "static/app.js").read_text(
        encoding="utf-8"
    )

    assert "name.includes('_duration_seconds')" in javascript
    assert "Math.round(Number(value))" in javascript


def test_dashboard_visually_separates_gateway_and_cloud_metrics() -> None:
    javascript = (Path(__file__).parents[1] / "static/app.js").read_text(
        encoding="utf-8"
    )
    stylesheet = (Path(__file__).parents[1] / "static/style.css").read_text(
        encoding="utf-8"
    )

    assert "Gateway metrics" in javascript
    assert "Cloud metrics" in javascript
    assert 'class="metric-section metric-section-${service}"' in javascript
    assert ".metric-section" in stylesheet
    assert ".metric-cards" in stylesheet


def test_gateway_duplicate_metric_describes_the_latest_sequence_rule() -> None:
    javascript = (Path(__file__).parents[1] / "static/app.js").read_text(
        encoding="utf-8"
    )

    assert "equals the latest accepted value for that device" in javascript


def test_dashboard_preserves_runtime_form_drafts_during_refresh() -> None:
    javascript = (Path(__file__).parents[1] / "static/app.js").read_text(
        encoding="utf-8"
    )

    assert "const runtimeDrafts = {};" in javascript
    assert "document.activeElement?.closest('.runtime-form')" in javascript
    assert "saveRuntimeDrafts();" in javascript
    assert "delete runtimeDrafts[service];" in javascript


def test_runtime_configuration_is_limited_to_safe_failure_controls() -> None:
    assert dashboard._validated_runtime_config(
        "cloud-service",
        {
            "FAILURE_MODE": "processing_delay",
            "FAILURE_RATE": "1",
            "FAILURE_SEED": "42",
            "FAILURE_DELAY_SECONDS": "2.5",
            "LOG_LEVEL": "debug",
        },
    ) == {
        "FAILURE_MODE": "processing_delay",
        "FAILURE_RATE": "1.0",
        "FAILURE_SEED": "42",
        "FAILURE_DELAY_SECONDS": "2.5",
        "LOG_LEVEL": "DEBUG",
    }


@pytest.mark.parametrize(
    "values",
    [
        {
            "FAILURE_MODE": "processing_delay",
            "FAILURE_RATE": "1",
            "FAILURE_SEED": "",
            "FAILURE_DELAY_SECONDS": "31",
            "LOG_LEVEL": "INFO",
        },
        {
            "FAILURE_MODE": "processing_delay",
            "FAILURE_RATE": "1",
            "FAILURE_SEED": "",
            "FAILURE_DELAY_SECONDS": "2",
            "LOG_LEVEL": "INFO",
            "SECURITY_MODE": "classical",
        },
    ],
)
def test_runtime_configuration_rejects_out_of_scope_values(
    values: dict[str, str]
) -> None:
    with pytest.raises(ValueError):
        dashboard._validated_runtime_config("cloud-service", values)
