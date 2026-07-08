"""
Tests for Issue #1030 INSIGHT-PULL context_assembler enrichment.

When intent is (MEMORY, "pull_insights"), the ContextAssembler must:
- Fetch insights via InsightRepository.list_for_user
- Bucket by confidence per PM R5 (high ≥ 0.75, medium 0.50-0.75, low < 0.50)
- Surface empty-state explicitly (is_empty=True)
- Fail-graceful (no exceptions reach the caller)

Plus the floor's _format_domain_context renders the insights section.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import ConversationalFloor


class _NoOpCache:
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
    monkeypatch.setattr(
        "services.intent_service.context_assembler.ContextCache",
        lambda *args, **kwargs: _NoOpCache(),
    )


def _mk_insight(expression, confidence, observation_count=1, topic_tags=None):
    """Construct a mock SurfaceableInsight matching the REAL nested shape the
    assembler reads (#1156 / #1144 test-discipline).

    SurfaceableInsight nests its content under `learning: ExtractedLearning` —
    the assembler reads `ins.learning.confidence`, `ins.learning.topic_tags`,
    `ins.learning.insight.expression`, plus `ins.surfaced_count` / `ins.id` /
    `ins.created_at`. The prior mock set these top-level, so the assembler read
    auto-MagicMocks (float(MagicMock) → 1.0) and bucketed everything high.
    """
    m = MagicMock()
    m.id = f"ins-{abs(hash(expression)) % 10000}"
    m.surfaced_count = observation_count
    m.created_at = datetime(2026, 5, 30, 14, 0, 0)
    # Real nested location (ExtractedLearning):
    m.learning.confidence = confidence
    m.learning.topic_tags = topic_tags or []
    m.learning.insight.expression = expression
    return m


class TestInsightPullEnrichment:
    """Verify _gather_insight_pull_context fetches + buckets correctly."""

    @pytest.mark.asyncio
    async def test_pull_insights_no_user_id_returns_empty_dict(self):
        """When user_id is missing, return empty insights structure (not None)."""
        assembler = ContextAssembler()
        ctx = await assembler._gather_insight_pull_context(user_id=None)
        assert "insights" in ctx
        assert ctx["insights"]["is_empty"] is True
        assert ctx["insights"]["total_count"] == 0
        assert ctx["insights"]["high_confidence"] == []
        assert ctx["insights"]["medium_confidence"] == []
        assert ctx["insights"]["low_confidence"] == []

    @pytest.mark.asyncio
    async def test_pull_insights_buckets_by_pm_r5_confidence_cuts(self):
        """Insights bucket per PM R5: high ≥ 0.75, medium 0.50-0.75, low < 0.50."""
        insights = [
            _mk_insight("user prefers async work", 0.85, observation_count=5),
            _mk_insight("user codes in mornings", 0.78, observation_count=3),
            _mk_insight("user might prefer Notion", 0.60, observation_count=2),
            _mk_insight("user mentioned coffee once", 0.50),  # exactly 0.50 → medium
            _mk_insight("user might be on EST", 0.40),
            _mk_insight("vague pattern", 0.20),
        ]
        # Mock repo + session
        mock_repo = AsyncMock()
        mock_repo.list_for_user.return_value = insights
        mock_session_factory = MagicMock()
        # session_scope is an async context manager
        mock_session_factory.session_scope.return_value.__aenter__ = AsyncMock(
            return_value=MagicMock()
        )
        mock_session_factory.session_scope.return_value.__aexit__ = AsyncMock(return_value=None)

        with (
            patch(
                "services.database.repositories.InsightRepository",
                return_value=mock_repo,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory",
                mock_session_factory,
            ),
        ):
            assembler = ContextAssembler()
            ctx = await assembler._gather_insight_pull_context(user_id="u-test")

        assert ctx["insights"]["is_empty"] is False
        assert ctx["insights"]["total_count"] == 6
        # high: 0.85, 0.78
        assert len(ctx["insights"]["high_confidence"]) == 2
        # medium: 0.60, 0.50
        assert len(ctx["insights"]["medium_confidence"]) == 2
        # low: 0.40, 0.20
        assert len(ctx["insights"]["low_confidence"]) == 2

    @pytest.mark.asyncio
    async def test_pull_insights_filters_internal_seed_tags(self):
        """#1216: internal/seed-provenance tags (dev_seed, seed_demo_object, uat-*)
        must NOT surface to the floor — they let the LLM announce an ungroundable
        'seed placeholders vs real observations' claim (the workstyle
        confabulation). Legit TOPICAL tags must still pass through."""
        insights = [
            _mk_insight(
                "batches github triage",
                0.64,
                observation_count=2,
                topic_tags=["workflow", "github", "uat-anniversary-2026-05-28"],
            ),
            _mk_insight(
                "completed a full lifecycle",
                0.80,
                topic_tags=["dev_seed", "seed_demo_object"],
            ),
        ]
        mock_repo = AsyncMock()
        mock_repo.list_for_user.return_value = insights
        mock_session_factory = MagicMock()
        mock_session_factory.session_scope.return_value.__aenter__ = AsyncMock(
            return_value=MagicMock()
        )
        mock_session_factory.session_scope.return_value.__aexit__ = AsyncMock(return_value=None)

        with (
            patch(
                "services.database.repositories.InsightRepository",
                return_value=mock_repo,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory",
                mock_session_factory,
            ),
        ):
            assembler = ContextAssembler()
            ctx = await assembler._gather_insight_pull_context(user_id="u-test")

        all_tags = []
        for band in ("high_confidence", "medium_confidence", "low_confidence"):
            for ins in ctx["insights"][band]:
                all_tags.extend(ins["topic_tags"])
        # Seed-provenance tags filtered out:
        assert "uat-anniversary-2026-05-28" not in all_tags
        assert "dev_seed" not in all_tags
        assert "seed_demo_object" not in all_tags
        # Legit topical tags preserved:
        assert "workflow" in all_tags
        assert "github" in all_tags

    @pytest.mark.asyncio
    async def test_pull_insights_empty_repo_signals_empty_state(self):
        """When user has no insights, is_empty=True so floor responds honestly."""
        mock_repo = AsyncMock()
        mock_repo.list_for_user.return_value = []
        mock_session_factory = MagicMock()
        mock_session_factory.session_scope.return_value.__aenter__ = AsyncMock(
            return_value=MagicMock()
        )
        mock_session_factory.session_scope.return_value.__aexit__ = AsyncMock(return_value=None)

        with (
            patch(
                "services.database.repositories.InsightRepository",
                return_value=mock_repo,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory",
                mock_session_factory,
            ),
        ):
            assembler = ContextAssembler()
            ctx = await assembler._gather_insight_pull_context(user_id="u-test")

        assert ctx["insights"]["is_empty"] is True
        assert ctx["insights"]["total_count"] == 0

    @pytest.mark.asyncio
    async def test_pull_insights_db_error_returns_empty_not_raises(self):
        """DB exception → empty insights dict (fail-graceful)."""
        mock_session_factory = MagicMock()
        mock_session_factory.session_scope.side_effect = RuntimeError("simulated DB failure")

        with patch(
            "services.database.session_factory.AsyncSessionFactory",
            mock_session_factory,
        ):
            assembler = ContextAssembler()
            ctx = await assembler._gather_insight_pull_context(user_id="u-test")

        assert ctx["insights"]["is_empty"] is True
        assert ctx["insights"]["total_count"] == 0

    @pytest.mark.asyncio
    async def test_gather_context_routes_pull_insights_via_action(self):
        """gather_context with (MEMORY, pull_insights) must call the new gatherer,
        not the legacy _gather_memory_context."""
        assembler = ContextAssembler()
        with (
            patch.object(
                assembler,
                "_gather_insight_pull_context",
                AsyncMock(return_value={"insights": {"is_empty": True, "total_count": 0}}),
            ) as mock_insight,
            patch.object(
                assembler,
                "_gather_memory_context",
                AsyncMock(return_value={"conversation_history_summary": {}}),
            ) as mock_memory,
        ):
            ctx = await assembler.gather_context(
                intent_category="MEMORY",
                user_id="u-test",
                session_id="s-test",
                intent_action="pull_insights",
            )
            mock_insight.assert_called_once()
            mock_memory.assert_not_called()
            assert "insights" in ctx

    @pytest.mark.asyncio
    async def test_gather_context_get_memory_still_uses_legacy_gatherer(self):
        """Regression: (MEMORY, get_memory) must still route to _gather_memory_context."""
        assembler = ContextAssembler()
        with (
            patch.object(
                assembler,
                "_gather_insight_pull_context",
                AsyncMock(return_value={"insights": {}}),
            ) as mock_insight,
            patch.object(
                assembler,
                "_gather_memory_context",
                AsyncMock(return_value={"conversation_history_summary": {}}),
            ) as mock_memory,
        ):
            await assembler.gather_context(
                intent_category="MEMORY",
                user_id="u-test",
                session_id="s-test",
                intent_action="get_memory",
            )
            mock_memory.assert_called_once()
            mock_insight.assert_not_called()


class TestFloorFormatsInsights:
    """Verify ConversationalFloor._format_domain_context renders insights."""

    def _floor(self):
        """Construct a Floor with whatever the constructor needs (stub LLM)."""
        return ConversationalFloor(llm_client=MagicMock())

    def test_format_renders_high_medium_low_sections(self):
        domain_context = {
            "current_time": "10:00 AM",
            "insights": {
                "high_confidence": [
                    {
                        "id": "1",
                        "expression": "User prefers async work",
                        "confidence": 0.85,
                        "topic_tags": ["work_style"],
                        "observation_count": 7,
                    }
                ],
                "medium_confidence": [
                    {
                        "id": "2",
                        "expression": "User might prefer Notion",
                        "confidence": 0.60,
                        "topic_tags": ["tools"],
                        "observation_count": 3,
                    }
                ],
                "low_confidence": [
                    {
                        "id": "3",
                        "expression": "Vague timing pattern",
                        "confidence": 0.30,
                        "topic_tags": [],
                        "observation_count": 1,
                    }
                ],
                "total_count": 3,
                "is_empty": False,
            },
        }
        out = self._floor()._format_domain_context(domain_context)
        assert "HIGH CONFIDENCE" in out
        assert "MEDIUM CONFIDENCE" in out
        assert "LOW CONFIDENCE" in out
        assert "User prefers async work" in out
        assert "User might prefer Notion" in out
        assert "Vague timing pattern" in out
        # Citation + correction-invitation guidance present
        assert "Invite correction" in out or "anything sounds off" in out

    def test_format_renders_empty_state_honestly(self):
        domain_context = {
            "current_time": "10:00 AM",
            "insights": {
                "high_confidence": [],
                "medium_confidence": [],
                "low_confidence": [],
                "total_count": 0,
                "is_empty": True,
            },
        }
        out = self._floor()._format_domain_context(domain_context)
        # Empty state should explicitly tell the floor LLM not to fabricate
        assert "NONE YET" in out or "not yet learned" in out
        assert "Do not fabricate" in out

    def test_format_skips_insights_section_if_not_present(self):
        """Regression: if insights key absent (non-pull queries), no insight section."""
        domain_context = {"current_time": "10:00 AM"}
        out = self._floor()._format_domain_context(domain_context)
        assert "HIGH CONFIDENCE" not in out
        assert "Composted insights" not in out

    def test_format_includes_provenance_honesty_guard_1216(self):
        """#1216 interim: insights carry no seed-vs-real provenance, so the
        instruction block must forbid the LLM from asserting that distinction
        (the UAT bug: two 100%-seeded insights presented as 'real' while others
        were characterized as 'seed placeholders' — pure confabulation, since
        InsightDB has no is_seed/source field)."""
        domain_context = {
            "insights": {
                "high_confidence": [
                    {
                        "id": "1",
                        "expression": "batch GitHub issue triage",
                        "confidence": 0.85,
                        "topic_tags": [],
                        "observation_count": 2,
                    }
                ],
                "medium_confidence": [],
                "low_confidence": [],
                "total_count": 1,
                "is_empty": False,
            },
        }
        out = self._floor()._format_domain_context(domain_context)
        assert "PROVENANCE" in out
        assert "CANNOT tell where these insights came from" in out
        assert "NEVER characterize" in out
        # The guard rides WITH the data — absent insights, absent guard.
        out_no_insights = self._floor()._format_domain_context({"current_time": "10:00 AM"})
        assert "PROVENANCE" not in out_no_insights
