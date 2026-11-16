"""#1976 — create_todo consumes the router's extracted `text` arg.

Web, alpha 4bd1a236e9 (2026-10-11): 'add a todo to web test one' stored the
title 'to web test one' — the regex extractor strips the command lead-in and
keeps the verb phrase's 'to' ('add a todo to X' means a todo ABOUT X). The
#1943 family's fix: the rail description asks the router for ``args.text``
(the todo's own words without the lead-in) and the handler consumes it first,
with an honesty guard (every word of the arg occurs in the message — an
LLM-written arg never adds words the user did not say), falling back to the
unchanged regex path otherwise.

Layer (m-43): the handler with todo_service stubbed and the Intent shaped the
way ``inversion_live`` shapes a router-served one (``context["inversion_args"]``);
the description pinned at source; the scorer's args matcher as a pure
function. No LLM, no DB. Whether the served router actually names the arg is
the rule-7 measurement (the corpus row 'add a todo to web test one' with
``expected_args.text``), not this file.
"""

import importlib.util
import os
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1976-4b00-9e00-000000001976"


def _intent(message, text=None, args=None):
    ctx = {"original_message": message}
    if args is not None:
        ctx["inversion_args"] = args
    elif text is not None:
        ctx["inversion_args"] = {"text": text}
    return Intent(
        category=IntentCategory.EXECUTION,
        action="create_todo",
        original_message=message,
        confidence=0.95,
        context=ctx,
    )


@pytest.fixture
def handlers():
    h = TodoIntentHandlers()
    h.todo_service = AsyncMock()

    async def _create(user_id, text, priority):
        return Todo(
            id=str(uuid4()), text=text, priority=priority, status="pending", completed=False
        )

    h.todo_service.create_todo = AsyncMock(side_effect=_create)
    return h


class TestRouterTextGuard:
    def test_router_text_wins_when_its_words_are_the_users(self):
        assert (
            TodoIntentHandlers._router_todo_text(
                _intent("add a todo to web test one", text="web test one"),
                "add a todo to web test one",
            )
            == "web test one"
        )

    def test_whitespace_collapsed(self):
        assert (
            TodoIntentHandlers._router_todo_text(
                _intent("add a todo to  web   test one", text="  web   test one "),
                "add a todo to  web   test one",
            )
            == "web test one"
        )

    @pytest.mark.parametrize(
        "args",
        [
            None,
            {},
            {"text": ""},
            {"text": "   "},
            {"text": 7},
            {"text": None},
            "web test one",
            ["web"],
        ],
    )
    def test_absent_empty_or_unsupported_falls_back(self, args):
        intent = (
            _intent("add a todo to web test one", args=args)
            if args is not None
            else _intent("add a todo to web test one")
        )
        assert TodoIntentHandlers._router_todo_text(intent, "add a todo to web test one") == ""

    def test_words_the_user_did_not_say_are_refused(self):
        """The honesty guard: an LLM-written arg cannot put words in the title."""
        assert (
            TodoIntentHandlers._router_todo_text(
                _intent("add a todo to web test one", text="web test one (urgent)"),
                "add a todo to web test one",
            )
            == ""
        )
        assert (
            TodoIntentHandlers._router_todo_text(
                _intent("add a todo to web test one", text="call the vendor"),
                "add a todo to web test one",
            )
            == ""
        )

    def test_no_regex_in_the_guard(self):
        import inspect

        src = inspect.getsource(TodoIntentHandlers._router_todo_text)
        assert not any(
            tok in src for tok in ("re.search", "re.match", "re.compile", "re.findall", "re.sub")
        )


