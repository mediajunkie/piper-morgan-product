"""#1987 half 2 — the which-todo ask lists the candidates and ARMS the pick.

CXO's addition (Web's alpha run 651756d520, 2026-10-12): two reminders just
set, `delete a reminder` → "Which todo should I remove? Try: 'delete todo
[number]'" — the generic, unarmed prompt; the user has to leave the chat to
find numbers. Bar: when the candidates are known and few, list them
numbered with titles in the question itself. Arch's condition (the #2000
census row on ``handle_delete_todo``): the numbered pick must ARM via the
#846 store.

Under test: ``delete_todo_pick.arm_delete_pick`` (the ARM half, reached from
``handle_delete_todo``'s no-number branch with the store handed in by the
rail entry point), ``handle_delete_todo_pick_turn`` (the ANSWER half at the
pop seam: the shared #1906 binder, then the #1666 title-bound DESTRUCTIVE
confirm armed with the row bound by id), the registered bare-yes landing,
and the source-level wiring (pop-seam branch, no-clobber flag, abandoned
map, registry axes).

Layer (m-43): the module functions with todo_service, the offer store and
the session stubbed (an in-memory one-slot store standing in for the #846
WorkflowOfferService); the handler and the rail entry point called with the
same stubs; the pop-seam branch and the registry pinned at source level. No
LLM, no DB, no served turn. The served check (PM's card: 'delete a
reminder' with two set → the numbered ask; '2' → the D1 confirm; 'yes' →
gone) is the issue's third AC and stays owed.
"""

import datetime as _dt
import inspect
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service import delete_todo_pick as dtp
from services.intent_service.acceptance import declared_axes_for_workflow
from services.intent_service.delete_todo_pick import (
    CLARIFY_DELETE_PICK_WORKFLOW,
    DELETE_PICK_KIND,
    MAX_LISTED,
    PICK_PENDING_FLAG,
    arm_delete_pick,
    handle_delete_todo_pick_turn,
    render_pick_question,
    run_clarify_delete_todo_pick_workflow,
)
from services.intent_service.destructive_confirm import (
    DESTRUCTIVE_CONFIRM_KIND,
    RESOLVED_TODO_CONTEXT_KEY,
)
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_dispatcher import (
    get_action_workflows,
    get_registered_workflows,
)
from services.intent_service.workflow_entries import (
    register_default_workflows,
    run_delete_todo_workflow,
)
from services.shared_types import EffectClass, IntentCategory

_USER = "3f7b8a52-1987-4b00-9e00-000000001988"
_SESSION = "sess-1987-pick"
_T0 = _dt.datetime(2026, 10, 14, 16, 0, tzinfo=_dt.timezone.utc)


def _todo(text, reminder_hours=None):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=(_T0 + _dt.timedelta(hours=reminder_hours))
        if reminder_hours is not None
        else None,
    )


def _intent(message, action="delete_todo"):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )


class _Store:
    """One-slot stand-in for the #846 WorkflowOfferService."""

    def __init__(self):
        self.slot = None
        self.calls = []

    def set_pending_offer(self, session_id, offer, user_id=None):
        self.slot = offer
        self.calls.append((session_id, offer, user_id))

    def peek_pending_offer(self, session_id):
        return self.slot

    def get_and_clear_pending_offer(self, session_id, user_id=None):
        offer, self.slot = self.slot, None
        return offer


@pytest.fixture
def rows():
    # Two reminders (later one first in the list → the ask must reorder) and one plain todo.
    return [_todo("send the invoice", 48), _todo("water the plants", 1), _todo("review the pr")]


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
def intent_service(todo_service, store):
    handlers = TodoIntentHandlers()
    handlers.todo_service = todo_service
    return SimpleNamespace(todo_handlers=handlers, workflow_offer_service=store)


@pytest.fixture(autouse=True)
def _no_router(monkeypatch):
    """The unresolved branch's second oracle is a router read — keep every
    test deterministic and LLM-free (the pre-classifier claim is tested on
    its own)."""
    from services.intent_service import inversion_live

    async def _none(*a, **k):
        return None

    monkeypatch.setattr(inversion_live, "read_op_claims_turn", _none)


async def _armed_pick(message, todo_service, store, principal=_USER):
    return await arm_delete_pick(message, _SESSION, principal, UUID(_USER), todo_service, store)


