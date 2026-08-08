"""#1532 F3 — POST /api/v1/intent must enforce conversation ownership.

Pre-fix, the chat route checked conversation EXISTENCE only (auto-create,
#731) and never the owner — authenticated user B posting user A's session
UUID sailed into process_intent, hydrating A's turns and appending B's.
The REST surface (conversations.py:173) enforced exactly the check this
path skipped. Contract pinned here:

- cross-owner session id → HTTP 404 (treated as not-found for this account;
  existence and the true owner are never leaked in the response), BEFORE
  process_intent runs;
- a hypothetical anonymous-owned row hit by an authenticated user → same 404
  (the safe not-found contract);
- own session id / fresh session id → unchanged behavior (process + auto-create);
- the ownership 404 must NOT be swallowed by the Pattern-007 degradation
  except (which turns everything else into a 200).
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

import web.api.routes.intent as intent_route
from services.database import session_factory as sf
from web.api.routes.intent import process_intent

USER_B = str(uuid4())
USER_A = str(uuid4())


def _claims(sub):
    return SimpleNamespace(
        sub=sub,
        workspace_id=None,
        user_email="user@example.com",
        session_id=None,
    )


def _mock_request(session_id):
    req = MagicMock()
    req.json = AsyncMock(return_value={"message": "hello", "session_id": session_id})
    req.headers = MagicMock()
    req.headers.get = MagicMock(return_value=None)
    req.cookies = {}
    req.state = SimpleNamespace()
    mock_result = MagicMock(
        message="hi there",
        intent_data={},
        workflow_id=None,
        requires_clarification=False,
        clarification_type=None,
        suggestions=[],
        preferences={},
        error=None,
        error_type=None,
        async_work_started=False,
    )
    req.app.state.intent_service = MagicMock()
    req.app.state.intent_service.process_intent = AsyncMock(return_value=mock_result)
    return req


@pytest.fixture
def db_row(monkeypatch):
    """Patch the fresh-session factory the route uses; returns a setter for
    what session.get(ConversationDB, session_id) finds."""
    holder = {"row": None}
    session = MagicMock()
    session.get = AsyncMock(side_effect=lambda *_a, **_k: holder["row"])
    session.add = MagicMock()
    session.commit = AsyncMock()
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=session)
    cm.__aexit__ = AsyncMock(return_value=None)
    monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope_fresh", lambda: cm)
    # keep the BYOC key-resolution seam out of the picture
    monkeypatch.setattr(
        intent_route, "resolve_request_api_key", AsyncMock(return_value="sk-test")
    )
    holder["session"] = session
    return holder


@pytest.mark.asyncio
async def test_cross_owner_session_id_refused_404_before_processing(db_row):
    session_id = str(uuid4())
    db_row["row"] = SimpleNamespace(user_id=USER_A)
    req = _mock_request(session_id)

    with pytest.raises(HTTPException) as exc:
        await process_intent(req, current_user=_claims(USER_B))

    assert exc.value.status_code == 404
    # honest not-found copy; never confirms existence or names the owner
    assert "not found" in str(exc.value.detail).lower()
    assert USER_A not in str(exc.value.detail)
    # refused BEFORE any hydration/append could happen
    req.app.state.intent_service.process_intent.assert_not_called()


@pytest.mark.asyncio
async def test_anonymous_owned_row_treated_as_not_found_for_authenticated_user(db_row):
    """PINNED safe contract: authenticated user + anonymous-owned row → 404."""
    db_row["row"] = SimpleNamespace(user_id=None)
    req = _mock_request(str(uuid4()))

    with pytest.raises(HTTPException) as exc:
        await process_intent(req, current_user=_claims(USER_B))

    assert exc.value.status_code == 404
    req.app.state.intent_service.process_intent.assert_not_called()


@pytest.mark.asyncio
async def test_own_session_id_processes_normally(db_row):
    db_row["row"] = SimpleNamespace(user_id=USER_B)
    req = _mock_request(str(uuid4()))

    result = await process_intent(req, current_user=_claims(USER_B))

    req.app.state.intent_service.process_intent.assert_awaited_once()
    assert result["message"] == "hi there"
    assert result["conversation_created"] is False


@pytest.mark.asyncio
async def test_fresh_session_id_still_auto_creates(db_row):
    """#731 auto-create unchanged when no row exists."""
    db_row["row"] = None
    req = _mock_request(str(uuid4()))

    result = await process_intent(req, current_user=_claims(USER_B))

    db_row["session"].add.assert_called_once()
    assert result["conversation_created"] is True
    req.app.state.intent_service.process_intent.assert_awaited_once()
