"""#1320: the server-key fallback must never apply to a fully anonymous caller.

Discovered 2026-07-01: the Caddy edge gate that made the anonymous→server-key
fallback safe was removed 2026-06-29, but the paired server-side change flagged in
the 2026-06-17 memo (mailboxes/pa/read/memo-lead-to-pa-cc-pm-caddy-gate-issue-
explainer-plus-fallback-security-interaction-2026-06-17.md) hadn't shipped — so
`/api/v1/intent` (the only route with optional auth reaching this resolver;
`/documents/*` all require auth via `Depends(get_current_user)`, never anonymous)
could silently bill the server's own Anthropic key to any unauthenticated caller
with no key. These pin the fix: authenticated callers are unaffected; only the
fully-anonymous+keyless case is gated.
"""

import pytest

from services.llm.request_key import AnonymousLLMKeyRequiredError, resolve_request_api_key


async def _fetch_none(user_id):
    return None


async def _fetch_key(user_id):
    return f"sk-stored-{user_id}"


async def _fetch_boom(user_id):
    raise AssertionError("fetch_stored must not be called for an anonymous caller")


@pytest.mark.asyncio
async def test_anonymous_no_header_is_refused_not_server_fallback():
    """The vulnerability: unauthenticated + no header must REFUSE, never silently
    resolve to None (→ server key)."""
    with pytest.raises(AnonymousLLMKeyRequiredError):
        await resolve_request_api_key(None, None, _fetch_boom)


@pytest.mark.asyncio
async def test_anonymous_blank_header_is_also_refused():
    """A blank header is 'absent', same as no header — still refused when anonymous."""
    with pytest.raises(AnonymousLLMKeyRequiredError):
        await resolve_request_api_key("", None, _fetch_boom)


@pytest.mark.asyncio
async def test_anonymous_with_header_key_still_works_byoc_preserved():
    """The whole point of #1162 (BYOC needs no login) must be UNCHANGED: an
    anonymous caller who brings their own key is fine — never refused."""
    assert await resolve_request_api_key("sk-byoc", None, _fetch_boom) == "sk-byoc"


@pytest.mark.asyncio
async def test_authenticated_no_stored_key_still_falls_back_to_server_pms_own_use():
    """The 'PM's own use' path must be UNCHANGED: authenticated + no header + no
    stored key → None (server-key fallback), not refused. Only anonymous is gated."""
    assert await resolve_request_api_key(None, "u1", _fetch_none) is None


@pytest.mark.asyncio
async def test_authenticated_stored_key_still_resolves_unchanged():
    assert await resolve_request_api_key(None, "u1", _fetch_key) == "sk-stored-u1"


@pytest.mark.asyncio
async def test_authenticated_no_fetch_stored_provided_still_falls_back_not_refused():
    """user_id present but no fetch_stored callable injected (defensive edge) →
    still the authenticated server-fallback path, not the anonymous refusal."""
    assert await resolve_request_api_key(None, "u1", None) is None
