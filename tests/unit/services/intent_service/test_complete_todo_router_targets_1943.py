"""#1943 — complete_todo acts on ROUTER-named targets (Arch's (a), 2026-10-05).

PM live, alpha v169 (2026-10-05): "Mark the first three complete and leave
the fourth one pending" completed ONE (the regex binder knew single
ordinals only); a verb answer carrying the list became complete_todo('it').
The ruling: the LLM decides meaning (the router emits args.targets /
args.exclude in a small mini-grammar — "1" · "1-3" · "last" · "all" ·
"name:<text>"), code decides permission (resolution against the real list,
and the #1190 confirm that ENUMERATES what will be touched and what won't).

CXO's two rulings (2026-10-06) are pinned here verbatim: the five strings
(count-first confirm with duplicate titles collapsed, the Okay-family
decline, a summary that reports only what completed, an unresolved ask that
names the list it searched, today's single-item line) and the scope rule —
an ORDINAL resolves only against a list the user was last shown NUMBERED.

Layer (m-43): handler-level tests with todo_service, the offer store and
the session context mocked — the resolver is pure; the confirm is asserted
by the offer record it arms and by the confirmed re-entry completing exactly
the bound ids. No LLM, no DB. The router's side is the scored corpus
(inversion-args-score-2026-10-06-anthropic.md, 13/13); the served answer is
tests/e2e/test_complete_todo_router_targets_live.py.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from services.intent_service import todo_handlers as th
from services.intent_service.conversation_context import NumberedList
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
    CONFIRMED_CONTEXT_KEY,
)
from services.intent_service.todo_handlers import (
    BATCH_COMPLETE_IDS_KEY,
    BATCH_COMPLETE_LEFT_KEY,
    BATCH_COMPLETE_TEXTS_KEY,
    TodoIntentHandlers,
    resolve_router_targets,
)

_NOW = datetime.now(timezone.utc)


def _due(text: str, minutes_ago: int) -> Todo:
    t = Todo(text=text, priority="medium")
    t.id = str(uuid4())
    t.reminder_date = _NOW - timedelta(minutes=minutes_ago)
    t.completed = False
    return t


@pytest.fixture
def four():
    return [
        _due("check the test card again", 400),
        _due("check the test card again", 300),
        _due("review the pr", 200),
        _due("revise the pr", 100),
    ]


class TestResolveRouterTargets:
    def test_positions_index_the_numbered_list_only(self, four):
        picked, un = resolve_router_targets(["1-3"], four, ordinal_candidates=four)
        assert [t.id for t in picked] == [t.id for t in four[:3]] and un == []
        picked, un = resolve_router_targets(["#2", "4"], four, ordinal_candidates=four)
        assert [t.text for t in picked] == ["check the test card again", "revise the pr"]
        # the numbered list may be a different ORDER than the pool
        reversed_list = list(reversed(four))
        picked, _ = resolve_router_targets(["1"], four, ordinal_candidates=reversed_list)
        assert picked == [four[3]]

    def test_no_numbered_list_means_every_ordinal_is_unresolved(self, four):
        picked, un = resolve_router_targets(["1-3", "last", "#2"], four, ordinal_candidates=[])
        assert picked == [] and un == ["1-3", "last", "#2"]

    def test_last_and_all(self, four):
        assert resolve_router_targets(["last"], four, ordinal_candidates=four)[0] == [four[3]]
        assert len(resolve_router_targets(["all"], four, ordinal_candidates=[])[0]) == 4

    def test_name_matches_every_candidate_with_that_text(self, four):
        picked, un = resolve_router_targets(
            ["name:check the test card again"], four, ordinal_candidates=[]
        )
        assert len(picked) == 2 and un == []

    def test_name_substring_unique_text(self, four):
        picked, un = resolve_router_targets(["name:revise"], four, ordinal_candidates=[])
        assert [t.text for t in picked] == ["revise the pr"] and un == []

    def test_out_of_range_and_unknown_name_are_unresolved_never_guessed(self, four):
        picked, un = resolve_router_targets(
            ["7", "name:water the plants"], four, ordinal_candidates=four
        )
        assert picked == [] and un == ["7", "name:water the plants"]

    def test_ambiguous_name_across_different_texts_is_unresolved(self, four):
        picked, un = resolve_router_targets(["name:the pr"], four, ordinal_candidates=[])
        assert picked == [] and un == ["name:the pr"]


class TestCopyHelpers:
    def test_confirm_collapses_duplicates_and_counts_first(self):
        q = th._batch_confirm_question(
            ["check the test card again", "check the test card again", "review the pr"],
            ["revise the pr"],
        )
        assert q == (
            'Complete 3 reminders: "check the test card again" (2 items) and "review the pr"? '
            'Leaving "revise the pr" as is. (yes/no)'
        )

    def test_confirm_two_distinct_and_no_leaving(self):
        assert (
            th._batch_confirm_question(["A", "B"], [])
            == 'Complete 2 reminders: "A" and "B"? (yes/no)'
        )

    def test_confirm_more_than_five_uses_bullets_and_counts_the_left(self):
        q = th._batch_confirm_question([f"t{i}" for i in range(7)], [f"l{i}" for i in range(4)])
        lines = q.splitlines()
        assert lines[0] == "Complete 7 reminders?"
        assert lines[1:8] == [f"• t{i}" for i in range(7)]
        assert lines[8] == "Leaving the other 4 as is."
        assert lines[-1] == "(yes/no)"

    def test_summary_reports_only_what_completed(self):
        s = th._batch_summary(["a", "a", "b"], [("c", "no longer there")], ["d"])
        assert s.splitlines() == [
            "Marked 3 reminders done:",
            "• a (2 items)",
            "• b",
            "Couldn't mark \"c\" done — it's no longer there.",
            'Left "d" as is.',
        ]
        assert th._batch_summary(["only"], [], []).startswith("Marked 1 reminder done:")


def _intent(message: str, targets, exclude=None, extra=None) -> Intent:
    ctx = {"original_message": message, "inversion_args": {"targets": targets}}
    if exclude is not None:
        ctx["inversion_args"]["exclude"] = exclude
    if extra:
        ctx.update(extra)
    return Intent(
        category=IntentCategory.EXECUTION,
        action="complete_todo",
        original_message=message,
        confidence=0.95,
        context=ctx,
    )


class TestHandleCompleteTodoTargets:
    @pytest.fixture
    def handlers(self, four):
        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        h.todo_service.list_todos = AsyncMock(return_value=four)
        # the real service returns the completed Todo (the formatter reads .text)
        h.todo_service.complete_todo = AsyncMock(
            side_effect=lambda todo_id, user_id: next(t for t in four if t.id == str(todo_id))
        )
        return h

    @pytest.fixture
    def offers(self):
        store = MagicMock()
        store.set_pending_offer = MagicMock()
        return store

    @pytest.fixture
    def session_ctx(self, monkeypatch):
        """The session context the handler reads/writes the numbered list on."""
        ctx = MagicMock()
        ctx.last_numbered_list = None
        monkeypatch.setattr(
            "services.intent_service.conversation_context.get_or_create_context",
            lambda session_id, user_id=None: ctx,
        )
        return ctx

    def _shown(self, session_ctx, four):
        session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[t.id for t in four], texts=[t.text for t in four]
        )

    @pytest.mark.asyncio
    async def test_no_router_targets_returns_none_so_the_legacy_handler_runs(
        self, handlers, offers, session_ctx
    ):
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="complete the PR review",
            context={"original_message": "complete the PR review"},
        )
        assert (
            await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u") is None
        )
        handlers.todo_service.complete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_pm_first_three_after_a_numbered_list_arms_the_enumerating_confirm(
        self, handlers, offers, session_ctx, four
    ):
        """PM's 10-05 sentence after 'what reminders do I have?' showed the
        numbered list: targets 1-3 → the count-first confirm, nothing changed."""
        self._shown(session_ctx, four)
        intent = _intent("Mark the first three complete and leave the fourth one pending.", ["1-3"])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg == (
            'Complete 3 reminders: "check the test card again" (2 items) and "review the pr"? '
            'Leaving "revise the pr" as is. (yes/no)'
        )
        handlers.todo_service.complete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_called_once()
        _sid, offer = offers.set_pending_offer.call_args.args[:2]
        assert offer["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert offer["question"] == msg
        pa = offer["pending_action"]
        assert pa["kind"] == "todo_batch_complete" and pa["action"] == "complete_todo"
        assert pa["intent"].context[BATCH_COMPLETE_IDS_KEY] == [t.id for t in four[:3]]
        assert pa["intent"].context[BATCH_COMPLETE_LEFT_KEY] == ["revise the pr"]
        assert (
            offer["decline_message"] == "Okay — I won't mark those done. Nothing has been changed."
        )

    @pytest.mark.asyncio
    async def test_ordinal_without_a_numbered_list_is_unresolved_and_shows_the_list_numbered(
        self, handlers, offers, session_ctx, four
    ):
        """CXO's scope rule: no numbered list shown → the ordinal is NOT
        guessed; the reply numbers the active list (grounding the next turn)."""
        intent = _intent("Mark the first three complete and leave the fourth one pending.", ["1-3"])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        lines = msg.splitlines()
        assert lines[0] == "There's no number 1-3 in your due reminders. You have 4:"
        assert lines[1:5] == [f"{i + 1}. {t.text}" for i, t in enumerate(four)]
        assert lines[-1] == "Tell me which one, and I'll mark it done."
        assert "?" not in msg
        handlers.todo_service.complete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_not_called()
        # the list just shown is now the numbered list
        assert session_ctx.last_numbered_list.ids == [t.id for t in four]

    @pytest.mark.asyncio
    async def test_confirmed_reentry_completes_exactly_the_bound_ids(
        self, handlers, offers, session_ctx, four
    ):
        """The "yes" re-dispatches the bound intent — not a re-resolve."""
        intent = _intent(
            "Mark the first three complete and leave the fourth one pending.",
            ["1-3"],
            extra={
                CONFIRMED_CONTEXT_KEY: True,
                BATCH_COMPLETE_IDS_KEY: [t.id for t in four[:3]],
                BATCH_COMPLETE_TEXTS_KEY: [t.text for t in four[:3]],
                BATCH_COMPLETE_LEFT_KEY: ["revise the pr"],
            },
        )
        # the list may have shifted since the ask; the bound ids still rule
        handlers.todo_service.list_todos = AsyncMock(return_value=four[1:])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        called = [
            str(c.kwargs["todo_id"]) for c in handlers.todo_service.complete_todo.call_args_list
        ]
        assert called == [t.id for t in four[:3]]
        assert msg.splitlines() == [
            "Marked 3 reminders done:",
            "• check the test card again (2 items)",
            "• review the pr",
            'Left "revise the pr" as is.',
        ]
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_confirmed_reentry_reports_only_what_completed(
        self, handlers, offers, session_ctx, four
    ):
        gone = four[1]
        handlers.todo_service.complete_todo = AsyncMock(
            side_effect=lambda todo_id, user_id: None
            if str(todo_id) == gone.id
            else next(t for t in four if t.id == str(todo_id))
        )
        intent = _intent(
            "x",
            ["1-3"],
            extra={
                CONFIRMED_CONTEXT_KEY: True,
                BATCH_COMPLETE_IDS_KEY: [t.id for t in four[:3]],
                BATCH_COMPLETE_TEXTS_KEY: [t.text for t in four[:3]],
                BATCH_COMPLETE_LEFT_KEY: ["revise the pr"],
            },
        )
        msg, _ = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert msg.splitlines()[0] == "Marked 2 reminders done:"
        assert "Couldn't mark \"check the test card again\" done — it's no longer there." in msg

    @pytest.mark.asyncio
    async def test_two_named_targets_need_no_numbered_list(self, handlers, offers, session_ctx):
        intent = _intent(
            "clear 'check the test card again' and 'review the pr' — mark them done",
            ["name:check the test card again", "name:review the pr"],
        )
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg.startswith(
            'Complete 3 reminders: "check the test card again" (2 items) and "review the pr"?'
        )
        assert 'Leaving "revise the pr" as is.' in msg

    @pytest.mark.asyncio
    async def test_all_except_name_arms_with_the_exception_left(
        self, handlers, offers, session_ctx
    ):
        intent = _intent(
            "mark all my reminders done except for 'revise the pr'",
            ["all"],
            exclude=["name:revise the pr"],
        )
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg.startswith("Complete 3 reminders:")
        assert 'Leaving "revise the pr" as is.' in msg

    @pytest.mark.asyncio
    async def test_single_target_completes_directly_no_question(
        self, handlers, offers, session_ctx, four
    ):
        self._shown(session_ctx, four)
        intent = _intent("complete the last one", ["last"])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        handlers.todo_service.complete_todo.assert_awaited_once()
        assert "?" not in msg
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_unknown_name_asks_naming_the_list_it_searched(
        self, handlers, offers, session_ctx
    ):
        intent = _intent("mark 'water the plants' done", ["name:water the plants"])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        assert (
            msg.splitlines()[0]
            == 'I couldn\'t find "water the plants" in your due reminders. You have:'
        )
        assert msg.splitlines()[-1] == "Tell me which one, and I'll mark it done."
        handlers.todo_service.complete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_partial_resolution_promises_only_what_the_state_holds(
        self, handlers, offers, session_ctx, four
    ):
        """CXO flaw 1 (10-06): one target resolves, one doesn't. Nothing is
        armed, so the tail must NOT invite a one-item answer that would
        complete one and silently drop the rest."""
        self._shown(session_ctx, four)
        intent = _intent(
            "mark the first one and 'water the plants' done", ["1", "name:water the plants"]
        )
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        assert msg.splitlines()[-1] == (
            "Nothing has been changed. Say it again with the right name or number."
        )
        assert "Tell me which one" not in msg
        handlers.todo_service.complete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_only_the_rows_on_screen_are_remembered_as_the_numbered_list(
        self, handlers, offers, session_ctx
    ):
        """CXO flaw 2 (10-06): the reply caps the list at 10; the remembered
        numbered list must be those 10, never the full pool."""
        twelve = [_due(f"item {i}", 100 - i) for i in range(12)]
        handlers.todo_service.list_todos = AsyncMock(return_value=twelve)
        intent = _intent("mark 'water the plants' done", ["name:water the plants"])
        msg, _ = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert "…and 2 more." in msg
        assert session_ctx.last_numbered_list.ids == [t.id for t in twelve[:10]]

    @pytest.mark.asyncio
    async def test_no_session_never_arms_an_unpoppable_offer(
        self, handlers, offers, session_ctx, four
    ):
        intent = _intent(
            "mark 'review the pr' and 'revise the pr' done",
            ["name:review the pr", "name:revise the pr"],
        )
        msg, armed = await handlers.handle_complete_todo_targets(intent, None, uuid4(), offers, "u")
        assert armed is False
        offers.set_pending_offer.assert_not_called()
        handlers.todo_service.complete_todo.assert_not_awaited()


class TestReminderListIsNumberedAndRemembered:
    @pytest.mark.asyncio
    async def test_list_reminders_numbers_due_first_and_records_the_list(self, four, monkeypatch):
        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        h.todo_service.list_todos = AsyncMock(return_value=four)
        ctx = MagicMock()
        ctx.last_numbered_list = None
        monkeypatch.setattr(
            "services.intent_service.conversation_context.get_or_create_context",
            lambda session_id, user_id=None: ctx,
        )
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_reminders_query",
            original_message="what reminders do I have?",
            context={"original_message": "what reminders do I have?"},
        )
        reply = await h.handle_list_reminders(intent, "s1", uuid4())
        lines = [ln for ln in reply.splitlines() if ln[:2] in {"1.", "2.", "3.", "4."}]
        assert [ln.split(". **")[1].split("**")[0] for ln in lines] == [t.text for t in four]
        assert ctx.last_numbered_list.kind == "reminders"
        assert ctx.last_numbered_list.ids == [t.id for t in four]

    @pytest.mark.asyncio
    async def test_upcoming_block_renders_as_a_list_continuing_the_numbering(self, monkeypatch):
        """CXO's render check (10-06). Under CommonMark an ordered list can
        interrupt a paragraph only when it starts at 1, so "📅 Upcoming:"
        followed directly by "3. …" rendered as one run-on paragraph. Pinned
        at the source (blank line after each header) and, where node is
        available, at the render layer through the vendored marked."""
        import shutil
        import subprocess
        from pathlib import Path

        due = [_due("check the test card again", 120), _due("review the pr", 60)]
        upcoming = [_due("revise the pr", -600), _due("call mom", -3000)]  # future
        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        h.todo_service.list_todos = AsyncMock(return_value=due + upcoming)
        ctx = MagicMock()
        ctx.last_numbered_list = None
        monkeypatch.setattr(
            "services.intent_service.conversation_context.get_or_create_context",
            lambda session_id, user_id=None: ctx,
        )
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_reminders_query",
            original_message="what reminders do I have?",
            context={"original_message": "what reminders do I have?"},
        )
        reply = await h.handle_list_reminders(intent, "s1", uuid4())
        assert "📅 Upcoming:\n\n3. **revise the pr**" in reply
        assert "⏰ Due now:\n\n1. **check the test card again**" in reply
        assert ctx.last_numbered_list.texts == [
            "check the test card again",
            "review the pr",
            "revise the pr",
            "call mom",
        ]

        node = shutil.which("node")
        marked = Path("web/static/vendor/marked-15.0.12.min.js")
        if not node or not marked.exists():
            pytest.skip("render layer needs node + the vendored marked")
        js = (
            f"const m=require({str(marked.resolve())!r});"
            "const mk=m.marked||m;let s='';process.stdin.on('data',d=>s+=d);"
            "process.stdin.on('end',()=>process.stdout.write(mk.parse(s)));"
        )
        html = subprocess.run(
            [node, "-e", js], input=reply, capture_output=True, text=True, timeout=30
        ).stdout
        assert '<ol start="3">' in html, html
        assert "<li><strong>revise the pr</strong>" in html, html
