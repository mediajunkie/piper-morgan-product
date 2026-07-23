"""
Comprehensive Testing Framework for Error Message Enhancement

This test suite validates that error message improvements don't create regressions
while ensuring user experience enhancements are effective.

Test Categories:
1. Regression Prevention - Ensure existing functionality is preserved
2. User Experience Validation - Verify improvements provide value
3. Integration Testing - Test error handling across the system
4. Performance Validation - Ensure error handling doesn't impact performance
"""

import json
import re
from typing import Any, Dict
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from services.api.errors import (
    ERROR_MESSAGES,
    APIError,
    GitHubAuthFailedError,
    IntentClassificationFailedError,
    LowConfidenceIntentError,
    TaskFailedError,
    WorkflowTimeoutError,
)
from web.app import app


class TestErrorMessageRegression:
    """Ensure error message changes don't break functionality"""

    @pytest.fixture
    def test_client(self):
        """Test client for API testing"""
        return TestClient(app)

    def test_error_codes_preserved(self):
        """Ensure HTTP status codes remain correct after message enhancement"""

        # Test all APIError subclasses maintain correct status codes
        error_tests = [
            (IntentClassificationFailedError(), 500),
            (LowConfidenceIntentError(), 422),
            (WorkflowTimeoutError(), 504),
            (TaskFailedError(), 500),
            (GitHubAuthFailedError(), 502),
        ]

        for error, expected_status in error_tests:
            assert (
                error.status_code == expected_status
            ), f"Status code mismatch for {type(error).__name__}"

    def test_error_logging_maintained(self):
        """Verify technical details still logged for debugging"""

        # Test that error details are preserved in the error object
        error = TaskFailedError(
            task_description="test task",
            recovery_suggestion="try again",
            details={"technical_info": "debug_data"},
        )

        assert error.details["task_description"] == "test task"
        assert error.details["recovery_suggestion"] == "try again"
        assert error.details["technical_info"] == "debug_data"

    def test_error_context_preserved(self):
        """Ensure error context/details not lost in user-friendly messages"""

        # Test that error codes remain consistent
        error = LowConfidenceIntentError(suggestions="try 'list projects'")
        assert error.error_code == "LOW_CONFIDENCE_INTENT"

        # Test that details are preserved
        assert "suggestions" in error.details
        assert error.details["suggestions"] == "try 'list projects'"

    def test_centralized_error_messages_consistency(self):
        """Verify ERROR_MESSAGES dictionary maintains consistency"""

        # Test that all error codes have corresponding messages
        error_classes = [
            IntentClassificationFailedError,
            LowConfidenceIntentError,
            WorkflowTimeoutError,
            TaskFailedError,
            GitHubAuthFailedError,
        ]

        for error_class in error_classes:
            error = error_class()
            assert error.error_code in ERROR_MESSAGES, f"Missing message for {error.error_code}"

    def test_error_message_formatting(self):
        """Test that error message formatting works correctly"""

        # Test message with placeholders
        error = TaskFailedError(
            task_description="creating a ticket", recovery_suggestion="check your project settings"
        )

        message = ERROR_MESSAGES["TASK_FAILED"].format(
            task_description=error.details["task_description"],
            recovery_suggestion=error.details["recovery_suggestion"],
        )

        assert "creating a ticket" in message
        assert "check your project settings" in message


class TestUserFriendlyErrors:
    """Validate improved error messages provide value"""

    @pytest.fixture
    def test_client(self):
        """Test client for API testing"""
        return TestClient(app)

    def test_actionable_guidance_included(self):
        """Verify errors include next steps for users"""

        # Test that TaskFailedError includes recovery suggestions
        error = TaskFailedError(
            task_description="processing your request",
            recovery_suggestion="please check your input and try again",
        )

        message = ERROR_MESSAGES["TASK_FAILED"].format(
            task_description=error.details["task_description"],
            recovery_suggestion=error.details["recovery_suggestion"],
        )

        assert "please check your input" in message.lower()
        assert "try again" in message.lower()

    def test_user_guide_links_functional(self):
        """#1204: every /docs/*.md link embedded in a user-facing ERROR_MESSAGES
        entry must point to a file that exists.

        Validates the links *actually shown to users* (extracted from
        ERROR_MESSAGES), not a hardcoded list that can silently drift from the
        error content — the point is to protect users from dead links. The prior
        version checked a fixed list at docs/user-guides/, which moved to
        docs/public/user-guides/legacy-user-guides/ and broke."""
        import os

        from services.api.errors import ERROR_MESSAGES

        link_re = re.compile(r"/?(docs/[\w./-]+\.md)")
        checked = []
        for key, message in ERROR_MESSAGES.items():
            for match in link_re.finditer(message):
                rel_path = match.group(1)  # strip any leading slash → repo-relative
                checked.append((key, rel_path))
                assert os.path.exists(
                    rel_path
                ), f"Dead doc link in ERROR_MESSAGES[{key!r}]: {rel_path}"

        # Guard against a vacuous pass if the link format ever changes.
        assert checked, "expected at least one /docs/*.md link in ERROR_MESSAGES to validate"

    def test_error_message_clarity(self):
        """Ensure messages are non-technical and clear"""

        # Test that error messages don't contain technical jargon
        technical_terms = [
            "exception",
            "stack trace",
            "null pointer",
            "undefined",
            "segmentation fault",
            "internal server error",
        ]

        for error_code, message in ERROR_MESSAGES.items():
            for term in technical_terms:
                assert (
                    term.lower() not in message.lower()
                ), f"Technical term '{term}' found in {error_code} message"

    def test_error_message_length_appropriate(self):
        """Verify error messages are neither too short nor too long"""

        for error_code, message in ERROR_MESSAGES.items():
            # Messages should be informative but not overwhelming
            assert len(message) >= 20, f"Error message too short for {error_code}: {message}"
            assert len(message) <= 500, f"Error message too long for {error_code}: {message}"

    def test_error_message_tone_appropriate(self):
        """Ensure error messages have appropriate, helpful tone"""

        positive_indicators = [
            "please",
            "try",
            "check",
            "help",
            "guide",
            "suggestion",
        ]

        negative_indicators = [
            "error",
            "failed",
            "broken",
            "wrong",
            "invalid",
            "bad",
        ]

        for error_code, message in ERROR_MESSAGES.items():
            # Should contain helpful language
            has_positive = any(indicator in message.lower() for indicator in positive_indicators)
            # Should minimize negative language
            negative_count = sum(
                1 for indicator in negative_indicators if indicator in message.lower()
            )

            assert has_positive, f"Error message lacks helpful tone: {message}"
            assert negative_count <= 2, f"Error message too negative: {message}"


