"""#2219 / #2295 (Arch ruling 2026-11-06 07:31, option (b)): after the router picks the
todo list op, one op-local call says whether the person wants the list, only the next
todo, or only the completed ones. Code renders from the rows it read; the model's reply
is never rendered. A failed call is today's list.
"""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

from services.consciousness.todo_consciousness import (
    format_completed_todos,
    format_next_todo_line,
)
from services.domain.models import Intent, IntentCategory
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.todo_select_resolve import (
    OUTCOME_COMPLETED,
    OUTCOME_FAILED,
    OUTCOME_LIST,
    OUTCOME_NEXT,
    OUTCOME_SKIPPED,
    TASK_TYPE,
    TodoSelection,
    parse_selection,
    resolve_todo_selection,
)

USER = UUID("12345678-1234-5678-1234-567812345678")


def _todo(text, priority="medium", completed=False):
    return SimpleNamespace(text=text, priority=priority, completed=completed, status="")


def _intent(message="what's my next todo?"):
    return Intent(
        category=IntentCategory.QUERY,
        action="list_todos_query",
        original_message=message,
        confidence=0.9,
    )


def _handlers(rows, outcome):
    h = TodoIntentHandlers()
    h.todo_service = MagicMock()
    h.todo_service.list_todos = AsyncMock(return_value=rows)
    h._resolve_list_selection = AsyncMock(return_value=TodoSelection(outcome=outcome))
    return h


# --- parse: three selectors, anything else fails --------------------------------------


@pytest.mark.parametrize(
    "reply,outcome",
    [
        ('{"selector": "next"}', OUTCOME_NEXT),
        ('{"selector": "completed"}', OUTCOME_COMPLETED),
        ('{"selector": null}', OUTCOME_LIST),
        ('```json\n{"selector": "next"}\n```', OUTCOME_NEXT),
    ],
)
def test_the_three_selectors_parse(reply, outcome):
    assert parse_selection(reply).outcome == outcome


@pytest.mark.parametrize("reply", ['{"selector": "last"}', "{}", "[]", "next", '{"selector": 1}'])
def test_anything_else_raises(reply):
    with pytest.raises((ValueError, TypeError)):
        parse_selection(reply)


# --- the call -----------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_call_uses_its_own_task_and_records_the_providers_tokens():
    llm = MagicMock()

    async def complete(**kw):
        kw["served"]["usage"] = {"input_tokens": 120, "output_tokens": 7}
        assert kw["task_type"] == TASK_TYPE
        assert "what's my next todo?" in kw["prompt"]
        return '{"selector": "next"}'

    llm.complete = complete
    sel = await resolve_todo_selection("what's my next todo?", llm_service=llm, user_id="u")
    assert (sel.outcome, sel.input_tokens, sel.output_tokens) == (OUTCOME_NEXT, 120, 7)
    assert sel.latency_ms is not None


@pytest.mark.asyncio
async def test_an_unparseable_reply_is_failed_and_an_empty_message_is_skipped():
    llm = MagicMock()
    llm.complete = AsyncMock(return_value="the next one, I think")
    assert (await resolve_todo_selection("x", llm_service=llm, user_id="u")).outcome == (
        OUTCOME_FAILED
    )
    assert (await resolve_todo_selection("  ", llm_service=llm, user_id="u")).outcome == (
        OUTCOME_SKIPPED
    )


# --- the renders (CXO 11-05 20:47 and 11-06 07:35) -------------------------------------


def test_the_next_line_counts_the_first_rows_repeats():
    rows = [_todo("review prs"), _todo("buy milk"), _todo("review prs"), _todo("review prs")]
    assert format_next_todo_line(rows) == (
        'Your next todo is "review prs" (×3). Say "show my todos" for the rest.'
    )
    assert format_next_todo_line([_todo("buy milk")]) == (
        'Your next todo is "buy milk". Say "show my todos" for the rest.'
    )


def test_the_completed_list_never_says_open():
    assert format_completed_todos([]) == "You haven't completed any todos yet."
    assert format_completed_todos([_todo("a", completed=True)]) == (
        "You have 1 completed todo. Here it is:\n• a ✓"
    )
    reply = format_completed_todos(
        [_todo("a", completed=True), _todo("b", completed=True), _todo("a", completed=True)]
    )
    assert reply == "You have 3 completed todos. Here they are:\n• a (×2) ✓\n• b ✓"
    assert "open" not in reply


