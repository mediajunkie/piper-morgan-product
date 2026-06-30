"""
Response Flow Integration
Ensures workflow results reach Slack with spatial awareness and proper error handling.

This module handles the flow of responses from workflows back to Slack channels/threads,
preserving spatial coordinates and providing comprehensive error handling.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from uuid import UUID

from services.domain.models import Workflow, WorkflowResult
from services.integrations.slack.config_service import SlackConfigService
from services.integrations.slack.slack_client import SlackResponse
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

logger = logging.getLogger(__name__)


@dataclass
class ResponseTarget:
    """Target information for Slack response"""

    channel_id: str
    thread_ts: Optional[str] = None
    workspace_id: Optional[str] = None
    user_id: Optional[str] = None


@dataclass
class ResponseContent:
    """Content for Slack response"""

    text: str
    attachments: Optional[List[Dict[str, Any]]] = None
    blocks: Optional[List[Dict[str, Any]]] = None
    response_type: str = "in_channel"  # in_channel, ephemeral


class ResponseFlowIntegration:
    """Handles response flow from workflows to Slack"""

    def __init__(self, config_service: SlackConfigService):
        self.config_service = config_service
        self.logger = logging.getLogger(__name__)
        self._response_queue: List[Dict[str, Any]] = []
        self._max_retries = 3
        self._retry_delay = 1.0  # seconds

    async def process_workflow_result(
        self, workflow: Workflow, workflow_result: WorkflowResult
    ) -> bool:
        """Process workflow result and send response to Slack"""
        try:
            # Extract response target from workflow context
            response_target = self._extract_response_target(workflow)
            if not response_target:
                self.logger.warning(f"No response target found for workflow {workflow.id}")
                return False

            # Generate response content from workflow result
            response_content = self._generate_response_content(workflow, workflow_result)

            # Send response to Slack
            success = await self._send_response_to_slack(response_target, response_content)

            if success:
                self.logger.info(
                    f"Successfully sent response for workflow {workflow.id} to {response_target.channel_id}"
                )
            else:
                self.logger.error(f"Failed to send response for workflow {workflow.id}")

            return success

        except Exception as e:
            self.logger.error(f"Error processing workflow result: {e}", exc_info=True)
            return False

    def _extract_response_target(self, workflow: Workflow) -> Optional[ResponseTarget]:
        """Extract response target from workflow context"""
        try:
            # Check for spatial context first
            spatial_context = workflow.context.get("spatial_context", {})
            if spatial_context:
                return ResponseTarget(
                    channel_id=spatial_context.get("room_id"),
                    thread_ts=spatial_context.get("spatial_coordinates", {}).get("path_id"),
                    workspace_id=spatial_context.get("territory_id"),
                )

            # Check for response_target in context
            response_target_data = workflow.context.get("response_target", {})
            if response_target_data:
                return ResponseTarget(
                    channel_id=response_target_data.get("channel_id"),
                    thread_ts=response_target_data.get("thread_ts"),
                    workspace_id=response_target_data.get("workspace_id"),
                    user_id=response_target_data.get("user_id"),
                )

            # Check for spatial integration context
            spatial_integration = workflow.context.get("spatial_integration", {})
            if spatial_integration:
                return ResponseTarget(
                    channel_id=spatial_integration.get("room_id"),
                    thread_ts=spatial_integration.get("spatial_coordinates", {}).get("path_id"),
                    workspace_id=spatial_integration.get("territory_id"),
                )

            return None

        except Exception as e:
            self.logger.error(f"Error extracting response target: {e}")
            return None

    def _generate_response_content(
        self, workflow: Workflow, workflow_result: WorkflowResult
    ) -> ResponseContent:
        """Generate response content from workflow result"""
        try:
            # Extract message from workflow result
            if workflow_result.success:
                message = workflow_result.data.get("message", "Workflow completed successfully.")

                # Add workflow details if available
                if workflow_result.data.get("workflow_details"):
                    message += f"\n\nWorkflow Details: {workflow_result.data['workflow_details']}"

                # Add task results if available
                if workflow_result.data.get("task_results"):
                    task_summary = self._summarize_task_results(
                        workflow_result.data["task_results"]
                    )
                    message += f"\n\n{task_summary}"
            else:
                message = f"Workflow encountered an issue: {workflow_result.error}"
                if workflow_result.data.get("recovery_suggestion"):
                    message += f"\n\nSuggestion: {workflow_result.data['recovery_suggestion']}"

            # Add spatial context if available
            spatial_context = workflow.context.get("spatial_context", {})
            if spatial_context:
                attention_level = spatial_context.get("attention_level", "medium")
                if attention_level == "high":
                    message = f"🔔 {message}"  # Add notification indicator for high attention

            return ResponseContent(
                text=message,
                response_type="in_channel",
            )

        except Exception as e:
            self.logger.error(f"Error generating response content: {e}")
            return ResponseContent(
                text="An error occurred while processing the workflow result.",
                response_type="ephemeral",
            )

    def _summarize_task_results(self, task_results: List[Dict[str, Any]]) -> str:
        """Summarize task results for response"""
        if not task_results:
            return ""

        summary_parts = []
        for task in task_results:
            task_name = task.get("name", "Unknown Task")
            status = task.get("status", "unknown")

            if status == "completed":
                summary_parts.append(f"✅ {task_name}")
            elif status == "failed":
                summary_parts.append(f"❌ {task_name}")
            else:
                summary_parts.append(f"⏳ {task_name}")

        return "Task Summary:\n" + "\n".join(summary_parts)

    async def _send_response_to_slack(
        self, response_target: ResponseTarget, response_content: ResponseContent
    ) -> bool:
        """Send response to Slack with retry logic"""
        # #1110: a Slack API call requires a user_id (ADR-058 multi-tenancy).
        # The response target carries the owning user; without it we cannot
        # resolve credentials, so fail clearly rather than pass None downstream.
        if not response_target.user_id:
            self.logger.error(
                "Cannot send Slack response: response_target.user_id is missing "
                "(required for multi-tenant credential lookup, #1110)."
            )
            return False

        for attempt in range(self._max_retries):
            try:
                async with SlackIntegrationRouter(self.config_service) as slack_client:
                    # Prepare message parameters
                    message_params = {
                        "channel": response_target.channel_id,
                        "text": response_content.text,
                        "response_type": response_content.response_type,
                        "user_id": response_target.user_id,
                    }

                    # Add thread_ts if available
                    if response_target.thread_ts:
                        message_params["thread_ts"] = response_target.thread_ts

                    # Add attachments if available
                    if response_content.attachments:
                        message_params["attachments"] = response_content.attachments

                    # Add blocks if available
                    if response_content.blocks:
                        message_params["blocks"] = response_content.blocks

                    # Send message
                    response = await slack_client.send_message(**message_params)

                    if response.success:
                        return True
                    else:
                        self.logger.warning(
                            f"Slack API error on attempt {attempt + 1}: {response.error.message if response.error else 'Unknown error'}"
                        )

            except Exception as e:
                self.logger.error(f"Error sending response to Slack on attempt {attempt + 1}: {e}")

            # Wait before retry (exponential backoff)
            if attempt < self._max_retries - 1:
                await asyncio.sleep(self._retry_delay * (2**attempt))

        return False

    async def send_error_response(
        self,
        response_target: ResponseTarget,
        error_message: str,
        error_details: Optional[Dict] = None,
    ) -> bool:
        """Send error response to Slack"""
        try:
            error_content = ResponseContent(
                text=f"❌ {error_message}",
                response_type="ephemeral",
            )

            if error_details:
                error_content.text += f"\n\nDetails: {error_details}"

            return await self._send_response_to_slack(response_target, error_content)

        except Exception as e:
            self.logger.error(f"Error sending error response: {e}")
            return False

    async def send_acknowledgment(
        self, response_target: ResponseTarget, acknowledgment_message: str
    ) -> bool:
        """Send acknowledgment message to Slack"""
        try:
            ack_content = ResponseContent(
                text=f"✅ {acknowledgment_message}",
                response_type="ephemeral",
            )

            return await self._send_response_to_slack(response_target, ack_content)

        except Exception as e:
            self.logger.error(f"Error sending acknowledgment: {e}")
            return False

    def queue_response(
        self, response_target: ResponseTarget, response_content: ResponseContent, priority: int = 1
    ):
        """Queue response for later processing"""
        self._response_queue.append(
            {
                "target": response_target,
                "content": response_content,
                "priority": priority,
                "timestamp": asyncio.get_event_loop().time(),
            }
        )

    async def process_queued_responses(self) -> int:
        """Process all queued responses"""
        if not self._response_queue:
            return 0

        # Sort by priority and timestamp
        self._response_queue.sort(key=lambda x: (-x["priority"], x["timestamp"]))

        processed_count = 0
        failed_count = 0

        for response_item in self._response_queue:
            try:
                success = await self._send_response_to_slack(
                    response_item["target"], response_item["content"]
                )
                if success:
                    processed_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                self.logger.error(f"Error processing queued response: {e}")
                failed_count += 1

        # Clear processed responses
        self._response_queue.clear()

        self.logger.info(f"Processed {processed_count} responses, {failed_count} failed")
        return processed_count
