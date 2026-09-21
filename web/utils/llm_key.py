"""#1185 — shared per-user LLM key resolution for user-facing LLM routes.

`/intent` resolved the caller's stored Anthropic key inline (#1185 Phase 1). Other
user-facing LLM routes (e.g. the `/documents` analyze/question/summarize/compare/
reference endpoints) invoked the LLM WITHOUT resolving the caller's key — so a hosted
user's document analysis silently used the *server* key, not theirs (#1185 Phase 2).

This helper is the shared resolver: it wraps `resolve_request_api_key`
(services/llm/request_key.py) with the DB-backed stored-key fetcher, so any route can
resolve the caller's key (header > stored > refuse) and bind it via
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

#1812 step 5 (2026-09-21): `is_designated_operator` — the one place that supplied the
operator-principal check to the resolver — is DELETED with the operator seam itself.
Resolution is header > stored > honest refusal, for every principal including PM
(normal-account ruling, decisions.log 2026-09-19). These resolvers return a key or
raise; they never return ``None``.
"""

from __future__ import annotations

from typing import Dict, Optional

import structlog

from services.llm.request_key import resolve_request_api_key

logger = structlog.get_logger(__name__)


async def resolve_user_llm_key(header_key: Optional[str], user_id: Optional[str]) -> str:
    """Resolve the per-request Anthropic key for a user-facing route (header > stored,
    else refuse — #1185/#1807/#1812).

    Args:
        header_key: the ``X-User-Api-Key`` header value if present (Desktop BYOC), else
            None. Hosted-web routes pass None (the browser never sends it).
        user_id: the authenticated user's id — pass ``current_user.sub`` (the string
            form the stored key is keyed under, consistent with /intent).

    Returns the resolved key — always the acting user's own. Feed it to
    ``request_api_key(...)`` at the call site.

    Raises:
        UserLLMKeyRequiredError: authenticated, no key of their own.
        AnonymousLLMKeyRequiredError: no login and no header key (#1320).
    """

    async def _fetch_stored(uid: str) -> Optional[str]:
        # Injected DB-backed fetcher — the only DB touch; opens a scoped session.
        from services.database.session_factory import AsyncSessionFactory
        from services.security.user_api_key_service import UserAPIKeyService

        async with AsyncSessionFactory.session_scope() as session:
            return await UserAPIKeyService().retrieve_user_key(session, uid, "anthropic")

    return await resolve_request_api_key(header_key, user_id, _fetch_stored)


async def _fetch_stored_provider_key(user_id: str, provider: str) -> Optional[str]:
    """DB-backed stored-key fetch for one provider row (#1819).

    ``session_scope_fresh`` (not ``session_scope``): a per-call engine bound to the
    running loop — the #1802 lesson.
    """
    from services.database.session_factory import AsyncSessionFactory
    from services.security.user_api_key_service import UserAPIKeyService

    async with AsyncSessionFactory.session_scope_fresh() as session:
        return await UserAPIKeyService().retrieve_user_key(session, user_id, provider)


async def expand_llm_key_binding(resolved: str, user_id: Optional[str]) -> Dict[str, str]:
    """Expand a resolved Anthropic key into the provider-keyed binding (#1819).

    ``resolved`` is the output of ``resolve_request_api_key`` / ``resolve_user_llm_key``
    (so the #1807/#1320 refusal rungs have ALREADY run — this function never decides
    entitlement, it only widens a granted one): ``{"anthropic": key}``, plus the
    user's OWN stored OpenAI key when one exists — so provider selection (#1415) can
    route their turn to OpenAI and the leg spends THEIR key, not a refusal. A fetch
    failure degrades to fewer bound providers (fail-closed for spend: the OpenAI leg
    refuses), never to a wider binding.

    #1812 step 5: ``resolved`` is required (the resolvers never return ``None`` any
    more — the operator seam that produced one is deleted). An empty value raises
    rather than silently re-encoding "bind nothing that spends as someone else".

    Gemini is deliberately not fetched: ``_gemini_complete`` has no per-request client
    path (see clients.py, #1819) and setup stores no Gemini rows — fetching one would
    be plumbing to a leg that refuses it.
    """
    if not resolved:
        raise ValueError(
            "expand_llm_key_binding requires a resolved key: the resolvers refuse "
            "instead of returning None since #1812 step 5, so an empty value here "
            "means a caller skipped resolution."
        )
    binding: Dict[str, str] = {"anthropic": resolved}
    if user_id:
        try:
            openai_key = await _fetch_stored_provider_key(user_id, "openai")
        except Exception as e:  # silent-ok: fewer providers bound = fail-closed for spend
            logger.warning("stored_openai_key_fetch_failed_1819", error=str(e))
            openai_key = None
        if openai_key:
            binding["openai"] = openai_key
    return binding


async def resolve_user_openai_key(user_id: Optional[str]) -> str:
    """Resolve the per-request OPENAI key for a route whose spend is an OpenAI
    credential (#1819 — today: the KG embedding search surface).

    Same rungs as ``resolve_user_llm_key``, same refusal semantics (#1807/#1320),
    different provider row: the user's own stored OpenAI key, else refuse. There is
    no header rung — ``X-User-Api-Key`` is an Anthropic key by construction
    (``REQUEST_KEY_PROVIDER``).

    Returns the key — always the acting user's own. Feed it to
    ``request_api_key({"openai": key})`` at the call site.

    Raises:
        UserLLMKeyRequiredError: authenticated, no OpenAI key of their own.
        AnonymousLLMKeyRequiredError: no authenticated user (#1320).
    """

    async def _fetch_stored(uid: str) -> Optional[str]:
        return await _fetch_stored_provider_key(uid, "openai")

    return await resolve_request_api_key(None, user_id, _fetch_stored)
