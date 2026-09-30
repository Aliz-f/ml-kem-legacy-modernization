"""Regression checks for safe root-level development configuration."""

from pathlib import Path


ROOT = Path(__file__).parents[1]


def _environment_keys() -> set[str]:
    return {
        line.split("=", 1)[0]
        for line in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#")
    }


def test_env_example_uses_frozen_service_scoped_failure_inputs() -> None:
    keys = _environment_keys()

    assert {
        "SECURITY_MODE",
        "SESSION_TTL_SECONDS",
        "LEGACY_FAILURE_MODE",
        "LEGACY_FAILURE_RATE",
        "LEGACY_FAILURE_SEED",
        "GATEWAY_FAILURE_MODE",
        "GATEWAY_FAILURE_RATE",
        "GATEWAY_FAILURE_SEED",
        "CLOUD_FAILURE_MODE",
        "CLOUD_FAILURE_RATE",
        "CLOUD_FAILURE_SEED",
        "CLOUD_FAILURE_DELAY_SECONDS",
    } <= keys
    assert not {"FAILURE_MODE", "FAILURE_RATE", "FAILURE_SEED", "FAILURE_DELAY_SECONDS"} & keys


def test_env_example_has_only_safe_frozen_defaults() -> None:
    values = {
        line.split("=", 1)[0]: line.split("=", 1)[1]
        for line in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#")
    }

    assert values["SECURITY_MODE"] == "classical"
    assert values["SESSION_TTL_SECONDS"] == "300"
    assert values["PQC_FAILURE_POLICY"] == "fail_closed"
    assert values["CLOUD_FAILURE_DELAY_SECONDS"] == "2"
    assert all("secret" not in key.lower() for key in values)


def test_env_example_documents_valid_values_for_every_setting() -> None:
    lines = (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
    setting_lines = [index for index, line in enumerate(lines) if "=" in line and not line.startswith("#")]

    for index in setting_lines:
        assert index > 0
        assert lines[index - 1].startswith("#")

    documented_options = "\n".join(line for line in lines if line.startswith("#"))
    for value in (
        "classical", "mlkem", "invalid_temperature", "session_expired",
        "mlkem_handshake_failure", "mlkem_decapsulation_failure", "drop_response",
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL",
    ):
        assert value in documented_options


def test_gitignore_keeps_example_and_excludes_local_runtime_files() -> None:
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8")

    for entry in (".venv/", "__pycache__/", ".env", ".env.*", "!.env.example", "*.log", "*.db"):
        assert entry in ignored
