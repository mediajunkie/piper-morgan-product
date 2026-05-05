"""Pre-classifier pattern tests for milestones + releases (Issue #1039)."""

from __future__ import annotations

import pytest

from services.intent_service.pre_classifier import PreClassifier


class TestMilestonePatterns:
    """Issue #1039: milestone-listing pattern matches."""

    @pytest.mark.parametrize(
        "msg",
        [
            "show milestones",
            "Show milestones",
            "show me the milestones",
            "list milestones",
            "list our milestones",
            "next milestone",
            "what milestones are open",
            "what milestones",
            "when is the next milestone",
            "milestones status",
            "milestones list",
        ],
    )
    def test_positive_match(self, msg):
        matched = PreClassifier._matches_patterns(
            msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS
        )
        assert matched, f"expected match for {msg!r}"
        action = PreClassifier._get_github_action(msg.lower())
        assert action == "list_milestones_query", (
            f"expected list_milestones_query for {msg!r}, got {action}"
        )

    @pytest.mark.parametrize(
        "msg",
        [
            "milestone moment in my career",  # singular as adjective; no list verb
            "I had a milestone last year",  # narrative usage
        ],
    )
    def test_negative_no_match(self, msg):
        # These should NOT match the github_query pattern set
        matched = PreClassifier._matches_patterns(
            msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS
        )
        assert not matched, f"unexpected match for {msg!r}"


class TestReleasePatterns:
    """Issue #1039: release-listing pattern matches."""

    @pytest.mark.parametrize(
        "msg",
        [
            "recent releases",
            "show releases",
            "show me releases",
            "list releases",
            "list our releases",
            "what version are we on",
            "what version is current",
            "current release",
            "current version",
            "latest release",
        ],
    )
    def test_positive_match(self, msg):
        matched = PreClassifier._matches_patterns(
            msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS
        )
        assert matched, f"expected match for {msg!r}"
        action = PreClassifier._get_github_action(msg.lower())
        assert action == "list_releases_query", (
            f"expected list_releases_query for {msg!r}, got {action}"
        )

    @pytest.mark.parametrize(
        "msg",
        [
            "release me from this meeting",  # "release" as verb, not noun
            "I need a release from this stress",
        ],
    )
    def test_negative_no_match(self, msg):
        matched = PreClassifier._matches_patterns(
            msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS
        )
        assert not matched, f"unexpected match for {msg!r}"


class TestNoRegressionsExistingPatterns:
    """New patterns don't shadow existing GitHub query routes."""

    @pytest.mark.parametrize(
        "msg,expected_action",
        [
            ("show issues", "list_issues_query"),
            ("list issues", "list_issues_query"),
            ("open issues", "list_issues_query"),
            ("show my prs", "list_prs_query"),
            ("list my prs", "list_prs_query"),
            ("show stale prs", "stale_prs_query"),
            ("what shipped this week", "shipped_query"),
            ("close issue #42", "close_issue_query"),
            ("reopen issue #42", "reopen_issue_query"),
            ("comment on issue #42", "comment_issue_query"),
        ],
    )
    def test_existing_patterns_unchanged(self, msg, expected_action):
        matched = PreClassifier._matches_patterns(
            msg.lower(), PreClassifier.GITHUB_QUERY_PATTERNS
        )
        assert matched
        action = PreClassifier._get_github_action(msg.lower())
        assert action == expected_action, f"{msg!r}: expected {expected_action}, got {action}"


class TestStateFilterPatternsExcluded:
    """Q3 + Q4 dispositions: state-filter patterns NOT included.

    PM 2026-05-04: 'I don't like shaky nonfunctional features — withhold
    till status has meaning.' These patterns are tracked by #1051 for
    post-MVP wiring.
    """

    @pytest.mark.parametrize(
        "msg",
        [
            # These should not be added until state-filter UX ships (#1051)
            "open milestones",
            "closed milestones",
            "show pre-releases",
            "list prereleases",
        ],
    )
    def test_state_filter_patterns_intentionally_absent(self, msg):
        # These DO match other things (e.g., "open milestones" could match
        # via show.*milestones?), but specifically the state-filter qualifiers
        # should not have their own dedicated patterns. The bare
        # \bopen milestones?\b and \bclosed milestones?\b patterns must
        # NOT exist in the pattern set.
        # We assert this by verifying the patterns array doesn't contain them.
        forbidden = [
            r"\bopen milestones?\b",
            r"\bclosed milestones?\b",
            r"\bpre[- ]releases?\b",
            r"\bprereleases?\b",
        ]
        for pattern in forbidden:
            assert pattern not in PreClassifier.GITHUB_QUERY_PATTERNS, (
                f"State-filter pattern {pattern!r} present; should be deferred to #1051"
            )


class TestActionRegistry:
    """New actions registered for #1039."""

    def test_milestones_action_registered(self):
        from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition

        assert ("QUERY", "list_milestones_query") in ACTION_REGISTRY
        assert (
            ACTION_REGISTRY[("QUERY", "list_milestones_query")]
            == ActionDisposition.WORKFLOW
        )

    def test_releases_action_registered(self):
        from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition

        assert ("QUERY", "list_releases_query") in ACTION_REGISTRY
        assert (
            ACTION_REGISTRY[("QUERY", "list_releases_query")]
            == ActionDisposition.WORKFLOW
        )


class TestLensInference:
    """New actions map to PROJECTS lens."""

    def test_milestones_lens(self):
        from services.intent_service.lens_inference import ACTION_TO_LENS
        from services.shared_types import ConversationalLens

        assert ACTION_TO_LENS["list_milestones_query"] == ConversationalLens.PROJECTS

    def test_releases_lens(self):
        from services.intent_service.lens_inference import ACTION_TO_LENS
        from services.shared_types import ConversationalLens

        assert ACTION_TO_LENS["list_releases_query"] == ConversationalLens.PROJECTS
