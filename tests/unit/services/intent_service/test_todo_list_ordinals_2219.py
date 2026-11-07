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
    # CXO 11-06 08:3x: one copy of a grouped line says how many are still open.
    assert out["message"] == 'Marked one "review prs" as done. 2 are still open.'
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
    # CXO 11-06 15:58: two copies read "both".
    assert msg == '"review prs" is on your list 2 times. Complete one, or both?'
    assert store.slot["pending_action"]["line_ids"] == [rows[3].id, rows[4].id]


# ---------------------------------------------------------------------------
# 4. Delete under xian's #2019 cap (DELETE_CAP = 1): a grouped line confirms ONE copy
#    and never offers "all" (CXO's one-or-all delete question waits on the cap's lift)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_delete_on_a_grouped_line_confirms_its_first_copy_only(
    handlers, store, service, rows
):
    await _show(handlers)
    msg, armed = await _delete(handlers, store, 3, "delete the third one")
    # CXO 11-06 08:3x: the confirm says the count, so "(×3)" isn't read as all three.
    assert msg == 'Delete one of your 3 "review prs" todos? (yes/no)'
    assert "all" not in msg
    assert armed is True
    assert store.slot["pending_action"]["kind"] == "todo_batch_delete"
    assert service.deleted_ids == []


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


# ---------------------------------------------------------------------------
# 6. CXO 11-06 08:3x: touching ONE copy of a grouped line always says the count
# ---------------------------------------------------------------------------


async def _say_yes_to_delete(handlers, store):
    """The #1190 confirmed re-entry: the bound intent the confirm armed, marked yes."""
    from services.intent_service.destructive_confirm import CONFIRMED_CONTEXT_KEY

    bound = store.get_and_clear_pending_offer(_SESSION)["pending_action"]["intent"]
    bound.context = {**bound.context, CONFIRMED_CONTEXT_KEY: True}
    return await handlers.handle_delete_todo_targets(bound, _SESSION, UUID(_USER), store, _USER)


@pytest.mark.asyncio
async def test_the_grouped_delete_confirm_says_reminders_when_the_person_does(handlers, store):
    await _show(handlers)
    msg, _ = await _delete(handlers, store, 3, "delete the third reminder")
    assert msg == 'Delete one of your 3 "review prs" reminders? (yes/no)'


@pytest.mark.asyncio
async def test_yes_on_the_grouped_delete_says_how_many_are_left(handlers, store, service, rows):
    await _show(handlers)
    await _delete(handlers, store, 3)
    msg, armed = await _say_yes_to_delete(handlers, store)
    assert msg == 'Deleted one "review prs". 2 are left on your list.'
    assert armed is False
    assert service.deleted_ids == [rows[2].id]


@pytest.mark.asyncio
async def test_the_left_count_comes_from_the_armed_record_not_the_words(
    handlers, store, service, rows
):
    """Two copies shown → "1 is left", carried on the confirm, not re-read."""
    service.rows.remove(rows[4])
    await _show(handlers)
    msg, _ = await _delete(handlers, store, 3)
    assert msg == 'Delete one of your 2 "review prs" todos? (yes/no)'
    assert store.slot["pending_action"]["intent"].context["batch_delete_line_copies"] == 2
    msg, _ = await _say_yes_to_delete(handlers, store)
    assert msg == 'Deleted one "review prs". 1 is left on your list.'


@pytest.mark.asyncio
async def test_yes_on_a_one_copy_delete_keeps_todays_summary(handlers, store, service, rows):
    await _show(handlers)
    await _delete(handlers, store, 1)
    msg, _ = await _say_yes_to_delete(handlers, store)
    assert msg == "Deleted 1 todo:\n• urgent task"


@pytest.mark.asyncio
async def test_a_batch_naming_a_grouped_line_says_one_of_three(handlers, store, service):
    await _show(handlers)
    msg, armed = await handlers.handle_complete_todo_targets(
        _intent("complete_todo", "complete the first and third", ["1", "3"]),
        _SESSION,
        UUID(_USER),
        store,
        _USER,
    )
    assert armed is True
    assert msg.startswith('Complete 2 todos: "urgent task" and "review prs" (1 of 3)?')
    assert service.completed_ids == []


def test_the_bulleted_batch_confirm_says_one_of_three_too():
    from services.intent_service.todo_handlers import _batch_confirm_question

    targets = ["a", "b", "c", "d", "e", "review prs"]
    q = _batch_confirm_question(targets, [], "todo", notes={"review prs": "1 of 3"})
    assert "• review prs (1 of 3)" in q.split("\n")
    # Without notes the old forms hold.
    assert (
        _batch_confirm_question(["x", "x"], [], "todo")
        == 'Complete 2 todos: "x" (2 items)? (yes/no)'
    )


def test_the_line_pick_refuses_to_arm_a_delete():
    """Arch 11-06 09:17: no path around xian's #2019 delete cap lives in the line pick."""
    from services.intent_service.todo_line_pick import arm_group_line_question

    with pytest.raises(ValueError):
        arm_group_line_question("delete", [object(), object()], "todo", "", "s", object(), "u")


@pytest.mark.asyncio
async def test_a_capped_multi_delete_shows_a_grouped_line_as_the_list_did(handlers, store, service):
    """CXO 11-06 09:16: the capped list names a grouped line as shown, "review prs" (×3).
    #2318 (CXO 11-07): numbered as the list showed them, and armed as the pick."""
    await _show(handlers)
    msg, armed = await handlers.handle_delete_todo_targets(
        _intent("delete_todo", "delete the first and third", ["1", "3"]),
        _SESSION,
        UUID(_USER),
        store,
        _USER,
    )
    assert armed is True
    assert '1. "urgent task"\n' in msg
    assert '3. "review prs" (×3)' in msg
    assert service.deleted_ids == []


def test_the_capped_reply_without_counts_is_unchanged():
    from services.intent_service.delete_cap import capped_delete_reply

    assert capped_delete_reply(["a", "b"], "todo") == (
        'I can delete one todo at a time for now. You asked about these:\n1. "a"\n2. "b"'
        "\n\nTell me which one to delete first. Nothing has been changed."
    )


@pytest.mark.asyncio
async def test_a_named_delete_of_a_grouped_line_asks_one_of_your_n(handlers, store, service, rows):
    """CXO 11-06 15:58 (Web's served turn on 7ffd460640, "delete the review prs todos"):
    a NAMED target on a grouped line asks the same one-copy question as the ordinal."""
    await _show(handlers)
    msg, armed = await handlers.handle_delete_todo_targets(
        _intent("delete_todo", "delete the review prs todos", ["review prs"]),
        _SESSION,
        UUID(_USER),
        store,
        _USER,
    )
    assert msg == 'Delete one of your 3 "review prs" todos? (yes/no)'
    assert armed is True
    assert service.deleted_ids == []
