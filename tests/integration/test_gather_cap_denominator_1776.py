"""#1776 at the DB layer: the gather cap's companion count is a REAL pre-LIMIT
row count, proven against Postgres — not a mock's return value.

The unit suite (`tests/unit/services/intent_service/test_gather_cap_denominator_1776.py`)
pins the contract with a mocked session, which proves the plumbing and the
render but CANNOT prove the statement is valid SQL or that `COUNT(*) OVER ()`
survives the `LIMIT` — the two claims the whole fix rests on. A mock returning
`(rows, 25)` would pass identically if the window function were nonsense.

m-43 (name the layer): this file is the DB layer and only the DB layer. It
seeds more rows than the gather cap, reads through the real repository, and
follows the value up through `_get_todays_todos` into the rendered agenda.

Mirrors the scratch-user fixture from `test_pending_todos_query_1544.py`.
"""

import uuid

import pytest
from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.repositories.todo_repository import TodoRepository
from services.shared_types import TodoStatus

# More pending rows than `_get_todays_todos`' cap of 10 — the entire point.
_SEEDED = 25
_GATHER_CAP = 10


@pytest.fixture
async def scratch_user():
    """A scratch user, removed with its todos afterwards."""
    username = f"todo-1776-{uuid.uuid4().hex[:8]}"
    async with AsyncSessionFactory.session_scope() as s:
        r = await s.execute(
            text(
                "INSERT INTO users (username, email, is_active) "
                "VALUES (:u, :e, true) RETURNING id"
            ),
            {"u": username, "e": f"{username}@example.com"},
        )
        uid = r.scalar()
        await s.commit()
    yield uid
    async with AsyncSessionFactory.session_scope() as s:
        await s.execute(text("DELETE FROM todo_items WHERE owner_id = :u"), {"u": str(uid)})
        await s.execute(
            text(
                "DELETE FROM items WHERE id NOT IN (SELECT id FROM todo_items) "
                "AND text LIKE 'repro-1776%'"
            )
        )
        await s.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


async def _seed(user_id) -> None:
    from services.todo.todo_management_service import TodoManagementService

    svc = TodoManagementService()
    for i in range(_SEEDED):
        await svc.create_todo(text=f"repro-1776 pending item {i:02d}", user_id=user_id)


async def test_window_count_survives_the_limit_against_real_postgres(scratch_user):
    """The load-bearing SQL claim: `COUNT(*) OVER ()` is evaluated before
    `LIMIT`, so a 10-row page carries the full 25."""
    await _seed(scratch_user)

    async with AsyncSessionFactory.session_scope() as s:
        todos, total = await TodoRepository(s).get_todos_by_owner_with_total(
            owner_id=str(scratch_user), status=TodoStatus.PENDING, limit=_GATHER_CAP
        )

    assert len(todos) == _GATHER_CAP, "the gather cap must still cap"
    assert total == _SEEDED, "the count must be the pre-LIMIT row count, not the page size"


async def test_legacy_list_contract_unchanged_against_real_postgres(scratch_user):
    """`get_todos_by_owner` delegates to the window-count query now. Its
    callers must still receive a plain list of domain objects."""
    await _seed(scratch_user)

    async with AsyncSessionFactory.session_scope() as s:
        todos = await TodoRepository(s).get_todos_by_owner(
            owner_id=str(scratch_user), status=TodoStatus.PENDING, limit=_GATHER_CAP
        )

    assert isinstance(todos, list)
    assert len(todos) == _GATHER_CAP
    assert all(hasattr(t, "text") for t in todos)


async def test_agenda_states_the_true_total_over_a_capped_gather(scratch_user):
    """End of the chain: a user with 25 pending todos is told 25, not 10.

    Pre-#1776 this rendered "**Total**: 10 pending tasks" — the gather cap
    presented as the user's own count.
    """
    await _seed(scratch_user)

    handlers = CanonicalHandlers()
    todos, total_pending = await handlers._get_todays_todos(user_id=str(scratch_user))

    assert todos is not None and len(todos) == _GATHER_CAP
    assert total_pending == _SEEDED

    message = handlers._format_agenda_granular(None, todos, [], total_pending=total_pending)
    assert f"**Total**: {_SEEDED} pending tasks" in message
    assert f"**Total**: {_GATHER_CAP} pending tasks" not in message
    assert f"showing the first {_GATHER_CAP} above" in message


async def test_empty_owner_gets_an_exact_zero_not_an_absence(scratch_user):
    """#1544/#1639's verified-empty distinction survives the tuple: the read
    RAN and found nothing, so both the page and the denominator are 0."""
    async with AsyncSessionFactory.session_scope() as s:
        todos, total = await TodoRepository(s).get_todos_by_owner_with_total(
            owner_id=str(scratch_user), status=TodoStatus.PENDING, limit=_GATHER_CAP
        )

    assert todos == []
    assert total == 0
