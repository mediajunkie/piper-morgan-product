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
    def test_discovery_patterns_match(self, message: str):
        """Test that capability queries route to DISCOVERY."""
        result = PreClassifier.pre_classify(message)

        assert result is not None, f"'{message}' should match a pattern"
        assert (
            result.category == IntentCategory.DISCOVERY
        ), f"'{message}' should route to DISCOVERY, got {result.category}"
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

        discovery_message = "what can you do for me"
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
