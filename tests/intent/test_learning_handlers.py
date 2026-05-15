"""
Tests for LEARNING category handlers in IntentService.

These tests cover pattern learning handlers that LEARN from historical data
to identify patterns, recognize similarities, and improve future decisions.

Test Coverage:
- _handle_learn_pattern (Phase 5 - FINAL HANDLER!)
  - Issue similarity pattern learning
  - Validation and error handling
  - Pattern structure and quality

Created: 2025-10-11 (Phase 5 - GAP-1 FINAL HANDLER)
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.shared_types import IntentCategory


@pytest.fixture
def mock_orchestration_engine():
    """Mock orchestration engine for testing."""
    mock_engine = Mock()
    mock_engine.create_workflow_from_intent = AsyncMock()

    # Mock workflow
    mock_workflow = Mock()
    mock_workflow.id = "test-workflow-learning"
    mock_engine.create_workflow_from_intent.return_value = mock_workflow

    return mock_engine


@pytest.fixture
def intent_service(mock_orchestration_engine):
    """Create IntentService instance for testing."""
    return IntentService()


class TestHandleLearnPattern:
    """Test suite for LEARNING category - pattern learning handler."""

    # =========================================================================
    # HANDLER EXISTENCE AND VALIDATION TESTS
    # =========================================================================

    def test_learn_pattern_handler_exists(self, intent_service):
        """Test that _handle_learn_pattern handler exists and is callable."""
        assert hasattr(intent_service, "_handle_learn_pattern")
        assert callable(intent_service._handle_learn_pattern)

    @pytest.mark.asyncio
    async def test_learn_pattern_not_placeholder(self, intent_service):
        """Test that handler is NOT a placeholder (no requires_clarification=True)."""
        intent = Intent(
            original_message="learn from authentication issues",
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.95,
            context={
                "pattern_type": "issue_similarity",
                "source": "github_issues",
                "query": "authentication",
            },
        )

        result = await intent_service._handle_learn_pattern(intent, workflow_id="test_wf")

        # Should NOT have requires_clarification=True (placeholder indicator)
        assert result.requires_clarification is not True, "Handler should not be a placeholder"

    @pytest.mark.asyncio
    async def test_learn_pattern_missing_type(self, intent_service):
        """Test validation when pattern_type parameter is missing."""
        intent = Intent(
            original_message="learn from issues",
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.95,
            context={
                "source": "github_issues",
                # Missing pattern_type
            },
        )

        result = await intent_service._handle_learn_pattern(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "pattern_type_required"
        assert "pattern" in result.message.lower() and "type" in result.message.lower()

    @pytest.mark.asyncio
    async def test_learn_pattern_missing_source(self, intent_service):
        """Test validation when source parameter is missing."""
        intent = Intent(
            original_message="learn patterns",
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.95,
            context={
                "pattern_type": "issue_similarity",
                # Missing source
            },
        )

        result = await intent_service._handle_learn_pattern(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "source_required"
        assert "source" in result.message.lower()

    @pytest.mark.asyncio
    async def test_learn_pattern_unknown_type(self, intent_service):
        """Test validation when pattern_type is not supported."""
        intent = Intent(
            original_message="learn quantum patterns",
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.95,
            context={
                "pattern_type": "quantum_entanglement",
                "source": "github_issues",
            },
        )

        result = await intent_service._handle_learn_pattern(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "unsupported_pattern_type"
        assert "unsupported" in result.message.lower() or "not supported" in result.message.lower()
        # Should list supported types
        assert "issue_similarity" in result.message.lower()

    # =========================================================================
    # SUCCESS TESTS - ISSUE SIMILARITY LEARNING
    # =========================================================================

    @pytest.mark.asyncio
    async def test_learn_pattern_issue_similarity_success(self, intent_service):
        """Test successful issue similarity pattern learning."""
        intent = Intent(
            original_message="learn from authentication issues",
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.95,
            context={
                "pattern_type": "issue_similarity",
                "source": "github_issues",
                "query": "authentication",
                "timeframe": "6_months",
                "min_occurrences": 2,
            },
        )

        result = await intent_service._handle_learn_pattern(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain patterns_found
        assert "patterns_found" in result.intent_data
        patterns = result.intent_data["patterns_found"]
        assert isinstance(patterns, list)

        # Should have metadata
        assert "pattern_type" in result.intent_data
        assert result.intent_data["pattern_type"] == "issue_similarity"
        assert "total_items_analyzed" in result.intent_data
        assert "patterns_count" in result.intent_data
        assert result.intent_data["patterns_count"] == len(patterns)

        # If patterns found, verify structure
        if len(patterns) > 0:
            pattern = patterns[0]
            assert "pattern_id" in pattern or "description" in pattern
            assert "confidence" in pattern or "occurrences" in pattern

    @pytest.mark.asyncio
    async def test_learn_pattern_with_examples(self, intent_service):
        """Test that patterns include examples when found."""
        intent = Intent(
            original_message="learn bug patterns",
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.95,
            context={
                "pattern_type": "issue_similarity",
                "source": "github_issues",
                "query": "bug",
            },
        )

        result = await intent_service._handle_learn_pattern(intent, workflow_id="test_wf")

        assert result.success is True

        patterns = result.intent_data.get("patterns_found", [])
        if len(patterns) > 0:
            pattern = patterns[0]
            # Should have examples or occurrences
            assert "examples" in pattern or "occurrences" in pattern

            # If examples exist, verify structure
            if "examples" in pattern and pattern["examples"]:
                example = pattern["examples"][0]
                # Should have issue reference
                assert "number" in example or "title" in example

    @pytest.mark.asyncio
    async def test_learn_pattern_no_data_graceful(self, intent_service):
        """Test graceful handling when no historical data available."""
        intent = Intent(
            original_message="learn from nonexistent data",
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.95,
            context={
                "pattern_type": "issue_similarity",
                "source": "github_issues",
                "query": "zzz_nonexistent_query_zzz",
            },
        )

        result = await intent_service._handle_learn_pattern(intent, workflow_id="test_wf")

        # Should succeed but with no patterns
        assert result.success is True
        assert result.intent_data["patterns_count"] == 0
        assert len(result.intent_data["patterns_found"]) == 0

        # Should have informative message
        assert "no" in result.message.lower() or "0" in result.message.lower()
