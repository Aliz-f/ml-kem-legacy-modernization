"""Gateway-generated tracing IDs, separate from canonical measurement data."""

import logging
from uuid import uuid4


logger = logging.getLogger("edge_gateway")


def create_request_id() -> str:
    """Create once after validation and sequence acceptance, before delivery.

    Keep this value for transport retries and session recovery. IDs are public
    tracing context, never key material or metric labels. No payload or inbound
    header contributes to the generated value.
    """
    request_id = f"req-{uuid4()}"
    logger.info("gateway_request_created request_id=%s", request_id, extra={"request_id": request_id})
    return request_id


def baseline_headers(request_id: str) -> dict[str, str]:
    """Carry the already-created ID to Cloud without modifying the JSON body.

    The caller passes an ID from create_request_id, including on retries.
    """
    return {"X-Request-ID": request_id}
