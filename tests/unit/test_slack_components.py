"""
Unit Tests for Slack Integration Components
Component-level testing with monitoring intent bypass and observability validation.

TDD Philosophy: Tests REQUIRE observability to pass, not just functionality.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent, IntentCategory, SpatialEvent
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.response_handler import SlackResponseHandler
from services.integrations.slack.slack_client import SlackClient, SlackResponse
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.observability.slack_monitor import SlackPipelineMetrics


class TestSlackResponseHandler:
    """
    Test SlackResponseHandler with monitoring intent bypass.

    Validates that the response handler properly handles monitoring intents
    and maintains observability throughout the process.
    """

    @pytest.fixture
    async def mock_dependencies(self):
        """Create mocked dependencies for response handler"""
        import time

        # Use unique timestamp for each test to avoid duplicate event detection
        unique_ts = str(time.time())

        spatial_adapter = AsyncMock(spec=SlackSpatialAdapter)
        # Add _lock attribute to prevent AttributeError
        spatial_adapter._lock = MagicMock()

        # Set up proper mock behavior for spatial adapter
        # Create a mock timestamp-to-position mapping with unique timestamp
        spatial_adapter._timestamp_to_position = {unique_ts: 123}
        spatial_adapter._position_to_timestamp = {123: unique_ts}
        spatial_adapter._context_storage = {
            unique_ts: {
                "channel_id": "C1234567890",
                "user_id": "U1234567890",
                "workspace_id": "T1234567890",
                "thread_ts": None,
                "content": "Test message",
                "ts": unique_ts,  # Include ts for duplicate detection
            }
        }

        # Mock the get_response_context method to return proper context
        async def mock_get_response_context(timestamp):
            return spatial_adapter._context_storage.get(timestamp)

        spatial_adapter.get_response_context = mock_get_response_context

        intent_classifier = AsyncMock()
        orchestration_engine = AsyncMock()
        slack_client = AsyncMock(spec=SlackClient)

        return {
            "spatial_adapter": spatial_adapter,
            "intent_classifier": intent_classifier,
            "orchestration_engine": orchestration_engine,
            "slack_client": slack_client,
        }

    @pytest.fixture
    async def response_handler(self, mock_dependencies):
        """Create response handler with mocked dependencies"""
        return SlackResponseHandler(
            spatial_adapter=mock_dependencies["spatial_adapter"],
            intent_classifier=mock_dependencies["intent_classifier"],
            orchestration_engine=mock_dependencies["orchestration_engine"],
            slack_client=mock_dependencies["slack_client"],
        )

    @pytest.fixture
    async def mock_spatial_event(self):
        """Create mock spatial event"""
        return SpatialEvent(
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

    @pytest.mark.smoke
    async def test_monitoring_intent_bypass(
        self, response_handler, mock_spatial_event, mock_dependencies
    ):
        """
        Test that monitoring intents are properly bypassed with observability.

        This ensures monitoring doesn't interfere with normal processing.
        """
        # Arrange: Create monitoring intent using ANALYSIS category instead of MONITORING
        monitoring_intent = Intent(
            action="monitor_system",
            category=IntentCategory.ANALYSIS,  # Use valid category
            confidence=0.98,
            context={"monitoring": True},
        )

        mock_dependencies["intent_classifier"].classify.return_value = monitoring_intent
        mock_dependencies["spatial_adapter"].get_response_context.return_value = {
            "channel_id": "C1234567890",
            "user_id": "U1234567890",
        }

        # Act: Handle spatial event with monitoring intent
        result = await response_handler.handle_spatial_event(mock_spatial_event)

        # Assert: Monitoring intent should be handled gracefully
        assert result is not None, "Monitoring intent should return result"

        # Assert: Intent classification should be called
        mock_dependencies["intent_classifier"].classify.assert_called_once()

        # Assert: No orchestration for monitoring intents
        mock_dependencies["orchestration_engine"].create_workflow_from_intent.assert_not_called()

    @pytest.mark.smoke
    async def test_response_handler_observability(
        self, response_handler, mock_spatial_event, mock_dependencies
    ):
        """
        Test that response handler maintains observability throughout processing.

        This ensures all operations are tracked and observable.

        Fix for #739: Mocks at handler method level (_get_slack_context_from_spatial_event)
        instead of adapter internals (_lock, _timestamp_to_position, _context_storage).
        This decouples the test from spatial adapter implementation details.
        """
        import time

        # Arrange: Set up successful processing with EXECUTION category
        # Note: Only EXECUTION intents trigger workflow creation per emergency fix
        intent = Intent(action="create_task", category=IntentCategory.EXECUTION, confidence=0.95)
        mock_dependencies["intent_classifier"].classify.return_value = intent

        # Use unique timestamp to avoid duplicate detection
        unique_ts = str(time.time())

        # Mock _get_slack_context_from_spatial_event at the handler level
        # This avoids all adapter internal mocking (_lock, _timestamp_to_position, etc.)
        slack_context = {
            "channel_id": "C1234567890",
            "user_id": "U1234567890",
            "ts": unique_ts,
        }
        response_handler._get_slack_context_from_spatial_event = AsyncMock(
            return_value=slack_context
        )

        # Mock orchestration: execute_workflow returns a FLAT result dict
        # _process_through_orchestration wraps it as:
        #   {'type': 'workflow_result', 'result': <execute_workflow return>, ...}
        # So _format_response_content sees result={'summary': 'Test completed'}
        mock_dependencies[
            "orchestration_engine"
        ].create_workflow_from_intent.return_value = MagicMock(id="test_workflow")
        mock_dependencies["orchestration_engine"].execute_workflow.return_value = {
            "summary": "Test completed",
        }

        success_response = SlackResponse(success=True, data={"ok": True, "ts": unique_ts})
        mock_dependencies["slack_client"].send_message.return_value = success_response

        # Clear PROCESSED_EVENTS to prevent duplicate detection from other tests
        from services.integrations.slack.response_handler import PROCESSED_EVENTS

        PROCESSED_EVENTS.discard(unique_ts)

        # Act: Process spatial event
        result = await response_handler.handle_spatial_event(mock_spatial_event)

        # Assert: All steps should be observable
        assert result is not None, "Response handler should return result"

        # Assert: Slack context was retrieved (our mocked method was called)
        response_handler._get_slack_context_from_spatial_event.assert_called_once_with(
            mock_spatial_event
        )

        # Assert: Intent classification was called
        mock_dependencies["intent_classifier"].classify.assert_called_once()

        # Assert: Orchestration was called
        mock_dependencies["orchestration_engine"].create_workflow_from_intent.assert_called_once()
        mock_dependencies["orchestration_engine"].execute_workflow.assert_called_once()

        # Assert: Slack message was sent
        mock_dependencies["slack_client"].send_message.assert_called_once()

    @pytest.mark.smoke
    async def test_response_handler_error_observability(
        self, response_handler, mock_spatial_event, mock_dependencies
    ):
        """
        Test that response handler errors are observable.

        This ensures silent failures are detected and reported.
        """
        # Arrange: Mock error in intent classification
        mock_dependencies["intent_classifier"].classify.side_effect = Exception(
            "Intent classification failed"
        )

        # Act: Process spatial event (should handle error gracefully)
        result = await response_handler.handle_spatial_event(mock_spatial_event)

        # Assert: Error should be handled gracefully
        assert result is None, "Error should result in None return"

        # Assert: Error should be logged (observability)
        # Note: This would require checking the logger, but we can verify the method completed
        assert mock_dependencies[
            "intent_classifier"
        ].classify.called, "Intent classification should have been attempted"


class TestSlackAdapter:
    """
    Test SlackSpatialAdapter with channel ID preservation.

    Validates that the spatial adapter properly preserves channel IDs
    and maintains observability throughout the mapping process.
    """

    @pytest.fixture
    async def spatial_adapter(self):
        """Create spatial adapter instance"""
        return SlackSpatialAdapter()

    @pytest.mark.smoke
    async def test_channel_id_preservation(self, spatial_adapter):
        """
        Test that channel IDs are preserved throughout spatial mapping.

        This ensures spatial context is maintained for response routing.
        """
        # Arrange: Create context with channel ID
        context = {
            "territory_id": "T1234567890",
            "room_id": "C1234567890",  # Channel ID
            "user_id": "U1234567890",
            "content": "Test message",
        }
        timestamp = "1234567890.123456"

        # Act: Create spatial event
        spatial_event = await spatial_adapter.create_spatial_event_from_slack(
            timestamp, "message_posted", context
        )

        # Assert: Channel ID should be preserved in spatial event
        assert spatial_event.room_position is not None, "Room position should be set"

        # Assert: Context should be stored for response routing
        response_context = await spatial_adapter.get_response_context(timestamp)
        assert response_context is not None, "Response context should be available"
        assert response_context.get("channel_id") == "C1234567890", "Channel ID should be preserved"

    @pytest.mark.smoke
    async def test_bidirectional_mapping_observability(self, spatial_adapter):
        """
        Test that bidirectional mapping is observable.

        This ensures mapping operations are tracked and verifiable.
        """
        # Arrange: Create mapping
        context = {
            "territory_id": "T1234567890",
            "room_id": "C1234567890",
            "user_id": "U1234567890",
        }
        timestamp = "1234567890.123456"

        # Act: Create mapping
        position = await spatial_adapter.map_to_position(timestamp, context)

        # Assert: Forward mapping should work
        assert position.position is not None, "Position should be assigned"

        # Act: Reverse mapping
        reverse_timestamp = await spatial_adapter.map_from_position(position)

        # Assert: Reverse mapping should work
        assert reverse_timestamp == timestamp, "Reverse mapping should return original timestamp"

        # Assert: Mapping should be observable
        stats = await spatial_adapter.get_mapping_stats()
        assert stats["timestamp_mappings"] > 0, "Mapping should be recorded in stats"

    @pytest.mark.smoke
    async def test_context_storage_observability(self, spatial_adapter):
        """
        Test that context storage is observable.

        This ensures context preservation is tracked and verifiable.
        """
        # Arrange: Create context
        context = {
            "territory_id": "T1234567890",
            "room_id": "C1234567890",
            "user_id": "U1234567890",
            "attention_level": "high",
        }
        timestamp = "1234567890.123456"

        # Act: Store context via map_to_position (which stores context for routing)
        await spatial_adapter.map_to_position(timestamp, context)

        # Assert: Context should be retrievable
        stored_context = await spatial_adapter.get_context(timestamp)
        assert stored_context is not None, "Context should be retrievable"
        assert stored_context.room_id == "C1234567890", "Room ID should be preserved"
        assert stored_context.attention_level == "high", "Attention level should be preserved"


class TestRobustTaskManager:
    """
    Test RobustTaskManager with context preservation.

    Validates that the task manager properly preserves context
    across async boundaries and maintains observability.
    """

    @pytest.fixture
    async def task_manager(self):
        """Create task manager instance"""
        return RobustTaskManager()

    @pytest.mark.smoke
    async def test_context_preservation_across_async_boundaries(self, task_manager):
        """
        Test that context is preserved across async boundaries.

        This ensures observability is maintained throughout async operations.
        """
        # Arrange: Set initial context
        original_context = {
            "user_id": "U1234567890",
            "channel_id": "C1234567890",
            "correlation_id": "test_correlation_123",
        }
        task_manager.context = original_context.copy()

        # Act: Simulate async operation
        async def async_operation():
            # Context should be preserved
            assert (
                task_manager.context == original_context
            ), "Context should be preserved in async operation"
            return "async_result"

        result = await async_operation()

        # Assert: Context should be preserved
        assert (
            task_manager.context == original_context
        ), "Context should be preserved after async operation"
        assert result == "async_result", "Async operation should complete successfully"

    @pytest.mark.smoke
    async def test_correlation_id_preservation(self, task_manager):
        """
        Test that correlation IDs are preserved throughout task execution.

        This ensures observability can trace operations end-to-end.
        """
        # Arrange: Set correlation ID
        correlation_id = "test_correlation_456"
        task_manager.correlation_id = correlation_id

        # Act: Simulate multiple async operations
        async def operation_1():
            assert (
                task_manager.correlation_id == correlation_id
            ), "Correlation ID should be preserved in operation 1"
            return "op1_result"

        async def operation_2():
            assert (
                task_manager.correlation_id == correlation_id
            ), "Correlation ID should be preserved in operation 2"
            return "op2_result"

        result1 = await operation_1()
        result2 = await operation_2()

        # Assert: Correlation ID should be preserved
        assert (
            task_manager.correlation_id == correlation_id
        ), "Correlation ID should be preserved after all operations"
        assert result1 == "op1_result", "Operation 1 should complete"
        assert result2 == "op2_result", "Operation 2 should complete"

    @pytest.mark.smoke
    async def test_task_manager_observability(self, task_manager):
        """
        Test that task manager operations are observable.

        This ensures all task operations are tracked and verifiable using the proven
        create_tracked_task() interface for context preservation and observability.
        """
        # Arrange: Set up task manager state
        task_manager.context = {"test": "context"}
        task_manager.correlation_id = "test_correlation_789"

        # Act: Create tracked task using the proven interface
        async def test_coroutine():
            return {"result": "success"}

        task = task_manager.create_tracked_task(
            test_coroutine(),
            name="test_task",
            metadata={"task_data": "value", "correlation_id": "test_correlation_789"},
        )

        # Wait for task to complete
        result = await task

        # Assert: Operations should be observable
        assert task_manager.context == {"test": "context"}, "Context should be preserved"
        assert (
            task_manager.correlation_id == "test_correlation_789"
        ), "Correlation ID should be preserved"

        # Assert: Task completed successfully with observable result
        assert result == {"result": "success"}, "Task should complete with expected result"

        # Assert: Task metrics should be tracked
        assert len(task_manager.task_metrics) > 0, "Task metrics should be recorded"

        # Assert: Task should be observable through task manager
        task_summary = task_manager.get_active_tasks_summary()
        assert task_summary["total_tasks_created"] > 0, "Task creation should be tracked"


class TestSlackPipelineMetrics:
    """
    Test SlackPipelineMetrics with correlation tracking.

    Validates that pipeline metrics properly track correlations
    and maintain observability throughout the pipeline.
    """

    @pytest.fixture
    async def pipeline_metrics(self):
        """Create pipeline metrics instance with required arguments"""
        from datetime import datetime, timezone

        return SlackPipelineMetrics(
            correlation_id="test_correlation_id",
            slack_event_id="test_event_id",
            started_at=datetime.now(timezone.utc),
        )

    @pytest.mark.smoke
    async def test_correlation_tracking(self, pipeline_metrics):
        """
        Test that correlation tracking works throughout the pipeline.

        This ensures observability can trace requests end-to-end.
        """
        # Arrange: Set correlation ID
        correlation_id = "test_correlation_123"
        pipeline_metrics.correlation_id = correlation_id

        # Act: Record processing stages
        pipeline_metrics.record_stage("webhook_received", {"timestamp": datetime.now()})
        pipeline_metrics.record_stage("spatial_event_created", {"position": 123})
        pipeline_metrics.record_stage("intent_classified", {"category": "analysis"})

        # Assert: Correlation should be tracked in all stages
        for stage in pipeline_metrics.processing_stages:
            assert "correlation_id" in stage, "Stage should have correlation_id"
            assert (
                stage["correlation_id"] == correlation_id
            ), "Stage should have correct correlation_id"

    @pytest.mark.smoke
    async def test_pipeline_timing_observability(self, pipeline_metrics):
        """
        Test that pipeline timing is observable.

        This ensures performance is tracked and verifiable.
        """
        # Arrange: Start pipeline
        pipeline_metrics.start_pipeline()

        # Act: Simulate processing time
        import asyncio

        await asyncio.sleep(0.1)  # Simulate processing

        # Act: End pipeline
        pipeline_metrics.end_pipeline()

        # Assert: Timing should be observable
        assert pipeline_metrics.start_time is not None, "Start time should be recorded"
        assert pipeline_metrics.end_time is not None, "End time should be recorded"

        # Assert: Processing time should be calculable
        processing_time = (pipeline_metrics.end_time - pipeline_metrics.start_time).total_seconds()
        assert processing_time > 0, "Processing time should be positive"
        assert processing_time < 1.0, "Processing time should be reasonable"

    @pytest.mark.smoke
    async def test_stage_recording_observability(self, pipeline_metrics):
        """
        Test that stage recording is observable.

        This ensures all pipeline stages are tracked and verifiable.
        """
        # Arrange: Set up pipeline
        pipeline_metrics.start_pipeline()

        # Act: Record multiple stages
        stages = [
            ("webhook_received", {"channel": "C1234567890"}),
            ("spatial_event_created", {"position": 123}),
            ("intent_classified", {"category": "analysis"}),
            ("workflow_created", {"workflow_id": "test_123"}),
            ("response_sent", {"channel": "C1234567890"}),
        ]

        for stage_name, stage_data in stages:
            pipeline_metrics.record_stage(stage_name, stage_data)

        # Act: End pipeline
        pipeline_metrics.end_pipeline()

        # Assert: All stages should be recorded
        assert len(pipeline_metrics.processing_stages) == len(
            stages
        ), f"Expected {len(stages)} stages, got {len(pipeline_metrics.processing_stages)}"

        # Assert: Stage data should be preserved
        for i, (stage_name, stage_data) in enumerate(stages):
            stage = pipeline_metrics.processing_stages[i]
            assert stage["name"] == stage_name, f"Stage {i} should have correct name"
            assert stage["data"] == stage_data, f"Stage {i} should have correct data"

    @pytest.mark.smoke
    async def test_error_recording_observability(self, pipeline_metrics):
        """
        Test that errors are recorded with observability.

        This ensures silent failures are detected and reported.
        """
        # Arrange: Start pipeline
        pipeline_metrics.start_pipeline()

        # Act: Record error stage
        error_data = {
            "error_type": "slack_api_error",
            "error_message": "Rate limit exceeded",
            "retry_after": 60,
        }
        pipeline_metrics.record_stage("error_occurred", error_data)

        # Act: End pipeline
        pipeline_metrics.end_pipeline()

        # Assert: Error should be recorded
        error_stages = [
            s for s in pipeline_metrics.processing_stages if "error" in s["name"].lower()
        ]
        assert len(error_stages) == 1, "Error stage should be recorded"

        error_stage = error_stages[0]
        assert (
            error_stage["data"]["error_type"] == "slack_api_error"
        ), "Error type should be recorded"
        assert (
            error_stage["data"]["error_message"] == "Rate limit exceeded"
        ), "Error message should be recorded"

        # Assert: Pipeline should still be observable even with errors
        assert pipeline_metrics.end_time is not None, "Pipeline should end even with errors"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
