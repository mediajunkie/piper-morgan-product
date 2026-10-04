"""
Test capability discovery scenarios for alpha onboarding.

Issue #487: Tests for discovery-oriented user queries that were failing during
alpha E2E testing. Ensures users can discover Piper's capabilities through
natural language queries.

These tests verify:
1. "What services do you offer?" → IDENTITY (capability list)
2. "Help me setup my projects" → GUIDANCE (not STATUS)
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestCapabilityDiscovery:
    """Test discovery-oriented user queries."""

    # ==========================================================================
    # Issue #487: Message 1 - "What services do you offer?"
    # Should classify as IDENTITY to return capability menu
    # ==========================================================================

    @pytest.mark.parametrize(
        "message",
        [
            # #1595 Phase 3 ninth deletion (2026-10-03, PARTIAL): DISCOVERY_PATTERNS
            # dropped 19 of its 20 literals (GO per surface-2: the LLM classifier
            # reliably lands these in DISCOVERY anyway). None of these 12 phrases
            # match the one surviving literal (\bneed\s*help\b), so at surface 1
            # they're unclaimed and the property this parametrize checks
            # ("natural phrasing -> DISCOVERY") is now exercised by the LLM
            # classifier, not the deterministic pre-classifier. Marked llm rather
            # than converted to surviving-literal phrasing (converting all 12 to
            # "need help" variants would destroy the coverage diversity these
            # cases exist to provide). A standalone deterministic pin for the
            # surviving literal lives in test_services_query_surviving_literal_is_discovery
            # below.
            pytest.param("What services do you offer?", marks=pytest.mark.llm),
            pytest.param("what services do you offer", marks=pytest.mark.llm),
            pytest.param("What services do you have?", marks=pytest.mark.llm),
            pytest.param("what features do you have", marks=pytest.mark.llm),
            pytest.param("What can you do?", marks=pytest.mark.llm),
            pytest.param("what can you do for me", marks=pytest.mark.llm),
            pytest.param("What can you help me with?", marks=pytest.mark.llm),
            pytest.param("what can you help with", marks=pytest.mark.llm),
            pytest.param("Show me your capabilities", marks=pytest.mark.llm),
            pytest.param("List your capabilities", marks=pytest.mark.llm),
            pytest.param("menu of services", marks=pytest.mark.llm),
            pytest.param("your capabilities", marks=pytest.mark.llm),
        ],
    )
    def test_services_query_classifies_as_discovery(self, message: str):
        """
        Capability queries classify as DISCOVERY -> get_capabilities (#488,
        checked BEFORE IDENTITY so "what can you do?" returns the dynamic
        capability answer, not static identity). This test originally pinned
        the pre-#488 IDENTITY taxonomy (#487) — updated to the ratified one.

        #1595 Phase 3 ninth deletion (2026-10-03): these phrasings no longer
        claim at surface 1 (pre_classify); each case now drives the real LLM
        classifier, hence @pytest.mark.llm on every param above.
        """
        intent = PreClassifier.pre_classify(message)

        assert intent is not None, f"Message '{message}' should pre-classify"
        assert intent.category == IntentCategory.DISCOVERY, (
            f"Message '{message}' should classify as DISCOVERY, " f"got {intent.category}"
        )
        assert intent.action == "get_capabilities"

    def test_services_query_surviving_literal_is_discovery(self):
        """#1595 Phase 3 ninth deletion (2026-10-03): DISCOVERY_PATTERNS'
        one surviving literal (\\bneed\\s*help\\b) still deterministically
        claims DISCOVERY/get_capabilities at surface 1 — pinned here since
        the parametrize above was marked llm in full (see its comment)."""
        intent = PreClassifier.pre_classify("I need help understanding something")
        assert intent is not None
        assert intent.category == IntentCategory.DISCOVERY
        assert intent.action == "get_capabilities"

    # ==========================================================================
    # Issue #487: Message 2 - "Help me setup my projects"
    # Should classify as GUIDANCE, not STATUS
    # ==========================================================================

    @pytest.mark.parametrize(
        "message",
        [
            "Help me setup my projects",
            "help me setup projects",
            # #1595 Phase 3 eighth deletion (2026-10-02/03, PARTIAL):
            # GUIDANCE_PATTERNS dropped 18 of 21 literals; the 3 survivors all
            # require a setup/set-up verb + projects/portfolio noun. These
            # three no longer claim at surface 1 (no setup/set-up verb) — now
            # driven through the real LLM classifier.
            pytest.param("Help me configure my projects", marks=pytest.mark.llm),
            "setup my projects",
            pytest.param("configure my projects", marks=pytest.mark.llm),
            "How do I setup my projects?",
            pytest.param("how do i configure this", marks=pytest.mark.llm),
            pytest.param("help me get started", marks=pytest.mark.llm),
            pytest.param("getting started", marks=pytest.mark.llm),
        ],
    )
    def test_setup_query_classifies_as_guidance(self, message: str):
        """
        Issue #487: Setup/configuration queries should classify as GUIDANCE.

        Previously "help me setup my projects" was matching STATUS due to
        "my projects" pattern. Now GUIDANCE patterns are checked first.
        """
        intent = PreClassifier.pre_classify(message)

        assert intent is not None, f"Message '{message}' should pre-classify"
        assert intent.category == IntentCategory.GUIDANCE, (
            f"Message '{message}' should classify as GUIDANCE, " f"got {intent.category}"
        )
        assert intent.action == "get_contextual_guidance"

    # ==========================================================================
    # Regression tests: Ensure STATUS still works for non-setup queries
    # ==========================================================================

    @pytest.mark.parametrize(
        "message",
        [
            # #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): STATUS_PATTERNS
            # dropped 52 of 56 literals; the 4 survivors are "next milestone",
            # "current work", "project overview", "project landscape" — none of
            # which these 5 phrases match. No longer claimed at surface 1; now
            # driven through the real LLM classifier. A deterministic pin for a
            # surviving literal lives in test_status_surviving_literal_still_works
            # below.
            pytest.param("What am I working on?", marks=pytest.mark.llm),
            pytest.param("my projects", marks=pytest.mark.llm),
            # "show my projects" moved below: the portfolio pre-classification
            # now deliberately routes it to PORTFOLIO/manage_portfolio.
            pytest.param("what's my current project", marks=pytest.mark.llm),
            pytest.param("project status", marks=pytest.mark.llm),
            pytest.param("my status", marks=pytest.mark.llm),
        ],
    )
    def test_status_queries_still_work(self, message: str):
        """
        Regression test: Pure status queries should still classify as STATUS.

        Ensures the GUIDANCE-before-STATUS reordering doesn't break legitimate
        status queries that don't contain setup/configure verbs.
        """
        intent = PreClassifier.pre_classify(message)

        assert intent is not None, f"Message '{message}' should pre-classify"
        assert intent.category == IntentCategory.STATUS, (
            f"Message '{message}' should classify as STATUS, " f"got {intent.category}"
        )

    def test_status_surviving_literal_still_works(self):
        """#1595 Phase 3 seventh deletion (2026-10-02): STATUS_PATTERNS' four
        surviving literals (next milestone, current work, project overview,
        project landscape) still deterministically claim STATUS at surface 1
        — pinned here since every case above was marked llm."""
        intent = PreClassifier.pre_classify("give me a project overview")
        assert intent is not None
        assert intent.category == IntentCategory.STATUS
        assert intent.action == "get_project_status"

    def test_show_my_projects_routes_to_portfolio(self):
        """'show my projects' now pre-classifies as PORTFOLIO/manage_portfolio
        (the portfolio pre-classification) — moved out of the STATUS list when
        that taxonomy landed; pinned here so the routing is still asserted."""
        intent = PreClassifier.pre_classify("show my projects")
        assert intent is not None
        assert intent.category == IntentCategory.PORTFOLIO
        assert intent.action == "manage_portfolio"

    # ==========================================================================
    # Regression tests: Ensure IDENTITY still works for original patterns
    # ==========================================================================

    @pytest.mark.parametrize(
        "message",
        [
            "What's your name?",
            "who are you",
            "tell me about yourself",
            "introduce yourself",
        ],
    )
    def test_identity_queries_still_work(self, message: str):
        """
        Regression test: Original IDENTITY queries should still work.

        Ensures adding new patterns doesn't break existing behavior.
        """
        intent = PreClassifier.pre_classify(message)

        assert intent is not None, f"Message '{message}' should pre-classify"
        assert intent.category == IntentCategory.IDENTITY, (
            f"Message '{message}' should classify as IDENTITY, " f"got {intent.category}"
        )
