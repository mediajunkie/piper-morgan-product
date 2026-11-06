"""#2219 row 3 (Arch 11-06 10:16 and 10:48; CXO's words): a write the classifier files
under a floor category reaches its handler, MARKED, and on that turn asks but never
writes.

Served on alpha 0d4938cf23: after "show my todos", "complete the second one" was
classified CONVERSATION/complete_todo, went to the floor (the #911 gate is
category-keyed), and the floor said "If you'd like me to mark "high task" as complete,
just tell me directly." Nothing was written.

Pins, per effect class: a floor-category WRITE and DESTRUCTIVE write nothing on the
marked turn; a READ op under a floor category still goes to the floor; an EXECUTION or
router-named complete is unchanged (Gap B completes at once); the named complete asks
CXO's yes/no and "yes" completes once; no target after the shown list picks over it,
and the answer binds; no list shown is a statement.

Drives the REAL ``IntentService.process_intent`` and classifier chain; the only pinned
seam is the LLM boundary (the legacy classifier's emission), as the #2294 and #2219
delete-pick pins do. The router case pins the classification result instead, since a
router emission is what carries ``inversion_args``.
"""

import json
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.floor_write_ask import (
    COMPLETE_NO_TARGET_STATEMENT,
    FLOOR_WRITE_MARK_KEY,
)
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2219-4c00-9e00-000000003219"
_SID = "e2e-2219-floor-write"


class _PinnedEmissionLLM:
    def __init__(self, category: str, action: str):
        self.emission = {
            "category": category,
            "action": action,
            "confidence": 0.9,
            "reasoning": "pinned",
            "helpful_knowledge_domains": [],
            "ambiguity_notes": [],
            "knowledge_used": [],
        }

    async def complete(self, task_type=None, **kwargs):
        if task_type != "intent_classification":
            raise AssertionError(f"LLM boundary touched for task_type={task_type!r}")
        return json.dumps(self.emission)


def _todo(text, priority="medium"):
    return Todo(id=str(uuid4()), text=text, priority=priority, status="pending", completed=False)


@pytest.fixture
def boundary(monkeypatch):
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": [
            _todo("urgent task", "urgent"),
            _todo("high task", "high"),
            _todo("review prs"),
            _todo("review prs"),
            _todo("review prs"),
        ],
        "completed": [],
        "deleted": [],
        "created": [],
    }

    async def _list_todos(self, user_id, include_completed=False):
        return [t for t in state["todos"] if include_completed or not t.completed]

    async def _complete(self, todo_id, user_id):
        row = next((t for t in state["todos"] if t.id == str(todo_id)), None)
        if row is None or row.completed:
            return None
        state["completed"].append(str(todo_id))
        row.completed = True
        row.status = "completed"
        return row

    async def _delete(self, todo_id, user_id):
        state["deleted"].append(str(todo_id))
        state["todos"] = [t for t in state["todos"] if t.id != str(todo_id)]
        return True

    async def _create(self, user_id, text, priority="medium", **kwargs):
        row = _todo(text, priority)
        state["created"].append(text)
        state["todos"].append(row)
        return row

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "complete_todo", _complete)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    monkeypatch.setattr(TodoManagementService, "create_todo", _create)
    return state


def _wrote(state):
    return state["completed"] + state["deleted"] + state["created"]


def _shown(state):
    """What "show my todos" records (Gap A): one entry per line, every copy's id."""
    t = state["todos"]
    lines = [[t[0]], [t[1]], [t[2], t[3], t[4]]]
    TodoIntentHandlers._remember_numbered_list(
        _SID,
        _USER,
        "todos",
        [line[0].id for line in lines],
        [line[0].text for line in lines],
        groups=[[x.id for x in line] for line in lines],
    )


def _service(category="conversation", action="complete_todo"):
    register_default_workflows()
    return IntentService(
        intent_classifier=IntentClassifier(llm_service=_PinnedEmissionLLM(category, action))
    )


_PICK = (
    "Which todo should I complete?\n"
    "1. urgent task (urgent)\n"
    "2. high task (high)\n"
    "3. review prs (×3)\n"
    "\n"
    "Say the number or the name, or 'never mind' to leave them alone."
)


# ── the served row: no target after the shown list → the pick, and the answer binds ──


@pytest.mark.asyncio
async def test_served_row_after_the_list_asks_the_pick_and_writes_nothing(boundary):
    _shown(boundary)
    result = await _service().process_intent(
        message="complete the second one", session_id=_SID, user_id=_USER
    )
    assert result.message == _PICK
    assert "just tell me directly" not in result.message
    assert _wrote(boundary) == []


