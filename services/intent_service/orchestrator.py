"""
Intent orchestration for multi-substantive intent handling.

Issue #764: GLUE-MULTIINTENT — Multi-Intent Handling Enhancements

Provides:
- ExecutionPlan for planning multi-intent execution
- IntentOrchestrator for executing multiple intents and aggregating responses
- Graceful fallback on partial failure
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

import structlog

from services.domain.models import Intent
from services.intent_service.pre_classifier import MultiIntentResult

logger = structlog.get_logger()

# Maximum intents to process in a single message
MAX_INTENTS = 4


class ExecutionStrategy(str, Enum):
    """How to execute multiple intents."""

    PARALLEL = "parallel"  # All intents can run independently (default)
    SEQUENTIAL = "sequential"  # Intents have dependencies


@dataclass
class ExecutionPlan:
    """Plan for executing multiple intents from a single message."""

    intents: List[Intent]
    strategy: ExecutionStrategy = ExecutionStrategy.PARALLEL
    original_message: str = ""
    has_greeting: bool = False
    capped: bool = False  # True if intents were capped at MAX_INTENTS

    @property
    def intent_count(self) -> int:
        return len(self.intents)


@dataclass
class IntentExecutionResult:
    """Result of executing a single intent within an orchestrated plan."""

    intent: Intent
    response: str = ""
    intent_data: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None
    duration_ms: float = 0.0


@dataclass
class OrchestratedResponse:
    """Aggregated response from executing multiple intents."""

    results: List[IntentExecutionResult] = field(default_factory=list)
    aggregated_message: str = ""
    has_partial_failure: bool = False
    total_duration_ms: float = 0.0
    greeting_prefix: bool = False

    @property
    def successful_results(self) -> List[IntentExecutionResult]:
        return [r for r in self.results if r.success]

    @property
    def failed_results(self) -> List[IntentExecutionResult]:
        return [r for r in self.results if not r.success]

    @property
    def primary_intent_data(self) -> Dict[str, Any]:
        """Get intent_data from first successful result."""
        for result in self.results:
            if result.success:
                return result.intent_data
        return {}


class IntentOrchestrator:
    """
    Orchestrates execution of multiple intents from a single message.

    Receives a MultiIntentResult with 2+ substantive intents, creates an
    execution plan, runs each through existing handlers, and aggregates
    the responses into a single coherent message.

    Per Chief Architect guidance: handlers stay single-intent; this layer
    orchestrates and aggregates.
    """

    def __init__(self, canonical_handlers):
        """
        Args:
            canonical_handlers: CanonicalHandlers instance for dispatching intents
        """
        self._handlers = canonical_handlers

    def create_plan(self, multi_result: MultiIntentResult) -> ExecutionPlan:
        """
        Create an execution plan from a multi-intent result.

        Caps at MAX_INTENTS and determines execution strategy.
        All execution is parallel by default (no dependency detection yet).
        """
        intents = list(multi_result.intents)
        capped = len(intents) > MAX_INTENTS

        if capped:
            logger.warning(
                "multi_intent_capped",
                original_count=len(intents),
                max_intents=MAX_INTENTS,
            )
            intents = intents[:MAX_INTENTS]

        plan = ExecutionPlan(
            intents=intents,
            strategy=ExecutionStrategy.PARALLEL,
            original_message=multi_result.original_message,
            has_greeting=multi_result.has_greeting,
            capped=capped,
        )

        logger.info(
            "execution_plan_created",
            intent_count=plan.intent_count,
            strategy=plan.strategy.value,
            has_greeting=plan.has_greeting,
            capped=capped,
        )

        return plan

    async def execute_plan(
        self,
        plan: ExecutionPlan,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> OrchestratedResponse:
        """
        Execute all intents in the plan and aggregate responses.

        Currently executes sequentially (async for each) since handlers
        may share state. Can be upgraded to asyncio.gather for true parallel.
        """
        start_time = time.monotonic()
        results: List[IntentExecutionResult] = []

        for intent in plan.intents:
            result = await self._execute_single(intent, session_id, user_id)
            results.append(result)

        total_ms = (time.monotonic() - start_time) * 1000
        has_failure = any(not r.success for r in results)

        response = OrchestratedResponse(
            results=results,
            has_partial_failure=has_failure,
            total_duration_ms=total_ms,
            greeting_prefix=plan.has_greeting,
        )

        # Aggregate the messages
        response.aggregated_message = self._aggregate_messages(response)

        logger.info(
            "orchestrated_execution_complete",
            total_intents=len(results),
            successful=len(response.successful_results),
            failed=len(response.failed_results),
            duration_ms=round(total_ms, 1),
        )

        return response

    async def _execute_single(
        self,
        intent: Intent,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> IntentExecutionResult:
        """Execute a single intent through canonical handlers."""
        start_time = time.monotonic()

        try:
            if not self._handlers.can_handle(intent):
                return IntentExecutionResult(
                    intent=intent,
                    success=False,
                    error=f"No handler for category: {intent.category.value}",
                    duration_ms=(time.monotonic() - start_time) * 1000,
                )

            result = await self._handlers.handle(intent, session_id, user_id)
            duration_ms = (time.monotonic() - start_time) * 1000

            return IntentExecutionResult(
                intent=intent,
                response=result.get("message", ""),
                intent_data=result.get("intent", {}),
                success=True,
                duration_ms=duration_ms,
            )

        except Exception as e:
            duration_ms = (time.monotonic() - start_time) * 1000
            logger.warning(
                "intent_execution_failed",
                category=intent.category.value,
                action=intent.action,
                error=str(e),
                duration_ms=round(duration_ms, 1),
            )
            return IntentExecutionResult(
                intent=intent,
                success=False,
                error=str(e),
                duration_ms=duration_ms,
            )

    def _aggregate_messages(self, response: OrchestratedResponse) -> str:
        """
        Aggregate multiple intent responses into a single coherent message.

        Uses natural transitions between responses. Handles partial failures
        by noting what couldn't be processed.
        """
        successful = response.successful_results
        failed = response.failed_results

        if not successful:
            return "I'm having trouble processing that right now. You could try rephrasing your request, or ask about something specific like your calendar or tasks."

        # Build the aggregated message
        parts: List[str] = []

        # Add greeting prefix if detected
        if response.greeting_prefix:
            parts.append("Hi there!")

        # Single successful result — no aggregation needed
        if len(successful) == 1 and not failed:
            if parts:
                parts.append(successful[0].response)
                return " ".join(parts)
            return successful[0].response

        # Multiple successful results — use transitions
        transitions = [
            "As for {topic}",
            "Regarding {topic}",
            "On the {topic} front",
        ]

        for i, result in enumerate(successful):
            if i == 0:
                parts.append(result.response)
            else:
                topic = _intent_topic_label(result.intent)
                transition = transitions[i % len(transitions)].format(topic=topic)
                parts.append(f"{transition}, {_lowercase_first(result.response)}")

        # Note any failures
        if failed:
            failure_topics = [_intent_topic_label(r.intent) for r in failed]
            if len(failure_topics) == 1:
                # #1198: no false retry promise — nothing retries in the background.
                parts.append(
                    f"I wasn't able to check on {failure_topics[0]} right now — ask me again and I'll retry."
                )
            else:
                topics = ", ".join(failure_topics)
                # #1198: no false retry promise — nothing retries in the background.
                parts.append(f"I wasn't able to check on {topics} right now — ask me again and I'll retry.")

        return " ".join(parts)


def _intent_topic_label(intent: Intent) -> str:
    """Get a human-readable topic label for an intent."""
    labels = {
        "meeting_time": "your calendar",
        "week_calendar": "your calendar",
        "recurring_meetings": "your calendar",
        "get_project_status": "project status",
        "get_top_priority": "priorities",
        "get_contextual_guidance": "guidance",
        "get_identity": "that",
        "get_capabilities": "that",
        "list_todos_query": "your todos",
        "github_query": "GitHub",
        "productivity_query": "productivity",
        "get_current_time": "the time",
        "explain_trust": "trust",
        "get_memory": "memory",
        "manage_portfolio": "your portfolio",
    }
    return labels.get(intent.action, intent.action.replace("_", " "))


def _lowercase_first(text: str) -> str:
    """Lowercase the first character of a string (for natural transitions)."""
    if not text:
        return text
    # Don't lowercase if starts with a proper noun indicator (capital after article)
    # or common abbreviations
    if text[:2] in ("I ", "I'"):
        return text
    return text[0].lower() + text[1:]
