# Legacy Device

The current provisional launcher can be run from the repository root with:

```text
uv run python -m legacy_system.main
```

The process reads its validated settings from the environment, constructs the
device controller, and runs until it receives `SIGINT` (Ctrl+C) or `SIGTERM`.
Both signals stop new work, log shutdown, and let the process exit normally.
The controller closes injected clients during shutdown. The current urllib
client releases each request's resources through its response context manager
and does not expose a separate `close()` operation.

The architecture documents do not yet define the permanent Legacy Device
launcher. The team must later decide whether to keep this `main.py` composition
root, move startup into `device.py`, or adopt `__main__.py` or a console script.
This module is therefore a provisional launcher and must not be treated as a
silent change to the frozen architecture. A container runtime's Docker stop
signal is `SIGTERM`, so it follows the same shutdown path when this module is
used as the container process.