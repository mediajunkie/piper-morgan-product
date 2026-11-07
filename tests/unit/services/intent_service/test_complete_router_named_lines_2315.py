"""#2315 (PA's served run on 0af6078171, 11-06 20:43): "complete the X todo" reaches
the ROUTER-TARGET complete path (``handle_complete_todo_targets``, the router names
``complete_todo`` with ``targets``), which never read the lines the person saw:

- "complete the review prs todo" asked to complete BOTH copies of line 4 and dropped
  line 8 ("review prs for harbor pilot");
- "complete the review todo" said 'I couldn't find "review"' and re-listed by storage
  numbers, unarmed.

Now one named target reads the shown lines the way the legacy complete and the delete
gate do (every named word in the title, #2169): several lines → the ARMED pick labelled
by the shown numbers (CXO 18:32/18:47); copies of one line → the armed one-or-all
question; no match → CXO's line, nothing armed; with no list → the pick 1..k (19:22).

Drives the REAL ``IntentService.process_intent``. The router emission is the only
classification replaced (a ``complete_todo`` Intent carrying ``inversion_args``, as
``test_floor_category_write_2219.py`` does); every other turn classifies through the
real classifier over a pinned LLM. The todo store is replaced."""

import json
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2315-4c00-9e00-000000002315"
_TAIL = "Say the number or the name, or 'never mind' to leave them alone."

# What the router names for each ask (PA's served phrasings and the pins' own).
_ROUTED = {
    "complete the review prs todo": "name:review prs",
    "complete the review todo": "name:review",
    "complete the call mom todo": "name:call mom",
    "complete the dentist todo": "name:dentist",
    "complete the urgent task todo": "name:urgent task",
}


class _PinnedLLM:
    async def complete(self, task_type=None, **kwargs):
        return json.dumps(
            {
                "category": "conversation",
                "action": "chat",
                "confidence": 0.5,
                "reasoning": "not a routed ask",
            }
        )


def _todo(text, priority="medium"):
    return Todo(id=str(uuid4()), text=text, priority=priority, status="pending", completed=False)


@pytest.fixture
def store(monkeypatch):
    from services.todo.todo_management_service import TodoManagementService

    t = [
        _todo("urgent task", "urgent"),  # 1
        _todo("review the deployment plan"),  # 2
        _todo("call mom"),  # 3 (×2)
        _todo("call mom"),
        _todo("review prs"),  # 4 (×2)
        _todo("review prs"),
        _todo("book flights"),  # 5
        _todo("water plants"),  # 6
        _todo("pay rent"),  # 7
        _todo("review prs for harbor pilot"),  # 8
    ]
    state = {"todos": t, "completed": [], "sid": f"e2e-2315-{uuid4()}"}

    async def _list_todos(self, user_id, include_completed=False):
        return [x for x in state["todos"] if x.id not in state["completed"]]

    async def _complete(self, todo_id, user_id):
        state["completed"].append(str(todo_id))
        return next(x for x in state["todos"] if x.id == str(todo_id))

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "complete_todo", _complete)

    original = IntentClassifier.classify

    async def _classify(self, message=None, *args, **kwargs):
        msg = message or kwargs.get("text") or ""
        if msg in _ROUTED:
            return Intent(
                category=IntentCategory.EXECUTION,
                action="complete_todo",
                confidence=0.95,
                original_message=msg,
                context={
                    "original_message": msg,
                    "inversion_args": {"targets": [_ROUTED[msg]]},
                },
            )
        return await original(self, message, *args, **kwargs)

    monkeypatch.setattr(IntentClassifier, "classify", _classify)
    return state


def _show(state):
    """What "show my todos" records: one entry per line, every copy's id."""
    t = state["todos"]
    lines = [[t[0]], [t[1]], [t[2], t[3]], [t[4], t[5]], [t[6]], [t[7]], [t[8]], [t[9]]]
    TodoIntentHandlers._remember_numbered_list(
        state["sid"],
        _USER,
        "todos",
        [line[0].id for line in lines],
        [line[0].text for line in lines],
        groups=[[x.id for x in line] for line in lines],
    )


def _service():
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_PinnedLLM()))


async def _turn(service, store, message):
    return await service.process_intent(message=message, session_id=store["sid"], user_id=_USER)


def _armed(service, store):
    return service.workflow_offer_service.peek_pending_offer(store["sid"], _USER) is not None


# --- after "show my todos" ---------------------------------------------------------


@pytest.mark.asyncio
async def test_review_prs_over_a_grouped_line_and_another_line_asks_the_labelled_pick(store):
    _show(store)
    service = _service()
    result = await _turn(service, store, "complete the review prs todo")
    assert result.message == (
        "Which todo should I complete?\n"
        "4. review prs (×2)\n"
        "8. review prs for harbor pilot\n"
        "\n" + _TAIL
    )
    assert _armed(service, store)
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_the_label_completes_its_line(store):
    _show(store)
    service = _service()
    await _turn(service, store, "complete the review prs todo")
    await _turn(service, store, "8")
    assert store["completed"] == [store["todos"][9].id]


@pytest.mark.asyncio
async def test_the_grouped_label_asks_one_or_both(store):
    _show(store)
    service = _service()
    await _turn(service, store, "complete the review prs todo")
    result = await _turn(service, store, "4")
    assert result.message == '"review prs" is on your list 2 times. Complete one, or both?'
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_copies_of_one_shown_line_ask_one_or_both_not_a_batch_confirm(store):
    _show(store)
    service = _service()
    result = await _turn(service, store, "complete the call mom todo")
    assert result.message == '"call mom" is on your list 2 times. Complete one, or both?'
    assert "Complete 2 todos" not in result.message
    await _turn(service, store, "one")
    assert len(store["completed"]) == 1


@pytest.mark.asyncio
async def test_review_asks_the_labelled_pick_over_lines_2_4_8(store):
    _show(store)
    service = _service()
    result = await _turn(service, store, "complete the review todo")
    assert result.message == (
        "Which todo should I complete?\n"
        "2. review the deployment plan\n"
        "4. review prs (×2)\n"
        "8. review prs for harbor pilot\n"
        "\n" + _TAIL
    )
    assert "couldn't find" not in result.message
    assert _armed(service, store)


@pytest.mark.asyncio
async def test_no_match_after_the_list_says_cxos_line_and_arms_nothing(store):
    _show(store)
    service = _service()
    result = await _turn(service, store, "complete the dentist todo")
    assert result.message == (
        'I couldn\'t find a todo called "dentist", so nothing was changed. '
        'Say "show my todos" to see them.'
    )
    assert not _armed(service, store)
    assert store["completed"] == []


@pytest.mark.asyncio
async def test_one_row_still_completes_at_once(store):
    _show(store)
    await _turn(_service(), store, "complete the urgent task todo")
    assert store["completed"] == [store["todos"][0].id]


# --- no list shown -----------------------------------------------------------------


@pytest.mark.asyncio
async def test_no_list_several_todos_ask_the_pick_1_to_k(store):
    service = _service()
    result = await _turn(service, store, "complete the review todo")
    assert result.message == (
        "Which todo should I complete?\n"
        "1. review the deployment plan\n"
        "2. review prs (×2)\n"
        "3. review prs for harbor pilot\n"
        "\n" + _TAIL
    )
    assert _armed(service, store)
    await _turn(service, store, "3")
    assert store["completed"] == [store["todos"][9].id]