@pytest.mark.asyncio
async def test_the_picked_line_completes_once(boundary):
    _shown(boundary)
    service = _service()
    await service.process_intent(message="complete the second one", session_id=_SID, user_id=_USER)
    done = await service.process_intent(message="2", session_id=_SID, user_id=_USER)
    assert boundary["completed"] == [boundary["todos"][1].id]
    assert "high task" in done.message


@pytest.mark.asyncio
async def test_a_picked_grouped_line_asks_one_or_all(boundary):
    _shown(boundary)
    service = _service()
    await service.process_intent(message="complete the second one", session_id=_SID, user_id=_USER)
    ask = await service.process_intent(message="3", session_id=_SID, user_id=_USER)
    assert ask.message == '"review prs" is on your list 3 times. Complete one, or all 3?'
    assert _wrote(boundary) == []


@pytest.mark.asyncio
async def test_never_mind_on_the_pick_writes_nothing(boundary):
    _shown(boundary)
    service = _service()
    await service.process_intent(message="complete the second one", session_id=_SID, user_id=_USER)
    await service.process_intent(message="never mind", session_id=_SID, user_id=_USER)
    assert _wrote(boundary) == []


@pytest.mark.asyncio
async def test_no_list_shown_is_a_statement_and_nothing_is_armed(boundary):
    service = _service()
    result = await service.process_intent(
        message="complete the second one", session_id=_SID + "-nolist", user_id=_USER
    )
    assert result.message == COMPLETE_NO_TARGET_STATEMENT
    assert _wrote(boundary) == []
    assert service.workflow_offer_service.peek_pending_offer(_SID + "-nolist", _USER) is None


# ── a named target: CXO's yes/no, and only the yes writes, once ──


@pytest.mark.asyncio
async def test_named_complete_asks_cxos_confirm_and_writes_nothing(boundary):
    result = await _service().process_intent(
        message="mark high task as done", session_id=_SID + "-named", user_id=_USER
    )
    assert result.message == 'Mark "high task" as done? (yes/no)'
    assert _wrote(boundary) == []


@pytest.mark.asyncio
async def test_yes_completes_exactly_the_shown_row_once(boundary):
    service = _service()
    sid = _SID + "-yes"
    await service.process_intent(message="mark high task as done", session_id=sid, user_id=_USER)
    await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert boundary["completed"] == [boundary["todos"][1].id]
    # a second yes has nothing armed to fire
    await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert boundary["completed"] == [boundary["todos"][1].id]


@pytest.mark.asyncio
async def test_no_writes_nothing(boundary):
    service = _service()
    sid = _SID + "-no"
    await service.process_intent(message="mark high task as done", session_id=sid, user_id=_USER)
    declined = await service.process_intent(message="no", session_id=sid, user_id=_USER)
    assert _wrote(boundary) == []
    assert declined.message == (
        'Okay — I won\'t mark "high task" as done. Nothing has been changed.'
    )


@pytest.mark.asyncio
async def test_a_musing_with_a_fuzzy_match_is_shown_before_anything_is_done(boundary):
    """Arch's reason for the mark: the named leg fuzzy-matches and would complete at once."""
    boundary["todos"].append(_todo("write the report"))
    result = await _service().process_intent(
        message="I should complete the report someday", session_id=_SID + "-muse", user_id=_USER
    )
    assert result.message == 'Mark "write the report" as done? (yes/no)'
    assert _wrote(boundary) == []


# ── other effect classes on a marked turn ──


@pytest.mark.asyncio
async def test_a_floor_category_destructive_write_writes_nothing(boundary):
    service = _service(action="delete_todo")
    sid = _SID + "-del"
    high = boundary["todos"][1].id
    result = await service.process_intent(
        message="delete the high task todo", session_id=sid, user_id=_USER
    )
    assert result.message == 'Delete the todo "high task"? (yes/no)'
    assert _wrote(boundary) == []
    await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert boundary["deleted"] == [high]


@pytest.mark.asyncio
async def test_another_floor_category_write_asks_the_generic_confirm(boundary):
    """Any write but complete and delete gets the #1190 carrier's existing words today
    (CXO to word them); it writes nothing until yes."""
    service = _service(action="create_todo")
    sid = _SID + "-create"
    result = await service.process_intent(
        message="I keep meaning to add buy milk", session_id=sid, user_id=_USER
    )
    assert result.message == "Are you sure you want me to create todo? (yes/no)"
    assert _wrote(boundary) == []
    await service.process_intent(message="no", session_id=sid, user_id=_USER)
    assert _wrote(boundary) == []


