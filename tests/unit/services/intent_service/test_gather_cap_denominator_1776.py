"""#1776 — a gather cap must never present itself as a total.

#1762's census separated four classes of truncation. Class (d) is this one,
and it is NOT the render-provenance defect the rest of that sweep fixed:

    A render cap truncates a string that a full structured set produced, so
    "render == data" is the expressible repair. A GATHER cap truncates
    BEFORE any render exists — the data genuinely IS short and the render is
    honest about the short data it was handed. The defect moves to the
    DENOMINATOR.

The assembler already holds the honest shape in two places, and this suite
mirrors it rather than inventing a second mechanism:

  * ``pending_todo_count`` (#1544) / ``completed_todo_count`` (#1639) — a
    row-derived companion count rides beside the capped list.
  * ``_compute_projects`` (#1645) — ``COUNT(*) OVER ()`` rides the same
    LIMIT-ed query, so the true total costs no extra round trip.

The uncounted sites let the floor's denominator silently BECOME the cap, and
two sites are worse than silent — they state the slice length as a total:

  * ``_format_agenda_granular``: ``**Total**: {len(todos)} pending tasks``
    over a ``limit=10`` gather. A user with 25 pending todos is TOLD they
    have 10. (``_format_agenda_embedded``'s ``{len(todos)} tasks`` is the
    same statement in the terse register — found by this session's census,
    not named in #1776.)
  * ``_gather_insight_pull_context``: ``total_count = len(insights)`` over a
    ``limit=50`` read, rendered by the floor as "(N total, sectioned by
    confidence)". Also census-found; the key is literally named `total`.

Layer honesty (m-43): every test here pins a DETERMINISTIC seam — the
formatters called directly with their real signatures, the handler seam with
the repository mocked, the assembler's gather methods with their data sources
mocked, and the floor's real ``_format_domain_context`` prompt-composition.
No live model, no DB, no delivered turn.

Denominator (m-44): this suite covers the four uncounted gather sites plus
the two false-total renders. The COUNTED sites (pending/completed todos,
`projects`, blocked items, milestones, recent activity, high-priority issues)
are pinned here only as GREEN CONTROLS — they were already honest.
"""

from contextlib import asynccontextmanager
from typing import List
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import ConversationalFloor

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def handler():
    return CanonicalHandlers()


def _todos(n: int, priority: str = "medium", prefix: str = "Task") -> List[dict]:
    return [
        {"title": f"{prefix} {i}", "priority": priority, "due_date": None, "context": None}
        for i in range(1, n + 1)
    ]


def _user_ctx(projects=None, priorities=None, organization=None):
    """A user_context_service-shaped object (attribute access, not dict)."""
    obj = MagicMock()
    obj.projects = projects if projects is not None else []
    obj.priorities = priorities if priorities is not None else []
    obj.organization = organization
    return obj


def _floor():
    """Real ConversationalFloor, LLM client mocked — we call the deterministic
    prompt-composition method directly, never a model."""
    return ConversationalFloor(llm_client=MagicMock())


def _domain_lines(domain_context: dict) -> str:
    return _floor()._format_domain_context(domain_context)


# ===========================================================================
# 1. The agenda's `**Total**` — an ACTIVELY FALSE statement, the #1776 priority
# ===========================================================================


