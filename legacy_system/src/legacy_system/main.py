"""Executable entrypoint for the Legacy Device."""

from collections.abc import Callable
import logging

from legacy_system.config import Config, ConfigurationError, load_config
from legacy_system.device import DeviceController


def main(
    controller_factory: Callable[[Config], DeviceController] = DeviceController,
    config_loader: Callable[[], Config] | None = None,
) -> int:
    """Load configuration and run the Legacy Device controller."""
    try:
        config = (load_config if config_loader is None else config_loader)()
    except ConfigurationError as exc:
        logging.basicConfig(
            level=logging.ERROR,
            format="%(levelname)s %(name)s %(message)s",
        )
        logging.getLogger(__name__).error("event=invalid_configuration error=%s", exc)
        return 1
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format="%(levelname)s %(name)s %(message)s",
    )
    controller_factory(config).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
