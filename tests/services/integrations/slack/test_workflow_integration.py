"""
Tests for Slack Workflow Integration
Tests integration between spatial events and Piper Morgan workflows.
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import Intent, Workflow
from services.integrations.slack.event_handler import EventProcessingResult
from services.integrations.slack.slack_workflow_factory import (
    SlackWorkflowFactory,
    SlackWorkflowMapping,
    SpatialWorkflowContext,
)
from services.integrations.slack.spatial_agent import NavigationDecision, NavigationIntent
from services.integrations.slack.spatial_intent_classifier import (
    IntentClassificationResult,
    SpatialIntentClassifier,
    SpatialIntentPattern,
)
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import IntentCategory, WorkflowType


class TestSlackWorkflowFactory:
    """Test Slack workflow factory integration"""

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
        result.attention_level.value = "high"
        result.emotional_valence.value = "positive"
        result.spatial_changes = [{"type": "attention_attracted", "room_id": "C123456"}]
        result.spatial_event = Mock()
        result.spatial_event.event_type = "attention_attracted"
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

    def test_create_spatial_mappings(self, slack_workflow_factory):
        """Test creation of spatial workflow mappings"""
        mappings = slack_workflow_factory.spatial_mappings

        assert len(mappings) > 0
        assert all(isinstance(mapping, SlackWorkflowMapping) for mapping in mappings)

        # Check for specific mappings
        attention_mappings = [m for m in mappings if m.spatial_event_type == "attention_attracted"]
        assert len(attention_mappings) > 0

        message_mappings = [m for m in mappings if m.spatial_event_type == "message_placed"]
        assert len(message_mappings) > 0

    @patch("services.integrations.slack.slack_workflow_factory.WorkflowFactory")
    async def test_create_workflow_from_spatial_event(
        self,
        mock_workflow_factory_class,
        workflow_factory,
        mock_event_result,
        mock_navigation_decision,
        spatial_context,
    ):
        """Test creating workflow from spatial event"""
        mock_workflow_factory_class.return_value = workflow_factory

        # Mock workflow creation
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "wf-123"
        mock_workflow.context = {}
        mock_workflow.tasks = []
        workflow_factory.create_from_intent = AsyncMock(return_value=mock_workflow)

        slack_workflow_factory = SlackWorkflowFactory(workflow_factory)

        result = await slack_workflow_factory.create_workflow_from_spatial_event(
            mock_event_result, mock_navigation_decision, spatial_context
        )

        assert result is not None
        assert result.id == "wf-123"
        assert "spatial_integration" in result.context

    def test_find_workflow_mapping(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test finding appropriate workflow mapping"""
        mapping = slack_workflow_factory._find_workflow_mapping(
            mock_event_result, mock_navigation_decision, spatial_context
        )

        assert mapping is not None
        assert mapping.spatial_event_type == "attention_attracted"
        assert mapping.attention_level == "high"
        assert mapping.navigation_intent == "respond"

    def test_calculate_mapping_score(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test calculating mapping score"""
        mapping = SlackWorkflowMapping(
            spatial_event_type="attention_attracted",
            attention_level="high",
            navigation_intent="respond",
            workflow_type=WorkflowType.CREATE_TASK,
            priority=1,
            confidence_threshold=0.8,
        )

        score = slack_workflow_factory._calculate_mapping_score(
            mapping, mock_event_result, mock_navigation_decision, spatial_context
        )

        assert score > 0.0
        assert score <= 1.0

    def test_create_intent_from_spatial_event(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test creating intent from spatial event"""
        mapping = SlackWorkflowMapping(
            spatial_event_type="attention_attracted",
            attention_level="high",
            navigation_intent="respond",
            workflow_type=WorkflowType.CREATE_TASK,
            priority=1,
            confidence_threshold=0.8,
        )

        intent = slack_workflow_factory._create_intent_from_spatial_event(
            mock_event_result, mock_navigation_decision, spatial_context, mapping
        )

        assert intent is not None
        assert intent.category == IntentCategory.EXECUTION
        assert intent.action == "create_task"
        assert "spatial_context" in intent.context

    def test_get_workflow_mappings(self, slack_workflow_factory):
        """Test getting workflow mappings"""
        mappings = slack_workflow_factory.get_workflow_mappings()

        assert len(mappings) > 0
        assert all(isinstance(mapping, SlackWorkflowMapping) for mapping in mappings)

    def test_get_spatial_workflow_stats(self, slack_workflow_factory):
        """Test getting spatial workflow statistics"""
        stats = slack_workflow_factory.get_spatial_workflow_stats()

        assert "total_mappings" in stats
        assert "workflow_types" in stats
        assert "spatial_event_types" in stats
        assert "attention_levels" in stats
        assert "navigation_intents" in stats
        assert "priority_distribution" in stats

        assert stats["total_mappings"] > 0
        assert len(stats["workflow_types"]) > 0


class TestSpatialIntentClassifier:
    """Test spatial intent classifier"""

    @pytest.fixture
    def intent_classifier(self):
        """Spatial intent classifier instance"""
        return SpatialIntentClassifier()

    @pytest.fixture
    def mock_event_result(self):
        """Mock event processing result"""
        result = Mock(spec=EventProcessingResult)
        result.success = True
        result.attention_level.value = "high"
        result.emotional_valence.value = "positive"
        result.spatial_changes = [
            {"type": "attention_attracted", "content": "I need help with this bug"}
        ]
        result.spatial_event = Mock()
        result.spatial_event.event_type = "attention_attracted"
        return result

    @pytest.fixture
    def mock_navigation_decision(self):
        """Mock navigation decision"""
        decision = Mock(spec=NavigationDecision)
        decision.intent = NavigationIntent.RESPOND
        decision.confidence = 0.9
        return decision

    def test_create_intent_patterns(self, intent_classifier):
        """Test creation of intent patterns"""
        patterns = intent_classifier.intent_patterns

        assert len(patterns) > 0
        assert all(isinstance(pattern, SpatialIntentPattern) for pattern in patterns)

        # Check for specific pattern types
        help_patterns = [p for p in patterns if "help" in p.keywords]
        assert len(help_patterns) > 0

        bug_patterns = [p for p in patterns if "bug" in p.keywords]
        assert len(bug_patterns) > 0

    def test_classify_spatial_event_help_request(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test classifying help request spatial event"""
        result = intent_classifier.classify_spatial_event(
            mock_event_result, mock_navigation_decision, "I need help with this bug"
        )

        assert result is not None
        assert result.intent is not None
        assert result.confidence > 0.0
        assert (
            "help" in result.classification_reason.lower()
            or "bug" in result.classification_reason.lower()
        )

    def test_classify_spatial_event_bug_report(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test classifying bug report spatial event"""
        result = intent_classifier.classify_spatial_event(
            mock_event_result,
            mock_navigation_decision,
            "There's a critical bug in the login system",
        )

        assert result is not None
        assert result.intent is not None
        assert result.confidence > 0.0
        assert result.intent.action == "create_ticket"

    def test_classify_spatial_event_feature_request(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test classifying feature request spatial event"""
        result = intent_classifier.classify_spatial_event(
            mock_event_result,
            mock_navigation_decision,
            "We should add a new feature for user management",
        )

        assert result is not None
        assert result.intent is not None
        assert result.confidence > 0.0
        assert result.intent.action == "create_feature"

    def test_classify_spatial_event_status_update(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test classifying status update spatial event"""
        result = intent_classifier.classify_spatial_event(
            mock_event_result, mock_navigation_decision, "Status update: Project is 75% complete"
        )

        assert result is not None
        assert result.intent is not None
        assert result.confidence > 0.0
        assert result.intent.action == "generate_report"

    def test_classify_spatial_event_unknown(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test classifying unknown spatial event"""
        result = intent_classifier.classify_spatial_event(
            mock_event_result, mock_navigation_decision, "Random message without clear intent"
        )

        assert result is not None
        assert result.intent is not None
        assert result.intent.category == IntentCategory.UNKNOWN
        assert result.confidence == 0.3

    def test_extract_text_content_from_message(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test extracting text content from message"""
        text = intent_classifier._extract_text_content(mock_event_result, "Hello world")

        assert text == "hello world"

    def test_extract_text_content_from_spatial_changes(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test extracting text content from spatial changes"""
        text = intent_classifier._extract_text_content(mock_event_result, "")

        assert "help" in text.lower() and "bug" in text.lower()

    def test_find_best_pattern(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test finding best pattern for text content"""
        pattern = intent_classifier._find_best_pattern(
            "I need help with this bug", mock_event_result, mock_navigation_decision
        )

        assert pattern is not None
        assert "help" in pattern.keywords or "bug" in pattern.keywords

    def test_calculate_pattern_score(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test calculating pattern score"""
        pattern = SpatialIntentPattern(
            pattern=r"help|bug",
            intent_category=IntentCategory.EXECUTION,
            action="create_task",
            confidence=0.8,
            keywords=["help", "bug"],
        )

        score = intent_classifier._calculate_pattern_score(
            pattern, "I need help with this bug", mock_event_result, mock_navigation_decision
        )

        assert score > 0.0
        assert score <= 1.0

    def test_create_intent_from_pattern(
        self, intent_classifier, mock_event_result, mock_navigation_decision
    ):
        """Test creating intent from pattern"""
        pattern = SpatialIntentPattern(
            pattern=r"help",
            intent_category=IntentCategory.EXECUTION,
            action="create_task",
            confidence=0.8,
            keywords=["help"],
        )

        intent = intent_classifier._create_intent_from_pattern(
            pattern, mock_event_result, mock_navigation_decision, "I need help"
        )

        assert intent is not None
        assert intent.category == IntentCategory.EXECUTION
        assert intent.action == "create_task"
        assert intent.confidence == 0.8
        assert "spatial_event_type" in intent.context

    def test_get_intent_patterns(self, intent_classifier):
        """Test getting intent patterns"""
        patterns = intent_classifier.get_intent_patterns()

        assert len(patterns) > 0
        assert all(isinstance(pattern, SpatialIntentPattern) for pattern in patterns)

    def test_get_classification_stats(self, intent_classifier):
        """Test getting classification statistics"""
        stats = intent_classifier.get_classification_stats()

        assert "total_patterns" in stats
        assert "intent_categories" in stats
        assert "actions" in stats
        assert "confidence_distribution" in stats
        assert "pattern_types" in stats

        assert stats["total_patterns"] > 0
        assert len(stats["intent_categories"]) > 0
        assert len(stats["actions"]) > 0

    def test_classify_batch(self, intent_classifier, mock_event_result, mock_navigation_decision):
        """Test batch classification"""
        events = [
            (mock_event_result, mock_navigation_decision, "I need help"),
            (mock_event_result, mock_navigation_decision, "There's a bug"),
            (mock_event_result, mock_navigation_decision, "Status update"),
        ]

        results = intent_classifier.classify_batch(events)

        assert len(results) == 3
        assert all(isinstance(result, IntentClassificationResult) for result in results)
        assert all(result.intent is not None for result in results)


class TestWorkflowIntegration:
    """Integration tests for workflow integration"""

    @pytest.fixture
    def workflow_factory(self):
        """Mock workflow factory"""
        return Mock(spec=WorkflowFactory)

    @pytest.fixture
    def slack_workflow_factory(self, workflow_factory):
        """Slack workflow factory instance"""
        return SlackWorkflowFactory(workflow_factory)

    @pytest.fixture
    def intent_classifier(self):
        """Spatial intent classifier instance"""
        return SpatialIntentClassifier()

    @pytest.fixture
    def mock_event_result(self):
        """Mock event processing result"""
        result = Mock(spec=EventProcessingResult)
        result.success = True
        result.attention_level.value = "high"
        result.emotional_valence.value = "positive"
        result.spatial_changes = [
            {"type": "attention_attracted", "content": "I need help with this bug"}
        ]
        result.spatial_event = Mock()
        result.spatial_event.event_type = "attention_attracted"
        return result

    @pytest.fixture
    def mock_navigation_decision(self):
        """Mock navigation decision"""
        decision = Mock(spec=NavigationDecision)
        decision.intent = NavigationIntent.RESPOND
        decision.target_room = "C123456"
        decision.confidence = 0.9
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

    async def test_end_to_end_workflow_creation(
        self,
        slack_workflow_factory,
        intent_classifier,
        mock_event_result,
        mock_navigation_decision,
        spatial_context,
    ):
        """Test end-to-end workflow creation from spatial event"""
        # Mock workflow creation
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "wf-123"
        mock_workflow.context = {}
        mock_workflow.tasks = []
        slack_workflow_factory.workflow_factory.create_from_intent = AsyncMock(
            return_value=mock_workflow
        )

        # Classify intent
        classification_result = intent_classifier.classify_spatial_event(
            mock_event_result, mock_navigation_decision, "I need help with this bug"
        )

        # Create workflow
        workflow = await slack_workflow_factory.create_workflow_from_spatial_event(
            mock_event_result, mock_navigation_decision, spatial_context
        )

        # Verify results
        assert classification_result is not None
        assert classification_result.intent is not None
        assert workflow is not None
        assert workflow.id == "wf-123"
        assert "spatial_integration" in workflow.context

    def test_spatial_context_enrichment(
        self, slack_workflow_factory, mock_event_result, mock_navigation_decision, spatial_context
    ):
        """Test enrichment of workflow with spatial context"""
        # Create mock workflow
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.context = {}
        mock_workflow.tasks = [Mock(), Mock()]  # Two tasks

        # Enrich workflow
        slack_workflow_factory._enrich_workflow_with_spatial_context(mock_workflow, spatial_context)

        # Verify spatial context was added
        assert "spatial_integration" in mock_workflow.context
        spatial_integration = mock_workflow.context["spatial_integration"]
        assert spatial_integration["room_id"] == "C123456"
        assert spatial_integration["territory_id"] == "T123456"
        assert spatial_integration["spatial_event_type"] == "attention_attracted"

        # Verify tasks were enriched
        for task in mock_workflow.tasks:
            assert task.result is not None
            assert "spatial_context" in task.result
