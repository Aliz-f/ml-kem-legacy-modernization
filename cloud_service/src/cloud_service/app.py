"""Cloud baseline and authenticated secure ingestion with managed lifecycle.

Routes are assembled by ``create_app`` so every application instance has the
same protocol surface.
"""

from contextlib import asynccontextmanager
import logging
from time import perf_counter

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

from cloud_service.config import Config, ConfigurationError, SecurityMode, load_config
from cloud_service.crypto.kdf import derive_session_key
from cloud_service.crypto.keys import KeyService
from cloud_service.crypto.session import SessionAccessError, SessionManager
from cloud_service.crypto.symmetric import decrypt
from cloud_service.failure import FailureInjector
from cloud_service.gateway.crypto import router as crypto_router
from cloud_service.gateway.routes import router as gateway_router
from cloud_service.gateway.queries import router as query_router
from cloud_service.gateway.sessions import router as session_router, session_access_error_handler
from cloud_service.gateway.secure import router as secure_router
from cloud_service.storage.database import Database, StorageError
from cloud_service.storage.repository import MeasurementRepository
from cloud_service.metrics import CloudMetrics

logger = logging.getLogger("cloud_service")


class StartupError(RuntimeError):
    """The configured mode cannot be served by this implementation."""


def _crypto_dependencies_ready() -> bool:
    """Probe the maintained KDF and AEAD dependencies without using a session.

    This is a local readiness self-test with fixed non-protocol inputs.  It
    never creates, stores, transmits, or logs a Cloud session key.
    """
    try:
        key = derive_session_key(b"\x00" * 32)
        nonce = b"\x00" * 12
        ciphertext = AESGCM(key).encrypt(nonce, b"ready", b"cloud-readiness")
        return decrypt(key, nonce, ciphertext, b"cloud-readiness") == b"ready"
    except Exception:
        return False


def create_app(config: Config | None = None) -> FastAPI:
    """Create an isolated app using settings validated by the config loader.

    Importing this module does not read configuration, bind sockets, or create
    storage. Tests may pass a Config obtained from load_config(mapping).
    """
    settings = load_config() if config is None else config

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.setLevel(settings.log_level)
        logger.info("cloud_starting security_mode=%s", settings.security_mode.value)
        try:
            database = Database(settings.database_url)
        except StorageError:
            logger.error("cloud_startup_failed: storage unavailable")
            raise StartupError("Cloud storage initialization failed") from None
        app.state.database = database
        app.state.repository = MeasurementRepository(database)
        try:
            if settings.security_mode == SecurityMode.MLKEM:
                try:
                    app.state.keys = KeyService()
                    app.state.sessions = SessionManager(settings.session_ttl_seconds)
                except Exception:
                    logger.error("cloud_startup_failed: key initialization failed")
                    raise StartupError("Cloud key initialization failed") from None
            app.state.running = True
            logger.info("event=cloud_ready component=cloud_service security_mode=%s", settings.security_mode.value)
            yield
        finally:
            app.state.running = False
            if app.state.sessions is not None:
                app.state.sessions.close()
                app.state.sessions = None
            if app.state.keys is not None:
                app.state.keys.close()
                app.state.keys = None
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
    app.state.keys = None
    app.state.sessions = None
    app.state.metrics = CloudMetrics()
    app.state.failure_injector = FailureInjector.from_config(
        settings, on_applied=app.state.metrics.failure_injected,
    )
    app.include_router(gateway_router)
    app.include_router(query_router)
    app.include_router(crypto_router)
    app.include_router(session_router)
    app.include_router(secure_router)
    app.add_exception_handler(SessionAccessError, session_access_error_handler)

    @app.middleware("http")
    async def observe_request_duration(request, call_next):
        started = perf_counter()
        try:
            response = await call_next(request)
            if request.url.path == "/api/v1/baseline/measurements":
                app.state.metrics.increment("cloud_baseline_requests_total")
            elif request.url.path == "/api/v1/secure/measurements":
                app.state.metrics.increment("cloud_secure_requests_total")
                if response.status_code >= 400:
                    app.state.metrics.increment("cloud_secure_requests_rejected_total")
            return response
        finally:
            if request.url.path in {"/api/v1/baseline/measurements", "/api/v1/secure/measurements"}:
                app.state.metrics.observe_request_duration(perf_counter() - started)

    @app.get("/health")
    async def health():
        if not app.state.running:
            return _unavailable()
        return {"status": "ok"}

    @app.get("/ready")
    async def ready():
        database = app.state.database
        repository = app.state.repository
        if not app.state.running or database is None or database.closed or repository is None:
            return _unavailable()
        if settings.security_mode == SecurityMode.CLASSICAL:
            return {"status": "ready", "storage": "ok"}
        keys, sessions = app.state.keys, app.state.sessions
        if keys is None or keys.closed or sessions is None or not _crypto_dependencies_ready():
            return _unavailable()
        return {"status": "ready", "storage": "ok", "mlkem": "available"}

    @app.get("/metrics")
    async def metrics() -> Response:
        """Expose bounded Cloud operational and PQC observability metrics."""
        sessions = app.state.sessions
        app.state.metrics.set_active_sessions(0 if sessions is None else len(sessions))
        return Response(
            content=(
                "# HELP cloud_service_info Cloud Service process information.\n"
                "# TYPE cloud_service_info gauge\n"
                f'cloud_service_info{{security_mode="{settings.security_mode.value}"}} 1\n'
                f"{app.state.metrics.render()}"
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
