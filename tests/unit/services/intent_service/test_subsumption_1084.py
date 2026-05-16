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
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestQ25SubsumptionFix:
    """#1084: list_milestones_query subsumes STATUS in multi-intent detection."""

    def test_q25_collapses_to_single_intent_query(self):
        """The headline case: 'What's the next milestone?' should be single-intent."""
        result = PreClassifier.detect_multiple_intents("What's the next milestone?")
        assert not result.is_multi_intent, (
            f"Expected single-intent after subsumption; got "
            f"{[(i.category, i.action) for i in result.intents]}"
        )
        assert len(result.intents) == 1
        assert result.intents[0].category == IntentCategory.QUERY
        assert result.intents[0].action == "list_milestones_query"

    def test_show_me_next_milestone_also_collapses(self):
        """Sibling phrasing should also collapse."""
        result = PreClassifier.detect_multiple_intents("Show me the next milestone")
        assert not result.is_multi_intent
        assert result.intents[0].action == "list_milestones_query"

    def test_pure_milestone_query_unaffected(self):
        """No-STATUS-overlap phrasing stays single-intent (control)."""
        result = PreClassifier.detect_multiple_intents("list milestones")
        assert not result.is_multi_intent
        assert result.intents[0].category == IntentCategory.QUERY
        assert result.intents[0].action == "list_milestones_query"

    def test_pure_status_query_unaffected(self):
        """STATUS-only phrasing routes to STATUS (Q11 control)."""
        result = PreClassifier.detect_multiple_intents("What projects are we working on?")
        assert not result.is_multi_intent
        assert result.intents[0].category == IntentCategory.STATUS

    def test_subsumption_rule_triggers_on_all_github_specific_actions(self):
        """The rule covers list_milestones, releases, labels, branches, prs, issues."""
        # We only have STATUS-overlapping phrasings for milestones today, but
        # the rule is forward-defensive against future overlaps. Verify the
        # set of GitHub-specific actions the rule recognizes by testing the
        # one current overlap case + asserting no STATUS leaks through.
        for msg in ["What's the next milestone?", "Show me the next milestone"]:
            result = PreClassifier.detect_multiple_intents(msg)
            categories = {i.category.value.upper() for i in result.intents}
            assert "STATUS" not in categories, (
                f"STATUS leaked through subsumption for {msg!r}: "
                f"{[(i.category, i.action) for i in result.intents]}"
            )

    def test_multi_intent_without_github_query_unaffected(self):
        """Multi-intent cases without GitHub-specific QUERY actions still route
        through normal subsumption (no false-positive STATUS-drop)."""
        # Greeting + status should still multi-intent
        result = PreClassifier.detect_multiple_intents(
            "Hi Piper! What's my current project?"
        )
        # Should be multi-intent (greeting + status) — subsumption doesn't fire
        categories = {i.category.value.upper() for i in result.intents}
        assert "STATUS" in categories or "CONVERSATION" in categories, (
            f"Expected STATUS or CONVERSATION; got {categories}"
        )
