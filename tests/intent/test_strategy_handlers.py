"""
Tests for STRATEGY category handlers in IntentService.

These tests cover strategic planning handlers that PLAN future actions
(as opposed to ANALYSIS handlers that understand past/present, or SYNTHESIS
handlers that create new content).

Test Coverage:
- _handle_strategic_planning (Phase 4)
  - sprint planning
  - feature roadmap planning
  - issue resolution planning
  - validation and error handling

Created: 2025-10-11 (Phase 4 - CORE-CRAFT-GAP)
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
    mock_workflow.id = "test-workflow-strategy"
    mock_engine.create_workflow_from_intent.return_value = mock_workflow

    return mock_engine


@pytest.fixture
def intent_service(mock_orchestration_engine):
    """Create IntentService instance for testing."""
    return IntentService()


class TestHandleStrategicPlanning:
    """Test suite for STRATEGY category - strategic planning handler."""

    # =========================================================================
    # HANDLER EXISTENCE AND VALIDATION TESTS
    # =========================================================================

    def test_strategic_planning_handler_exists(self, intent_service):
        """Test that _handle_strategic_planning handler exists and is callable."""
        assert hasattr(intent_service, "_handle_strategic_planning")
        assert callable(intent_service._handle_strategic_planning)

    @pytest.mark.asyncio
    async def test_strategic_planning_missing_planning_type(self, intent_service):
        """Test validation when planning_type parameter is missing."""
        intent = Intent(
            original_message="create a plan",
            category=IntentCategory.STRATEGY,
            action="strategic_planning",
            confidence=0.95,
            context={
                "goal": "Complete authentication features",
                # Missing planning_type
            },
        )

        result = await intent_service._handle_strategic_planning(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "planning_type_required"
        assert (
            "planning type" in result.message.lower() or "planning_type" in result.message.lower()
        )

    @pytest.mark.asyncio
    async def test_strategic_planning_missing_goal(self, intent_service):
        """Test validation when goal parameter is missing."""
        intent = Intent(
            original_message="create a sprint plan",
            category=IntentCategory.STRATEGY,
            action="strategic_planning",
            confidence=0.95,
            context={
                "planning_type": "sprint",
                # Missing goal
            },
        )

        result = await intent_service._handle_strategic_planning(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "goal_required"
        assert "goal" in result.message.lower()

    @pytest.mark.asyncio
    async def test_strategic_planning_unknown_planning_type(self, intent_service):
        """Test validation when planning_type is not supported."""
        intent = Intent(
            original_message="create invalid plan",
            category=IntentCategory.STRATEGY,
            action="strategic_planning",
            confidence=0.95,
            context={
                "planning_type": "invalid_type",
                "goal": "Do something",
            },
        )

        result = await intent_service._handle_strategic_planning(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "unsupported_planning_type"
        assert "unsupported" in result.message.lower() or "not supported" in result.message.lower()
        assert (
            "planning type" in result.message.lower() or "planning_type" in result.message.lower()
        )
        # Should list supported types
        assert "sprint" in result.message.lower()

    # =========================================================================
    # SUCCESS TESTS - SPRINT PLANNING
    # =========================================================================

    @pytest.mark.asyncio
    async def test_strategic_planning_sprint_success(self, intent_service):
        """Test successful sprint plan generation."""
        intent = Intent(
            original_message="create a sprint plan for authentication work",
            category=IntentCategory.STRATEGY,
            action="strategic_planning",
            confidence=0.95,
            context={
                "planning_type": "sprint",
                "goal": "Complete OAuth integration and user authentication",
                "timeframe": "2_weeks",
                "context": "Team of 3 developers, includes testing and deployment",
            },
        )

        result = await intent_service._handle_strategic_planning(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain plan in intent_data
        assert "plan" in result.intent_data
        plan = result.intent_data["plan"]

        # Verify plan structure
        assert "goal" in plan
        assert plan["goal"] == "Complete OAuth integration and user authentication"
        assert "duration" in plan or "timeframe" in plan
        assert "phases" in plan

        # Verify phases exist and have content
        assert len(plan["phases"]) > 0
        first_phase = plan["phases"][0]
        assert "phase" in first_phase
        assert "name" in first_phase
        assert "tasks" in first_phase
        assert len(first_phase["tasks"]) > 0

        # Verify tasks have structure
        first_task = first_phase["tasks"][0]
        assert "task" in first_task
        assert "priority" in first_task

        # Verify success criteria
        assert "success_criteria" in plan
        assert len(plan["success_criteria"]) > 0

        # Should have recommendations
        assert "recommendations" in result.intent_data
        assert len(result.intent_data["recommendations"]) > 0

        # Verify metadata
        assert result.intent_data["planning_type"] == "sprint"
        assert result.intent_data["goal"] == "Complete OAuth integration and user authentication"
        assert result.intent_data["timeframe"] == "2_weeks"

        # Should mention planning in message
        assert "plan" in result.message.lower() or "sprint" in result.message.lower()

    @pytest.mark.asyncio
    async def test_strategic_planning_sprint_no_placeholder(self, intent_service):
        """Test that sprint plans do not contain placeholder messages."""
        intent = Intent(
            original_message="create sprint plan",
            category=IntentCategory.STRATEGY,
            action="strategic_planning",
            confidence=0.95,
            context={
                "planning_type": "sprint",
                "goal": "Build user dashboard",
                "timeframe": "2_weeks",
            },
        )

        result = await intent_service._handle_strategic_planning(intent, workflow_id="test_wf")

        # If successful, should not contain placeholder messages
        if result.success:
            plan_str = str(result.intent_data.get("plan", ""))
            message = result.message.lower()

            # Should NOT contain these phrases
            assert "implementation in progress" not in message
            assert "implementation in progress" not in plan_str.lower()
            assert "placeholder" not in message
            assert "placeholder" not in plan_str.lower()
            assert "handler is ready" not in message
            assert "handler ready" not in message
            assert "planning ready" not in message

            # Success means requires_clarification should be False
            assert result.requires_clarification is False

    # =========================================================================
    # SUCCESS TESTS - FEATURE ROADMAP
    # =========================================================================

    @pytest.mark.asyncio
    async def test_strategic_planning_feature_roadmap_success(self, intent_service):
        """Test successful feature roadmap generation."""
        intent = Intent(
            original_message="plan a feature rollout",
            category=IntentCategory.STRATEGY,
            action="strategic_planning",
            confidence=0.95,
            context={
                "planning_type": "feature_roadmap",
                "goal": "Build comprehensive analytics dashboard",
                "timeframe": "3_months",
                "context": "Need user research before starting, deploy incrementally",
            },
        )

        result = await intent_service._handle_strategic_planning(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain plan
        assert "plan" in result.intent_data
        plan = result.intent_data["plan"]

        # Verify roadmap structure
        assert "goal" in plan
        assert "phases" in plan
        assert len(plan["phases"]) >= 2  # At least 2 phases for feature roadmap

        # Feature roadmaps should have milestones
        assert "milestones" in plan or len(plan["phases"]) > 2

        # Should have recommendations
        assert "recommendations" in result.intent_data
        assert len(result.intent_data["recommendations"]) > 0

        # Verify metadata
        assert result.intent_data["planning_type"] == "feature_roadmap"

    # =========================================================================
    # SUCCESS TESTS - ISSUE RESOLUTION
    # =========================================================================

    @pytest.mark.asyncio
    async def test_strategic_planning_issue_resolution_success(self, intent_service):
        """Test successful issue resolution plan generation."""
        intent = Intent(
            original_message="plan how to resolve database timeout issue",
            category=IntentCategory.STRATEGY,
            action="strategic_planning",
            confidence=0.95,
            context={
                "planning_type": "issue_resolution",
                "goal": "Database queries timing out during peak load",
                "context": "Affects 10% of users, happens 2-3 PM daily, query times >30s",
            },
        )

        result = await intent_service._handle_strategic_planning(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain plan
        assert "plan" in result.intent_data
        plan = result.intent_data["plan"]

        # Verify resolution plan structure
        assert "goal" in plan
        assert "phases" in plan
        assert len(plan["phases"]) > 0

        # Issue resolution should have investigation/analysis phases
        phase_names = [p["name"].lower() for p in plan["phases"]]
        # Should contain words related to investigation/analysis/solution
        all_phase_text = " ".join(phase_names)
        assert any(
            word in all_phase_text
            for word in ["investigation", "analysis", "solution", "implement", "verify"]
        )

        # Should have success criteria
        assert "success_criteria" in plan
        assert len(plan["success_criteria"]) > 0

        # Should have recommendations
        assert "recommendations" in result.intent_data

        # Verify metadata
        assert result.intent_data["planning_type"] == "issue_resolution"

    # =========================================================================
    # MULTIPLE PLANNING TYPES TEST
    # =========================================================================

    @pytest.mark.asyncio
    async def test_strategic_planning_all_types(self, intent_service):
        """Test that all planning types work correctly."""
        planning_configs = [
            {
                "planning_type": "sprint",
                "goal": "Complete authentication features",
                "timeframe": "2_weeks",
            },
            {
                "planning_type": "feature_roadmap",
                "goal": "Build analytics dashboard",
                "timeframe": "3_months",
            },
            {
                "planning_type": "issue_resolution",
                "goal": "Fix memory leak in worker process",
                "context": "Causing crashes every 6 hours",
            },
        ]

        for config in planning_configs:
            intent = Intent(
                original_message=f"create {config['planning_type']} plan",
                category=IntentCategory.STRATEGY,
                action="strategic_planning",
                confidence=0.95,
                context=config,
            )

            result = await intent_service._handle_strategic_planning(intent, workflow_id="test_wf")

            # Each type should succeed
            assert result.success is True, f"Failed for {config['planning_type']}"
            assert result.requires_clarification is False

            # Each should have a plan
            assert "plan" in result.intent_data
            assert "phases" in result.intent_data["plan"]
            assert len(result.intent_data["plan"]["phases"]) > 0

            # Each should have recommendations
            assert "recommendations" in result.intent_data
            assert len(result.intent_data["recommendations"]) > 0

            # Verify planning type in metadata
            assert result.intent_data["planning_type"] == config["planning_type"]


class TestHandlePrioritization:
    """Test suite for STRATEGY category - prioritization handler."""

    # =========================================================================
    # HANDLER EXISTENCE AND VALIDATION TESTS
    # =========================================================================

    def test_prioritization_handler_exists(self, intent_service):
        """Test that _handle_prioritization handler exists and is callable."""
        assert hasattr(intent_service, "_handle_prioritization")
        assert callable(intent_service._handle_prioritization)

    @pytest.mark.asyncio
    async def test_prioritization_missing_type(self, intent_service):
        """Test validation when prioritization_type parameter is missing."""
        intent = Intent(
            original_message="prioritize these items",
            category=IntentCategory.STRATEGY,
            action="prioritization",
            confidence=0.95,
            context={
                "items": ["Item 1", "Item 2"],
                # Missing prioritization_type
            },
        )

        result = await intent_service._handle_prioritization(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "prioritization_type_required"
        assert (
            "prioritization type" in result.message.lower()
            or "prioritization_type" in result.message.lower()
        )

    @pytest.mark.asyncio
    async def test_prioritization_missing_items(self, intent_service):
        """Test validation when items parameter is missing."""
        intent = Intent(
            original_message="prioritize issues",
            category=IntentCategory.STRATEGY,
            action="prioritization",
            confidence=0.95,
            context={
                "prioritization_type": "issues",
                # Missing items
            },
        )

        result = await intent_service._handle_prioritization(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "items_required"
        assert "items" in result.message.lower()

    @pytest.mark.asyncio
    async def test_prioritization_empty_items(self, intent_service):
        """Test validation when items list is empty."""
        intent = Intent(
            original_message="prioritize nothing",
            category=IntentCategory.STRATEGY,
            action="prioritization",
            confidence=0.95,
            context={
                "prioritization_type": "issues",
                "items": [],  # Empty list
            },
        )

        result = await intent_service._handle_prioritization(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "items_empty"
        assert "empty" in result.message.lower() or "no items" in result.message.lower()

    @pytest.mark.asyncio
    async def test_prioritization_unknown_type(self, intent_service):
        """Test validation when prioritization_type is not supported."""
        intent = Intent(
            original_message="prioritize with unknown method",
            category=IntentCategory.STRATEGY,
            action="prioritization",
            confidence=0.95,
            context={
                "prioritization_type": "invalid_type",
                "items": ["Item 1", "Item 2"],
            },
        )

        result = await intent_service._handle_prioritization(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "unsupported_prioritization_type"
        assert "unsupported" in result.message.lower() or "not supported" in result.message.lower()
        # Should list supported types
        assert "issues" in result.message.lower()

    # =========================================================================
    # SUCCESS TESTS - ISSUE PRIORITIZATION
    # =========================================================================

    @pytest.mark.asyncio
    async def test_prioritization_issues_success(self, intent_service):
        """Test successful issue prioritization with scores."""
        items = [
            {"title": "Critical security bug", "impact": 9, "urgency": 10, "effort": 2},
            {"title": "Nice feature request", "impact": 5, "urgency": 3, "effort": 8},
            {"title": "Important performance fix", "impact": 8, "urgency": 7, "effort": 3},
        ]

        intent = Intent(
            original_message="prioritize these issues",
            category=IntentCategory.STRATEGY,
            action="prioritization",
            confidence=0.95,
            context={
                "prioritization_type": "issues",
                "items": items,
            },
        )

        result = await intent_service._handle_prioritization(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain prioritized_items
        assert "prioritized_items" in result.intent_data
        prioritized = result.intent_data["prioritized_items"]

        # Should have 3 items
        assert len(prioritized) == 3

        # Each item should have structure
        first_item = prioritized[0]
        assert "rank" in first_item
        assert first_item["rank"] == 1
        assert "priority_score" in first_item
        assert "scores" in first_item
        assert "reasoning" in first_item

        # Scores should be present
        assert "impact" in first_item["scores"]
        assert "urgency" in first_item["scores"]
        assert "effort" in first_item["scores"]

        # Should have recommendations
        assert "recommendations" in result.intent_data
        assert len(result.intent_data["recommendations"]) > 0

        # Verify metadata
        assert result.intent_data["prioritization_type"] == "issues"
        assert result.intent_data["total_items"] == 3

    @pytest.mark.asyncio
    async def test_prioritization_ranking_order(self, intent_service):
        """Test that items are actually ranked correctly by priority score."""
        items = [
            {"title": "Low priority task", "impact": 2, "urgency": 2, "effort": 8},
            {"title": "High priority task", "impact": 10, "urgency": 10, "effort": 1},
            {"title": "Medium priority task", "impact": 5, "urgency": 5, "effort": 5},
        ]

        intent = Intent(
            original_message="prioritize these items",
            category=IntentCategory.STRATEGY,
            action="prioritization",
            confidence=0.95,
            context={
                "prioritization_type": "issues",
                "items": items,
            },
        )

        result = await intent_service._handle_prioritization(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        prioritized = result.intent_data["prioritized_items"]

        # High priority should be rank 1 (first in list)
        assert prioritized[0]["rank"] == 1
        assert "High priority task" in str(prioritized[0]["item"])

        # Low priority should be last
        assert prioritized[-1]["item"]["title"] == "Low priority task"
        assert prioritized[-1]["rank"] == 3

        # Priority scores should be in descending order
        scores = [item["priority_score"] for item in prioritized]
        assert scores == sorted(scores, reverse=True), "Items not sorted by priority score"

    # =========================================================================
    # SUCCESS TESTS - ALL TYPES
    # =========================================================================

    @pytest.mark.asyncio
    async def test_prioritization_all_types(self, intent_service):
        """Test that all prioritization types work correctly."""
        # Test issues type
        issues_intent = Intent(
            original_message="prioritize issues",
            category=IntentCategory.STRATEGY,
            action="prioritization",
            confidence=0.95,
            context={
                "prioritization_type": "issues",
                "items": [
                    {"title": "Bug 1", "impact": 8, "urgency": 7, "effort": 3},
                    {"title": "Bug 2", "impact": 5, "urgency": 5, "effort": 5},
                ],
            },
        )

        result = await intent_service._handle_prioritization(issues_intent, workflow_id="test_wf")

        assert result.success is True
        assert result.requires_clarification is False
        assert "prioritized_items" in result.intent_data
        assert len(result.intent_data["prioritized_items"]) == 2
        assert result.intent_data["prioritization_type"] == "issues"
