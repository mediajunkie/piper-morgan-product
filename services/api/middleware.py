"""
API Middleware for Piper Morgan
Handles request/response processing and error handling.

Ethics enforcement is now done at the domain layer in
services/ethics/boundary_enforcer_refactored.py, wired through
services/intent/intent_service.py for universal coverage across
web API, CLI, Slack webhooks, and direct service calls. See ADR-029
(domain service mediation) and ADR-032 (universal entry point).
"""

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from services.api.errors import ERROR_MESSAGES, APIError
from services.infrastructure.logging.config import generate_request_id, get_logger

# Configure structured logger
logger = get_logger(__name__)


class CorrelationMiddleware(BaseHTTPMiddleware):
    """Middleware to add correlation IDs to all requests"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Generate correlation IDs
        request_id = generate_request_id()
        session_id = request.headers.get("X-Session-ID")

        # Add correlation data to request state
        request.state.correlation = {"request_id": request_id, "session_id": session_id}

        # Create correlation logger
        correlation_logger = get_logger(__name__, session_id=session_id, request_id=request_id)

        # Log request start
        correlation_logger.info(
            "request_start",
            event_type="request_start",
            method=request.method,
            url=str(request.url),
            session_id=session_id,
            request_id=request_id,
        )

        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)

            # Calculate response time
            response_time = (time.time() - start_time) * 1000

            # Log request complete
            correlation_logger.info(
                "request_complete",
                event_type="request_complete",
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                response_time_ms=response_time,
                session_id=session_id,
                request_id=request_id,
            )

            return response

        except Exception as e:
            # Calculate response time
            response_time = (time.time() - start_time) * 1000

            # Log request error
            correlation_logger.error(
                "request_error",
                error=str(e),
                event_type="request_error",
                method=request.method,
                url=str(request.url),
                response_time_ms=response_time,
                session_id=session_id,
                request_id=request_id,
            )
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except APIError as exc:
            # Handle our custom, structured API errors
            user_message = ERROR_MESSAGES.get(exc.error_code, "An unexpected error occurred.")

            # Format the message with details from the exception
            try:
                formatted_message = user_message.format(**exc.details)
            except (KeyError, TypeError):
                # Fallback if formatting fails
                formatted_message = user_message

            # Log the error with correlation context
            correlation_data = getattr(request.state, "correlation", {})
            logger.error(
                "api_error",
                event_type="api_error",
                error_code=exc.error_code,
                details=exc.details,
                session_id=correlation_data.get("session_id"),
                request_id=correlation_data.get("request_id"),
            )

            return Response(
                status_code=exc.status_code,
                content=formatted_message,
                media_type="text/plain",
            )
        except Exception as e:
            # Handle unexpected errors
            correlation_data = getattr(request.state, "correlation", {})
            logger.error(
                "unexpected_error",
                event_type="unexpected_error",
                error=str(e),
                session_id=correlation_data.get("session_id"),
                request_id=correlation_data.get("request_id"),
            )

            return Response(
                status_code=500,
                content="An unexpected error occurred.",
                media_type="text/plain",
            )