# --- the handler ------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_next_answers_with_the_first_open_row_in_the_lists_order():
    rows = [_todo("done one", "urgent", completed=True), _todo("ship it", "high"), _todo("x")]
    reply = await _handlers(rows, OUTCOME_NEXT).handle_list_todos(_intent(), "s", USER)
    assert reply == 'Your next todo is "ship it". Say "show my todos" for the rest.'


@pytest.mark.asyncio
async def test_next_with_no_open_todos_says_so():
    h = _handlers([_todo("a", completed=True)], OUTCOME_NEXT)
    reply = await h.handle_list_todos(_intent(), "s", USER)
    assert reply.startswith("I checked your active todos and there are none.")


@pytest.mark.asyncio
async def test_completed_reads_the_done_rows_even_when_the_first_read_was_open_only():
    open_rows = [_todo("a")]
    all_rows = [_todo("a"), _todo("b", completed=True)]
    h = _handlers(open_rows, OUTCOME_COMPLETED)
    h.todo_service.list_todos = AsyncMock(side_effect=[open_rows, all_rows])
    reply = await h.handle_list_todos(_intent("what have I finished?"), "s", USER)
    assert reply == "You have 1 completed todo. Here it is:\n• b ✓"
    assert h.todo_service.list_todos.await_args_list[-1].kwargs["include_completed"] is True


@pytest.mark.parametrize("outcome", [OUTCOME_LIST, OUTCOME_FAILED, OUTCOME_SKIPPED])
@pytest.mark.asyncio
async def test_null_and_failure_give_todays_list_without_the_word_next(outcome):
    rows = [_todo("a"), _todo("b")]
    reply = await _handlers(rows, outcome).handle_list_todos(_intent("show my todos"), "s", USER)
    assert reply.startswith("You have 2 open todos. Here they are:")
    assert "next" not in reply.lower()


@pytest.mark.asyncio
async def test_the_selector_starts_before_the_read_finishes():
    """#2250's shape: the call runs concurrently with the read."""
    order = []
    h = TodoIntentHandlers()

    async def select(message, user_id):
        order.append("selector-start")
        await asyncio.sleep(0)
        return TodoSelection(outcome=OUTCOME_LIST)

    async def read(**kw):
        order.append("read-start")
        await asyncio.sleep(0)
        order.append("read-end")
        return [_todo("a")]

    h._resolve_list_selection = select
    h.todo_service = MagicMock()
    h.todo_service.list_todos = read
    await h.handle_list_todos(_intent("show my todos"), "s", USER)
    assert order.index("selector-start") < order.index("read-end")


@pytest.mark.asyncio
async def test_a_cancelled_turn_cancels_the_selector():
    """#2250 (Arch 13:13): a cancelled turn stays cancelled and never waits on the call."""
    started = asyncio.Event()
    selector_cancelled = asyncio.Event()
    h = TodoIntentHandlers()

    async def select(message, user_id):
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            selector_cancelled.set()
            raise

    async def read(**kw):
        started.set()
        await asyncio.sleep(10)

    h._resolve_list_selection = select
    h.todo_service = MagicMock()
    h.todo_service.list_todos = read
    turn = asyncio.ensure_future(h.handle_list_todos(_intent(), "s", USER))
    await started.wait()
    turn.cancel()
    with pytest.raises(asyncio.CancelledError):
        await turn
    await asyncio.wait_for(selector_cancelled.wait(), timeout=1)


@pytest.mark.asyncio
async def test_a_selector_past_the_ceiling_gives_todays_list(monkeypatch):
    """Arch 11-06 07:54: a hard ceiling on the await; a timeout is failed, so the list."""
    import services.intent_service.todo_handlers as th

    monkeypatch.setattr(th, "SELECTOR_CEILING_S", 0.01)
    h = TodoIntentHandlers()
    cancelled = asyncio.Event()

    async def select(message, user_id):
        try:
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            cancelled.set()
            raise
        return TodoSelection(outcome=OUTCOME_NEXT)

    h._resolve_list_selection = select
    h.todo_service = MagicMock()
    h.todo_service.list_todos = AsyncMock(return_value=[_todo("a"), _todo("b")])
    reply = await h.handle_list_todos(_intent(), "s", USER)
    assert reply.startswith("You have 2 open todos. Here they are:")
    assert cancelled.is_set()


def test_the_ceiling_sits_above_the_measured_range():
    from services.intent_service.todo_handlers import SELECTOR_CEILING_S

    assert SELECTOR_CEILING_S == 2.5
