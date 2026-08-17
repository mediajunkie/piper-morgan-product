"""#1544 — "what todos are pending?" must surface the USER's todos (real Postgres).

PM live 2026-08-09: with 2+ todos existing, the reply was "I don't see any
todos in your list right now — nothing's showing up on my end for this
conversation." The phrasing passes the pre-classifier untouched (verified by
direct execution), the LLM emits an unrailed QUERY action, and the floor door
(#1570's `_handle_unknown_intent`) gathers context with category QUERY — the
#960 else-branch → `_gather_status_priority_context` → the OWNER-scoped
pending-todos read.

This test drives that exact gather against the real repository and real
Postgres — no mocks at the boundary that failed — then renders the floor's
context block. Layer honesty (m-43): the LLM classification and the model's
final prose are NOT under test here (no live model); what is pinned is that
the deterministic pipeline delivers the user's rows (or a verified-empty
fact) to the floor, owner-scoped, with no conversation-scoped framing on any
deterministic surface. The prompt-side pins live in
tests/unit/services/intent_service/test_todo_scope_framing_1544.py.
"""

import uuid

import pytest
from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory
from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import ConversationalFloor
from services.todo.todo_management_service import TodoManagementService


@pytest.fixture
async def repro_user():
    """A scratch user, removed with its todos afterwards."""
    username = f"todo-1544-{uuid.uuid4().hex[:8]}"
    async with AsyncSessionFactory.session_scope() as s:
        r = await s.execute(
            text(
                "INSERT INTO users (username, email, is_active) "
                "VALUES (:u, :e, true) RETURNING id"
            ),
            {"u": username, "e": f"{username}@example.com"},
        )
        uid = r.scalar()
        await s.commit()
    yield uid
    async with AsyncSessionFactory.session_scope() as s:
        await s.execute(
            text("DELETE FROM todo_items WHERE owner_id = :u"), {"u": str(uid)}
        )
        await s.execute(
            text(
                "DELETE FROM items WHERE id NOT IN (SELECT id FROM todo_items) "
                "AND text LIKE 'repro-1544%'"
            )
        )
        await s.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


async def _gather_as_the_floor_door_would(user_id: str) -> dict:
    """The exact call `_handle_unknown_intent` makes post-#1570 for an
    unrailed QUERY emission ("what todos are pending?")."""
    assembler = ContextAssembler()
    return await assembler.gather_context(
        intent_category="QUERY",
        user_id=user_id,
        session_id=f"s-1544-{uuid.uuid4().hex[:8]}",
        intent_action="list_pending_todos",  # a paraphrase emission, unrailed
    )


@pytest.mark.asyncio
async def test_users_todos_reach_the_floor_context_owner_scoped(repro_user):
    """AC-1: with todos existing for the user, the QUERY floor gather
    returns THEM — read owner-scoped from the real store."""
    svc = TodoManagementService()
    t1 = await svc.create_todo(text="repro-1544 review beta feedback", user_id=repro_user)
    t2 = await svc.create_todo(text="repro-1544 draft release notes", user_id=repro_user)
    assert t1 is not None and t2 is not None

    ctx = await _gather_as_the_floor_door_would(str(repro_user))

    todos = ctx.get("pending_todos")
    assert isinstance(todos, list) and todos, (
        f"user's todos missing from floor context; keys={sorted(ctx.keys())}"
    )
    texts = {t.get("text") for t in todos}
    assert "repro-1544 review beta feedback" in texts
    assert "repro-1544 draft release notes" in texts
    assert ctx.get("pending_todo_count") == 2

    # And the rendered block the floor model actually sees names them.
    block = ConversationalFloor(llm_client=object())._format_domain_context(ctx)
    assert "PENDING TODOS (2)" in block
    assert "repro-1544 review beta feedback" in block
    assert "repro-1544 draft release notes" in block


@pytest.mark.asyncio
async def test_zero_todos_is_verified_empty_not_absence(repro_user):
    """AC-2: a user with NO todos gets a definite checked-and-empty fact —
    never a silent absence the model must hedge over."""
    ctx = await _gather_as_the_floor_door_would(str(repro_user))

    assert ctx.get("pending_todos") == [], (
        f"verified-empty must be present as []; keys={sorted(ctx.keys())}"
    )
    assert ctx.get("pending_todo_count") == 0
    assert "pending_todos_source_failed" not in ctx

    block = ConversationalFloor(llm_client=object())._format_domain_context(ctx)
    assert "PENDING TODOS: none" in block
    assert "checked" in block


@pytest.mark.asyncio
async def test_no_conversation_scoped_framing_on_any_deterministic_surface(repro_user):
    """AC-3 (transcript-shape regression): neither the populated nor the
    empty rendered block may carry the misframe PM saw."""
    floor = ConversationalFloor(llm_client=object())

    empty_block = floor._format_domain_context(
        await _gather_as_the_floor_door_would(str(repro_user))
    )

    svc = TodoManagementService()
    await svc.create_todo(text="repro-1544 one live todo", user_id=repro_user)
    populated_block = floor._format_domain_context(
        await _gather_as_the_floor_door_would(str(repro_user))
    )

    for phrase in ("for this conversation", "on my end", "I don't see any todos"):
        assert phrase not in empty_block, (phrase, empty_block)
        assert phrase not in populated_block, (phrase, populated_block)
