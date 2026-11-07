"""#2219 Gap A follow-up (CXO 11-06 18:32 words, 18:47 binding; Arch 18:45 mechanism):
a named delete or complete that matches SEVERAL lines of the grouped "show my todos"
list asks the ARMED #1987 pick over those lines, each labelled with the number the
person saw. It replaces the unarmed "I found N todos matching … Try 'delete todo
[number]'" text (#1730: never a list shown with nothing armed).

Binding (CXO 18:47): a number binds the candidate whose LABEL it is; a number that is
not a label re-asks; an ordinal word binds by the pick's position, unless that
ordinal's number is a DIFFERENT candidate's label, which re-asks once with CXO's
words. "never mind" declines as the pick always has.

Drives the REAL ``IntentService.process_intent``; only the LLM boundary (a legacy
``delete_todo`` / ``complete_todo`` emission, no router args) and the todo store are
replaced, as in ``test_delete_pick_shown_lines_2219.py`` and
``test_complete_shown_lines_2219.py``."""

import json
from uuid import uuid4

import pytest

from services.domain.models import Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2219-4c00-9e00-000000002221"

_TAIL = "Say the number or the name, or 'never mind' to leave them alone."


class _Emission:
    def __init__(self, action):
        self.action = action

    async def complete(self, task_type=None, **kwargs):
        return json.dumps(
            {
                "category": "execution",
                "action": self.action,
                "confidence": 0.9,
                "reasoning": f"{self.action} a named todo",
            }
        )


def _todo(text, priority="medium"):
    return Todo(id=str(uuid4()), text=text, priority=priority, status="pending", completed=False)


@pytest.fixture
def store(monkeypatch):
    from services.todo.todo_management_service import TodoManagementService

    t = [
        _todo("urgent task", "urgent"),
        _todo("review prs"),
        _todo("review prs"),
        _todo("review prs"),
        _todo("write spec draft"),
        _todo("call mom"),
        _todo("write spec final"),
        _todo("review prs for alpha"),
    ]
    state = {"todos": t, "deleted": [], "completed": [], "sid": f"e2e-2219-named-{uuid4()}"}

    async def _list_todos(self, user_id, include_completed=False):
        gone = set(state["deleted"]) | set(state["completed"])
        return [x for x in state["todos"] if x.id not in gone]

    async def _delete(self, todo_id, user_id):
        state["deleted"].append(str(todo_id))
        return True

    async def _complete(self, todo_id, user_id):
        state["completed"].append(str(todo_id))
        return next(x for x in state["todos"] if x.id == str(todo_id))

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    monkeypatch.setattr(TodoManagementService, "complete_todo", _complete)
    # Shown lines: 1 urgent task (urgent), 2 review prs (×3), 3 write spec draft,
    # 4 call mom, 5 write spec final, 6 review prs for alpha.
    lines = [[t[0]], [t[1], t[2], t[3]], [t[4]], [t[5]], [t[6]], [t[7]]]
    TodoIntentHandlers._remember_numbered_list(
        state["sid"],
        _USER,
        "todos",
        [line[0].id for line in lines],
        [line[0].text for line in lines],
        groups=[[x.id for x in line] for line in lines],
    )
    return state


def _service(action):
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_Emission(action)))


async def _turn(service, store, message):
    return await service.process_intent(message=message, session_id=store["sid"], user_id=_USER)


_DELETE_PICK = (
    "Which todo should I delete?\n" "2. review prs (×3)\n" "6. review prs for alpha\n" "\n" + _TAIL
)
_COMPLETE_PICK = (
    "Which todo should I complete?\n"
    "2. review prs (×3)\n"
    "6. review prs for alpha\n"
    "\n" + _TAIL
)
_COLLISION = (
    "Do you mean the line numbered 2, or the second one in this list? "
    "Say the number shown next to it, or the name."
)


# --- delete -------------------------------------------------------------------


@pytest.mark.asyncio
async def test_named_delete_over_several_lines_asks_the_armed_pick_labelled_as_shown(store):
    service = _service("delete_todo")
    result = await _turn(service, store, "delete the review prs todos")
    assert result.message == _DELETE_PICK
    assert "I found" not in result.message
    assert service.workflow_offer_service.peek_pending_offer(store["sid"], _USER) is not None
    assert store["deleted"] == []


@pytest.mark.asyncio
async def test_a_label_binds_its_line_and_arms_the_existing_confirm(store):
    service = _service("delete_todo")
    await _turn(service, store, "delete the review prs todos")
    confirm = await _turn(service, store, "6")
    assert confirm.message == 'Delete the todo "review prs for alpha"? (yes/no)'
    assert store["deleted"] == []
    await _turn(service, store, "yes")
    assert store["deleted"] == [store["todos"][7].id]


@pytest.mark.asyncio
async def test_a_hash_label_binds_the_grouped_line_with_its_count(store):
    service = _service("delete_todo")
    await _turn(service, store, "delete the review prs todos")
    confirm = await _turn(service, store, "#2")
    assert confirm.message == 'Delete one of your 3 "review prs" todos? (yes/no)'


