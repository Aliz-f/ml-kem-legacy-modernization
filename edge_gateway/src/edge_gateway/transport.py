"""Application-facing Cloud transport contract, independent of security mode."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


class CloudDeliveryError(Exception):
    """A selected Cloud transport could not confirm measurement acceptance."""


@runtime_checkable
class CloudTransport(Protocol):
    """Deliver one normalized measurement with separate request correlation.

    The application pipeline depends on this interface only. ``CloudDispatch``
    supplies the Gateway identity and selects the baseline or secure adapter.
    """

    async def send(
        self,
        *,
        request_id: str,
        device_id: str,
        temperature_c: float,
        humidity_pct: float,
        measured_at: str,
        sequence_number: int,
        received_at: str,
    ) -> object:
        """Return a transport acceptance or raise ``CloudDeliveryError``."""
