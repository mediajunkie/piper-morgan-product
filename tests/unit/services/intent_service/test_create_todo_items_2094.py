"""#2094 — a list of todo titles in one message creates one todo per title.

xian, alpha e801b1a309, 2026-10-19 13:51: "Add three todos for the launch: draft brief, book venue,
send invites" → "I didn't catch what you'd like me to add." The router already names the list
(measured 3/3 the same day: args={"items": [...], "context": "launch"}); the handler now consumes
it (Arch's shape: consume the router's extracted items, never split a string) and the reply names
every todo. Also #2095's small ask: a leading "to " is dropped from a stored title.

LAYER: the handler through its method with the todo service replaced at its one seam.
DENOMINATOR: the list path, the honesty guard, the single path, the leading-"to" rule.
"""

import types
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

MSG = "Add three todos for the launch: draft brief, book venue, send invites"
USER = "11111111-1111-1111-1111-111111111111"


def _handlers():
    h = TodoIntentHandlers.__new__(TodoIntentHandlers)
    created = []

    async def create_todo(user_id, text, priority="medium", **_):
        todo = types.SimpleNamespace(
            id=f"t-{len(created) + 1}", text=text, priority=priority, completed=False
        )
        created.append(todo)
        return todo

    h.todo_service = MagicMock()
    h.todo_service.create_todo = AsyncMock(side_effect=create_todo)
    h._created = created
    return h


def _intent(message, args=None):
    ctx = {"original_message": message}
    if args is not None:
        ctx["inversion_args"] = args
    return Intent(
        original_message=message,
        category=IntentCategory.EXECUTION,
        action="create_todo",
        confidence=0.95,
        context=ctx,
    )


class TestRouterItems:
    def test_measured_args_yield_the_three_titles(self):
        items = TodoIntentHandlers._router_todo_items(
            _intent(
                MSG, {"items": ["draft brief", "book venue", "send invites"], "context": "launch"}
            ),
            MSG,
        )
        assert items == ["draft brief", "book venue", "send invites"]

    def test_titles_key_is_accepted_too(self):
        assert TodoIntentHandlers._router_todo_items(
            _intent(MSG, {"titles": ["draft brief", "book venue"]}), MSG
        ) == [
            "draft brief",
            "book venue",
        ]

    def test_a_word_the_user_did_not_say_empties_the_list(self):
        assert (
            TodoIntentHandlers._router_todo_items(
                _intent(MSG, {"items": ["draft brief", "hire a band"]}), MSG
            )
            == []
        )

    def test_no_args_no_items(self):
        assert TodoIntentHandlers._router_todo_items(_intent(MSG), MSG) == []


class TestHandlerCreatesOnePerTitle:
    @pytest.mark.asyncio
    async def test_three_todos_named_in_the_reply(self):
        h = _handlers()
        from services.intent_service.conversation_context import get_or_create_context

        reply = await h.handle_create_todo(
            _intent(
                MSG, {"items": ["draft brief", "book venue", "send invites"], "context": "launch"}
            ),
            "sess-2094",
            USER,
        )
        assert [t.text for t in h._created] == ["draft brief", "book venue", "send invites"]
        # Issue 2427 (CXO 11-23): the reply ends with the fact; no closing offer.
        assert reply == (
            "I've added 3 todos to your list: 'draft brief', 'book venue' and 'send invites'."
        )
        parked = get_or_create_context("sess-2094", user_id=USER).pending_created_activity
        assert [r["target_title"] for r in parked] == ["draft brief", "book venue", "send invites"]
        assert all(r["action_type"] == "todo_created" for r in parked)

    @pytest.mark.asyncio
    async def test_single_router_title_wins_and_keeps_its_words(self):
        # Arch (#2094 validation): a router title is never stripped; only the
        # regex fallback drops a leading "to".
        h = _handlers()
        msg = "add todo to review the roadmap"
        await h.handle_create_todo(
            _intent(msg, {"text": "to review the roadmap"}), "sess-2094b", USER
        )
        assert [t.text for t in h._created] == ["to review the roadmap"]

    @pytest.mark.asyncio
    async def test_router_items_keep_their_words_too(self):
        h = _handlers()
        msg = "Create two todos: to review the roadmap, and email the team"
        await h.handle_create_todo(
            _intent(msg, {"items": ["to review the roadmap", "email the team"]}), "sess-2094e", USER
        )
        assert [t.text for t in h._created] == ["to review the roadmap", "email the team"]

    @pytest.mark.asyncio
    async def test_regex_path_also_drops_a_leading_to(self):
        h = _handlers()
        await h.handle_create_todo(_intent("add todo: to review the roadmap"), "sess-2094c", USER)
        assert [t.text for t in h._created] == ["review the roadmap"]

    @pytest.mark.asyncio
    async def test_a_comma_inside_one_title_is_not_split(self):
        h = _handlers()
        msg = "add todo: call Sam, then Priya"
        await h.handle_create_todo(
            _intent(msg, {"text": "call Sam, then Priya"}), "sess-2094d", USER
        )
        assert [t.text for t in h._created] == ["call Sam, then Priya"]

    def test_strip_leading_to_keeps_to_do(self):
        assert TodoIntentHandlers._strip_leading_to("to-do list review") == "to-do list review"
        assert TodoIntentHandlers._strip_leading_to("to review") == "review"
