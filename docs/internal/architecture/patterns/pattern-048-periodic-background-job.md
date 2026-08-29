# Pattern-048: Periodic Background Job

**Status**: Proven
**Category**: Infrastructure & Scheduling
**First Documented**: January 10, 2026
**Ratified**: January 10, 2026 (Code Architecture)

---

## Problem Statement

Applications frequently need lightweight, configurable background jobs that run at regular intervals without complex scheduler dependencies. Common scenarios include:

- Cleanup tasks (expired token removal every 24 hours)
- Periodic notifications (standup reminders every 1 hour)
- Recurring maintenance (decay calculations every 5 minutes)

Common challenges:

- Long sleep periods make shutdown slow and unresponsive
- Hard-coded intervals require code changes to tune
- Complex orchestration frameworks add unnecessary overhead
- Lack of standardized lifecycle management

This pattern provides a lightweight, asyncio-based solution suitable for many background job scenarios.

---

## Solution

Implement periodic jobs using a simple asyncio-based class with:

1. **Configurable interval** - Set at construction with MIN/MAX bounds
2. **Responsive shutdown** - Break sleep into 1-minute chunks for quick termination
3. **Clean lifecycle** - `start()`, `stop()`, `is_running()` methods
4. **Structured result format** - Consistent return structure for execute methods
5. **App state integration** - Store in `app.state` for shutdown access
6. **Optional tuneable intervals** - Integrate with UserPreferenceManager for dynamic configuration

---

## Pattern Description

A **Periodic Background Job** is an asyncio task that repeatedly executes work at a configured interval. The pattern emphasizes:

- **Lightweight implementation**: No external scheduler, minimal dependencies
- **Responsive lifecycle**: Quick startup and shutdown via chunked sleep
- **Separation of concerns**: Job class focuses only on scheduling, delegates work to execute methods
- **Graceful error handling**: Errors in one cycle don't stop subsequent cycles
- **Observable results**: Each execution returns structured results with timestamps and error information

### Key Characteristics

1. **Interval configuration**: Settable in constructor with validation bounds
2. **Sleep chunking**: Breaks long sleep periods into smaller chunks (typically 1-5 minutes)
3. **Running flag**: Boolean `_running` controls lifecycle
4. **Execute method pattern**: Separate `execute_*()` method contains actual work logic
5. **Structured returns**: Result dicts include timestamp, success flag, and error tracking
6. **Error isolation**: Exceptions in one cycle are caught and logged, don't break loop

---

## Implementation

### Structure

```python
class PeriodicBackgroundJob:
    """Base pattern for periodic background jobs."""

    def __init__(
        self,
        interval_minutes: int,
        min_interval: int = 1,
        max_interval: int = 1440,  # 24 hours
    ):
        """
        Initialize job with configurable interval.

        Args:
            interval_minutes: How often to run job (in minutes)
            min_interval: Minimum allowed interval (default: 1 minute)
            max_interval: Maximum allowed interval (default: 1440 minutes / 24 hours)

        Raises:
            ValueError: If interval outside [min_interval, max_interval] bounds
        """
        if not (min_interval <= interval_minutes <= max_interval):
            raise ValueError(
                f"interval_minutes {interval_minutes} outside bounds "
                f"[{min_interval}, {max_interval}]"
            )

        self.interval_minutes = interval_minutes
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def execute_work(self) -> Dict[str, Any]:
        """
        Execute the actual job work.

        Must be implemented by subclasses.

        Returns:
            Dict with structure:
            {
                "success": bool,
                "timestamp": str (ISO format),
                "error": Optional[str],
                ... additional fields specific to job
            }
        """
        raise NotImplementedError("Subclasses must implement execute_work()")

    async def start(self) -> None:
        """
        Start the periodic job loop.

        Runs continuously, executing work every interval_minutes.
        Breaks sleep into smaller chunks (1-minute) for responsive shutdown.
        """
        if self._running:
            logger.warning("Job already running, ignoring start request")
            return

        self._running = True
        logger.info("Job starting", interval_minutes=self.interval_minutes)

        while self._running:
            try:
                # Execute work
                logger.debug("Executing job work")
                result = await self.execute_work()

                if result.get("success"):
                    logger.info("Job execution successful", **result)
                else:
                    logger.warning("Job execution had errors", **result)

            except Exception as e:
                logger.error("Unexpected error in job loop", error=str(e), exc_info=True)

            # Sleep until next run, in 1-minute chunks for responsive shutdown
            if self._running:
                logger.debug(f"Sleeping for {self.interval_minutes} minutes")

                sleep_chunks = self.interval_minutes  # One chunk per minute
                for _ in range(sleep_chunks):
                    if not self._running:
                        break
                    await asyncio.sleep(60)  # 1 minute per chunk

        logger.info("Job stopped")

    async def stop(self) -> None:
        """
        Stop the job gracefully.

        Sets running flag to False, allowing current execution to complete.
        Optionally waits for current task with timeout.
        """
        if not self._running:
            logger.warning("Job not running")
            return

        logger.info("Stopping job...")
        self._running = False

        # Optionally wait for current task (max 10 seconds)
        if self._task and not self._task.done():
            try:
                await asyncio.wait_for(asyncio.shield(self._task), timeout=10.0)
            except asyncio.TimeoutError:
                logger.warning("Job shutdown timeout, cancelling task")
                self._task.cancel()

        logger.info("Job stopped")

    def is_running(self) -> bool:
        """Check if job is currently running."""
        return self._running
```

