"""#2219 Gap A (CXO 11-06 07:35): the todo list is numbered, and ordinals bind to it.

PA's served run on alpha e64de73062: after "show my todos" (a bulleted list), "complete
the first one" answered "I haven't shown you a numbered list yet" and showed a
different, ungrouped list. CXO's ruling: number the lines, record the list one entry
per LINE (every copy's id kept), and on a grouped line ask one, or all:

- complete: ``"review prs" is on your list 3 times. Complete one, or all 3?``
- delete: ``Delete one "review prs", or all 3? This can't be undone.``

"one" acts on the first copy in list order; "all" / "all 3" / "both" on every copy.
A one-copy line keeps today's behaviour (complete at once; delete always confirms).

Layer: the list formatter, ``TodoIntentHandlers`` (list, complete and delete target
paths) and the ``todo_line_pick`` answer turn, with a stateful in-memory todo service
and the one-slot offer store stubbed. Delete is driven at the handler with router
targets ["1"] (bare "delete the first one" routes elsewhere today, #2294). No LLM,
no DB, no served turn.
"""

from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from services.consciousness.todo_consciousness import format_todo_list_conscious
from services.domain.models import Intent, Todo
from services.intent_service import todo_line_pick as tlp
from services.intent_service.conversation_context import clear_context, get_or_create_context
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

_USER = "5a1e2219-0000-4000-8000-000000002219"
_SESSION = "sess-2219-ordinals"

_COMPLETE_Q = '"review prs" is on your list 3 times. Complete one, or all 3?'
_DELETE_Q = 'Delete one "review prs", or all 3? This can\'t be undone.'


def _todo(text, priority="medium", completed=False):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority=priority,
        status="completed" if completed else "pending",
        completed=completed,
    )


class _TodoService:
    """In-memory rows in list order; complete and delete change them."""

    def __init__(self, rows):
        self.rows = list(rows)
        self.completed_ids = []
        self.deleted_ids = []

    async def list_todos(self, user_id=None, include_completed=False, **_):
        return [t for t in self.rows if include_completed or not t.completed]

    async def complete_todo(self, todo_id, user_id=None):
        for t in self.rows:
            if t.id == str(todo_id):
                t.completed = True
                t.status = "completed"
                self.completed_ids.append(t.id)
                return t
        return None

    async def delete_todo(self, todo_id, user_id=None):
        for t in self.rows:
            if t.id == str(todo_id):
                self.rows.remove(t)
                self.deleted_ids.append(t.id)
                return True
        return False


class _Store:
    def __init__(self):
        self.slot = None

    def set_pending_offer(self, session_id, offer, user_id=None):
        self.slot = offer

    def peek_pending_offer(self, session_id):
        return self.slot

    def get_and_clear_pending_offer(self, session_id, user_id=None):
        offer, self.slot = self.slot, None
        return offer


@pytest.fixture
def rows():
    # CXO's example: urgent, high, then three "review prs".
    return [
        _todo("urgent task", "urgent"),
        _todo("high task", "high"),
        _todo("review prs"),
        _todo("review prs"),
        _todo("review prs"),
    ]


@pytest.fixture
def service(rows):
    return _TodoService(rows)


@pytest.fixture
def store():
    return _Store()


@pytest.fixture
def handlers(service):
    h = TodoIntentHandlers()
    h.todo_service = service
    return h


@pytest.fixture
def intent_service(handlers, store):
    return SimpleNamespace(todo_handlers=handlers, workflow_offer_service=store)


@pytest.fixture(autouse=True)
def _fresh_context():
    clear_context(_SESSION, user_id=_USER)
    yield
    clear_context(_SESSION, user_id=_USER)


@pytest.fixture(autouse=True)
def _no_router(monkeypatch):
    """The answer turn's release discriminator must not call a model."""
    from services.intent_service import inversion_live

    async def _none(*a, **k):
        return None

    monkeypatch.setattr(inversion_live, "read_op_claims_turn", _none)


def _intent(action, message, targets=None):
    ctx = {"original_message": message}
    if targets is not None:
        ctx["inversion_args"] = {"targets": targets}
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=1.0,
        context=ctx,
    )


async def _show(handlers, message="show my todos"):
    return await handlers.handle_list_todos(_intent("list_todos", message), _SESSION, UUID(_USER))


async def _complete(handlers, store, n, message="complete the first one"):
    return await handlers.handle_complete_todo_targets(
        _intent("complete_todo", message, [str(n)]), _SESSION, UUID(_USER), store, _USER
    )