@pytest.mark.asyncio
async def test_a_read_op_under_a_floor_category_still_goes_to_the_floor(boundary, monkeypatch):
    from services.intent.intent_service import IntentProcessingResult

    seen = []

    async def _floor(self, intent, session_id, **kwargs):
        seen.append(intent.action)
        return IntentProcessingResult(success=True, message="FLOOR", intent_data={})

    monkeypatch.setattr(IntentService, "_handle_floor_with_context", _floor)
    result = await _service(action="list_todos_query").process_intent(
        message="what's on my plate", session_id=_SID + "-read", user_id=_USER
    )
    assert seen == ["list_todos_query"]
    assert result.message.startswith("FLOOR")


# ── unchanged: an EXECUTION classification or a router-named complete ──


@pytest.mark.asyncio
async def test_an_execution_complete_completes_at_once(boundary):
    result = await _service(category="execution").process_intent(
        message="mark high task as done", session_id=_SID + "-exec", user_id=_USER
    )
    assert boundary["completed"] == [boundary["todos"][1].id]
    assert "(yes/no)" not in result.message


@pytest.mark.asyncio
async def test_a_router_named_complete_is_never_marked_and_completes_at_once(boundary, monkeypatch):
    message = "mark high task as done"

    async def _classify(self, message=None, *args, **kwargs):
        msg = message or kwargs.get("text") or ""
        return Intent(
            category=IntentCategory.CONVERSATION,
            action="complete_todo",
            confidence=0.95,
            original_message=msg,
            context={"original_message": msg, "inversion_args": {"targets": ["name:high task"]}},
        )

    monkeypatch.setattr(IntentClassifier, "classify", _classify)
    service = _service()
    result = await service.process_intent(
        message=message, session_id=_SID + "-router", user_id=_USER
    )
    assert boundary["completed"] == [boundary["todos"][1].id]
    assert "(yes/no)" not in result.message


def test_the_mark_reads_category_effect_and_router_provenance():
    service = _service()

    def _intent(category, action, **ctx):
        return Intent(
            category=category,
            action=action,
            confidence=0.9,
            original_message="m",
            context={"original_message": "m", **ctx},
        )

    assert service._is_floor_category_write(_intent(IntentCategory.CONVERSATION, "complete_todo"))
    assert service._is_floor_category_write(_intent(IntentCategory.STATUS, "delete_todo"))
    # READ op, router emission, EXECUTION category: never marked
    assert not service._is_floor_category_write(
        _intent(IntentCategory.CONVERSATION, "list_todos_query")
    )
    assert not service._is_floor_category_write(
        _intent(IntentCategory.CONVERSATION, "complete_todo", inversion_args={})
    )
    assert not service._is_floor_category_write(_intent(IntentCategory.EXECUTION, "complete_todo"))
    # the gate sends the write to its handler, and still floors the READ
    assert not service._should_route_to_floor(_intent(IntentCategory.CONVERSATION, "complete_todo"))
    assert service._should_route_to_floor(_intent(IntentCategory.CONVERSATION, "list_todos_query"))


def test_the_yes_runs_unmarked():
    from services.intent_service.floor_write_ask import (
        mark_floor_category_write,
        unmark_floor_category_write,
    )

    intent = Intent(
        category=IntentCategory.CONVERSATION,
        action="complete_todo",
        confidence=0.9,
        original_message="m",
        context={"original_message": "m"},
    )
    mark_floor_category_write(intent)
    assert intent.context[FLOOR_WRITE_MARK_KEY] is True
    unmark_floor_category_write(intent)
    assert FLOOR_WRITE_MARK_KEY not in intent.context


@pytest.mark.asyncio
@pytest.mark.parametrize("stored", [{"value": "complete"}, None])
async def test_a_marked_clear_family_turn_asks_where_it_would_have_written(
    boundary, monkeypatch, stored
):
    """The #1605 flow is the one passthrough that writes on its first turn: a stored
    "complete" default auto-applies, and so does the trust-inferences meta mode. On a
    marked turn both ask their existing questions instead."""
    from services.intent_service import verified_inference as vi
    from services.intent_service.reminder_clear import variant_two_always_ask_question

    async def _stored(user_id, key):
        return stored

    async def _mode(user_id):
        return vi.VerificationMetaMode.TRUST_INFERENCES

    monkeypatch.setattr(vi, "get_verified_inference", _stored)
    monkeypatch.setattr(vi, "get_meta_mode", _mode)
    result = await _service().process_intent(
        message="clear my todos", session_id=_SID + "-clear", user_id=_USER
    )
    assert _wrote(boundary) == []
    assert result.requires_clarification
    if stored:
        assert result.message == variant_two_always_ask_question()


