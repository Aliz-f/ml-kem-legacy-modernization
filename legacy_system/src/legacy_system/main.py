"""Executable entrypoint for the Legacy Device."""

from collections.abc import Callable
import logging

from legacy_system.config import Config, load_config
from legacy_system.device import DeviceController


def main(
    controller_factory: Callable[[Config], DeviceController] = DeviceController,
) -> None:
    """Load configuration and run the Legacy Device controller."""
    config = load_config()
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format="%(levelname)s %(name)s %(message)s",
    )
    controller_factory(config).run()


if __name__ == "__main__":
    main()