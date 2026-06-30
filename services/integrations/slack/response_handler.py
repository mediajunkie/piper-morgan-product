"""
Slack Response Handler
Spatial-to-Intent bridge maintaining metaphor purity for complete integration flow.

This handler processes spatial events through the complete Piper Morgan pipeline:
1. Receives spatial events with integer positions
2. Maps back to Slack context via adapter
3. Creates intents from spatial events
4. Dispatches EXECUTION intents via intent_service direct dispatch (task_type
   registry, Pattern-072) — #1094 deleted the prior OrchestrationEngine chain
5. Routes responses back to Slack with proper targeting
"""

import logging
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

import structlog

from services.domain.models import Intent, SpatialEvent
from services.integrations.slack.slack_client import SlackClient
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.intent_service.classifier import IntentClassifier
from services.shared_types import IntentCategory

logger = logging.getLogger(__name__)

# Circuit breaker for duplicate events (Emergency Fix 1)
PROCESSED_EVENTS: Set[str] = set()
LAST_CLEANUP = time.time()

# Rate limiting for workflow creation (Emergency Fix 3)
from collections import defaultdict

WORKFLOW_RATE_LIMIT = defaultdict(list)  # user_id -> timestamps
MAX_WORKFLOWS_PER_MINUTE = 3

# PM-079-SUB: Message consolidation tracking
MESSAGE_CONSOLIDATION_BUFFER: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
CONSOLIDATION_TIMEOUT = 5.0  # seconds
CONSOLIDATION_MAX_MESSAGES = 5


async def is_duplicate_event(slack_context: Dict[str, Any]) -> bool:
    """
    Check if we've already processed this Slack event to prevent runaway workflows.

    Emergency fix to prevent processing the same Slack event multiple times
    which was causing 80+ unwanted GitHub issues.
    """
    global LAST_CLEANUP

    # Get unique event identifier from Slack context
    event_id = (
        slack_context.get("original_timestamp")
        or slack_context.get("ts")
        or slack_context.get("client_msg_id")
        or ""
    )

    if not event_id:
        logger.warning("No event ID found in Slack context - allowing processing")
        return False

    # Check if already processed
    if event_id in PROCESSED_EVENTS:
        logger.warning(f"🚨 EMERGENCY CIRCUIT BREAKER: Duplicate event detected: {event_id}")
        return True

    # Add to processed set
    PROCESSED_EVENTS.add(event_id)
    logger.info(f"✅ Event {event_id} marked as processed ({len(PROCESSED_EVENTS)} total)")

    # Cleanup old events every 5 minutes to prevent memory leak
    current_time = time.time()
    if current_time - LAST_CLEANUP > 300:  # 5 minutes
        if len(PROCESSED_EVENTS) > 100:
            # Keep only recent 50 events
            PROCESSED_EVENTS.clear()
            LAST_CLEANUP = current_time
            logger.info("🧹 Cleared processed events cache to prevent memory leak")

    return False


def check_workflow_rate_limit(user_id: str) -> bool:
    """
    Check if user has exceeded workflow creation rate limit.

    Emergency fix to prevent workflow spam causing 80+ unwanted GitHub issues.
    """
    current_time = time.time()
    user_timestamps = WORKFLOW_RATE_LIMIT[user_id]

    # Remove timestamps older than 1 minute
    user_timestamps[:] = [ts for ts in user_timestamps if current_time - ts < 60]

    # Check if under limit
    if len(user_timestamps) >= MAX_WORKFLOWS_PER_MINUTE:
        logger.warning(
            f"🚨 EMERGENCY RATE LIMIT: User {user_id} exceeded {MAX_WORKFLOWS_PER_MINUTE} workflows per minute"
        )
        return False

    # Add current timestamp
    user_timestamps.append(current_time)
    logger.info(
        f"✅ Workflow rate check passed for user {user_id} ({len(user_timestamps)}/{MAX_WORKFLOWS_PER_MINUTE})"
    )
    return True


