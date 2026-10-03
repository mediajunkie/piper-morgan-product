"""
Tests for #488 DISCOVERY intent - capability discovery queries.

Issue #488: MUX-INTERACT-DISCOVERY
Tests that "What can you do?" queries route to DISCOVERY (not IDENTITY).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestDiscoveryPatternMatching:
    """Test DISCOVERY_PATTERNS matching in pre_classifier."""

    # #1595 Phase 3, ninth deletion (2026-10-03): DISCOVERY_PATTERNS was
    # PARTIALLY emptied — 19 of 20 literals tombstoned, 1 SURVIVES
    # (`\bneed\s*help\b`). Every phrasing below matched one of the 19
    # deleted literals; none of them match the lone survivor, so surface 1
    # (PreClassifier.pre_classify) now returns None for all of them —
    # unclaimed, not misrouted. Production still reaches get_capabilities
    # for the real corpus rows these phrasings are drawn from, via the LLM
    # classifier at surface 2 (verified live for the corpus's own wording in
    # the deletion gate/ledger, scripts/inversion_phase3_deleted_patterns.json
    # DISCOVERY_PATTERNS entry) — this suite makes no live-LLM call, so it
    # asserts only the surface-1 claim, not the end-to-end route.
    @pytest.mark.parametrize(
        "message",
        [
            "what can you do",
            "What can you do?",
            "what are your capabilities",
            "show me your capabilities",
            "what services do you offer",
            "what features do you have",
            "what can you help with",
            "menu of services",
            "list your capabilities",
            "your capabilities",
            "capability menu",
            "capabilities menu",
            "show menu",
            "what are you able to do",
            "show features",
            "available features",
            # Issue #814: "help me get started" moved to GUIDANCE (setup routing)
        ],
    )
    def test_discovery_patterns_now_unclaimed_by_surface_1(self, message: str):
        """Capability-query phrasings that matched a DELETED DISCOVERY_PATTERNS
        literal are now unclaimed by surface 1 (ninth deletion, partial)."""
        result = PreClassifier.pre_classify(message)

        assert result is None, (
            f"'{message}' should be unclaimed by surface 1 post-ninth-deletion, "
            f"got {result!r} — either a literal survived that shouldn't have, "
            f"or this phrase matches the surviving \\bneed\\s*help\\b literal"
        )

    def test_discovery_survivor_literal_still_matches(self):
        """The one load-bearing DISCOVERY_PATTERNS survivor
        (`\\bneed\\s*help\\b`) still claims DISCOVERY/get_capabilities —
        the partial deletion did not touch the class's claim branch, only
        its literal count."""
        result = PreClassifier.pre_classify("I need help understanding something")

        assert result is not None
        assert result.category == IntentCategory.DISCOVERY
        assert result.action == "get_capabilities"

    @pytest.mark.parametrize(
        "message",
        [
            "who are you",
            "what's your name",
            "your role",
            "what do you do",  # This is ambiguous but kept in IDENTITY
            "tell me about yourself",
            "introduce yourself",
        ],
    )
    def test_identity_patterns_still_work(self, message: str):
        """Test that identity queries still route to IDENTITY (regression test)."""
        result = PreClassifier.pre_classify(message)

        assert result is not None, f"'{message}' should match a pattern"
        assert (
            result.category == IntentCategory.IDENTITY
        ), f"'{message}' should route to IDENTITY, got {result.category}"
        assert result.action == "get_identity"

    def test_discovery_before_identity_precedence(self):
        """Test that DISCOVERY patterns are checked before IDENTITY."""
        # This tests the fix from #488 - capability queries shouldn't
        # accidentally match IDENTITY patterns
        #
        # #1595 Phase 3 ninth deletion (2026-10-03): the original fixture
        # phrase "what can you do for me" matched a now-deleted
        # DISCOVERY_PATTERNS literal (`\bwhat can you do\b`); swapped to the
        # one load-bearing survivor (`\bneed\s*help\b`) — still exercises
        # DISCOVERY's position ahead of IDENTITY in pre_classify's if-chain
        # (confirmed live this session: still routes to DISCOVERY, not
        # IDENTITY).

        discovery_message = "I need help understanding something"
        result = PreClassifier.pre_classify(discovery_message)

        # Should match DISCOVERY, not IDENTITY
        assert result is not None
        assert result.category == IntentCategory.DISCOVERY


class TestIntentCategoryEnum:
    """Test that DISCOVERY is properly added to IntentCategory."""

    def test_discovery_in_enum(self):
        """Test that DISCOVERY exists in IntentCategory."""
        assert hasattr(IntentCategory, "DISCOVERY")
        assert IntentCategory.DISCOVERY.value == "discovery"

    def test_identity_still_exists(self):
        """Test that IDENTITY still exists (regression)."""
        assert hasattr(IntentCategory, "IDENTITY")
        assert IntentCategory.IDENTITY.value == "identity"