@pytest.mark.asyncio
class TestHandlerConsumes:
    async def test_router_text_is_the_stored_title(self, handlers):
        msg = await handlers.handle_create_todo(
            _intent("add a todo to web test one", text="web test one"), "s-1976", UUID(_USER)
        )
        handlers.todo_service.create_todo.assert_awaited_once()
        assert handlers.todo_service.create_todo.await_args.kwargs["text"] == "web test one"
        assert "web test one" in msg
        assert "to web test one" not in msg

    async def test_without_router_args_the_regex_path_is_unchanged(self, handlers):
        """The legacy path, byte-for-byte: a classifier-served intent (no
        inversion_args) still stores the regex capture — including the
        stray 'to' this issue is about, which the regex alone cannot fix."""
        await handlers.handle_create_todo(_intent("add todo: buy milk"), "s-1976", UUID(_USER))
        assert handlers.todo_service.create_todo.await_args.kwargs["text"] == "buy milk"
        handlers.todo_service.create_todo.reset_mock()
        await handlers.handle_create_todo(
            _intent("add a todo to web test one"), "s-1976", UUID(_USER)
        )
        # #2094/#2095 (CXO): the regex path now drops a leading "to " as well, so the
        # legacy fallback stores the todo's own words; the rest of the path is unchanged.
        assert handlers.todo_service.create_todo.await_args.kwargs["text"] == "web test one"

    async def test_refused_router_text_falls_back_to_the_regex(self, handlers):
        await handlers.handle_create_todo(
            _intent("add todo: buy milk", text="buy oat milk"), "s-1976", UUID(_USER)
        )
        assert handlers.todo_service.create_todo.await_args.kwargs["text"] == "buy milk"

    async def test_priority_still_read_from_the_message(self, handlers):
        await handlers.handle_create_todo(
            _intent("add a todo to call the vendor, high priority", text="call the vendor"),
            "s-1976",
            UUID(_USER),
        )
        kw = handlers.todo_service.create_todo.await_args.kwargs
        assert (kw["text"], kw["priority"]) == ("call the vendor", "high")

    async def test_nothing_extractable_still_asks(self, handlers):
        msg = await handlers.handle_create_todo(_intent("add a todo"), "s-1976", UUID(_USER))
        assert msg.startswith("I didn't catch what you'd like me to add")
        handlers.todo_service.create_todo.assert_not_awaited()


class TestDescriptionAndScorer:
    def test_create_todo_description_is_the_screened_wording(self):
        from services.intent_service.workflow_dispatcher import get_registered_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        """#1976 landed with NO description change ("Create-todo via action dispatch
        (#1685)"): measured ×3 under it, the served router already named
        text='web test one', and two candidate wordings were screened and dropped.
        Arm B (#2297, Arch 2026-11-14) replaces it with the wording below, which
        lands only if its rule-7 screen passes; that screen carries this file's
        'add a todo to web test one' row as a control (text still named, no project)."""
        register_default_workflows()
        d = get_registered_workflows()["create_todo"].description
        assert d == (
            "Create a todo. If the person names one of their projects for it, put that "
            "project's name in args as project, in their words. Leave project out if "
            "they don't name one."
        )

    @staticmethod
    def _scorer():
        root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            )
        )
        path = os.path.join(root, "scripts", "inversion_phase1_shadow_score.py")
        spec = importlib.util.spec_from_file_location("inversion_phase1_shadow_score", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_args_match_text_key(self):
        m = self._scorer()
        assert m.args_match({"text": "web test one"}, {"text": "web test one"}) == (True, "")
        assert m.args_match({"text": "web test one"}, {"text": "  Web  test one."})[0] is True
        ok, note = m.args_match({"text": "web test one"}, {"text": "to web test one"})
        assert ok is False and note.startswith("text:")
        ok, note = m.args_match({"text": "web test one"}, {})
        assert ok is False and note.startswith("text:")
        # a row that asserts no text never fails on one the model added
        assert m.args_match({"targets": ["1"]}, {"targets": ["1"], "text": "x"}) == (True, "")

    def test_corpus_row_is_the_measured_args_shape(self):
        root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            )
        )
        yaml_path = os.path.join(root, "tests", "fixtures", "inversion_corpus_phase0.yaml")
        with open(yaml_path, encoding="utf-8") as fh:
            body = fh.read()
        i = body.index('phrase: "add a todo to web test one"')
        block = body[i : i + 600]
        assert "expected: action:create_todo" in block
        assert 'expected_args: {"text": "web test one"}' in block