### Code Example

**Example 1: Token Blacklist Cleanup** (24-hour interval)

```python
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
import structlog

from services.auth.token_blacklist import TokenBlacklist
from services.cache.redis_factory import RedisFactory
from services.database.session_factory import AsyncSessionFactory

logger = structlog.get_logger(__name__)


class BlacklistCleanupJob:
    """
    Background job to clean up expired blacklist entries.

    Runs periodically to remove expired tokens from database storage.
    Redis entries auto-expire via TTL and don't need cleanup.
    """

    def __init__(
        self,
        redis_factory: Optional[RedisFactory] = None,
        db_session_factory: Optional[AsyncSessionFactory] = None,
        interval_hours: int = 24,
    ):
        """
        Initialize cleanup job.

        Args:
            redis_factory: Redis factory for blacklist
            db_session_factory: Database session factory
            interval_hours: Hours between cleanup runs (default: 24)
        """
        self.redis_factory = redis_factory or RedisFactory()
        self.db_session_factory = db_session_factory or AsyncSessionFactory()
        self.interval_minutes = interval_hours * 60  # Convert to minutes
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._blacklist: Optional[TokenBlacklist] = None

        logger.info("BlacklistCleanupJob initialized", interval_hours=interval_hours)

    async def _initialize_blacklist(self) -> None:
        """Initialize TokenBlacklist instance."""
        if self._blacklist is None:
            self._blacklist = TokenBlacklist(self.redis_factory, self.db_session_factory)
            await self._blacklist.initialize()
            logger.info("TokenBlacklist initialized for cleanup job")

    async def execute_cleanup(self) -> Dict[str, Any]:
        """
        Execute cleanup of expired blacklist entries.

        Returns:
            Dict with cleanup results: {
                "removed": int,
                "timestamp": str,
                "success": bool,
                "error": Optional[str]
            }
        """
        try:
            await self._initialize_blacklist()

            # Remove expired entries from database
            count = await self._blacklist.remove_expired()

            result = {
                "removed": count,
                "timestamp": datetime.utcnow().isoformat(),
                "success": True,
                "error": None,
            }

            logger.info("Blacklist cleanup completed", removed=count)
            return result

        except Exception as e:
            error_msg = f"Blacklist cleanup failed: {str(e)}"
            logger.error(error_msg, exc_info=True)

            return {
                "removed": 0,
                "timestamp": datetime.utcnow().isoformat(),
                "success": False,
                "error": error_msg,
            }

    async def start(self) -> None:
        """
        Start the cleanup job loop.

        Runs continuously, cleaning expired entries every 24 hours (default).
        Breaks sleep into 1-minute chunks for responsive shutdown.
        """
        if self._running:
            logger.warning("Cleanup job already running, ignoring start request")
            return

        self._running = True
        logger.info("Blacklist cleanup job starting", interval_hours=self.interval_minutes // 60)

        while self._running:
            try:
                logger.debug("Executing blacklist cleanup")
                result = await self.execute_cleanup()

                if result["success"]:
                    logger.info("Blacklist cleanup successful", removed=result["removed"])
                else:
                    logger.warning("Blacklist cleanup encountered error", error=result.get("error"))

            except Exception as e:
                logger.error("Unexpected error in cleanup job loop", error=str(e), exc_info=True)

            # Sleep in 1-minute chunks for responsive shutdown
            if self._running:
                logger.debug(f"Sleeping for {self.interval_minutes} minutes until next cleanup")

                for _ in range(self.interval_minutes):
                    if not self._running:
                        break
                    await asyncio.sleep(60)  # 1 minute

        logger.info("Blacklist cleanup job stopped")

    async def stop(self) -> None:
        """Stop the cleanup job gracefully."""
        if not self._running:
            logger.warning("Cleanup job not running")
            return

        logger.info("Stopping blacklist cleanup job...")
        self._running = False

        if self._task and not self._task.done():
            try:
                await asyncio.wait_for(asyncio.shield(self._task), timeout=10.0)
            except asyncio.TimeoutError:
                logger.warning("Cleanup job shutdown timeout, cancelling task")
                self._task.cancel()

        logger.info("Blacklist cleanup job stopped")

    def is_running(self) -> bool:
        """Check if cleanup job is currently running."""
        return self._running
```