# ---------------------------------------------------------------------------
# 1. The ARM half — the question names what it binds
# ---------------------------------------------------------------------------


class TestRenderQuestion:
    def test_reminder_copy_lists_numbered_titles_and_the_exit(self):
        q = render_pick_question("reminder", ["water the plants", "send the invoice"])
        assert q.splitlines() == [
            "Which reminder should I delete?",
            "1. water the plants",
            "2. send the invoice",
            "",  # #2002: a blank line so the tail is its own paragraph, not item N's
            "Say the number or the name, or 'never mind' to leave them alone.",
        ]

    def test_more_tail_names_the_count_and_the_full_list(self):
        q = render_pick_question("todo", ["a", "b"], more=3)
        assert "(+3 more — say 'show my todos' for the full list.)" in q.splitlines()[-1]

    def test_reasked_head(self):
        q = render_pick_question("reminder", ["a"], reasked=True)
        assert q.startswith("Still not sure which reminder you mean — you have:")


@pytest.mark.asyncio
class TestArm:
    async def test_reminder_ask_lists_only_reminders_due_soonest_first_and_arms(
        self, rows, todo_service, store
    ):
        q = await _armed_pick("delete a reminder", todo_service, store)
        assert q.splitlines()[:3] == [
            "Which reminder should I delete?",
            "1. water the plants",
            "2. send the invoice",
        ]
        assert "review the pr" not in q
        offer = store.slot
        assert offer["workflow_type"] == CLARIFY_DELETE_PICK_WORKFLOW
        assert offer["question"] == q  # #1665: rendered once, stored + said
        pa = offer["pending_action"]
        assert pa["kind"] == DELETE_PICK_KIND
        assert pa["noun"] == "reminder"
        assert pa["pick_texts"] == ["water the plants", "send the invoice"]
        assert pa["pick_ids"] == [rows[1].id, rows[0].id]
        assert pa["pick_due"][0] < pa["pick_due"][1]
        assert pa["user_id"] == _USER
        assert pa["original_message"] == "delete a reminder"
        assert "Nothing has been deleted" in offer["decline_message"]

    async def test_todo_ask_lists_every_active_row_in_list_order(self, rows, todo_service, store):
        q = await _armed_pick("delete a todo", todo_service, store)
        assert q.splitlines()[1:4] == [
            "1. send the invoice",
            "2. water the plants",
            "3. review the pr",
        ]
        assert store.slot["pending_action"]["noun"] == "todo"

    async def test_more_than_max_lists_max_and_counts_the_rest(self, todo_service, store):
        many = [_todo(f"item {i}", i) for i in range(MAX_LISTED + 3)]
        todo_service.list_todos = AsyncMock(return_value=many)
        q = await _armed_pick("delete one of my reminders", todo_service, store)
        assert len(store.slot["pending_action"]["pick_ids"]) == MAX_LISTED
        assert f"(+3 more" in q
        assert f"{MAX_LISTED}. item {MAX_LISTED - 1}" in q
        assert f"{MAX_LISTED + 1}." not in q

    async def test_no_candidates_is_an_honest_line_nothing_armed(self, todo_service, store):
        todo_service.list_todos = AsyncMock(return_value=[_todo("review the pr")])
        q = await _armed_pick("delete a reminder", todo_service, store)
        assert q == "You don't have any reminders right now — nothing to delete."
        assert "?" not in q  # not an ask, so not an unarmed ask
        assert store.slot is None

    async def test_no_session_or_store_cannot_arm(self, todo_service, store):
        assert (
            await arm_delete_pick(
                "delete a reminder", None, _USER, UUID(_USER), todo_service, store
            )
            is None
        )
        assert (
            await arm_delete_pick(
                "delete a reminder", _SESSION, _USER, UUID(_USER), todo_service, None
            )
            is None
        )
        assert store.slot is None

    async def test_list_failure_falls_back_nothing_armed(self, todo_service, store):
        todo_service.list_todos = AsyncMock(side_effect=RuntimeError("db down"))
        assert await _armed_pick("delete a reminder", todo_service, store) is None
        assert store.slot is None


