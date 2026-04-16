"""
Standard error response utilities for REST API compliance.

Implements Pattern 034: Error Handling Standards
Related Issue: #215 (CORE-ERROR-STANDARDS)

All error responses follow REST principles:
- Proper HTTP status codes (400, 422, 404, 500)
- Consistent JSON format
- Sanitized error details
- Logging integration

Usage:
    from web.utils.error_responses import (
        bad_request_error,
        validation_error,
        not_found_error,
        internal_error
    )

    # In endpoints:
    if not data.get("required_field"):
        return validation_error(
            "Required field missing",
            {"field": "required_field", "issue": "Cannot be empty"}
        )
"""

import logging
import uuid
from enum import Enum
from typing import Any, Dict, Optional

from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class ErrorCode(str, Enum):
    """
    Standard error codes for API responses.

    These codes provide semantic meaning beyond HTTP status codes,
    allowing clients to handle specific error types programmatically.
    """

    BAD_REQUEST = "BAD_REQUEST"  # Malformed request syntax
    VALIDATION_ERROR = "VALIDATION_ERROR"  # Semantic validation failure
    NOT_FOUND = "NOT_FOUND"  # Resource doesn't exist
    INTERNAL_ERROR = "INTERNAL_ERROR"  # Unexpected server error


def error_response(
    status_code: int, code: ErrorCode, message: str, details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create standardized error response.

    All error responses follow this structure:
    {
        "status": "error",
        "code": "<ERROR_CODE>",
        "message": "User-friendly message",
        "details": {optional additional info}
    }

    Args:
        status_code: HTTP status code (400, 422, 404, 500, etc.)
        code: ErrorCode enum value
        message: User-friendly error message
        details: Optional additional information (sanitized)

    Returns:
        JSONResponse with proper status code and error body

    Example:
        return error_response(
            422,
            ErrorCode.VALIDATION_ERROR,
            "Validation failed",
            {"field": "email", "issue": "Invalid format"}
        )
    """
    response_body = {
        "status": "error",
        "code": code.value,
        "message": message,
    }

    if details:
        response_body["details"] = details

    return JSONResponse(status_code=status_code, content=response_body)


def bad_request_error(
    message: str = "Request syntax is malformed", details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Return 400 Bad Request error.

    Use for malformed request syntax:
    - Invalid JSON syntax
    - Missing required headers
    - Malformed URL parameters
    - Wrong content-type

    Args:
        message: User-friendly error message
        details: Optional additional information

    Returns:
        JSONResponse with 400 status code

    Example:
        try:
            data = await request.json()
        except JSONDecodeError as e:
            return bad_request_error(
                "Invalid JSON",
                {"issue": str(e)}
            )
    """
    logger.warning(f"Bad request: {message} - {details}")
    return error_response(
        status_code=400, code=ErrorCode.BAD_REQUEST, message=message, details=details
    )


def validation_error(
    message: str = "Validation failed", details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Return 422 Unprocessable Entity error.

    Use for syntactically valid but semantically invalid requests:
    - Empty required fields
    - Invalid field values
    - Business rule violations
    - Type mismatches

    Args:
        message: User-friendly error message
        details: Optional additional information (e.g., field name, issue)

    Returns:
        JSONResponse with 422 status code

    Example:
        if not data.get("intent"):
            return validation_error(
                "Required field missing",
                {"field": "intent", "issue": "Cannot be empty"}
            )
    """
    logger.warning(f"Validation error: {message} - {details}")
    return error_response(
        status_code=422, code=ErrorCode.VALIDATION_ERROR, message=message, details=details
    )


def not_found_error(
    message: str = "Resource not found", details: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Return 404 Not Found error.

    Use when requested resource doesn't exist:
    - Workflow ID not found
    - User ID not found
    - Unknown endpoint

    Args:
        message: User-friendly error message
        details: Optional additional information (e.g., resource type, ID)

    Returns:
        JSONResponse with 404 status code

    Example:
        workflow = await workflow_service.get(workflow_id)
        if not workflow:
            return not_found_error(
                "Workflow not found",
                {"resource": "workflow", "id": workflow_id}
            )
    """
    logger.info(f"Resource not found: {message} - {details}")
    return error_response(
        status_code=404, code=ErrorCode.NOT_FOUND, message=message, details=details
    )


def internal_error(
    message: str = "An unexpected error occurred", error_id: Optional[str] = None
) -> JSONResponse:
    """
    Return 500 Internal Server Error.

    Use for unexpected server errors:
    - Unhandled exceptions
    - Service failures
    - Database errors
    - Backend unavailable

    IMPORTANT: Never expose sensitive information in error details.
    Never include: stack traces, internal paths, credentials, config.

    Args:
        message: Generic user-friendly message (avoid exposing internals)
        error_id: Optional error ID for log correlation (auto-generated if not provided)

    Returns:
        JSONResponse with 500 status code

    Example:
        try:
            result = await service.process()
            return {"status": "success", "data": result}
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return internal_error()  # Never expose error details to client
    """
    if not error_id:
        error_id = str(uuid.uuid4())

    logger.error(
        f"Internal error: {message} (error_id: {error_id})",
        exc_info=False,  # exc_info should be logged at call site, not here
    )

    return error_response(
        status_code=500,
        code=ErrorCode.INTERNAL_ERROR,
        message=message,
        details={"error_id": error_id},
    )
