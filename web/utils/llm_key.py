"""#1185 — shared per-user LLM key resolution for user-facing LLM routes.

`/intent` resolved the caller's stored Anthropic key inline (#1185 Phase 1). Other
user-facing LLM routes (e.g. the `/documents` analyze/question/summarize/compare/
reference endpoints) invoked the LLM WITHOUT resolving the caller's key — so a hosted
user's document analysis silently used the *server* key, not theirs (#1185 Phase 2).

This helper is the shared resolver: it wraps `resolve_request_api_key`
(services/llm/request_key.py) with the DB-backed stored-key fetcher, so any route can
resolve the caller's key (header > stored > None) and bind it via
`with request_api_key(resolved): ...`.

It lives in the web layer (NOT in request_key.py) on purpose: request_key.py stays
DB-free — its `fetch_stored` is deliberately injected so it's unit-testable without a
database. This helper is the one place that injects the real DB-backed fetcher.

Security (this is credential handling — keep it):
- The resolved key is bound ONLY inside the caller's `with request_api_key(...)` block
  — a per-asyncio-task ContextVar, reset in a `finally`, so it never outlives the
  request and cannot leak across concurrent requests.
- The key is never logged here. Lookup is by the authenticated user's id (pass
  `current_user.sub` — the string form the key is stored under, matching /intent).
"""

from __future__ import annotations

from typing import Optional

from services.llm.request_key import resolve_request_api_key


async def resolve_user_llm_key(
    header_key: Optional[str], user_id: Optional[str]
) -> Optional[str]:
    """Resolve the per-request Anthropic key for a user-facing route (header > stored > None).

    Args:
        header_key: the ``X-User-Api-Key`` header value if present (Desktop BYOC), else
            None. Hosted-web routes pass None (the browser never sends it).
        user_id: the authenticated user's id — pass ``current_user.sub`` (the string
            form the stored key is keyed under, consistent with /intent).

    Returns the resolved key (or None → the LLM client falls back to the server key).
    Feed it to ``request_api_key(...)`` at the call site.
    """

    async def _fetch_stored(uid: str) -> Optional[str]:
        # Injected DB-backed fetcher — the only DB touch; opens a scoped session.
        from services.database.session_factory import AsyncSessionFactory
        from services.security.user_api_key_service import UserAPIKeyService

        async with AsyncSessionFactory.session_scope() as session:
            return await UserAPIKeyService().retrieve_user_key(session, uid, "anthropic")

    return await resolve_request_api_key(header_key, user_id, _fetch_stored)
