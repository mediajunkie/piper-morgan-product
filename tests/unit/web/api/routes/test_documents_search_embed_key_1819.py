"""#1819 — /api/v1/documents/search binds the caller's OWN OpenAI key for the embedding spend.

Semantic search EMBEDS the query via OpenAI — a billable spend this route used to make
on a server-owned keychain key with no key resolution at all (the only one of the six
document routes with none). It now resolves stored-openai > refuse (#1807's rung
structure with the provider row the spend actually needs; #1812 step 5 deleted the
designated-operator rung this file used to pin) and binds it
for the handler's duration, same reset-in-finally rail as the five LLM-calling routes
(#1185).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from services.llm.request_key import (
    UserLLMKeyRequiredError,
    get_request_api_key,
    request_api_key,
)

pytestmark = pytest.mark.asyncio

_U = "user-1"


def _user() -> MagicMock:
    mock_user = MagicMock()
    mock_user.sub = _U
    mock_user.user_id = "uuid-1"
    return mock_user


async def test_search_binds_the_users_openai_key_during_the_call_and_resets_after():
    from web.api.routes import documents

    captured = {}

    async def _spy_handler(**kwargs):
        captured["openai_key_during_call"] = get_request_api_key("openai")
        captured["anthropic_key_during_call"] = get_request_api_key("anthropic")
        return {"results": [], "count": 0}

    assert get_request_api_key("openai") is None  # clean baseline
    with (
        patch.object(documents, "resolve_user_openai_key", AsyncMock(return_value="kOPENAI")),
        patch.object(documents, "handle_search_documents", _spy_handler),
    ):
        result = await documents.search_documents(q="pricing", current_user=_user())

    assert result["count"] == 0
    # the user's OpenAI key was bound WHILE the embedding-spending handler ran…
    assert captured["openai_key_during_call"] == "kOPENAI"
    # …under its own provider only (no invented anthropic entitlement)…
    assert captured["anthropic_key_during_call"] is None
    # …and reset afterwards — no cross-request leak
    assert get_request_api_key("openai") is None


async def test_search_refuses_a_keyless_caller_with_the_openai_specific_403():
    from web.api.routes import documents

    handler = AsyncMock()
    with (
        patch.object(
            documents,
            "resolve_user_openai_key",
            AsyncMock(side_effect=UserLLMKeyRequiredError("no openai key")),
        ),
        patch.object(documents, "handle_search_documents", handler),
    ):
        with pytest.raises(HTTPException) as exc_info:
            await documents.search_documents(q="pricing", current_user=_user())

    assert exc_info.value.status_code == 403
    assert "OpenAI" in exc_info.value.detail  # honest about WHICH key is needed
    handler.assert_not_awaited()  # refused BEFORE any embedding spend


async def test_search_surfaces_an_embed_layer_refusal_as_403_not_500():
    """If the refusal fires at the spend itself (a deeper layer re-deciding
    entitlement), the route answers honestly instead of masking it as a server
    error."""
    from services.llm.request_key import UnboundLLMKeyError
    from web.api.routes import documents

    async def _refusing_handler(**kwargs):
        raise UnboundLLMKeyError("no spendable key")

    with (
        patch.object(documents, "resolve_user_openai_key", AsyncMock(return_value="kOPENAI")),
        patch.object(documents, "handle_search_documents", _refusing_handler),
    ):
        with pytest.raises(HTTPException) as exc_info:
            await documents.search_documents(q="pricing", current_user=_user())

    assert exc_info.value.status_code == 403


async def test_resolve_user_openai_key_reads_the_openai_row():
    """The shared-resolver rungs run against the provider row the spend needs."""
    from web.utils.llm_key import resolve_user_openai_key

    svc = MagicMock()
    svc.retrieve_user_key = AsyncMock(return_value="stored-openai-key")
    session = AsyncMock()
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=session)
    scope.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock()
    factory.session_scope_fresh.return_value = scope
    with (
        patch("services.database.session_factory.AsyncSessionFactory", factory),
        patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc),
    ):
        got = await resolve_user_openai_key(_U)
    assert got == "stored-openai-key"
    args, _ = svc.retrieve_user_key.call_args
    assert args[1] == _U and args[2] == "openai"


async def test_expand_llm_key_binding_carries_the_stored_openai_key_alongside():
    """#1819 — the /intent and /documents LLM routes widen a granted anthropic
    resolution into the provider-keyed binding; the openai row rides along."""
    from web.utils import llm_key as llm_key_module

    with patch.object(
        llm_key_module,
        "_fetch_stored_provider_key",
        AsyncMock(return_value="stored-openai-key"),
    ):
        binding = await llm_key_module.expand_llm_key_binding("kANTHROPIC", _U)
    assert binding == {"anthropic": "kANTHROPIC", "openai": "stored-openai-key"}


async def test_expand_llm_key_binding_requires_a_resolved_key():
    """#1812 step 5: the None passthrough (the operator grant, verbatim) is deleted —
    an empty 'resolved' now raises, because nothing legitimately produces one."""
    from web.utils.llm_key import expand_llm_key_binding

    with pytest.raises(ValueError, match="1812"):
        await expand_llm_key_binding(None, _U)


async def test_expand_llm_key_binding_fetch_failure_is_fail_closed():
    """A stored-key fetch failure binds FEWER providers (the openai leg refuses),
    never more."""
    from web.utils import llm_key as llm_key_module

    with patch.object(
        llm_key_module,
        "_fetch_stored_provider_key",
        AsyncMock(side_effect=RuntimeError("db down")),
    ):
        binding = await llm_key_module.expand_llm_key_binding("kANTHROPIC", _U)
    assert binding == {"anthropic": "kANTHROPIC"}
