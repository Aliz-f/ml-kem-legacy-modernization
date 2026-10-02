"""Gateway HTTP application and synchronous Legacy measurement endpoint."""

from contextlib import asynccontextmanager
from datetime import UTC, datetime
import logging
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, Response

from edge_gateway.config import ConfigurationError, GatewayConfig, load_config
from edge_gateway.cloud.baseline import BaselineCloudClient
from edge_gateway.crypto.failure import CryptoFailureInjector
from edge_gateway.crypto.metrics import PqcMetrics
from edge_gateway.crypto.secure_transport import SecureTransport
from edge_gateway.crypto.session import SessionManager
from edge_gateway.dispatch import BaselineTransport, CloudDispatch
from edge_gateway.errors import GatewayError, GatewayErrorCode
from edge_gateway.measurements import MeasurementProcessor, ProcessingHook, UnavailableBaseline
from edge_gateway.models import LegacyMeasurementSchemaError
from edge_gateway.validation import (
    LegacyJSONError,
    LegacyMeasurementDomainError,
    parse_legacy_measurement,
    validate_legacy_measurement,
)

logger = logging.getLogger("edge_gateway")


def get_config(request: Request) -> GatewayConfig:
    """Expose application settings through an overridable route dependency."""
    return request.app.state.config


def create_app(
    config: GatewayConfig | None = None, *, pqc_metrics: PqcMetrics | None = None,
    baseline_transport: BaselineTransport | None = None,
    secure_transport: SecureTransport | None = None,
    processing_hook: ProcessingHook | None = None,
) -> FastAPI:
    """Build an isolated app; importing this module has no startup side effects.

    Tests and Gateway composition inject the one process-wide PQC registry through
    ``pqc_metrics``. Transport construction belongs to composition; missing
    transport dependencies fail closed. No client/session is created implicitly.
    """
    settings = load_config() if config is None else config
    level = _logging_level(settings)
    registry = pqc_metrics or PqcMetrics()
    if settings.security_mode == "mlkem" and secure_transport is None:
        secure_transport = _secure_transport(settings, registry)
    dispatch = CloudDispatch(
        settings,
        baseline=baseline_transport or _baseline_transport(settings),
        secure=secure_transport,
        pqc_metrics=registry,
    )
    processor = MeasurementProcessor(
        gateway_id=settings.gateway_id, dispatch=dispatch, processing_hook=processing_hook,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logging.basicConfig(level=level, format="%(levelname)s %(name)s %(message)s")
        logger.setLevel(level)
        logger.info("gateway_starting security_mode=%s", settings.security_mode)
        app.state.running = True
        try:
            yield
        finally:
            app.state.running = False
            transport = getattr(app.state, "secure_transport", None)
            shutdown = getattr(transport, "shutdown", None)
            if shutdown is not None:
                shutdown()
            logger.info("gateway_shutting_down")

    app = FastAPI(
        title="Edge Gateway", lifespan=lifespan,
        docs_url=None, redoc_url=None, openapi_url=None,
    )
    app.state.config = settings
    app.state.pqc_metrics = registry
    app.state.running = False
    app.state.secure_transport = secure_transport

    @app.exception_handler(LegacyJSONError)
    async def invalid_json(request: Request, error: LegacyJSONError):
        return _error_response(GatewayErrorCode.INVALID_JSON)

    @app.exception_handler(LegacyMeasurementSchemaError)
    @app.exception_handler(LegacyMeasurementDomainError)
    async def invalid_measurement(request: Request, error: ValueError):
        return _error_response(GatewayErrorCode.INVALID_MEASUREMENT)

    @app.exception_handler(GatewayError)
    async def application_error(request: Request, error: GatewayError):
        return _error_response(error.code)

    @app.exception_handler(Exception)
    async def internal_error(request: Request, error: Exception):
        # Never interpolate exception text or traceback: either can contain secrets.
        logger.error("gateway_internal_error")
        return _error_response(GatewayErrorCode.INTERNAL_ERROR)

    @app.get("/health")
    async def health():
        if not app.state.running:
            return _unavailable()
        return {"status": "ok"}

    @app.get("/ready")
    async def ready():
        # Operational readiness is a later Member 2 task.
        return _unavailable()

    @app.post("/api/v1/measurements")
    async def measurements(request: Request):
        received_at = datetime.now(UTC)
        measurement = parse_legacy_measurement(await request.body())
        validate_legacy_measurement(measurement)
        await processor.process(measurement, received_at=received_at)
        return JSONResponse(status_code=202, content={"status": "accepted"})

    @app.get("/metrics")
    async def metrics(config: Annotated[GatewayConfig, Depends(get_config)]) -> Response:
        return Response(
            content=(
                "# HELP gateway_service_info Gateway process information.\n"
                "# TYPE gateway_service_info gauge\n"
                f'gateway_service_info{{security_mode="{config.security_mode}"}} 1\n'
                f"{registry.render()}"
            ),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    return app


def _baseline_transport(config: GatewayConfig) -> BaselineTransport:
    """Construct the baseline client only for explicit classical-mode dispatch."""
    if config.security_mode == "classical":
        return BaselineCloudClient(
            cloud_url=config.cloud_url,
            timeout_seconds=config.cloud_timeout_seconds,
            max_retries=config.cloud_max_retries,
        )
    return UnavailableBaseline()


def _secure_transport(config: GatewayConfig, metrics: PqcMetrics) -> SecureTransport:
    """Compose the one fail-closed Gateway secure path for Modernized Mode."""
    injector = CryptoFailureInjector.from_config(config)
    sessions = SessionManager(
        config.gateway_id,
        config.cloud_url,
        config.cloud_timeout_seconds,
        metrics=metrics,
        injector=injector,
    )
    return SecureTransport(
        sessions,
        cloud_url=config.cloud_url,
        timeout_seconds=config.cloud_timeout_seconds,
        max_retries=config.cloud_max_retries,
        injector=injector,
        metrics=metrics,
    )


def _unavailable() -> JSONResponse:
    return _error_response(GatewayErrorCode.SERVICE_UNAVAILABLE)


def _error_response(code: GatewayErrorCode) -> JSONResponse:
    return JSONResponse(status_code=code.status_code, content=code.to_dict())


def _logging_level(config: GatewayConfig) -> int:
    # M2-01 permits non-empty LOG_LEVEL; reject unusable names before serving.
    level = logging.getLevelNamesMapping().get(config.log_level)
    if level is None:
        raise ConfigurationError("LOG_LEVEL must name a Python logging level")
    return level


def main() -> int:
    """Run one server process with Uvicorn managing signals and shutdown."""
    try:
        config = load_config()
        app = create_app(config)
    except ConfigurationError:
        logging.basicConfig(level=logging.ERROR)
        logger.error("gateway_startup_failed: invalid configuration")
        return 1

    import uvicorn

    uvicorn.run(
        app, host=config.host, port=config.port,
        log_level=_logging_level(config), access_log=False,
        timeout_graceful_shutdown=5,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
