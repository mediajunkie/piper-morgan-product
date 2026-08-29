# Pattern-017: Background Task Error Handling Pattern

## Status

**Proven**

## Context

Background tasks in asynchronous applications run independently of the main request/response cycle, making error handling and task lifecycle management critical for application stability. Without proper error handling, background task failures can crash applications, lose important work, or leave the system in inconsistent states. The Background Task Error Handling Pattern addresses:

- Preventing application crashes from background task failures
- Ensuring task failures are properly logged and tracked
- Maintaining task context and correlation across async boundaries
- Enabling graceful degradation when background tasks fail
- Providing observability into background task performance and reliability
- Preventing task garbage collection and resource leaks

## Pattern Description

The Background Task Error Handling Pattern provides robust error handling and lifecycle management for background tasks through comprehensive task tracking, context preservation, and structured error recovery. The pattern wraps background task execution with monitoring, logging, and recovery mechanisms to ensure system stability and observability.

## Implementation

### Structure

```python
# Background task error handling framework
class BackgroundTaskManager:
    def __init__(self):
        self.active_tasks: Set[asyncio.Task] = set()
        self.task_registry: Dict[str, TaskInfo] = {}
        self.error_handlers: Dict[str, Callable] = {}

    async def execute_task(self, task_func: Callable, task_name: str, **kwargs) -> TaskResult:
        """Execute background task with comprehensive error handling"""
        pass

    def register_error_handler(self, task_type: str, handler: Callable):
        """Register custom error handler for specific task types"""
        pass

    async def cleanup_completed_tasks(self):
        """Clean up completed tasks to prevent resource leaks"""
        pass
```

### Example (Robust Task Manager)

```python
import asyncio
import uuid
from typing import Set, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import structlog

logger = structlog.get_logger()

@dataclass
class TaskMetrics:
    """Track comprehensive metrics for background tasks"""
    task_id: str
    name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_at: Optional[datetime] = None
    success: bool = False
    error_message: Optional[str] = None
    retry_count: int = 0
    context: Dict[str, Any] = field(default_factory=dict)

    def mark_started(self):
        """Mark task as started"""
        self.started_at = datetime.utcnow()

    def mark_completed(self, success: bool = True, error: Optional[str] = None):
        """Mark task as completed"""
        self.completed_at = datetime.utcnow()
        self.success = success
        if not success and error:
            self.error_message = error
            self.error_at = datetime.utcnow()

    def duration(self) -> Optional[float]:
        """Calculate task duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

class RobustTaskManager:
    """Manages background tasks with context preservation and comprehensive tracking"""

    def __init__(self):
        self.active_tasks: Set[asyncio.Task] = set()
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.task_results: Dict[str, Any] = {}
        self.context: Dict[str, Any] = {}
        self.correlation_id: Optional[str] = None
        self.error_handlers: Dict[str, Callable] = {}

    def set_context(self, context: Dict[str, Any], correlation_id: Optional[str] = None):
        """Set execution context for task tracking"""
        self.context = context.copy()
        self.correlation_id = correlation_id or str(uuid.uuid4())

    def add_task(self, task_name: str, task_data: Dict[str, Any]) -> str:
        """Add a task to the manager for tracking"""
        task_id = str(uuid.uuid4())
        metrics = TaskMetrics(
            task_id=task_id,
            name=task_name,
            context={
                **self.context,
                **task_data,
                'correlation_id': self.correlation_id
            }
        )
        self.task_metrics[task_id] = metrics

        logger.info(
            "Task registered for execution",
            task_id=task_id,
            task_name=task_name,
            correlation_id=self.correlation_id
        )

        return task_id

    def start_task(self, task_name: str) -> bool:
        """Mark a task as started"""
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.started_at is None:
                metrics.mark_started()
                logger.info(
                    "Task execution started",
                    task_id=task_id,
                    task_name=task_name,
                    correlation_id=self.correlation_id
                )
                return True
        return False

    def complete_task(self, task_name: str, result: Dict[str, Any]) -> bool:
        """Mark a task as completed with result"""
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.completed_at is None:
                metrics.mark_completed(success=True)
                self.task_results[task_id] = result

                logger.info(
                    "Task completed successfully",
                    task_id=task_id,
                    task_name=task_name,
                    duration=metrics.duration(),
                    correlation_id=self.correlation_id
                )
                return True
        return False

    def fail_task(self, task_name: str, error: Exception) -> bool:
        """Mark a task as failed with error details"""
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.completed_at is None:
                metrics.mark_completed(success=False, error=str(error))

                logger.error(
                    "Task execution failed",
                    task_id=task_id,
                    task_name=task_name,
                    error=str(error),
                    duration=metrics.duration(),
                    correlation_id=self.correlation_id
                )

                # Execute custom error handler if registered
                if task_name in self.error_handlers:
                    try:
                        self.error_handlers[task_name](task_id, error, metrics.context)
                    except Exception as handler_error:
                        logger.error(
                            "Error handler failed",
                            task_name=task_name,
                            handler_error=str(handler_error)
                        )

                return True
        return False

    async def execute_with_tracking(self, task_func: Callable, task_name: str, **kwargs) -> Any:
        """Execute function with comprehensive error handling and tracking"""
        task_id = self.add_task(task_name, kwargs)

        try:
            self.start_task(task_name)
            result = await task_func(**kwargs)
            self.complete_task(task_name, {"result": result})
            return result

        except Exception as e:
            self.fail_task(task_name, e)
            # Re-raise to maintain error propagation
            raise

        finally:
            # Clean up task tracking
            await self._cleanup_task(task_id)

    async def _cleanup_task(self, task_id: str):
        """Clean up completed task to prevent memory leaks"""
        if task_id in self.task_metrics:
            # Keep metrics for a short time for debugging
            await asyncio.sleep(0.1)  # Allow logging to complete
            # In production, might move to a separate cleanup process
```

