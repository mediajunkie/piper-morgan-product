"""
Tests for Issue #901: Intent classifier keyword disambiguation.

5 queries were misrouted due to keyword collisions in the pre-classifier.
These tests verify the fixes:
- Q27: "Tell me more about the GitHub integration" → query (not identity)
- Q33: "Find time for a 1:1 with the team lead" → query (not temporal)
- Q40: "Update the project roadmap document" → query (not portfolio)
- Q43: "What's blocking the milestone?" → analysis (not status)
- Q62: "Check my calendar for conflicts" → query (not temporal)
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)


class TestKeywordDisambiguationQ27:
    """Q27: Feature/integration info queries → QUERY, not IDENTITY."""

    def test_github_integration_routes_to_query(self):
        result = PreClassifier.pre_classify("Tell me more about the GitHub integration")
        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "get_feature_info"

    def test_slack_integration_routes_to_query(self):
        result = PreClassifier.pre_classify("Tell me about the Slack integration")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_calendar_feature_routes_to_query(self):
        result = PreClassifier.pre_classify("Tell me more about the calendar integration")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_notion_integration_routes_to_query(self):
        result = PreClassifier.pre_classify("Tell me about Notion")
        assert result is not None
        assert result.category == IntentCategory.QUERY

    def test_tell_me_about_yourself_still_identity(self):
        """Regression: 'Tell me about yourself' must stay IDENTITY."""
        result = PreClassifier.pre_classify("Tell me about yourself")
        assert result is not None
        assert result.category == IntentCategory.IDENTITY

    def test_who_are_you_still_identity(self):
        """Regression: Standard identity queries unchanged."""
        result = PreClassifier.pre_classify("Who are you?")
        assert result is not None
        assert result.category == IntentCategory.IDENTITY


class TestKeywordDisambiguationQ33:
    """Q33: Scheduling/availability queries — ORIGINALLY routed to QUERY
    (calendar), not TEMPORAL (issue #901). SUPERSEDED 2026-10-01 by #1595
    Phase 3's third deletion: CXO ruled "find time for X" / "schedule a
    meeting" / "book a slot" capability-gap asks (no scheduling/booking
    feature exists) should honestly floor rather than claim a fabricated
    QUERY op (scripts/inversion_phase3_deleted_patterns.json's
    CALENDAR_QUERY_PATTERNS entry — these exact phrases' row shapes are
    ruled `floor`). CALENDAR_QUERY_PATTERNS is deleted, so surface 1 no
    longer claims any of these — the #901 QUERY-routing fix these tests
    pinned is intentionally walked back by the floor ruling, not broken.
    """

    def test_find_time_for_1on1_routes_to_query(self):
        result = PreClassifier.pre_classify("Find time for a 1:1 with the team lead")
        assert result is None, (
            "CALENDAR_QUERY_PATTERNS is deleted and this is a CXO-ruled floor "
            f"ask — surface 1 should no longer claim it (got {result!r})"
        )

    def test_schedule_meeting_routes_to_query(self):
        result = PreClassifier.pre_classify("Schedule a 1:1 with Sarah")
        assert result is None, (
            "CALENDAR_QUERY_PATTERNS is deleted and this is a CXO-ruled floor "
            f"ask — surface 1 should no longer claim it (got {result!r})"
        )

    def test_book_meeting_routes_to_query(self):
        result = PreClassifier.pre_classify("Book a time for our sync")
        assert result is None, (
            "CALENDAR_QUERY_PATTERNS is deleted and this is a CXO-ruled floor "
            f"ask — surface 1 should no longer claim it (got {result!r})"
        )

    @pytest.mark.asyncio
    async def test_what_time_still_temporal(self, monkeypatch):
        """Regression: Pure time queries must stay reachable.

        #1595 Phase 3 fourth deletion (2026-10-01): TEMPORAL_PATTERNS is now
        `[]` — surface 1 no longer claims this at all. Converted to the
        decline+inversion-routes idiom: surface 1 declines, and the
        Inversion (stubbed, no live LLM call) still dispatches get_current_time
        via the get_current_time_entry rail entry #1595 registered the same
        day."""
        assert PreClassifier.pre_classify("What time is it?") is None
        await assert_inversion_routes(
            monkeypatch,
            "What time is it?",
            live_categories="read_temporal",
            expected_action="get_current_time",
        )


class TestKeywordDisambiguationQ40:
    """Q40: Document update queries → QUERY, not PORTFOLIO."""

    def test_update_document_routes_to_query(self):
        result = PreClassifier.pre_classify("Update the project roadmap document")
        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "update_document_query"

    def test_archive_project_still_portfolio(self):
        """Regression: Portfolio operations unchanged."""
        result = PreClassifier.pre_classify("Archive my project")
        assert result is not None
        assert result.category == IntentCategory.PORTFOLIO


class TestKeywordDisambiguationQ43:
    """Q43: Blocker/analysis queries → ANALYSIS, not STATUS.

    #1595 Phase 3 twelfth deletion (2026-10-03, PARTIAL): ANALYSIS_PATTERNS'
    `\\bwhat'?s blocking\\b`, `\\bwhat is blocking\\b`, `\\bblockers?\\s+
    (?:for|on|in)\\b`, and `\\brisk assessment\\b` literals are gone (12 of
    16 deleted) — the four phrases below ("What's blocking the milestone?",
    "What is blocking the release?", "What are the blockers for the
    sprint?", "I need a risk assessment") are now genuinely UNCLAIMED at
    surface 1 (confirmed via claim_for_phrase, no reabsorption). Swapped to
    the 4 surviving literals' own corpus phrases — same disambiguation
    point (ANALYSIS reachable at surface 1, not misrouted to STATUS)."""

    def test_main_obstacle_routes_to_analysis(self):
        result = PreClassifier.pre_classify("what's the main obstacle here")
        assert result is not None
        assert result.category == IntentCategory.ANALYSIS
        assert result.action == "analyze_blockers"

    def test_in_the_way_routes_to_analysis(self):
        result = PreClassifier.pre_classify("what's in the way of finishing this")
        assert result is not None
        assert result.category == IntentCategory.ANALYSIS

    def test_analyze_risk_routes_to_analysis(self):
        result = PreClassifier.pre_classify("let's analyze the risk here")
        assert result is not None
        assert result.category == IntentCategory.ANALYSIS

    def test_impact_analysis_routes_to_analysis(self):
        result = PreClassifier.pre_classify("can you run an impact analysis on this change")
        assert result is not None
        assert result.category == IntentCategory.ANALYSIS

    def test_project_status_still_status(self):
        """Regression: Status queries unchanged.

        #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): STATUS_PATTERNS'
        \\bproject status\\b literal is gone (52 of 56 deleted). Swapped for
        "can you summarize my current work" (matches the surviving
        \\bcurrent work\\b literal) — same point, a STATUS-category ask."""
        result = PreClassifier.pre_classify("can you summarize my current work")
        assert result is not None
        assert result.category == IntentCategory.STATUS


class TestKeywordDisambiguationQ62:
    """Q62: Calendar conflict/check queries — ORIGINALLY routed to QUERY, not
    TEMPORAL (issue #901). SUPERSEDED 2026-10-01 by #1595 Phase 3's third
    deletion: CXO ruled calendar conflict/overlap-check asks a
    capability-gap (no conflict-check feature exists) that should honestly
    floor rather than claim a fabricated QUERY op. CALENDAR_QUERY_PATTERNS
    is deleted; surface 1 no longer claims any of these as QUERY.

    Right after the third deletion, two of the four phrases below were
    reabsorbed by TEMPORAL_PATTERNS' broader calendar vocabulary
    (DISAGREEING — claimed get_current_time), a DOCUMENTED, REPORTED finding
    (scripts/inversion_phase3_deleted_patterns.json's CALENDAR_QUERY_PATTERNS
    entry, known_reabsorptions). Resolved by the FOURTH deletion, same day:
    TEMPORAL_PATTERNS is now ALSO `[]` — all four phrases genuinely decline
    at surface 1 now (the reabsorption entry's `resolved_by` field records
    this).
    """

    def test_check_calendar_conflicts_routes_to_query(self):
        result = PreClassifier.pre_classify("Check my calendar for conflicts")
        assert result is None, (
            "both CALENDAR_QUERY_PATTERNS and TEMPORAL_PATTERNS are deleted — "
            f"surface 1 should no longer claim this CXO-ruled floor ask (got {result!r})"
        )

    def test_calendar_conflicts_routes_to_query(self):
        result = PreClassifier.pre_classify("Any calendar conflicts this week?")
        assert result is None, (
            "CALENDAR_QUERY_PATTERNS is deleted and this is a CXO-ruled floor "
            f"ask — surface 1 should no longer claim it (got {result!r})"
        )

    def test_calendar_overlap_routes_to_query(self):
        result = PreClassifier.pre_classify("Check for calendar overlaps")
        assert result is None, (
            "CALENDAR_QUERY_PATTERNS is deleted and this is a CXO-ruled floor "
            f"ask — surface 1 should no longer claim it (got {result!r})"
        )

    @pytest.mark.asyncio
    async def test_whats_on_calendar_still_query(self, monkeypatch):
        """Was: 'Regression: Existing calendar queries unchanged.' Then (third
        deletion): CALENDAR_QUERY_PATTERNS deleted, TEMPORAL_PATTERNS
        reabsorbed this phrase disagreeing. Now (fourth deletion, same day):
        TEMPORAL_PATTERNS is ALSO `[]` — surface 1 declines entirely;
        converted to the decline+inversion-routes idiom, which proves the
        ruled destination (meeting_time) is still reachable live."""
        result = PreClassifier.pre_classify("What's on my calendar today?")
        assert result is None, "known TEMPORAL_PATTERNS reabsorption should be resolved"
        await assert_inversion_routes(
            monkeypatch,
            "What's on my calendar today?",
            live_categories="read_temporal",
            expected_action="meeting_time",
        )

    @pytest.mark.asyncio
    async def test_what_day_still_temporal(self, monkeypatch):
        """Regression: Pure temporal queries must stay reachable.

        #1595 Phase 3 fourth deletion: TEMPORAL_PATTERNS is now `[]` —
        converted to the decline+inversion-routes idiom (same reasoning as
        TestKeywordDisambiguationQ33::test_what_time_still_temporal)."""
        result = PreClassifier.pre_classify("What day is it?")
        assert result is None
        await assert_inversion_routes(
            monkeypatch,
            "What day is it?",
            live_categories="read_temporal",
            expected_action="get_current_time",
        )
