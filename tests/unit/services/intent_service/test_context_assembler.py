"""
Tests for ContextAssembler (#951 + #950 iteration).

Covers:
- _compute_deadline_proximity pure helper (Phase 1 of #951)
- _gather_calendar_context wiring + failure path (Phase 3 of #951)
- pending_todos due_date / deadline_proximity surfacing (Phase 2 of #951)
- _gather_identity_context user-anchoring data (#950 iteration)
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.context_assembler import (
    ContextAssembler,
    _compute_deadline_proximity,
)


class _NoOpCache:
    """Cache stub that always misses — pre-#984 behavior for legacy tests."""

    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()

    async def get(self, key):
        return None

    async def set(self, key, value, ttl_seconds):
        return False

    async def invalidate(self, key):
        return False

    async def invalidate_prefix(self, prefix):
        return 0


@pytest.fixture(autouse=True)
def _patch_context_cache(monkeypatch):
    """#984: default ContextAssembler tests run with a no-op cache so they
    exercise compute paths directly, identical to pre-cache behavior. Cache-
    specific behavior is verified in dedicated tests that pass their own cache.
    """
    monkeypatch.setattr(
        "services.intent_service.context_assembler.ContextCache",
        lambda *args, **kwargs: _NoOpCache(),
    )


# #1156 test-drift: deterministic "now" for the time-of-day-sensitive "due_today"
# assertions. `_compute_deadline_proximity` reads a naive module-level
# `datetime.now()`, so a "due today at 23:59" fixture flips to "overdue" when the
# suite runs after 23:59 (the flake observed 2026-06-06 23:25). `_FrozenNoon`
# freezes NAIVE now() to a fixed midday but delegates tz-aware now(tz) to the real
# clock, so the gatherer's tz-aware calls (e.g. _current_time_in_configured_tz)
# are unaffected. Removes the wall-clock dependence entirely.
_FIXED_NOON = datetime(2026, 1, 15, 12, 0, 0)


class _FrozenNoon(datetime):
    @classmethod
    def now(cls, tz=None):
        return _FIXED_NOON if tz is None else datetime.now(tz)


def _freeze_noon():
    return patch("services.intent_service.context_assembler.datetime", _FrozenNoon)


# -------------------------------------------------------------------
# Phase 1: _compute_deadline_proximity helper
# -------------------------------------------------------------------


class TestComputeDeadlineProximity:
    """Pure function; covers all 5 buckets + None + edge cases."""

    def test_none_returns_none_bucket(self):
        assert _compute_deadline_proximity(None) == "none"

    def test_past_due_date_returns_overdue(self):
        past = datetime.now() - timedelta(hours=1)
        assert _compute_deadline_proximity(past) == "overdue"

    def test_past_days_returns_overdue(self):
        past = datetime.now() - timedelta(days=5)
        assert _compute_deadline_proximity(past) == "overdue"

    def test_today_returns_due_today(self):
        # Due later today (but not right now). #1156: freeze now to noon so a
        # same-day 23:59 due-time is deterministically "due_today" (was flaky
        # when the suite ran after 23:59).
        today = _FIXED_NOON.replace(hour=23, minute=59, second=0, microsecond=0)
        with _freeze_noon():
            assert _compute_deadline_proximity(today) == "due_today"

    def test_exactly_now_is_due_today(self):
        # Boundary: due_date == now should be "due_today" (not overdue).
        # #1156: freeze now so the +500us boundary can't cross midnight.
        with _freeze_noon():
            now = _FIXED_NOON + timedelta(microseconds=500)
            assert _compute_deadline_proximity(now) == "due_today"

    def test_tomorrow_returns_due_this_week(self):
        tomorrow = datetime.now() + timedelta(days=1)
        assert _compute_deadline_proximity(tomorrow) == "due_this_week"

    def test_in_six_days_returns_due_this_week(self):
        in_six = datetime.now() + timedelta(days=6)
        assert _compute_deadline_proximity(in_six) == "due_this_week"

    def test_in_eight_days_returns_later(self):
        in_eight = datetime.now() + timedelta(days=8)
        assert _compute_deadline_proximity(in_eight) == "later"

    def test_in_one_month_returns_later(self):
        in_month = datetime.now() + timedelta(days=30)
        assert _compute_deadline_proximity(in_month) == "later"


# -------------------------------------------------------------------
# Phase 3: _gather_calendar_context — calendar wiring
# -------------------------------------------------------------------


class TestGatherCalendarContext:
    """Calendar assembly via CalendarIntegrationRouter."""

    @pytest.mark.asyncio
    async def test_calendar_available_returns_mapped_fields(self):
        """When router returns a temporal summary, assembler maps to formatter schema."""
        summary = {
            "next_meeting": {"title": "CXO 1:1", "start": "2026-04-16T14:00:00"},
            "free_blocks": [
                {"start": "2026-04-16T15:00:00", "duration_minutes": 90},
            ],
            "time_available_minutes": 30,
        }
        mock_router = MagicMock()
        mock_router.get_temporal_summary = AsyncMock(return_value=summary)

        assembler = ContextAssembler()
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=mock_router,
        ):
            result = await assembler._gather_calendar_context(user_id="test-user")

        assert "calendar" in result
        cal = result["calendar"]
        assert cal["next_meeting"]["title"] == "CXO 1:1"
        assert cal["next_meeting"]["start"] == "2026-04-16T14:00:00"
        assert cal["next_free_block"]["start"] == "2026-04-16T15:00:00"
        assert cal["next_free_block"]["duration_minutes"] == 90
        assert cal["time_available_minutes"] == 30

    @pytest.mark.asyncio
    async def test_calendar_unavailable_returns_empty(self):
        """When router raises, assembler returns empty dict — no exception, no calendar key."""
        mock_router = MagicMock()
        mock_router.get_temporal_summary = AsyncMock(
            side_effect=RuntimeError("No calendar integration available")
        )

        assembler = ContextAssembler()
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=mock_router,
        ):
            result = await assembler._gather_calendar_context(user_id="test-user")

        assert result == {}
        assert "calendar" not in result

    @pytest.mark.asyncio
    async def test_calendar_no_user_id_returns_empty(self):
        """Without user_id, can't do timezone-aware calendar query — skip gracefully."""
        assembler = ContextAssembler()
        result = await assembler._gather_calendar_context(user_id=None)
        assert result == {}

    @pytest.mark.asyncio
    async def test_calendar_partial_summary_handled(self):
        """If router returns summary without free_blocks, time_available_minutes absent."""
        summary = {
            "next_meeting": {"title": "Standup", "start": "2026-04-16T09:00:00"},
            "free_blocks": [],
            "time_available_minutes": None,
        }
        mock_router = MagicMock()
        mock_router.get_temporal_summary = AsyncMock(return_value=summary)

        assembler = ContextAssembler()
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=mock_router,
        ):
            result = await assembler._gather_calendar_context(user_id="test-user")

        assert "calendar" in result
        assert result["calendar"]["next_meeting"]["title"] == "Standup"
        assert "next_free_block" not in result["calendar"]  # empty list → no field


