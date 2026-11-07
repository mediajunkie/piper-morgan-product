"""#2294 (PA's served run on e64de73062, 3 of 3): after a list, a bare "delete the
first one" reached the generic "I didn't recognize that" decline.

Why: the live router answers CLARIFY on that phrasing (0.30 ×3 in Lead's 11-06 probe:
no object and no history), so the legacy classifier runs and emits
EXECUTION/delete_item, which was no rail key. The fix is the #1527 alias discipline:
``delete_item`` is a rail alias of the delete_todo entry and a member of
``_DELETE_TODO_FAMILY``, so it reaches the built delete path, which always confirms.

These drive the REAL ``IntentService.process_intent`` and classifier chain; the only
mocked seam is the LLM boundary, which returns a verb-less ``delete_item`` emission
(the action PA's transcript names; the full live emission was not captured).
"""

import datetime as _dt
import json
from uuid import uuid4

import pytest

from services.domain.models import Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.delete_todo_pick import (
    DELETE_ITEM_NO_LIST_LEAD,
    KIND_CHOICE_DECLINE,
    KIND_CHOICE_QUESTION,
    KIND_CHOICE_SHORT_QUESTION,
)
from services.intent_service.destructive_confirm import is_delete_todo_action
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.unwired_writes import GENERIC_UNWIRED_WRITE_DECLINE
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2294-4b00-9e00-000000002294"

_EMISSION = {
    "category": "execution",
    "action": "delete_item",
    "confidence": 0.9,
    "reasoning": "The user asks to delete an item from the list just shown.",
    "helpful_knowledge_domains": [],
    "ambiguity_notes": [],
    "knowledge_used": [],
}


class _PinnedEmissionLLM:
    def __init__(self, emission: dict):
        self._payload = json.dumps(emission)

    async def complete(self, task_type=None, **kwargs):
        if task_type != "intent_classification":
            raise AssertionError(f"LLM boundary touched for task_type={task_type!r}")
        return self._payload

    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name}) beyond complete()")


def _todo(text, reminder=False):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=(
            _dt.datetime(2026, 11, 7, 17, 0, tzinfo=_dt.timezone.utc) if reminder else None
        ),
    )


@pytest.fixture
def todo_boundary(monkeypatch):
    from services.todo.todo_management_service import TodoManagementService

    state = {"todos": [_todo("call mom", reminder=True), _todo("call the dentist")]}

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        raise AssertionError("delete fired without a confirmed yes")

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


def _service():
    register_default_workflows()
    return IntentService(
        intent_classifier=IntentClassifier(llm_service=_PinnedEmissionLLM(_EMISSION))
    )


def test_delete_item_is_the_delete_todo_entry_and_in_the_confirm_family():
    register_default_workflows()
    wf = get_action_workflows()
    assert wf["delete_item"] is wf["delete_todo"]
    assert is_delete_todo_action("delete_item")


@pytest.mark.asyncio
async def test_after_a_list_it_reaches_the_armed_delete_pick_not_the_decline(todo_boundary):
    """The legacy emission carries no target, so the built delete path asks its armed
    #1987 pick (numbered candidates); nothing is deleted on this turn."""
    sid = "e2e-2294-after-list"
    reminder = todo_boundary["todos"][0]
    TodoIntentHandlers._remember_numbered_list(
        sid, _USER, "reminders", [reminder.id], [reminder.text]
    )
    result = await _service().process_intent(
        message="delete the first one", session_id=sid, user_id=_USER
    )
    assert result.message != GENERIC_UNWIRED_WRITE_DECLINE
    assert "didn't recognize" not in result.message
    # The last list was reminders, so the pick says "reminder" and lists reminders only.
    assert result.message.startswith("Which reminder should I delete?")
    assert "1. call mom" in result.message
    assert "call the dentist" not in result.message


@pytest.mark.asyncio
async def test_with_no_list_shown_it_reshows_instead_of_the_generic_decline(todo_boundary):
    result = await _service().process_intent(
        message="delete the first one", session_id="e2e-2294-no-list", user_id=_USER
    )
    assert "didn't recognize" not in result.message
    assert result.message != GENERIC_UNWIRED_WRITE_DECLINE
    # #2321 (Arch 14:41 (d); CXO 14:44): no presumption of todos, but an ARMED
    # closed choice of kind, so the answer never reaches the floor.
    assert result.message == f"{DELETE_ITEM_NO_LIST_LEAD}\n\n{KIND_CHOICE_QUESTION}"
    assert "Which todo" not in result.message
    assert result.requires_clarification is True


