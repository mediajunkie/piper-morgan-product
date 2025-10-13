"""
Tests for Spatial → Workflow Factory Integration
Tests the integration between spatial events and workflow creation.

Following TDD principles: Write failing test → See it fail → Verify integration works → Make test pass
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import Workflow
from services.integrations.slack.event_handler import EventProcessingResult
from services.integrations.slack.slack_workflow_factory import (
    SlackWorkflowFactory,
    SlackWorkflowMapping,
    SpatialWorkflowContext,
)
from services.integrations.slack.spatial_agent import NavigationDecision, NavigationIntent
from services.integrations.slack.spatial_types import (
    AttentionLevel,
    EmotionalValence,
    SpatialCoordinates,
    SpatialEvent,
)
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import WorkflowType


class TestSpatialWorkflowFactory:
    """Test spatial events to workflow creation integration"""

    @pytest.fixture
    def workflow_factory(self):
        """Mock workflow factory"""
        return Mock(spec=WorkflowFactory)

    @pytest.fixture
    def slack_workflow_factory(self, workflow_factory):
        """Slack workflow factory instance"""
        return SlackWorkflowFactory(workflow_factory)

    @pytest.fixture
    def mock_event_result(self):
        """Mock event processing result"""
        result = Mock(spec=EventProcessingResult)
        result.success = True
        result.attention_level = AttentionLevel.HIGH
        result.emotional_valence = EmotionalValence.POSITIVE
        result.spatial_changes = [{"type": "attention_attracted", "room_id": "C123456"}]
        result.spatial_event = Mock(spec=SpatialEvent)
        result.spatial_event.event_type = "attention_attracted"
        result.spatial_event.coordinates = Mock(spec=SpatialCoordinates)
        result.spatial_event.coordinates.room_id = "C123456"
        result.spatial_event.coordinates.territory_id = "T123456"
        return result

    @pytest.fixture
    def mock_navigation_decision(self):
        """Mock navigation decision"""
        decision = Mock(spec=NavigationDecision)
        decision.intent = NavigationIntent.RESPOND
        decision.target_room = "C123456"
        decision.confidence = 0.9
        decision.reasoning = "High attention event requires response"
        return decision

    @pytest.fixture
    def spatial_context(self):
        """Spatial workflow context"""
        return SpatialWorkflowContext(
            room_id="C123456",
            territory_id="T123456",
            spatial_event_type="attention_attracted",
            attention_level="high",
            emotional_valence="positive",
            navigation_intent="respond",
        )

    async def test_high_attention_event_creates_task_workflow(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test that high attention events create task workflows"""
        # Arrange
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "wf-123"
        mock_workflow.context = {}
        mock_workflow.tasks = []
        slack_workflow_factory.workflow_factory.create_from_intent = AsyncMock(
            return_value=mock_workflow
        )

        # Act
        workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
            mock_event_result, mock_navigation_decision, spatial_context
        )

        # Assert
        assert workflow is not None
        assert workflow.id == "wf-123"
        assert "spatial_integration" in workflow.context

    async def test_medium_attention_event_creates_report_workflow(
        self, slack_workflow_factory, workflow_factory
    ):
        """Test that medium attention events create report workflows"""
        # Arrange
        event_result = Mock(spec=EventProcessingResult)
        event_result.success = True
        event_result.attention_level = AttentionLevel.MEDIUM
        event_result.emotional_valence = EmotionalValence.NEUTRAL
        event_result.spatial_event = Mock()
        event_result.spatial_event.event_type = "message_placed"

        navigation_decision = Mock(spec=NavigationDecision)
        navigation_decision.intent = NavigationIntent.MONITOR
        navigation_decision.confidence = 0.7

        context = SpatialWorkflowContext(
            room_id="C123456",
            territory_id="T123456",
            spatial_event_type="message_placed",
            attention_level="medium",
            emotional_valence="neutral",
            navigation_intent="monitor",
        )

        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "wf-report"
        mock_workflow.context = {}
        workflow_factory.create_from_intent = AsyncMock(return_value=mock_workflow)

        # Act
        workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
            event_result, navigation_decision, context
        )

        # Assert
        assert workflow is not None
        assert workflow.id == "wf-report"

    async def test_emotional_event_creates_feedback_workflow(
        self, slack_workflow_factory, workflow_factory
    ):
        """Test that emotional events create feedback analysis workflows"""
        # Arrange
        event_result = Mock(spec=EventProcessingResult)
        event_result.success = True
        event_result.attention_level = AttentionLevel.MEDIUM
        event_result.emotional_valence = EmotionalValence.NEGATIVE
        event_result.spatial_event = Mock()
        event_result.spatial_event.event_type = "emotional_marker_updated"

        navigation_decision = Mock(spec=NavigationDecision)
        navigation_decision.intent = NavigationIntent.INVESTIGATE
        navigation_decision.confidence = 0.8

        context = SpatialWorkflowContext(
            room_id="C123456",
            territory_id="T123456",
            spatial_event_type="emotional_marker_updated",
            attention_level="medium",
            emotional_valence="negative",
            navigation_intent="investigate",
        )

        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "wf-feedback"
        mock_workflow.context = {}
        workflow_factory.create_from_intent = AsyncMock(return_value=mock_workflow)

        # Act
        workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
            event_result, navigation_decision, context
        )

        # Assert
        assert workflow is not None
        assert workflow.id == "wf-feedback"

    def test_new_room_event_creates_pattern_workflow(
        self, slack_workflow_factory, workflow_factory
    ):
        """Test that new room events create pattern learning workflows"""
        # Arrange
        event_result = Mock(spec=EventProcessingResult)
        event_result.success = True
        event_result.attention_level = AttentionLevel.LOW
        event_result.emotional_valence = EmotionalValence.NEUTRAL
        event_result.spatial_event = Mock()
        event_result.spatial_event.event_type = "room_created"

        navigation_decision = Mock(spec=NavigationDecision)
        navigation_decision.intent = NavigationIntent.EXPLORE
        navigation_decision.confidence = 0.8

        context = SpatialWorkflowContext(
            room_id="C789012",
            territory_id="T123456",
            spatial_event_type="room_created",
            attention_level="low",
            emotional_valence="neutral",
            navigation_intent="explore",
        )

        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "wf-pattern"
        mock_workflow.context = {}
        workflow_factory.create_from_intent = AsyncMock(return_value=mock_workflow)

        # Act
        workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
            event_result, navigation_decision, context
        )

        # Assert
        assert workflow is not None
        assert workflow.id == "wf-pattern"

    def test_no_mapping_returns_none(self, slack_workflow_factory, workflow_factory):
        """Test that events without mappings return None"""
        # Arrange
        event_result = Mock(spec=EventProcessingResult)
        event_result.success = True
        event_result.attention_level = AttentionLevel.LOW
        event_result.emotional_valence = EmotionalValence.NEUTRAL
        event_result.spatial_event = Mock()
        event_result.spatial_event.event_type = "unknown_event_type"

        navigation_decision = Mock(spec=NavigationDecision)
        navigation_decision.intent = NavigationIntent.MONITOR
        navigation_decision.confidence = 0.3

        context = SpatialWorkflowContext(
            room_id="C123456",
            territory_id="T123456",
            spatial_event_type="unknown_event_type",
            attention_level="low",
            emotional_valence="neutral",
            navigation_intent="monitor",
        )

        # Act
        workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
            event_result, navigation_decision, context
        )

        # Assert
        assert workflow is None

    def test_workflow_context_enrichment(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test that workflows are enriched with spatial context"""
        # Arrange
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "wf-123"
        mock_workflow.context = {}
        mock_workflow.tasks = [Mock(), Mock()]
        slack_workflow_factory.workflow_factory.create_from_intent = AsyncMock(
            return_value=mock_workflow
        )

        # Act
        workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
            mock_event_result, mock_navigation_decision, spatial_context
        )

        # Assert
        assert "spatial_integration" in workflow.context
        spatial_integration = workflow.context["spatial_integration"]
        assert spatial_integration["room_id"] == "C123456"
        assert spatial_integration["territory_id"] == "T123456"
        assert spatial_integration["spatial_event_type"] == "attention_attracted"
        assert spatial_integration["attention_level"] == "high"
        assert spatial_integration["emotional_valence"] == "positive"
        assert spatial_integration["navigation_intent"] == "respond"

        # Check tasks are enriched
        for task in workflow.tasks:
            assert task.result is not None
            assert "spatial_context" in task.result
            assert task.result["spatial_context"]["room_id"] == "C123456"

    def test_mapping_score_calculation(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test that mapping scores are calculated correctly"""
        # Arrange
        mapping = SlackWorkflowMapping(
            spatial_event_type="attention_attracted",
            attention_level="high",
            navigation_intent="respond",
            workflow_type=WorkflowType.CREATE_TASK,
            priority=1,
            confidence_threshold=0.8,
        )

        # Act
        score = slack_workflow_factory._calculate_mapping_score(
            mapping, mock_event_result, mock_navigation_decision, spatial_context
        )

        # Assert
        assert score > 0.0
        assert score <= 1.0
        assert score >= mapping.confidence_threshold

    def test_intent_creation_from_spatial_event(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test that intents are created correctly from spatial events"""
        # Arrange
        mapping = SlackWorkflowMapping(
            spatial_event_type="attention_attracted",
            attention_level="high",
            navigation_intent="respond",
            workflow_type=WorkflowType.CREATE_TASK,
            priority=1,
            confidence_threshold=0.8,
        )

        # Act
        intent = slack_workflow_factory._create_intent_from_spatial_event(
            mock_event_result, mock_navigation_decision, spatial_context, mapping
        )

        # Assert
        assert intent is not None
        assert intent.action == "create_task"
        assert intent.confidence == 0.9
        assert "spatial_context" in intent.context
        assert intent.context["spatial_context"]["room_id"] == "C123456"
        assert intent.context["spatial_context"]["territory_id"] == "T123456"

    def test_workflow_mapping_registry(self, slack_workflow_factory):
        """Test that workflow mappings are properly registered"""
        # Arrange & Act
        mappings = slack_workflow_factory.get_workflow_mappings()

        # Assert
        assert len(mappings) > 0
        assert all(isinstance(mapping, SlackWorkflowMapping) for mapping in mappings)

        # Check for specific mappings
        attention_mappings = [m for m in mappings if m.spatial_event_type == "attention_attracted"]
        assert len(attention_mappings) > 0

        message_mappings = [m for m in mappings if m.spatial_event_type == "message_placed"]
        assert len(message_mappings) > 0

    def test_workflow_factory_error_handling(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test that workflow factory errors are handled gracefully"""
        # Arrange
        slack_workflow_factory.workflow_factory.create_from_intent = AsyncMock(
            side_effect=Exception("Workflow creation failed")
        )

        # Act
        workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
            mock_event_result, mock_navigation_decision, spatial_context
        )

        # Assert
        assert workflow is None

    def test_spatial_workflow_statistics(self, slack_workflow_factory):
        """Test that spatial workflow statistics are generated correctly"""
        # Act
        stats = slack_workflow_factory.get_spatial_workflow_stats()

        # Assert
        assert "total_mappings" in stats
        assert "workflow_types" in stats
        assert "spatial_event_types" in stats
        assert "attention_levels" in stats
        assert "navigation_intents" in stats
        assert "priority_distribution" in stats

        assert stats["total_mappings"] > 0
        assert len(stats["workflow_types"]) > 0
        assert len(stats["spatial_event_types"]) > 0
