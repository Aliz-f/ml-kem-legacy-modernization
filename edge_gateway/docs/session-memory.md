# Gateway session memory

The Gateway session key stays in process memory only. The manager holds at most one session object. That object keeps the key in a `bytearray`.

The key is not written to a debug dump, a cache file, SQLite, JSON state, or AI history. Tests do not save snapshots that contain real key bytes.

When a session is replaced, the old session object is cleared and dereferenced. `clear` overwrites the session-key buffer, and the manager then drops its reference. Expiry, invalidation, close, and a new handshake all use that order. A handshake that finds a session still held clears it before the new session is stored.

Python does not guarantee secure memory zeroization. Overwriting the session-key buffer does not remove every copy. The ML-KEM shared secret and the HKDF output are immutable `bytes`, and encryption uses a copy of the session key. Those copies remain until the process releases them.

The frozen statement is section 17 of `docs/architecture/02 - Edge Gateway.md`.
