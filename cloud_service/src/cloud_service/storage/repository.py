"""Parameterized SQLite operations, independent of HTTP and crypto."""

from datetime import datetime
import sqlite3

from cloud_service.models import CanonicalMeasurement
from cloud_service.storage.database import Database, StorageError
from cloud_service.storage.models import StoredMeasurement


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
            connection.execute(
                """INSERT INTO measurements
                (record_id, device_id, gateway_id, temperature_c, humidity_pct,
                 measured_at, gateway_received_at, cloud_received_at, sequence_number)
                VALUES (:record_id, :device_id, :gateway_id, :temperature_c, :humidity_pct,
                        :measured_at, :gateway_received_at, :cloud_received_at, :sequence_number)""",
                values,
            )
        return stored

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
