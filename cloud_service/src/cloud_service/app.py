"""Cloud HTTP shell with storage lifecycle; ingestion and crypto follow later."""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

from cloud_service.config import Config, ConfigurationError, SecurityMode, load_config
from cloud_service.storage.database import Database, StorageError
from cloud_service.storage.repository import MeasurementRepository

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
        try:
            database = Database(settings.database_url)
        except StorageError:
            logger.error("cloud_startup_failed: storage unavailable")
            raise StartupError("Cloud storage initialization failed") from None
        app.state.database = database
        app.state.repository = MeasurementRepository(database)
        app.state.running = True
        try:
            yield
        finally:
            app.state.running = False
            try:
                database.close()
            finally:
                app.state.database = None
                app.state.repository = None
                logger.info("cloud_shutting_down")

    app = FastAPI(
        title="Cloud Service", lifespan=lifespan,
        docs_url=None, redoc_url=None, openapi_url=None,
    )
    app.state.config = settings
    app.state.running = False
    app.state.database = None
    app.state.repository = None

    @app.get("/health")
    async def health():
        if not app.state.running:
            return _unavailable()
        return {"status": "ok"}

    @app.get("/ready")
    async def ready():
        # Ingestion is not implemented yet; complete readiness is a later task.
        return _unavailable()

    @app.get("/metrics")
    async def metrics() -> Response:
        """Expose the bounded service-info metric available before storage exists."""
        return Response(
            content=(
                "# HELP cloud_service_info Cloud Service process information.\n"
                "# TYPE cloud_service_info gauge\n"
                f'cloud_service_info{{security_mode="{settings.security_mode.value}"}} 1\n'
            ),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

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
