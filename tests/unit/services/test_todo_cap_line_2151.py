"""#2151 TODO-CAP (CXO 10-23 17:55): "Showing your first 100 tasks."

The list read took a 100-row window that included completed rows and dropped them
afterwards, so an account with many completed todos saw a short active list, and
nothing said the list was capped. Completion is now filtered in SQL (the window holds
the rows asked for), ``list_todos`` returns a ``TodoPage`` whose ``capped`` says more
rows matched than the window held, and the list reply says so in CXO's words.
"""

from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.repositories.todo_repository import TodoRepository
from services.todo.todo_management_service import (
    TODO_LIST_CAP,
    TodoManagementService,
    TodoPage,
)


class _CapturingSession:
    def __init__(self):
        self.statements = []

    async def execute(self, statement):
        self.statements.append(statement)
        result = MagicMock()
        result.all.return_value = []
        return result


def _where(statement) -> str:
    sql = str(statement.compile(compile_kwargs={"literal_binds": True}))
    return sql.split("WHERE", 1)[1].split("ORDER BY", 1)[0], sql


@pytest.mark.asyncio
async def test_completion_is_filtered_in_sql_before_the_limit():
    session = _CapturingSession()
    await TodoRepository(session).get_todos_by_owner_with_total(
        "owner-1", completed=False, limit=TODO_LIST_CAP
    )
    where, sql = _where(session.statements[0])
    assert "completed" in where
    assert "LIMIT 100" in sql


@pytest.mark.asyncio
async def test_no_completion_filter_when_completed_is_none():
    session = _CapturingSession()
    await TodoRepository(session).get_todos_by_owner_with_total("owner-1", completed=None)
    where, _ = _where(session.statements[0])
    assert "completed" not in where


@asynccontextmanager
async def _fake_scope():
    yield MagicMock()


def _todo(n, completed=False):
    return SimpleNamespace(text=f"fake {n}", completed=completed, list_id=None, status="pending")


async def _list(repo_read, **kwargs):
    with (
        patch(
            "services.todo.todo_management_service.AsyncSessionFactory.session_scope",
            new=_fake_scope,
        ),
        patch.object(TodoRepository, "get_todos_by_owner_with_total", new=repo_read),
    ):
        service = TodoManagementService.__new__(TodoManagementService)
        return await service.list_todos(user_id=uuid4(), **kwargs)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "rows,total,capped", [(100, 140, True), (100, 100, False), (3, 3, False), (0, 0, False)]
)
async def test_list_todos_says_whether_the_window_was_full(rows, total, capped):
    repo_read = AsyncMock(return_value=([_todo(i) for i in range(rows)], total))
    out = await _list(repo_read)
    assert isinstance(out, TodoPage) and isinstance(out, list)
    assert out.capped is capped
    assert len(out) == rows
    assert repo_read.await_args.kwargs["completed"] is False
    assert repo_read.await_args.kwargs["limit"] == TODO_LIST_CAP


@pytest.mark.asyncio
async def test_include_completed_reads_both():
    repo_read = AsyncMock(return_value=([_todo(1), _todo(2, completed=True)], 2))
    out = await _list(repo_read, include_completed=True)
    assert len(out) == 2
    assert repo_read.await_args.kwargs["completed"] is None


async def _list_reply(page):
    from services.intent_service.todo_handlers import TodoIntentHandlers

    handlers = TodoIntentHandlers.__new__(TodoIntentHandlers)
    handlers.todo_service = MagicMock()
    handlers.todo_service.list_todos = AsyncMock(return_value=page)
    intent = SimpleNamespace(original_message="show my todos", context={})
    with patch(
        "services.intent_service.todo_handlers.format_todo_list_conscious",
        return_value="FAKE LIST",
    ):
        return await handlers.handle_list_todos(intent, "s1", uuid4())


@pytest.mark.asyncio
async def test_a_capped_list_says_so_in_cxos_words():
    page = TodoPage([_todo(i) for i in range(100)], capped=True)
    assert await _list_reply(page) == "FAKE LIST\n\nShowing your first 100 tasks."


@pytest.mark.asyncio
async def test_an_uncapped_list_has_no_cap_line():
    assert await _list_reply(TodoPage([_todo(1)], capped=False)) == "FAKE LIST"
    assert await _list_reply([_todo(1)]) == "FAKE LIST"


# ── Arch 10-24 08:26: the list and status filters run in SQL too ──


@pytest.mark.asyncio
async def test_list_and_status_filters_are_in_sql_before_the_limit():
    session = _CapturingSession()
    await TodoRepository(session).get_todos_by_owner_with_total(
        "owner-1", status="pending", list_id="list-x", completed=False, limit=TODO_LIST_CAP
    )
    where, sql = _where(session.statements[0])
    assert "list_id" in where and "'list-x'" in where
    assert "status" in where and "'pending'" in where
    assert "LIMIT 100" in sql


@pytest.mark.asyncio
async def test_a_list_past_the_first_hundred_comes_back_whole_and_uncapped():
    """120 active rows, 10 on list X ranked after the first 100: the SQL filter returns
    all 10, the total is 10, and nothing is capped (the post-filter returned the matches
    among the first 100 and said capped)."""
    list_x = [_todo(i) for i in range(10)]
    repo_read = AsyncMock(return_value=(list_x, 10))
    out = await _list(repo_read, list_id="list-x")
    assert len(out) == 10 and out.capped is False
    assert repo_read.await_args.kwargs["list_id"] == "list-x"


@pytest.mark.asyncio
async def test_the_status_filter_is_passed_down():
    repo_read = AsyncMock(return_value=([], 0))
    await _list(repo_read, status="blocked")
    assert repo_read.await_args.kwargs["status"] == "blocked"