class TestAgendaTotalIsTheSourceCountNotTheSliceLength:
    def test_granular_total_states_the_row_derived_count(self, handler):
        """25 pending todos, 10 gathered: the Total line says 25, not 10."""
        msg = handler._format_agenda_granular(None, _todos(10), [], total_pending=25)
        assert "**Total**: 25 pending tasks" in msg
        assert "**Total**: 10 pending tasks" not in msg

    def test_granular_names_the_shown_subset_when_truncated(self, handler):
        """A true denominator over an unannounced subset is still a promise
        only the render can see (#1762's inverted-canary lesson). Say which
        part was shown."""
        msg = handler._format_agenda_granular(None, _todos(10), [], total_pending=25)
        assert "10" in msg.split("**Total**:")[1]

    def test_granular_falls_back_to_len_when_no_count_supplied(self, handler):
        """GREEN CONTROL: with no separate count, the slice length is all the
        formatter knows — and it is then TRUE (nothing was capped away)."""
        msg = handler._format_agenda_granular(None, _todos(4), [])
        assert "**Total**: 4 pending tasks" in msg

    def test_granular_adds_no_truncation_notice_when_nothing_truncated(self, handler):
        """GREEN CONTROL: total == shown renders exactly as before."""
        msg = handler._format_agenda_granular(None, _todos(4), [], total_pending=4)
        assert "**Total**: 4 pending tasks" in msg
        assert "showing" not in msg.lower()

    def test_embedded_task_count_states_the_row_derived_count(self, handler):
        """Same false statement in the terse register: EMBEDDED renders a bare
        count and NO list, so the count is the entire claim."""
        msg = handler._format_agenda_embedded(None, _todos(10), [], total_pending=25)
        assert "25 tasks" in msg
        assert "10 tasks" not in msg

    def test_standard_states_a_denominator_when_the_gather_was_capped(self, handler):
        """STANDARD lists todos and states no total at all — silent, not false.
        Silence over a capped gather is m-44's purest form: the truncation is
        not reported, so it reads as a measurement."""
        msg = handler._format_agenda_standard(None, _todos(10), [], total_pending=25)
        assert "25" in msg

    def test_standard_unchanged_when_nothing_truncated(self, handler):
        """GREEN CONTROL: the un-capped render keeps its pre-#1776 shape."""
        msg = handler._format_agenda_standard(None, _todos(3), [], total_pending=3)
        assert "Here's your agenda for today:" in msg
        assert "showing" not in msg.lower()

    def test_no_formatter_presents_the_gather_cap_as_a_total(self, handler):
        """The class invariant, stated once over all three formatters: when the
        source count exceeds the gather cap, the cap must not appear as a
        total anywhere in the render."""
        cap, true_total = 10, 25
        todos = _todos(cap)
        for fmt in (
            handler._format_agenda_embedded,
            handler._format_agenda_standard,
            handler._format_agenda_granular,
        ):
            msg = fmt(None, todos, [], total_pending=true_total)
            assert str(true_total) in msg, f"{fmt.__name__} dropped the true total"
            assert f"**Total**: {cap} " not in msg
            assert f"{cap} tasks" not in msg, f"{fmt.__name__} states the cap as a total"


# ===========================================================================
# 2. The gather itself must PRODUCE the true count — no extra query
# ===========================================================================


def _todo_row(text: str, priority: str = "medium"):
    row = MagicMock()
    row.text = text
    row.priority = priority
    row.due_date = None
    row.context = None
    return row


def _repo_returning(todos, total):
    repo = MagicMock()
    repo.get_todos_by_owner_with_total = AsyncMock(return_value=(todos, total))
    return repo


@asynccontextmanager
async def _fake_scope(session=None):
    yield session or MagicMock()


class TestGetTodaysTodosCarriesTheRowDerivedTotal:
    @pytest.mark.asyncio
    async def test_returns_capped_items_and_the_true_total(self):
        rows = [_todo_row(f"t{i}") for i in range(10)]
        repo = _repo_returning(rows, 25)

        with (
            patch("services.repositories.todo_repository.TodoRepository", return_value=repo),
            patch("services.database.session_factory.AsyncSessionFactory") as factory,
        ):
            factory.session_scope = _fake_scope
            todos, total = await CanonicalHandlers()._get_todays_todos(user_id=str(uuid4()))

        assert len(todos) == 10
        assert total == 25, "the gather must surface the pre-LIMIT row count"

    @pytest.mark.asyncio
    async def test_anonymous_caller_owns_nothing(self):
        todos, total = await CanonicalHandlers()._get_todays_todos(user_id=None)
        assert todos == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_source_failure_keeps_the_none_sentinel(self):
        """#1425: a failed lookup stays None so the formatters render
        "couldn't check", never "no tasks". The tuple must not launder that."""
        repo = MagicMock()
        repo.get_todos_by_owner_with_total = AsyncMock(side_effect=RuntimeError("db down"))

        with (
            patch("services.repositories.todo_repository.TodoRepository", return_value=repo),
            patch("services.database.session_factory.AsyncSessionFactory") as factory,
        ):
            factory.session_scope = _fake_scope
            todos, total = await CanonicalHandlers()._get_todays_todos(user_id=str(uuid4()))

        assert todos is None
        assert total == 0


