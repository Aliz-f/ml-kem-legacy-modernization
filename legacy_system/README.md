# Legacy Device

Run the Legacy Device from the repository root with:

```text
uv run python -m legacy_system.main
```

The process reads its validated settings from the environment, constructs the
device controller, and runs until it receives `SIGINT` (Ctrl+C) or `SIGTERM`.
Both signals stop new work, log shutdown, and let the process exit normally.
The controller closes injected clients during shutdown. The current urllib
client releases each request's resources through its response context manager
and does not expose a separate `close()` operation.

The installed `legacy-device` console script uses the same `main.py`
composition root. The Docker image likewise runs `python -m
legacy_system.main`; its `SIGTERM` follows the same shutdown path.

## Architecture and Operations

For complete architectural details, module responsibilities, JSON wire contract,
failure-injection mechanics, retry algorithms, and operational procedures, see
[architecture-operations.md](docs/architecture-operations.md).

