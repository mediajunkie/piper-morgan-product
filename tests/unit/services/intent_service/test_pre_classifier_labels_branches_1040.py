"""Pre-classifier pattern tests for labels + branches (Issue #1040).

#1595 Phase 3 fifth deletion (2026-10-02): `GITHUB_QUERY_PATTERNS` is now
`[]` (tombstoned) — `_matches_patterns`/`_get_github_action` against it can
never match/branch again (see `scripts/inversion_phase3_deleted_patterns.json`
and `docs/internal/architecture/current/intent-routing-stack.md`'s "Fifth
deletion" subsection). Every phrase this file pinned as a surface-1 MATCH is
converted to pin the new reality (DECLINE at surface 1); `TestActionRegistry`
below is unaffected (the WORKFLOW actions stay registered, just unreachable
via this now-dead surface-1 branch) and `TestInversionRoutesSurvive` adds a
representative live-routes pin (stubbed router, no LLM) proving these
destinations are still reachable through the Inversion, not just vanished.
"""

from __future__ import annotations

import pytest

from services.intent_service.pre_classifier import PreClassifier
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)


class TestLabelPatterns:
    """Issue #1040 / #1595 Phase 3 fifth deletion: label-listing phrasings
    no longer match at surface 1 — GITHUB_QUERY_PATTERNS is `[]`."""

    @pytest.mark.parametrize(
        "msg",
        [
            "what labels do we use",
            "what labels",
            "show labels",
            "show me the labels",
            "show issue labels",
            "list labels",
            "list our labels",
            "issue labels",
            "labels list",
            "labels count",
            "available labels",
            "all labels",
        ],
    )
    def test_positive_match(self, msg):
        matched = PreClassifier._matches_patterns(msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS)
        assert not matched, f"unexpected match for {msg!r} — GITHUB_QUERY_PATTERNS is tombstoned"

    @pytest.mark.parametrize(
        "msg",
        [
            "label this as urgent",  # "label" as verb
            "please label the issue with bug",  # verb usage
        ],
    )
    def test_negative_no_match(self, msg):
        matched = PreClassifier._matches_patterns(msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS)
        assert not matched, f"unexpected match for {msg!r}"


class TestBranchPatterns:
    """Issue #1040 / #1595 Phase 3 fifth deletion: branch-listing phrasings
    no longer match at surface 1 — GITHUB_QUERY_PATTERNS is `[]`."""

    @pytest.mark.parametrize(
        "msg",
        [
            "active branches",
            "show branches",
            "show me the branches",
            "list branches",
            "list our branches",
            "feature branches",
            "show feature branches",
            "current branches",
            "what branches",
            "what branches are open",
        ],
    )
    def test_positive_match(self, msg):
        matched = PreClassifier._matches_patterns(msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS)
        assert not matched, f"unexpected match for {msg!r} — GITHUB_QUERY_PATTERNS is tombstoned"

    @pytest.mark.parametrize(
        "msg",
        [
            "branch out from this approach",  # "branch" as verb
            "this is a new branch of inquiry",  # different domain meaning
        ],
    )
    def test_negative_no_match(self, msg):
        matched = PreClassifier._matches_patterns(msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS)
        assert not matched, f"unexpected match for {msg!r}"


class TestNoRegressionsExistingPatterns:
    """#1595 Phase 3 fifth deletion: these GitHub query routes no longer
    match at surface 1 either — the whole list is tombstoned, not just the
    label/branch additions this class used to guard against regression."""

    @pytest.mark.parametrize(
        "msg,expected_action",
        [
            ("show issues", "list_issues_query"),
            ("list issues", "list_issues_query"),
            ("show my prs", "list_prs_query"),
            ("show stale prs", "stale_prs_query"),
            ("what shipped this week", "shipped_query"),
            ("close issue #42", "close_issue_query"),
            # #1039 sibling
            ("show milestones", "list_milestones_query"),
            ("recent releases", "list_releases_query"),
        ],
    )
    def test_existing_patterns_unchanged(self, msg, expected_action):
        matched = PreClassifier._matches_patterns(msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS)
        assert not matched, f"unexpected match for {msg!r} — GITHUB_QUERY_PATTERNS is tombstoned"


class TestInversionRoutesSurvive:
    """#1595 Phase 3 fifth deletion: a representative sample of the phrases
    above (one per destination action) still routes correctly through the
    Inversion's live consult (stubbed router — no LLM call, ever), proving
    the destinations above didn't just vanish when surface 1 stopped
    claiming them."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "phrase,action",
        [
            ("show labels", "list_labels_query"),
            ("show branches", "list_branches_query"),
        ],
    )
    async def test_routes_live(self, monkeypatch, phrase, action):
        await assert_inversion_routes(
            monkeypatch,
            phrase,
            live_categories="read_status",
            expected_action=action,
        )


class TestActionRegistry:
    """New actions registered for #1040."""

    def test_labels_action_registered(self):
        from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition

        assert ("QUERY", "list_labels_query") in ACTION_REGISTRY
        assert ACTION_REGISTRY[("QUERY", "list_labels_query")] == ActionDisposition.WORKFLOW

    def test_branches_action_registered(self):
        from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition

        assert ("QUERY", "list_branches_query") in ACTION_REGISTRY
        assert ACTION_REGISTRY[("QUERY", "list_branches_query")] == ActionDisposition.WORKFLOW


# #1768 (2026-09-12): the TestLensInference class (ACTION_TO_LENS coverage for
# the new actions) was deleted with services/intent_service/lens_inference.py —
# the lens table's only consumer was zero-caller classify_conscious.