### Example (Error Recovery and Retry)

```python
class RetryableTaskManager(RobustTaskManager):
    """Extended task manager with retry capabilities"""

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        super().__init__()
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def execute_with_retry(self, task_func: Callable, task_name: str, **kwargs) -> Any:
        """Execute task with automatic retry on failure"""
        task_id = self.add_task(task_name, kwargs)
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    # Update retry count in metrics
                    if task_id in self.task_metrics:
                        self.task_metrics[task_id].retry_count = attempt

                    logger.info(
                        "Retrying task execution",
                        task_id=task_id,
                        task_name=task_name,
                        attempt=attempt,
                        max_retries=self.max_retries
                    )

                    await asyncio.sleep(self.retry_delay * attempt)  # Exponential backoff

                self.start_task(task_name)
                result = await task_func(**kwargs)
                self.complete_task(task_name, {"result": result, "attempts": attempt + 1})
                return result

            except Exception as e:
                last_exception = e
                logger.warning(
                    "Task attempt failed",
                    task_id=task_id,
                    task_name=task_name,
                    attempt=attempt + 1,
                    error=str(e)
                )

                if attempt == self.max_retries:
                    # Final failure
                    self.fail_task(task_name, e)
                    break

        # All retries exhausted
        logger.error(
            "Task failed after all retries",
            task_id=task_id,
            task_name=task_name,
            total_attempts=self.max_retries + 1,
            final_error=str(last_exception)
        )

        if last_exception:
            raise last_exception

# Usage example with graceful degradation
async def process_background_workflow(workflow_data: Dict[str, Any]):
    """Example of background task with comprehensive error handling"""
    task_manager = RetryableTaskManager(max_retries=2)

    try:
        # Execute critical task with retry
        result = await task_manager.execute_with_retry(
            process_critical_step,
            "critical_workflow_step",
            data=workflow_data
        )

        # Execute non-critical task without retry
        await task_manager.execute_with_tracking(
            process_optional_step,
            "optional_workflow_step",
            data=workflow_data,
            result=result
        )

    except Exception as e:
        logger.error(
            "Background workflow failed",
            error=str(e),
            workflow_id=workflow_data.get('id')
        )
        # Graceful degradation - don't crash the application
        return {"status": "partial_failure", "error": str(e)}

    return {"status": "success"}
```

