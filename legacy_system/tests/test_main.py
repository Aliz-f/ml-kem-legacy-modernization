import logging

from legacy_system.config import Config, ConfigurationError, FailureMode
from legacy_system.main import main


class RecordingController:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.ran = False

    def run(self) -> None:
        self.ran = True


def make_config() -> Config:
    return Config(
        device_id="sensor-001",
        gateway_url="http://gateway.example.test",
        send_interval_seconds=5,
        request_timeout_seconds=3,
        max_retries=2,
        failure_mode=FailureMode.NONE,
        failure_rate=0.0,
        failure_seed=None,
        log_level="INFO",
    )


def test_main_loads_configuration_and_runs_controller(monkeypatch) -> None:
    config = make_config()
    controllers: list[RecordingController] = []

    def factory(received_config: Config) -> RecordingController:
        controller = RecordingController(received_config)
        controllers.append(controller)
        return controller

    monkeypatch.setattr("legacy_system.main.load_config", lambda: config)

    assert main(factory) == 0

    assert len(controllers) == 1
    assert controllers[0].config is config
    assert controllers[0].ran is True


def test_main_logs_invalid_configuration_and_returns_nonzero(
    caplog,
) -> None:
    caplog.set_level(logging.ERROR, logger="legacy_system.main")

    def invalid_config() -> Config:
        raise ConfigurationError("SEND_INTERVAL_SECONDS must be greater than zero")

    assert main(config_loader=invalid_config) == 1
    assert "event=invalid_configuration" in caplog.text
    assert "SEND_INTERVAL_SECONDS" in caplog.text
