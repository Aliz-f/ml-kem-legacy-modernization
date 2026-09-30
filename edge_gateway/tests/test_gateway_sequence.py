"""M2-10 policy and M2-11 process-local state lifetime and concurrency."""

from concurrent.futures import ThreadPoolExecutor
import logging
from threading import Barrier, Event

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
    original = SequenceTracker()
    original.check_and_update("sensor-001", 100)
    SequenceTracker().check_and_update("sensor-001", 0)
    with pytest.raises(GatewayError) as error:
        original.check_and_update("sensor-001", 100)
    assert error.value.code is GatewayErrorCode.DUPLICATE_SEQUENCE


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


@pytest.mark.parametrize("failure_type", [TimeoutError, ConnectionError])
def test_committed_sequence_survives_later_cloud_failure(failure_type):
    """Exercise the tracker boundary with a stub, not the future HTTP route."""
    tracker = SequenceTracker()
    tracker.check_and_update("sensor-001", 9)

    def failing_cloud_delivery():
        # State must already be committed when the downstream call starts.
        with pytest.raises(GatewayError) as error:
            tracker.check_and_update("sensor-001", 10)
        assert error.value.code is GatewayErrorCode.DUPLICATE_SEQUENCE
        raise failure_type("simulated Cloud delivery failure")

    with pytest.raises(failure_type):
        tracker.check_and_update("sensor-001", 10)
        failing_cloud_delivery()

    # A Legacy retry remains a duplicate even though Cloud did not accept it.
    with pytest.raises(GatewayError) as error:
        tracker.check_and_update("sensor-001", 10)
    assert error.value.code is GatewayErrorCode.DUPLICATE_SEQUENCE
    assert error.value.code.status_code == 409
    tracker.check_and_update("sensor-001", 11)


def test_pending_cloud_failure_does_not_block_or_undo_newer_sequence():
    tracker = SequenceTracker()
    delivery_started = Event()
    release_delivery = Event()

    def accept_then_deliver():
        tracker.check_and_update("sensor-001", 10)
        delivery_started.set()
        assert release_delivery.wait(timeout=5)
        raise TimeoutError("simulated Cloud timeout")

    with ThreadPoolExecutor(max_workers=2) as pool:
        delivery = pool.submit(accept_then_deliver)
        try:
            assert delivery_started.wait(timeout=5)
            newer = pool.submit(tracker.check_and_update, "sensor-001", 11)
            newer.result(timeout=5)
        finally:
            release_delivery.set()
        with pytest.raises(TimeoutError):
            delivery.result(timeout=5)

    with pytest.raises(GatewayError) as error:
        tracker.check_and_update("sensor-001", 11)
    assert error.value.code is GatewayErrorCode.DUPLICATE_SEQUENCE
    with pytest.raises(GatewayError) as error:
        tracker.check_and_update("sensor-001", 10)
    assert error.value.code is GatewayErrorCode.OUT_OF_ORDER_SEQUENCE


def test_concurrent_different_sequences_leave_highest_accepted_state():
    tracker = SequenceTracker()
    tracker.check_and_update("sensor-001", 9)
    barrier = Barrier(8)

    def submit(sequence_number):
        barrier.wait(timeout=5)
        try:
            tracker.check_and_update("sensor-001", sequence_number)
        except GatewayError as error:
            return sequence_number, error.code
        return sequence_number, None

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(pool.map(submit, range(10, 18)))
    # Scheduling may vary; 17 must be accepted and the final state must be 17.
    assert results[17] is None
    assert all(code in (None, GatewayErrorCode.OUT_OF_ORDER_SEQUENCE) for code in results.values())
    with pytest.raises(GatewayError) as error:
        tracker.check_and_update("sensor-001", 17)
    assert error.value.code is GatewayErrorCode.DUPLICATE_SEQUENCE
    tracker.check_and_update("sensor-001", 18)
