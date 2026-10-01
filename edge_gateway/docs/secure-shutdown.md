# Gateway secure shutdown

Member 2 owns application lifecycle, including Ctrl+C, SIGTERM, and Docker stop. Member 3 owns the security cleanup that runs when a secure transport is attached.

The lifespan first marks the Gateway as not running. It then calls `SecureTransport.shutdown` when `app.state.secure_transport` is set. That method follows section 53 of `docs/architecture/02 - Edge Gateway.md`:

1. Stop accepting secure work.
2. Close the HTTP client and drop it.
3. Clear the active session reference. `clear` overwrites the session-key buffer.

Shutdown does not log key material. A later secure send fails closed and does not call the baseline endpoint. A second shutdown call does nothing.

M3-56 lists the HTTP client close after the session is cleared. Section 53 and Member 2 task M2-37 close the client first. This cleanup follows section 53.

Python does not guarantee secure memory zeroization. Closing the client and clearing the session reference does not prove that every copy of the key has left process memory.