# -------------------------------------------------------------------
# Phase 2: pending_todos due_date / deadline_proximity surfacing
# -------------------------------------------------------------------


class TestPendingTodosDeadlineSurfacing:
    """pending_todos entries should include due_date and deadline_proximity."""

    @pytest.mark.asyncio
    async def test_temporal_gatherer_surfaces_due_date(self):
        """_gather_temporal_context pending_todos include due_date + deadline_proximity."""
        # #1156: build fixtures from a fixed noon (paired with _freeze_noon below)
        # so "due today at 23:00" is deterministically "due_today", not "overdue"
        # when the suite runs late at night.
        due_today = _FIXED_NOON.replace(hour=23, minute=0, second=0, microsecond=0)
        due_next_week = _FIXED_NOON + timedelta(days=10)

        mock_todos = [
            _make_mock_todo(text="M2c gameplan review", due_date=due_today, priority="high"),
            _make_mock_todo(text="Archive old logs", due_date=due_next_week, priority="low"),
            _make_mock_todo(text="No deadline task", due_date=None, priority="medium"),
        ]

        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(return_value=mock_todos)

        from uuid import uuid4

        user_id = str(uuid4())
        assembler = ContextAssembler()

        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            # Also patch the projects / session / history bits to avoid DB calls
            with patch("services.database.session_factory.AsyncSessionFactory"):
                with patch("services.intent_service.conversation_context.get_or_create_context"):
                    # Skip calendar for this test (Phase 2 focus)
                    with patch.object(
                        assembler, "_gather_calendar_context", AsyncMock(return_value={})
                    ):
                        # #1156: freeze now → proximity computes against fixed noon.
                        with _freeze_noon():
                            result = await assembler._gather_temporal_context(
                                user_id=user_id, session_id="s1"
                            )

        assert "pending_todos" in result
        todos = result["pending_todos"]
        assert len(todos) == 3

        # First todo: due_today
        assert todos[0]["text"] == "M2c gameplan review"
        assert todos[0]["deadline_proximity"] == "due_today"
        assert todos[0]["due_date"] is not None
        # ISO-format string expected
        assert "T" in todos[0]["due_date"] or ":" in todos[0]["due_date"]

        # Second todo: due_this_week or later
        assert todos[1]["deadline_proximity"] in ("due_this_week", "later")

        # Third todo: no deadline
        assert todos[2]["deadline_proximity"] == "none"
        assert todos[2]["due_date"] is None


# -------------------------------------------------------------------
# #950 iteration: _gather_identity_context user-anchoring
# -------------------------------------------------------------------


class TestIdentityContextUserAnchoring:
    """Identity context should include user-anchoring data, not just capabilities."""

    @pytest.mark.asyncio
    async def test_identity_context_includes_user_projects_when_available(self):
        """When user_context_service returns projects, they appear in identity context."""
        mock_user_ctx = MagicMock()
        mock_user_ctx.projects = ["piper-morgan", "klatch"]
        mock_user_ctx.priorities = None
        mock_user_ctx.organization = None

        assembler = ContextAssembler()
        # Short-circuit the workflow dispatcher / plugin registry paths to keep
        # the test focused on user-anchoring
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            with patch("services.plugins.get_plugin_registry") as mock_registry:
                mock_registry.return_value.get_status_all.return_value = {}
                with patch("services.user_context_service.user_context_service") as mock_svc:
                    mock_svc.get_user_context = AsyncMock(return_value=mock_user_ctx)
                    result = await assembler._gather_identity_context(
                        user_id="test-user", session_id="s1"
                    )

        assert "user_projects" in result, f"Expected user_projects in {list(result.keys())}"
        assert result["user_projects"] == ["piper-morgan", "klatch"]


class TestUserContextPrioritiesShape:
    """#496: _compute_user_context must emit priorities in the DICT shape the floor
    formatter reads (p.get('user_priorities')), not a bare list — else configured
    PIPER.md priorities never render in the PRIORITY floor (and would AttributeError)."""

    @pytest.mark.asyncio
    async def test_priorities_emitted_as_dict_with_user_priorities(self):
        mock_user_ctx = MagicMock()
        mock_user_ctx.projects = None
        mock_user_ctx.organization = None
        mock_user_ctx.priorities = ["ship Phase 4", "review the PRs", "unblock #1124"]

        assembler = ContextAssembler()
        with patch("services.user_context_service.user_context_service") as mock_svc:
            mock_svc.get_user_context = AsyncMock(return_value=mock_user_ctx)
            result = await assembler._compute_user_context("test-user")

        assert result is not None
        assert isinstance(result["priorities"], dict)
        assert result["priorities"] == {
            "user_priorities": ["ship Phase 4", "review the PRs", "unblock #1124"]
        }

    def test_floor_renders_user_priorities_from_dict_shape(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context(
            {"priorities": {"user_priorities": ["ship Phase 4", "review the PRs"]}}
        )
        assert "User's stated priorities: ship Phase 4, review the PRs" in out

    @pytest.mark.asyncio
    async def test_identity_context_includes_recent_topics_when_available(self):
        """When conversation_context has recent turns, topics appear in identity context."""
        from services.intent_service.context_assembler import ContextAssembler

        mock_turn1 = MagicMock()
        mock_turn1.message = "I'm working on the floor prompt"
        mock_turn2 = MagicMock()
        mock_turn2.message = "Let's improve the canonical retest"

        mock_conv_ctx = MagicMock()
        mock_conv_ctx.turns = [mock_turn1, mock_turn2]

        assembler = ContextAssembler()
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            with patch("services.plugins.get_plugin_registry") as mock_registry:
                mock_registry.return_value.get_status_all.return_value = {}
                with patch(
                    "services.intent_service.conversation_context.get_or_create_context",
                    return_value=mock_conv_ctx,
                ):
                    result = await assembler._gather_identity_context(
                        user_id="test-user", session_id="s1"
                    )

        assert "recent_topics" in result, f"Expected recent_topics in {list(result.keys())}"
        assert len(result["recent_topics"]) == 2
        assert "floor prompt" in result["recent_topics"][0]

    @pytest.mark.asyncio
    async def test_identity_context_no_user_id_skips_anchoring(self):
        """Without user_id, user-anchoring fields are absent (no exception)."""
        assembler = ContextAssembler()
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            with patch("services.plugins.get_plugin_registry") as mock_registry:
                mock_registry.return_value.get_status_all.return_value = {}
                result = await assembler._gather_identity_context(user_id=None, session_id=None)

        # Capabilities + integrations still there; user-anchoring absent
        assert "capabilities" in result
        assert "user_projects" not in result
        assert "recent_topics" not in result

    @pytest.mark.asyncio
    async def test_identity_context_user_service_failure_is_graceful(self):
        """user_context_service raising doesn't break identity context assembly."""
        assembler = ContextAssembler()
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            with patch("services.plugins.get_plugin_registry") as mock_registry:
                mock_registry.return_value.get_status_all.return_value = {}
                with patch("services.user_context_service.user_context_service") as mock_svc:
                    mock_svc.get_user_context = AsyncMock(side_effect=RuntimeError("db down"))
                    # Should not raise
                    result = await assembler._gather_identity_context(
                        user_id="test-user", session_id="s1"
                    )

        # Capabilities still gathered; user-anchoring absent (not fabricated)
        assert "capabilities" in result
        assert "user_projects" not in result


# -------------------------------------------------------------------
# Issue #1057: UNKNOWN-fallback + context_contract_empty_data warning
#
# Backfills coverage for the f2408df6 commit (#960/#961 context contract).
# Architect's soundness review 2026-05-04 flagged that commit as item 4 of
# 5 cleanup items (no-tests on a contract path). This block adds the 4
# tests called out in the issue body:
#   1. UNKNOWN with user_id → falls through to status_priority context
#   2. UNKNOWN without user_id → returns empty cleanly (no exception)
#   3. TEMPORAL/STATUS/PRIORITY with no data → emits warning
#   4. TEMPORAL/STATUS/PRIORITY with data → does NOT emit warning
# -------------------------------------------------------------------


class TestUnknownCategoryFallback:
    """#1057 / #960: UNKNOWN routes through status_priority gatherer."""

    @pytest.mark.asyncio
    async def test_unknown_with_user_id_falls_through_to_status_priority(self):
        """UNKNOWN category + user_id → context populated with status_priority data."""
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_status_priority_context",
            new=AsyncMock(
                return_value={
                    "pending_todos": [{"text": "ship the thing"}],
                    "completed_todos": [],
                    "projects": ["alpha"],
                    "priorities": [],
                }
            ),
        ) as mock_gather:
            result = await assembler.gather_context(
                intent_category="UNKNOWN",
                user_id="test-user",
                session_id="s1",
            )
            mock_gather.assert_called_once_with("test-user")
            assert "pending_todos" in result
            assert result["pending_todos"] == [{"text": "ship the thing"}]
            assert "projects" in result
            assert result["projects"] == ["alpha"]

    @pytest.mark.asyncio
    async def test_unknown_without_user_id_returns_minimal_context(self):
        """UNKNOWN + user_id=None → no fallback gather, returns only current_time."""
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_status_priority_context",
            new=AsyncMock(),
        ) as mock_gather:
            result = await assembler.gather_context(
                intent_category="UNKNOWN",
                user_id=None,
                session_id="s1",
            )
            mock_gather.assert_not_called()
            # current_time is always set; nothing else for a userless UNKNOWN
            assert "current_time" in result
            assert "pending_todos" not in result
            assert "projects" not in result