async def _delete(handlers, store, n, message="delete the first one"):
    return await handlers.handle_delete_todo_targets(
        _intent("delete_todo", message, [str(n)]), _SESSION, UUID(_USER), store, _USER
    )


async def _answer(text, intent_service, store):
    return await tlp.handle_todo_group_line_turn(
        store.get_and_clear_pending_offer(_SESSION), text, _SESSION, _USER, intent_service
    )


# ---------------------------------------------------------------------------
# 1. The render: numbered lines, done lines too; the header unchanged
# ---------------------------------------------------------------------------


def test_the_open_list_is_numbered_by_line(rows):
    assert format_todo_list_conscious(rows).split("\n") == [
        "You have 5 open todos. Here they are:",
        "1. urgent task (urgent)",
        "2. high task (high)",
        "3. review prs (×3)",
    ]


def test_done_lines_are_numbered_and_keep_done():
    todos = [_todo("a"), _todo("b", completed=True), _todo("b", completed=True)]
    assert format_todo_list_conscious(todos, include_completed=True).split("\n") == [
        "You have 1 open todo and 2 done. Here they are:",
        "1. a",
        "2. b (×2) ✓ done",
    ]


def test_one_line_still_says_here_it_is():
    assert format_todo_list_conscious([_todo("a"), _todo("a")]) == (
        "You have 2 open todos. Here it is:\n1. a (×2)"
    )


# ---------------------------------------------------------------------------
# 2. The list records itself as the last numbered list, one entry per line
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_list_records_one_entry_per_line_with_every_copy(handlers, rows):
    await _show(handlers)
    numbered = get_or_create_context(_SESSION, user_id=_USER).last_numbered_list
    assert numbered is not None
    assert numbered.kind == "todos"
    assert numbered.texts == ["urgent task", "high task", "review prs"]
    assert numbered.ids == [rows[0].id, rows[1].id, rows[2].id]
    assert numbered.groups == [[rows[0].id], [rows[1].id], [r.id for r in rows[2:]]]


@pytest.mark.asyncio
async def test_the_no_numbered_list_fallback_no_longer_fires_after_the_list(
    handlers, store, service, rows
):
    await _show(handlers)
    msg, armed = await _complete(handlers, store, 1)
    assert "haven't shown you" not in msg
    assert "numbered list" not in msg
    assert armed is False
    assert service.completed_ids == [rows[0].id]


# ---------------------------------------------------------------------------
# 3. Complete: one copy acts at once; a grouped line asks
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_complete_on_a_one_copy_line_completes_at_once(handlers, store, service, rows):
    await _show(handlers)
    msg, armed = await _complete(handlers, store, 2, "mark the second one done")
    assert msg == "Nice - I've marked 'high task' as done. Good progress!"
    assert armed is False and store.slot is None
    assert service.completed_ids == [rows[1].id]


@pytest.mark.asyncio
async def test_complete_on_a_grouped_line_arms_cxos_question(handlers, store, service, rows):
    await _show(handlers)
    msg, armed = await _complete(handlers, store, 3, "complete the third one")
    assert msg == _COMPLETE_Q
    assert armed is True
    assert service.completed_ids == []
    pa = store.slot["pending_action"]
    assert pa["kind"] == tlp.GROUP_LINE_KIND
    assert store.slot["workflow_type"] == tlp.CLARIFY_GROUP_LINE_WORKFLOW
    assert pa["verb"] == "complete"
    assert pa["line_ids"] == [r.id for r in rows[2:]]


@pytest.mark.asyncio
async def test_answer_one_completes_the_first_copy_in_list_order(
    handlers, store, service, rows, intent_service
):
    await _show(handlers)
    await _complete(handlers, store, 3)
    out = await _answer("one", intent_service, store)
    assert out["message"] == "Nice - I've marked 'review prs' as done. Good progress!"
    assert service.completed_ids == [rows[2].id]
    assert store.slot is None


@pytest.mark.parametrize("answer", ["all 3", "all", "both", "all of them"])
@pytest.mark.asyncio
async def test_answer_all_completes_every_copy(
    answer, handlers, store, service, rows, intent_service
):
    await _show(handlers)
    await _complete(handlers, store, 3)
    out = await _answer(answer, intent_service, store)
    assert service.completed_ids == [r.id for r in rows[2:]]
    assert out["message"].startswith("Marked 3 todos done:")
    assert store.slot is None