@pytest.mark.asyncio
class TestHandlerAndRail:
    async def test_handle_delete_todo_no_number_arms_the_pick(self, intent_service, store):
        msg = await intent_service.todo_handlers.handle_delete_todo(
            _intent("delete a reminder"),
            _SESSION,
            UUID(_USER),
            offer_service=store,
            principal=_USER,
        )
        assert msg.startswith("Which reminder should I delete?")
        assert store.slot["pending_action"]["kind"] == DELETE_PICK_KIND

    async def test_handle_delete_todo_without_a_store_gives_an_instruction_not_a_question(
        self, intent_service
    ):
        msg = await intent_service.todo_handlers.handle_delete_todo(
            _intent("delete a reminder"), _SESSION, UUID(_USER)
        )
        assert "?" not in msg
        assert "delete todo [number]" in msg and "show my todos" in msg

    async def test_numbered_delete_unchanged(self, intent_service, store, rows):
        """'delete todo 2' still takes the positional path (the rail's gate
        arms its confirm one turn earlier; here the handler alone deletes
        the row at that position)."""
        msg = await intent_service.todo_handlers.handle_delete_todo(
            _intent("delete todo 2"), _SESSION, UUID(_USER), offer_service=store, principal=_USER
        )
        assert store.slot is None
        intent_service.todo_handlers.todo_service.delete_todo.assert_awaited_once()
        assert rows[1].text in msg

    async def test_rail_entry_point_stamps_the_pending_flag(
        self, intent_service, store, monkeypatch
    ):
        from services.intent_service import reminder_clear as rc

        async def _none(*a, **k):
            return None

        monkeypatch.setattr(rc, "maybe_handle_clear_family", _none)
        monkeypatch.setattr(rc, "maybe_handle_explicit_bulk_delete", _none)
        result = await run_delete_todo_workflow(
            _SESSION,
            user_id=_USER,
            context={"intent_service": intent_service, "intent": _intent("delete a reminder")},
        )
        assert result.message.startswith("Which reminder should I delete?")
        assert result.intent_data[PICK_PENDING_FLAG] is True
        assert result.requires_clarification is True
        assert store.slot["pending_action"]["kind"] == DELETE_PICK_KIND


# ---------------------------------------------------------------------------
# 2. The ANSWER half — the pick arms the title-bound confirm, row bound by id
# ---------------------------------------------------------------------------


async def _answer(message, intent_service, store, user=_USER):
    offer = store.get_and_clear_pending_offer(_SESSION)
    return await handle_delete_todo_pick_turn(
        offer, message, session_id=_SESSION, user_id=user, intent_service=intent_service
    )