@pytest.mark.asyncio
async def test_an_ordinal_whose_number_is_another_label_re_asks(store):
    service = _service("delete_todo")
    await _turn(service, store, "delete the review prs todos")
    result = await _turn(service, store, "the second one")
    assert result.message == _COLLISION
    assert store["deleted"] == []
    # Still armed: the number shown next to it then binds.
    confirm = await _turn(service, store, "6")
    assert confirm.message == 'Delete the todo "review prs for alpha"? (yes/no)'


@pytest.mark.asyncio
async def test_an_ordinal_with_no_collision_binds_by_position(store):
    service = _service("delete_todo")
    await _turn(service, store, "delete the review prs todos")
    # "first" is 1, not a label here: position 1 is line 2.
    confirm = await _turn(service, store, "the first one")
    assert confirm.message == 'Delete one of your 3 "review prs" todos? (yes/no)'


@pytest.mark.asyncio
async def test_the_last_one_binds_the_last_position(store):
    service = _service("delete_todo")
    await _turn(service, store, "delete the review prs todos")
    confirm = await _turn(service, store, "the last one")
    assert confirm.message == 'Delete the todo "review prs for alpha"? (yes/no)'


@pytest.mark.asyncio
async def test_labels_three_and_five_the_second_one_is_line_five(store):
    service = _service("delete_todo")
    pick = await _turn(service, store, "delete the write spec todos")
    assert pick.message == (
        "Which todo should I delete?\n" "3. write spec draft\n" "5. write spec final\n" "\n" + _TAIL
    )
    confirm = await _turn(service, store, "the second one")
    assert confirm.message == 'Delete the todo "write spec final"? (yes/no)'


@pytest.mark.asyncio
async def test_a_number_that_is_not_a_label_re_asks_the_pick(store):
    service = _service("delete_todo")
    await _turn(service, store, "delete the review prs todos")
    result = await _turn(service, store, "1")
    assert result.message == (
        "Still not sure which todo you mean — you have:\n"
        "2. review prs (×3)\n"
        "6. review prs for alpha\n"
        "\n" + _TAIL
    )
    assert store["deleted"] == []


@pytest.mark.asyncio
async def test_never_mind_declines(store):
    service = _service("delete_todo")
    await _turn(service, store, "delete the review prs todos")
    result = await _turn(service, store, "never mind")
    assert result.message == "Okay — I haven't touched your todos. Nothing has been deleted."
    assert store["deleted"] == []


@pytest.mark.asyncio
async def test_one_match_keeps_the_confirm(store):
    result = await _turn(_service("delete_todo"), store, "delete the call mom todo")
    assert result.message == 'Delete the todo "call mom"? (yes/no)'


@pytest.mark.asyncio
async def test_no_match_says_so_and_arms_nothing(store):
    service = _service("delete_todo")
    result = await _turn(service, store, "delete the dentist todo")
    assert result.message == (
        'I couldn\'t find a todo called "dentist", so nothing was changed. '
        'Say "show my todos" to see them.'
    )
    assert service.workflow_offer_service.peek_pending_offer(store["sid"], _USER) is None
    assert store["deleted"] == []


# --- complete -----------------------------------------------------------------


@pytest.mark.asyncio
async def test_named_complete_over_several_lines_asks_the_armed_pick(store):
    service = _service("complete_todo")
    result = await _turn(service, store, "complete review prs")
    assert result.message == _COMPLETE_PICK
    assert service.workflow_offer_service.peek_pending_offer(store["sid"], _USER) is not None
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_complete_a_label_completes_that_line(store):
    service = _service("complete_todo")
    await _turn(service, store, "complete review prs")
    await _turn(service, store, "6")
    assert store["completed"] == [store["todos"][7].id]


@pytest.mark.asyncio
async def test_complete_a_grouped_label_asks_one_or_all(store):
    service = _service("complete_todo")
    await _turn(service, store, "complete review prs")
    result = await _turn(service, store, "2")
    assert result.message == '"review prs" is on your list 3 times. Complete one, or all 3?'
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_complete_collision_re_asks(store):
    service = _service("complete_todo")
    await _turn(service, store, "complete review prs")
    result = await _turn(service, store, "the second one")
    assert result.message == _COLLISION
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_complete_never_mind_declines(store):
    service = _service("complete_todo")
    await _turn(service, store, "complete review prs")
    result = await _turn(service, store, "never mind")
    assert result.message == "Okay — I haven't touched your todos. Nothing has been changed."
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_complete_no_match_says_so(store):
    result = await _turn(_service("complete_todo"), store, "complete the dentist")
    assert result.message == (
        'I couldn\'t find a todo called "dentist", so nothing was changed. '
        'Say "show my todos" to see them.'
    )
    assert store["completed"] == []