@pytest.mark.asyncio
async def test_after_one_copy_is_done_the_line_asks_about_the_two_left(
    handlers, store, service, rows, intent_service
):
    await _show(handlers)
    await _complete(handlers, store, 3)
    await _answer("one", intent_service, store)
    msg, armed = await _complete(handlers, store, 3)
    assert msg == '"review prs" is on your list 2 times. Complete one, or all 2?'
    assert store.slot["pending_action"]["line_ids"] == [rows[3].id, rows[4].id]


# ---------------------------------------------------------------------------
# 4. Delete: a grouped line asks one or all, and the answer is the confirmation
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_delete_on_a_grouped_line_asks_one_or_all(handlers, store, service):
    await _show(handlers)
    msg, armed = await _delete(handlers, store, 3, "delete the third one")
    assert msg == _DELETE_Q
    assert armed is True
    assert store.slot["pending_action"]["verb"] == "delete"
    assert service.deleted_ids == []


@pytest.mark.asyncio
async def test_delete_answer_one_deletes_the_first_copy(
    handlers, store, service, rows, intent_service
):
    await _show(handlers)
    await _delete(handlers, store, 3)
    out = await _answer("one", intent_service, store)
    assert service.deleted_ids == [rows[2].id]
    assert out["message"] == "Deleted 1 todo:\n• review prs"
    assert store.slot is None  # no second yes/no


@pytest.mark.asyncio
async def test_delete_answer_all_deletes_every_copy(handlers, store, service, rows, intent_service):
    ids = [r.id for r in rows[2:]]
    await _show(handlers)
    await _delete(handlers, store, 3)
    out = await _answer("all 3", intent_service, store)
    assert service.deleted_ids == ids
    assert out["message"] == "Deleted 3 todos:\n• review prs (3 items)"
    assert store.slot is None  # the answer IS the confirmation


@pytest.mark.asyncio
async def test_delete_on_a_one_copy_line_keeps_the_always_confirm(handlers, store, service):
    await _show(handlers)
    msg, armed = await _delete(handlers, store, 1)
    assert msg == 'Delete the todo "urgent task"? (yes/no)'
    assert armed is True
    assert store.slot["pending_action"]["kind"] == "todo_batch_delete"
    assert service.deleted_ids == []


# ---------------------------------------------------------------------------
# 5. The noun rule, and the armed question's other answers
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_noun_rule_still_says_reminder_when_the_person_does(handlers, store):
    await _show(handlers)
    msg, _ = await _delete(handlers, store, 1, "delete the first reminder")
    assert msg == 'Delete the reminder "urgent task"? (yes/no)'


@pytest.mark.asyncio
async def test_an_unclear_answer_reasks_once_then_releases(
    handlers, store, service, intent_service
):
    await _show(handlers)
    await _complete(handlers, store, 3)
    out = await _answer("hmm, the purple ones", intent_service, store)
    assert out["message"] == _COMPLETE_Q
    assert out["intent_data"][tlp.GROUP_LINE_PENDING_FLAG] is True
    assert store.slot["pending_action"]["line_reasked"] is True
    assert await _answer("purple monkey dishwasher", intent_service, store) is None
    assert store.slot is None and service.completed_ids == []


@pytest.mark.asyncio
async def test_thanks_keeps_the_question_and_a_decline_falls_through(
    handlers, store, service, intent_service
):
    await _show(handlers)
    await _complete(handlers, store, 3)
    out = await _answer("thanks", intent_service, store)
    assert out["message"] == f"You're welcome.\n{_COMPLETE_Q}"
    assert store.slot["pending_action"]["kind"] == tlp.GROUP_LINE_KIND
    assert await _answer("no", intent_service, store) is None  # generic seam declines
    assert service.completed_ids == []


@pytest.mark.asyncio
async def test_a_bare_yes_lands_on_the_offer_only_workflow_which_reasks(
    handlers, store, intent_service
):
    from services.intent_service.workflow_dispatcher import get_registered_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()

    await _show(handlers)
    await _complete(handlers, store, 3)
    offer = store.get_and_clear_pending_offer(_SESSION)
    assert (
        await tlp.handle_todo_group_line_turn(offer, "yes", _SESSION, _USER, intent_service) is None
    )
    entry = get_registered_workflows().get(tlp.CLARIFY_GROUP_LINE_WORKFLOW)
    assert entry is not None and not entry.action_triggered
    out = await tlp.run_clarify_todo_group_line_workflow(
        _SESSION,
        user_id=_USER,
        context={"pending_action": offer["pending_action"], "intent_service": intent_service},
    )
    assert out["message"] == f"Just so I get it right: {_COMPLETE_Q}"
    assert store.slot["pending_action"]["kind"] == tlp.GROUP_LINE_KIND
