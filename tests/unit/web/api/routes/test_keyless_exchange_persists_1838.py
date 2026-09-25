"""#1838: a signed-in, keyless first turn must not vanish.

PM's live failure (2026-09-20): keyless on first run, typed a message, got the
(correct) "add your key" refusal, went to Settings, added the key, came back —
and the chat they had just started was not findable.

Mechanism (traced in web/api/routes/intent.py): the #731 auto-create block
creates the ``ConversationDB`` row BEFORE the #1807
``UserLLMKeyRequiredError`` gate returns — but the gate returns before
``intent_service.process_intent`` ever runs, and turn persistence
(``conv_ctx.add_turn`` / ``ConversationRepository.save_turn``) lives inside
that service path. So the refused exchange (the user's message + Piper's
refusal) was never saved. On return, the sidebar shows an empty "New
conversation" row, and ``/api/v1/conversations/{id}/turns`` returns nothing —
reading as "my chat is gone".

Contract pinned here:
- a signed-in, keyless turn persists ONE ``ConversationTurn`` row (via
  ``ConversationRepository.save_turn`` — the SAME repository call the normal
  turn-persistence path uses) carrying both the user's message and Piper's
  refusal, in order, turn_number 1.
- persistence failure never changes the refusal response returned to the
  caller (best-effort, mirrors the #731 block's own try/except).
- the genuinely anonymous (#1320) path persists NOTHING — there is no
  authenticated owner to attach a conversation row to.

Layer note: like the neighbouring #1532/#1520 route tests, this file mocks
the DB entirely (``AsyncSessionFactory.session_scope_fresh`` + the
``ConversationRepository`` methods it calls) rather than hitting a real
database — assertions are made at the REPOSITORY-CALL layer
(``ConversationRepository.save_turn`` invocation and its arguments), not by
reading back through a live ``/turns`` endpoint.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

import web.api.routes.intent as intent_route
from services.database import repositories as repos_module
from services.database import session_factory as sf
from services.llm.request_key import AnonymousLLMKeyRequiredError, UserLLMKeyRequiredError
from web.api.routes.intent import process_intent

USER_ID = str(uuid4())


def _claims(sub):
    return SimpleNamespace(
        sub=sub,
        workspace_id=None,
        user_email="user@example.com",
        session_id=None,
    )


def _mock_request(session_id, message="hello there"):
    req = MagicMock()
    req.json = AsyncMock(return_value={"message": message, "session_id": session_id})
    req.headers = MagicMock()
    req.headers.get = MagicMock(return_value=None)
    req.cookies = {}
    req.state = SimpleNamespace()
    req.app.state.intent_service = MagicMock()
    req.app.state.intent_service.process_intent = AsyncMock()
    return req


@pytest.fixture
def fresh_session_factory(monkeypatch):
    """Patch session_scope_fresh (used by BOTH the #731 auto-create block and
    the new #1838 persistence call) with a fake session that answers the
    #731 block's existence check as "no row yet" so conversation auto-create
    runs. ConversationRepository's own methods are patched separately below,
    so this fake session is never asked to do real SQL for the turn save."""
    session = MagicMock()
    session.get = AsyncMock(return_value=None)
    session.add = MagicMock()
    session.commit = AsyncMock()
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=session)
    cm.__aexit__ = AsyncMock(return_value=None)
    monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope_fresh", lambda: cm)
    return session


@pytest.fixture
def keyless_gate(monkeypatch):
    """Force the #1807 signed-in-but-keyless gate."""
    monkeypatch.setattr(
        intent_route,
        "resolve_user_llm_binding",
        AsyncMock(side_effect=UserLLMKeyRequiredError()),
    )


@pytest.mark.asyncio
async def test_keyless_signed_in_turn_persists_both_messages_in_order(
    fresh_session_factory, keyless_gate, monkeypatch
):
    save_calls = []

    async def _fake_get_next_turn_number(self, conversation_id, is_admin=False):
        return 1

    async def _fake_save_turn(self, turn, is_admin=False, user_id=None):
        save_calls.append((turn, user_id))

    monkeypatch.setattr(
        repos_module.ConversationRepository, "get_next_turn_number", _fake_get_next_turn_number
    )
    monkeypatch.setattr(repos_module.ConversationRepository, "save_turn", _fake_save_turn)

    session_id = str(uuid4())
    req = _mock_request(session_id, message="hello there")

    result = await process_intent(req, current_user=_claims(USER_ID))

    # The refusal itself is unaffected — never reaches intent_service/the LLM.
    assert result["error_type"] == "user_key_required"
    req.app.state.intent_service.process_intent.assert_not_called()

    # The refused exchange was persisted as one turn, both messages in order.
    assert len(save_calls) == 1
    turn, saved_user_id = save_calls[0]
    assert saved_user_id == USER_ID
    assert turn.conversation_id == session_id
    assert turn.turn_number == 1
    assert turn.user_message == "hello there"
    assert turn.assistant_response == result["message"]
    assert turn.assistant_response  # the refusal copy, non-empty


@pytest.mark.asyncio
async def test_persistence_failure_does_not_change_refusal_response(
    fresh_session_factory, keyless_gate, monkeypatch
):
    async def _boom(self, conversation_id, is_admin=False):
        raise RuntimeError("db unavailable")

    monkeypatch.setattr(repos_module.ConversationRepository, "get_next_turn_number", _boom)

    session_id = str(uuid4())
    req = _mock_request(session_id, message="hello there")

    result = await process_intent(req, current_user=_claims(USER_ID))

    # Same refusal shape as the happy path — persistence failure is invisible
    # to the caller.
    assert result["error_type"] == "user_key_required"
    assert result["requires_clarification"] is True
    assert "message" in result and result["message"]
    req.app.state.intent_service.process_intent.assert_not_called()


@pytest.mark.asyncio
async def test_anonymous_path_persists_nothing(monkeypatch):
    """#1320 unchanged: no authenticated user → no conversation row to attach
    a turn to, and no attempt is made to persist one."""
    save_turn_mock = AsyncMock()
    monkeypatch.setattr(repos_module.ConversationRepository, "save_turn", save_turn_mock)
    monkeypatch.setattr(
        intent_route,
        "resolve_user_llm_binding",
        AsyncMock(side_effect=AnonymousLLMKeyRequiredError()),
    )

    req = _mock_request(str(uuid4()), message="hello there")

    result = await process_intent(req, current_user=None)

    assert result["error_type"] == "anonymous_key_required"
    save_turn_mock.assert_not_called()
    req.app.state.intent_service.process_intent.assert_not_called()
