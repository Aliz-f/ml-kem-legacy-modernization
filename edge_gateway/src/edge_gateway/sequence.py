"""In-memory Legacy sequence policy, independent of downstream delivery."""

import logging
from threading import Lock

from edge_gateway.application_log import log_application
from edge_gateway.errors import GatewayError, GatewayErrorCode


class SequenceTracker:
    """Track the last valid sequence accepted for each device in one process.

    Share one instance across requests. Restarting loses history. Call only
    after schema/domain validation and before Cloud delivery; accepted state
    is never rolled back for a later delivery failure.

    The lock protects only the local check and commit. Cloud I/O belongs to
    the caller after this method returns and must not hold the sequence lock.
    Instances do not share state across processes or persist it to storage.
    """

    def __init__(self) -> None:
        self._last_sequence: dict[str, int] = {}
        self._lock = Lock()

    def check_and_update(self, device_id: str, sequence_number: int) -> None:
        """Atomically accept a validated sequence or raise its frozen 409 error.

        First values (including zero) and higher values are accepted. Gaps are
        logged. Rejections leave the previously accepted state unchanged.
        """
        with self._lock:
            previous = self._last_sequence.get(device_id)
            if previous is not None:
                if sequence_number == previous:
                    log_application(
                        "sequence_duplicate_detected", logging.WARNING,
                        device_id=device_id, sequence_number=sequence_number,
                    )
                    raise GatewayError(GatewayErrorCode.DUPLICATE_SEQUENCE)
                if sequence_number < previous:
                    log_application(
                        "sequence_out_of_order_detected", logging.WARNING,
                        device_id=device_id, sequence_number=sequence_number,
                        previous_sequence_number=previous,
                    )
                    raise GatewayError(GatewayErrorCode.OUT_OF_ORDER_SEQUENCE)
            self._last_sequence[device_id] = sequence_number

        if previous is not None and sequence_number > previous + 1:
            log_application(
                "sequence_gap_detected",
                device_id=device_id,
                sequence_number=sequence_number,
                previous_sequence_number=previous,
            )
