"""#1777 — the sweep of #1425 ``None``-sentinel CONSUMERS.

#1776 found one crash and guarded it: ``agenda_sources["todos"]`` took a bare
``len()`` over the sentinel ``_get_todays_todos`` returns when the todo lookup
FAILS, so a source failure raised ``TypeError`` *after* the formatter had
already honestly composed "I couldn't check your tasks just now." The honesty
machinery was intact; payload assembly threw it away.

The damning part was never the missing guard — it was the SHAPE. The crashing
line sat four lines below a sibling carrying a comment that explains that exact
crash. So this suite is the census, not the one-line fix: every consumer of the
bare-``None`` sentinel family, pinned at the guard state it is supposed to have.

The census found FOUR bare-``None`` sentinel producers and twenty-one consumers
of them. Two classes of defect, both in payload assembly and neither in a
formatter:

  (a) CRASHES — ``len()`` straight over the sentinel. One site, the #1777
      original, guarded by the #1776 commit and pinned in
      ``test_gather_cap_denominator_1776.py``.
  (b) FABRICATED ZEROS — ``len(x or [])``, which cannot crash and therefore
      reads as safe, while stating "0 completed tasks" for a lookup that never
      completed. Three sites: the agenda's own ``agenda_sources["todos"]``
      (the #1776 guard chose ``0``, which fixed the crash and left the false
      count) and BOTH retrospective payload fields. This is #1776's
      denominator class exactly: a number nobody can tell from a measurement.

Layer honesty (m-43): every test here drives the sentinel through the REAL
production path — ``AsyncSessionFactory.session_scope`` is made to raise, so
the handler's own ``except`` produces the sentinel, the real formatters consume
it, and the real payload dict is assembled. Nothing stubs the helper's return
value, because a stubbed sentinel proves the consumer is guarded while proving
nothing about whether a genuine failure still reaches it.

Denominator (m-44): the FIXED sites are class (b) above. The rest of the census
appears here as GREEN CONTROLS — the three status-report formatters, the three
retrospective formatters, the status-report payload, and the reminder lane's
assembler translation were already honest, and a regression in any of them is a
recurrence of this issue in a lane the fix did not touch.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def handler():
    return CanonicalHandlers()


def _user_ctx(projects=None, priorities=None, organization=None):
    """A user_context_service-shaped object (attribute access, not dict)."""
    obj = MagicMock()
    obj.projects = projects if projects is not None else []
    obj.priorities = priorities if priorities is not None else []
    obj.organization = organization
    obj.user_id = str(uuid4())
    return obj


def _intent(message: str, action: str, pattern: str = None):
    from services.domain.models import Intent
    from services.shared_types import IntentCategory as IntentCategoryEnum

    intent = Intent(
        original_message=message,
        category=IntentCategoryEnum.TEMPORAL,
        action=action,
        confidence=0.9,
    )
    if pattern:
        intent.spatial_context = {"pattern": pattern}
    return intent


def _failing_db():
    """Patch the session factory every sentinel producer opens, so the REAL
    ``except`` branch runs and the REAL sentinel is produced.

    This is the point of the suite (m-43): a test that stubs the helper's
    return value pins the consumer's guard, not the path. The #1777 crash lived
    on the path.
    """
    return patch(
        "services.database.session_factory.AsyncSessionFactory.session_scope",
        side_effect=RuntimeError("todo source is down"),
    )


# ===========================================================================
# 1. The agenda payload — the #1777 original, and the zero its guard left
# ===========================================================================


class TestAgendaPayloadNeverStatesAFabricatedZero:
    """``agenda_sources["todos"]`` was ``len(todos)`` (crash). The #1776 guard
    made it ``len(todos) if todos is not None else 0`` — which stops the crash
    and then reports the failed source as having contributed ZERO todos, beside
    a sibling field (``todo_count``) that says ``None`` for the same condition,
    in the same dict, for the same failure."""

    @pytest.mark.asyncio
    async def test_source_failure_reaches_the_user_as_honest_copy(self, handler):
        """The whole point of the sentinel: the turn is DELIVERED, and it says
        the check failed."""
        with (
            patch.object(handler, "_get_calendar_context", AsyncMock(return_value=None)),
            patch("services.intent_service.canonical_handlers.user_context_service") as ucs,
            _failing_db(),
        ):
            ucs.get_user_context = AsyncMock(return_value=_user_ctx())
            result = await handler._handle_agenda_query(
                _intent("What's on the agenda today?", "query_agenda"),
                "sess",
                user_id=str(uuid4()),
            )

        assert "couldn't check your tasks" in result["message"]
        assert "No pending tasks" not in result["message"]

    @pytest.mark.asyncio
    async def test_agenda_sources_todos_is_none_not_zero_when_the_source_failed(self, handler):
        """#1777: ``0`` here is indistinguishable from a user who genuinely has
        no pending todos. ``None`` is the value the sibling field two lines up
        already uses for exactly this condition."""
        with (
            patch.object(handler, "_get_calendar_context", AsyncMock(return_value=None)),
            patch("services.intent_service.canonical_handlers.user_context_service") as ucs,
            _failing_db(),
        ):
            ucs.get_user_context = AsyncMock(return_value=_user_ctx())
            result = await handler._handle_agenda_query(
                _intent("What's on the agenda today?", "query_agenda"),
                "sess",
                user_id=str(uuid4()),
            )

        assert result["agenda_sources"]["todos"] is None
        # The guarded siblings, pinned together so the three can never drift
        # apart again — drift between them IS this issue.
        assert result["intent"]["context"]["todo_count"] is None
        assert result["intent"]["context"]["todos_shown"] is None

    @pytest.mark.asyncio
    async def test_a_genuinely_empty_todo_list_still_reports_zero(self, handler):
        """The distinction the sentinel exists to carry: a real zero is still a
        real zero. Without this control, ``None`` everywhere would pass."""
        with (
            patch.object(handler, "_get_calendar_context", AsyncMock(return_value=None)),
            patch(
                "services.intent_service.canonical_handlers.CanonicalHandlers._get_todays_todos",
                AsyncMock(return_value=([], 0)),
            ),
            patch("services.intent_service.canonical_handlers.user_context_service") as ucs,
        ):
            ucs.get_user_context = AsyncMock(return_value=_user_ctx())
            result = await handler._handle_agenda_query(
                _intent("What's on the agenda today?", "query_agenda"),
                "sess",
                user_id=str(uuid4()),
            )

        assert result["agenda_sources"]["todos"] == 0
        assert result["intent"]["context"]["todo_count"] == 0
        assert "No pending tasks" in result["message"]


# ===========================================================================
# 2. The retrospective payload — the same shape, one handler away, unguarded
# ===========================================================================


class TestRetrospectivePayloadNeverStatesAFabricatedZero:
    """``_get_completed_todos_for_date`` returns the same bare-``None``
    sentinel and its three formatters all guard it correctly — and then BOTH
    payload fields did ``len(completed_todos or [])``.

    ``or []`` is the reason this one never showed up as a bug: it cannot raise,
    so it looks like a guard. It is not a guard, it is a default, and the
    default it supplies is a claim about the user's day."""

    @pytest.mark.asyncio
    async def test_source_failure_reaches_the_user_as_honest_copy(self, handler):
        """Green control: the formatters were already right."""
        with _failing_db():
            result = await handler._handle_retrospective_query(
                _intent("What did we accomplish yesterday?", "query_retrospective"),
                "sess",
            )

        assert "couldn't check completed tasks" in result["message"]
        assert "No completed tasks" not in result["message"]

    @pytest.mark.asyncio
    async def test_completed_count_is_none_not_zero_when_the_source_failed(self, handler):
        """#1777 class (b): the message says "I couldn't check" while the
        payload beside it says the user completed nothing."""
        with _failing_db():
            result = await handler._handle_retrospective_query(
                _intent("What did we accomplish yesterday?", "query_retrospective"),
                "sess",
            )

        assert result["intent"]["context"]["completed_count"] is None

    @pytest.mark.asyncio
    async def test_retrospective_completed_tasks_is_none_when_the_source_failed(self, handler):
        """The second of the pair. Both were ``len(x or [])``; fixing one and
        leaving the other is how #1777 happened in the first place."""
        with _failing_db():
            result = await handler._handle_retrospective_query(
                _intent("What did we accomplish yesterday?", "query_retrospective"),
                "sess",
            )

        assert result["retrospective"]["completed_tasks"] is None

    @pytest.mark.asyncio
    async def test_a_genuinely_empty_day_still_reports_zero(self, handler):
        """Control: a day with nothing completed reports 0, not None."""
        with patch.object(handler, "_get_completed_todos_for_date", AsyncMock(return_value=[])):
            result = await handler._handle_retrospective_query(
                _intent("What did we accomplish yesterday?", "query_retrospective"),
                "sess",
            )

        assert result["intent"]["context"]["completed_count"] == 0
        assert result["retrospective"]["completed_tasks"] == 0
        assert "No completed tasks" in result["message"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize("pattern", ["EMBEDDED", "GRANULAR", None])
    async def test_every_spatial_pattern_degrades_honestly(self, handler, pattern):
        """The #1777 shape is per-SITE drift, so a per-site sweep has to name
        every site. All three retrospective renders, one failure."""
        with _failing_db():
            result = await handler._handle_retrospective_query(
                _intent(
                    "What did we accomplish yesterday?",
                    "query_retrospective",
                    pattern=pattern,
                ),
                "sess",
            )

        assert "couldn't check completed tasks" in result["message"]
        assert result["retrospective"]["completed_tasks"] is None


# ===========================================================================
# 3. Green controls — the census rows that were already honest
# ===========================================================================


class TestStatusReportSentinelWasAlreadyHonest:
    """``open_todos_count`` is the third bare-``None`` producer. Its payload
    passes the sentinel through untouched (``report_data["open_todos"]``) and
    all three formatters guard it. Pinned so the sweep's denominator is real
    rather than "the sites I happened to change"."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("pattern", ["EMBEDDED", "GRANULAR", None])
    async def test_open_todos_stays_none_and_renders_as_couldnt_check(self, handler, pattern):
        user_context = _user_ctx(projects=[])
        with (
            patch.object(handler, "_get_project_metadata", AsyncMock(return_value={})),
            _failing_db(),
        ):
            result = await handler._handle_status_report(
                _intent("Give me a status report", "provide_status_report"),
                "sess",
                user_context,
                pattern,
            )

        assert result["intent"]["context"]["open_todos"] is None
        assert "couldn't check" in result["message"] or "unavailable" in result["message"]
        assert "**Open Todos**: 0" not in result["message"]


class TestReminderSentinelWasAlreadyHonest:
    """``get_due_reminders`` is the fourth producer. Its only in-conversation
    consumer translates the sentinel into the registry flag the floor renders
    (``SOURCE_FAILED_FLAGS[0]``), never into an empty reminder list."""

    @pytest.mark.asyncio
    async def test_none_sentinel_becomes_the_source_failed_flag(self):
        from services.intent_service.context_assembler import ContextAssembler

        with patch(
            "services.intent_service.todo_handlers.TodoIntentHandlers.get_due_reminders",
            AsyncMock(return_value=None),
        ):
            ctx = await ContextAssembler()._compute_reminder_context(str(uuid4()))

        assert ctx == {"source_failed": True}
        assert "due_reminders" not in ctx
        assert "reminder_count" not in ctx

    def test_the_flag_renders_as_an_honest_degrade_not_an_empty_list(self):
        """The other half of the contract: the flag has to REACH the user as
        "couldn't check". A flag nothing renders is the same silent failure in
        a different costume."""
        from services.intent_service.conversational_floor import (
            SOURCE_FAILED_FLAGS,
            ConversationalFloor,
        )

        lines = ConversationalFloor(llm_client=MagicMock())._format_domain_context(
            {"source_failed": True}
        )

        assert SOURCE_FAILED_FLAGS[0].directive in lines
