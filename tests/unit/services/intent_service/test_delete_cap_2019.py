"""Issue 2019: bulk todo/reminder deletes are capped at one item until soft
delete exists (xian's 2026-10-14 ruling; PPM's interim B; Arch's placement:
the cap lives in the delete handlers, so every entry path gets it).

CXO's capped reply (the issue's copy comment) is the spec, byte for byte:
it names the resolved items in the order the user sees them, ends on
"Nothing has been changed.", and arms nothing ("Tell me which one to delete
first." is an instruction, not an offer). Single deletes keep today's named
confirm; mark done on a bulk set stays uncapped.

This file holds the copy pin and the entry paths whose pins are not in a
sibling suite:

- the shared builder (``delete_cap.capped_delete_reply``);
- ``handle_delete_todo_targets`` through the REAL rail entry point
  (``run_delete_todo_workflow``), the served case
  ``delete the first two reminders``;
- ``delete_todo_pick`` (an answer naming several candidates);
- the legacy ``handle_delete_todo`` and the #1666 rail gate
  (``build_todo_delete_confirmation``): structurally one item at most,
  pinned so a later change cannot quietly arm a multi-item delete there.

Sibling pins: ``test_delete_todo_router_targets.py`` (handler-level cap and
the confirmed-re-entry belt), ``test_clear_todos_resolver.py`` (the
clear_todos re-entries, real dispatch, and mark done uncapped),
``test_bulk_delete_reminders_1696.py`` (explicit bulk, e2e),
``test_reminder_clear_verb_1605.py::TestIssue2019DeleteCap`` (the #1605
seam's variant 3, verb answer, ALWAYS_ASK branch, correction turn, and the
confirmed sink).

Layer (m-43): handler and rail-entry-point level with todo_service, the
offer store and the session context stubbed. No LLM, no DB.
"""

import datetime as _dt
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service.conversation_context import NumberedList
from services.intent_service.delete_cap import (
    DELETE_CAPPED_FLAG,
    capped_delete_reply,
    exceeds_delete_cap,
)
from services.intent_service.delete_todo_pick import (
    DELETE_PICK_KIND,
    arm_delete_pick,
    handle_delete_todo_pick_turn,
)
from services.intent_service.destructive_confirm import (
    DESTRUCTIVE_CONFIRM_KIND,
    RESOLVED_TODO_CONTEXT_KEY,
    build_todo_delete_confirmation,
)
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_entries import run_delete_todo_workflow
from services.shared_types import IntentCategory

_USER = "5a1e2d40-2019-4b00-9e00-000000002019"
_SESSION = "sess-2019-cap"
# A fixed clock in the PAST (the 1987/2003 files use the same date): the
# targets handler's pool is the reminders that are DUE, so a base time on the
# day the test runs made the served case straddle the clock (one reminder due
# before 17:00 UTC, two after) — the two rail-entry pins passed in the morning
# and failed in CI's 16:49Z run. Both reminders are always due now.
_T0 = _dt.datetime(2026, 10, 14, 16, 0, tzinfo=_dt.timezone.utc)

CXO_CAPPED_REPLY = (
    "I can delete one reminder at a time for now. You asked about these:\n"
    '1. "revise the pr"\n'
    '2. "send the budget review to the board"\n'
    "\n"
    "Tell me which one to delete first. Nothing has been changed."
)


def _todo(text, reminder_hours=None):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=(
            (_T0 + _dt.timedelta(hours=reminder_hours)) if reminder_hours is not None else None
        ),
    )


def _intent(message, targets=None):
    ctx = {"original_message": message}
    if targets is not None:
        ctx["inversion_args"] = {"targets": targets}
    return Intent(
        category=IntentCategory.EXECUTION,
        action="delete_todo",
        original_message=message,
        confidence=0.95,
        context=ctx,
    )


class _Store:
    """One-slot stand-in for the #846 WorkflowOfferService."""

    def __init__(self):
        self.slot = None
        self.calls = []

    def set_pending_offer(self, session_id, offer, user_id=None):
        self.slot = offer
        self.calls.append((session_id, offer, user_id))

    def peek_pending_offer(self, session_id, user_id=None):
        return self.slot

    def get_and_clear_pending_offer(self, session_id, user_id=None):
        offer, self.slot = self.slot, None
        return offer