class TestContextContractEmptyDataWarning:
    """#1057 / #960: empty-data warning for TEMPORAL/STATUS/PRIORITY.

    structlog doesn't route through stdlib logging cleanly in this codebase,
    so we patch the module-level `logger.warning` directly to capture calls.
    """

    @pytest.mark.asyncio
    async def test_empty_data_warning_emitted_when_no_keys(self):
        """STATUS reaches floor with no data keys → context_contract_empty_data fires."""
        from services.intent_service import context_assembler as ca_module

        assembler = ContextAssembler()
        with (
            patch.object(
                assembler,
                "_gather_status_priority_context",
                new=AsyncMock(return_value={}),  # gather returns empty
            ),
            patch.object(ca_module.logger, "warning") as mock_warn,
        ):
            await assembler.gather_context(
                intent_category="STATUS",
                user_id="test-user",
                session_id="s1",
            )
        # First positional arg of structlog .warning() is the event name
        events = [call.args[0] for call in mock_warn.call_args_list if call.args]
        assert (
            "context_contract_empty_data" in events
        ), f"Expected context_contract_empty_data warning; got: {events}"

    @pytest.mark.asyncio
    async def test_empty_data_warning_NOT_emitted_when_data_present(self):
        """STATUS reaches floor WITH data keys → no warning."""
        from services.intent_service import context_assembler as ca_module

        assembler = ContextAssembler()
        with (
            patch.object(
                assembler,
                "_gather_status_priority_context",
                new=AsyncMock(
                    return_value={
                        "pending_todos": [{"text": "x"}],
                        "projects": ["alpha"],
                    }
                ),
            ),
            patch.object(ca_module.logger, "warning") as mock_warn,
        ):
            await assembler.gather_context(
                intent_category="STATUS",
                user_id="test-user",
                session_id="s1",
            )
        events = [call.args[0] for call in mock_warn.call_args_list if call.args]
        assert (
            "context_contract_empty_data" not in events
        ), f"Did not expect empty-data warning; got: {events}"


# -------------------------------------------------------------------
# #984: Cache integration tests
# -------------------------------------------------------------------


class _StatefulCache:
    """In-memory cache that mimics ContextCache for integration testing.

    Exposes hit_count and compute_count so tests can assert that the second
    call hits the cache instead of recomputing.
    """

    def __init__(self):
        self.store = {}
        self.compute_count = 0
        self.invalidate_calls = []

    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        if key in self.store:
            return self.store[key]
        self.compute_count += 1
        value = await compute_fn()
        if value is not None:
            self.store[key] = value
        return value

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ttl_seconds):
        self.store[key] = value
        return True

    async def invalidate(self, key):
        self.invalidate_calls.append(("key", key))
        return self.store.pop(key, None) is not None

    async def invalidate_prefix(self, prefix):
        self.invalidate_calls.append(("prefix", prefix))
        matched = [k for k in self.store if k.startswith(prefix)]
        for k in matched:
            del self.store[k]
        return len(matched)


