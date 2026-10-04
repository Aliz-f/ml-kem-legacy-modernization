"""SQLite initialization, transaction ownership, and safe storage errors."""

from contextlib import contextmanager
import sqlite3
from threading import RLock

from cloud_service.config import ConfigurationError, load_config


class StorageError(RuntimeError):
    """Storage failed; exception text never includes SQL, paths, or payloads."""


class StorageConflictError(StorageError):
    """An insert violated a database constraint; not idempotent success."""


_SCHEMA = """
CREATE TABLE IF NOT EXISTS measurements (
    record_id TEXT PRIMARY KEY NOT NULL,
    device_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    temperature_c REAL NOT NULL,
    humidity_pct REAL NOT NULL,
    measured_at TEXT NOT NULL,
    gateway_received_at TEXT NOT NULL,
    cloud_received_at TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    UNIQUE(device_id, sequence_number)
)
"""


class Database:
    """One process-local connection, serialized across application threads.

    Parent directories must exist. A file survives close/reopen; :memory: is
    connection-local. Transactions are committed before results leave callers.
    """

    def __init__(self, database_url: str):
        self._lock = RLock()
        self._connection: sqlite3.Connection | None = None
        try:
            url = load_config({"DATABASE_URL": database_url}).database_url
            connection = sqlite3.connect(url.removeprefix("sqlite:///"), timeout=3, check_same_thread=False)
            self._connection = connection
            connection.row_factory = sqlite3.Row
            with connection:
                connection.execute(_SCHEMA)
        except (sqlite3.Error, ConfigurationError):
            if self._connection is not None:
                self._connection.close()
                self._connection = None
            raise StorageError("storage initialization failed") from None

    @property
    def closed(self) -> bool:
        with self._lock:
            return self._connection is None

    @contextmanager
    def transaction(self):
        with self._lock:
            if self._connection is None:
                raise StorageError("storage is closed")
            try:
                with self._connection:
                    yield self._connection
            except sqlite3.IntegrityError:
                raise StorageConflictError("storage constraint conflict") from None
            except (sqlite3.Error, OverflowError):
                raise StorageError("storage operation failed") from None

    def is_writable(self) -> bool:
        """Return whether SQLite can currently acquire a write transaction.

        ``BEGIN IMMEDIATE`` checks the capability required by ingestion without
        changing application data; the transaction is always rolled back.
        """
        with self._lock:
            if self._connection is None:
                return False
            try:
                self._connection.execute("BEGIN IMMEDIATE")
                self._connection.execute("ROLLBACK")
            except sqlite3.Error:
                return False
            return True

    def close(self) -> None:
        with self._lock:
            if self._connection is not None:
                try:
                    self._connection.close()
                except sqlite3.Error:
                    raise StorageError("storage shutdown failed") from None
                finally:
                    self._connection = None
