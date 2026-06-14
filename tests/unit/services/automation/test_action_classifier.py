"""Tests for ActionClassifier safety classification (#225) + the #1210 fix.

#1210: the "_query" ROUTING suffix contains the SAFE keyword "query", so a plain
substring scan classified mutating actions (close_issue_query / reopen_issue_query
/ comment_issue_query) as SAFE → autonomous-executable. The fix matches mutating
CONFIRMATION verbs as exact underscore-delimited tokens, checked before the safe
scan, while verb-less reads (attention_query, shipped_query) still classify SAFE.

These tests pin the inner safety gate (the OUTER gate is the #1195 allow-list).
"""

import pytest

from services.automation.action_classifier import ActionClassifier, ActionSafetyLevel


@pytest.fixture
def clf():
    return ActionClassifier()


# ---------------------------------------------------------------------------
# #1210 regression — mutating "_query" actions must NOT be SAFE
# ---------------------------------------------------------------------------


class TestMutatingQuerySuffixNotSafe:
    @pytest.mark.parametrize(
        "action",
        ["close_issue_query", "reopen_issue_query", "comment_issue_query"],
    )
    def test_mutating_query_actions_not_safe(self, clf, action):
        """The #1210 bug: these matched the safe 'query' substring → SAFE.
        They are state-changing and must require confirmation (never auto-exec)."""
        result = clf.classify_action(action)
        assert result.safety_level != ActionSafetyLevel.SAFE, (
            f"{action} classified SAFE — the #1210 regression "
            f"(reason: {result.reason})"
        )
        assert result.safety_level == ActionSafetyLevel.REQUIRES_CONFIRMATION

    @pytest.mark.parametrize(
        "action",
        ["close_issue_query", "reopen_issue_query", "comment_issue_query"],
    )
    def test_mutating_query_actions_blocked_from_auto_exec_even_high_conf(self, clf, action):
        """Even at confidence 1.0, mutating actions must not auto-execute."""
        assert clf.is_safe_for_auto_execution(action, confidence=1.0) is False

    def test_update_document_query_is_destructive(self, clf):
        """'update' is destructive → never auto-execute (caught before 'query')."""
        result = clf.classify_action("update_document_query")
        assert result.safety_level == ActionSafetyLevel.DESTRUCTIVE
        assert clf.is_safe_for_auto_execution("update_document_query", 1.0) is False


# ---------------------------------------------------------------------------
# Read "_query" actions (on the #1195 allow-list) must STAY SAFE
# ---------------------------------------------------------------------------


class TestReadQueryActionsStaySafe:
    @pytest.mark.parametrize(
        "action",
        [
            "list_issues_query",
            "list_prs_query",
            "list_labels_query",   # collision check: "labels" token != "label" verb
            "list_milestones_query",
            "next_todo_query",
            "attention_query",     # verb-less read — SAFE only via the "query" token
            "shipped_query",       # verb-less read
            "get_issue",
        ],
    )
    def test_read_query_actions_are_safe(self, clf, action):
        result = clf.classify_action(action)
        assert result.safety_level == ActionSafetyLevel.SAFE, (
            f"{action} should be SAFE (read) but got {result.safety_level} "
            f"(reason: {result.reason})"
        )

    @pytest.mark.parametrize("action", ["list_issues_query", "attention_query", "get_issue"])
    def test_read_query_actions_auto_exec_at_high_conf(self, clf, action):
        assert clf.is_safe_for_auto_execution(action, confidence=0.95) is True

    def test_safe_action_below_confidence_threshold_not_auto_exec(self, clf):
        """SAFE but confidence < 0.9 → still requires confirmation."""
        assert clf.is_safe_for_auto_execution("list_issues_query", confidence=0.8) is False


# ---------------------------------------------------------------------------
# General keyword classification
# ---------------------------------------------------------------------------


class TestKeywordClassification:
    @pytest.mark.parametrize("action", ["delete_repo", "deploy_prod", "publish_doc", "drop_table"])
    def test_destructive_keywords_never_auto_exec(self, clf, action):
        result = clf.classify_action(action)
        assert result.safety_level == ActionSafetyLevel.DESTRUCTIVE
        assert clf.is_safe_for_auto_execution(action, confidence=1.0) is False

    @pytest.mark.parametrize("action", ["create_issue", "comment_on_pr", "add_label", "send_message"])
    def test_confirmation_keywords_require_approval(self, clf, action):
        result = clf.classify_action(action)
        assert result.safety_level == ActionSafetyLevel.REQUIRES_CONFIRMATION

    def test_unknown_action_defaults_to_confirmation(self, clf):
        result = clf.classify_action("frobnicate_widget")
        assert result.safety_level == ActionSafetyLevel.REQUIRES_CONFIRMATION
