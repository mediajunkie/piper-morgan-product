# PM-078 TDD Implementation Plan - Bulletproof Slack Integration

> ⚠️ **Dated note (2026-08-30)**: HISTORICAL plan. The debugging surface it specifies
> (`SlackPipelineInspector` / `PipelineDebugger` in `services/debugging/`, and the
> `slack_monitoring` API router) was built but never mounted or imported by any live path, and
> was disposed in the Batch-2 census-dead-family disposal. The observability layer it feeds on
> (`services/observability/slack_monitor`) remains live. Retrievable by commit hash via the
> 2026-08-30 disposal record in decisions.log.

**Date:** July 29, 2025, 7:18 PM PT
**Mission:** Build a thoroughly monitored, auditable, and debuggable Slack integration using TDD
**Context:** Based on research revealing silent failure patterns in FastAPI background tasks

## Executive Summary

Our current Slack integration suffers from **silent failures** - everything appears to work but no responses reach users. Research reveals this is likely due to:
1. Background tasks dying without error reporting
2. Context loss across async boundaries
3. HTTP client session lifecycle issues
4. Exception masking in FastAPI

This plan implements a **test-first, observable-by-design** integration that cannot fail silently.

## Phase 1: Observability Foundation (1 hour)

### Step 1.1: Create Comprehensive Logging Infrastructure

**Deploy Code - Create Observability Layer**:
```
Build a correlation-tracked logging system for the entire Slack pipeline.

CREATE services/observability/slack_monitor.py:

```python
import asyncio
import contextvars
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any
from enum import Enum

# Context variables for request tracking
correlation_id: ContextVar[str] = ContextVar('correlation_id')
slack_event_id: ContextVar[Optional[str]] = ContextVar('slack_event_id', default=None)
processing_stage: ContextVar[str] = ContextVar('processing_stage', default='unknown')

class ProcessingStage(Enum):
    WEBHOOK_RECEIVED = "webhook_received"
    CONTEXT_EXTRACTED = "context_extracted"
    SPATIAL_MAPPED = "spatial_mapped"
    INTENT_CLASSIFIED = "intent_classified"
    WORKFLOW_CREATED = "workflow_created"
    WORKFLOW_EXECUTED = "workflow_executed"
    RESPONSE_GENERATED = "response_generated"
    SLACK_API_CALLED = "slack_api_called"
    COMPLETE = "complete"
    FAILED = "failed"

@dataclass
class SlackPipelineMetrics:
    correlation_id: str
    event_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    stages: Dict[str, float] = field(default_factory=dict)
    errors: list = field(default_factory=list)
    context_data: Dict[str, Any] = field(default_factory=dict)

    def record_stage(self, stage: ProcessingStage, metadata: Dict[str, Any] = None):
        self.stages[stage.value] = time.time()
        if metadata:
            self.context_data[stage.value] = metadata

    def add_error(self, stage: str, error: Exception):
        self.errors.append({
            "stage": stage,
            "error": str(error),
            "type": type(error).__name__,
            "timestamp": time.time()
        })

    def get_duration(self) -> float:
        return time.time() - self.start_time

    def get_stage_durations(self) -> Dict[str, float]:
        durations = {}
        sorted_stages = sorted(self.stages.items(), key=lambda x: x[1])
        for i, (stage, timestamp) in enumerate(sorted_stages):
            if i < len(sorted_stages) - 1:
                next_timestamp = sorted_stages[i + 1][1]
                durations[stage] = next_timestamp - timestamp
            else:
                durations[stage] = time.time() - timestamp
        return durations

# Global metrics storage for debugging
ACTIVE_PIPELINES: Dict[str, SlackPipelineMetrics] = {}
```

WRITE TESTS FIRST in tests/test_observability.py
```

### Step 1.2: Create Context-Preserving Background Task Manager