class TestTodoRepositoryWindowCountRidesTheSameQuery:
    """#1645's idiom, applied to todos: COUNT(*) OVER () is computed before
    LIMIT, so one query yields both the capped page and the true total."""

    @pytest.mark.asyncio
    async def test_window_count_is_in_the_statement_and_one_query_runs(self):
        from services.database.models import TodoStatus
        from services.repositories.todo_repository import TodoRepository

        db_todo = MagicMock()
        db_todo.to_domain.return_value = "domain-todo"
        result = MagicMock()
        result.all.return_value = [(db_todo, 25) for _ in range(10)]
        session = MagicMock()
        session.execute = AsyncMock(return_value=result)

        todos, total = await TodoRepository(session).get_todos_by_owner_with_total(
            owner_id="owner-1", status=TodoStatus.PENDING, limit=10
        )

        assert total == 25
        assert len(todos) == 10
        assert session.execute.await_count == 1, "the count must not cost a second query"
        stmt = str(session.execute.await_args.args[0])
        assert "count(*) OVER ()" in stmt.replace("COUNT", "count")
        assert "LIMIT" in stmt

    @pytest.mark.asyncio
    async def test_empty_result_is_a_true_zero(self):
        from services.repositories.todo_repository import TodoRepository

        result = MagicMock()
        result.all.return_value = []
        session = MagicMock()
        session.execute = AsyncMock(return_value=result)

        todos, total = await TodoRepository(session).get_todos_by_owner_with_total(
            owner_id="owner-1"
        )
        assert todos == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_legacy_list_only_method_still_returns_a_plain_list(self):
        """GREEN CONTROL: `get_todos_by_owner` keeps its contract for the
        callers that do not need a denominator."""
        from services.repositories.todo_repository import TodoRepository

        db_todo = MagicMock()
        db_todo.to_domain.return_value = "domain-todo"
        result = MagicMock()
        result.all.return_value = [(db_todo, 3)]
        session = MagicMock()
        session.execute = AsyncMock(return_value=result)

        out = await TodoRepository(session).get_todos_by_owner(owner_id="owner-1")
        assert out == ["domain-todo"]


