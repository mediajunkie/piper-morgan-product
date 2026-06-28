"""
#1032 MUX-INSIGHT-PUSH — gating + maybe_push tests.

Per Q7 (May 3): negative-assertion probe tests are MANDATORY CI gates —
Stage 1+2 users NEVER receive Push regardless of any other condition.
This file enforces that invariant + tests each gate independently.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from services.mux.composting_models import ExtractedLearning, Pattern
from services.mux.composting_pipeline import SurfaceableInsight
from services.mux.push_mode import (
    EXPLAIN_AFFORDANCE_TEXT,
    FramedPushPayload,
    MUTE_AFFORDANCE_TEXT,
    PushContext,
    SESSION_MUTE_PATTERNS,
    TRUST_STAGE_PUSH_MIN,
    format_push_for_chat,
    get_min_confidence,
    get_min_interval_minutes,
    get_relevance_threshold,
    get_stage_stability_hours,
    is_eligible_by_trust,
    is_relevant,
    is_right_moment,
    is_session_mute_trigger,
    maybe_push,
    score_context_relevance,
)


pytestmark_async = pytest.mark.asyncio


# =============================================================================
# Configuration defaults match Phase 0 design doc
# =============================================================================


class TestConfigDefaults:
    def test_min_confidence_default(self):
        assert get_min_confidence() == 0.75

    def test_relevance_threshold_default(self):
        assert get_relevance_threshold() == 3

    def test_min_interval_default(self):
        assert get_min_interval_minutes() == 30

    def test_stability_hours_default(self):
        assert get_stage_stability_hours() == 2

    def test_trust_stage_push_min_is_3(self):
        """Per D4 §Prerequisites: 'Trust level: Stage 3 or higher'."""
        assert TRUST_STAGE_PUSH_MIN == 3


# =============================================================================
# Trust gate (Q7 hard gate + fail-safe)
# =============================================================================


def _trust_service(stage: int):
    """Helper: build a mock trust service that returns the given stage."""
    svc = AsyncMock()
    svc.get_trust_stage = AsyncMock(return_value=stage)
    return svc


@pytest.mark.asyncio
class TestTrustGate:
    async def test_stage_1_blocked(self):
        eligible = await is_eligible_by_trust(user_id="alpha", trust_service=_trust_service(1))
        assert eligible is False

    async def test_stage_2_blocked(self):
        eligible = await is_eligible_by_trust(user_id="alpha", trust_service=_trust_service(2))
        assert eligible is False

    async def test_stage_3_stable_eligible(self):
        # No promotion timestamp = treated as stable (acceptable per design)
        eligible = await is_eligible_by_trust(user_id="alpha", trust_service=_trust_service(3))
        assert eligible is True

    async def test_stage_4_stable_eligible(self):
        eligible = await is_eligible_by_trust(user_id="alpha", trust_service=_trust_service(4))
        assert eligible is True

    async def test_stage_3_within_stability_window_blocked(self):
        now = datetime(2026, 5, 3, 12, 0, 0, tzinfo=timezone.utc)
        # promoted 1 hour ago (default stability is 2 hours)
        promoted = now - timedelta(hours=1)
        eligible = await is_eligible_by_trust(
            user_id="alpha",
            trust_service=_trust_service(3),
            stage_promoted_at=promoted,
            now=now,
        )
        assert eligible is False

    async def test_stage_3_past_stability_window_eligible(self):
        now = datetime(2026, 5, 3, 12, 0, 0, tzinfo=timezone.utc)
        promoted = now - timedelta(hours=5)
        eligible = await is_eligible_by_trust(
            user_id="alpha",
            trust_service=_trust_service(3),
            stage_promoted_at=promoted,
            now=now,
        )
        assert eligible is True

    async def test_trust_read_error_fail_safe(self):
        """Q7: trust-read errors → NO Push (fail-safe, not default-allow)."""
        svc = AsyncMock()
        svc.get_trust_stage = AsyncMock(side_effect=RuntimeError("simulated"))
        eligible = await is_eligible_by_trust(user_id="alpha", trust_service=svc)
        assert eligible is False

    async def test_naive_promotion_datetime_handled(self):
        """Stage promotion timestamps may be naive datetime in some paths."""
        now = datetime(2026, 5, 3, 12, 0, 0, tzinfo=timezone.utc)
        promoted = datetime(2026, 5, 3, 5, 0, 0)  # naive, 7 hours ago
        eligible = await is_eligible_by_trust(
            user_id="alpha",
            trust_service=_trust_service(3),
            stage_promoted_at=promoted,
            now=now,
        )
        assert eligible is True


# =============================================================================
# Right-moment + anti-spam
# =============================================================================


class TestIsRightMoment:
    def test_no_constraints_passes(self):
        ok, reason = is_right_moment(last_push_at=None)
        assert ok is True
        assert reason == "ok"

    def test_anti_spam_recent_push_blocks(self):
        now = datetime(2026, 5, 3, 12, 0, 0, tzinfo=timezone.utc)
        last = now - timedelta(minutes=10)  # 10 min ago, under default 30
        ok, reason = is_right_moment(last_push_at=last, now=now)
        assert ok is False
        assert reason == "anti_spam_cooldown"

    def test_anti_spam_past_window_passes(self):
        now = datetime(2026, 5, 3, 12, 0, 0, tzinfo=timezone.utc)
        last = now - timedelta(minutes=45)
        ok, reason = is_right_moment(last_push_at=last, now=now)
        assert ok is True

    def test_decline_state_blocks(self):
        ok, reason = is_right_moment(last_push_at=None, in_decline_state=True)
        assert ok is False
        assert reason == "in_decline_state"

    def test_onboarding_blocks(self):
        ok, reason = is_right_moment(last_push_at=None, in_onboarding=True)
        assert ok is False
        assert reason == "in_onboarding"


# =============================================================================
# Relevance scoring (Q2 Option B)
# =============================================================================


def _make_insight(*, applies_to_entities=None, topic_tags=None, context_tags=None, confidence=0.85):
    learning = ExtractedLearning(
        pattern=Pattern(description="test pattern"),
        confidence=confidence,
        applies_to_entities=applies_to_entities or [],
        topic_tags=topic_tags or [],
    )
    return SurfaceableInsight(
        object_id="obj-1",
        user_id="alpha",
        learning=learning,
        context_tags=context_tags or [],
    )


class TestScoreContextRelevance:
    def test_zero_when_no_overlap(self):
        insight = _make_insight(applies_to_entities=["x"], topic_tags=["a"])
        assert score_context_relevance(insight, ["y"], ["b"]) == 0

    def test_entity_overlap_scores_2(self):
        insight = _make_insight(applies_to_entities=["deadlines"])
        assert score_context_relevance(insight, ["deadlines"], []) == 2

    def test_topic_overlap_scores_1(self):
        insight = _make_insight(topic_tags=["work-patterns"])
        assert score_context_relevance(insight, [], ["work-patterns"]) == 1

    def test_context_tag_overlap_scores_1(self):
        insight = _make_insight(context_tags=["sprint"])
        assert score_context_relevance(insight, ["sprint"], []) == 1

    def test_combined_score(self):
        """2 entity + 2 topic + 1 context = 5"""
        insight = _make_insight(
            applies_to_entities=["e1", "e2"],
            topic_tags=["t1", "t2"],
            context_tags=["c1"],
        )
        score = score_context_relevance(insight, ["e1", "e2", "c1"], ["t1", "t2"])
        # entity overlap: 2 entities × 2 = 4
        # topic overlap: 2 topics × 1 = 2
        # context_tag overlap: c1 matches entity_set → 1
        assert score == 7

    def test_none_insight_returns_zero(self):
        assert score_context_relevance(None, ["x"], ["y"]) == 0


class TestIsRelevant:
    def test_above_threshold_true(self):
        insight = _make_insight(applies_to_entities=["a", "b"])
        # 4 from entity overlap; threshold default 3
        assert is_relevant(insight, ["a", "b"], []) is True

    def test_below_threshold_false(self):
        insight = _make_insight(topic_tags=["t"])
        # 1 from topic overlap; below threshold 3
        assert is_relevant(insight, [], ["t"]) is False


# =============================================================================
# Mute (Q4 NL trigger detection)
# =============================================================================


class TestSessionMuteTrigger:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("don't push insights", True),
            ("stop surfacing insights", True),
            ("mute insights", True),
            ("mute learnings", True),
            ("quiet the insights", True),
            ("hold off on suggestions", True),
            ("not now, hold off the insights please", True),
            # safe variants
            ("Tell me about the project", False),
            ("What time is it?", False),
            ("I learned a lot today", False),
            ("Can you mute notifications?", False),  # mute used, but not insights
            ("", False),
        ],
    )
    def test_session_mute_detection(self, text, expected):
        assert is_session_mute_trigger(text) is expected


# =============================================================================
# maybe_push integration — multi-gate orchestration
# =============================================================================


@pytest.mark.asyncio
class TestMaybePush:
    async def test_session_muted_returns_none(self):
        ctx = PushContext(user_id="alpha", session_mute_active=True)
        result = await maybe_push(ctx, journal=AsyncMock(), trust_service=_trust_service(4))
        assert result is None

    async def test_mute_trigger_in_message_returns_none(self):
        ctx = PushContext(user_id="alpha", user_message="please mute insights")
        result = await maybe_push(ctx, journal=AsyncMock(), trust_service=_trust_service(4))
        assert result is None

    async def test_decline_state_returns_none(self):
        ctx = PushContext(user_id="alpha", in_decline_state=True)
        result = await maybe_push(ctx, journal=AsyncMock(), trust_service=_trust_service(4))
        assert result is None

    async def test_anti_spam_returns_none(self):
        now = datetime(2026, 5, 3, 12, 0, 0, tzinfo=timezone.utc)
        ctx = PushContext(
            user_id="alpha",
            last_push_at=now - timedelta(minutes=10),
        )
        result = await maybe_push(
            ctx, journal=AsyncMock(), trust_service=_trust_service(4), now=now
        )
        assert result is None

    async def test_stage_1_returns_none(self):
        """Q7 hard gate: Stage 1 → no push regardless of other conditions."""
        ctx = PushContext(user_id="alpha")
        mock_journal = AsyncMock()
        mock_journal.get_unsurfaced = AsyncMock(
            return_value=[_make_insight(applies_to_entities=["x", "y", "z"])]
        )
        result = await maybe_push(ctx, journal=mock_journal, trust_service=_trust_service(1))
        assert result is None

    async def test_stage_2_returns_none(self):
        """Q7 hard gate: Stage 2 → no push regardless."""
        ctx = PushContext(user_id="alpha")
        mock_journal = AsyncMock()
        mock_journal.get_unsurfaced = AsyncMock(
            return_value=[_make_insight(applies_to_entities=["x", "y", "z"])]
        )
        result = await maybe_push(ctx, journal=mock_journal, trust_service=_trust_service(2))
        assert result is None

    async def test_no_relevant_insights_returns_none(self):
        ctx = PushContext(
            user_id="alpha",
            context_entities=["unrelated"],
            context_topics=["unrelated"],
        )
        mock_journal = AsyncMock()
        mock_journal.get_unsurfaced = AsyncMock(
            return_value=[_make_insight(applies_to_entities=["other"])]
        )
        result = await maybe_push(ctx, journal=mock_journal, trust_service=_trust_service(4))
        assert result is None

    async def test_empty_candidate_set_returns_none(self):
        ctx = PushContext(user_id="alpha", context_entities=["x"])
        mock_journal = AsyncMock()
        mock_journal.get_unsurfaced = AsyncMock(return_value=[])
        result = await maybe_push(ctx, journal=mock_journal, trust_service=_trust_service(4))
        assert result is None

    async def test_all_gates_pass_returns_payload(self):
        ctx = PushContext(
            user_id="alpha",
            context_entities=["e1", "e2"],
            context_topics=["t1"],
        )
        mock_journal = AsyncMock()
        relevant_insight = _make_insight(
            applies_to_entities=["e1", "e2"],  # 2 × 2 = 4 → above threshold
            topic_tags=["t1"],
        )
        mock_journal.get_unsurfaced = AsyncMock(return_value=[relevant_insight])
        result = await maybe_push(ctx, journal=mock_journal, trust_service=_trust_service(4))
        assert result is not None
        assert isinstance(result, FramedPushPayload)
        assert result.insight_id == relevant_insight.id

    async def test_trust_read_error_returns_none(self):
        """Fail-safe: trust-read raises → no push."""
        ctx = PushContext(user_id="alpha")
        svc = AsyncMock()
        svc.get_trust_stage = AsyncMock(side_effect=RuntimeError("boom"))
        mock_journal = AsyncMock()
        mock_journal.get_unsurfaced = AsyncMock(
            return_value=[_make_insight(applies_to_entities=["x"])]
        )
        result = await maybe_push(ctx, journal=mock_journal, trust_service=svc)
        assert result is None

    async def test_picks_highest_relevance(self):
        ctx = PushContext(
            user_id="alpha",
            context_entities=["a", "b"],
            context_topics=["t1"],
        )
        low_relevance = _make_insight(applies_to_entities=["a"])  # 2
        high_relevance = _make_insight(applies_to_entities=["a", "b"], topic_tags=["t1"])  # 5
        mock_journal = AsyncMock()
        mock_journal.get_unsurfaced = AsyncMock(return_value=[low_relevance, high_relevance])
        result = await maybe_push(ctx, journal=mock_journal, trust_service=_trust_service(4))
        assert result is not None
        assert result.insight_id == high_relevance.id


# =============================================================================
# In-chat renderer (Phase 6)
# =============================================================================


class TestFormatPushForChat:
    def test_appends_payload_to_floor_response(self):
        payload = FramedPushPayload(
            insight_id="i1",
            framed_text="Having reflected, you front-load smaller tasks.",
        )
        out = format_push_for_chat("Here's the deadline info.", payload)
        assert "Here's the deadline info." in out
        assert "front-load smaller tasks" in out
        assert MUTE_AFFORDANCE_TEXT in out
        assert EXPLAIN_AFFORDANCE_TEXT in out
        # Separator between floor response and push
        assert "---" in out


# =============================================================================
# Probe-set regression (mandatory CI gates per Q7)
# =============================================================================


PROBE_PATH = Path("tests/mux/probes/push_mode_probes.json")


@pytest.fixture(scope="module")
def probes():
    with PROBE_PATH.open() as f:
        data = json.load(f)
    return data["probes"]


def test_probe_set_has_negative_stage_assertions(probes):
    """Mandatory: Stage 1 + Stage 2 NEVER → no_push regardless of other conditions."""
    stage_1_probes = [p for p in probes if p.get("stage") == 1]
    stage_2_probes = [p for p in probes if p.get("stage") == 2]
    assert len(stage_1_probes) >= 1, "Probe set must include Stage 1 negative assertion"
    assert len(stage_2_probes) >= 1, "Probe set must include Stage 2 negative assertion"
    # Every Stage 1 + Stage 2 probe must have verdict no_push
    for p in stage_1_probes + stage_2_probes:
        assert p["verdict"] == "no_push", (
            f"Probe {p['id']} has Stage {p['stage']} but verdict {p['verdict']!r} "
            "— Q7 invariant is Stage 1+2 NEVER push"
        )


def test_probe_set_has_fail_safe_assertion(probes):
    """Mandatory: trust-read error → no_push (fail-safe)."""
    fs_probes = [p for p in probes if p.get("trust_read_raises") is True]
    assert len(fs_probes) >= 1, "Probe set must include trust-read-error fail-safe assertion"
    for p in fs_probes:
        assert p["verdict"] == "no_push"


def test_probe_set_size_meets_design_target(probes):
    """Phase 0 design: ~20 probes (Q2 disposition)."""
    assert 18 <= len(probes) <= 25
