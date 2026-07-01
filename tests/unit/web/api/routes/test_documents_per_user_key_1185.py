"""#1185 Phase 2 — /documents LLM routes bind the caller's per-user Anthropic key.

Before: the analyze/question/summarize/compare/reference routes invoked the LLM WITHOUT
resolving the caller's stored key → a hosted user's document analysis silently used the
SERVER key, not theirs. Now each resolves + binds via `with request_api_key(...)`.

SECURITY-CRITICAL tests (the failure mode is one user's key leaking into another's
request): the rail must be bound DURING the LLM call, and RESET after (no cross-request
leak) — the reset-in-finally guarantee of `request_api_key`.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.llm.request_key import get_request_api_key
from web.utils.llm_key import resolve_user_llm_key

pytestmark = pytest.mark.asyncio

_U = "user-1"


def _mock_session_factory():
    session = AsyncMock()
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=session)
    scope.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock()
    factory.session_scope.return_value = scope
    return factory


# ---- resolve_user_llm_key (the shared resolver) ----

async def test_resolves_stored_key_when_no_header():
    svc = MagicMock()
    svc.retrieve_user_key = AsyncMock(return_value="stored-key")
    with (
        patch("services.database.session_factory.AsyncSessionFactory", _mock_session_factory()),
        patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc),
    ):
        got = await resolve_user_llm_key(None, _U)
    assert got == "stored-key"
    args, _ = svc.retrieve_user_key.call_args
    assert args[1] == _U and args[2] == "anthropic"


async def test_header_wins_and_db_not_touched():
    svc = MagicMock()
    svc.retrieve_user_key = AsyncMock()
    with patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc):
        got = await resolve_user_llm_key("hdr-key", _U)
    assert got == "hdr-key"
    svc.retrieve_user_key.assert_not_awaited()  # explicit per-call key → DB never read


async def test_none_when_no_header_and_no_stored():
    svc = MagicMock()
    svc.retrieve_user_key = AsyncMock(return_value=None)
    with (
        patch("services.database.session_factory.AsyncSessionFactory", _mock_session_factory()),
        patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc),
    ):
        got = await resolve_user_llm_key(None, _U)
    assert got is None  # → LLM client falls back to the server key


# ---- /documents endpoint: rail bound during the call + reset after (SECURITY) ----

async def test_analyze_binds_user_key_during_call_and_resets_after_1185():
    from web.api.routes import documents

    captured = {}

    async def _spy_handler(**kwargs):
        captured["key_during_call"] = get_request_api_key()
        return {"summary": "s", "key_findings": []}

    mock_user = MagicMock()
    mock_user.sub = _U
    mock_user.user_id = "uuid-1"

    assert get_request_api_key() is None  # clean baseline
    with (
        patch.object(documents, "resolve_user_llm_key", AsyncMock(return_value="kUSER")),
        patch.object(documents, "handle_analyze_document", _spy_handler),
    ):
        result = await documents.analyze_document(file_id="f1", current_user=mock_user)

    assert result["summary"] == "s"
    # the user's key was bound WHILE the LLM handler ran
    assert captured["key_during_call"] == "kUSER"
    # and reset afterwards — no cross-request leak
    assert get_request_api_key() is None


async def test_no_cross_request_leak_between_users_1185():
    """User A (has a key) then user B (no key): B's call must NOT see A's key."""
    from web.api.routes import documents

    seen = {}

    def _make_spy(tag):
        async def _spy(**kwargs):
            seen[tag] = get_request_api_key()
            return {"summary": "s", "key_findings": []}
        return _spy

    user_a = MagicMock(); user_a.sub = "A"; user_a.user_id = "ua"
    user_b = MagicMock(); user_b.sub = "B"; user_b.user_id = "ub"

    # User A → resolves "kA"
    with (
        patch.object(documents, "resolve_user_llm_key", AsyncMock(return_value="kA")),
        patch.object(documents, "handle_analyze_document", _make_spy("A")),
    ):
        await documents.analyze_document(file_id="f", current_user=user_a)

    # User B → resolves None (no stored key)
    with (
        patch.object(documents, "resolve_user_llm_key", AsyncMock(return_value=None)),
        patch.object(documents, "handle_analyze_document", _make_spy("B")),
    ):
        await documents.analyze_document(file_id="f", current_user=user_b)

    assert seen["A"] == "kA"
    assert seen["B"] is None  # NOT "kA" — no leak from A's request into B's
    assert get_request_api_key() is None