**Example 2: Standup Reminder Job** (1-hour interval with timezone awareness)

```python
class StandupReminderJob:
    """
    Daily standup reminder job with timezone awareness.

    Sends Slack DMs to users at their configured reminder time.
    """

    def __init__(
        self,
        task_manager: RobustTaskManager,
        slack_router: SlackIntegrationRouter,
        preference_manager: UserPreferenceManager,
        interval_minutes: int = 60,  # Check every hour
    ):
        """Initialize reminder job with dependencies."""
        self.task_manager = task_manager
        self.slack_router = slack_router
        self.preference_manager = preference_manager
        self.interval_minutes = interval_minutes
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def execute_daily_reminders(self) -> Dict[str, Any]:
        """
        Execute hourly check for reminders to send.

        Returns:
            Dict with results: {
                "checked": int,
                "sent": int,
                "failed": int,
                "errors": List[str],
                "timestamp": str
            }
        """
        logger.info("Starting reminder check")

        results = {
            "checked": 0,
            "sent": 0,
            "failed": 0,
            "errors": [],
            "timestamp": datetime.utcnow().isoformat(),
        }

        try:
            # Get all users with reminders enabled
            enabled_users = await self._get_enabled_users()
            results["checked"] = len(enabled_users)

            # Process each enabled user
            for user_id in enabled_users:
                try:
                    # Check if it's reminder time for this user (timezone-aware)
                    should_send = await self._should_send_reminder(user_id)

                    if should_send:
                        # Send the reminder
                        success = await self._send_reminder(user_id)

                        if success:
                            results["sent"] += 1
                            logger.info("Reminder sent", user_id=user_id)
                        else:
                            results["failed"] += 1
                            error_msg = f"Failed to send reminder to {user_id}"
                            results["errors"].append(error_msg)
                            logger.warning(error_msg)

                except Exception as e:
                    results["failed"] += 1
                    error_msg = f"Error processing user {user_id}: {str(e)}"
                    results["errors"].append(error_msg)
                    logger.error("Error processing user", user_id=user_id, error=str(e))

            results["success"] = results["failed"] == 0

            logger.info(
                "Reminder check complete",
                checked=results["checked"],
                sent=results["sent"],
                failed=results["failed"],
            )

        except Exception as e:
            error_msg = f"Critical error in reminder check: {str(e)}"
            results["errors"].append(error_msg)
            results["success"] = False
            logger.error("Critical error in reminder check", error=str(e))

        return results

    async def start(self) -> None:
        """Start the reminder job loop (checks every hour)."""
        if self._running:
            logger.warning("Reminder job already running")
            return

        self._running = True
        logger.info("Standup reminder job starting", interval_minutes=self.interval_minutes)

        while self._running:
            try:
                result = await self.execute_daily_reminders()
                if not result.get("success"):
                    logger.warning("Reminder execution had issues", **result)

            except Exception as e:
                logger.error("Unexpected error in reminder job", error=str(e), exc_info=True)

            # Sleep in 1-minute chunks
            if self._running:
                for _ in range(self.interval_minutes):
                    if not self._running:
                        break
                    await asyncio.sleep(60)

        logger.info("Standup reminder job stopped")

    async def stop(self) -> None:
        """Stop the reminder job gracefully."""
        if not self._running:
            return

        logger.info("Stopping standup reminder job...")
        self._running = False

        if self._task and not self._task.done():
            try:
                await asyncio.wait_for(asyncio.shield(self._task), timeout=10.0)
            except asyncio.TimeoutError:
                self._task.cancel()

        logger.info("Standup reminder job stopped")

    def is_running(self) -> bool:
        """Check if reminder job is currently running."""
        return self._running
```

