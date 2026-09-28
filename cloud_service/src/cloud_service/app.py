"""Cloud HTTP shell; persistence and secure processing arrive in later tasks."""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from cloud_service.config import Config, ConfigurationError, SecurityMode, load_config

logger = logging.getLogger("cloud_service")


class StartupError(RuntimeError):
    """The configured mode cannot be served by this implementation."""


def create_app(config: Config | None = None) -> FastAPI:
    """Create an isolated app using settings validated by the config loader.

    Importing this module does not read configuration, bind sockets, or create
    storage. Tests may pass a Config obtained from load_config(mapping).
    """
    settings = load_config() if config is None else config

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.setLevel(settings.log_level)
        if settings.security_mode != SecurityMode.CLASSICAL:
            logger.error("cloud_startup_failed: secure subsystems unavailable")
            raise StartupError("Modernized Mode is not implemented yet")
        logger.info("cloud_starting security_mode=%s", settings.security_mode.value)
        app.state.running = True
        try:
            yield
        finally:
            app.state.running = False
            logger.info("cloud_shutting_down")

    app = FastAPI(
        title="Cloud Service", lifespan=lifespan,
        docs_url=None, redoc_url=None, openapi_url=None,
    )
    app.state.config = settings
    app.state.running = False

    @app.get("/health")
    async def health():
        if not app.state.running:
            return _unavailable()
        return {"status": "ok"}

    @app.get("/ready")
    async def ready():
        # No storage exists at M4-02. Never claim readiness to persist data.
        return _unavailable()

    return app


def _unavailable() -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"error": {"code": "SERVICE_UNAVAILABLE", "message": "service is not ready"}},
    )


def main() -> int:
    """Load configuration and run the server with its managed signal lifecycle."""
    try:
        config = load_config()
    except ConfigurationError:
        # Do not echo environment values or exception details at startup.
        logging.basicConfig(level=logging.ERROR)
        logger.error("cloud_startup_failed: invalid configuration")
        return 1

    logging.basicConfig(level=config.log_level, format="%(levelname)s %(name)s %(message)s")
    import uvicorn

    uvicorn.run(
        create_app(config), host=config.host, port=config.port,
        log_level=config.log_level.lower(), access_log=False,
        timeout_graceful_shutdown=5,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