class SlackResponseHandler:
    """
    Handles complete flow from spatial events to Slack responses.

    Maintains spatial metaphor purity by using adapter for context mapping
    while enabling full integration with Piper Morgan's intent and orchestration systems.
    """

    def __init__(
        self,
        spatial_adapter: Optional[SlackSpatialAdapter] = None,
        intent_classifier: Optional[IntentClassifier] = None,
        slack_client: Optional[SlackClient] = None,
        intent_service: Optional[Any] = None,
    ):
        """Initialize SlackResponseHandler with dependency injection and graceful fallbacks.

        #1094 (2026-05-15): EXECUTION-intent dispatch flows through ``intent_service``
        (direct dispatch via task_type registry, Pattern-072). Lazy-initialized on
        first use to avoid circular-import-at-construction issues with the intent
        module.
        """
        logger = structlog.get_logger()

        try:
            # Initialize spatial adapter with fallback
            if spatial_adapter is None:
                logger.info("Initializing SlackSpatialAdapter with defaults")
                spatial_adapter = SlackSpatialAdapter()
            self.spatial_adapter = spatial_adapter

            # Initialize intent classifier with fallback
            if intent_classifier is None:
                logger.info("Initializing IntentClassifier with defaults")
                intent_classifier = IntentClassifier()
            self.intent_classifier = intent_classifier

            self._intent_service = intent_service

            # Initialize Slack client with fallback.
            # #1110: SlackClient requires a user_id at construction (ADR-058),
            # but this handler is built once with no user context (user_id is
            # per inbound event, available later in slack_context). So the
            # default client is the SlackIntegrationRouter — a startup singleton
            # that builds its per-user SlackClient lazily per send. This also
            # matches the production path, where SlackWebhookRouter injects the
            # router here. The send sites pass user_id from slack_context.
            if slack_client is None:
                logger.info("Initializing SlackIntegrationRouter with defaults")
                from services.integrations.slack.config_service import SlackConfigService
                from services.integrations.slack.slack_integration_router import (
                    SlackIntegrationRouter,
                )

                config_service = SlackConfigService()
                slack_client = SlackIntegrationRouter(config_service)
            self.slack_client = slack_client

            # Keep original logger for backward compatibility
            self.logger = logging.getLogger(__name__)

            logger.info("SlackResponseHandler initialized successfully with dependency injection")

        except ImportError as e:
            logger.error(f"Failed to import required Slack dependencies: {e}")
            logger.warning("SlackResponseHandler will operate in degraded mode")
            # Set minimal defaults to prevent hanging
            self.spatial_adapter = None
            self.intent_classifier = None
            self._intent_service = None
            self.slack_client = None
            self.logger = logging.getLogger(__name__)

        except Exception as e:
            logger.error(f"Failed to initialize SlackResponseHandler dependencies: {e}")
            from services.api.errors import SlackInitializationError

            raise SlackInitializationError(
                f"SlackResponseHandler initialization failed: {e}"
            ) from e

    @property
    def intent_service(self):
        """Lazy-load IntentService to avoid circular-import-at-construction issues.

        #1094 γ-preserve: IntentService is the canonical dispatch path for
        EXECUTION intents (replacing the engine + WorkflowFactory chain that
        silently failed for 8 of 14 WorkflowTypes).
        """
        if self._intent_service is None:
            from services.intent.intent_service import IntentService

            self._intent_service = IntentService()
        return self._intent_service

    def _get_consolidation_key(self, slack_context: Dict[str, Any]) -> str:
        """Generate unique key for message consolidation based on channel and thread"""
        channel_id = slack_context.get("channel_id", "unknown")
        thread_ts = slack_context.get("thread_ts", "main")
        return f"{channel_id}:{thread_ts}"

    def _add_to_consolidation_buffer(
        self, message_data: Dict[str, Any], slack_context: Dict[str, Any]
    ) -> None:
        """Add message to consolidation buffer for potential grouping"""
        consolidation_key = self._get_consolidation_key(slack_context)
        message_data["timestamp"] = time.time()
        MESSAGE_CONSOLIDATION_BUFFER[consolidation_key].append(message_data)

        # Limit buffer size
        if len(MESSAGE_CONSOLIDATION_BUFFER[consolidation_key]) > CONSOLIDATION_MAX_MESSAGES:
            MESSAGE_CONSOLIDATION_BUFFER[consolidation_key] = MESSAGE_CONSOLIDATION_BUFFER[
                consolidation_key
            ][-CONSOLIDATION_MAX_MESSAGES:]

        self.logger.debug(f"Added message to consolidation buffer for {consolidation_key}")

    def _should_consolidate_messages(self, consolidation_key: str) -> bool:
        """Determine if messages should be consolidated based on timing and count"""
        messages = MESSAGE_CONSOLIDATION_BUFFER.get(consolidation_key, [])
        if len(messages) < 2:
            return False

        # Check if messages are within consolidation timeout
        current_time = time.time()
        recent_messages = [
            msg for msg in messages if current_time - msg["timestamp"] <= CONSOLIDATION_TIMEOUT
        ]

        return len(recent_messages) >= 2

    def _format_consolidated_message(
        self, messages: List[Dict[str, Any]], slack_context: Dict[str, Any]
    ) -> str:
        """Format multiple messages into a single consolidated response"""
        if not messages:
            return ""

        # Extract main workflow result (most recent or most important)
        main_message = messages[-1]  # Most recent
        main_content = main_message.get("content", "")

        # Count different types of messages
        workflow_results = [msg for msg in messages if msg.get("type") == "workflow_result"]
        simple_responses = [
            msg for msg in messages if msg.get("type") in ["simple_response", "query_response"]
        ]

        # Build consolidated message
        consolidated_parts = []

        # Main workflow completion message
        if workflow_results:
            main_workflow = workflow_results[-1]
            workflow_content = main_workflow.get("content", "")
            if workflow_content:
                consolidated_parts.append(f"🤖 {workflow_content}")

        # Add summary of additional actions
        if len(messages) > 1:
            additional_count = len(messages) - 1
            if additional_count == 1:
                consolidated_parts.append("   📋 1 additional action completed")
            else:
                consolidated_parts.append(f"   📋 {additional_count} additional actions completed")

        # Add thread/reaction hint for detailed information
        if len(messages) > 1:
            consolidated_parts.append("   💬 Reply with 'details' for full breakdown")

        return "\n".join(consolidated_parts)

    def _clear_consolidation_buffer(self, consolidation_key: str) -> None:
        """Clear consolidation buffer for a specific key"""
        if consolidation_key in MESSAGE_CONSOLIDATION_BUFFER:
            del MESSAGE_CONSOLIDATION_BUFFER[consolidation_key]
            self.logger.debug(f"Cleared consolidation buffer for {consolidation_key}")

    async def _send_consolidated_response(
        self, slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Send consolidated response if conditions are met"""
        consolidation_key = self._get_consolidation_key(slack_context)

        if not self._should_consolidate_messages(consolidation_key):
            return None

        messages = MESSAGE_CONSOLIDATION_BUFFER[consolidation_key]
        consolidated_content = self._format_consolidated_message(messages, slack_context)

        if not consolidated_content:
            return None

        # Prepare Slack message parameters
        message_params = {
            "channel": slack_context.get("channel_id"),
            "text": consolidated_content,
        }

        # Add thread targeting if in thread
        thread_ts = slack_context.get("thread_ts")
        if thread_ts:
            message_params["thread_ts"] = thread_ts

        # #1110: resolve outbound credentials by the CONNECTOR-OWNER's Piper
        # user_id (not the sender's Slack user_id). Harmless for a raw
        # SlackClient (ignores the kwarg; user_id was bound at construction).
        message_params["user_id"] = slack_context.get("connector_user_id") or slack_context.get(
            "user_id"
        )

        # Send consolidated message
        response = await self.slack_client.send_message(**message_params)

        # Clear buffer after sending
        self._clear_consolidation_buffer(consolidation_key)

        self.logger.info(
            f"Sent consolidated response ({len(messages)} messages) to channel {slack_context.get('channel_id')}"
        )

        return {
            "slack_response": response,
            "target_channel": slack_context.get("channel_id"),
            "thread_ts": thread_ts,
            "response_content": consolidated_content,
            "consolidated_count": len(messages),
        }

    async def handle_spatial_event(self, spatial_event: SpatialEvent) -> Optional[Dict[str, Any]]:
        """
        Process spatial event through complete integration flow.

        Args:
            spatial_event: SpatialEvent with integer positioning from spatial adapter

        Returns:
            Response result if successful, None if no response needed
        """
        try:
            # Step 1: Get original Slack context from adapter using object position
            slack_context = await self._get_slack_context_from_spatial_event(spatial_event)
            if not slack_context:
                self.logger.warning(f"No Slack context found for spatial event {spatial_event.id}")
                return None

            # EMERGENCY FIX 1: Check for duplicate events to prevent runaway workflows
            if await is_duplicate_event(slack_context):
                self.logger.info(
                    f"🚨 SKIPPING duplicate event - prevented runaway workflow for {spatial_event.id}"
                )
                return None

            # Step 2: Create intent from spatial event with preserved context
            intent = await self._create_intent_from_spatial_event(spatial_event, slack_context)
            if not intent:
                self.logger.debug(f"No intent created for spatial event {spatial_event.event_type}")
                return None

            self.logger.info(
                f"SLACK_PIPELINE: Intent classified as {intent.category.value} - "
                f"Action: {intent.action}, Confidence: {intent.confidence:.2f}, "
                f"Channel: {slack_context.get('channel_id')}"
            )

            # Step 3: Dispatch via intent_service (post-#1094 direct dispatch)
            workflow_result = await self._process_through_orchestration(intent, slack_context)
            if not workflow_result:
                self.logger.debug(f"No workflow result for intent {intent.action}")
                return None

            self.logger.info(
                f"SLACK_PIPELINE: Workflow creation result: SUCCESS - "
                f"Type: {workflow_result.get('type', 'unknown')}, "
                f"Workflow ID: {workflow_result.get('workflow_id', 'N/A')}"
            )

            # Step 4: Send response back to Slack with proper targeting
            response_result = await self._send_slack_response(workflow_result, slack_context)

            self.logger.info(
                f"✅ COMPLETE INTEGRATION SUCCESS: {spatial_event.event_type} -> "
                f"{intent.action} -> workflow -> response sent to {slack_context.get('channel_id')}"
            )

            return response_result

        except Exception as e:
            self.logger.error(f"Error handling spatial event {spatial_event.id}: {e}")
            return None

    async def _get_slack_context_from_spatial_event(
        self, spatial_event: SpatialEvent
    ) -> Optional[Dict[str, Any]]:
        """
        Get original Slack context from spatial event using adapter.

        Maps from spatial event's object_position back to Slack timestamp,
        then retrieves full context for response routing.
        """
        try:
            # Use object_position to find original Slack timestamp via adapter
            if spatial_event.object_position is None:
                self.logger.warning(f"Spatial event {spatial_event.id} has no object_position")
                return None

            # Get all position mappings to find the one matching our spatial event
            # Since we need reverse lookup by position, we'll search through adapter mappings
            slack_timestamp = None

            # Check adapter's position mappings to find matching timestamp
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

            # Get full response context from adapter
            response_context = await self.spatial_adapter.get_response_context(slack_timestamp)
            if not response_context:
                self.logger.warning(f"No response context found for timestamp {slack_timestamp}")
                return None

            # Enrich with spatial event details
            response_context.update(
                {
                    "spatial_event_type": spatial_event.event_type,
                    "spatial_position": spatial_event.object_position,
                    "territory_position": spatial_event.territory_position,
                    "room_position": spatial_event.room_position,
                    "path_position": spatial_event.path_position,
                    "actor_id": spatial_event.actor_id,
                    "significance_level": spatial_event.significance_level,
                    "original_timestamp": slack_timestamp,
                }
            )

            return response_context

        except Exception as e:
            self.logger.error(f"Error getting Slack context from spatial event: {e}")
            return None

    async def _create_intent_from_spatial_event(
        self, spatial_event: SpatialEvent, slack_context: Dict[str, Any]
    ) -> Optional[Intent]:
        """
        Create intent from spatial event with preserved Slack context.

        Uses enhanced IntentClassifier with spatial context to maintain
        the spatial intelligence throughout the intent classification process.
        """
        try:
            # Determine message content for classification
            message = self._extract_message_from_context(slack_context)
            if not message:
                # Generate synthetic message from spatial event
                message = f"Spatial event: {spatial_event.event_type}"

            # Prepare spatial context for enhanced classification
            spatial_context = {
                "room_id": slack_context.get("channel_id"),
                "territory_id": slack_context.get("workspace_id"),
                "path_id": slack_context.get("thread_ts"),
                "spatial_event_type": spatial_event.event_type,
                "attention_level": slack_context.get("attention_level", "medium"),
                "emotional_valence": slack_context.get("emotional_valence", "neutral"),
                "navigation_intent": slack_context.get("navigation_intent", "monitor"),
                "spatial_coordinates": {
                    "territory_position": spatial_event.territory_position,
                    "room_position": spatial_event.room_position,
                    "path_position": spatial_event.path_position,
                    "object_position": spatial_event.object_position,
                },
            }

            # Classify with spatial context using enhanced IntentClassifier
            intent = await self.intent_classifier.classify(
                message=message,
                context={"user_id": slack_context.get("user_id")},
                spatial_context=spatial_context,
            )

            # Enrich intent context with response targeting
            intent.context.update(
                {
                    "response_target": {
                        "channel_id": slack_context.get("channel_id"),
                        "thread_ts": slack_context.get("thread_ts"),
                        "workspace_id": slack_context.get("workspace_id"),
                    },
                    "spatial_context": spatial_context,
                    "original_spatial_event": spatial_event.id,
                }
            )

            self.logger.debug(
                f"Created intent {intent.action} from spatial event {spatial_event.event_type} "
                f"with confidence {intent.confidence}"
            )

            return intent

        except Exception as e:
            self.logger.error(f"Error creating intent from spatial event: {e}")
            return None

    async def _process_through_orchestration(
        self, intent: Intent, slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Dispatch intent through intent_service (post-#1094 direct dispatch).

        Routes intent through intent_service.process_intent (task_type registry,
        Pattern-072) while preserving spatial context for response generation.
        The prior OrchestrationEngine chain was deleted in #1094.
        """
        try:
            # EMERGENCY FIX 2: Only create workflows for EXECUTION intents
            # This prevents "help" and other simple queries from creating unwanted GitHub issues
            if intent.category != IntentCategory.EXECUTION:
                self.logger.info(
                    f"🚨 EMERGENCY FILTER: Preventing workflow creation for {intent.category.value} intent: {intent.action}"
                )

                # Return appropriate simple response instead of creating workflow
                simple_response = self._get_simple_response_for_intent(intent)
                return {
                    "type": "simple_response",
                    "content": simple_response,
                    "intent": intent,
                }

            # EMERGENCY FIX 3: Check rate limit before creating workflows
            user_id = slack_context.get("user_id", "unknown")
            if not check_workflow_rate_limit(user_id):
                return {
                    "type": "rate_limit_response",
                    "content": "⏳ Please wait a moment before creating more workflows. I'm designed to prevent spam and ensure quality responses.",
                    "intent": intent,
                }

            # Only EXECUTION intents proceed to workflow creation
            self.logger.info(
                f"✅ WORKFLOW CREATION APPROVED: {intent.category.value} intent '{intent.action}' proceeding to orchestration"
            )

            # Skip QUERY intents that don't need orchestration (kept for backward compatibility)
            if intent.category == IntentCategory.QUERY:
                # For queries, generate direct response
                return {
                    "type": "query_response",
                    "content": await self._generate_query_response(intent, slack_context),
                    "intent": intent,
                }

            # Skip monitoring intents that should bypass orchestration
            if intent.action == "monitor_system" or intent.context.get("monitoring"):
                self.logger.debug(f"Bypassing orchestration for monitoring intent: {intent.action}")
                return {
                    "type": "monitoring_response",
                    "content": "Monitoring active - system status normal",
                    "intent": intent,
                }

            # Process EXECUTION and COMMAND intents through intent_service direct dispatch
            # via task_type registry (Pattern-072). The prior orchestration_engine path
            # silently failed for 8 of 14 WorkflowTypes (#1094, closed 2026-05-15).
            self.logger.debug(
                f"Processing {intent.category.value} intent '{intent.action}' via intent_service direct dispatch"
            )

            message = intent.original_message or intent.context.get("message", "")
            if not message:
                self.logger.warning(
                    f"No message available for intent {intent.action}; cannot dispatch"
                )
                return None

            slack_user_id = slack_context.get("user_id")
            slack_session_id = (
                slack_context.get("thread_ts") or slack_context.get("channel_id") or "slack-default"
            )

            try:
                result = await self.intent_service.process_intent(
                    message=message,
                    session_id=slack_session_id,
                    user_id=slack_user_id,
                )
            except Exception as exc:
                self.logger.error(
                    f"intent_service direct dispatch failed for intent " f"{intent.action}: {exc}",
                    exc_info=True,
                )
                return None

            if result is None or not getattr(result, "success", False):
                self.logger.warning(
                    f"intent_service dispatch returned no success for intent {intent.action}"
                )
                return None

            self.logger.info(
                f"✅ Successfully processed {intent.category.value} intent '{intent.action}' "
                f"via intent_service direct dispatch"
            )

            return {
                "type": "workflow_result",
                "result": {"message": getattr(result, "message", "")},
                "intent": intent,
            }

        except Exception as e:
            self.logger.error(f"Error processing intent through orchestration: {e}")
            return None

    async def _send_slack_response(
        self, workflow_result: Dict[str, Any], slack_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Send response back to Slack with proper targeting and message consolidation.

        Uses preserved Slack context to route response to correct
        channel/thread with spatial awareness and PM-079-SUB consolidation.
        """
        try:
            # Extract response content
            response_content = self._format_response_content(workflow_result)
            if not response_content:
                self.logger.debug("No response content to send")
                return None

            # Issue #1081: Append Notion-refs section if the incoming Slack
            # message contained Notion URLs that were successfully unfurled.
            # Per Pattern-073 discipline: only render refs that were actually
            # resolved (ok=True); honest-failure marker for the rest.
            notion_refs = slack_context.get("notion_refs", [])
            if notion_refs:
                from services.integrations.slack.notion_url_unfurler import (
                    format_notion_refs_for_slack,
                )

                refs_block = format_notion_refs_for_slack(notion_refs)
                if refs_block:
                    response_content = f"{response_content}\n\n{refs_block}"

            self.logger.info(
                f"SLACK_PIPELINE: Response generated: {response_content[:100]}{'...' if len(response_content) > 100 else ''}"
            )

            # PM-079-SUB: Add message to consolidation buffer
            message_data = {
                "content": response_content,
                "type": workflow_result.get("type", "unknown"),
                "workflow_result": workflow_result,
            }
            self._add_to_consolidation_buffer(message_data, slack_context)

            # Check if we should send consolidated response
            consolidated_response = await self._send_consolidated_response(slack_context)
            if consolidated_response:
                return consolidated_response

            # If no consolidation, send individual message
            # Prepare Slack message parameters with proper targeting
            message_params = {
                "channel": slack_context.get("channel_id"),
                "text": response_content,
            }

            # Add thread targeting if in thread
            thread_ts = slack_context.get("thread_ts")
            if thread_ts:
                message_params["thread_ts"] = thread_ts

            # #1110: outbound credentials use the connector-owner's Piper
            # user_id (not the sender's Slack user_id).
            message_params["user_id"] = slack_context.get(
                "connector_user_id"
            ) or slack_context.get("user_id")

            # Send message via Slack client
            response = await self.slack_client.send_message(**message_params)

            self.logger.info(
                f"Sent individual Slack response to channel {slack_context.get('channel_id')} "
                f"{'in thread' if thread_ts else 'in channel'}"
            )

            return {
                "slack_response": response,
                "target_channel": slack_context.get("channel_id"),
                "thread_ts": thread_ts,
                "response_content": response_content,
                "consolidated_count": 1,
            }

        except Exception as e:
            self.logger.error(f"Error sending Slack response: {e}")
            return None

    def _extract_message_from_context(self, slack_context: Dict[str, Any]) -> Optional[str]:
        """Extract original message content from Slack context"""
        # Try to get original message content from context
        content = slack_context.get("content")
        if content and isinstance(content, str):
            return content.strip()
        return None

    def _get_simple_response_for_intent(self, intent: Intent) -> str:
        """
        Generate simple responses for non-execution intents to prevent workflow creation.

        Emergency fix to prevent "help" and other queries from creating GitHub issues.
        """
        action = intent.action.lower()

        # Specific responses for common actions that were creating unwanted workflows
        if "help" in action:
            return "🤖 I'm Piper Morgan, your AI Product Management Assistant. I can help you create tickets, analyze data, and manage your projects. Try asking me to 'create a GitHub issue' or 'analyze project status'."
        elif "status" in action:
            return "📊 Current system status: All services operational. Slack integration active."
        elif "hello" in action or "hi" in action:
            return "👋 Hello! I'm here to assist with your product management tasks."
        elif "ping" in action:
            return "🏓 Pong! System is responsive."
        elif "test" in action:
            return "✅ Test successful. All systems operational."
        else:
            return f"🔍 I understand you want to {intent.action}. For complex tasks that require workflow creation, please be more specific about what you'd like me to execute."

    async def _generate_query_response(self, intent: Intent, slack_context: Dict[str, Any]) -> str:
        """Generate response content for query intents"""
        # Simple query response generation - could be enhanced with knowledge base
        action = intent.action

        if "status" in action.lower():
            return "📊 Current system status: All services operational"
        elif "help" in action.lower():
            return "🤖 I'm Piper Morgan, your AI Product Management Assistant. How can I help you today?"
        else:
            return f"🔍 I understand you want to {action}. Let me look into that for you."

    def _format_response_content(self, workflow_result: Dict[str, Any]) -> Optional[str]:
        """Format workflow result into response content"""
        result_type = workflow_result.get("type")

        if result_type == "simple_response":
            return workflow_result.get("content")
        elif result_type == "rate_limit_response":
            return workflow_result.get("content")
        elif result_type == "query_response":
            return workflow_result.get("content")
        elif result_type == "monitoring_response":
            return workflow_result.get("content")
        elif result_type == "workflow_result":
            result = workflow_result.get("result", {})
            if isinstance(result, dict):
                # Extract meaningful content from workflow result
                if "summary" in result:
                    return f"✅ {result['summary']}"
                elif "message" in result:
                    return result["message"]
                else:
                    # PM-079: Don't send generic success messages - prevents spam
                    logger.debug(
                        f"No specific message for workflow result, suppressing notification"
                    )
                    return None
            else:
                return str(result)

        return None

    async def get_handler_stats(self) -> Dict[str, Any]:
        """Get statistics about response handler performance"""
        # Calculate consolidation statistics
        total_buffered_messages = sum(
            len(messages) for messages in MESSAGE_CONSOLIDATION_BUFFER.values()
        )
        active_consolidation_keys = len(MESSAGE_CONSOLIDATION_BUFFER)

        return {
            "handler_type": "SlackResponseHandler",
            "adapter_stats": await self.spatial_adapter.get_mapping_stats(),
            "components": {
                "spatial_adapter": True,
                "intent_classifier": True,
                "intent_service": True,
                "slack_client": True,
            },
            "consolidation_stats": {
                "active_buffers": active_consolidation_keys,
                "total_buffered_messages": total_buffered_messages,
                "consolidation_timeout": CONSOLIDATION_TIMEOUT,
                "max_messages_per_buffer": CONSOLIDATION_MAX_MESSAGES,
            },
        }

    async def get_detailed_message_breakdown(self, slack_context: Dict[str, Any]) -> Optional[str]:
        """Get detailed breakdown of consolidated messages for user request"""
        consolidation_key = self._get_consolidation_key(slack_context)
        messages = MESSAGE_CONSOLIDATION_BUFFER.get(consolidation_key, [])

        if not messages:
            return "No detailed information available."

        breakdown_parts = ["📋 **Detailed Message Breakdown:**"]

        for i, message in enumerate(messages, 1):
            msg_type = message.get("type", "unknown")
            content = message.get("content", "")
            timestamp = message.get("timestamp", 0)

            breakdown_parts.append(f"{i}. **{msg_type}**: {content}")
            if timestamp:
                time_str = time.strftime("%H:%M:%S", time.localtime(timestamp))
                breakdown_parts.append(f"   ⏰ {time_str}")

        return "\n".join(breakdown_parts)