@pytest.fixture
def rows():
    # The served case's two reminders, plus a plain todo.
    return [
        _todo("revise the pr", 1),
        _todo("send the budget review to the board", 2),
        _todo("water the plants"),
    ]


@pytest.fixture
def todo_service(rows):
    svc = AsyncMock()
    svc.list_todos = AsyncMock(return_value=rows)
    svc.delete_todo = AsyncMock(return_value=True)
    return svc


@pytest.fixture
def store():
    return _Store()


@pytest.fixture
def session_ctx(monkeypatch):
    ctx = SimpleNamespace(last_numbered_list=None, last_created_todo=None)
    monkeypatch.setattr(
        "services.intent_service.conversation_context.get_or_create_context",
        lambda session_id, user_id=None: ctx,
    )
    return ctx


@pytest.fixture
def intent_service(todo_service, store, session_ctx):
    handlers = TodoIntentHandlers()
    handlers.todo_service = todo_service
    return SimpleNamespace(todo_handlers=handlers, workflow_offer_service=store)


@pytest.fixture(autouse=True)
def _no_router(monkeypatch):
    """The pick's unresolved branch consults the router; keep it LLM-free."""
    from services.intent_service import inversion_live

    async def _none(*a, **k):
        return None

    monkeypatch.setattr(inversion_live, "read_op_claims_turn", _none)


# ---------------------------------------------------------------------------
# 1. The copy: one builder, CXO's text byte for byte
# ---------------------------------------------------------------------------


class TestCappedCopy:
    def test_byte_identical_to_cxo_copy(self):
        assert (
            capped_delete_reply(["revise the pr", "send the budget review to the board"])
            == CXO_CAPPED_REPLY
        )

    def test_todo_noun_variant(self):
        assert capped_delete_reply(["a", "b"], "todo").startswith(
            "I can delete one todo at a time for now. You asked about these:\n"
        )

    def test_is_an_instruction_not_a_question(self):
        """TestUnarmedAskSiteRatchet: no line of the reply ends in '?'."""
        reply = capped_delete_reply(["a?", "b"])
        assert not reply.rstrip().endswith("?")
        assert "or I can mark" not in reply
        assert "undo" not in reply.lower()

    def test_cap_is_one(self):
        assert not exceeds_delete_cap(0)
        assert not exceeds_delete_cap(1)
        assert exceeds_delete_cap(2)


# ---------------------------------------------------------------------------
# 2. handle_delete_todo_targets through the real rail entry point
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestTargetsPathThroughTheRailEntryPoint:
    async def _run(self, intent_service, message, targets):
        return await run_delete_todo_workflow(
            _SESSION,
            user_id=_USER,
            context={"intent_service": intent_service, "intent": _intent(message, targets)},
        )

    async def test_served_case_first_two_is_capped_and_arms_nothing(
        self, intent_service, store, todo_service, session_ctx, rows
    ):
        session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[t.id for t in rows], texts=[t.text for t in rows]
        )
        result = await self._run(intent_service, "delete the first two reminders", ["1-2"])
        assert result.message == CXO_CAPPED_REPLY
        assert result.requires_clarification is False
        assert not result.intent_data.get("destructive_confirmation_pending")
        assert store.slot is None and store.calls == []
        todo_service.delete_todo.assert_not_awaited()
        # The capped list is now the numbered list on screen (context, not an arm).
        assert session_ctx.last_numbered_list.ids == [rows[0].id, rows[1].id]

    async def test_one_target_still_arms_todays_named_confirm(
        self, intent_service, store, todo_service, session_ctx, rows
    ):
        session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[t.id for t in rows], texts=[t.text for t in rows]
        )
        result = await self._run(intent_service, "delete the second one", ["2"])
        assert result.message == 'Delete the todo "send the budget review to the board"? (yes/no)'
        assert result.requires_clarification is True
        assert store.slot["pending_action"]["kind"] == "todo_batch_delete"
        todo_service.delete_todo.assert_not_awaited()


# ---------------------------------------------------------------------------
# 3. delete_todo_pick: an answer naming several candidates
# ---------------------------------------------------------------------------