class TestAgendaHandlerSeamThreadsTheTotal:
    @pytest.mark.asyncio
    async def test_granular_agenda_reports_the_true_total_end_to_end(self):
        """The handler seam, data source mocked: 10 gathered of 25 → the
        delivered message states 25."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on the agenda today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "GRANULAR"}

        handlers = CanonicalHandlers()
        with (
            patch.object(handlers, "_get_calendar_context", AsyncMock(return_value=None)),
            patch(
                "services.intent_service.canonical_handlers.CanonicalHandlers._get_todays_todos",
                AsyncMock(return_value=(_todos(10), 25)),
            ),
            patch("services.intent_service.canonical_handlers.user_context_service") as ucs,
        ):
            ucs.get_user_context = AsyncMock(return_value=_user_ctx(priorities=[]))
            result = await handlers._handle_agenda_query(intent, "sess", user_id=str(uuid4()))

        assert "**Total**: 25 pending tasks" in result["message"]
        assert "**Total**: 10 pending tasks" not in result["message"]
        assert result["intent"]["context"]["todo_count"] == 25
        assert result["intent"]["context"]["todos_shown"] == 10

    @pytest.mark.asyncio
    async def test_todo_source_failure_does_not_crash_the_agenda(self):
        """Discovered work (#1777), pinned here because #1776 is the commit
        that touches the expression: ``agenda_sources["todos"]`` was a bare
        ``len(todos)`` while its sibling two lines up guarded the #1425 None
        sentinel — so a todo-source FAILURE raised TypeError and took the
        whole agenda response down."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on the agenda today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        handlers = CanonicalHandlers()
        with (
            patch.object(handlers, "_get_calendar_context", AsyncMock(return_value=None)),
            patch(
                "services.intent_service.canonical_handlers.CanonicalHandlers._get_todays_todos",
                AsyncMock(return_value=(None, 0)),
            ),
            patch("services.intent_service.canonical_handlers.user_context_service") as ucs,
        ):
            ucs.get_user_context = AsyncMock(return_value=_user_ctx(priorities=[]))
            result = await handlers._handle_agenda_query(intent, "sess", user_id=str(uuid4()))

        assert "couldn't check your tasks" in result["message"]
        assert result["intent"]["context"]["todo_count"] is None
        # #1777 sweep: this asserted `== 0`, the value the #1776 guard chose to
        # stop the crash. Stopping the crash was right; reporting a failed
        # source as having contributed zero todos was the SAME false claim one
        # layer down. Now `None`, matching `todo_count` above. The full census
        # and the retrospective twin live in
        # tests/unit/services/intent_service/test_sentinel_consumer_sweep_1777.py.
        assert result["agenda_sources"]["todos"] is None


# ===========================================================================
# 3. The assembler's UNCOUNTED gathers gain a companion count
# ===========================================================================


class TestIdentityUserProjectsCarryACount:
    @pytest.mark.asyncio
    async def test_capped_user_projects_ride_with_the_true_count(self):
        assembler = ContextAssembler()
        ucs = MagicMock()
        ucs.get_user_context = AsyncMock(
            return_value=_user_ctx(projects=[f"p{i}" for i in range(8)])
        )
        with patch("services.user_context_service.user_context_service", ucs):
            ctx = await assembler._gather_identity_context(user_id=str(uuid4()))

        assert len(ctx["user_projects"]) == 5, "the gather cap itself is unchanged"
        assert ctx["user_project_count"] == 8, "the denominator must be the SOURCE count"

    @pytest.mark.asyncio
    async def test_uncapped_user_projects_still_carry_the_count(self):
        assembler = ContextAssembler()
        ucs = MagicMock()
        ucs.get_user_context = AsyncMock(return_value=_user_ctx(projects=["a", "b"]))
        with patch("services.user_context_service.user_context_service", ucs):
            ctx = await assembler._gather_identity_context(user_id=str(uuid4()))

        assert ctx["user_projects"] == ["a", "b"]
        assert ctx["user_project_count"] == 2


class TestUserContextPrioritiesCarryACount:
    @pytest.mark.asyncio
    async def test_capped_priorities_ride_with_the_true_count(self):
        assembler = ContextAssembler()
        ucs = MagicMock()
        ucs.get_user_context = AsyncMock(
            return_value=_user_ctx(priorities=[f"prio {i}" for i in range(7)])
        )
        with patch("services.user_context_service.user_context_service", ucs):
            out = await assembler._compute_user_context(str(uuid4()))

        assert len(out["priorities"]["user_priorities"]) == 5
        assert out["priorities"]["user_priority_count"] == 7

    @pytest.mark.asyncio
    async def test_projects_count_is_unchanged_green_control(self):
        """GREEN CONTROL: #1530 already counted this one — proof the census
        claim that `projects[:10]` is uncounted was STALE."""
        assembler = ContextAssembler()
        ucs = MagicMock()
        ucs.get_user_context = AsyncMock(
            return_value=_user_ctx(projects=[f"p{i}" for i in range(14)])
        )
        with patch("services.user_context_service.user_context_service", ucs):
            out = await assembler._compute_user_context(str(uuid4()))

        assert len(out["projects"]) == 10
        assert out["project_count"] == 14


class TestInsightTotalCountIsRowDerived:
    @pytest.mark.asyncio
    async def test_total_count_is_not_the_fifty_row_read_cap(self):
        """`total_count` over a `limit=50` read was the slice length wearing
        the word "total" — and the floor renders it as "(N total…)"."""
        insights = []
        for i in range(50):
            learning = MagicMock()
            learning.confidence = 0.9
            learning.topic_tags = []
            learning.insight = MagicMock(expression=f"insight {i}", description="")
            ins = MagicMock()
            ins.learning = learning
            ins.id = f"i{i}"
            ins.surfaced_count = 1
            ins.created_at = None
            insights.append(ins)

        repo = MagicMock()
        repo.list_for_user_with_total = AsyncMock(return_value=(insights, 0, 137))

        with (
            patch("services.database.repositories.InsightRepository", return_value=repo),
            patch("services.database.session_factory.AsyncSessionFactory") as factory,
        ):
            factory.session_scope = _fake_scope
            ctx = await ContextAssembler()._gather_insight_pull_context(str(uuid4()))

        assert ctx["insights"]["total_count"] == 137
        assert ctx["insights"]["total_count"] != 50
        assert ctx["insights"]["is_empty"] is False


# ===========================================================================
# 4. The floor states a denominator over every capped gather it renders
# ===========================================================================


class TestFloorStatesTheTrueDenominator:
    def test_user_projects_line_names_the_true_count_when_capped(self):
        out = _domain_lines({"user_projects": ["a", "b", "c", "d", "e"], "user_project_count": 8})
        assert "8" in out
        line = [ln for ln in out.splitlines() if "active projects" in ln.lower()]
        assert line, "the user-projects line must still render"

    def test_user_projects_line_is_unadorned_when_complete(self):
        """GREEN CONTROL: count == shown adds no truncation clause."""
        out = _domain_lines({"user_projects": ["a", "b"], "user_project_count": 2})
        assert "only the first" not in out

    def test_priorities_line_names_the_true_count_when_capped(self):
        out = _domain_lines(
            {
                "priorities": {
                    "user_priorities": ["p1", "p2", "p3", "p4", "p5"],
                    "user_priority_count": 9,
                }
            }
        )
        assert "9" in out

    def test_priorities_line_is_unadorned_when_complete(self):
        out = _domain_lines({"priorities": {"user_priorities": ["p1"], "user_priority_count": 1}})
        assert "only the first" not in out

    def test_projects_counted_lane_is_unchanged_green_control(self):
        """GREEN CONTROL: #1530/#1645's renderer is the shape being mirrored."""
        out = _domain_lines({"projects": [{"name": f"p{i}"} for i in range(5)], "project_count": 9})
        assert "Active project count: 9" in out
        assert "only the first 5 are listed above" in out

    def test_pending_todos_counted_lane_is_unchanged_green_control(self):
        out = _domain_lines(
            {"pending_todos": [{"text": f"t{i}"} for i in range(10)], "pending_todo_count": 25}
        )
        assert "PENDING TODOS (25)" in out