class TestContextAssemblerCaching:
    """Assert that wrapped gather methods consult cache and skip compute on hit."""

    @pytest.mark.asyncio
    async def test_calendar_second_call_hits_cache(self):
        cache = _StatefulCache()
        assembler = ContextAssembler(cache=cache)

        summary = {
            "next_meeting": {"title": "Standup", "start": "2026-05-12T10:00:00"},
            "free_blocks": [],
            "time_available_minutes": 0,
        }
        mock_router = MagicMock()
        mock_router.get_temporal_summary = AsyncMock(return_value=summary)

        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=mock_router,
        ):
            r1 = await assembler._gather_calendar_context(
                user_id="00000000-0000-0000-0000-000000000001"
            )
            r2 = await assembler._gather_calendar_context(
                user_id="00000000-0000-0000-0000-000000000001"
            )

        assert r1 == r2
        assert cache.compute_count == 1, "second call must be served from cache"
        # router invoked exactly once
        assert mock_router.get_temporal_summary.await_count == 1

    @pytest.mark.asyncio
    async def test_pending_todos_second_call_hits_cache(self):
        cache = _StatefulCache()
        assembler = ContextAssembler(cache=cache)

        mock_todos = [_make_mock_todo(f"task {i}") for i in range(3)]
        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(return_value=mock_todos)

        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            r1 = await assembler._get_pending_todos_cached(
                user_id="00000000-0000-0000-0000-000000000001", limit=10
            )
            r2 = await assembler._get_pending_todos_cached(
                user_id="00000000-0000-0000-0000-000000000001", limit=10
            )

        assert r1 == r2
        assert cache.compute_count == 1
        assert mock_svc.list_todos.await_count == 1, "list_todos must run once"

    @pytest.mark.asyncio
    async def test_pending_todos_different_limits_share_cache(self):
        """Cache stores up-to-10; callers slice on read. Different limits
        must NOT cause a second compute."""
        cache = _StatefulCache()
        assembler = ContextAssembler(cache=cache)

        mock_todos = [_make_mock_todo(f"task {i}") for i in range(8)]
        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(return_value=mock_todos)

        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            r_temporal = await assembler._get_pending_todos_cached(
                user_id="00000000-0000-0000-0000-000000000001", limit=10
            )
            r_status = await assembler._get_pending_todos_cached(
                user_id="00000000-0000-0000-0000-000000000001", limit=5
            )

        assert len(r_temporal["pending_todos"]) == 8  # all stored
        assert len(r_status["pending_todos"]) == 5  # sliced
        assert cache.compute_count == 1, "second call must reuse cached superset"

    @pytest.mark.asyncio
    async def test_trust_context_second_call_hits_cache(self):
        cache = _StatefulCache()
        assembler = ContextAssembler(cache=cache)

        from unittest.mock import patch as _patch

        # Force the compute path to take the "no profile loaded" branch
        # which is deterministic without DB.
        with _patch("services.database.session_factory.AsyncSessionFactory") as mock_factory:
            mock_session = AsyncMock()
            mock_factory.session_scope.return_value.__aenter__.return_value = mock_session
            mock_session.execute = AsyncMock()

            with _patch(
                "services.repositories.user_trust_profile_repository.UserTrustProfileRepository"
            ) as mock_repo_cls:
                mock_repo = MagicMock()
                mock_repo.get_by_user_id = AsyncMock(return_value=None)
                mock_repo_cls.return_value = mock_repo

                r1 = await assembler._gather_trust_context(
                    user_id="00000000-0000-0000-0000-000000000001"
                )
                r2 = await assembler._gather_trust_context(
                    user_id="00000000-0000-0000-0000-000000000001"
                )

        assert r1 == r2
        # compute fires once; second call hits the cache
        assert cache.compute_count == 1


# -------------------------------------------------------------------
# #983: Blocked-items gatherer tests
# -------------------------------------------------------------------


class TestGatherBlockedItemsContext:
    """Covers the _gather_blocked_items_context / _compute_blocked_items path."""

    def _make_github_router(self, issues):
        """Build a mock GitHubIntegrationRouter that yields `issues`."""
        router = MagicMock()
        router.initialize = AsyncMock()
        router.get_open_issues = AsyncMock(return_value=issues)
        return router

    @pytest.mark.asyncio
    async def test_no_user_id_returns_empty(self):
        assembler = ContextAssembler()
        result = await assembler._gather_blocked_items_context(user_id=None)
        assert result == {}

    @pytest.mark.asyncio
    async def test_no_open_issues_returns_empty(self):
        assembler = ContextAssembler()
        router = self._make_github_router(issues=[])
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_blocked_items_context(user_id="u1")
        assert result == {}

    @pytest.mark.asyncio
    async def test_no_blocked_label_returns_empty(self):
        assembler = ContextAssembler()
        issues = [
            {"number": 1, "title": "feat", "labels": ["enhancement"], "updated_at": "2026-05-12"},
            {"number": 2, "title": "bug", "labels": ["bug"], "updated_at": "2026-05-11"},
        ]
        router = self._make_github_router(issues=issues)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_blocked_items_context(user_id="u1")
        assert result == {}

    @pytest.mark.asyncio
    async def test_blocked_items_surface_with_canonical_label(self):
        assembler = ContextAssembler()
        issues = [
            {
                "number": 100,
                "title": "Blocked: needs PM disposition",
                "labels": ["status: blocked", "priority: high"],
                "updated_at": "2026-05-12T09:00:00Z",
                "uri": "https://github.com/x/y/issues/100",
            },
            {"number": 1, "title": "feat", "labels": ["enhancement"], "updated_at": "2026-05-11"},
            {
                "number": 50,
                "title": "Blocked: waiting on integration",
                "labels": ["status: blocked"],
                "updated_at": "2026-05-10T08:00:00Z",
                "uri": "https://github.com/x/y/issues/50",
            },
        ]
        router = self._make_github_router(issues=issues)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_blocked_items_context(user_id="u1")

        assert "blocked_items" in result
        assert result["blocked_count"] == 2
        # Sorted by updated_at desc — #100 (2026-05-12) before #50 (2026-05-10)
        assert result["blocked_items"][0]["number"] == 100
        assert result["blocked_items"][1]["number"] == 50
        # Non-blocked issue (#1) excluded
        assert all(b["number"] != 1 for b in result["blocked_items"])

    @pytest.mark.asyncio
    async def test_blocked_items_capped_at_10(self):
        assembler = ContextAssembler()
        issues = [
            {
                "number": i,
                "title": f"blocked {i}",
                "labels": ["status: blocked"],
                "updated_at": f"2026-05-{12 - (i % 12):02d}T00:00:00Z",
                "uri": f"https://github.com/x/y/issues/{i}",
            }
            for i in range(1, 20)  # 19 blocked items
        ]
        router = self._make_github_router(issues=issues)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_blocked_items_context(user_id="u1")

        assert len(result["blocked_items"]) == 10
        assert result["blocked_count"] == 19

    @pytest.mark.asyncio
    async def test_github_api_failure_returns_empty_no_exception(self):
        assembler = ContextAssembler()
        router = MagicMock()
        router.initialize = AsyncMock()
        router.get_open_issues = AsyncMock(side_effect=Exception("GitHub down"))
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_blocked_items_context(user_id="u1")
        assert result == {}

    @pytest.mark.asyncio
    async def test_blocked_items_second_call_hits_cache(self):
        """Cache-integration: only one router-init + API call across two reads."""
        cache = _StatefulCache()
        assembler = ContextAssembler(cache=cache)
        issues = [
            {
                "number": 100,
                "title": "blocked",
                "labels": ["status: blocked"],
                "updated_at": "2026-05-12",
                "uri": "https://github.com/x/y/issues/100",
            }
        ]
        router = self._make_github_router(issues=issues)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            r1 = await assembler._gather_blocked_items_context(user_id="u1")
            r2 = await assembler._gather_blocked_items_context(user_id="u1")

        assert r1 == r2
        assert cache.compute_count == 1
        assert router.get_open_issues.await_count == 1


# -------------------------------------------------------------------
# #985: Active-milestones gatherer tests
# -------------------------------------------------------------------