# ── CXO 11-06 11:2x: a named miss with no list, and several numbers on the pick ──


@pytest.mark.asyncio
async def test_a_named_complete_that_matches_nothing_says_so_and_arms_nothing(boundary):
    service = _service()
    sid = _SID + "-miss"
    result = await service.process_intent(
        message="mark water the plants as done", session_id=sid, user_id=_USER
    )
    assert result.message == (
        'I couldn\'t find a todo called "water the plants", so nothing was changed. '
        'Say "show my todos" to see them.'
    )
    assert _wrote(boundary) == []
    assert service.workflow_offer_service.peek_pending_offer(sid, _USER) is None


@pytest.mark.asyncio
async def test_several_numbers_on_the_pick_reask_one_at_a_time_and_never_complete(boundary):
    _shown(boundary)
    service = _service()
    await service.process_intent(message="complete the second one", session_id=_SID, user_id=_USER)
    ask = await service.process_intent(message="1 and 3", session_id=_SID, user_id=_USER)
    assert ask.message == "I can take one number at a time here. Which one should I complete?"
    assert _wrote(boundary) == []
    done = await service.process_intent(message="2", session_id=_SID, user_id=_USER)
    assert boundary["completed"] == [boundary["todos"][1].id]
    assert "high task" in done.message


@pytest.mark.asyncio
async def test_several_numbers_twice_releases_the_pick_and_writes_nothing(boundary):
    _shown(boundary)
    service = _service()
    await service.process_intent(message="complete the second one", session_id=_SID, user_id=_USER)
    await service.process_intent(message="1 and 3", session_id=_SID, user_id=_USER)
    second = await service.process_intent(message="1 and 3", session_id=_SID, user_id=_USER)
    assert second.message != "I can take one number at a time here. Which one should I complete?"
    assert _wrote(boundary) == []


# ── multi-intent: a CONVERSATION write sibling (Arch 11-06 11:38) ──


@pytest.mark.asyncio
async def test_conversation_write_sibling_writes_nothing_ask_pending_arch(boundary, monkeypatch):
    """Pins only what holds today: nothing is written and nothing claims it was done.

    The "the confirm/ask arms" half of Arch's pin is PENDING ARCH. Gap (pre-existing):
    the multi-intent partition in ``_process_intent_internal`` checks only
    ``_substantive_intents``, which exclude CONVERSATION, so the
    ``_is_orchestratable_sibling`` guard never sees a CONVERSATION write; the plan runs
    every intent and the orchestrator hands it to ``CanonicalHandlers.handle`` (the
    conversation handler), which writes nothing and arms nothing. Proposed one-line fix
    (not built): in the partition, also put any non-substantive intent for which
    ``self._is_floor_category_write(i)`` holds into ``_floor_routed_siblings``, so the
    #1763 branch runs the single path with it, marked, and the rail asks.
    """
    from services.intent_service.pre_classifier import MultiIntentResult

    def _sibling(category, action, text):
        return Intent(
            category=category,
            action=action,
            confidence=0.9,
            original_message=text,
            context={"original_message": text},
        )

    async def _classify_multiple(self, message, *args, **kwargs):
        return MultiIntentResult(
            intents=[
                _sibling(IntentCategory.TEMPORAL, "get_current_time", "what time is it"),
                _sibling(IntentCategory.TEMPORAL, "get_current_date", "what's the date"),
                _sibling(IntentCategory.CONVERSATION, "complete_todo", "mark high task as done"),
            ],
            original_message=message,
            is_multi_intent=True,
        )

    monkeypatch.setattr(IntentClassifier, "classify_multiple", _classify_multiple)
    result = await _service().process_intent(
        message="what time is it, what's the date, and mark high task as done",
        session_id=_SID + "-multi",
        user_id=_USER,
    )
    assert _wrote(boundary) == []
    assert not any(t.completed for t in boundary["todos"])
    lowered = (result.message or "").lower()
    assert "marked" not in lowered and "as done" not in lowered and "high task" not in lowered
