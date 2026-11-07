"""#2219 Gap A on the legacy complete path (Arch 11-06 17:52; PA's served run on
34efff2af8): "complete review prs" listed matches by storage position (2, 6, 7) and
pulled in "review the deployment plan" by a 0.3 overlap. After a grouped "show my
todos", complete now names todos by the delete gate's word-subset rule and numbers
them by the lines shown; "complete todo N" means line N; a grouped line asks CXO's
one-or-all question (armed).

Drives the REAL ``IntentService.process_intent``; only the LLM boundary (a legacy
``complete_todo`` emission, no router args) and the todo store are replaced."""

import json
from uuid import uuid4

import pytest

from services.domain.models import Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2219-4c00-9e00-000000002220"
_SID = "e2e-2219-complete-shown"


class _CompleteEmission:
    async def complete(self, task_type=None, **kwargs):
        return json.dumps(
            {
                "category": "execution",
                "action": "complete_todo",
                "confidence": 0.9,
                "reasoning": "complete a todo",
            }
        )


def _todo(text, priority="medium"):
    return Todo(id=str(uuid4()), text=text, priority=priority, status="pending", completed=False)


@pytest.fixture
def store(monkeypatch):
    from services.todo.todo_management_service import TodoManagementService

    # Storage order: urgent, review prs ×3, review the deployment plan, zz one.
    state = {
        "todos": [
            _todo("urgent task", "urgent"),
            _todo("review prs"),
            _todo("review prs"),
            _todo("review prs"),
            _todo("review the deployment plan"),
            _todo("zz one"),
        ],
        "completed": [],
    }

    async def _list_todos(self, user_id, include_completed=False):
        return [t for t in state["todos"] if t.id not in state["completed"]]

    async def _complete(self, todo_id, user_id):
        state["completed"].append(str(todo_id))
        row = next(t for t in state["todos"] if t.id == str(todo_id))
        return row

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "complete_todo", _complete)
    t = state["todos"]
    # Shown lines: 1 urgent, 2 review prs (×3), 3 review the deployment plan, 4 zz one.
    lines = [[t[0]], [t[1], t[2], t[3]], [t[4]], [t[5]]]
    TodoIntentHandlers._remember_numbered_list(
        _SID,
        _USER,
        "todos",
        [line[0].id for line in lines],
        [line[0].text for line in lines],
        groups=[[x.id for x in line] for line in lines],
    )
    return state


def _service():
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_CompleteEmission()))


@pytest.mark.asyncio
async def test_complete_todo_n_completes_the_line_shown(store):
    await _service().process_intent(message="complete todo 4", session_id=_SID, user_id=_USER)
    # Storage row 4 is a "review prs" copy; line 4 as shown is "zz one".
    assert store["completed"] == [store["todos"][5].id]


@pytest.mark.asyncio
async def test_complete_todo_n_on_a_grouped_line_asks_one_or_all(store):
    result = await _service().process_intent(
        message="complete todo 2", session_id=_SID, user_id=_USER
    )
    assert result.message == '"review prs" is on your list 3 times. Complete one, or all 3?'
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_a_name_is_matched_by_every_word_and_numbered_by_the_lines_shown(store):
    """'review prs' no longer pulls in 'review the deployment plan', and its three copies
    are one grouped line: the one-or-all question, not a match list."""
    result = await _service().process_intent(
        message="complete review prs", session_id=_SID, user_id=_USER
    )
    assert result.message == '"review prs" is on your list 3 times. Complete one, or all 3?'
    assert "deployment" not in result.message
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_the_one_or_all_question_is_armed_and_one_completes_one_copy(store):
    service = _service()
    await service.process_intent(message="complete todo 2", session_id=_SID, user_id=_USER)
    await service.process_intent(message="one", session_id=_SID, user_id=_USER)
    assert len(store["completed"]) == 1
    assert store["completed"][0] in {t.id for t in store["todos"][1:4]}
