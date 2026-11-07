"""#2219 interim (c) (Arch 11-06 09:58; CXO's words 10:11): a delete that reaches the
pick with no router target, right after the numbered "show my todos" list, picks over
THAT list's lines, in its order, grouping and chips; a grouped line takes the one-copy
confirm with its count (xian's #2019 cap), and the result says what's left.

PA's served row 5 (0d4938cf23): "delete the second one" after the list reached the
pick over an UNgrouped five-line list that contradicted what the person had just seen.

Drives the REAL ``IntentService.process_intent`` and classifier chain; the only mocked
seam is the LLM boundary (the legacy ``delete_item`` emission, as #2294's pins do).
"""

import json
from uuid import uuid4

import pytest

from services.domain.models import Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2219-4c00-9e00-000000002219"
_SID = "e2e-2219-pick-shown"

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
    async def complete(self, task_type=None, **kwargs):
        if task_type != "intent_classification":
            raise AssertionError(f"LLM boundary touched for task_type={task_type!r}")
        return json.dumps(_EMISSION)


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
        "deleted": [],
    }

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        state["deleted"].append(str(todo_id))
        state["todos"] = [t for t in state["todos"] if t.id != str(todo_id)]
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


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


def _service():
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_PinnedEmissionLLM()))


_PICK = (
    "Which todo should I delete?\n"
    "1. urgent task (urgent)\n"
    "2. high task (high)\n"
    "3. review prs (×3)\n"
    "\n"
    "Say the number or the name, or 'never mind' to leave them alone."
)


@pytest.mark.asyncio
async def test_after_the_list_the_pick_shows_the_lines_as_the_list_did(boundary):
    _shown(boundary)
    result = await _service().process_intent(
        message="delete the second one", session_id=_SID, user_id=_USER
    )
    assert result.message == _PICK
    assert boundary["deleted"] == []


@pytest.mark.asyncio
async def test_a_grouped_line_confirms_one_copy_with_its_count_and_says_whats_left(boundary):
    _shown(boundary)
    service = _service()
    await service.process_intent(message="delete the second one", session_id=_SID, user_id=_USER)
    confirm = await service.process_intent(message="3", session_id=_SID, user_id=_USER)
    assert confirm.message == 'Delete one of your 3 "review prs" todos? (yes/no)'
    assert boundary["deleted"] == []
    done = await service.process_intent(message="yes", session_id=_SID, user_id=_USER)
    assert len(boundary["deleted"]) == 1
    assert done.message == 'Deleted one "review prs". 2 are left on your list.'


@pytest.mark.asyncio
async def test_a_one_copy_line_keeps_the_one_item_confirm(boundary):
    _shown(boundary)
    service = _service()
    await service.process_intent(message="delete the second one", session_id=_SID, user_id=_USER)
    confirm = await service.process_intent(message="2", session_id=_SID, user_id=_USER)
    assert confirm.message == 'Delete the todo "high task"? (yes/no)'
    assert boundary["deleted"] == []


# ---------------------------------------------------------------------------
# PA's served run on 34efff2af8 (11-06 17:33): the gate's named and numbered legs
# numbered by storage order, so after a grouped list "delete the review prs todos"
# listed the three copies as lines 2, 6 and 7, and "delete todo 5" bound the 5th row
# in storage, not line 5 as shown. Both now read the shown lines (CXO 07:35).
# ---------------------------------------------------------------------------


class _DeleteTodoEmission:
    async def complete(self, task_type=None, **kwargs):
        return json.dumps(dict(_EMISSION, action="delete_todo"))


def _gate_service():
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_DeleteTodoEmission()))


def _shown_with_tail(state):
    """Lines: 1 urgent, 2 high, 3 review prs (×3), 4 zz one. Storage puts zz one 6th."""
    state["todos"].append(_todo("zz one"))
    t = state["todos"]
    lines = [[t[0]], [t[1]], [t[2], t[3], t[4]], [t[5]]]
    TodoIntentHandlers._remember_numbered_list(
        _SID,
        _USER,
        "todos",
        [line[0].id for line in lines],
        [line[0].text for line in lines],
        groups=[[x.id for x in line] for line in lines],
    )


@pytest.mark.asyncio
async def test_a_named_grouped_line_asks_one_of_your_n_on_the_gate_path(boundary):
    _shown_with_tail(boundary)
    service = _gate_service()
    confirm = await service.process_intent(
        message="delete the review prs todos", session_id=_SID, user_id=_USER
    )
    assert confirm.message == 'Delete one of your 3 "review prs" todos? (yes/no)'
    assert boundary["deleted"] == []
    done = await service.process_intent(message="yes", session_id=_SID, user_id=_USER)
    assert len(boundary["deleted"]) == 1
    assert done.message == 'Deleted one "review prs". 2 are left on your list.'


@pytest.mark.asyncio
async def test_delete_todo_n_binds_the_line_shown_not_the_storage_row(boundary):
    _shown_with_tail(boundary)
    confirm = await _gate_service().process_intent(
        message="delete todo 4", session_id=_SID, user_id=_USER
    )
    # Storage row 4 is a "review prs" copy; line 4 as shown is "zz one".
    assert confirm.message == 'Delete the todo "zz one"? (yes/no)'
    assert boundary["deleted"] == []


@pytest.mark.asyncio
async def test_delete_todo_n_on_a_grouped_line_says_its_count(boundary):
    _shown_with_tail(boundary)
    confirm = await _gate_service().process_intent(
        message="delete todo 3", session_id=_SID, user_id=_USER
    )
    assert confirm.message == 'Delete one of your 3 "review prs" todos? (yes/no)'