**Deploy Cursor - Background Task Infrastructure**:
```
Create a robust background task manager that preserves context and tracks execution.

CREATE services/infrastructure/task_manager.py:

```python
import asyncio
from typing import Set, Callable, Any, Optional
import contextvars
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class RobustTaskManager:
    """Manages background tasks with context preservation and tracking"""

    def __init__(self):
        self.active_tasks: Set[asyncio.Task] = set()
        self.task_results: Dict[str, Any] = {}
        self.task_errors: Dict[str, Exception] = {}

    def create_tracked_task(self, coro, name: str = None, preserve_context: bool = True):
        """Create a task that's tracked and can't be garbage collected"""
        if preserve_context:
            # Capture current context
            context = contextvars.copy_context()

            # Wrap coroutine to run in captured context
            async def context_wrapped():
                return await context.run(lambda: asyncio.create_task(coro))

            task = asyncio.create_task(context_wrapped(), name=name)
        else:
            task = asyncio.create_task(coro, name=name)

        # Track the task
        self.active_tasks.add(task)

        # Set up completion callback
        def handle_completion(finished_task):
            self.active_tasks.discard(finished_task)
            try:
                exception = finished_task.exception()
                if exception:
                    logger.error(f"Task {finished_task.get_name()} failed: {exception}")
                    self.task_errors[finished_task.get_name()] = exception
                else:
                    result = finished_task.result()
                    logger.info(f"Task {finished_task.get_name()} completed successfully")
                    self.task_results[finished_task.get_name()] = result
            except asyncio.CancelledError:
                logger.warning(f"Task {finished_task.get_name()} was cancelled")

        task.add_done_callback(handle_completion)
        return task

    async def wait_for_task(self, task_name: str, timeout: float = 5.0) -> Any:
        """Wait for a specific task to complete with timeout"""
        start_time = asyncio.get_event_loop().time()
        while task_name not in self.task_results and task_name not in self.task_errors:
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(f"Task {task_name} did not complete within {timeout}s")
            await asyncio.sleep(0.1)

        if task_name in self.task_errors:
            raise self.task_errors[task_name]
        return self.task_results.get(task_name)

# Global task manager instance
task_manager = RobustTaskManager()
```

WRITE COMPREHENSIVE TESTS for context preservation and task tracking
```

## Phase 2: TDD Test Suite Creation (1.5 hours)

### Step 2.1: End-to-End Integration Tests

**Deploy Code - Comprehensive Test Suite**:
```
Create integration tests that verify the complete Slack pipeline.

CREATE tests/integration/test_slack_e2e_pipeline.py:

```python
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import json
import time
from datetime import datetime

from services.observability.slack_monitor import (
    SlackPipelineMetrics, ProcessingStage, ACTIVE_PIPELINES,
    correlation_id, slack_event_id
)
from services.infrastructure.task_manager import task_manager

