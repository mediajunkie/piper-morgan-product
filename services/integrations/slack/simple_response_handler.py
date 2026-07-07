"""
Simplified Slack Response Handler
Foundation Repair: Eliminate global state and complex consolidation patterns
Implements immediate response pattern with circuit breaker protection

Issue #620: Grammar-conscious Slack responses
"""

import logging
import time
from typing import Any, Dict, Optional

from services.domain.models import Intent, SpatialEvent

# Issue #620: Grammar-conscious response components
from services.integrations.slack.response_context import SlackResponseContext
from services.integrations.slack.slack_client import SlackClient
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.integrations.slack.spatial_types import AttentionLevel, EmotionalValence
from services.intent_service.classifier import IntentClassifier
from services.shared_types import IntentCategory, InteractionSpace

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """Simple circuit breaker to prevent cascade failures"""

    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise e


class SimpleSlackResponseHandler:
    """
    Simplified Slack Response Handler with immediate response pattern.

    Eliminates:
    - Global state management
    - Message consolidation buffers
    - Complex timing logic
    - Memory leak patterns

    Implements:
    - Immediate response pattern
    - Circuit breaker protection
    - Clear error propagation
    - Single responsibility principle
    """

    def __init__(
        self,
        spatial_adapter: SlackSpatialAdapter,
        intent_classifier: IntentClassifier,
        slack_client: SlackClient,
        intent_service: Optional[Any] = None,
    ):
        self.spatial_adapter = spatial_adapter
        self.intent_classifier = intent_classifier
        self._intent_service = intent_service
        self.slack_client = slack_client
        self.logger = logging.getLogger(__name__)

        # Simple circuit breaker for integration protection
        self.circuit_breaker = CircuitBreaker()

        # Simple duplicate detection (session-scoped, not global)
        self.processed_events = set()
        self.session_start = time.time()

        self.logger.info("SimpleSlackResponseHandler initialized with immediate response pattern")
        self.logger.info("Grammar-conscious response components initialized (#620)")

    async def handle_spatial_event(self, spatial_event: SpatialEvent) -> Optional[Dict[str, Any]]:
        """
        Process spatial event with immediate response pattern.

        Single responsibility: spatial_event → response
        No consolidation, no global state, clear error propagation
        """
        try:
            # Step 1: Get Slack context (circuit breaker protected)
            slack_context = await self._get_slack_context_safely(spatial_event)
            if not slack_context:
                return None

            # Step 2: Simple duplicate detection (session-scoped)
            if self._is_duplicate_event_simple(slack_context):
                self.logger.info(f"Skipping duplicate event for session: {spatial_event.id}")
                return None

            # Step 3: Create intent
            intent = await self._create_intent_safely(spatial_event, slack_context)
            if not intent:
                return None

            # Step 4: Process through orchestration
            result = await self._process_safely(intent, slack_context)
            if not result:
                return None

            # Step 5: Send immediate response
            return await self._send_response_safely(result, slack_context)

        except Exception as e:
            self.logger.error(f"Error handling spatial event {spatial_event.id}: {e}")
            # Send error response if possible
            return await self._send_error_response(spatial_event, str(e))

    async def _get_slack_context_safely(
        self, spatial_event: SpatialEvent
    ) -> Optional[Dict[str, Any]]:
        """Get Slack context with circuit breaker protection"""
        try:
            return self.circuit_breaker.call(
                self._get_slack_context_from_spatial_event, spatial_event
            )
        except Exception as e:
            self.logger.error(f"Failed to get Slack context: {e}")
            return None

    async def _get_slack_context_from_spatial_event(
        self, spatial_event: SpatialEvent
    ) -> Optional[Dict[str, Any]]:
        """Get original Slack context from spatial event using adapter"""
        if spatial_event.object_position is None:
            self.logger.warning(f"Spatial event {spatial_event.id} has no object_position")
            return None

        # Find Slack timestamp by position
        slack_timestamp = None
        async with self.spatial_adapter._lock:
            for timestamp, position in self.spatial_adapter._timestamp_to_position.items():
                if position == spatial_event.object_position:
                    slack_timestamp = timestamp
                    break

        if not slack_timestamp:
            self.logger.warning(
                f"No Slack timestamp found for position {spatial_event.object_position}"
            )
            return None

        # Get response context
        response_context = await self.spatial_adapter.get_response_context(slack_timestamp)
        if not response_context:
            return None

        # Enrich with spatial event details
        response_context.update(
            {
                "spatial_event_type": spatial_event.event_type,
                "spatial_position": spatial_event.object_position,
                "actor_id": spatial_event.actor_id,
                "original_timestamp": slack_timestamp,
            }
        )

        return response_context

    def _is_duplicate_event_simple(self, slack_context: Dict[str, Any]) -> bool:
        """Simple session-scoped duplicate detection without global state"""
        event_id = (
            slack_context.get("original_timestamp")
            or slack_context.get("ts")
            or slack_context.get("client_msg_id")
            or ""
        )

        if not event_id:
            return False

        if event_id in self.processed_events:
            return True

        self.processed_events.add(event_id)

        # Simple cleanup: clear if session is old (1 hour)
        if time.time() - self.session_start > 3600:
            self.processed_events.clear()
            self.session_start = time.time()
            self.logger.info("Cleared session event cache")

        return False

    async def _create_intent_safely(
        self, spatial_event: SpatialEvent, slack_context: Dict[str, Any]
    ) -> Optional[Intent]:
        """Create intent with circuit breaker protection"""
        try:
            return self.circuit_breaker.call(
                self._create_intent_from_spatial_event, spatial_event, slack_context
            )
        except Exception as e:
            self.logger.error(f"Failed to create intent: {e}")
            return None

    async def _create_intent_from_spatial_event(
        self, spatial_event: SpatialEvent, slack_context: Dict[str, Any]
    ) -> Optional[Intent]:
        """Create intent from spatial event with preserved Slack context"""
        # Extract message content
        message = slack_context.get("content", f"Spatial event: {spatial_event.event_type}")

        # Prepare spatial context
        spatial_context = {
            "room_id": slack_context.get("channel_id"),
            "territory_id": slack_context.get("workspace_id"),
            "path_id": slack_context.get("thread_ts"),
            "spatial_event_type": spatial_event.event_type,
            "attention_level": slack_context.get("attention_level", "medium"),
        }

        # Classify with spatial context
        intent = await self.intent_classifier.classify(
            message=message,
            context={"user_id": slack_context.get("user_id")},
            spatial_context=spatial_context,
            user_id=slack_context.get("user_id"),
        )

        # Enrich intent context with response targeting
        intent.context.update(
            {
                "response_target": {
                    "channel_id": slack_context.get("channel_id"),
                    "thread_ts": slack_context.get("thread_ts"),
                    "workspace_id": slack_context.get("workspace_id"),
                },
                "original_spatial_event": spatial_event.id,
            }
        )

        return intent

    async def _process_safely(
        self, intent: Intent, slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Process intent through orchestration with circuit breaker protection"""
        try:
            return self.circuit_breaker.call(
                self._process_through_orchestration, intent, slack_context
            )
        except Exception as e:
            self.logger.error(f"Failed to process intent: {e}")
            return None

    async def _process_through_orchestration(
        self, intent: Intent, slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Dispatch intent through intent_service direct dispatch (post-#1094)."""
        # Only create workflows for EXECUTION intents
        if intent.category != IntentCategory.EXECUTION:
            return {
                "type": "simple_response",
                "content": self._get_simple_response_for_intent(intent, slack_context),
                "intent": intent,
            }

        # #1094 γ-preserve (2026-05-15): EXECUTION intents dispatched via
        # intent_service direct dispatch (was: engine.create_workflow_from_intent
        # + execute_workflow, which silently failed for 8 of 14 WorkflowTypes).
        try:
            message = intent.original_message or intent.context.get("message", "")
            if not message:
                self.logger.warning(
                    f"No message available for intent {intent.action}; cannot dispatch"
                )
                return None

            slack_user_id = (slack_context or {}).get("user_id")
            slack_session_id = (
                (slack_context or {}).get("thread_ts")
                or (slack_context or {}).get("channel_id")
                or "slack-default"
            )

            result = await self.intent_service.process_intent(
                message=message,
                session_id=slack_session_id,
                user_id=slack_user_id,
            )

            if result is None or not getattr(result, "success", False):
                return None

            return {
                "type": "workflow_result",
                "result": {"message": getattr(result, "message", "")},
                "intent": intent,
            }
        except Exception as e:
            self.logger.error(f"intent_service direct dispatch failed: {e}")
            return {
                "type": "error_response",
                "content": "I encountered an issue processing your request. Please try again.",
                "intent": intent,
            }

    @property
    def intent_service(self):
        """Lazy-load IntentService to avoid circular-import-at-construction issues.

        #1094 γ-preserve: IntentService is the canonical dispatch path for
        EXECUTION intents (replacing the engine + WorkflowFactory chain).
        """
        if self._intent_service is None:
            from services.intent.intent_service import IntentService

            self._intent_service = IntentService()
        return self._intent_service

    def _get_simple_response_for_intent(
        self, intent: Intent, slack_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate grammar-conscious responses for non-execution intents.

        Issue #620: Responses now adapt to Place and context.
        """
        action = intent.action.lower()

        # Build response context for grammar-conscious responses
        response_ctx = self._build_response_context(slack_context)
        formality = response_ctx.get_formality() if response_ctx else "professional"
        is_dm = response_ctx.place == InteractionSpace.SLACK_DM if response_ctx else False

        if "help" in action:
            # Grammar-conscious: No robot emoji, warm language
            if is_dm:
                return "Happy to help! I can assist with creating tickets, analyzing data, and managing projects. What would you like to work on?"
            else:
                return "I can help with tickets, data analysis, and project management. What do you need?"
        elif "status" in action:
            # Grammar-conscious: Casual language, no technical prefix
            return "Everything's running smoothly."
        elif "hello" in action or "hi" in action or "greeting" in action:
            # Grammar-conscious: Context-aware greeting
            if is_dm:
                return "Hey! What can I help you with?"
            else:
                return "Hi there! What can I help with?"
        else:
            # Grammar-conscious: Humanized action, no technical prefix
            humanized_action = self._humanize_action(intent.action)
            if formality == "casual":
                return f"Got it, you want to {humanized_action}. How can I help?"
            else:
                return f"I understand you want to {humanized_action}. How can I help with that?"

    def _build_response_context(
        self, slack_context: Optional[Dict[str, Any]]
    ) -> Optional[SlackResponseContext]:
        """
        Build grammar-conscious response context from Slack context.

        Issue #620: Enables Place-aware responses.
        """
        if not slack_context:
            return None
        try:
            return SlackResponseContext.from_spatial_context(slack_context)
        except Exception as e:
            self.logger.warning(f"Failed to build response context: {e}")
            return None

    def _humanize_action(self, action: str) -> str:
        """Convert technical action to human-readable form."""
        # Common action mappings for Slack
        action_narratives = {
            "create_item": "create something",
            "create_ticket": "create a ticket",
            "create_issue": "create an issue",
            "search_documents": "search for documents",
            "search_files": "find files",
            "get_status": "check status",
            "list_todos": "see your todos",
            "add_todo": "add a todo",
            "complete_todo": "complete a todo",
        }
        return action_narratives.get(action, action.replace("_", " "))

    async def _send_response_safely(
        self, result: Dict[str, Any], slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Send response with circuit breaker protection"""
        try:
            return self.circuit_breaker.call(self._send_immediate_response, result, slack_context)
        except Exception as e:
            self.logger.error(f"Failed to send response: {e}")
            return None

    async def _send_immediate_response(
        self, result: Dict[str, Any], slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Send immediate response to Slack"""
        response_content = self._format_response_content(result, slack_context)
        if not response_content:
            return None

        # Prepare message parameters
        message_params = {
            "channel": slack_context.get("channel_id"),
            "text": response_content,
        }

        # Add thread targeting if in thread
        thread_ts = slack_context.get("thread_ts")
        if thread_ts:
            message_params["thread_ts"] = thread_ts

        # #1110: outbound credentials use the connector-owner's Piper user_id
        # (not the sender's Slack user_id).
        message_params["user_id"] = slack_context.get("connector_user_id") or slack_context.get(
            "user_id"
        )

        # Send message
        response = await self.slack_client.send_message(**message_params)

        self.logger.info(
            f"Sent immediate Slack response to channel {slack_context.get('channel_id')}"
        )

        return {
            "slack_response": response,
            "target_channel": slack_context.get("channel_id"),
            "thread_ts": thread_ts,
            "response_content": response_content,
        }

    def _format_response_content(
        self, result: Dict[str, Any], slack_context: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Format result into grammar-conscious response content.

        Issue #620: Uses warm language, avoids robot prefixes.
        """
        result_type = result.get("type")

        if result_type == "simple_response":
            return result.get("content")
        elif result_type == "error_response":
            # Grammar-conscious error: warm, not technical
            content = result.get("content", "")
            if "encountered an issue" in content.lower():
                return "I ran into a small hiccup with that. You could try rephrasing, or ask me something else."
            return content
        elif result_type == "workflow_result":
            workflow_result = result.get("result", {})
            if isinstance(workflow_result, dict):
                if "summary" in workflow_result:
                    # Grammar-conscious: Warm completion, not checkmark prefix
                    summary = workflow_result["summary"]
                    return f"Done! {summary}"
                elif "message" in workflow_result:
                    return workflow_result["message"]
            else:
                return str(workflow_result)

        return None

    async def _send_error_response(
        self, spatial_event: SpatialEvent, error_message: str
    ) -> Optional[Dict[str, Any]]:
        """Send error response if possible"""
        try:
            # Try to get basic context for error response
            # This is a fallback, so we use simpler logic
            return {
                "type": "error_response",
                "content": "I encountered an unexpected error processing your request.",
                "error": error_message,
                "spatial_event_id": spatial_event.id,
            }
        except Exception:
            # If even error response fails, just log and return None
            self.logger.error(f"Could not send error response for event {spatial_event.id}")
            return None

    async def get_handler_stats(self) -> Dict[str, Any]:
        """Get statistics about simplified handler performance"""
        return {
            "handler_type": "SimpleSlackResponseHandler",
            "session_start_time": self.session_start,
            "processed_events_count": len(self.processed_events),
            "circuit_breaker_state": self.circuit_breaker.state,
            "circuit_breaker_failures": self.circuit_breaker.failure_count,
            "components": {
                "spatial_adapter": True,
                "intent_classifier": True,
                "intent_service": True,
                "slack_client": True,
                "circuit_breaker": True,
            },
        }