async def _armed(intent_service, store, todo_service):
    q = await arm_delete_pick(
        "delete a reminder", _SESSION, _USER, UUID(_USER), todo_service, store
    )
    assert q.startswith("Which reminder should I delete?")
    return store.get_and_clear_pending_offer(_SESSION)


@pytest.mark.asyncio
class TestPickPath:
    @pytest.mark.parametrize(
        "answer", ["1 and 2", "both", "the first and the last", "all of them", "#1, #2"]
    )
    async def test_multi_answer_is_capped_and_arms_nothing(
        self, intent_service, store, todo_service, answer
    ):
        offer = await _armed(intent_service, store, todo_service)
        out = await handle_delete_todo_pick_turn(
            offer, answer, session_id=_SESSION, user_id=_USER, intent_service=intent_service
        )
        assert out is not None, answer
        assert out["message"] == CXO_CAPPED_REPLY, answer
        assert out["intent_data"][DELETE_CAPPED_FLAG] is True
        assert not out.get("requires_clarification")
        assert store.slot is None, answer  # neither a delete confirm nor a re-armed pick
        todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.parametrize("answer", ["2", "the second one", "budget review"])
    async def test_single_answer_still_arms_the_named_confirm(
        self, intent_service, store, todo_service, rows, answer
    ):
        offer = await _armed(intent_service, store, todo_service)
        out = await handle_delete_todo_pick_turn(
            offer, answer, session_id=_SESSION, user_id=_USER, intent_service=intent_service
        )
        assert out["message"] == (
            'Delete the reminder "send the budget review to the board"? (yes/no)'
        )
        pa = store.slot["pending_action"]
        assert pa["kind"] == DESTRUCTIVE_CONFIRM_KIND
        assert pa["intent"].context[RESOLVED_TODO_CONTEXT_KEY]["todo_id"] == rows[1].id
        todo_service.delete_todo.assert_not_awaited()

    async def test_a_title_containing_all_still_binds_by_name(
        self, intent_service, store, todo_service, rows
    ):
        """The quantifier only counts when the name binder does not bind one
        candidate, so 'all' inside a real title is not a bulk answer."""
        rows[1].text = "call all hands"
        offer = await _armed(intent_service, store, todo_service)
        out = await handle_delete_todo_pick_turn(
            offer,
            "call all hands",
            session_id=_SESSION,
            user_id=_USER,
            intent_service=intent_service,
        )
        assert out["message"] == 'Delete the reminder "call all hands"? (yes/no)'


# ---------------------------------------------------------------------------
# 4. Legacy handle_delete_todo and the #1666 rail gate: one item at most
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestStructurallySinglePaths:
    async def test_legacy_handler_never_arms_a_multi_item_delete(
        self, intent_service, store, todo_service
    ):
        """No router targets: a plural ask reaches the legacy handler's
        no-number branch, which arms the PICK question (not a delete
        carrier) and deletes nothing."""
        msg = await intent_service.todo_handlers.handle_delete_todo(
            _intent("delete the first two reminders"),
            _SESSION,
            user_id=UUID(_USER),
            offer_service=store,
            principal=_USER,
        )
        assert msg.startswith("Which reminder should I delete?")
        assert store.slot["pending_action"]["kind"] == DELETE_PICK_KIND
        todo_service.delete_todo.assert_not_awaited()

    async def test_rail_gate_passes_a_positional_bulk_ask_through_unarmed(
        self, intent_service, todo_service
    ):
        gate = await build_todo_delete_confirmation(
            _intent("delete the first two reminders"),
            intent_service.todo_handlers,
            UUID(_USER),
            session_id=_SESSION,
        )
        assert gate.offer is None and gate.passthrough is True
        todo_service.delete_todo.assert_not_awaited()

    async def test_rail_gate_one_number_keeps_todays_named_confirm(
        self, intent_service, todo_service
    ):
        gate = await build_todo_delete_confirmation(
            _intent("delete todo 2"),
            intent_service.todo_handlers,
            UUID(_USER),
            session_id=_SESSION,
        )
        assert gate.offer is not None
        assert gate.offer.question == (
            'Delete the todo "send the budget review to the board"? (yes/no)'
        )
        todo_service.delete_todo.assert_not_awaited()
