"""
Tests for error response utilities.

Tests Pattern 034: Error Handling Standards
Related Issue: #215 (CORE-ERROR-STANDARDS)

Test Coverage:
- ErrorCode enum values
- Each error response function
- HTTP status codes
- Response structure
- Optional parameters
- Logging behavior
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi.responses import JSONResponse

from web.utils.error_responses import (
    ErrorCode,
    bad_request_error,
    error_response,
    internal_error,
    not_found_error,
    validation_error,
)


class TestErrorCode:
    """Test ErrorCode enum."""

    def test_error_code_values(self):
        """Test ErrorCode enum has correct values."""
        assert ErrorCode.BAD_REQUEST.value == "BAD_REQUEST"
        assert ErrorCode.VALIDATION_ERROR.value == "VALIDATION_ERROR"
        assert ErrorCode.NOT_FOUND.value == "NOT_FOUND"
        assert ErrorCode.INTERNAL_ERROR.value == "INTERNAL_ERROR"

    def test_error_code_count(self):
        """Test ErrorCode enum has exactly 4 values."""
        assert len(list(ErrorCode)) == 4


class TestErrorResponse:
    """Test base error_response function."""

    def test_error_response_basic(self):
        """Test basic error response structure."""
        response = error_response(
            status_code=400,
            code=ErrorCode.BAD_REQUEST,
            message="Test error",
        )

        assert isinstance(response, JSONResponse)
        assert response.status_code == 400

        body = json.loads(response.body.decode())
        assert body["status"] == "error"
        assert body["code"] == "BAD_REQUEST"
        assert body["message"] == "Test error"
        assert "details" not in body

    def test_error_response_with_details(self):
        """Test error response with details."""
        response = error_response(
            status_code=422,
            code=ErrorCode.VALIDATION_ERROR,
            message="Validation failed",
            details={"field": "email", "issue": "Invalid format"},
        )

        body = json.loads(response.body.decode())
        assert body["details"] == {"field": "email", "issue": "Invalid format"}

    def test_error_response_all_status_codes(self):
        """Test error response with various status codes."""
        status_codes = [400, 404, 422, 500, 502, 503]

        for status_code in status_codes:
            response = error_response(
                status_code=status_code,
                code=ErrorCode.INTERNAL_ERROR,
                message="Test",
            )
            assert response.status_code == status_code


class TestBadRequestError:
    """Test bad_request_error function."""

    def test_bad_request_default_message(self):
        """Test bad request error with default message."""
        response = bad_request_error()

        assert response.status_code == 400
        body = json.loads(response.body.decode())
        assert body["status"] == "error"
        assert body["code"] == "BAD_REQUEST"
        assert body["message"] == "Request syntax is malformed"

    def test_bad_request_custom_message(self):
        """Test bad request error with custom message."""
        response = bad_request_error("Invalid JSON syntax")

        body = json.loads(response.body.decode())
        assert body["message"] == "Invalid JSON syntax"

    def test_bad_request_with_details(self):
        """Test bad request error with details."""
        response = bad_request_error(
            "Invalid JSON",
            details={"line": 5, "column": 12},
        )

        body = json.loads(response.body.decode())
        assert body["details"] == {"line": 5, "column": 12}

    @patch("web.utils.error_responses.logger")
    def test_bad_request_logging(self, mock_logger):
        """Test bad request error logs warning."""
        bad_request_error("Test error", {"detail": "test"})
        mock_logger.warning.assert_called_once()


class TestValidationError:
    """Test validation_error function."""

    def test_validation_error_default_message(self):
        """Test validation error with default message."""
        response = validation_error()

        assert response.status_code == 422
        body = json.loads(response.body.decode())
        assert body["status"] == "error"
        assert body["code"] == "VALIDATION_ERROR"
        assert body["message"] == "Validation failed"

    def test_validation_error_custom_message(self):
        """Test validation error with custom message."""
        response = validation_error("Required field missing")

        body = json.loads(response.body.decode())
        assert body["message"] == "Required field missing"

    def test_validation_error_with_field_details(self):
        """Test validation error with field details."""
        response = validation_error(
            "Validation failed",
            details={"field": "intent", "issue": "Cannot be empty"},
        )

        body = json.loads(response.body.decode())
        assert body["details"]["field"] == "intent"
        assert body["details"]["issue"] == "Cannot be empty"

    @patch("web.utils.error_responses.logger")
    def test_validation_error_logging(self, mock_logger):
        """Test validation error logs warning."""
        validation_error("Test error", {"field": "test"})
        mock_logger.warning.assert_called_once()


class TestNotFoundError:
    """Test not_found_error function."""

    def test_not_found_default_message(self):
        """Test not found error with default message."""
        response = not_found_error()

        assert response.status_code == 404
        body = json.loads(response.body.decode())
        assert body["status"] == "error"
        assert body["code"] == "NOT_FOUND"
        assert body["message"] == "Resource not found"

    def test_not_found_custom_message(self):
        """Test not found error with custom message."""
        response = not_found_error("Workflow not found")

        body = json.loads(response.body.decode())
        assert body["message"] == "Workflow not found"

    def test_not_found_with_resource_details(self):
        """Test not found error with resource details."""
        response = not_found_error(
            "Workflow not found",
            details={"resource": "workflow", "id": "12345"},
        )

        body = json.loads(response.body.decode())
        assert body["details"]["resource"] == "workflow"
        assert body["details"]["id"] == "12345"

    @patch("web.utils.error_responses.logger")
    def test_not_found_logging(self, mock_logger):
        """Test not found error logs info."""
        not_found_error("Test error", {"resource": "test"})
        mock_logger.info.assert_called_once()


class TestInternalError:
    """Test internal_error function."""

    def test_internal_error_default_message(self):
        """Test internal error with default message."""
        response = internal_error()

        assert response.status_code == 500
        body = json.loads(response.body.decode())
        assert body["status"] == "error"
        assert body["code"] == "INTERNAL_ERROR"
        assert body["message"] == "An unexpected error occurred"

    def test_internal_error_custom_message(self):
        """Test internal error with custom message."""
        response = internal_error("Service unavailable")

        body = json.loads(response.body.decode())
        assert body["message"] == "Service unavailable"

    def test_internal_error_auto_generates_error_id(self):
        """Test internal error auto-generates error_id."""
        response = internal_error()

        body = json.loads(response.body.decode())
        assert "error_id" in body["details"]
        assert isinstance(body["details"]["error_id"], str)
        assert len(body["details"]["error_id"]) == 36  # UUID length

    def test_internal_error_custom_error_id(self):
        """Test internal error with custom error_id."""
        custom_id = "custom-error-12345"
        response = internal_error(error_id=custom_id)

        body = json.loads(response.body.decode())
        assert body["details"]["error_id"] == custom_id

    def test_internal_error_unique_ids(self):
        """Test internal error generates unique IDs."""
        response1 = internal_error()
        response2 = internal_error()

        body1 = json.loads(response1.body.decode())
        body2 = json.loads(response2.body.decode())

        assert body1["details"]["error_id"] != body2["details"]["error_id"]

    @patch("web.utils.error_responses.logger")
    def test_internal_error_logging(self, mock_logger):
        """Test internal error logs error."""
        internal_error("Test error", error_id="test-123")
        mock_logger.error.assert_called_once()


class TestResponseStructure:
    """Test response structure consistency."""

    def test_all_errors_have_status_field(self):
        """Test all error responses include 'status': 'error'."""
        errors = [
            bad_request_error(),
            validation_error(),
            not_found_error(),
            internal_error(),
        ]

        for response in errors:
            body = json.loads(response.body.decode())
            assert body["status"] == "error"

    def test_all_errors_have_code_field(self):
        """Test all error responses include 'code' field."""
        errors = [
            bad_request_error(),
            validation_error(),
            not_found_error(),
            internal_error(),
        ]

        for response in errors:
            body = json.loads(response.body.decode())
            assert "code" in body
            assert isinstance(body["code"], str)

    def test_all_errors_have_message_field(self):
        """Test all error responses include 'message' field."""
        errors = [
            bad_request_error(),
            validation_error(),
            not_found_error(),
            internal_error(),
        ]

        for response in errors:
            body = json.loads(response.body.decode())
            assert "message" in body
            assert isinstance(body["message"], str)

    def test_details_optional_for_all_errors(self):
        """Test details field is optional for all errors."""
        # Without details
        errors_without = [
            bad_request_error("Test"),
            validation_error("Test"),
            not_found_error("Test"),
        ]

        for response in errors_without:
            body = json.loads(response.body.decode())
            # internal_error always has details (error_id), others don't
            if response.status_code != 500:
                assert "details" not in body

        # With details
        test_details = {"test": "value"}
        errors_with = [
            bad_request_error("Test", test_details),
            validation_error("Test", test_details),
            not_found_error("Test", test_details),
        ]

        for response in errors_with:
            body = json.loads(response.body.decode())
            assert "details" in body
            assert body["details"]["test"] == "value"


class TestHTTPStatusCodes:
    """Test correct HTTP status codes are used."""

    def test_bad_request_returns_400(self):
        """Test bad_request_error returns 400."""
        response = bad_request_error()
        assert response.status_code == 400

    def test_validation_error_returns_422(self):
        """Test validation_error returns 422."""
        response = validation_error()
        assert response.status_code == 422

    def test_not_found_returns_404(self):
        """Test not_found_error returns 404."""
        response = not_found_error()
        assert response.status_code == 404

    def test_internal_error_returns_500(self):
        """Test internal_error returns 500."""
        response = internal_error()
        assert response.status_code == 500


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_missing_required_field_scenario(self):
        """Test typical missing required field scenario."""
        response = validation_error(
            "Required field missing",
            {"field": "message", "issue": "Cannot be empty"},
        )

        assert response.status_code == 422
        body = json.loads(response.body.decode())
        assert body["code"] == "VALIDATION_ERROR"
        assert "field" in body["details"]

    def test_invalid_json_scenario(self):
        """Test typical invalid JSON scenario."""
        response = bad_request_error(
            "Invalid JSON syntax",
            {"error": "Unexpected token at line 5"},
        )

        assert response.status_code == 400
        body = json.loads(response.body.decode())
        assert body["code"] == "BAD_REQUEST"

    def test_resource_not_found_scenario(self):
        """Test typical resource not found scenario."""
        response = not_found_error(
            "Workflow not found",
            {"resource": "workflow", "id": "wf-12345"},
        )

        assert response.status_code == 404
        body = json.loads(response.body.decode())
        assert body["code"] == "NOT_FOUND"
        assert body["details"]["id"] == "wf-12345"

    def test_service_failure_scenario(self):
        """Test typical service failure scenario."""
        response = internal_error("Backend service unavailable")

        assert response.status_code == 500
        body = json.loads(response.body.decode())
        assert body["code"] == "INTERNAL_ERROR"
        assert "error_id" in body["details"]