### App Integration

```python
# In web/startup.py or app initialization

async def startup_background_jobs():
    """Initialize and start background jobs."""

    # Create job instances
    cleanup_job = BlacklistCleanupJob(interval_hours=24)
    reminder_job = StandupReminderJob(
        task_manager=container.get_service("task_management"),
        slack_router=container.get_service("slack_integration"),
        preference_manager=container.get_service("user_preference"),
        interval_minutes=60,
    )

    # Store in app state for shutdown access
    app.state.background_jobs = [cleanup_job, reminder_job]

    # Start all jobs
    for job in app.state.background_jobs:
        asyncio.create_task(job.start())

    logger.info(f"Started {len(app.state.background_jobs)} background jobs")


async def shutdown_background_jobs():
    """Stop all background jobs gracefully."""

    if not hasattr(app.state, "background_jobs"):
        return

    logger.info(f"Shutting down {len(app.state.background_jobs)} background jobs...")

    # Stop all jobs concurrently
    stop_tasks = [job.stop() for job in app.state.background_jobs]
    await asyncio.gather(*stop_tasks, return_exceptions=True)

    logger.info("All background jobs stopped")


# Register lifecycle handlers
app.add_event_handler("startup", startup_background_jobs)
app.add_event_handler("shutdown", shutdown_background_jobs)
```

### Configuration

```python
# Configuration with UserPreferenceManager integration (optional)

class ConfigurableBackgroundJob:
    """
    Background job with tuneable interval from UserPreferenceManager.

    Allows ops to adjust job frequency without redeployment.
    """

    def __init__(
        self,
        base_interval_minutes: int,
        preference_key: Optional[str] = None,
        preference_manager: Optional[UserPreferenceManager] = None,
    ):
        """
        Initialize with optional preference-based configuration.

        Args:
            base_interval_minutes: Default interval if no preference set
            preference_key: UserPreferenceManager key (e.g., "cleanup_job_interval")
            preference_manager: UserPreferenceManager instance
        """
        self.base_interval_minutes = base_interval_minutes
        self.preference_key = preference_key
        self.preference_manager = preference_manager
        self._running = False

    async def get_current_interval(self) -> int:
        """Get current interval, checking preferences first."""
        if self.preference_manager and self.preference_key:
            try:
                pref = await self.preference_manager.get_global_preference(self.preference_key)
                if pref and isinstance(pref, int):
                    return max(1, min(1440, pref))  # Clamp to [1, 1440] minutes
            except Exception as e:
                logger.warning(f"Failed to load preference {self.preference_key}: {e}")

        return self.base_interval_minutes
```

---

## Usage Guidelines

### When to Use

✅ **Use Periodic Background Job when:**

- Task runs at regular intervals (hourly, daily, etc.)
- Don't need real-time precision (minute-level granularity is fine)
- Task is self-contained and independent
- Shutdown responsiveness matters (need quick stop)
- Want minimal operational overhead (no external scheduler)
- Task should continue despite transient errors
- Each execution should log and report results

### When NOT to Use

❌ **Don't use when:**

- **Real-time requirements**: Need sub-second precision → Use WebSocket/SSE instead
- **Event-driven**: React to user actions → Use pub/sub (Redis, message queue)
- **Complex scheduling**: Need cron-like expressions, retries, dependency chains → Use Temporal, APScheduler, or dedicated orchestrator
- **One-off tasks**: Just run once → Use direct call or immediate async task
- **Distributed coordination**: Multiple instances need to coordinate → Use distributed lock or central coordinator

