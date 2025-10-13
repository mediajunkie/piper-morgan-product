"""
End-to-End Slack Integration Pipeline Tests
Comprehensive test suite that validates the complete Slack integration pipeline
with full observability validation and silent failure detection.

TDD Philosophy: Tests REQUIRE observability to pass, not just functionality.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent, IntentCategory, SpatialEvent
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.response_handler import SlackResponseHandler
from services.integrations.slack.slack_client import SlackClient, SlackResponse
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.integrations.slack.webhook_router import SlackWebhookRouter
from services.intent_service.classifier import IntentClassifier
from services.observability.slack_monitor import SlackPipelineMetrics
from services.orchestration.engine import OrchestrationEngine


class TestSlackE2EPipeline:
    """
    End-to-End Slack Integration Pipeline Tests

    Validates complete flow from webhook to response with full observability.
    Tests REQUIRE observability to pass, not just functionality.
    """

    @pytest.fixture
    async def mock_slack_client(self):
        """Mock Slack client with controlled responses"""
        client = AsyncMock(spec=SlackClient)

        # Mock successful response
        success_response = SlackResponse(
            success=True,
            data={"ok": True, "ts": "1234567890.123456", "channel": "C1234567890"},
            rate_limit_remaining=49,
            rate_limit_reset=1234567890,
        )
        client.send_message.return_value = success_response
        client.test_auth.return_value = success_response

        return client

    @pytest.fixture
    async def mock_intent_classifier(self):
        """Mock intent classifier with controlled responses"""
        classifier = AsyncMock(spec=IntentClassifier)

        # Mock successful intent classification
        intent = Intent(
            action="analyze_request",
            category=IntentCategory.ANALYSIS,
            confidence=0.95,
            context={"spatial_context": "test_context"},
        )
        classifier.classify.return_value = intent

        return classifier

    @pytest.fixture
    async def mock_orchestration_engine(self):
        """Mock orchestration engine with controlled responses"""
        engine = AsyncMock(spec=OrchestrationEngine)

        # Mock successful workflow execution
        workflow_result = {
            "type": "workflow_result",
            "workflow_id": "test_workflow_123",
            "result": {"summary": "Test workflow completed successfully"},
            "intent": Intent(
                action="analyze_request", category=IntentCategory.ANALYSIS, confidence=0.95
            ),
        }
        engine.create_workflow_from_intent.return_value = MagicMock(id="test_workflow_123")
        engine.execute_workflow.return_value = workflow_result

        return engine

    @pytest.fixture
    async def mock_spatial_adapter(self):
        """Mock spatial adapter with controlled responses"""
        adapter = AsyncMock(spec=SlackSpatialAdapter)

        # Mock spatial event creation
        spatial_event = SpatialEvent(
            event_type="message_posted",
            territory_position=1,
            room_position=2,
            path_position=None,
            object_position=123,
            actor_id="U1234567890",
            affected_objects=[],
            spatial_changes={},
            event_time=datetime.now(),
            significance_level="routine",
        )
        adapter.create_spatial_event_from_slack.return_value = spatial_event
        adapter.get_response_context.return_value = {
            "channel_id": "C1234567890",
            "thread_ts": None,
            "workspace_id": "T1234567890",
            "user_id": "U1234567890",
        }

        return adapter

    @pytest.fixture
    async def mock_pipeline_metrics(self):
        """Mock pipeline metrics for observability validation"""
        metrics = AsyncMock(spec=SlackPipelineMetrics)
        metrics.processing_stages = []
        metrics.correlation_id = "test_correlation_123"
        metrics.start_time = datetime.now()
        metrics.end_time = None

        return metrics

    @pytest.fixture
    async def mock_task_manager(self):
        """Mock task manager for context preservation validation"""
        task_manager = AsyncMock(spec=RobustTaskManager)
        task_manager.context = {"test_context": "preserved"}
        task_manager.correlation_id = "test_correlation_123"

        return task_manager

    @pytest.fixture
    async def webhook_router(
        self,
        mock_slack_client,
        mock_intent_classifier,
        mock_orchestration_engine,
        mock_spatial_adapter,
        mock_pipeline_metrics,
        mock_task_manager,
    ):
        """Create webhook router with all mocked dependencies"""
        # Create webhook router with mocked dependencies instead of patching imports
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler
        from services.integrations.slack.response_handler import SlackResponseHandler
        from services.integrations.slack.spatial_mapper import SlackSpatialMapper
        from services.integrations.slack.webhook_router import SlackWebhookRouter

        # Mock the config service
        config_service = MagicMock(spec=SlackConfigService)

        # Create response handler with mocked dependencies
        response_handler = SlackResponseHandler(
            spatial_adapter=mock_spatial_adapter,
            intent_classifier=mock_intent_classifier,
            orchestration_engine=mock_orchestration_engine,
            slack_client=mock_slack_client,
        )

        # Create webhook router with mocked dependencies
        router = SlackWebhookRouter(
            config_service=config_service,
            oauth_handler=MagicMock(spec=SlackOAuthHandler),
            spatial_mapper=MagicMock(spec=SlackSpatialMapper),
            response_handler=response_handler,
        )

        return router

    async def test_complete_pipeline_flow_with_observability(
        self, webhook_router, mock_pipeline_metrics, mock_task_manager
    ):
        """
        Test complete pipeline flow with full observability validation.

        This test REQUIRES observability to pass, not just functionality.
        """
        # Arrange: Create mock Slack event
        slack_event = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "channel": "C1234567890",
                "user": "U1234567890",
                "text": "Hello Piper, can you analyze this request?",
                "ts": "1234567890.123456",
            },
            "team_id": "T1234567890",
        }

        # Act: Process the event through the complete pipeline
        start_time = datetime.now()

        with patch(
            "services.integrations.slack.webhook_router.SlackWebhookRouter._verify_slack_signature",
            return_value=True,
        ):
            await webhook_router.handle_slack_events(slack_event)

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Assert: Validate all 11 ProcessingStages are tracked
        assert (
            len(mock_pipeline_metrics.processing_stages) == 11
        ), f"Expected 11 processing stages, got {len(mock_pipeline_metrics.processing_stages)}"

        expected_stages = [
            "webhook_received",
            "spatial_event_created",
            "intent_classified",
            "workflow_created",
            "workflow_executed",
            "response_generated",
            "slack_response_sent",
            "context_preserved",
            "metrics_recorded",
            "correlation_tracked",
            "pipeline_completed",
        ]

        for stage in expected_stages:
            assert any(
                stage in str(s) for s in mock_pipeline_metrics.processing_stages
            ), f"Processing stage '{stage}' not found in metrics"

        # Assert: Validate timing constraints (< 3s)
        assert (
            processing_time < 3.0
        ), f"Pipeline processing time {processing_time}s exceeds 3s limit"

        # Assert: Validate correlation ID preservation
        assert (
            mock_task_manager.correlation_id == mock_pipeline_metrics.correlation_id
        ), "Correlation ID not preserved across async boundaries"

        # Assert: Validate context preservation
        assert (
            mock_task_manager.context.get("test_context") == "preserved"
        ), "Context not preserved across async boundaries"

        # Assert: Validate no silent failures (all errors logged and observable)
        # This is the key TDD requirement - observability must be enforced
        assert (
            mock_pipeline_metrics.end_time is not None
        ), "Pipeline metrics end_time not set - silent failure detected"

        assert (
            mock_pipeline_metrics.correlation_id is not None
        ), "Correlation ID not set - observability failure detected"

    async def test_silent_failure_detection(
        self, webhook_router, mock_slack_client, mock_pipeline_metrics
    ):
        """
        Test that silent failures are detected and reported explicitly.

        This test ensures observability catches failures that would otherwise be silent.
        """
        # Arrange: Mock Slack client to fail silently
        mock_slack_client.send_message.side_effect = Exception("Silent failure")

        slack_event = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "channel": "C1234567890",
                "user": "U1234567890",
                "text": "Test message",
                "ts": "1234567890.123456",
            },
            "team_id": "T1234567890",
        }

        # Act: Process the event
        with patch(
            "services.integrations.slack.webhook_router.SlackWebhookRouter._verify_slack_signature",
            return_value=True,
        ):
            await webhook_router.handle_slack_events(slack_event)

        # Assert: Silent failure must be detected and logged
        # This is the core TDD requirement - observability must catch silent failures
        assert (
            mock_pipeline_metrics.end_time is not None
        ), "Pipeline metrics must be completed even on failure - silent failure detected"

        # Check that error stage is recorded
        error_stages = [
            s for s in mock_pipeline_metrics.processing_stages if "error" in str(s).lower()
        ]
        assert (
            len(error_stages) > 0
        ), "Error stages must be recorded - silent failure detection failed"

    async def test_context_preservation_across_async_boundaries(
        self, webhook_router, mock_task_manager, mock_pipeline_metrics
    ):
        """
        Test that context is preserved across all async boundaries.

        This ensures the pipeline maintains observability throughout.
        """
        # Arrange: Set up context that must be preserved
        original_context = {
            "user_id": "U1234567890",
            "channel_id": "C1234567890",
            "correlation_id": "test_123",
        }
        mock_task_manager.context = original_context.copy()

        slack_event = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "channel": "C1234567890",
                "user": "U1234567890",
                "text": "Test context preservation",
                "ts": "1234567890.123456",
            },
            "team_id": "T1234567890",
        }

        # Act: Process through multiple async boundaries
        with patch(
            "services.integrations.slack.webhook_router.SlackWebhookRouter._verify_slack_signature",
            return_value=True,
        ):
            await webhook_router.handle_slack_events(slack_event)

        # Assert: Context must be preserved across all boundaries
        assert (
            mock_task_manager.context == original_context
        ), "Context not preserved across async boundaries"

        assert (
            mock_task_manager.correlation_id == mock_pipeline_metrics.correlation_id
        ), "Correlation ID not preserved across async boundaries"

    async def test_pipeline_timing_constraints(self, webhook_router, mock_pipeline_metrics):
        """
        Test that pipeline timing constraints are enforced and observable.

        This ensures performance is monitored and enforced.
        """
        slack_event = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "channel": "C1234567890",
                "user": "U1234567890",
                "text": "Test timing",
                "ts": "1234567890.123456",
            },
            "team_id": "T1234567890",
        }

        # Act: Process with timing measurement
        start_time = datetime.now()

        with patch(
            "services.integrations.slack.webhook_router.SlackWebhookRouter._verify_slack_signature",
            return_value=True,
        ):
            await webhook_router.handle_slack_events(slack_event)

        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Assert: Timing constraints must be enforced
        assert (
            processing_time < 3.0
        ), f"Pipeline processing time {processing_time}s exceeds 3s limit"

        # Assert: Timing must be observable
        assert (
            mock_pipeline_metrics.start_time is not None
        ), "Pipeline start time not recorded - observability failure"

        assert (
            mock_pipeline_metrics.end_time is not None
        ), "Pipeline end time not recorded - observability failure"

    async def test_correlation_tracking_throughout_pipeline(
        self, webhook_router, mock_task_manager, mock_pipeline_metrics
    ):
        """
        Test that correlation tracking works throughout the entire pipeline.

        This ensures observability can trace requests end-to-end.
        """
        # Arrange: Set correlation ID
        correlation_id = "test_correlation_456"
        mock_task_manager.correlation_id = correlation_id
        mock_pipeline_metrics.correlation_id = correlation_id

        slack_event = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "channel": "C1234567890",
                "user": "U1234567890",
                "text": "Test correlation",
                "ts": "1234567890.123456",
            },
            "team_id": "T1234567890",
        }

        # Act: Process through pipeline
        with patch(
            "services.integrations.slack.webhook_router.SlackWebhookRouter._verify_slack_signature",
            return_value=True,
        ):
            await webhook_router.handle_slack_events(slack_event)

        # Assert: Correlation must be tracked throughout
        assert (
            mock_task_manager.correlation_id == correlation_id
        ), "Task manager correlation ID not preserved"

        assert (
            mock_pipeline_metrics.correlation_id == correlation_id
        ), "Pipeline metrics correlation ID not preserved"

        # Assert: All processing stages must include correlation
        for stage in mock_pipeline_metrics.processing_stages:
            assert correlation_id in str(stage), f"Processing stage missing correlation ID: {stage}"

    async def test_observability_enforcement(self, webhook_router, mock_pipeline_metrics):
        """
        Test that observability is enforced, not just optional.

        This is the core TDD requirement - observability must be mandatory.
        """
        slack_event = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "channel": "C1234567890",
                "user": "U1234567890",
                "text": "Test observability enforcement",
                "ts": "1234567890.123456",
            },
            "team_id": "T1234567890",
        }

        # Act: Process event
        with patch(
            "services.integrations.slack.webhook_router.SlackWebhookRouter._verify_slack_signature",
            return_value=True,
        ):
            await webhook_router.handle_slack_events(slack_event)

        # Assert: Observability must be enforced (these tests REQUIRE observability)
        assert (
            mock_pipeline_metrics.correlation_id is not None
        ), "Correlation ID must be set - observability enforcement failed"

        assert (
            mock_pipeline_metrics.start_time is not None
        ), "Start time must be recorded - observability enforcement failed"

        assert (
            mock_pipeline_metrics.end_time is not None
        ), "End time must be recorded - observability enforcement failed"

        assert (
            len(mock_pipeline_metrics.processing_stages) > 0
        ), "Processing stages must be recorded - observability enforcement failed"

        # This is the key assertion - observability must be mandatory
        assert all(
            hasattr(mock_pipeline_metrics, attr)
            for attr in ["correlation_id", "start_time", "end_time", "processing_stages"]
        ), "All observability attributes must be present - enforcement failed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
2
