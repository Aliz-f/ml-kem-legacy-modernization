"""Parameterized SQLite operations, independent of HTTP and crypto."""

from datetime import datetime
from dataclasses import dataclass
import sqlite3

from cloud_service.models import CanonicalMeasurement
from cloud_service.storage.database import Database, StorageError
from cloud_service.storage.models import StoredMeasurement


_INSERT = """INSERT INTO measurements
    (record_id, device_id, gateway_id, temperature_c, humidity_pct,
     measured_at, gateway_received_at, cloud_received_at, sequence_number)
    VALUES (:record_id, :device_id, :gateway_id, :temperature_c, :humidity_pct,
            :measured_at, :gateway_received_at, :cloud_received_at, :sequence_number)"""


@dataclass(frozen=True, slots=True)
class SaveResult:
    measurement: StoredMeasurement
    created: bool


def _stored(row: sqlite3.Row) -> StoredMeasurement:
    try:
        values = dict(row)
        for name in ("measured_at", "gateway_received_at", "cloud_received_at"):
            values[name] = datetime.fromisoformat(values[name])
        return StoredMeasurement(**values)
    except (TypeError, ValueError):
        raise StorageError("stored measurement is invalid") from None


class MeasurementRepository:
    def __init__(self, database: Database):
        self._database = database

    def save(self, measurement: CanonicalMeasurement) -> StoredMeasurement:
        stored = StoredMeasurement.from_canonical(measurement)
        values = stored.to_dict()
        with self._database.transaction() as connection:
            connection.execute(_INSERT, values)
        return stored

    def save_idempotent(self, measurement: CanonicalMeasurement) -> SaveResult:
        """Commit one logical record or return the existing device/sequence row.

        The targeted conflict clause does not hide unrelated integrity failures.
        INSERT and lookup run in one transaction, including across connections.
        A repeat never overwrites the first accepted measurement or metadata.
        """
        candidate = StoredMeasurement.from_canonical(measurement)
        with self._database.transaction() as connection:
            cursor = connection.execute(
                _INSERT + " ON CONFLICT(device_id, sequence_number) DO NOTHING",
                candidate.to_dict(),
            )
            created = cursor.rowcount == 1
            row = connection.execute(
                "SELECT * FROM measurements WHERE device_id = ? AND sequence_number = ?",
                (measurement.device_id, measurement.sequence_number),
            ).fetchone()
            if row is None:
                raise StorageError("stored measurement could not be retrieved")
            result = SaveResult(_stored(row), created)
        return result

    def get(self, record_id: str) -> StoredMeasurement | None:
        with self._database.transaction() as connection:
            row = connection.execute("SELECT * FROM measurements WHERE record_id = ?", (record_id,)).fetchone()
            return None if row is None else _stored(row)

    def find_by_device_sequence(self, device_id: str, sequence_number: int) -> StoredMeasurement | None:
        with self._database.transaction() as connection:
            row = connection.execute(
                "SELECT * FROM measurements WHERE device_id = ? AND sequence_number = ?",
                (device_id, sequence_number),
            ).fetchone()
            return None if row is None else _stored(row)

    def list(self, limit: int = 100, *, device_id: str | None = None) -> list[StoredMeasurement]:
        """Return at most limit records, in stable insertion order."""
        if type(limit) is not int or limit <= 0:
            raise ValueError("limit must be a positive integer")
        with self._database.transaction() as connection:
            if device_id is None:
                rows = connection.execute("SELECT * FROM measurements ORDER BY rowid LIMIT ?", (limit,)).fetchall()
            else:
                rows = connection.execute(
                    "SELECT * FROM measurements WHERE device_id = ? ORDER BY rowid LIMIT ?",
                    (device_id, limit),
                ).fetchall()
            return [_stored(row) for row in rows]
