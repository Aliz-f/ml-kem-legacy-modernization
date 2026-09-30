"""Gateway HTTP application with Legacy syntax, schema, and domain validation."""

from contextlib import asynccontextmanager
import logging
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, Response

from edge_gateway.config import ConfigurationError, GatewayConfig, load_config
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


def create_app(config: GatewayConfig | None = None) -> FastAPI:
    """Build an isolated app; importing this module has no startup side effects.

    Tests can inject settings from load_config(mapping) and override dependencies
    using app.dependency_overrides. No Cloud client or crypto session exists yet.
    """
    settings = load_config() if config is None else config
    level = _logging_level(settings)

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
            logger.info("gateway_shutting_down")

    app = FastAPI(
        title="Edge Gateway", lifespan=lifespan,
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
        # Processing/transport is absent, irrespective of secure-session state.
        return _unavailable()

    @app.post("/api/v1/measurements")
    async def measurements(request: Request):
        try:
            measurement = parse_legacy_measurement(await request.body())
            validate_legacy_measurement(measurement)
        except LegacyJSONError:
            return JSONResponse(status_code=400, content={"error": {
                "code": "INVALID_JSON", "message": "request body must be valid JSON",
            }})
        except (LegacyMeasurementSchemaError, LegacyMeasurementDomainError):
            return JSONResponse(status_code=422, content={"error": {
                "code": "INVALID_MEASUREMENT", "message": "measurement validation failed",
            }})
        # Downstream delivery is not implemented yet.
        return _unavailable()

    @app.get("/metrics")
    async def metrics(config: Annotated[GatewayConfig, Depends(get_config)]) -> Response:
        return Response(
            content=(
                "# HELP gateway_service_info Gateway process information.\n"
                "# TYPE gateway_service_info gauge\n"
                f'gateway_service_info{{security_mode="{config.security_mode}"}} 1\n'
            ),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    return app


def _unavailable() -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"error": {"code": "SERVICE_UNAVAILABLE", "message": "service is not ready"}},
    )


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
