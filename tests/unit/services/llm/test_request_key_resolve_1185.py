"""#1185 BYO-KEY: resolve the per-request LLM key.

Priority: header (Claude Desktop BYOC) > stored (hosted web, by authenticated
user_id) > the designated operator principal, else refuse. The resolver is **pure** —
the DB-backed stored-key fetch and the operator check are both injected, so this
unit-tests without a database. The route (/api/v1/intent) wires the real fetch
(UserAPIKeyService.retrieve_user_key).

⚠️ AMENDED 2026-09-14 (#1807): the third rung used to be "None (→ server key fallback)"
for any authenticated caller. It is now the designated-operator path, default OFF, and
everyone else is refused — see tests/unit/services/llm/test_operator_server_key_1807.py.
"""

import pytest

from services.llm.request_key import resolve_request_api_key


async def _fetch_none(user_id):
    return None


async def _fetch_key(user_id):
    return f"sk-stored-{user_id}"


async def _fetch_boom(user_id):
    raise AssertionError("fetch_stored must not be called in this case")


@pytest.mark.asyncio
async def test_header_wins_without_touching_db():
    """Desktop BYOC: an explicit per-request header key always wins; no DB fetch."""
    assert await resolve_request_api_key("sk-header", "u1", _fetch_boom) == "sk-header"


@pytest.mark.asyncio
async def test_no_header_resolves_stored_by_user_id():
    """Hosted web: no header + authenticated user → that user's stored key."""
    assert await resolve_request_api_key(None, "u1", _fetch_key) == "sk-stored-u1"


@pytest.mark.asyncio
async def test_no_header_no_stored_is_refused_1807():
    """AMENDED by #1807. Was `is None` — the server-key fallback. An authenticated user
    with no key of their own is now refused, because a login is not authorization to
    spend the operator's money. The honest degrade happens at the route, which turns
    this into "add your LLM key"."""
    from services.llm.request_key import UserLLMKeyRequiredError

    with pytest.raises(UserLLMKeyRequiredError):
        await resolve_request_api_key(None, "u1", _fetch_none)


@pytest.mark.asyncio
async def test_no_user_id_skips_fetch():
    """Unauthenticated + no header → refused (#1320), and the DB fetch is never
    attempted. Was `is None` (silent server-key fallback) before #1320 — that
    codified the anonymous-billing gap; see test_request_key_anonymous_gate_1320.py."""
    from services.llm.request_key import AnonymousLLMKeyRequiredError

    with pytest.raises(AnonymousLLMKeyRequiredError):
        await resolve_request_api_key(None, None, _fetch_boom)


@pytest.mark.asyncio
async def test_blank_header_falls_through_to_stored():
    """A blank X-User-Api-Key header is 'absent' → fall back to the stored key."""
    assert await resolve_request_api_key("", "u1", _fetch_key) == "sk-stored-u1"


@pytest.mark.asyncio
async def test_resolved_stored_key_flows_through_the_rail_to_the_client():
    """Wiring (no internal mock): resolver(stored) → request_api_key ContextVar →
    anthropic_client_for_request returns a FRESH client keyed to the stored key —
    proving #1185's stored-key path rides the same #1162 rail end-to-end."""
    from services.llm.request_key import anthropic_client_for_request, request_api_key

    server_client = object()  # sentinel for the server's configured client
    key = await resolve_request_api_key(None, "u1", _fetch_key)  # → sk-stored-u1
    with request_api_key(key):
        client = anthropic_client_for_request(server_client)
        assert client is not server_client
        assert getattr(client, "api_key", None) == "sk-stored-u1"
    # after the block: ContextVar reset → back to the server client (no leak)
    assert anthropic_client_for_request(server_client) is server_client