@pytest.mark.asyncio
class TestPickTurn:
    @pytest.mark.parametrize(
        "answer", ["2", "#2", "the second one", "second", "invoice", "the last one"]
    )
    async def test_bound_pick_arms_d1_confirm_with_the_row_bound_by_id(
        self, rows, intent_service, store, answer
    ):
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        out = await _answer(answer, intent_service, store)
        assert out["message"] == 'Delete the reminder "send the invoice"? (yes/no)'
        assert out["requires_clarification"] is True
        assert out["intent_data"]["destructive_confirmation_pending"] is True
        assert out["intent_data"]["delete_todo_pick_bound"] is True
        armed = store.slot
        pa = armed["pending_action"]
        assert pa["kind"] == DESTRUCTIVE_CONFIRM_KIND
        assert pa["summary"] == 'delete the reminder "send the invoice"'
        bound = pa["intent"].context[RESOLVED_TODO_CONTEXT_KEY]
        assert bound["todo_id"] == rows[0].id
        assert bound["text"] == "send the invoice"
        assert bound["number"] == "1"  # its position in the OWNER'S list, as the #1666 yes expects
        assert pa["intent"].action == "delete_todo"
        assert pa["intent"].original_message == "delete a reminder"
        intent_service.todo_handlers.todo_service.delete_todo.assert_not_awaited()

    async def test_todo_noun_uses_the_1527_copy(self, rows, intent_service, store):
        await _armed_pick("delete a todo", intent_service.todo_handlers.todo_service, store)
        out = await _answer("3", intent_service, store)
        assert out["message"] == 'Delete the todo "review the pr"? (yes/no)'
        assert store.slot["pending_action"]["summary"] == 'delete the todo "review the pr"'

    async def test_confirmed_yes_deletes_exactly_the_bound_row(self, rows, intent_service, store):
        """The #1666 path the armed intent re-enters: resolved + confirmed →
        delete by the bound id, never a positional re-resolve."""
        from services.intent_service.destructive_confirm import CONFIRMED_CONTEXT_KEY

        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        await _answer("1", intent_service, store)
        intent = store.slot["pending_action"]["intent"]
        intent.context[CONFIRMED_CONTEXT_KEY] = True
        # The list shifted since the ask: the bound row is still the one deleted.
        intent_service.todo_handlers.todo_service.list_todos = AsyncMock(return_value=rows[::-1])
        msg = await intent_service.todo_handlers.handle_delete_todo(intent, _SESSION, UUID(_USER))
        intent_service.todo_handlers.todo_service.delete_todo.assert_awaited_once_with(
            todo_id=UUID(rows[1].id), user_id=UUID(_USER)
        )
        assert "water the plants" in msg

    async def test_gone_row_is_the_1987_didnt_find_line_nothing_armed(
        self, rows, intent_service, store
    ):
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        intent_service.todo_handlers.todo_service.list_todos = AsyncMock(
            return_value=[rows[0], rows[2]]
        )
        out = await _answer("1", intent_service, store)  # water the plants — gone on the Todos page
        assert out["message"].startswith('I can\'t find "water the plants" anymore')
        assert out["message"].endswith("nothing has been deleted.")
        assert out["intent_data"]["pick_target_gone"] is True
        assert store.slot is None

    @pytest.mark.parametrize("answer", ["yes", "never mind", "no", "did I set one for Friday?"])
    async def test_accept_decline_and_state_question_fall_through(
        self, intent_service, store, answer
    ):
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        assert await _answer(answer, intent_service, store) is None
        assert store.slot is None  # nothing re-armed here; the generic seam owns these

    async def test_claimed_command_releases(self, intent_service, store):
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        # The 1906 suite's deterministic surface-1 claim (pre_classify, no router).
        assert await _answer("are we behind upstream at all", intent_service, store) is None
        assert store.slot is None

    async def test_unresolved_reasks_once_then_releases(self, intent_service, store):
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        out = await _answer("hmm, the one about the thing", intent_service, store)
        assert out["message"].startswith("Still not sure which reminder you mean")
        assert out["intent_data"][PICK_PENDING_FLAG] is True
        assert store.slot["pending_action"]["pick_reasked"] is True
        assert store.slot["question"] == out["message"]
        assert await _answer("the one about the thing", intent_service, store) is None
        assert store.slot is None

    async def test_principal_mismatch_holds_off(self, intent_service, store):
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        out = await _answer("1", intent_service, store, user=str(uuid4()))
        assert out["intent_data"]["principal_mismatch"] is True
        assert store.slot is None
        intent_service.todo_handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.parametrize(
        "pleasantry,ack",
        [
            ("thanks", "You're welcome."),
            ("thank you!", "You're welcome."),
            ("hello", "Hi!"),
        ],
    )
    async def test_pleasantry_survives_the_armed_pick(
        self, rows, intent_service, store, pleasantry, ack
    ):
        """Arch's condition 3 (#1987): 'thanks' while the pick is armed is NOT
        short-circuited into a release — the record is re-armed with the same
        candidates and the reply is CXO's copy (09:50 ruling): the plain ack
        — one string, the canned thanks constant — then the question WITH its
        numbered list re-shown (the user may have scrolled past it); nothing
        is done or deleted."""
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        armed_before = store.slot["pending_action"]["pick_ids"]
        out = await _answer(pleasantry, intent_service, store)
        lines = out["message"].splitlines()
        assert lines[0] == ack
        assert lines[1:4] == [
            "Which reminder should I delete?",
            "1. water the plants",
            "2. send the invoice",
        ]
        assert lines[4] == ""  # #2002 blank line before the tail
        assert lines[5] == "Say the number or the name, or 'never mind' to leave them alone."
        assert out["intent_data"][PICK_PENDING_FLAG] is True
        assert out["requires_clarification"] is True
        assert store.slot["pending_action"]["kind"] == DELETE_PICK_KIND
        assert store.slot["pending_action"]["pick_ids"] == armed_before
        intent_service.todo_handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.parametrize("farewell", ["bye", "goodbye"])
    async def test_farewell_releases_the_pick(self, intent_service, store, farewell):
        """CXO's ruling (2026-10-13): a farewell is the user leaving, not
        answering — the pick releases (None here; the pop already cleared the
        slot) and the canned farewell serves unchanged; nothing deleted."""
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        assert await _answer(farewell, intent_service, store) is None
        assert store.slot is None
        intent_service.todo_handlers.todo_service.delete_todo.assert_not_awaited()

    async def test_number_after_thanks_still_binds(self, rows, intent_service, store):
        """Arch's bar, pin 2: 'thanks' then '2' binds row 2 into the D1
        title-bound confirm; nothing is deleted without the yes."""
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        await _answer("thanks", intent_service, store)
        out = await _answer("2", intent_service, store)
        assert out["message"] == 'Delete the reminder "send the invoice"? (yes/no)'
        pa = store.slot["pending_action"]
        assert pa["kind"] == DESTRUCTIVE_CONFIRM_KIND
        assert pa["intent"].context[RESOLVED_TODO_CONTEXT_KEY]["todo_id"] == rows[0].id
        intent_service.todo_handlers.todo_service.delete_todo.assert_not_awaited()

    async def test_pleasantry_with_substance_is_not_a_pleasantry(self, intent_service, store):
        """'ok thanks' reads ACCEPT at the seam (the landing re-asks — None
        here); a real command still releases (pin 3 keeps the discriminator)."""
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        assert await _answer("ok thanks", intent_service, store) is None
        assert store.slot is None

    async def test_foreign_kind_is_none(self, intent_service):
        assert (
            await handle_delete_todo_pick_turn(
                {"pending_action": {"kind": "reminder_time_question"}},
                "1",
                session_id=_SESSION,
                user_id=_USER,
                intent_service=intent_service,
            )
            is None
        )