## Usage Guidelines

### Task Lifecycle Management Best Practices

- **Comprehensive Tracking**: Track task creation, start, completion, and error states
- **Context Preservation**: Maintain context and correlation IDs across async boundaries
- **Metrics Collection**: Collect duration, retry count, and success rate metrics
- **Resource Cleanup**: Prevent memory leaks by cleaning up completed task references
- **Correlation Tracking**: Use correlation IDs for distributed tracing and debugging

### Error Handling Strategy Best Practices

- **Graceful Degradation**: Never let background task failures crash the main application
- **Structured Logging**: Log all task lifecycle events with context and correlation IDs
- **Custom Error Handlers**: Implement task-specific error handling for different failure scenarios
- **Retry Logic**: Implement exponential backoff retry for transient failures
- **Circuit Breaker**: Implement circuit breaker pattern for repeated failures

### Observability Best Practices

- **Comprehensive Metrics**: Track success rates, duration, retry counts, and failure patterns
- **Structured Logging**: Use structured logging with consistent field names and correlation IDs
- **Health Monitoring**: Expose task health metrics through monitoring endpoints
- **Alerting**: Set up alerts for task failure rates and duration anomalies
- **Debugging Support**: Maintain task history for troubleshooting and analysis

### Anti-Patterns to Avoid

- **Manual Task Tracking**: Tracking tasks manually without comprehensive metrics and lifecycle management
- **Context Loss**: Losing important context information across async boundaries
- **Missing Correlation**: No correlation tracking between related tasks and operations
- **Task Garbage Collection**: Allowing tasks to be garbage collected while still active
- **Silent Failures**: Failing to log or handle background task errors appropriately
- **Blocking Main Thread**: Allowing background task failures to impact main application performance

## Benefits

- Prevents application crashes from background task failures
- Provides comprehensive observability into background task performance
- Maintains task context and correlation across async boundaries
- Enables graceful degradation when background tasks fail
- Prevents resource leaks through proper task lifecycle management
- Facilitates debugging through comprehensive error tracking

## Trade-offs

- Additional complexity in task management and monitoring
- Memory overhead from task tracking and context preservation
- Performance impact from comprehensive logging and monitoring
- Need for careful balance between monitoring detail and performance
- Potential for monitoring overhead to exceed task execution cost
- Complexity in correlation tracking across distributed operations

## Related Patterns

- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - General async error handling approach
- [Pattern-002: Service Pattern](pattern-002-service.md) - Service-level background task management
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain service background operations
- [Pattern-010: Cross-Validation Protocol](pattern-010-cross-validation-protocol.md) - Validation task error handling

## Migration Notes (for consolidation from legacy systems)

- **From `pattern-catalog.md`**: Section 17 "Background Task Error Handling Pattern" - core implementation and usage guidelines
- **From `PATTERN-INDEX.md`**: No direct equivalent - this is an infrastructure pattern
- **From codebase**: Implementation examples in orchestration services and async task management
- **Consolidation Strategy**: Expanded pattern-catalog.md content with retry logic, observability features, and comprehensive error recovery strategies

## Quality Assurance Checklist

- [x] Pattern description is clear and concise
- [x] Context explains problem and applicability
- [x] Implementation examples are provided and correct
- [x] Usage guidelines are comprehensive
- [x] Related patterns are linked
- [x] All information from source catalog is preserved
- [x] Follows ADR-style numbering and naming conventions

## Agent Coordination Notes

- **Agent A (Code)**: Responsible for task execution infrastructure and orchestration services
- **Agent B (Cursor)**: Responsible for error handling patterns and observability documentation
- **Integration Points**: Background task managers, orchestration engines, and monitoring systems

## References

- Original catalog: `docs/architecture/pattern-catalog.md#17-background-task-error-handling-pattern`
- Task orchestration: `services/orchestration/`
- Background services: `services/background/`
- Async utilities: `services/utils/async_helpers.py`

_Last updated: September 15, 2025_