class TestGatherActiveMilestonesContext:
    """Covers _gather_active_milestones_context / _compute_active_milestones."""

    def _make_github_router(self, milestones):
        router = MagicMock()
        router.initialize = AsyncMock()
        router.list_milestones_via_mcp = AsyncMock(return_value=milestones)
        return router

    @pytest.mark.asyncio
    async def test_no_user_id_returns_empty(self):
        assembler = ContextAssembler()
        result = await assembler._gather_active_milestones_context(user_id=None)
        assert result == {}

    @pytest.mark.asyncio
    async def test_no_milestones_returns_empty(self):
        assembler = ContextAssembler()
        router = self._make_github_router(milestones=[])
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_active_milestones_context(user_id="u1")
        assert result == {}

    @pytest.mark.asyncio
    async def test_milestones_sorted_by_due_on_asc(self):
        assembler = ContextAssembler()
        milestones = [
            {
                "title": "Post-MVP",
                "number": 8,
                "due_on": "2026-10-30T00:00:00Z",
                "open_issues": 6,
                "closed_issues": 0,
                "html_url": "https://github.com/x/y/milestone/8",
            },
            {
                "title": "MVP",
                "number": 5,
                "due_on": "2026-05-27T00:00:00Z",
                "open_issues": 75,
                "closed_issues": 680,
                "html_url": "https://github.com/x/y/milestone/5",
            },
            {
                "title": "Fast Follow",
                "number": 7,
                "due_on": "2026-07-31T00:00:00Z",
                "open_issues": 35,
                "closed_issues": 2,
                "html_url": "https://github.com/x/y/milestone/7",
            },
        ]
        router = self._make_github_router(milestones=milestones)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_active_milestones_context(user_id="u1")

        titles = [m["title"] for m in result["active_milestones"]]
        assert titles == ["MVP", "Fast Follow", "Post-MVP"]
        assert result["active_milestone_count"] == 3

    @pytest.mark.asyncio
    async def test_milestones_without_due_on_sort_to_end(self):
        assembler = ContextAssembler()
        milestones = [
            {
                "title": "No-Date",
                "number": 99,
                "due_on": None,
                "open_issues": 1,
                "closed_issues": 0,
            },
            {
                "title": "MVP",
                "number": 5,
                "due_on": "2026-05-27T00:00:00Z",
                "open_issues": 75,
                "closed_issues": 680,
            },
        ]
        router = self._make_github_router(milestones=milestones)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_active_milestones_context(user_id="u1")
        titles = [m["title"] for m in result["active_milestones"]]
        assert titles == ["MVP", "No-Date"]

    @pytest.mark.asyncio
    async def test_milestones_capped_at_5(self):
        assembler = ContextAssembler()
        milestones = [
            {
                "title": f"M{i}",
                "number": i,
                "due_on": f"2026-0{i}-01T00:00:00Z",
                "open_issues": 0,
                "closed_issues": 0,
            }
            for i in range(1, 9)  # 8 milestones
        ]
        router = self._make_github_router(milestones=milestones)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_active_milestones_context(user_id="u1")
        assert len(result["active_milestones"]) == 5
        assert result["active_milestone_count"] == 8

    @pytest.mark.asyncio
    async def test_github_api_failure_returns_empty_no_exception(self):
        assembler = ContextAssembler()
        router = MagicMock()
        router.initialize = AsyncMock()
        router.list_milestones_via_mcp = AsyncMock(side_effect=Exception("GitHub down"))
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_active_milestones_context(user_id="u1")
        assert result == {}

    @pytest.mark.asyncio
    async def test_milestones_second_call_hits_cache(self):
        cache = _StatefulCache()
        assembler = ContextAssembler(cache=cache)
        milestones = [
            {
                "title": "MVP",
                "number": 5,
                "due_on": "2026-05-27T00:00:00Z",
                "open_issues": 75,
                "closed_issues": 680,
                "html_url": "https://github.com/x/y/milestone/5",
            }
        ]
        router = self._make_github_router(milestones=milestones)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            r1 = await assembler._gather_active_milestones_context(user_id="u1")
            r2 = await assembler._gather_active_milestones_context(user_id="u1")

        assert r1 == r2
        assert cache.compute_count == 1
        assert router.list_milestones_via_mcp.await_count == 1


# -------------------------------------------------------------------
# #986: Recent-activity gatherer tests
# -------------------------------------------------------------------


