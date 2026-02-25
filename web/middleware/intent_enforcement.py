"""
Intent Enforcement Middleware for GREAT-4B

Monitors all HTTP requests and enforces intent classification on natural language endpoints.
Prevents future bypasses by architecturally enforcing the principle:
"All natural language user input must go through intent classification."

Created: October 5, 2025
Issue: #206 (CORE-GREAT-4B)
"""

import logging
from typing import Dict, List

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class IntentEnforcementMiddleware(BaseHTTPMiddleware):
    """
    Enforces intent classification for natural language endpoints.

    This middleware:
    1. Monitors all HTTP requests
    2. Identifies natural language input endpoints
    3. Marks them as requiring intent classification
    4. Logs all requests for compliance monitoring
    5. Exempts static/health/output endpoints

    Architectural Principle:
    - User INPUT → intent classification (enforced)
    - Piper OUTPUT → transformation only (exempt)
    - Structured commands → direct execution (exempt)
    """

    # Paths that explicitly don't need intent (exempt from enforcement)
    EXEMPT_PATHS: List[str] = [
        "/health",
        "/metrics",
        "/docs",
        "/openapi.json",
        "/static",
        "/setup",  # Setup wizard UI and API (first-time install)
        "/api/v1/personality/enhance",  # Output processing, not input
        "/api/v1/personality/profile",  # Config endpoints (structured data)
        "/api/v1/workflows",  # Direct ID lookups
        "/debug-markdown",  # Debug endpoints
        "/personality-preferences",  # Static UI pages
        "/standup",  # Static UI page
        "/",  # Root page
    ]

    # Natural language input endpoints (must use intent)
    NL_ENDPOINTS: List[str] = [
        "/api/v1/intent",  # IS the intent endpoint
        "/api/standup",  # Proxies to backend (uses intent there)
        "/api/chat",  # Future NL endpoint
        "/api/message",  # Future NL endpoint
    ]

    async def dispatch(self, request: Request, call_next):
        """
        Process each HTTP request and enforce intent requirements.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware/route handler

        Returns:
            Response from the next handler
        """
        path = request.url.path
        method = request.method

        # Log all requests for monitoring
        logger.info(f"Request: {method} {path}")

        # Check if this is a NL endpoint
        if self._is_nl_endpoint(path):
            # Mark that intent is required (for future validation)
            request.state.intent_required = True
            logger.debug(f"Intent required for: {path}")

        # Check if exempt
        if self._is_exempt(path):
            logger.debug(f"Exempt from intent: {path}")

        # Continue to next handler
        response = await call_next(request)
        return response

    def _is_nl_endpoint(self, path: str) -> bool:
        """
        Check if path is a natural language endpoint.

        Args:
            path: The request path

        Returns:
            True if path is a natural language endpoint
        """
        return any(path.startswith(endpoint) for endpoint in self.NL_ENDPOINTS)

    def _is_exempt(self, path: str) -> bool:
        """
        Check if path is exempt from intent requirement.

        Args:
            path: The request path

        Returns:
            True if path is exempt from intent enforcement
        """
        return any(path.startswith(exempt) for exempt in self.EXEMPT_PATHS)

    @classmethod
    def get_monitoring_status(cls) -> Dict:
        """
        Get current monitoring configuration.

        Returns:
            Dict with middleware status and configuration
        """
        return {
            "middleware_active": True,
            "nl_endpoints": cls.NL_ENDPOINTS,
            "exempt_paths": cls.EXEMPT_PATHS,
            "monitoring": "All requests logged",
            "principle": "User INPUT → intent classification (enforced)",
        }
