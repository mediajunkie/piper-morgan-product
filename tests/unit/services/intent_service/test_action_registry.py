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
    ActionDisposition,
    get_disposition,
    validate_registry_coverage,
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
            "list_todos_query",
            "list_completed_todos",
            "next_todo_query",
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
