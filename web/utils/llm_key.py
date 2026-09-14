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

#1807 addendum: this helper is also the one place that supplies the *operator-principal*
check to the resolver. `request_key.py` stays DB-free and refuses when no checker is
injected, so wiring it here is what makes the single remaining server-key path possible —
and keeps every other caller fail-closed. The middle rung of the old resolution order
("any authenticated user → the server's key") is gone.
"""

from __future__ import annotations

import uuid
from typing import Optional

import structlog

from services.llm.request_key import operator_server_key_opted_in, resolve_request_api_key

logger = structlog.get_logger(__name__)


async def is_designated_operator(user_id: str) -> bool:
    """True only for the explicitly designated operator principal, and only when the
    operator has opted in to spending their own key (#1807).

    Two independent gates, both default-OFF, in cheap-to-expensive order:
      1. ``PIPER_OPERATOR_SERVER_KEY`` opted in. Absent ⇒ False immediately, with **no
         database touch at all** — so the hosted default costs nothing and cannot be
         flipped on by unrelated configuration.
      2. The caller IS the configured PM/operator principal. Resolved through the
         EXISTING convention rather than a new one: ``resolve_pm_owner_id`` (env
         ``PIPER_PM_USER_ID`` → the "PM Identity" section of ``config/PIPER.user.md``;
         #1260, ADR-071 D7, which already names the evolution from "the configured PM"
         to "this tenant's principal").

    Why identity is not sufficient on its own: ``PIPER_PM_USER_ID`` exists today to mark
    *document provenance*. If it also granted spending authority, any deployment that
    named its PM for ingest would silently acquire a billable server-key path. Gate 1
    keeps the two meanings separate.

    Fail-closed: any resolution error returns False (refuse), never True.
    """
    if not operator_server_key_opted_in():
        return False

    try:
        caller = uuid.UUID(str(user_id))
    except (ValueError, TypeError, AttributeError):
        return False

    try:
        from services.database.session_factory import AsyncSessionFactory
        from services.repositories.document_repository import resolve_pm_owner_id

        # session_scope_fresh (not session_scope): a per-call engine bound to the
        # running loop — the #1802 lesson about the global singleton's loop binding.
        async with AsyncSessionFactory.session_scope_fresh() as session:
            operator = await resolve_pm_owner_id(session)
    except Exception as e:
        logger.warning("operator_principal_check_unavailable_1807", error=str(e))
        return False

    if operator is None:
        return False
    allowed = operator == caller
    if allowed:
        # The operator spending their own key is a billable event with a named actor.
        logger.info("operator_server_key_used_1807", user_id=str(user_id))
    return allowed


async def resolve_user_llm_key(header_key: Optional[str], user_id: Optional[str]) -> Optional[str]:
    """Resolve the per-request Anthropic key for a user-facing route (header > stored >
    designated operator, else refuse — #1185/#1807).

    Args:
        header_key: the ``X-User-Api-Key`` header value if present (Desktop BYOC), else
            None. Hosted-web routes pass None (the browser never sends it).
        user_id: the authenticated user's id — pass ``current_user.sub`` (the string
            form the stored key is keyed under, consistent with /intent).

    Returns the resolved key, or None *only* for the designated operator (→ the LLM
    client uses the server key). Feed it to ``request_api_key(...)`` at the call site.

    Raises:
        UserLLMKeyRequiredError: authenticated, no key of their own, not the operator.
        AnonymousLLMKeyRequiredError: no login and no header key (#1320).
    """

    async def _fetch_stored(uid: str) -> Optional[str]:
        # Injected DB-backed fetcher — the only DB touch; opens a scoped session.
        from services.database.session_factory import AsyncSessionFactory
        from services.security.user_api_key_service import UserAPIKeyService

        async with AsyncSessionFactory.session_scope() as session:
            return await UserAPIKeyService().retrieve_user_key(session, uid, "anthropic")

    return await resolve_request_api_key(header_key, user_id, _fetch_stored, is_designated_operator)
