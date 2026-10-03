"""M2-26 application transport boundary independent of Member 3 internals."""

import asyncio
import ast
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest

from edge_gateway.cloud.baseline import BaselineCloudError
from edge_gateway.crypto.secure_transport import SecureTransportError
from edge_gateway.errors import GatewayError, GatewayErrorCode
from edge_gateway.measurements import MeasurementProcessor
from edge_gateway.models import LegacyMeasurement
from edge_gateway.transport import CloudDeliveryError, CloudTransport


class _Transport:
    def __init__(self, error: Exception | None = None) -> None:
        self.calls: list[dict[str, object]] = []
        self.error = error

    async def send(self, **fields: object) -> object:
        self.calls.append(fields)
        if self.error is not None:
            raise self.error
        return SimpleNamespace(status="accepted", record_id="rec-1")


def _measurement() -> LegacyMeasurement:
    return LegacyMeasurement(
        device_id="sensor-001",
        temperature_c=21.7,
        humidity_pct=42.5,
        timestamp=datetime(2026, 9, 21, 13, 45, 31, tzinfo=UTC),
        sequence_number=1,
    )


def test_processor_accepts_the_mode_independent_transport_protocol() -> None:
    transport = _Transport()
    assert isinstance(transport, CloudTransport)
    processor = MeasurementProcessor(gateway_id="gateway-001", dispatch=transport)

    asyncio.run(
        processor.process(
            _measurement(), received_at=datetime(2026, 9, 21, 13, 45, 32, tzinfo=UTC)
        )
    )

    assert len(transport.calls) == 1
    assert transport.calls[0]["device_id"] == "sensor-001"
    assert transport.calls[0]["request_id"].startswith("req-")
    assert "gateway_id" not in transport.calls[0]


def test_concrete_transport_errors_share_one_application_boundary() -> None:
    assert issubclass(BaselineCloudError, CloudDeliveryError)
    assert issubclass(SecureTransportError, CloudDeliveryError)

    for error in (
        BaselineCloudError("baseline unavailable", retryable=True),
        SecureTransportError("secure unavailable", retryable=True),
    ):
        processor = MeasurementProcessor(
            gateway_id="gateway-001", dispatch=_Transport(error)
        )
        with pytest.raises(GatewayError) as caught:
            asyncio.run(
                processor.process(
                    _measurement(),
                    received_at=datetime(2026, 9, 21, 13, 45, 32, tzinfo=UTC),
                )
            )
        assert caught.value.code is GatewayErrorCode.CLOUD_UNAVAILABLE


def test_application_processor_has_no_concrete_transport_imports() -> None:
    import edge_gateway.measurements as measurements

    path = Path(measurements.__file__)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert "edge_gateway.cloud.baseline" not in imported
    assert "edge_gateway.crypto.secure_transport" not in imported
    assert "edge_gateway.dispatch" not in imported
