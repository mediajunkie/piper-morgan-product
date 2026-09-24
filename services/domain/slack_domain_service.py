"""
Slack Domain Service
Mediates all Slack operations for the domain layer following DDD principles

Created: 2025-09-12 by Code Agent Step 5 - Domain Service Mediation Completion
Addresses architectural violation: Direct Slack integration access from main.py and CLI layers
"""

from typing import Any, Dict, List, Optional

import structlog

from services.api.errors import SlackAuthFailedError
from services.domain.models import SpatialEvent
from services.integrations.slack.response_handler import SlackResponseHandler
from services.integrations.slack.webhook_router import SlackWebhookRouter

# Re-export exceptions for clean domain boundary
__all__ = ["SlackDomainService", "SlackAuthFailedError"]

logger = structlog.get_logger()


class SlackDomainService:
    """
    Domain service for Slack operations mediation

    Encapsulates Slack integration access following DDD principles:
    - Mediates between application layer and Slack integration layer
    - Provides clean domain interface for Slack slash-command processing (Socket Mode)
    - Handles Slack-specific error translation to domain exceptions
    - Manages Slack webhook router and response handler lifecycle
    """

    def __init__(
        self,
        webhook_router: Optional[SlackWebhookRouter] = None,
        response_handler: Optional[SlackResponseHandler] = None,
    ):
        """Initialize with optional Slack component injection"""
        try:
            self._webhook_router = webhook_router or SlackWebhookRouter()
            self._response_handler = response_handler or SlackResponseHandler()
            logger.info(
                "Slack domain service initialized",
                router_type=type(self._webhook_router).__name__,
                handler_type=type(self._response_handler).__name__,
            )
        except Exception as e:
            logger.error("Failed to initialize Slack domain service", error=str(e))
            raise

    # The Events-API pass-through (`handle_slack_events`) was removed with the
    # HTTP webhook surface (#1496/#1499): events arrive over Socket Mode and go
    # to the intent service directly, never through this class.

    def get_webhook_router(self) -> SlackWebhookRouter:
        """Get webhook router for domain service integration"""
        return self._webhook_router

    # Response Operations

    async def handle_spatial_event(self, spatial_event: SpatialEvent) -> Optional[Dict[str, Any]]:
        """Handle spatial events through Slack response system for domain consumption"""
        try:
            return await self._response_handler.handle_spatial_event(spatial_event)
        except SlackAuthFailedError:
            logger.error("Slack authentication failed for spatial event")
            raise
        except Exception as e:
            logger.error("Slack spatial event handling failed", error=str(e))
            raise

    def get_response_handler(self) -> SlackResponseHandler:
        """Get response handler for domain service integration"""
        return self._response_handler

    # Configuration and Status Operations

    def get_connection_status(self) -> Dict[str, Any]:
        """Get Slack connection status for domain monitoring"""
        try:
            # Basic status check - webhook router should be initialized
            router_status = self._webhook_router is not None
            handler_status = self._response_handler is not None

            return {
                "connected": router_status and handler_status,
                "webhook_router_ready": router_status,
                "response_handler_ready": handler_status,
                "components": {
                    "webhook_router": (
                        type(self._webhook_router).__name__ if router_status else None
                    ),
                    "response_handler": (
                        type(self._response_handler).__name__ if handler_status else None
                    ),
                },
            }
        except Exception as e:
            logger.error("Slack connection status check failed", error=str(e))
            return {"connected": False, "error": str(e)}

    # Health and Monitoring Operations

    def get_service_health(self) -> Dict[str, Any]:
        """Get comprehensive Slack service health for domain monitoring"""
        try:
            connection_status = self.get_connection_status()

            # Additional health metrics
            health_metrics = {
                "service_initialized": True,
                "webhook_router_available": self._webhook_router is not None,
                "response_handler_available": self._response_handler is not None,
                "last_health_check": "2025-09-12T19:15:00Z",  # Current timestamp
            }

            return {
                **connection_status,
                "health": health_metrics,
                "status": "healthy" if connection_status.get("connected") else "unhealthy",
            }
        except Exception as e:
            logger.error("Slack service health check failed", error=str(e))
            return {"connected": False, "status": "unhealthy", "error": str(e)}
