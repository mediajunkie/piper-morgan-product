"""
Tests for the Action Registry and related systemic fixes.

Issue #915/#916/#919: Ensures every pre-classifier action has a registry
entry, stub actions route to floor, and multi-intent subsumption works.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.action_registry import (
    ACTION_EXAMPLES,
    ACTION_REGISTRY,
    ACTION_TO_VERB,
    ActionDisposition,
    Verb,
    get_disposition,
    get_verb,
    validate_registry_coverage,
    validate_verb_coverage,
    verb_sourcetype_to_legacy_action,
)
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

# ---- Registry Coverage Tests ----


class TestRegistryCoverage:
    """Every pre-classifier action must have a registry entry."""

    def test_registry_covers_all_pre_classifier_actions(self):
        """The registry should have entries for all pre-classifier outputs."""
        missing = validate_registry_coverage()
        assert missing == [], f"Actions missing from registry: {missing}"

    def test_every_registry_entry_has_example(self):
        """Every registry entry should have an example message."""
        missing_examples = []
        for key in ACTION_REGISTRY:
            if key not in ACTION_EXAMPLES:
                missing_examples.append(f"{key[0]}/{key[1]}")
        assert missing_examples == [], f"Missing examples: {missing_examples}"

    def test_example_messages_classify_correctly(self):
        """Each example message should classify to its expected action."""
        for (category, action), message in ACTION_EXAMPLES.items():
            result = PreClassifier.pre_classify(message)
            if result is not None:
                assert (
                    result.category.value.upper() == category
                ), f"'{message}' expected {category} but got {result.category.value}"

    def test_registry_has_no_empty_entries(self):
        """All registry entries should have valid dispositions."""
        for key, disposition in ACTION_REGISTRY.items():
            assert isinstance(
                disposition, ActionDisposition
            ), f"Invalid disposition for {key}: {disposition}"


class TestDisposition:
    """Test get_disposition lookups."""

    def test_known_canonical_action(self):
        assert get_disposition("IDENTITY", "get_identity") == ActionDisposition.CANONICAL

    def test_known_floor_action(self):
        assert get_disposition("ANALYSIS", "analyze_blockers") == ActionDisposition.FLOOR

    def test_known_workflow_action(self):
        assert get_disposition("QUERY", "meeting_time") == ActionDisposition.WORKFLOW

    def test_unknown_action_defaults_to_floor(self):
        """Unknown actions should default to FLOOR (safe fallback)."""
        assert get_disposition("QUERY", "nonexistent_action") == ActionDisposition.FLOOR

    def test_case_insensitive_category(self):
        """Category lookup should be case-insensitive."""
        assert get_disposition("identity", "get_identity") == ActionDisposition.CANONICAL
        assert get_disposition("IDENTITY", "get_identity") == ActionDisposition.CANONICAL


# ---- Stub Routing Tests ----


class TestStubActionsRouteToFloor:
    """Actions that previously returned dev stubs now route to floor."""

    def test_get_feature_info_disposition_is_floor(self):
        """get_feature_info should route to floor, not return stub."""
        assert get_disposition("QUERY", "get_feature_info") == ActionDisposition.FLOOR

    def test_analyze_blockers_disposition_is_floor(self):
        """analyze_blockers should route to floor, not return stub."""
        assert get_disposition("ANALYSIS", "analyze_blockers") == ActionDisposition.FLOOR


# ---- Response Quality Smoke Tests ----


# Known stub phrases that should NEVER appear in user-facing responses
STUB_PHRASES = [
    "processed successfully:",
    "processed:",
    "Analysis processed:",
    "Query processed successfully:",
    "not yet implemented",
    "not yet fully implemented",
    "Unhandled intent category",
]


class TestNoStubPhrases:
    """Pre-classifier action examples must not produce stub responses.

    These tests can't run the full async pipeline in unit tests,
    but they verify the registry marks stub-prone actions as FLOOR
    so they bypass the stub handlers entirely.
    """

    def test_floor_actions_bypass_stubs(self):
        """Actions marked FLOOR never reach stub handlers."""
        floor_actions = [
            (cat, act)
            for (cat, act), disp in ACTION_REGISTRY.items()
            if disp == ActionDisposition.FLOOR
        ]
        # All previously-stubbed actions should be in this list
        assert ("QUERY", "get_feature_info") in floor_actions
        assert ("ANALYSIS", "analyze_blockers") in floor_actions

    def test_no_handler_actions_without_registry_floor_marking(self):
        """No HANDLER/WORKFLOW action should fall through to a stub.

        This test verifies that the only actions marked as non-FLOOR
        actually have handler branches. Since we can't easily introspect
        handler if/elif chains programmatically, this test documents the
        known-handled actions as a regression guard.
        """
        workflow_actions = [
            (cat, act)
            for (cat, act), disp in ACTION_REGISTRY.items()
            if disp == ActionDisposition.WORKFLOW
        ]
        # All workflow actions should be actions we know have handler branches
        known_handled_query_actions = {
            "meeting_time",
            "recurring_meetings",
            "week_calendar",
            "shipped_query",
            "stale_prs_query",
            "close_issue_query",
            "reopen_issue_query",
            "comment_issue_query",
            "list_issues_query",
            "list_prs_query",
            "review_issue_query",
            # Issue #1039
            "list_milestones_query",
            "list_releases_query",
            # Issue #1040
            "list_labels_query",
            "list_branches_query",
            "update_document_query",
            "changes_query",
            "attention_query",
            "productivity_query",
            # #1394 / ADR-078 B4 — handled by _handle_session_activity_query via the rail
            "session_activity_query",
            # #1411 — handled by _handle_update_issue via the rail (+ elif backstop)
            "update_issue",
            "list_todos_query",
            "list_completed_todos",
            "next_todo_query",
            # RECONNECT #1327: conversational set-default-repo
            "set_default_repo",
            # RECONNECT #1327 build #2: conversational get-default-repo (read)
            "get_default_repo",
        }
        known_handled_execution_actions = {"complete_todo"}

        for cat, act in workflow_actions:
            if cat == "QUERY":
                assert (
                    act in known_handled_query_actions
                ), f"QUERY/{act} marked WORKFLOW but not in known-handled set"
            elif cat == "EXECUTION":
                assert (
                    act in known_handled_execution_actions
                ), f"EXECUTION/{act} marked WORKFLOW but not in known-handled set"


# ---- Verb Canonicalization Tests (#1124 Phase 2, ADR-060 amendment) ----


class TestVerbCoverage:
    """Every registry action maps to a canonical Verb (additive layer)."""

    def test_every_registry_action_maps_to_a_verb(self):
        """validate_verb_coverage() must be empty — no action without a verb."""
        missing = validate_verb_coverage()
        assert missing == [], f"Registry actions with no Verb mapping: {missing}"

    def test_action_to_verb_only_references_real_actions(self):
        """ACTION_TO_VERB must not reference actions absent from the registry."""
        registry_actions = {action for (_cat, action) in ACTION_REGISTRY}
        orphans = [a for a in ACTION_TO_VERB if a not in registry_actions]
        assert orphans == [], f"ACTION_TO_VERB references non-registry actions: {orphans}"

    def test_get_verb_known_actions(self):
        assert get_verb("close_issue_query") == Verb.CLOSE
        assert get_verb("reopen_issue_query") == Verb.REOPEN
        assert get_verb("comment_issue_query") == Verb.COMMENT
        assert get_verb("update_document_query") == Verb.UPDATE
        assert get_verb("greeting") == Verb.GREET
        assert get_verb("list_issues_query") == Verb.LIST

    def test_get_verb_unknown_returns_none(self):
        """Unknown action -> None (caller floors, per ADR-060 floor-default)."""
        assert get_verb("nonexistent_action") is None
        assert get_verb("summarize_github_issue") is None  # the improvised name

    def test_verb_values_are_unique(self):
        values = [v.value for v in Verb]
        assert len(values) == len(set(values)), "Duplicate Verb values"

    def test_cohort_verbs_present(self):
        """Cohort verbs are registered so handlers bind to typed verbs, not
        improvised collapsed names (the #1158 failure pattern)."""
        assert Verb.SUMMARIZE in Verb
        assert Verb.PRIORITIZE in Verb


# ---- Phase 4 transition shim (#1124) ----


class TestVerbSourceToLegacyActionShim:
    """verb + source_type → legacy action string (the Phase 4 consumer shim)."""

    def test_cohort_targets_map_to_category_routing_aliases(self):
        assert verb_sourcetype_to_legacy_action(Verb.PRIORITIZE) == "prioritize"

    def test_summarize_verb_is_deliberately_unmapped_floors(self):
        """SUMMARIZE-TAXONOMY (#1158, 2026-06-09): SUMMARIZE is intentionally NOT in
        the shim. PPM ruled summary output is ALWAYS floor-rendered, so the canonical
        summarize verb must NOT canonicalize to the structured `summarize` action.
        Unmapped → None → caller floors (ADR-060 floor-default), for every source."""
        assert verb_sourcetype_to_legacy_action(Verb.SUMMARIZE) is None
        assert verb_sourcetype_to_legacy_action(Verb.SUMMARIZE, "github_issue") is None
        assert verb_sourcetype_to_legacy_action(Verb.SUMMARIZE, "text") is None

    def test_source_agnostic_fallback(self):
        """Most verbs map to one action regardless of source_type."""
        assert verb_sourcetype_to_legacy_action(Verb.CLOSE) == "close_issue_query"
        # any source_type falls back to the (verb, None) entry
        assert verb_sourcetype_to_legacy_action(Verb.CLOSE, "issue") == "close_issue_query"

    def test_mutation_verb_outputs_are_consistent_with_action_to_verb(self):
        """Registry-backed shim outputs round-trip through get_verb (Phase-2 consistency)."""
        for verb in (Verb.CLOSE, Verb.REOPEN, Verb.COMMENT, Verb.UPDATE, Verb.COMPLETE):
            action = verb_sourcetype_to_legacy_action(verb)
            assert action is not None
            assert get_verb(action) == verb, f"{verb} → {action} → {get_verb(action)}"

    def test_cohort_targets_are_not_registry_actions(self):
        """summarize/prioritize are category-routing aliases, not registry actions —
        so they're not in ACTION_TO_VERB (they're the canonicalization targets)."""
        assert get_verb("summarize") is None
        assert get_verb("prioritize") is None

    def test_unseeded_verbs_floor_safely(self):
        """Pre-classifier-handled broad verbs aren't in the shim → None → caller floors."""
        assert verb_sourcetype_to_legacy_action(Verb.GET) is None
        assert verb_sourcetype_to_legacy_action(Verb.LIST) is None
        assert verb_sourcetype_to_legacy_action(Verb.GET, "anything") is None


# ---- Multi-Intent Subsumption Tests ----


class TestMultiIntentSubsumption:
    """Issue #919: detect_multiple_intents should not produce phantom intents."""

    def test_calendar_check_does_not_produce_temporal(self):
        """'Check my calendar for conflicts' should NOT trigger TEMPORAL."""
        result = PreClassifier.detect_multiple_intents("Check my calendar for conflicts")
        categories = [i.category for i in result.intents]
        assert IntentCategory.QUERY in categories
        assert (
            IntentCategory.TEMPORAL not in categories
        ), "TEMPORAL should be subsumed by QUERY for calendar queries"

    def test_show_my_calendar_does_not_produce_temporal(self):
        """'Show my calendar' should not double-match as TEMPORAL."""
        result = PreClassifier.detect_multiple_intents("Show my calendar")
        categories = [i.category for i in result.intents]
        if IntentCategory.QUERY in categories:
            assert IntentCategory.TEMPORAL not in categories

    def test_whats_on_my_calendar_today(self):
        """'What's on my calendar today' should be QUERY, not QUERY+TEMPORAL."""
        result = PreClassifier.detect_multiple_intents("What's on my calendar today?")
        categories = [i.category for i in result.intents]
        if IntentCategory.QUERY in categories:
            assert IntentCategory.TEMPORAL not in categories

    def test_greeting_plus_calendar_preserved(self):
        """'Good morning! What's on my calendar?' should keep both."""
        result = PreClassifier.detect_multiple_intents("Good morning! What's on my calendar?")
        categories = [i.category for i in result.intents]
        # Greeting + QUERY should both be present
        assert IntentCategory.CONVERSATION in categories
        # But TEMPORAL should be subsumed
        if IntentCategory.QUERY in categories:
            assert IntentCategory.TEMPORAL not in categories

    def test_pure_temporal_not_affected(self):
        """'What time is it?' should still be TEMPORAL (no subsumption)."""
        result = PreClassifier.detect_multiple_intents("What time is it?")
        categories = [i.category for i in result.intents]
        assert IntentCategory.TEMPORAL in categories

    def test_greeting_plus_temporal_preserved(self):
        """'Hello! What time is it?' should keep both CONVERSATION and TEMPORAL."""
        result = PreClassifier.detect_multiple_intents("Hello! What time is it?")
        categories = [i.category for i in result.intents]
        assert IntentCategory.CONVERSATION in categories
        assert IntentCategory.TEMPORAL in categories

    def test_priority_subsumes_guidance(self):
        """Priority queries should subsume guidance when both match."""
        result = PreClassifier.detect_multiple_intents("What should I focus on next?")
        categories = [i.category for i in result.intents]
        # At most one of PRIORITY or GUIDANCE, not both
        if IntentCategory.PRIORITY in categories:
            assert IntentCategory.GUIDANCE not in categories

    def test_single_intent_not_affected(self):
        """Single-intent messages should pass through unchanged."""
        result = PreClassifier.detect_multiple_intents("Close issue #42")
        assert len(result.intents) == 1
        assert result.intents[0].category == IntentCategory.QUERY