class TestIntegrationErrorScenarios:
    """Test error handling across the system.

    #1452 rewrite (2026-07-23): the originals patched `main.classifier` — an
    attribute gone since the intent stack moved into services — so every test
    died at setup with AttributeError. They also pinned pre-degradation 500/502
    error shapes; the CURRENT /api/v1/intent contract is Pattern-007 graceful
    degradation: service failures return HTTP 200 with a conversational
    message (web/api/routes/intent.py `_create_degradation_response`), and
    only request validation returns 422. The rewrites patch the real seam —
    `app.state.intent_service` — and pin the real contract.
    """

    @pytest.fixture
    def test_client(self):
        """Test client for API testing"""
        return TestClient(app)

    @pytest.fixture
    def failing_intent_service(self):
        """Swap app.state.intent_service for a mock; restore after."""
        original = getattr(app.state, "intent_service", None)
        mock_service = AsyncMock()
        app.state.intent_service = mock_service
        yield mock_service
        app.state.intent_service = original

    def test_invalid_api_request_handling(self, test_client):
        """Malformed requests never crash: the route parses the body itself
        and degrades gracefully (Pattern-007) instead of FastAPI 422s."""
        response = test_client.post("/api/v1/intent", data="invalid json")
        assert response.status_code < 500
        assert response.json().get("message")

        response = test_client.post("/api/v1/intent", json={})
        assert response.status_code < 500
        assert response.json().get("message")

    def test_database_connection_error_handling(self, test_client, failing_intent_service):
        """Service failures degrade gracefully: HTTP 200 + friendly message."""
        failing_intent_service.process_intent.side_effect = Exception(
            "Database connection failed"
        )

        response = test_client.post("/api/v1/intent", json={"message": "test"})

        assert response.status_code == 200
        data = response.json()
        assert data["message"], "degradation response must carry a message"
        # No stack traces or raw driver noise to the user
        assert "Traceback" not in data["message"]

    def test_missing_authentication_handling(self, test_client, failing_intent_service):
        """Integration auth failures degrade to guidance, not a 5xx."""
        failing_intent_service.process_intent.side_effect = GitHubAuthFailedError()

        response = test_client.post(
            "/api/v1/intent", json={"message": "create GitHub issue"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["message"]

    def test_malformed_conversation_context_handling(self, test_client):
        """Malformed context must not crash the endpoint (422 or graceful 200)."""
        invalid_context = {
            "session_id": None,
            "conversation_history": "not a list",
        }

        response = test_client.post(
            "/api/v1/intent", json={"message": "test", "context": invalid_context}
        )

        # GREAT-5: graceful handling means validation error or degradation,
        # never an unhandled 500.
        assert response.status_code in (200, 400, 422)

    def test_rate_limiting_error_handling(self, test_client, failing_intent_service):
        """Upstream rate-limit errors degrade without leaking internals."""
        failing_intent_service.process_intent.side_effect = Exception(
            "Rate limit exceeded"
        )

        response = test_client.post("/api/v1/intent", json={"message": "test"})

        assert response.status_code == 200
        data = response.json()
        assert "Traceback" not in data["message"]


class TestPerformanceValidation:
    """Ensure error handling doesn't impact performance"""

    @pytest.fixture
    def test_client(self):
        """Test client for API testing"""
        return TestClient(app)

    def test_error_message_generation_performance(self):
        """Test that error message generation is fast"""

        import time

        # Test error message generation speed
        start_time = time.time()

        for _ in range(100):
            error = TaskFailedError(task_description="test task", recovery_suggestion="try again")
            message = ERROR_MESSAGES["TASK_FAILED"].format(
                task_description=error.details["task_description"],
                recovery_suggestion=error.details["recovery_suggestion"],
            )

        end_time = time.time()
        elapsed = (end_time - start_time) * 1000  # Convert to milliseconds

        # Should complete 100 error messages in under 100ms
        assert elapsed < 100, f"Error message generation too slow: {elapsed:.2f}ms"

    def test_error_handling_response_time(self, test_client):
        """Error responses are fast (degradation path does no heavy work)."""
        import time

        original = getattr(app.state, "intent_service", None)
        mock_service = AsyncMock()
        mock_service.process_intent.side_effect = IntentClassificationFailedError()
        app.state.intent_service = mock_service
        try:
            start_time = time.time()
            response = test_client.post("/api/v1/intent", json={"message": "test"})
            elapsed = (time.time() - start_time) * 1000
        finally:
            app.state.intent_service = original

        assert response.status_code == 200
        # Error responses should be fast (< 500ms)
        assert elapsed < 500, f"Error response too slow: {elapsed:.2f}ms"


class TestErrorRecoverySuggestions:
    """Test automatic recovery suggestions for common errors"""

    def test_common_error_patterns(self):
        """Test that common error patterns have recovery suggestions"""

        # Test common error scenarios and their recovery suggestions
        error_scenarios = [
            {
                "error": TaskFailedError(task_description="database operation"),
                "expected_suggestion": "try again",
            },
            {
                "error": LowConfidenceIntentError(suggestions="try 'list projects'"),
                "expected_suggestion": "list projects",
            },
            {"error": GitHubAuthFailedError(), "expected_suggestion": "check your access token"},
        ]

        for scenario in error_scenarios:
            error = scenario["error"]
            expected = scenario["expected_suggestion"]

            # Verify error includes recovery suggestion
            if hasattr(error, "details") and error.details:
                if "recovery_suggestion" in error.details:
                    assert expected.lower() in error.details["recovery_suggestion"].lower()
                elif "suggestions" in error.details:
                    assert expected.lower() in error.details["suggestions"].lower()


class TestErrorCategorization:
    """Test error categorization and severity levels"""

    def test_error_severity_classification(self):
        """Test that errors are properly categorized by severity"""

        # Define expected severity levels
        critical_errors = [IntentClassificationFailedError, TaskFailedError]
        warning_errors = [LowConfidenceIntentError]
        info_errors = [WorkflowTimeoutError]  # Timeout might be expected in some cases

        # Test severity classification
        for error_class in critical_errors:
            error = error_class()
            assert error.status_code >= 500, f"{error_class.__name__} should be critical"

        for error_class in warning_errors:
            error = error_class()
            assert error.status_code == 422, f"{error_class.__name__} should be warning"

    def test_error_context_categorization(self):
        """Test that errors are properly categorized by context"""

        # Test API errors
        api_errors = [IntentClassificationFailedError, TaskFailedError]
        for error_class in api_errors:
            error = error_class()
            assert isinstance(
                error, APIError
            ), f"{error_class.__name__} should inherit from APIError"

        # Test integration errors
        integration_errors = [GitHubAuthFailedError]
        for error_class in integration_errors:
            error = error_class()
            assert isinstance(
                error, APIError
            ), f"{error_class.__name__} should inherit from APIError"


class TestErrorDocumentation:
    """Test error documentation and user guide integration"""

    def test_error_documentation_consistency(self):
        """Test that error codes have consistent documentation"""

        # Verify all error codes are documented
        documented_errors = set(ERROR_MESSAGES.keys())

        # Get all actual error codes from error classes
        actual_error_codes = set()
        for error_class in [
            IntentClassificationFailedError,
            LowConfidenceIntentError,
            WorkflowTimeoutError,
            TaskFailedError,
            GitHubAuthFailedError,
        ]:
            error = error_class()
            actual_error_codes.add(error.error_code)

        # All actual error codes should be documented
        missing_docs = actual_error_codes - documented_errors
        assert not missing_docs, f"Missing documentation for error codes: {missing_docs}"

    def test_user_guide_error_references(self):
        """Test that user guides reference appropriate error handling"""

        # Check that user guides mention error handling
        user_guide_files = [
            "docs/user-guides/getting-started-conversational-ai.md",
            "docs/user-guides/understanding-anaphoric-references.md",
            "docs/user-guides/conversation-memory-guide.md",
            "docs/user-guides/upgrading-from-command-mode.md",
        ]

        import os

        for guide_file in user_guide_files:
            if os.path.exists(guide_file):
                with open(guide_file, "r") as f:
                    content = f.read()
                    # Should mention troubleshooting or error handling
                    assert any(
                        term in content.lower()
                        for term in ["troubleshoot", "error", "problem", "issue", "help"]
                    ), f"User guide {guide_file} should mention error handling"


if __name__ == "__main__":
    # Run the test suite
    pytest.main([__file__, "-v"])