async def _ask_then(service, sid, *answers):
    await service.process_intent(message="delete the first one", session_id=sid, user_id=_USER)
    out = None
    for a in answers:
        out = await service.process_intent(message=a, session_id=sid, user_id=_USER)
    return out


@pytest.mark.asyncio
async def test_kind_choice_todos_shows_the_todo_list_with_the_armed_delete_question(
    todo_boundary,
):
    out = await _ask_then(_service(), "e2e-2321-todos", "todos")
    assert out.message.startswith("I haven't shown you a numbered list yet. Here are your todos:")
    assert '"call the dentist"' in out.message
    assert out.message.endswith(
        "Which one should I delete? Say the number or the name, or 'never mind' "
        "to leave them alone."
    )


@pytest.mark.asyncio
async def test_kind_choice_reminders_shows_the_reminders(todo_boundary):
    out = await _ask_then(_service(), "e2e-2321-rem", "reminders")
    assert out.message.startswith(
        "I haven't shown you a numbered list yet. Here are your reminders:"
    )
    assert '"call mom"' in out.message and "call the dentist" not in out.message


@pytest.mark.asyncio
async def test_kind_choice_never_mind_is_the_decline(todo_boundary):
    out = await _ask_then(_service(), "e2e-2321-nm", "never mind")
    assert out.message == KIND_CHOICE_DECLINE


@pytest.mark.asyncio
async def test_a_stray_answer_asks_once_more_then_declines(todo_boundary):
    """CXO 14:44: a bare 2 names no kind — the short question once, then the decline;
    never the floor."""
    service = _service()
    sid = "e2e-2321-stray"
    first = await _ask_then(service, sid, "2")
    assert first.message == KIND_CHOICE_SHORT_QUESTION
    second = await service.process_intent(message="2", session_id=sid, user_id=_USER)
    assert second.message == KIND_CHOICE_DECLINE


@pytest.mark.asyncio
async def test_an_ask_that_names_reminders_skips_the_question(todo_boundary):
    out = await _service().process_intent(
        message="delete the second reminder", session_id="e2e-2321-named", user_id=_USER
    )
    assert out.message.startswith(
        "I haven't shown you a numbered list yet. Here are your reminders:"
    )


@pytest.mark.asyncio
async def test_a_typed_delete_todo_still_asks_which_todo_with_no_list(todo_boundary):
    """The gate is the invented noun's only: a real delete_todo emission keeps today's pick."""
    register_default_workflows()
    emission = dict(_EMISSION, action="delete_todo")
    service = IntentService(
        intent_classifier=IntentClassifier(llm_service=_PinnedEmissionLLM(emission))
    )
    result = await service.process_intent(
        message="delete a todo", session_id="e2e-2294-typed", user_id=_USER
    )
    assert result.message.startswith("Which todo should I delete?")


# Arch 11-06 15:59: the plural invented noun ("delete review prs and urgent task",
# PA's served run on 7ffd460640) is the same entry under the same 08:06 conditions.
def test_delete_items_is_the_delete_todo_entry_and_in_the_confirm_family():
    register_default_workflows()
    wf = get_action_workflows()
    assert wf["delete_items"] is wf["delete_todo"]
    assert is_delete_todo_action("delete_items")


@pytest.mark.asyncio
async def test_delete_items_with_no_list_gets_the_honest_ask(todo_boundary):
    register_default_workflows()
    service = IntentService(
        intent_classifier=IntentClassifier(
            llm_service=_PinnedEmissionLLM(dict(_EMISSION, action="delete_items"))
        )
    )
    result = await service.process_intent(
        message="delete review prs and urgent task", session_id="e2e-items-none", user_id=_USER
    )
    assert "didn't recognize" not in result.message
    assert result.message == f"{DELETE_ITEM_NO_LIST_LEAD}\n\n{KIND_CHOICE_QUESTION}"
