"""M2-19 application fault selection and ownership boundaries."""

import logging
import random

import pytest

from edge_gateway.config import KNOWN_FAILURE_MODES, load_config
from edge_gateway.failure import APPLICATION_FAILURE_MODES, FailureInjector


@pytest.mark.parametrize("mode", sorted(KNOWN_FAILURE_MODES))
def test_zero_rate_never_selects(mode):
    injector = FailureInjector(mode, 0, "demo")
    assert all(injector.select() is None for _ in range(50))


def test_defaults_are_disabled():
    assert FailureInjector().select() is None
    assert FailureInjector.from_config(load_config({})).select() is None


@pytest.mark.parametrize("mode", sorted(APPLICATION_FAILURE_MODES))
def test_rate_one_always_selects_configured_application_fault(mode):
    injector = FailureInjector.from_config(load_config({
        "FAILURE_MODE": mode, "FAILURE_RATE": "1", "FAILURE_SEED": "demo",
    }))
    assert [injector.select() for _ in range(20)] == [mode] * 20
    assert injector.select(APPLICATION_FAILURE_MODES - {mode}) is None


@pytest.mark.parametrize("mode", sorted(KNOWN_FAILURE_MODES - APPLICATION_FAILURE_MODES - {"random"}))
def test_non_application_modes_are_inert(mode):
    assert FailureInjector(mode, 1).select() is None


@pytest.mark.parametrize("mode", ["processing_error", "random"])
def test_seed_reproduces_mixed_decisions_without_global_random_changes(mode):
    global_state = random.getstate()
    first = FailureInjector(mode, 0.5, "repeatable")
    second = FailureInjector(mode, 0.5, "repeatable")
    decisions = [first.select() for _ in range(100)]
    assert decisions == [second.select() for _ in range(100)]
    assert None in decisions
    assert any(decision is not None for decision in decisions)
    assert set(decisions) <= APPLICATION_FAILURE_MODES | {None}
    assert random.getstate() == global_state


def test_random_candidates_are_stable_and_restricted_to_applicable_faults():
    allowed = ["processing_error", "cloud_timeout"]
    first = FailureInjector("random", 1, "demo")
    second = FailureInjector("random", 1, "demo")
    decisions = [first.select(allowed) for _ in range(100)]
    assert decisions == [second.select(reversed(allowed)) for _ in range(100)]
    assert set(decisions) == set(allowed)
    assert first.select([]) is None
    assert first.select(["corrupt_ciphertext"]) is None


def test_ineligible_calls_do_not_consume_seeded_decisions():
    first = FailureInjector("processing_error", 0.5, "demo")
    second = FailureInjector("processing_error", 0.5, "demo")
    for _ in range(50):
        assert first.select(["cloud_timeout"]) is None
    assert [first.select() for _ in range(50)] == [second.select() for _ in range(50)]


@pytest.mark.parametrize("rate", [-0.1, 1.1, float("nan"), float("inf"), True, "0.5", None])
def test_invalid_rate_rejected(rate):
    with pytest.raises(ValueError, match="failure_rate"):
        FailureInjector("random", rate)


@pytest.mark.parametrize("mode", ["unknown", "", None, []])
def test_invalid_mode_rejected(mode):
    with pytest.raises(ValueError, match="failure_mode"):
        FailureInjector(mode, 1)


def test_invalid_seed_rejected():
    with pytest.raises(ValueError, match="failure_seed"):
        FailureInjector("random", 1, object())


def test_logs_distinguish_selection_from_execution_and_omit_seed(caplog):
    with caplog.at_level(logging.DEBUG, logger="edge_gateway.failure.injector"):
        FailureInjector().select()
        assert not caplog.records
        injector = FailureInjector("processing_error", 1, "private-seed-marker")
        injector.select()
    assert "event=failure_injection_enabled mode=processing_error" in caplog.text
    assert "event=failure_selected failure_type=processing_error" in caplog.text
    assert "failure_injected" not in caplog.text
    assert "private-seed-marker" not in caplog.text