class TestGatherRecentActivityContext:
    """Covers _gather_recent_activity_context / _compute_recent_activity."""

    def _make_github_router(self, items):
        """Mock GitHubIntegrationRouter exposing the MCP adapter path."""
        router = MagicMock()
        router.initialize = AsyncMock()
        router._resolve_default_repo = AsyncMock(
            return_value=("mediajunkie", "piper-morgan-product")
        )
        adapter = MagicMock()
        adapter.list_github_issues_direct = AsyncMock(return_value=items)
        router.mcp_adapter = adapter
        return router

    @staticmethod
    def _iso(days_ago):
        """Build a UTC ISO timestamp `days_ago` days ago."""
        from datetime import datetime, timedelta, timezone

        dt = datetime.now(timezone.utc) - timedelta(days=days_ago)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    @pytest.mark.asyncio
    async def test_no_user_id_returns_empty(self):
        assembler = ContextAssembler()
        result = await assembler._gather_recent_activity_context(user_id=None)
        assert result == {}

    @pytest.mark.asyncio
    async def test_no_items_returns_empty(self):
        assembler = ContextAssembler()
        router = self._make_github_router(items=[])
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        assert result == {}

    @pytest.mark.asyncio
    async def test_window_filter_excludes_old_items(self):
        assembler = ContextAssembler()
        items = [
            {
                "number": 100,
                "title": "fresh",
                "state": "open",
                "updated_at": self._iso(1),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/100",
            },
            {
                "number": 200,
                "title": "ancient",
                "state": "closed",
                "updated_at": self._iso(30),  # outside 7d window
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/200",
            },
        ]
        router = self._make_github_router(items=items)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        numbers = [a["number"] for a in result["recent_activity"]]
        assert numbers == [100]
        assert result["recent_activity_count"] == 1

    @pytest.mark.asyncio
    async def test_pr_vs_issue_distinction(self):
        assembler = ContextAssembler()
        items = [
            {
                "number": 50,
                "title": "the PR",
                "state": "open",
                "updated_at": self._iso(2),
                "is_pull_request": True,
                "uri": "https://github.com/x/y/pull/50",
            },
            {
                "number": 51,
                "title": "the issue",
                "state": "open",
                "updated_at": self._iso(3),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/51",
            },
        ]
        router = self._make_github_router(items=items)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        types = {a["number"]: a["type"] for a in result["recent_activity"]}
        assert types[50] == "pr"
        assert types[51] == "issue"

    @pytest.mark.asyncio
    async def test_sorted_desc_and_capped_at_10(self):
        assembler = ContextAssembler()
        items = [
            {
                "number": i,
                "title": f"item-{i}",
                "state": "open",
                "updated_at": self._iso(i % 7),  # all within window
                "is_pull_request": False,
                "uri": f"https://github.com/x/y/issues/{i}",
            }
            for i in range(1, 16)  # 15 items
        ]
        router = self._make_github_router(items=items)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        assert len(result["recent_activity"]) == 10
        assert result["recent_activity_count"] == 15
        # Newest first
        updated = [a["updated_at"] for a in result["recent_activity"]]
        assert updated == sorted(updated, reverse=True)

    @pytest.mark.asyncio
    async def test_unresolved_repo_returns_empty(self):
        assembler = ContextAssembler()
        router = MagicMock()
        router.initialize = AsyncMock()
        router._resolve_default_repo = AsyncMock(return_value=None)
        router.mcp_adapter = MagicMock()
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        assert result == {}

    @pytest.mark.asyncio
    async def test_github_api_failure_returns_empty_no_exception(self):
        assembler = ContextAssembler()
        router = MagicMock()
        router.initialize = AsyncMock()
        router._resolve_default_repo = AsyncMock(return_value=("o", "r"))
        adapter = MagicMock()
        adapter.list_github_issues_direct = AsyncMock(side_effect=Exception("GitHub down"))
        router.mcp_adapter = adapter
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        assert result == {}

    @pytest.mark.asyncio
    async def test_recent_activity_second_call_hits_cache(self):
        cache = _StatefulCache()
        assembler = ContextAssembler(cache=cache)
        items = [
            {
                "number": 100,
                "title": "x",
                "state": "open",
                "updated_at": self._iso(1),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/100",
            }
        ]
        router = self._make_github_router(items=items)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            r1 = await assembler._gather_recent_activity_context(user_id="u1")
            r2 = await assembler._gather_recent_activity_context(user_id="u1")
        assert r1 == r2
        assert cache.compute_count == 1
        assert router.mcp_adapter.list_github_issues_direct.await_count == 1

    # ===== Issue #1085 slice 1: schema unification (source field) =====

    @pytest.mark.asyncio
    async def test_each_item_carries_source_github_field(self):
        """Issue #1085 slice 1: every recent_activity item has source='github'
        for GitHub-emitted items. Unblocks multi-source aggregation (slice 2
        adds 'slack'; #1086 adds 'calendar')."""
        assembler = ContextAssembler()
        items = [
            {
                "number": 1,
                "title": "issue alpha",
                "state": "open",
                "updated_at": self._iso(1),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/1",
            },
            {
                "number": 2,
                "title": "pr beta",
                "state": "open",
                "updated_at": self._iso(2),
                "is_pull_request": True,
                "uri": "https://github.com/x/y/pull/2",
            },
        ]
        router = self._make_github_router(items=items)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        assert "recent_activity" in result
        for activity_item in result["recent_activity"]:
            assert activity_item.get("source") == "github", (
                f"#1085 slice 1 contract: each item must carry source='github'; "
                f"got {activity_item!r}"
            )

    @pytest.mark.asyncio
    async def test_source_field_does_not_break_existing_item_shape(self):
        """Slice 1 is backward-compatible: existing fields
        (number/title/state/type/updated_at/url) still present."""
        assembler = ContextAssembler()
        items = [
            {
                "number": 42,
                "title": "test issue",
                "state": "closed",
                "updated_at": self._iso(1),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/42",
            }
        ]
        router = self._make_github_router(items=items)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        item = result["recent_activity"][0]
        # All pre-slice-1 fields must remain
        assert item["number"] == 42
        assert item["title"] == "test issue"
        assert item["state"] == "closed"
        assert item["type"] == "issue"
        assert item["url"] == "https://github.com/x/y/issues/42"
        # The new source field is additive
        assert item["source"] == "github"

    # ===== Issue #1086: calendar source =====

    @staticmethod
    def _make_calendar_router(events):
        """Mock CalendarIntegrationRouter returning events from get_events_in_range."""
        router = MagicMock()
        router.get_events_in_range = AsyncMock(return_value=events)
        return router

    @staticmethod
    def _calendar_event(
        start_days_ago,
        *,
        title="Standup",
        duration_minutes=30,
        attendees=3,
        status="confirmed",
        is_all_day=False,
    ):
        """Build a calendar event dict matching google_calendar_adapter shape."""
        from datetime import datetime, timedelta, timezone

        start = datetime.now(timezone.utc) - timedelta(days=start_days_ago)
        end = start + timedelta(minutes=duration_minutes)
        return {
            "title": title,
            "summary": title,
            "start_time": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_time": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": status,
            "location": "",
            "description": "",
            "attendees": attendees,
            "is_all_day": is_all_day,
            "duration_minutes": duration_minutes,
        }

    @pytest.mark.asyncio
    async def test_calendar_source_items_carry_source_field(self):
        """Calendar items have source='calendar' + the calendar-specific fields."""
        assembler = ContextAssembler()
        events = [self._calendar_event(2, title="Sprint Demo")]
        github_router = self._make_github_router(items=[])
        cal_router = self._make_calendar_router(events=events)
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        assert "recent_activity" in result
        cal_items = [i for i in result["recent_activity"] if i.get("source") == "calendar"]
        assert len(cal_items) == 1
        item = cal_items[0]
        assert item["source"] == "calendar"
        assert item["title"] == "Sprint Demo"
        # Calendar-specific fields present
        assert "duration_minutes" in item
        assert "attendees" in item
        assert "start_time" in item

    @pytest.mark.asyncio
    async def test_all_day_calendar_events_excluded(self):
        """All-day events are excluded — focused on meetings."""
        assembler = ContextAssembler()
        events = [
            self._calendar_event(1, title="Holiday", is_all_day=True),
            self._calendar_event(2, title="Standup", is_all_day=False),
        ]
        github_router = self._make_github_router(items=[])
        cal_router = self._make_calendar_router(events=events)
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        cal_titles = [
            i["title"] for i in result["recent_activity"] if i.get("source") == "calendar"
        ]
        assert "Holiday" not in cal_titles
        assert "Standup" in cal_titles

    @pytest.mark.asyncio
    async def test_calendar_events_outside_window_excluded(self):
        """Calendar events outside _RECENT_ACTIVITY_WINDOW_DAYS are excluded."""
        assembler = ContextAssembler()
        events = [
            self._calendar_event(3, title="Recent"),  # 3 days ago → in 7d window
            self._calendar_event(30, title="Ancient"),  # 30 days ago → out
        ]
        github_router = self._make_github_router(items=[])
        cal_router = self._make_calendar_router(events=events)
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        cal_titles = [
            i["title"] for i in result["recent_activity"] if i.get("source") == "calendar"
        ]
        assert "Recent" in cal_titles
        assert "Ancient" not in cal_titles

    @pytest.mark.asyncio
    async def test_calendar_failure_does_not_break_github(self):
        """Per-source fail-graceful: calendar API down → GitHub still returned."""
        assembler = ContextAssembler()
        github_items = [
            {
                "number": 1,
                "title": "issue",
                "state": "open",
                "updated_at": self._iso(1),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/1",
            }
        ]
        github_router = self._make_github_router(items=github_items)
        # Calendar router that raises on get_events_in_range
        bad_cal_router = MagicMock()
        bad_cal_router.get_events_in_range = AsyncMock(side_effect=Exception("calendar API down"))
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=bad_cal_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        # GitHub items still returned despite calendar failure
        github_items_returned = [
            i for i in result["recent_activity"] if i.get("source") == "github"
        ]
        assert len(github_items_returned) == 1

    @pytest.mark.asyncio
    async def test_github_failure_does_not_break_calendar(self):
        """Per-source fail-graceful: GitHub API down → calendar still returned."""
        assembler = ContextAssembler()
        bad_github_router = MagicMock()
        bad_github_router.initialize = AsyncMock(side_effect=Exception("github down"))
        events = [self._calendar_event(1, title="Sync")]
        cal_router = self._make_calendar_router(events=events)
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=bad_github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        # Calendar item still returned despite GitHub failure
        cal_items = [i for i in result["recent_activity"] if i.get("source") == "calendar"]
        assert len(cal_items) == 1
        assert cal_items[0]["title"] == "Sync"

    @pytest.mark.asyncio
    async def test_cross_source_sort_by_updated_at_desc(self):
        """Items from both sources are interleaved by updated_at descending."""
        assembler = ContextAssembler()
        github_items = [
            {
                "number": 1,
                "title": "old gh",
                "state": "closed",
                "updated_at": self._iso(5),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/1",
            },
            {
                "number": 2,
                "title": "new gh",
                "state": "open",
                "updated_at": self._iso(1),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/2",
            },
        ]
        events = [
            self._calendar_event(3, title="middle cal"),  # between old gh and new gh
        ]
        github_router = self._make_github_router(items=github_items)
        cal_router = self._make_calendar_router(events=events)
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        # Order should be: new gh (1d) → middle cal (3d) → old gh (5d)
        titles_in_order = [i.get("title") for i in result["recent_activity"]]
        assert titles_in_order == ["new gh", "middle cal", "old gh"]

    @pytest.mark.asyncio
    async def test_both_sources_empty_returns_empty(self):
        """No GitHub items + no calendar events → caller sees no recent_activity."""
        assembler = ContextAssembler()
        github_router = self._make_github_router(items=[])
        cal_router = self._make_calendar_router(events=[])
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        assert result == {}

    # ===== Issue #1085 slice 2: Slack source =====

    @staticmethod
    def _slack_response(success=True, data=None):
        """Build a mock SlackResponse-like object."""
        resp = MagicMock()
        resp.success = success
        resp.data = data or {}
        return resp

    @staticmethod
    def _make_slack_router(channels, messages_per_channel):
        """Mock SlackIntegrationRouter for DM list + history.

        channels: list of channel dicts (id, is_mpim, ...)
        messages_per_channel: dict of channel_id → list of message dicts
        """
        router = MagicMock()
        list_data = {"channels": channels}
        router.list_im_channels = AsyncMock(
            return_value=TestGatherRecentActivityContext._slack_response(
                success=True, data=list_data
            )
        )

        async def _history(channel, limit=20, oldest=None, **kwargs):
            msgs = messages_per_channel.get(channel, [])
            return TestGatherRecentActivityContext._slack_response(
                success=True, data={"messages": msgs}
            )

        router.get_conversation_history = AsyncMock(side_effect=_history)
        return router

    @staticmethod
    def _slack_message(days_ago, *, user="U_OTHER", text="hello"):
        """Build a Slack message dict with `ts` `days_ago` ago."""
        from datetime import datetime, timedelta, timezone

        ts = (datetime.now(timezone.utc) - timedelta(days=days_ago)).timestamp()
        return {"ts": f"{ts:.6f}", "user": user, "text": text, "type": "message"}

    @pytest.mark.asyncio
    async def test_slack_dm_items_carry_source_field(self):
        """Slack DM items have source='slack' + channel + ts."""
        assembler = ContextAssembler()
        github_router = self._make_github_router(items=[])
        cal_router = self._make_calendar_router(events=[])
        slack_router = self._make_slack_router(
            channels=[{"id": "D123", "is_mpim": False}],
            messages_per_channel={"D123": [self._slack_message(1, text="hey there")]},
        )
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=slack_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        slack_items = [i for i in result["recent_activity"] if i.get("source") == "slack"]
        assert len(slack_items) == 1
        item = slack_items[0]
        assert item["source"] == "slack"
        assert item["channel"] == "D123"
        assert item["channel_type"] == "im"
        assert "ts" in item
        # title is a preview of the message text
        assert "hey there" in item["title"]

    @pytest.mark.asyncio
    async def test_slack_mpim_distinct_channel_type(self):
        """Multi-party DMs get channel_type='mpim'."""
        assembler = ContextAssembler()
        github_router = self._make_github_router(items=[])
        cal_router = self._make_calendar_router(events=[])
        slack_router = self._make_slack_router(
            channels=[{"id": "G456", "is_mpim": True}],
            messages_per_channel={"G456": [self._slack_message(1, text="group msg")]},
        )
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=slack_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        slack_items = [i for i in result["recent_activity"] if i.get("source") == "slack"]
        assert len(slack_items) == 1
        assert slack_items[0]["channel_type"] == "mpim"

    @pytest.mark.asyncio
    async def test_slack_failure_does_not_break_other_sources(self):
        """Slack down → GitHub + calendar still returned."""
        assembler = ContextAssembler()
        github_items = [
            {
                "number": 1,
                "title": "gh issue",
                "state": "open",
                "updated_at": self._iso(1),
                "is_pull_request": False,
                "uri": "https://github.com/x/y/issues/1",
            }
        ]
        github_router = self._make_github_router(items=github_items)
        cal_router = self._make_calendar_router(events=[self._calendar_event(2)])
        # Slack router raises on list
        bad_slack = MagicMock()
        bad_slack.list_im_channels = AsyncMock(side_effect=Exception("slack down"))
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=bad_slack,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        sources = {i.get("source") for i in result["recent_activity"]}
        assert "github" in sources
        assert "calendar" in sources
        assert "slack" not in sources  # gracefully absent

    @pytest.mark.asyncio
    async def test_slack_list_failure_returns_empty(self):
        """list_im_channels returning success=False → helper returns []."""
        assembler = ContextAssembler()
        github_router = self._make_github_router(items=[])
        cal_router = self._make_calendar_router(events=[])
        bad_list_slack = MagicMock()
        bad_list_slack.list_im_channels = AsyncMock(
            return_value=self._slack_response(success=False, data={})
        )
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=bad_list_slack,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        # No sources had data → empty result
        assert result == {}

    @pytest.mark.asyncio
    async def test_slack_per_channel_failure_continues(self):
        """If one channel's history fails, others still aggregate."""
        assembler = ContextAssembler()
        github_router = self._make_github_router(items=[])
        cal_router = self._make_calendar_router(events=[])

        slack_router = MagicMock()
        slack_router.list_im_channels = AsyncMock(
            return_value=self._slack_response(
                success=True,
                data={
                    "channels": [
                        {"id": "D_BAD", "is_mpim": False},
                        {"id": "D_GOOD", "is_mpim": False},
                    ]
                },
            )
        )

        async def _history(channel, limit=20, oldest=None, **kwargs):
            if channel == "D_BAD":
                raise Exception("channel fetch failed")
            return self._slack_response(
                success=True,
                data={"messages": [self._slack_message(1, text="hi from good")]},
            )

        slack_router.get_conversation_history = AsyncMock(side_effect=_history)

        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=github_router,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=cal_router,
            ),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=slack_router,
            ),
        ):
            result = await assembler._gather_recent_activity_context(user_id="u1")
        slack_items = [i for i in result["recent_activity"] if i.get("source") == "slack"]
        # The good channel's message comes through despite the bad channel failing
        assert len(slack_items) == 1
        assert slack_items[0]["channel"] == "D_GOOD"


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------


