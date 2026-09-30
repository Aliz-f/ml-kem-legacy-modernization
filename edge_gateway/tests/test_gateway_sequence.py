"""M2-10 frozen per-device sequence acceptance and rejection policy."""

from concurrent.futures import ThreadPoolExecutor
import logging
from threading import Barrier

import pytest

from edge_gateway.errors import GatewayError, GatewayErrorCode
from edge_gateway.sequence import SequenceTracker


@pytest.mark.parametrize("first", [0, 1, 184])
def test_first_and_next_sequence_are_accepted_without_gap(first, caplog):
    tracker = SequenceTracker()
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        tracker.check_and_update("sensor-001", first)
        tracker.check_and_update("sensor-001", first + 1)
    assert not caplog.records
    with pytest.raises(GatewayError) as error:
        tracker.check_and_update("sensor-001", first + 1)
    assert error.value.code is GatewayErrorCode.DUPLICATE_SEQUENCE


@pytest.mark.parametrize(
    ("rejected", "code"),
    [(10, GatewayErrorCode.DUPLICATE_SEQUENCE), (9, GatewayErrorCode.OUT_OF_ORDER_SEQUENCE)],
)
def test_rejection_has_frozen_error_and_does_not_change_state(rejected, code):
    tracker = SequenceTracker()
    tracker.check_and_update("sensor-001", 10)
    with pytest.raises(GatewayError) as error:
        tracker.check_and_update("sensor-001", rejected)
    assert error.value.code is code
    assert error.value.code.status_code == 409
    with pytest.raises(GatewayError) as unchanged:
        tracker.check_and_update("sensor-001", 10)
    assert unchanged.value.code is GatewayErrorCode.DUPLICATE_SEQUENCE
    tracker.check_and_update("sensor-001", 11)


def test_gap_is_logged_and_advances_state(caplog):
    tracker = SequenceTracker()
    tracker.check_and_update("sensor-001", 40)
    with caplog.at_level(logging.INFO, logger="edge_gateway"):
        tracker.check_and_update("sensor-001", 43)
    record, = caplog.records
    assert record.getMessage().startswith("sequence_gap_detected ")
    assert record.device_id == "sensor-001"
    assert record.previous_sequence_number == 40
    assert record.sequence_number == 43
    with pytest.raises(GatewayError) as error:
        tracker.check_and_update("sensor-001", 42)
    assert error.value.code is GatewayErrorCode.OUT_OF_ORDER_SEQUENCE
    with pytest.raises(GatewayError) as error:
        tracker.check_and_update("sensor-001", 43)
    assert error.value.code is GatewayErrorCode.DUPLICATE_SEQUENCE
    tracker.check_and_update("sensor-001", 44)


def test_devices_have_independent_state():
    tracker = SequenceTracker()
    tracker.check_and_update("sensor-a", 100)
    tracker.check_and_update("sensor-b", 0)
    tracker.check_and_update("sensor-b", 1)
    tracker.check_and_update("sensor-a", 101)


def test_new_tracker_has_no_previous_history():
    SequenceTracker().check_and_update("sensor-001", 100)
    SequenceTracker().check_and_update("sensor-001", 0)


def test_concurrent_same_sequence_is_accepted_only_once():
    tracker = SequenceTracker()
    barrier = Barrier(8)

    def submit():
        barrier.wait(timeout=5)
        try:
            tracker.check_and_update("sensor-001", 10)
        except GatewayError as error:
            return error.code
        return None

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: submit(), range(8)))
    assert results.count(None) == 1
    assert results.count(GatewayErrorCode.DUPLICATE_SEQUENCE) == 7
