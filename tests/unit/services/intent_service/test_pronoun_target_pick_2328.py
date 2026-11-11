"""#2328: a completion whose only target is a pronoun ("them", "it") asks which one.

Before: `I couldn't find a todo matching 'them'.` — a statement about a todo named
'them'. Now (CXO 11-10 17:36, existing words only): the armed which-one pick, the same
text the no-list ordinals get; with the numbered list still shown, the armed question
alone over the numbers the person saw. Nothing is completed on the asking turn.
"""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service.delete_todo_pick import DELETE_PICK_KIND, last_numbered_list
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.todo_handlers import TodoIntentHandlers, _is_pronoun_only_target
from services.shared_types import IntentCategory

QUESTION = (
    "Which one should I complete? Say the number or the name, or 'never mind' to leave "
    "them alone."
)
PHRASINGS = ["make clear mark them done", "complete them"]


def _todo(text):
    t = Todo(text=text, priority="medium")
    t.id = str(uuid4())
    return t


def _handlers(rows):
    h = TodoIntentHandlers()
    h.todo_service = AsyncMock()
    h.todo_service.list_todos = AsyncMock(return_value=rows)
    return h


async def _ask(h, message, session, user, offers):
    return await h.handle_complete_todo(
        Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message=message,
            confidence=0.9,
        ),
        session,
        user,
        offer_service=offers,
        principal=str(user),
    )


@pytest.mark.parametrize("message", PHRASINGS)
async def test_no_list_shown_gets_the_no_list_armed_pick(message):
    rows = [_todo("review prs"), _todo("call the vet"), _todo("hydrate")]
    h, offers, user, session = _handlers(rows), WorkflowOfferService(), uuid4(), f"s-{uuid4()}"

    reply = await _ask(h, message, session, user, offers)

    assert reply == (
        "I haven't shown you a numbered list yet. Here are your todos:\n\n"
        '1. "review prs"\n2. "call the vet"\n3. "hydrate"\n\n' + QUESTION
    )
    assert "'them'" not in reply and "couldn't find" not in reply
    h.todo_service.complete_todo.assert_not_called()
    pending = offers.peek_pending_offer(session, str(user))["pending_action"]
    assert pending["kind"] == DELETE_PICK_KIND
    assert pending["verb"] == "complete"
    # The rows shown are the session's numbered list, so "2" binds next turn.
    assert [str(i) for i in last_numbered_list(session, str(user)).ids] == [r.id for r in rows]


@pytest.mark.parametrize("message", PHRASINGS)
async def test_with_the_list_shown_asks_over_the_numbers_the_person_saw(message):
    rows = [_todo("review prs"), _todo("call the vet"), _todo("hydrate")]
    h, offers, user, session = _handlers(rows), WorkflowOfferService(), uuid4(), f"s-{uuid4()}"
    h._remember_numbered_list(
        session,
        str(user),
        "active todos",
        [r.id for r in rows],
        [r.text for r in rows],
        groups=[[r.id] for r in rows],
    )

    reply = await _ask(h, message, session, user, offers)

    assert reply == QUESTION  # the list is on screen: no false "I haven't shown you"
    h.todo_service.complete_todo.assert_not_called()
    pending = offers.peek_pending_offer(session, str(user))["pending_action"]
    assert pending["kind"] == DELETE_PICK_KIND and pending["verb"] == "complete"


async def test_a_shown_list_with_a_closed_line_is_shown_again_never_renumbered_silently():
    """A line whose todo is gone would shift the numbers; the list is shown afresh."""
    rows = [_todo("review prs"), _todo("hydrate")]
    gone = str(uuid4())
    h, offers, user, session = _handlers(rows), WorkflowOfferService(), uuid4(), f"s-{uuid4()}"
    h._remember_numbered_list(
        session,
        str(user),
        "active todos",
        [rows[0].id, gone, rows[1].id],
        ["review prs", "call the vet", "hydrate"],
        groups=[[rows[0].id], [gone], [rows[1].id]],
    )

    reply = await _ask(h, "complete them", session, user, offers)

    assert '1. "review prs"\n2. "hydrate"' in reply and reply.endswith(QUESTION)
    h.todo_service.complete_todo.assert_not_called()


@pytest.mark.parametrize(
    "text,expected",
    [
        ("them", True),
        ("it", True),
        ("that one", True),
        ("those", True),
        ("one", False),  # "one" alone is a number word, not a pointer
        ("all of them", False),  # a bulk ask is a different question
        ("the vet", False),
        ("them apples", False),
        ("", False),
        (None, False),
    ],
)
def test_pronoun_only_target_is_a_word_set_check(text, expected):
    assert _is_pronoun_only_target(text) is expected


async def test_a_named_todo_still_completes():
    rows = [_todo("review prs"), _todo("call the vet")]
    h, offers, user, session = _handlers(rows), WorkflowOfferService(), uuid4(), f"s-{uuid4()}"
    h.todo_service.complete_todo = AsyncMock(return_value=rows[1])

    await _ask(h, "complete the vet todo", session, user, offers)

    h.todo_service.complete_todo.assert_called_once()


@pytest.mark.parametrize("target", ["them", "name:them", "it"])
async def test_a_router_named_pronoun_target_gets_the_same_pick(target):
    """The router can name the pronoun itself (inversion_args.targets); that path
    used to say it couldn't find "them" in the list."""
    rows = [_todo("review prs"), _todo("call the vet")]
    h, offers, user, session = _handlers(rows), WorkflowOfferService(), uuid4(), f"s-{uuid4()}"
    h._due_reminder_todos = AsyncMock(return_value=[])
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="complete_todo",
        original_message="complete them",
        confidence=0.9,
        context={"inversion_args": {"targets": [target]}},
    )

    reply, armed = await h.handle_complete_todo_targets(intent, session, user, offers, str(user))

    assert armed is True
    assert reply == (
        "I haven't shown you a numbered list yet. Here are your todos:\n\n"
        '1. "review prs"\n2. "call the vet"\n\n' + QUESTION
    )
    h.todo_service.complete_todo.assert_not_called()