def _make_mock_todo(text, due_date=None, priority="medium", completed=False):
    """Construct a mock Todo-like object for tests."""
    t = MagicMock()
    t.text = text
    t.due_date = due_date
    t.priority = priority
    t.completed = completed
    t.completed_at = None
    return t


# -------------------------------------------------------------------
# #1085 slice 3 — Slack mentions-of-user aggregator
# (#1338: migrated off direct-aiohttp onto SlackIntegrationRouter; the
#  former _make_aiohttp_{response,session}_mock helpers were removed as
#  dead code once these tests stopped mocking aiohttp.)
# -------------------------------------------------------------------


class TestFetchSlackMentionsItems:
    """Cover `_fetch_slack_mentions_items` — the #1085 slice 3 path that hits
    Slack `search.messages` via the user token.

    #1338: migrated off direct-aiohttp onto `SlackIntegrationRouter` — these tests
    now mock the router's `test_auth(use_user_token=True)` + `search_messages()`
    rather than `aiohttp.ClientSession`. The conversion-logic coverage (time-window
    filter, missing-ts skip, item shape, fail-graceful) is preserved.
    """

    @staticmethod
    def _patched_router(*, auth, search=None):
        """A mock SlackIntegrationRouter; auth/search are mock SlackResponses."""
        router = MagicMock()
        router.test_auth = AsyncMock(return_value=auth)
        router.search_messages = AsyncMock(return_value=search)
        return patch(
            "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
            return_value=router,
        ), router

    @pytest.mark.asyncio
    async def test_returns_empty_when_no_user_token(self):
        """No user token → the router's user-token auth honest-degrades → [] silently."""
        # honest-degrade: test_auth(use_user_token=True) returns success=False
        router_patch, router = self._patched_router(
            auth=MagicMock(success=False, data={})
        )
        assembler = ContextAssembler()
        with router_patch, patch(
            "services.integrations.slack.config_service.SlackConfigService"
        ):
            result = await assembler._fetch_slack_mentions_items(user_id="u1")

        assert result == []
        router.search_messages.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_returns_empty_when_auth_test_not_ok(self):
        """If auth.test fails, skip the search call entirely."""
        router_patch, router = self._patched_router(
            auth=MagicMock(success=False, data={})
        )
        assembler = ContextAssembler()
        with router_patch, patch(
            "services.integrations.slack.config_service.SlackConfigService"
        ):
            result = await assembler._fetch_slack_mentions_items(user_id="u1")

        assert result == []
        router.search_messages.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_returns_items_from_search_messages_response(self):
        """Happy path: search.messages returns matches → items list with correct shape."""
        recent_ts = (datetime.now() - timedelta(days=1)).timestamp()
        router_patch, _ = self._patched_router(
            auth=MagicMock(success=True, data={"user": "alice"}),
            search=MagicMock(
                success=True,
                data={
                    "messages": {
                        "matches": [
                            {
                                "ts": f"{recent_ts:.6f}",
                                "text": "Hey @alice, can you look at this?",
                                "user": "U2BOB",
                                "channel": {"id": "C123", "name": "general"},
                                "permalink": "https://example.slack.com/archives/C123/p1",
                            }
                        ]
                    }
                },
            ),
        )
        assembler = ContextAssembler()
        with router_patch, patch(
            "services.integrations.slack.config_service.SlackConfigService"
        ):
            result = await assembler._fetch_slack_mentions_items(user_id="u1")

        assert len(result) == 1
        item = result[0]
        assert item["source"] == "slack"
        assert item["channel_type"] == "mention"
        assert item["channel"] == "C123"
        assert item["user"] == "U2BOB"
        assert item["title"].startswith("Hey @alice")
        assert item["permalink"] == "https://example.slack.com/archives/C123/p1"
        assert item["ts"] == f"{recent_ts:.6f}"

    @pytest.mark.asyncio
    async def test_filters_messages_outside_time_window(self):
        """Mentions older than the recent-activity window are dropped."""
        recent_ts = (datetime.now() - timedelta(days=1)).timestamp()
        old_ts = (datetime.now() - timedelta(days=60)).timestamp()
        router_patch, _ = self._patched_router(
            auth=MagicMock(success=True, data={"user": "alice"}),
            search=MagicMock(
                success=True,
                data={
                    "messages": {
                        "matches": [
                            {
                                "ts": f"{recent_ts:.6f}",
                                "text": "recent ping",
                                "user": "U1",
                                "channel": {"id": "C123"},
                            },
                            {
                                "ts": f"{old_ts:.6f}",
                                "text": "ancient ping",
                                "user": "U2",
                                "channel": {"id": "C456"},
                            },
                        ]
                    }
                },
            ),
        )
        assembler = ContextAssembler()
        with router_patch, patch(
            "services.integrations.slack.config_service.SlackConfigService"
        ):
            result = await assembler._fetch_slack_mentions_items(user_id="u1")

        assert len(result) == 1
        assert result[0]["title"] == "recent ping"

    @pytest.mark.asyncio
    async def test_fail_graceful_on_exception(self):
        """Any exception during the flow returns [] rather than propagating."""
        router_patch, router = self._patched_router(auth=MagicMock(success=True, data={}))
        router.test_auth = AsyncMock(side_effect=RuntimeError("boom"))
        assembler = ContextAssembler()
        with router_patch, patch(
            "services.integrations.slack.config_service.SlackConfigService"
        ):
            result = await assembler._fetch_slack_mentions_items(user_id="u1")

        assert result == []

    @pytest.mark.asyncio
    async def test_missing_ts_in_match_is_skipped(self):
        """Match entries lacking a `ts` field are skipped without error."""
        recent_ts = (datetime.now() - timedelta(days=1)).timestamp()
        router_patch, _ = self._patched_router(
            auth=MagicMock(success=True, data={"user": "alice"}),
            search=MagicMock(
                success=True,
                data={
                    "messages": {
                        "matches": [
                            {"text": "no-ts-here", "user": "U1", "channel": {"id": "C1"}},
                            {
                                "ts": f"{recent_ts:.6f}",
                                "text": "valid-ping",
                                "user": "U2",
                                "channel": {"id": "C2"},
                            },
                        ]
                    }
                },
            ),
        )
        assembler = ContextAssembler()
        with router_patch, patch(
            "services.integrations.slack.config_service.SlackConfigService"
        ):
            result = await assembler._fetch_slack_mentions_items(user_id="u1")

        assert len(result) == 1
        assert result[0]["title"] == "valid-ping"
