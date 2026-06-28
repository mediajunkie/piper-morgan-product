"""Pre-classifier pattern tests for labels + branches (Issue #1040)."""

from __future__ import annotations

import pytest

from services.intent_service.pre_classifier import PreClassifier


class TestLabelPatterns:
    """Issue #1040: label-listing pattern matches."""

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
        assert matched, f"expected match for {msg!r}"
        action = PreClassifier._get_github_action(msg.lower())
        assert (
            action == "list_labels_query"
        ), f"expected list_labels_query for {msg!r}, got {action}"

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
    """Issue #1040: branch-listing pattern matches."""

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
        assert matched, f"expected match for {msg!r}"
        action = PreClassifier._get_github_action(msg.lower())
        assert (
            action == "list_branches_query"
        ), f"expected list_branches_query for {msg!r}, got {action}"

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
    """New patterns don't shadow existing GitHub query routes."""

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
        assert matched
        action = PreClassifier._get_github_action(msg.lower())
        assert action == expected_action, f"{msg!r}: expected {expected_action}, got {action}"


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


class TestLensInference:
    """New actions map to PROJECTS lens."""

    def test_labels_lens(self):
        from services.intent_service.lens_inference import ACTION_TO_LENS
        from services.shared_types import ConversationalLens

        assert ACTION_TO_LENS["list_labels_query"] == ConversationalLens.PROJECTS

    def test_branches_lens(self):
        from services.intent_service.lens_inference import ACTION_TO_LENS
        from services.shared_types import ConversationalLens

        assert ACTION_TO_LENS["list_branches_query"] == ConversationalLens.PROJECTS