class TestSlackE2EPipeline:
    """Test complete Slack event → response pipeline"""

    @pytest.fixture
    def mock_slack_event(self):
        """Standard Slack app_mention event"""
        return {
            "type": "app_mention",
            "text": "@Piper Morgan help with projects",
            "ts": "1234567890.123456",
            "channel": "C123456",
            "user": "U123456",
            "event_ts": "1234567890.123456"
        }

    @pytest.fixture
    def mock_slack_client(self):
        """Mock SlackClient with response tracking"""
        client = MagicMock()
        client.chat_postMessage = AsyncMock(return_value={"ok": True, "ts": "1234567890.654321"})
        return client

    @pytest.mark.asyncio
    async def test_complete_pipeline_with_observability(self, mock_slack_event, mock_slack_client):
        """Test that every stage is observable and traceable"""
        # Arrange
        from services.integrations.slack.webhook_router import handle_event_callback
        pipeline_metrics = None

        # Act
        with patch('services.integrations.slack.response_handler.slack_client', mock_slack_client):
            # Trigger the pipeline
            result = await handle_event_callback(mock_slack_event)

            # Give background tasks time to complete
            await asyncio.sleep(0.5)

            # Get pipeline metrics
            pipeline_metrics = list(ACTIVE_PIPELINES.values())[-1]

        # Assert - Pipeline stages completed
        assert ProcessingStage.WEBHOOK_RECEIVED.value in pipeline_metrics.stages
        assert ProcessingStage.SPATIAL_MAPPED.value in pipeline_metrics.stages
        assert ProcessingStage.INTENT_CLASSIFIED.value in pipeline_metrics.stages
        assert ProcessingStage.SLACK_API_CALLED.value in pipeline_metrics.stages

        # Assert - No silent failures
        assert len(pipeline_metrics.errors) == 0, f"Pipeline errors: {pipeline_metrics.errors}"

        # Assert - Slack API actually called
        mock_slack_client.chat_postMessage.assert_called_once()
        call_args = mock_slack_client.chat_postMessage.call_args
        assert call_args[1]['channel'] == 'C123456'
        assert 'text' in call_args[1] or 'blocks' in call_args[1]

        # Assert - Timing constraints met
        assert pipeline_metrics.get_duration() < 3.0, "Pipeline must complete within Slack's 3s limit"

    @pytest.mark.asyncio
    async def test_pipeline_failure_is_observable(self, mock_slack_event):
        """Test that failures are logged and observable, not silent"""
        # Arrange - Force a failure in intent classification
        with patch('services.intent.classifier.IntentClassifier.classify',
                   side_effect=ValueError("Test classification error")):

            # Act
            result = await handle_event_callback(mock_slack_event)
            await asyncio.sleep(0.5)

            # Get pipeline metrics
            pipeline_metrics = list(ACTIVE_PIPELINES.values())[-1]

        # Assert - Failure is recorded
        assert len(pipeline_metrics.errors) > 0
        assert any(error['type'] == 'ValueError' for error in pipeline_metrics.errors)
        assert ProcessingStage.FAILED.value in pipeline_metrics.stages

        # Assert - We know exactly where it failed
        failed_stage = pipeline_metrics.errors[0]['stage']
        assert failed_stage == ProcessingStage.INTENT_CLASSIFIED.value

    @pytest.mark.asyncio
    async def test_context_preserved_across_boundaries(self, mock_slack_event):
        """Test that context variables survive async boundaries"""
        captured_contexts = []

        async def capture_context_at_each_stage():
            # Simulate pipeline stages
            stages = [
                ProcessingStage.WEBHOOK_RECEIVED,
                ProcessingStage.SPATIAL_MAPPED,
                ProcessingStage.INTENT_CLASSIFIED,
                ProcessingStage.SLACK_API_CALLED
            ]

            for stage in stages:
                processing_stage.set(stage.value)
                captured_contexts.append({
                    'stage': stage.value,
                    'correlation_id': correlation_id.get(),
                    'event_id': slack_event_id.get()
                })
                await asyncio.sleep(0.01)

        # Set initial context
        correlation_id.set("test-correlation-123")
        slack_event_id.set("test-event-456")

        # Run through task manager to test context preservation
        task = task_manager.create_tracked_task(
            capture_context_at_each_stage(),
            name="test_context_preservation"
        )
        await task

        # Assert - Context preserved at all stages
        assert all(ctx['correlation_id'] == "test-correlation-123" for ctx in captured_contexts)
        assert all(ctx['event_id'] == "test-event-456" for ctx in captured_contexts)
```

### Step 2.2: Component-Level Tests with Mocks

**Deploy Cursor - Component Testing**:
```
Create focused tests for each pipeline component.

CREATE tests/unit/test_slack_components.py:

```python
class TestSlackResponseHandler:
    """Test response handler in isolation"""

    @pytest.mark.asyncio
    async def test_monitoring_intent_bypass(self):
        """Test that monitoring intents don't require full workflows"""
        from services.integrations.slack.response_handler import SlackResponseHandler

        handler = SlackResponseHandler(
            adapter=Mock(),
            classifier=Mock(),
            engine=Mock(),
            slack_client=AsyncMock()
        )

        # Create monitoring intent spatial event
        spatial_event = SpatialEvent(
            object_position=1,
            room_id="C123456",
            description="monitoring conversation"
        )

        # Mock classifier to return CONVERSATION intent
        handler.classifier.classify.return_value = Intent(
            category=IntentCategory.CONVERSATION,
            action="monitor_channel",
            confidence=0.9
        )

        # Act
        await handler.handle_spatial_event(spatial_event)

        # Assert - Should post direct response, not create workflow
        handler.slack_client.chat_postMessage.assert_called_once()
        handler.engine.process_intent.assert_not_called()

class TestSlackAdapter:
    """Test spatial adapter isolation"""

    def test_channel_id_preservation(self):
        """Test that original channel IDs are preserved"""
        adapter = SlackSpatialAdapter()

        # Store context with channel ID
        await adapter.store_context("123.456", {
            "channel": "C123456",
            "thread_ts": None,
            "original_channel_id": "C123456"
        })

        # Retrieve and verify
        context = await adapter.get_context("123.456")
        assert context["original_channel_id"] == "C123456"
        assert context["channel"] == "C123456"
```

## Phase 3: Debugging Infrastructure (1 hour)

### Step 3.1: Pipeline Inspection Tools