### Best Practices

1. **Name execute methods clearly**: Use `execute_[task_name]()` to make purpose obvious
2. **Return structured results**: Always include `timestamp`, `success`, error information
3. **Break sleeps into chunks**: 1-5 minute chunks provide responsive shutdown
4. **Error isolation**: Catch exceptions in execute method, don't let them break the loop
5. **Validate intervals**: Check bounds in constructor
6. **Log execution results**: Info on success, warning/error on failure
7. **Store in app.state**: Makes cleanup during shutdown possible
8. **Implement graceful shutdown**: Always define stop() method
9. **Use preference manager**: For tuneable intervals in production
10. **Monitor via results**: Use execute results for observability/alerting

---

## Examples in Codebase

### Primary Usage

- `services/scheduler/blacklist_cleanup_job.py` - Token blacklist cleanup every 24 hours
- `services/scheduler/standup_reminder_job.py` - Standup reminders with timezone awareness, checks every hour

### Test Examples

- `tests/unit/scheduler/test_blacklist_cleanup_job.py` - Lifecycle, error handling
- `tests/unit/scheduler/test_standup_reminder_job.py` - Timezone logic, preference querying

### App Integration

- `web/startup.py` - Job initialization and lifecycle management
- `services/container/service_container.py` - Job dependency injection

---

## Implementation Checklist

- [ ] Create job class inheriting from pattern
- [ ] Implement `execute_[task]()` method with structured return
- [ ] Define `start()` with responsive sleep chunking
- [ ] Define `stop()` with graceful shutdown
- [ ] Define `is_running()` status check
- [ ] Validate interval bounds in constructor
- [ ] Add comprehensive logging at debug/info/warning/error levels
- [ ] Integrate with app.state for lifecycle management
- [ ] Add startup/shutdown event handlers
- [ ] Test lifecycle: start → execute → sleep chunks → stop
- [ ] Test error isolation: execute errors don't break loop
- [ ] Test responsive shutdown: stop() completes quickly
- [ ] Document execute method return structure
- [ ] Consider UserPreferenceManager integration for tuneable intervals

---

## Related Patterns

### Complements

- **[Pattern-017: Background Task Error Handling](pattern-017-background-task-error-handling.md)** - Error handling strategy for background tasks
- **[Pattern-018: Configuration Access](pattern-018-configuration-access.md)** - How to configure job intervals
- **[Pattern-021: Development Session Management](pattern-021-development-session-management.md)** - Session-based job scheduling

### Alternatives

- **[Pattern-015: Internal Task Handler](pattern-015-internal-task-handler.md)** - For event-driven task processing instead of periodic
- **Temporal Workflow Orchestration** - For complex multi-step workflows with retries and dependencies
- **APScheduler** - For cron-like scheduling with advanced features
- **Celery/RQ** - For distributed task queues with worker coordination

### Dependencies

- **Asyncio** - Core async runtime (Python standard library)
- **Structlog** - For consistent logging
- **Pattern-013: Session Management** - For database access in execute methods

---

## Evidence

**Proven Pattern** - Successfully implemented in:

1. **BlacklistCleanupJob** (24-hour interval)
   - Location: `services/scheduler/blacklist_cleanup_job.py`
   - Status: Active, production use
   - Interval: 24 hours with 5-minute sleep chunks
   - Lifecycle: start() loops, stop() with task cleanup

2. **StandupReminderJob** (hourly interval)
   - Location: `services/scheduler/standup_reminder_job.py`
   - Status: Active development
   - Interval: 1 hour (60-minute chunks)
   - Timezone-aware scheduling
   - Integration with UserPreferenceManager

**Test Coverage**:
- Lifecycle tests: startup, shutdown, is_running
- Error handling: execute() errors don't break loop
- Sleep chunking: responsive shutdown within 1-2 seconds
- Interval validation: bounds checking

**Production Characteristics**:
- Minimal overhead (native asyncio)
- Responsive to shutdown (1-minute chunks)
- Observable via structured results
- Graceful error handling

---

_Pattern Identified: December 2025_
_Ratified: January 10, 2026_
_Category: Infrastructure & Scheduling_
