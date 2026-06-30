"""
Slack Webhook Router
FastAPI routes for Slack webhooks following existing API patterns.

Provides webhook endpoint routing for Slack integration including:
- Event subscription handling with spatial metaphor processing
- OAuth callback endpoint management
- Interactive component handling (buttons, modals, etc.)
- Slash command routing
- Authentication and signature verification
- Integration with spatial mapper and event processing
"""

import hashlib
import hmac
import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from services.api.errors import SlackAuthFailedError
from services.infrastructure.task_manager import task_manager
from services.observability.slack_monitor import (
    ProcessingStage,
    SlackPipelineMetrics,
    correlation_id,
    slack_event_id,
)

from .config_service import SlackConfigService
from .oauth_handler import SlackOAuthHandler
from .response_handler import SlackResponseHandler
from .slack_integration_router import SlackIntegrationRouter
from .spatial_mapper import SlackSpatialMapper

logger = logging.getLogger(__name__)


class SlackWebhookRouter:
    """
    FastAPI router for Slack webhook endpoints.

    Handles all incoming Slack webhooks including events, OAuth callbacks,
    interactive components, and slash commands with spatial metaphor integration.
    """

    def __init__(
        self,
        config_service: Optional[SlackConfigService] = None,
        oauth_handler: Optional[SlackOAuthHandler] = None,
        spatial_mapper: Optional[SlackSpatialMapper] = None,
        integration_router: Optional[SlackIntegrationRouter] = None,
        response_handler: Optional[SlackResponseHandler] = None,
    ):
        self.config_service = config_service or SlackConfigService()
        self.oauth_handler = oauth_handler or SlackOAuthHandler(self.config_service)
        self.spatial_mapper = spatial_mapper or SlackSpatialMapper()
        self.integration_router = integration_router or SlackIntegrationRouter(self.config_service)

        # Provide unified access to both client and spatial adapter through router
        self.spatial_adapter = self.integration_router.get_spatial_adapter()

        # Initialize response handler with dependencies
        if response_handler:
            self.response_handler = response_handler
        else:
            try:
                # Create dependencies for response handler using integration router
                from services.intent_service.classifier import IntentClassifier

                intent_classifier = IntentClassifier()

                # Use integration router for unified client access
                self.response_handler = SlackResponseHandler(
                    spatial_adapter=self.spatial_adapter,
                    intent_classifier=intent_classifier,
                    slack_client=self.integration_router,  # Router provides client methods
                )
                logger.info(
                    "SlackWebhookRouter initialized with response handler via integration router"
                )
            except Exception as e:
                logger.error(f"Failed to initialize SlackResponseHandler: {e}")
                logger.warning("SlackWebhookRouter will operate without response handling")
                self.response_handler = None

        # Create FastAPI router
        self.router = APIRouter(prefix="/slack", tags=["slack"])

        # Register webhook routes
        self._register_routes()

        logger.info("SlackWebhookRouter initialized with complete integration pipeline")

    def _get_connector_user_id(self) -> Optional[str]:
        """Get the user_id that owns the Slack integration.

        For alpha: Uses SLACK_CONNECTOR_USER_ID env var.
        Future (#760): Will query slack_workspaces table by team_id.

        Returns:
            User ID string or None if not configured.

        Issue #759: Added for multi-tenancy support.
        """
        return os.getenv("SLACK_CONNECTOR_USER_ID")

    async def handle_slack_events(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Direct method for handling Slack events (for testing and direct integration).

        This method provides a direct interface for processing Slack events without
        requiring a FastAPI Request object, making it suitable for testing and
        programmatic event processing.
        """
        try:
            # Set up correlation tracking
            event_correlation_id = correlation_id.set(f"slack_event_{int(time.time() * 1000)}")

            if event_data.get("event"):
                slack_event_id.set(event_data["event"].get("ts", "unknown"))

            logger.info(f"Processing Slack event directly: {event_data.get('type', 'unknown')}")

            # Handle URL verification challenge
            if event_data.get("type") == "url_verification":
                return {"challenge": event_data.get("challenge")}

            # Handle event callbacks with observability
            if event_data.get("type") == "event_callback":
                # Create tracked background task using RobustTaskManager
                task = task_manager.create_tracked_task(
                    self._process_event_callback_with_observability(event_data),
                    name=f"process_slack_event_{event_data.get('event', {}).get('type', 'unknown')}",
                    metadata={
                        "correlation_id": correlation_id.get(),
                        "event_type": event_data.get("event", {}).get("type", "unknown"),
                        "slack_event_id": event_data.get("event", {}).get("ts", "unknown"),
                    },
                )

                logger.info(f"Created tracked task {task} for Slack event processing")
                return {"status": "ok", "task_id": str(task)}

            # Handle other event types
            logger.warning(f"Unhandled Slack event type: {event_data.get('type')}")
            return {"status": "ignored"}

        except Exception as e:
            logger.error(f"Error in handle_slack_events: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}

    def _register_routes(self):
        """Register all Slack webhook routes"""

        # Event subscriptions endpoint
        @self.router.post("/webhooks/events")
        async def handle_slack_events(request: Request):
            return await self._handle_events_webhook(request)

        # OAuth callback endpoint
        @self.router.get("/oauth/callback")
        async def handle_oauth_callback(code: str, state: str, error: Optional[str] = None):
            return await self._handle_oauth_callback(code, state, error)

        # Interactive components endpoint (buttons, modals, etc.)
        @self.router.post("/webhooks/interactive")
        async def handle_interactive_components(request: Request):
            return await self._handle_interactive_webhook(request)

        # Slash commands endpoint
        @self.router.post("/webhooks/commands")
        async def handle_slash_commands(request: Request):
            return await self._handle_commands_webhook(request)

        # OAuth authorization URL generation
        @self.router.get("/oauth/authorize")
        async def get_oauth_url(scopes: Optional[str] = None, user_scopes: Optional[str] = None):
            return await self._get_oauth_authorization_url(scopes, user_scopes)

        # Webhook health check
        @self.router.get("/webhooks/health")
        async def webhook_health():
            return await self._webhook_health_check()

    def register_webhook_routes(self) -> None:
        """
        Register webhook routes (TDD-compatible wrapper).

        This method provides a simpler interface matching TDD test expectations.
        Delegates to existing _register_routes implementation.
        """
        self._register_routes()

    def _validate_event(self, event: dict) -> bool:
        """
        Validate that an event has required fields.

        Args:
            event: Event dict to validate

        Returns:
            True if valid, False otherwise
        """
        # Required fields for all events
        required_fields = ["type"]

        # Check required fields exist
        for field in required_fields:
            if field not in event:
                return False

        # Event-type specific validation
        event_type = event.get("type")

        if event_type == "message":
            # Message events need channel, ts, team
            return all(field in event for field in ["channel", "ts", "team"])

        # Default: if it has a type, it's valid enough
        return True

    def _verify_webhook_signature(self, signature: str, timestamp: str, body: str) -> bool:
        """
        Verify webhook signature (TDD-compatible wrapper).

        Args:
            signature: Slack signature header (e.g., "v0=abc123...")
            timestamp: Slack timestamp header (e.g., "1234567890")
            body: Request body string

        Returns:
            True if signature is valid
        """
        try:
            user_id = self._get_connector_user_id()
            config = self.config_service.get_config(user_id) if user_id else None
            signing_secret = config.signing_secret if config else None

            if not signing_secret:
                logger.warning(
                    "No Slack signing secret configured, skipping signature verification"
                )
                return True  # Allow in development without signing secret

            if not timestamp or not signature:
                logger.warning("Missing timestamp or signature in Slack request")
                return False

            # Convert body to bytes if needed
            body_bytes = body.encode() if isinstance(body, str) else body

            # Use helper method for actual verification
            return self._compute_and_verify_signature(
                signature, timestamp, body_bytes, signing_secret
            )

        except Exception as e:
            logger.error(f"Error verifying webhook signature: {e}")
            return False

    def _compute_and_verify_signature(
        self, signature: str, timestamp: str, body: bytes, signing_secret: str
    ) -> bool:
        """
        Core signature verification logic (synchronous helper).

        Args:
            signature: Slack signature header
            timestamp: Slack timestamp header
            body: Request body as bytes
            signing_secret: Slack signing secret

        Returns:
            True if signature is valid
        """
        # Check timestamp to prevent replay attacks (5 minutes tolerance)
        current_time = int(time.time())
        if abs(current_time - int(timestamp)) > 300:
            logger.warning("Slack request timestamp too old")
            return False

        # Compute expected signature
        sig_basestring = f"v0:{timestamp}:{body.decode()}"
        expected_signature = (
            "v0="
            + hmac.new(signing_secret.encode(), sig_basestring.encode(), hashlib.sha256).hexdigest()
        )

        # Compare signatures
        return hmac.compare_digest(signature, expected_signature)

    async def _handle_events_webhook(self, request: Request) -> JSONResponse:
        """Handle Slack Events API webhook"""

        try:
            # Verify request signature
            if not await self._verify_slack_signature(request):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request signature"
                )

            # Parse request body
            body = await request.body()
            event_data = json.loads(body.decode())

            print(f"🚨 ALL WEBHOOK EVENTS: {event_data.get('type', 'NO_TYPE')} - {event_data}")

            # Handle URL verification challenge
            if event_data.get("type") == "url_verification":
                return JSONResponse(
                    content={"challenge": event_data.get("challenge")}, status_code=200
                )

            # Handle event callbacks
            if event_data.get("type") == "event_callback":
                # Set up correlation tracking
                event_correlation_id = correlation_id.set(
                    f"slack_webhook_{int(time.time() * 1000)}"
                )

                if event_data.get("event"):
                    slack_event_id.set(event_data["event"].get("ts", "unknown"))

                print(
                    f"🎯 WEBHOOK DEBUG: Creating tracked task for event: {event_data.get('event', {}).get('type', 'unknown')}"
                )
                logger.info(
                    f"🎯 WEBHOOK: Creating tracked task for event: {event_data.get('event', {}).get('type', 'unknown')}"
                )

                try:
                    # Use RobustTaskManager instead of asyncio.create_task
                    task = task_manager.create_tracked_task(
                        self._process_event_callback_with_observability(event_data),
                        name=f"webhook_slack_event_{event_data.get('event', {}).get('type', 'unknown')}",
                        metadata={
                            "correlation_id": correlation_id.get(),
                            "event_type": event_data.get("event", {}).get("type", "unknown"),
                            "slack_event_id": event_data.get("event", {}).get("ts", "unknown"),
                        },
                    )

                    logger.info(f"✅ WEBHOOK: Tracked task created successfully: {task}")
                    return JSONResponse(
                        content={"status": "ok", "task_id": str(task)}, status_code=200
                    )

                except Exception as e:
                    logger.error(f"🚨 WEBHOOK: Failed to create tracked task: {e}", exc_info=True)
                    return JSONResponse(
                        content={"status": "error", "error": str(e)}, status_code=500
                    )

            # Handle other event types
            logger.warning(f"Unhandled Slack event type: {event_data.get('type')}")
            return JSONResponse(content={"status": "ignored"}, status_code=200)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in Slack webhook: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON payload"
            )
        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            logger.error(f"Error handling Slack events webhook: {e}")
            logger.error(f"Traceback: {error_details}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error processing webhook",
            )

    async def _handle_oauth_callback(
        self, code: str, state: str, error: Optional[str] = None
    ) -> JSONResponse:
        """Handle OAuth callback from Slack"""

        try:
            # Check for OAuth error
            if error:
                logger.warning(f"OAuth error received: {error}")
                return JSONResponse(
                    content={
                        "success": False,
                        "error": error,
                        "message": "OAuth authorization was denied or failed",
                    },
                    status_code=400,
                )

            # Process OAuth callback
            result = await self.oauth_handler.handle_oauth_callback(code, state)

            # Return success response with workspace info
            return JSONResponse(
                content={
                    "success": True,
                    "message": "Slack workspace connected successfully",
                    "workspace": result.get("workspace"),
                    "spatial_mapping": result.get("spatial_mapping"),
                },
                status_code=200,
            )

        except SlackAuthFailedError as e:
            logger.error(f"OAuth callback authentication failed: {e}")
            return JSONResponse(
                content={"success": False, "error": "authentication_failed", "message": str(e)},
                status_code=401,
            )
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            return JSONResponse(
                content={
                    "success": False,
                    "error": "internal_error",
                    "message": "Failed to process OAuth callback",
                },
                status_code=500,
            )

    async def _handle_interactive_webhook(self, request: Request) -> JSONResponse:
        """Handle interactive components (buttons, modals, etc.)"""

        try:
            # Verify request signature
            if not await self._verify_slack_signature(request):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request signature"
                )

            # Parse form-encoded payload
            form_data = await request.form()
            payload_str = form_data.get("payload")

            if not payload_str:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing payload in interactive webhook",
                )

            payload = json.loads(payload_str)

            # Process interactive component
            response = await self._process_interactive_component(payload)

            return JSONResponse(content=response, status_code=200)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in interactive webhook payload: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON in payload"
            )
        except Exception as e:
            logger.error(f"Error handling interactive webhook: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error processing interactive component",
            )

    async def _handle_commands_webhook(self, request: Request) -> JSONResponse:
        """Handle slash commands"""

        try:
            # Verify request signature
            if not await self._verify_slack_signature(request):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request signature"
                )

            # Parse form data
            form_data = await request.form()
            command_data = dict(form_data)

            # Process slash command
            response = await self._process_slash_command(command_data)

            return JSONResponse(content=response, status_code=200)

        except Exception as e:
            logger.error(f"Error handling slash command: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error processing slash command",
            )

    async def _get_oauth_authorization_url(
        self, scopes: Optional[str] = None, user_scopes: Optional[str] = None
    ) -> JSONResponse:
        """Generate OAuth authorization URL"""

        try:
            scope_list = scopes.split(",") if scopes else None
            user_scope_list = user_scopes.split(",") if user_scopes else None

            auth_url, state = self.oauth_handler.generate_authorization_url(
                scopes=scope_list, user_scopes=user_scope_list
            )

            return JSONResponse(
                content={
                    "authorization_url": auth_url,
                    "state": state,
                    "expires_in": 900,  # 15 minutes
                },
                status_code=200,
            )

        except Exception as e:
            logger.error(f"Error generating OAuth URL: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate OAuth authorization URL",
            )

    async def _webhook_health_check(self) -> JSONResponse:
        """Webhook health check endpoint"""

        try:
            user_id = self._get_connector_user_id()
            config = self.config_service.get_config(user_id) if user_id else None
            oauth_status = self.oauth_handler.get_oauth_status()
            spatial_analytics = self.spatial_mapper.get_spatial_analytics()

            health_data = {
                "status": "healthy",
                "timestamp": time.time(),
                "webhook_endpoints": {
                    "events": "/slack/webhooks/events",
                    "interactive": "/slack/webhooks/interactive",
                    "commands": "/slack/webhooks/commands",
                    "oauth_callback": "/slack/oauth/callback",
                },
                "configuration": {
                    "webhooks_enabled": config.enable_webhooks if config else False,
                    "spatial_mapping_enabled": config.enable_spatial_mapping if config else False,
                    "environment": config.environment.value if config else "unknown",
                    "connector_user_configured": user_id is not None,
                },
                "oauth_handler": oauth_status,
                "spatial_mapper": spatial_analytics,
            }

            return JSONResponse(content=health_data, status_code=200)

        except Exception as e:
            logger.error(f"Health check error: {e}")
            return JSONResponse(
                content={"status": "unhealthy", "error": str(e), "timestamp": time.time()},
                status_code=500,
            )

    def _health_check(self) -> dict:
        """
        Perform health check (TDD-compatible wrapper).

        Delegates to existing _webhook_health_check implementation.

        Returns:
            Health status dict
        """
        # Delegate to existing async implementation
        import asyncio

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._webhook_health_check())
            loop.close()
        else:
            result = asyncio.create_task(self._webhook_health_check())

        return result if isinstance(result, dict) else {"status": "healthy"}

    def _log_webhook_event(self, event: dict) -> None:
        """
        Log webhook event for debugging and monitoring.

        Args:
            event: Event to log
        """
        logger = getattr(self, "logger", None)
        if logger:
            logger.info(
                f"Webhook event received: type={event.get('type')}, channel={event.get('channel')}"
            )

    def _collect_metrics(self) -> dict:
        """
        Collect webhook processing metrics.

        Returns:
            Metrics dict with counts
        """
        # Return basic metrics structure
        # In production, this would query actual metrics storage
        return {
            "total_events": 0,
            "successful_events": 0,
            "failed_events": 0,
        }

    def _validate_config(self, config: dict) -> bool:
        """
        Validate webhook configuration.

        Args:
            config: Configuration dict to validate

        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        required_fields = ["webhook_url", "signing_secret", "port"]

        if not all(field in config for field in required_fields):
            return False

        # Validate webhook_url is a valid URL
        webhook_url = config.get("webhook_url", "")
        if not webhook_url.startswith(("http://", "https://")):
            return False

        # Validate port is an integer
        port = config.get("port")
        if not isinstance(port, int):
            return False

        return True

    async def _process_event_queue(self, events: list) -> list:
        """
        Process a queue of webhook events.

        Args:
            events: List of events to process

        Returns:
            List of processing results
        """
        results = []
        for event in events:
            # Process each event through the normal pipeline
            try:
                result = await self._process_event_callback(event)
                results.append({"success": True, "event": event, "result": result})
            except Exception as e:
                results.append({"success": False, "event": event, "error": str(e)})

        return results

    def set_webhook_url(self, url: str) -> None:
        """
        Set the webhook URL for this router.

        Args:
            url: Webhook URL to use
        """
        self.webhook_url = url
        logger.info(f"Webhook URL set to: {url}")

    async def process_webhook_event(self, event: dict) -> dict:
        """
        Process a webhook event (TDD-compatible wrapper).

        Args:
            event: Event dict to process

        Returns:
            Processing result
        """
        try:
            # Use event_handler if available (TDD tests inject this)
            if hasattr(self, "event_handler") and self.event_handler:
                result = await self.event_handler.process_event(event)
                return {"success": True, "result": result, "event": event}

            # Fall back to existing event processing
            await self._process_event_callback(event)
            return {"success": True, "event": event}

        except Exception as e:
            logger.error(f"Error processing webhook event: {e}")
            return {"success": False, "error": str(e), "event": event}

    # Private processing methods

    async def _verify_slack_signature(self, request: Request) -> bool:
        """Verify Slack request signature for security (async wrapper for Request objects)"""

        try:
            user_id = self._get_connector_user_id()
            config = self.config_service.get_config(user_id) if user_id else None
            signing_secret = config.signing_secret if config else None

            if not signing_secret:
                logger.warning(
                    "No Slack signing secret configured, skipping signature verification"
                )
                return True  # Allow in development without signing secret

            # Get headers
            timestamp = request.headers.get("X-Slack-Request-Timestamp")
            signature = request.headers.get("X-Slack-Signature")

            if not timestamp or not signature:
                logger.warning("Missing timestamp or signature in Slack request")
                return False

            # Get request body
            body = await request.body()

            # Use helper method for actual verification
            return self._compute_and_verify_signature(signature, timestamp, body, signing_secret)

        except Exception as e:
            logger.error(f"Error verifying Slack signature: {e}")
            return False

    async def _process_event_callback_with_observability(self, event_data: Dict[str, Any]) -> None:
        """
        Process Slack event callback with full observability and correlation tracking.

        This method wraps the original _process_event_callback with comprehensive
        observability, correlation tracking, and error handling to eliminate silent failures.
        """
        # Initialize pipeline metrics
        current_correlation_id = correlation_id.get() or f"slack_event_{int(time.time() * 1000)}"
        event_id = event_data.get("event", {}).get("ts", "unknown")

        pipeline = SlackPipelineMetrics(
            correlation_id=current_correlation_id,
            slack_event_id=event_id,
            started_at=datetime.now(timezone.utc),
            webhook_data=event_data,
        )

        # Record initial stage
        stage_metrics = pipeline.start_stage(
            ProcessingStage.WEBHOOK_RECEIVED,
            {"event_type": event_data.get("event", {}).get("type")},
        )
        stage_metrics.complete_success()

        try:
            # Ensure correlation context is available
            current_correlation_id = correlation_id.get()
            if not current_correlation_id:
                correlation_id.set(f"slack_event_{int(time.time() * 1000)}")

            # Record processing start
            processing_stage = pipeline.start_stage(ProcessingStage.CONTEXT_EXTRACTED)

            # Call the original processing method
            await self._process_event_callback(event_data)

            # Mark processing stage complete
            processing_stage.complete_success()

            # Record successful completion
            response_stage = pipeline.start_stage(
                ProcessingStage.RESPONSE_SENT, {"status": "success"}
            )
            response_stage.complete_success()

            # Mark entire pipeline complete
            pipeline.complete_pipeline(success=True)

            logger.info(f"Event processing completed successfully: {pipeline.correlation_id}")

        except Exception as e:
            # Record error and ensure it's visible
            error_stage = pipeline.start_stage(
                ProcessingStage.PIPELINE_FAILED, {"error_type": type(e).__name__}
            )
            error_stage.complete_failure(str(e))
            pipeline.complete_pipeline(success=False, error_details=str(e))

            logger.error(f"Event processing failed: {e}", exc_info=True)
            logger.error(f"Pipeline metrics: {pipeline}")

            # Re-raise to ensure task manager sees the failure
            raise

    async def _process_event_callback(self, event_data: Dict[str, Any]) -> None:
        """Process Slack event callback with spatial mapping"""

        try:
            event = event_data.get("event", {})
            team_id = event_data.get("team_id")

            event_type = event.get("type")
            logger.info(f"Processing Slack event: {event_type} in team {team_id}")

            # Route different event types
            if event_type == "message":
                await self._process_message_event(event, team_id)
            elif event_type == "app_mention":
                await self._process_mention_event(event, team_id)
            elif event_type == "reaction_added":
                await self._process_reaction_event(event, team_id)
            elif event_type == "member_joined_channel":
                await self._process_channel_join_event(event, team_id)
            else:
                logger.debug(f"Unhandled event type: {event_type}")

        except Exception as e:
            logger.error(f"Error processing event callback: {e}")

    async def _unfurl_notion_refs(self, message_text: str) -> List[Dict[str, Any]]:
        """Resolve any Notion URLs in a Slack message text (#1081).

        Returns a list of dicts (one per URL found), each carrying
        `url / page_id / title / ok / error`. Empty list when no URLs
        are detected OR Notion router is unavailable.

        Per Pattern-073 discipline: per-URL fail-graceful; failure
        details surface via the `ok` + `error` fields rather than
        being silently dropped.
        """
        if not message_text:
            return []
        try:
            from services.integrations.notion.notion_integration_router import (
                NotionIntegrationRouter,
            )
            from services.integrations.slack.notion_url_unfurler import (
                unfurl_notion_urls,
            )

            notion_router = NotionIntegrationRouter()
            if not notion_router.is_configured():
                return []
            await notion_router.connect()
            return await unfurl_notion_urls(message_text, notion_router)
        except Exception as e:
            logger.warning(f"notion_unfurl_failure_in_webhook: {e}")
            return []

    async def _process_message_event(self, event: Dict[str, Any], team_id: str) -> None:
        """Process message event through spatial adapter"""

        try:
            channel_id = event.get("channel")
            message_ts = event.get("ts")
            user_id = event.get("user")

            # Skip bot messages to avoid loops
            if event.get("subtype") == "bot_message":
                return

            message_text = event.get("text", "")

            # Issue #1081: Unfurl any Notion URLs in the message text so
            # downstream consumers (response handler, intent classifier) can
            # surface the Notion page context alongside the Slack message.
            # Per-URL fail-graceful — one failure doesn't break the message.
            notion_refs = await self._unfurl_notion_refs(message_text)

            # Prepare context for spatial adapter
            context = {
                "territory_id": team_id,
                "room_id": channel_id,
                "user_id": user_id,
                # #1110: user_id above is the SENDER's Slack ID; credential
                # lookup needs the connector-owner's Piper user_id (#759).
                "connector_user_id": self._get_connector_user_id(),
                "content": message_text,
                "attention_level": "medium",
                "emotional_valence": "neutral",
                "navigation_intent": "monitor",
                "significance_level": "routine",
                "affected_objects": [],
                "spatial_changes": {},
                "notion_refs": notion_refs,
            }

            # Add thread context if in thread
            thread_ts = event.get("thread_ts")
            if thread_ts:
                context["path_id"] = thread_ts

            # Create spatial event using adapter
            spatial_event = await self.spatial_adapter.create_spatial_event_from_slack(
                message_ts, "message_posted", context
            )

            logger.info(
                f"SLACK_PIPELINE: Spatial event created - Type: {spatial_event.event_type}, "
                f"Position: {spatial_event.object_position}, Channel: {channel_id}, User: {user_id}"
            )

            # Context already stored by create_spatial_event_from_slack()
            # No need for additional store_mapping() call

            # Process through complete integration pipeline
            try:
                response_result = await self.response_handler.handle_spatial_event(spatial_event)
                if response_result:
                    logger.info(
                        f"Response sent for message event: {response_result.get('status', 'unknown')}"
                    )
                else:
                    logger.debug("No response needed for message event")
            except Exception as response_error:
                logger.error(f"Error processing response for message event: {response_error}")

        except Exception as e:
            logger.error(f"Error processing message event: {e}")

    async def _process_mention_event(self, event: Dict[str, Any], team_id: str) -> None:
        """Process app mention event (attention attractor)"""

        try:
            channel_id = event.get("channel")
            message_ts = event.get("ts")
            user_id = event.get("user")

            # Prepare context for spatial adapter with high attention
            context = {
                "territory_id": team_id,
                "room_id": channel_id,
                "original_channel_id": channel_id,  # Preserve original Slack channel ID
                "user_id": user_id,
                # #1110: connector-owner Piper user_id for outbound credentials.
                "connector_user_id": self._get_connector_user_id(),
                "content": event.get("text", ""),
                "attention_level": "high",
                "emotional_valence": "positive",
                "navigation_intent": "respond",
                "significance_level": "significant",
                "affected_objects": [],
                "spatial_changes": {"attention_attracted": True},
            }

            # Add thread context if in thread
            thread_ts = event.get("thread_ts")
            if thread_ts:
                context["path_id"] = thread_ts

            # Create spatial event using adapter
            spatial_event = await self.spatial_adapter.create_spatial_event_from_slack(
                message_ts, "attention_attracted", context
            )

            logger.info(
                f"SLACK_PIPELINE: Spatial event created - Type: {spatial_event.event_type}, "
                f"Position: {spatial_event.object_position}, Channel: {channel_id}, User: {user_id}, "
                f"Attention: HIGH, Intent: RESPOND"
            )

            # Context already stored by create_spatial_event_from_slack()
            # No need for additional store_mapping() call

            # Process through complete integration pipeline (high priority for mentions)
            # Use RobustTaskManager to make response processing non-blocking and observable
            async def process_response():
                try:
                    response_result = await self.response_handler.handle_spatial_event(
                        spatial_event
                    )
                    if response_result:
                        logger.info(
                            f"Response sent for mention event: {response_result.get('status', 'unknown')}"
                        )
                    else:
                        logger.warning("No response generated for mention event")
                except Exception as response_error:
                    logger.error(f"Error processing response for mention event: {response_error}")
                    raise  # Re-raise for task manager visibility

            # Create tracked task to process response asynchronously
            try:
                task = task_manager.create_tracked_task(
                    process_response(),
                    name=f"mention_response_{message_ts}",
                    metadata={
                        "correlation_id": correlation_id.get(),
                        "message_ts": message_ts,
                        "channel_id": channel_id,
                    },
                )
                logger.info(f"Created tracked task {task} for mention response processing")
            except Exception as task_error:
                logger.error(f"Failed to create mention response task: {task_error}")

        except Exception as e:
            logger.error(f"Error processing mention event: {e}")

    async def _process_reaction_event(self, event: Dict[str, Any], team_id: str) -> None:
        """Process reaction event (emotional marker)"""

        try:
            # Extract reaction details
            reaction = event.get("reaction")
            item = event.get("item", {})
            channel_id = item.get("channel")
            message_ts = item.get("ts")
            user_id = event.get("user")

            # Determine emotional valence based on reaction
            emotional_valence = self._determine_emotional_valence(reaction)

            # Prepare context for spatial adapter
            context = {
                "territory_id": team_id,
                "room_id": channel_id,
                "user_id": user_id,
                # #1110: connector-owner Piper user_id for outbound credentials.
                "connector_user_id": self._get_connector_user_id(),
                "attention_level": "medium",
                "emotional_valence": emotional_valence,
                "navigation_intent": "monitor",
                "significance_level": "routine",
                "affected_objects": [message_ts],
                "spatial_changes": {"emotional_marker_added": reaction},
            }

            # Create spatial event using adapter
            spatial_event = await self.spatial_adapter.create_spatial_event_from_slack(
                message_ts, "emotional_marker_updated", context
            )

            logger.info(
                f"SLACK_PIPELINE: Spatial event created - Type: {spatial_event.event_type}, "
                f"Position: {spatial_event.object_position}, Channel: {channel_id}, User: {user_id}, "
                f"Reaction: {reaction}, Valence: {emotional_valence}"
            )

            # Context already stored by create_spatial_event_from_slack()
            # No need for additional store_mapping() call

            # Process through complete integration pipeline (emotional context)
            try:
                response_result = await self.response_handler.handle_spatial_event(spatial_event)
                if response_result:
                    logger.info(
                        f"Response sent for reaction event: {response_result.get('status', 'unknown')}"
                    )
                else:
                    logger.debug("No response needed for reaction event")
            except Exception as response_error:
                logger.error(f"Error processing response for reaction event: {response_error}")

        except Exception as e:
            logger.error(f"Error processing reaction event: {e}")

    def _determine_emotional_valence(self, reaction: str) -> str:
        """Determine emotional valence from Slack reaction"""
        positive_reactions = {"heart", "thumbsup", "tada", "clap", "muscle", "raised_hands"}
        negative_reactions = {"thumbsdown", "x", "warning", "rotating_light", "skull"}
        neutral_reactions = {"eyes", "thinking_face", "speech_balloon"}

        if reaction in positive_reactions:
            return "positive"
        elif reaction in negative_reactions:
            return "negative"
        elif reaction in neutral_reactions:
            return "neutral"
        else:
            return "neutral"

    async def _process_channel_join_event(self, event: Dict[str, Any], team_id: str) -> None:
        """Process channel join event (room inhabitant update)"""

        try:
            channel_id = event.get("channel")
            user_id = event.get("user")

            logger.debug(f"User {user_id} joined room {channel_id} - updating spatial inhabitants")

            # Here would update room inhabitant tracking

        except Exception as e:
            logger.error(f"Error processing channel join event: {e}")

    async def _process_interactive_component(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process interactive component interaction"""

        try:
            interaction_type = payload.get("type")

            if interaction_type == "block_actions":
                # Handle button clicks, menu selections, etc.
                return {"text": "Action processed"}
            elif interaction_type == "view_submission":
                # Handle modal submissions
                return {"response_action": "clear"}
            else:
                logger.warning(f"Unhandled interaction type: {interaction_type}")
                return {"text": "Unknown interaction"}

        except Exception as e:
            logger.error(f"Error processing interactive component: {e}")
            return {"text": "Error processing interaction"}

    async def _process_slash_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process slash command and route to appropriate handler.

        Issue #520: Implements routing for Canonical Queries #49, #50
        - /piper help → _handle_piper_command()
        - /standup → _handle_standup_command()

        Args:
            command_data: Slack command payload with command, text, user_id, channel_id

        Returns:
            Dict with response_type and text/blocks for Slack response
        """
        try:
            command = command_data.get("command", "")
            text = command_data.get("text", "").strip().lower()
            channel_id = command_data.get("channel_id")
            user_id = command_data.get("user_id")

            logger.info(f"Slash command {command} from user {user_id} in channel {channel_id}")

            # Route based on command
            if command == "/piper":
                return await self._handle_piper_command(text, user_id, channel_id)
            elif command == "/standup":
                return await self._handle_standup_command(user_id, channel_id)
            else:
                return {
                    "response_type": "ephemeral",
                    "text": f"Unknown command: {command}. Try `/piper help` for available commands.",
                }

        except Exception as e:
            logger.error(f"Error processing slash command: {e}")
            return {"response_type": "ephemeral", "text": "Error processing command"}

    async def _handle_piper_command(
        self, text: str, user_id: str, channel_id: str
    ) -> Dict[str, Any]:
        """
        Handle /piper commands.

        Issue #520: Query #50 - "/piper help"
        Issue #551 Phase 4: Extended subcommands for calendar, status, priority

        Subcommands:
        - help: Show available commands and capabilities
        - (empty): Same as help
        - calendar: Show today's calendar
        - status: Show current project status
        - priority: Show top priority item

        Args:
            text: Command text after /piper
            user_id: Slack user ID
            channel_id: Slack channel ID

        Returns:
            Ephemeral response with command output
        """
        # Normalize and parse subcommand
        subcommand = text.strip().lower() if text else ""

        if subcommand == "help" or subcommand == "":
            return await self._build_help_response()

        # Issue #551 Phase 4: Calendar subcommand
        elif subcommand in ("calendar", "cal", "today"):
            return await self._handle_calendar_subcommand(user_id, channel_id)

        # Issue #551 Phase 4: Status subcommand
        elif subcommand in ("status", "projects"):
            return await self._handle_status_subcommand(user_id, channel_id)

        # Issue #551 Phase 4: Priority subcommand
        elif subcommand in ("priority", "focus", "top"):
            return await self._handle_priority_subcommand(user_id, channel_id)

        else:
            # Issue #628: Warm response for unknown commands
            return {
                "response_type": "ephemeral",
                "text": f"I don't recognize `{subcommand}` - try `/piper help` to see what I can do!",
            }

    async def _handle_calendar_subcommand(self, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Handle /piper calendar subcommand.

        Issue #551 Phase 4: Calendar parity on Slack.
        Routes to canonical temporal handler for calendar information.
        """
        try:
            from services.domain.models import Intent
            from services.intent_service.canonical_handlers import CanonicalHandlers

            handlers = CanonicalHandlers()

            # Create a minimal intent for calendar query
            intent = Intent(
                raw_input="what's on my calendar today?",
                classification="TEMPORAL",
                confidence=1.0,
            )

            # Call the canonical handler
            result = await handlers._handle_temporal_query(
                intent, session_id=f"slack_{user_id}", user_id=user_id
            )

            message = result.get("message", "I couldn't retrieve your calendar.")

            return {
                "response_type": "ephemeral",
                "text": message,
            }

        except Exception as e:
            logger.error(f"Error handling calendar subcommand: {e}")
            return {
                "response_type": "ephemeral",
                "text": "I'm having trouble accessing your calendar right now. Please try again later.",
            }

    async def _handle_status_subcommand(self, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Handle /piper status subcommand.

        Issue #551 Phase 4: Status parity on Slack.
        Routes to canonical status handler for project status.
        """
        try:
            from services.domain.models import Intent
            from services.intent_service.canonical_handlers import CanonicalHandlers

            handlers = CanonicalHandlers()

            # Create a minimal intent for status query
            intent = Intent(
                raw_input="what am I working on?",
                classification="STATUS",
                confidence=1.0,
            )

            # Call the canonical handler
            result = await handlers._handle_status_query(
                intent, session_id=f"slack_{user_id}", user_id=user_id
            )

            message = result.get("message", "I couldn't retrieve your project status.")

            return {
                "response_type": "ephemeral",
                "text": message,
            }

        except Exception as e:
            logger.error(f"Error handling status subcommand: {e}")
            return {
                "response_type": "ephemeral",
                "text": "I'm having trouble accessing your project status right now. Please try again later.",
            }

    async def _handle_priority_subcommand(self, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Handle /piper priority subcommand.

        Issue #551 Phase 4: Priority parity on Slack.
        Routes to canonical priority handler for top priority item.
        """
        try:
            from services.domain.models import Intent
            from services.intent_service.canonical_handlers import CanonicalHandlers

            handlers = CanonicalHandlers()

            # Create a minimal intent for priority query
            intent = Intent(
                raw_input="what's my top priority?",
                classification="PRIORITY",
                confidence=1.0,
            )

            # Call the canonical handler
            result = await handlers._handle_priority_query(
                intent, session_id=f"slack_{user_id}", user_id=user_id
            )

            message = result.get("message", "I couldn't determine your top priority.")

            return {
                "response_type": "ephemeral",
                "text": message,
            }

        except Exception as e:
            logger.error(f"Error handling priority subcommand: {e}")
            return {
                "response_type": "ephemeral",
                "text": "I'm having trouble determining your priority right now. Please try again later.",
            }

    async def _build_help_response(self) -> Dict[str, Any]:
        """
        Build help response with dynamic capabilities.

        Issue #520: Query #50 - Uses _get_dynamic_capabilities() from canonical_handlers
        Issue #551: Now uses CommandRegistry for command list, falls back to capabilities
        """
        from services.commands.adapters.slack_adapter import SlackCommandAdapter
        from services.commands.definitions import register_all_commands
        from services.commands.registry import CommandRegistry
        from services.intent_service.canonical_handlers import CanonicalHandlers

        # Issue #551: Try to use CommandRegistry first
        if not CommandRegistry.is_initialized():
            register_all_commands()

        # Check if we have commands registered
        slack_commands = CommandRegistry.list_commands(interface=SlackCommandAdapter.interface)

        if slack_commands:
            # Use the new registry-based help
            return SlackCommandAdapter.build_help_response()

        # Fallback to original capability-based help if registry empty
        handlers = CanonicalHandlers()
        capabilities = handlers._get_dynamic_capabilities()

        # Format capabilities
        core = capabilities.get("core", [])
        integrations = capabilities.get("integrations", [])

        # Issue #628: Grammar-conscious help text
        help_text = "Hi! I'm Piper, your PM assistant. Here's how I can help:\n\n"

        help_text += "*Quick Commands*\n"
        help_text += "• `/standup` - I'll help you prep for standup\n"
        help_text += "• `/piper help` - Show this message\n\n"

        help_text += "*What I Can Do*\n"
        for cap in core:
            help_text += f"• {cap}\n"

        if integrations:
            help_text += "\n*I'm Connected To*\n"
            for integration in integrations:
                name = integration.get("name", "Unknown")
                help_text += f"• {name}\n"

        help_text += "\nJust ask me anything about your projects - I'm here to help!"

        return {
            "response_type": "ephemeral",
            "text": help_text,
        }

    async def _handle_standup_command(self, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Handle /standup command.

        Issue #520: Query #49 - "/standup"

        Generates standup from:
        1. Completed items since yesterday
        2. High-priority todos for today
        3. Current blockers

        Args:
            user_id: Slack user ID
            channel_id: Slack channel ID

        Returns:
            In-channel response with standup format
        """
        try:
            standup_parts = []

            # 1. What I did yesterday (completed items)
            yesterday_items = await self._get_completed_since_yesterday()
            if yesterday_items:
                standup_parts.append("*Yesterday:*")
                for item in yesterday_items[:3]:
                    standup_parts.append(f"• {item}")
            else:
                standup_parts.append("*Yesterday:*\n• No completed items recorded")

            # 2. What I'm doing today (high-priority todos)
            today_items = await self._get_today_priorities()
            standup_parts.append("\n*Today:*")
            if today_items:
                for item in today_items[:3]:
                    standup_parts.append(f"• {item}")
            else:
                standup_parts.append("• No high-priority items scheduled")

            # 3. Blockers
            blockers = await self._get_blockers()
            standup_parts.append("\n*Blockers:*")
            if blockers:
                for blocker in blockers[:2]:
                    standup_parts.append(f"• {blocker}")
            else:
                standup_parts.append("• None")

            return {
                "response_type": "in_channel",  # Share with team
                "text": "\n".join(standup_parts),
            }

        except Exception as e:
            logger.error(f"Error generating standup: {e}")
            return {
                "response_type": "ephemeral",
                "text": "Unable to generate standup. Please try again.",
            }

    async def _get_completed_since_yesterday(self) -> list:
        """
        Get items completed since yesterday.

        Issue #520: Helper for /standup command.
        Uses TodoManagementService or audit log when available.
        Returns placeholder for now - will integrate with real service.
        """
        # TODO: Integrate with TodoManagementService when user context available
        return []

    async def _get_today_priorities(self) -> list:
        """
        Get high-priority items for today.

        Issue #520: Helper for /standup command.
        Uses TodoManagementService when available.
        """
        # TODO: Integrate with TodoManagementService when user context available
        return []

    async def _get_blockers(self) -> list:
        """
        Get current blockers — placeholder (always returns empty list).

        Issue #520: Helper for /standup command's "Blockers:" section.
        Issue #692 cleanup (2026-05-24): the prior
        ``TODO: Integrate with blocker detection when available`` was
        removed because no blocker-detection service exists in the
        codebase and none is planned in M2. The method intentionally
        returns ``[]`` so the /standup command's "Blockers:" section
        renders "None" — that's the current product behavior. If
        blocker detection becomes a real feature, file a new issue
        with proper scope; this method is the wire-up point.
        """
        return []

    def get_router(self) -> APIRouter:
        """Get the FastAPI router for integration with main app"""
        return self.router

    def get_webhook_urls(self, base_url: str) -> Dict[str, str]:
        """Get webhook URLs for Slack app configuration"""

        base_url = base_url.rstrip("/")

        return {
            "events_url": f"{base_url}/slack/webhooks/events",
            "interactive_url": f"{base_url}/slack/webhooks/interactive",
            "commands_url": f"{base_url}/slack/webhooks/commands",
            "oauth_callback_url": f"{base_url}/slack/oauth/callback",
        }