**Deploy Code - Debugging Utilities**:
```
Create tools to inspect pipeline state during failures.

CREATE services/debugging/slack_inspector.py:

```python
class SlackPipelineInspector:
    """Tools for debugging silent failures"""

    @staticmethod
    def get_active_pipelines() -> List[SlackPipelineMetrics]:
        """Get all currently active pipeline executions"""
        return list(ACTIVE_PIPELINES.values())

    @staticmethod
    def get_pipeline_by_event(event_id: str) -> Optional[SlackPipelineMetrics]:
        """Find pipeline metrics by Slack event ID"""
        for metrics in ACTIVE_PIPELINES.values():
            if metrics.event_id == event_id:
                return metrics
        return None

    @staticmethod
    def print_pipeline_trace(correlation_id: str):
        """Print detailed trace of a pipeline execution"""
        metrics = ACTIVE_PIPELINES.get(correlation_id)
        if not metrics:
            print(f"No pipeline found for correlation ID: {correlation_id}")
            return

        print(f"\n=== Pipeline Trace: {correlation_id} ===")
        print(f"Event ID: {metrics.event_id}")
        print(f"Total Duration: {metrics.get_duration():.3f}s")
        print(f"Errors: {len(metrics.errors)}")

        print("\nStage Progression:")
        for stage, duration in metrics.get_stage_durations().items():
            status = "✓" if stage != ProcessingStage.FAILED.value else "✗"
            print(f"  {status} {stage}: {duration:.3f}s")

        if metrics.errors:
            print("\nErrors Encountered:")
            for error in metrics.errors:
                print(f"  - {error['stage']}: {error['type']} - {error['error']}")

        print("\nContext Data:")
        for stage, data in metrics.context_data.items():
            print(f"  {stage}: {json.dumps(data, indent=2)}")

    @staticmethod
    async def replay_event(event: dict, mock_api_calls: bool = True):
        """Replay a Slack event through the pipeline for debugging"""
        print(f"Replaying event: {event.get('event_ts', 'unknown')}")

        if mock_api_calls:
            # Mock external calls to prevent side effects
            with patch('services.integrations.slack.response_handler.slack_client') as mock_client:
                mock_client.chat_postMessage = AsyncMock(return_value={"ok": True})
                result = await handle_event_callback(event)
        else:
            result = await handle_event_callback(event)

        # Wait for background processing
        await asyncio.sleep(1.0)

        # Find and display the pipeline trace
        latest_pipeline = list(ACTIVE_PIPELINES.values())[-1]
        SlackPipelineInspector.print_pipeline_trace(latest_pipeline.correlation_id)

        return latest_pipeline
```

CREATE management command for debugging:
```python
# services/debugging/commands.py
async def debug_slack_pipeline():
    """Interactive debugging session for Slack pipeline"""
    print("Slack Pipeline Debugger")
    print("Commands: trace <correlation_id>, replay <event_json>, active, exit")

    while True:
        command = input("> ").strip().split()

        if not command:
            continue

        if command[0] == "trace" and len(command) > 1:
            SlackPipelineInspector.print_pipeline_trace(command[1])

        elif command[0] == "replay" and len(command) > 1:
            event_json = " ".join(command[1:])
            event = json.loads(event_json)
            await SlackPipelineInspector.replay_event(event)

        elif command[0] == "active":
            pipelines = SlackPipelineInspector.get_active_pipelines()
            print(f"Active pipelines: {len(pipelines)}")
            for p in pipelines:
                print(f"  - {p.correlation_id}: {p.event_id} ({p.get_duration():.3f}s)")

        elif command[0] == "exit":
            break
```
```

### Step 3.2: Health Check Endpoints

