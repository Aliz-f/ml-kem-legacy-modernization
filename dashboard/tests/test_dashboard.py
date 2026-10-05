import importlib.util
from pathlib import Path

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
