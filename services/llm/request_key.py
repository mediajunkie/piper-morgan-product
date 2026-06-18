"""#1162 BYOC credential decoupling — per-request, user-supplied LLM API key.

A hosted-BYOC user supplies their OWN Anthropic key (Claude Desktop env →
``X-User-Api-Key`` header on the request to ``/api/v1/intent``). The route binds it
into a request-scoped ``ContextVar``; the LLM client uses it for *that request's*
Anthropic calls instead of the server's configured key, falling back to the server
key when absent (PM's own use / unauthenticated path).

Why this unblocks distribution (#1162): with users paying for their own LLM calls,
the hosted server no longer has to authenticate them to use it — the static
bearer-token gate (the thing 401-ing external testers) can come off.

Security properties (this is credential handling — keep them):
- The key lives ONLY in the ContextVar for the request's duration and is **reset in
  a finally** (`request_api_key` context manager) → it never outlives the request.
- ContextVars are per-asyncio-task, so concurrent requests can't leak keys to each
  other (each request is its own task).
- The key is **never logged** and **never persisted** — it transits in the header
  (HTTPS at the edge) and is used in-memory for the one call.
- A blank/empty header binds nothing → the server's configured key is used.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from typing import Any, Iterator, Optional

# Default None = "no per-request key bound; use the server's configured key".
_user_api_key: ContextVar[Optional[str]] = ContextVar("user_api_key", default=None)


def get_request_api_key() -> Optional[str]:
    """The current request's user-supplied API key, or None (→ use the server key)."""
    return _user_api_key.get()


@contextlib.contextmanager
def request_api_key(key: Optional[str]) -> Iterator[None]:
    """Bind a per-request user API key for the duration of the block, then reset.

    A blank/None key binds None (falls back to the server key). The reset in the
    ``finally`` guarantees the key never outlives the request — no cross-request leak.
    """
    token = _user_api_key.set(key or None)
    try:
        yield
    finally:
        _user_api_key.reset(token)


def anthropic_client_for_request(server_client: Any) -> Any:
    """Return the Anthropic client to use for the current request.

    If the request bound a user-supplied key (BYOC), return a fresh client keyed to
    it; otherwise return the server's configured client. Kept tiny + pure so it's
    unit-testable without standing up the full LLM client.
    """
    user_key = get_request_api_key()
    if user_key:
        from anthropic import Anthropic

        return Anthropic(api_key=user_key)
    return server_client
