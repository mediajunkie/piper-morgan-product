"""#2316 (Arch 11-06 21:31 mechanism; CXO 21:32 words): an answer to an armed todo
pick that NAMES a todo containing a number ("call 3 vendors") used to bind the number
as a position or label, so it could pick a different todo, and on a complete pick
over a single-copy line it wrote at once.

Now the pick compares the binder's two readings of the same answer over the recorded
candidates: the number (position or label) and the name. When both bind and they name
DIFFERENT candidates, neither binds: CXO's two-line re-ask, once, on the same record.
When they agree, or only one binds, the pick binds as before.

Drives the REAL ``IntentService.process_intent``; only the LLM emission and the todo
store are replaced."""

import json
from uuid import uuid4

import pytest

from services.domain.models import Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2316-4c00-9e00-000000002316"
_TAIL = "Which one? Say the number shown next to it, or 'never mind' to leave them alone."


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


def _make_store(monkeypatch, texts):
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": [_todo(t) for t in texts],
        "deleted": [],
        "completed": [],
        "sid": f"e2e-2316-{uuid4()}",
    }

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
    return state


# No list shown: the "call" pick is 1. call mom, 2. call 3 vendors, 3. call the bank,
# 4. call 4 people. "call 3 vendors" reads 3 by number (call the bank) and 2 by name.
@pytest.fixture
def plain(monkeypatch):
    return _make_store(
        monkeypatch, ["call mom", "call 3 vendors", "pay rent", "call the bank", "call 4 people"]
    )


# After "show my todos": 1 pay rent, 2 call mom, 3 water plants, 4 call 6 vendors,
# 5 book flights, 6 call the bank (×2). The "call" pick is labelled 2, 4, 6;
# "call 6 vendors" reads label 6 (call the bank) by number and line 4 by name.
@pytest.fixture
def shown(monkeypatch):
    state = _make_store(
        monkeypatch,
        [
            "pay rent",
            "call mom",
            "water plants",
            "call 6 vendors",
            "book flights",
            "call the bank",
            "call the bank",
        ],
    )
    t = state["todos"]
    lines = [[t[0]], [t[1]], [t[2]], [t[3]], [t[4]], [t[5], t[6]]]
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


_PLAIN_CONFLICT = (
    "That could mean two different todos:\n2. call 3 vendors\n3. call the bank\n" + _TAIL
)
_SHOWN_CONFLICT = (
    "That could mean two different todos:\n4. call 6 vendors\n6. call the bank (×2)\n" + _TAIL
)


# --- 1..k pick, delete --------------------------------------------------------------


@pytest.mark.asyncio
async def test_plain_delete_name_with_another_position_re_asks(plain):
    service = _service("delete_todo")
    pick = await _turn(service, plain, "delete the call todos")
    assert pick.message.splitlines()[1:5] == [
        "1. call mom",
        "2. call 3 vendors",
        "3. call the bank",
        "4. call 4 people",
    ]
    result = await _turn(service, plain, "call 3 vendors")
    assert result.message == _PLAIN_CONFLICT
    assert plain["deleted"] == []
    confirm = await _turn(service, plain, "2")
    assert confirm.message == 'Delete the todo "call 3 vendors"? (yes/no)'


@pytest.mark.asyncio
async def test_plain_delete_conflict_then_never_mind_declines(plain):
    service = _service("delete_todo")
    await _turn(service, plain, "delete the call todos")
    await _turn(service, plain, "call 3 vendors")
    result = await _turn(service, plain, "never mind")
    assert result.message == "Okay — I haven't touched your todos. Nothing has been deleted."
    assert plain["deleted"] == []


@pytest.mark.asyncio
async def test_plain_readings_that_agree_bind_as_before(plain):
    service = _service("delete_todo")
    await _turn(service, plain, "delete the call todos")
    confirm = await _turn(service, plain, "call 4 people")
    assert confirm.message == 'Delete the todo "call 4 people"? (yes/no)'


@pytest.mark.asyncio
async def test_plain_name_only_and_number_only_bind_as_before(plain):
    service = _service("delete_todo")
    await _turn(service, plain, "delete the call todos")
    confirm = await _turn(service, plain, "call the bank")
    assert confirm.message == 'Delete the todo "call the bank"? (yes/no)'
    service = _service("delete_todo")
    plain["sid"] = f"e2e-2316-{uuid4()}"
    await _turn(service, plain, "delete the call todos")
    confirm = await _turn(service, plain, "3")
    assert confirm.message == 'Delete the todo "call the bank"? (yes/no)'


# --- 1..k pick, complete --------------------------------------------------------------


@pytest.mark.asyncio
async def test_plain_complete_conflict_writes_nothing_then_the_number_completes(plain):
    service = _service("complete_todo")
    await _turn(service, plain, "complete call")
    result = await _turn(service, plain, "call 3 vendors")
    assert result.message == _PLAIN_CONFLICT
    assert plain["completed"] == []
    await _turn(service, plain, "2")
    assert plain["completed"] == [plain["todos"][1].id]


# --- labelled pick, delete --------------------------------------------------------------


@pytest.mark.asyncio
async def test_labelled_delete_name_with_another_label_re_asks(shown):
    service = _service("delete_todo")
    pick = await _turn(service, shown, "delete the call todos")
    assert pick.message.splitlines()[1:4] == [
        "2. call mom",
        "4. call 6 vendors",
        "6. call the bank (×2)",
    ]
    result = await _turn(service, shown, "call 6 vendors")
    assert result.message == _SHOWN_CONFLICT
    assert shown["deleted"] == []
    confirm = await _turn(service, shown, "4")
    assert confirm.message == 'Delete the todo "call 6 vendors"? (yes/no)'


@pytest.mark.asyncio
async def test_labelled_bare_and_hash_labels_still_bind(shown):
    service = _service("delete_todo")
    await _turn(service, shown, "delete the call todos")
    confirm = await _turn(service, shown, "#4")
    assert confirm.message == 'Delete the todo "call 6 vendors"? (yes/no)'


# --- labelled pick, complete --------------------------------------------------------------


@pytest.mark.asyncio
async def test_labelled_complete_conflict_writes_nothing(shown):
    service = _service("complete_todo")
    await _turn(service, shown, "complete call")
    result = await _turn(service, shown, "call 6 vendors")
    assert result.message == _SHOWN_CONFLICT
    assert shown["completed"] == []
    await _turn(service, shown, "4")
    assert shown["completed"] == [shown["todos"][3].id]


@pytest.mark.asyncio
async def test_labelled_complete_conflict_never_mind_declines(shown):
    service = _service("complete_todo")
    await _turn(service, shown, "complete call")
    await _turn(service, shown, "call 6 vendors")
    result = await _turn(service, shown, "never mind")
    assert result.message == "Okay — I haven't touched your todos. Nothing has been changed."
    assert shown["completed"] == []
