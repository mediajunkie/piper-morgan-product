"""Regression tests for #1084 — GitHub-specific QUERY subsumes STATUS.

"What's the next milestone?" matched BOTH the milestone-specific
GITHUB_QUERY_PATTERNS (→ QUERY/list_milestones_query) AND STATUS_PATTERNS
(milestone phrasings live there too, likely from #1068 tuning). The
resulting multi-intent went to IntentOrchestrator → CanonicalHandlers,
which only routes TEMPORAL/GUIDANCE/PORTFOLIO/CONVERSATION; both QUERY
and STATUS failed with "No handler for category" and the user got the
"I'm having trouble processing..." fallback.

The subsumption rule (this issue's fix) drops STATUS when a GitHub-
specific QUERY action is also present. The single-intent QUERY then
routes through intent_service._handle_query_intent which has a working
_handle_list_milestones_query path.

These tests verify the collapse happens for Q25 + sibling phrasings,
and that pure-STATUS / pure-QUERY messages are unaffected.

#1595 Phase 3 fifth deletion (2026-10-02): GITHUB_QUERY_PATTERNS is now `[]`
(tombstoned) — "What's the next milestone?" / "Show me the next milestone"
can no longer match it at all, so they ONLY claim via STATUS_PATTERNS'
MILESTONE_STATUS_INLINE_PATTERNS-adjacent phrasing now (confirmed
empirically: single intent, STATUS/get_project_status, no collision to
subsume). The `_apply_subsumption_filter`'s `github_specific_query_actions`
branch (`services/intent_service/pre_classifier.py` ~2481) is therefore
STRUCTURALLY INERT — its member action names (list_milestones_query,
list_releases_query, list_labels_query, list_branches_query, list_prs_query,
list_issues_query) can now only ever be produced by this same now-dead
GITHUB_QUERY_PATTERNS claim path, so the branch's own `query_actions &
github_specific_query_actions` intersection can never be non-empty again.
Kept as documented dead code (tombstone discipline), not removed. Tests
below converted to pin the new reality — the collapse this file was named
for no longer has anything to collapse — rather than deleted.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestQ25SubsumptionFix:
    """#1084: list_milestones_query subsumes STATUS in multi-intent detection.

    #1595 Phase 3 fifth deletion: see module docstring — the subsumption
    rule this class is named for is now structurally inert (GITHUB_QUERY_
    PATTERNS, the only source of a github_specific_query_actions claim, is
    `[]`). Converted to pin what actually happens now, not what the
    subsumption rule used to produce."""

    def test_q25_collapses_to_single_intent_query(self):
        """'What's the next milestone?' is still single-intent — now because
        ONLY STATUS_PATTERNS claims it at all (GITHUB_QUERY_PATTERNS is `[]`
        and can no longer contribute a QUERY sibling for the subsumption
        rule to collapse away), not because the subsumption rule fired."""
        result = PreClassifier.detect_multiple_intents("What's the next milestone?")
        assert not result.is_multi_intent, (
            f"Expected single-intent; got " f"{[(i.category, i.action) for i in result.intents]}"
        )
        assert len(result.intents) == 1
        assert result.intents[0].category == IntentCategory.STATUS
        assert result.intents[0].action == "get_project_status"

    def test_show_me_next_milestone_also_collapses(self):
        """Sibling phrasing: same new reality as the headline case above."""
        result = PreClassifier.detect_multiple_intents("Show me the next milestone")
        assert not result.is_multi_intent
        assert result.intents[0].category == IntentCategory.STATUS
        assert result.intents[0].action == "get_project_status"

    def test_pure_milestone_query_unaffected(self):
        """No-STATUS-overlap phrasing stays single-intent (control).

        #1595 Phase 3 fifth deletion: "list milestones" was the original
        control (GITHUB_QUERY_PATTERNS, no STATUS overlap) — it no longer
        claims at all (confirmed empirically: 0 intents, GITHUB_QUERY_
        PATTERNS is `[]`), degrading this control the same way the
        subsumption cases above degraded. Swapped to "what branch are we
        on" (LOCAL_GIT_STATUS_PATTERNS, unaffected by any of the five
        deletions to date) — same control property: a QUERY-category claim
        with no STATUS overlap, still single-intent."""
        result = PreClassifier.detect_multiple_intents("what branch are we on")
        assert not result.is_multi_intent
        assert result.intents[0].category == IntentCategory.QUERY
        assert result.intents[0].action == "local_git_status_query"

    def test_pure_status_query_unaffected(self):
        """STATUS-only phrasing routes to STATUS (Q11 control)."""
        result = PreClassifier.detect_multiple_intents("What projects are we working on?")
        assert not result.is_multi_intent
        assert result.intents[0].category == IntentCategory.STATUS

    def test_subsumption_rule_triggers_on_all_github_specific_actions(self):
        """#1595 Phase 3 fifth deletion: the rule this test pinned (no
        STATUS leaks through when a github_specific_query_actions claim is
        present) is now vacuous — there is no github_specific_query_actions
        claim left to leak PAST (see module docstring: the branch is
        structurally inert). Converted to pin the actual new reality
        instead of a vacuously-true-for-the-wrong-reason assertion: STATUS
        is now the ONLY category claimed for these phrasings, not a leak
        suppressed by subsumption."""
        for msg in ["What's the next milestone?", "Show me the next milestone"]:
            result = PreClassifier.detect_multiple_intents(msg)
            categories = {i.category.value.upper() for i in result.intents}
            assert categories == {"STATUS"}, (
                f"expected STATUS-only (no subsumption to perform any more) "
                f"for {msg!r}: {[(i.category, i.action) for i in result.intents]}"
            )

    def test_multi_intent_without_github_query_unaffected(self):
        """Multi-intent cases without GitHub-specific QUERY actions still route
        through normal subsumption (no false-positive STATUS-drop)."""
        # Greeting + status should still multi-intent
        result = PreClassifier.detect_multiple_intents("Hi Piper! What's my current project?")
        # Should be multi-intent (greeting + status) — subsumption doesn't fire
        categories = {i.category.value.upper() for i in result.intents}
        assert (
            "STATUS" in categories or "CONVERSATION" in categories
        ), f"Expected STATUS or CONVERSATION; got {categories}"