**Deploy Cursor - Health Monitoring**:
```
Add health check endpoints for Slack integration status.

ADD to services/api/health.py:

```python
@router.get("/health/slack")
async def slack_integration_health():
    """Comprehensive Slack integration health check"""

    health_status = {
        "status": "unknown",
        "checks": {},
        "metrics": {},
        "timestamp": datetime.utcnow().isoformat()
    }

    # Check 1: Slack token configured
    health_status["checks"]["slack_token"] = bool(os.getenv("SLACK_BOT_TOKEN"))

    # Check 2: Can reach Slack API
    try:
        from services.integrations.slack.client import slack_client
        auth_test = await slack_client.auth_test()
        health_status["checks"]["slack_api_reachable"] = auth_test.get("ok", False)
        health_status["checks"]["workspace"] = auth_test.get("team", "unknown")
    except Exception as e:
        health_status["checks"]["slack_api_reachable"] = False
        health_status["checks"]["slack_api_error"] = str(e)

    # Check 3: Recent pipeline success rate
    recent_pipelines = [p for p in ACTIVE_PIPELINES.values()
                       if p.start_time > time.time() - 300]  # Last 5 minutes

    if recent_pipelines:
        successful = sum(1 for p in recent_pipelines
                        if ProcessingStage.COMPLETE.value in p.stages)
        health_status["metrics"]["recent_success_rate"] = successful / len(recent_pipelines)
        health_status["metrics"]["recent_pipeline_count"] = len(recent_pipelines)

        # Average processing time
        durations = [p.get_duration() for p in recent_pipelines
                    if ProcessingStage.COMPLETE.value in p.stages]
        if durations:
            health_status["metrics"]["avg_processing_time"] = sum(durations) / len(durations)

    # Check 4: Background task health
    health_status["checks"]["active_tasks"] = len(task_manager.active_tasks)
    health_status["checks"]["task_errors"] = len(task_manager.task_errors)

    # Overall status determination
    if all(health_status["checks"].get(k, False) for k in ["slack_token", "slack_api_reachable"]):
        if health_status["metrics"].get("recent_success_rate", 0) > 0.8:
            health_status["status"] = "healthy"
        else:
            health_status["status"] = "degraded"
    else:
        health_status["status"] = "unhealthy"

    return health_status
```

## Phase 4: Fix Implementation with Tests (1.5 hours)

### Step 4.1: Implement Fixes Based on Research

**Deploy Code - Apply Research Findings**:
```
Implement the specific fixes our research identified.

UPDATE services/integrations/slack/webhook_router.py:

1. Add comprehensive pipeline tracking
2. Fix context preservation
3. Handle monitoring intents properly
4. Ensure HTTP client lifecycle management

UPDATE services/integrations/slack/response_handler.py:

1. Add bypass for monitoring intents
2. Preserve original channel IDs
3. Add circuit breaker for Slack API
4. Implement proper error propagation

The key insight: Make EVERY step observable and testable.
```

### Step 4.2: Validate with TDD Cycle

**Deploy Both Agents - Red/Green/Refactor**:
```
Run the complete TDD cycle:

1. Run all tests - they should FAIL (Red)
2. Implement fixes until tests PASS (Green)
3. Refactor for clarity while keeping tests GREEN

Critical: If tests pass but Slack still doesn't work, we need more tests!
```

## Phase 5: Production Hardening (30 minutes)

### Step 5.1: Add Monitoring Dashboards

**Deploy Cursor - Monitoring Views**:
```
Create simple web dashboard for Slack pipeline monitoring.

CREATE services/api/slack_monitoring.py:

```python
@router.get("/slack/pipelines")
async def get_pipeline_status():
    """Get current pipeline status for monitoring dashboard"""
    return {
        "active": len(ACTIVE_PIPELINES),
        "recent_errors": [
            {
                "correlation_id": p.correlation_id,
                "event_id": p.event_id,
                "errors": p.errors,
                "duration": p.get_duration()
            }
            for p in ACTIVE_PIPELINES.values()
            if p.errors
        ][-10:],  # Last 10 errors
        "performance": {
            "avg_duration": calculate_avg_duration(),
            "success_rate": calculate_success_rate()
        }
    }
```

## Success Criteria

### Must Have
- [ ] No silent failures - every error is logged and traceable
- [ ] Complete observability - can trace any event through the pipeline
- [ ] Context preservation - correlation IDs maintained across boundaries
- [ ] Actual Slack messages posted successfully
- [ ] All tests pass AND real Slack works

### Should Have
- [ ] Pipeline replay capability for debugging
- [ ] Health check endpoints showing integration status
- [ ] Performance metrics (< 3s end-to-end)
- [ ] Circuit breaker preventing cascade failures

### Nice to Have
- [ ] Web dashboard for monitoring
- [ ] Automatic error recovery patterns
- [ ] Webhook event replay from failed attempts

## Key Insights from Research

1. **FastAPI BackgroundTasks can mask exceptions** - We must catch and log everything
2. **Context is lost across task boundaries** - Explicit preservation required
3. **HTTP clients close prematurely** - Global session management needed
4. **Garbage collection kills unreferenced tasks** - Strong references required

## The TDD Difference

By writing tests FIRST that verify observability, we ensure our implementation cannot fail silently. If it passes all tests but still doesn't work, that reveals missing test coverage - not implementation bugs.

---

**Remember**: If you can't observe it, you can't debug it. Make everything observable!