@pytest.mark.asyncio
class TestBareYesLanding:
    async def test_reasks_and_rearms_the_same_candidates(self, intent_service, store):
        await _armed_pick("delete a reminder", intent_service.todo_handlers.todo_service, store)
        payload = store.get_and_clear_pending_offer(_SESSION)["pending_action"]
        out = await run_clarify_delete_todo_pick_workflow(
            _SESSION,
            user_id=_USER,
            context={"pending_action": payload, "intent_service": intent_service},
        )
        assert out["message"].startswith("Just so I get it right:\nWhich reminder should I delete?")
        assert out["intent_data"][PICK_PENDING_FLAG] is True
        assert store.slot["pending_action"]["pick_ids"] == payload["pick_ids"]
        assert store.slot["question"] == out["message"]

    async def test_foreign_payload_is_none(self, intent_service):
        assert (
            await run_clarify_delete_todo_pick_workflow(
                _SESSION,
                context={"pending_action": {"kind": "other"}, "intent_service": intent_service},
            )
            is None
        )


# ---------------------------------------------------------------------------
# 3. Wiring pins — registry axes, the pop seam, the no-clobber flag
# ---------------------------------------------------------------------------


class TestWiring:
    def test_registered_offer_only_read(self):
        register_default_workflows()
        entry = get_registered_workflows()[CLARIFY_DELETE_PICK_WORKFLOW]
        assert entry.effect is EffectClass.READ
        assert CLARIFY_DELETE_PICK_WORKFLOW not in get_action_workflows()  # action_triggered=False
        assert declared_axes_for_workflow(CLARIFY_DELETE_PICK_WORKFLOW)[0] is EffectClass.READ

    def test_pop_seam_consults_the_kind_before_generic_accept(self):
        from services.intent import intent_service as mod

        src = inspect.getsource(mod)
        branch = src.index('elif _vi_payload.get("kind") == "delete_todo_pick_question":')
        generic = src.index("# ADR-059: Unified offer acceptance via workflow dispatcher.")
        assert generic < branch
        assert "handle_delete_todo_pick_turn(" in src[branch : branch + 900]
        assert '"delete_todo_pick_question": "delete_todo_pick_question_released"' in src

    def test_no_clobber_flag_listed(self):
        from services.intent import intent_service as mod

        src = inspect.getsource(mod)
        flags = src[src.index("_pending_flags = (") : src.index("_pending_flags = (") + 1800]
        assert f'"{PICK_PENDING_FLAG}"' in flags

    def test_no_new_regex(self):
        import re as _re

        src = inspect.getsource(dtp)
        assert "re.compile" not in src and "_re.compile" not in src
        assert _re.search(r"\bimport re\b", src) is None
