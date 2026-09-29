"""Controlled-clock ownership/expiry, cleanup and publication tests."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest

from cloud_service.crypto.session import SessionAccessError, SessionManager, SessionState


@pytest.fixture
def clock():
    return [datetime(2026, 9, 29, tzinfo=timezone.utc)]


def test_ownership_before_expiry_and_exact_boundary(clock):
    manager = SessionManager(clock=lambda: clock[0])
    session = manager.create("gw1", "key1", b"a" * 32)
    assert session.expires_at == session.created_at + timedelta(seconds=300)
    assert "session_key" not in repr(session)
    original_expiry = session.expires_at
    clock[0] += timedelta(seconds=299, microseconds=999999)
    assert manager.get(session.session_id, "gw1") is session
    assert session.expires_at == original_expiry
    clock[0] += timedelta(microseconds=1)
    with pytest.raises(SessionAccessError) as caught:
        manager.get(session.session_id, "gw2")
    assert (caught.value.status_code, caught.value.code) == (400, "SECURE_MESSAGE_REJECTED")
    assert session.state == SessionState.ACTIVE  # Wrong owner cannot remove it.
    with pytest.raises(SessionAccessError) as caught:
        manager.get(session.session_id, "gw1")
    assert (caught.value.status_code, caught.value.code) == (409, "SESSION_EXPIRED")
    assert session.state == SessionState.EXPIRED
    assert session.session_key == bytearray(32)
    assert len(manager) == 0
    assert session.expires_at == original_expiry
    with pytest.raises(SessionAccessError) as caught:
        manager.get(session.session_id, "gw1")
    assert caught.value.code == "SESSION_INVALID"


def test_unknown_wrong_owner_and_invalidation(clock):
    manager = SessionManager(clock=lambda: clock[0])
    with pytest.raises(SessionAccessError) as caught:
        manager.get("missing", "gw")
    assert (caught.value.status_code, caught.value.code) == (409, "SESSION_INVALID")
    session = manager.create("gw", "key", b"a" * 32)
    with pytest.raises(SessionAccessError) as caught:
        manager.get(session.session_id, "other")
    assert caught.value.code == "SECURE_MESSAGE_REJECTED"
    assert manager.get(session.session_id, "gw") is session
    manager.invalidate(session.session_id)
    manager.invalidate(session.session_id)
    assert session.state == SessionState.INVALIDATED
    assert session.session_key == bytearray(32)
    assert len(manager) == 0


def test_remove_expired_and_shutdown(clock):
    manager = SessionManager(clock=lambda: clock[0])
    expired = manager.create("gw", "key", b"a" * 32)
    clock[0] += timedelta(seconds=200)
    active = manager.create("gw", "key", b"b" * 32)
    clock[0] += timedelta(seconds=100)
    assert manager.remove_expired() == 1
    assert expired.state == SessionState.EXPIRED
    assert expired.session_key == bytearray(32)
    assert manager.get(active.session_id, "gw") is active
    manager.close()
    manager.close()
    assert active.state == SessionState.CLOSED
    assert active.session_key == bytearray(32)
    assert len(manager) == 0
    with pytest.raises(ValueError, match="closed"):
        manager.create("gw", "key", b"c" * 32)


@pytest.mark.parametrize("ttl", [0, 1, 299, 301, True, 300.0])
def test_production_ttl_is_fixed(ttl):
    with pytest.raises(ValueError):
        SessionManager(ttl)


@pytest.mark.parametrize("values", [("", "key", b"a" * 32), ("gw", " ", b"a" * 32),
                                     ("gw", "key", b"a" * 31), ("gw", "key", "a" * 32)])
def test_invalid_creation_never_publishes(values):
    manager = SessionManager()
    with pytest.raises(ValueError):
        manager.create(*values)
    assert len(manager) == 0


def test_clock_failure_never_publishes():
    manager = SessionManager(clock=lambda: datetime(2026, 1, 1))
    with pytest.raises(ValueError, match="UTC"):
        manager.create("gw", "key", b"a" * 32)
    assert len(manager) == 0


def test_parallel_sessions_are_distinct_and_independent():
    manager = SessionManager()
    with ThreadPoolExecutor(max_workers=4) as pool:
        sessions = list(pool.map(lambda index: manager.create(f"gw-{index}", "key", b"a" * 32), range(16)))
    assert len({session.session_id for session in sessions}) == len(manager) == 16
    for session in sessions:
        assert manager.get(session.session_id, session.gateway_id) is session
    manager.close()
    assert all(session.session_key == bytearray(32) for session in sessions)
