"""
API-Level Degradation Integration Tests
Verification-first methodology: Test that API properly handles QueryRouter degradation responses
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from web.app import app


class TestAPIDegradationIntegration:
    """Test API-level degradation handling and response structure"""

    @pytest.fixture
    def test_client(self):
        """Create test client for API testing with lifespan context and authentication"""
        from uuid import UUID

        # Use context manager to ensure lifespan events run
        with TestClient(app) as client:
            # Generate a valid test token for authentication
            jwt_service = JWTService()
            test_token = jwt_service.generate_access_token(
                user_id=UUID("11111111-1111-1111-1111-111111111111"),
                user_email="test@example.com",
                scopes=[],
            )
            # Add token to default headers for all requests
            client.headers["Authorization"] = f"Bearer {test_token}"
            # #1747/#1809: this fixed test principal holds no stored key, so
            # post-#1809 the /intent gate (correctly) refuses before the
            # degradation behaviors under test are reached. The fake BYOC key on
            # the documented header rung restores reach; an unexpected live
            # spend 401s loudly (see tests/conftest.py E2E_FAKE_BYOC_KEY).
            from tests.conftest import E2E_FAKE_BYOC_KEY

            client.headers["X-User-Api-Key"] = E2E_FAKE_BYOC_KEY
            yield client

    def test_api_handles_database_degradation_gracefully(self, test_client):
        """Test API returns proper structured response when IntentService is unavailable"""

        # Mock IntentService being unavailable (simulates service initialization failure)
        with patch.object(test_client.app.state, "intent_service", None):
            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            # Should return 200 with proper structured response (Pattern-007 graceful degradation)
            assert response.status_code == 200
            data = response.json()

            # Verify IntentResponse structure
            assert "message" in data
            assert "intent" in data
            assert "workflow_id" in data
            assert "requires_clarification" in data
            assert "clarification_type" in data

            # Verify degradation message is user-friendly (stored in error field per Pattern-007)
            assert "Database temporarily unavailable" in data["error"]
            assert "Docker" in data["error"] or "try again" in data["error"]

    def test_api_handles_circuit_breaker_degradation(self, test_client):
        """Test API handles exceptions during intent processing gracefully"""

        # Mock IntentService.process_intent to throw exception
        async def mock_process_intent_error(*args, **kwargs):
            raise Exception("Circuit breaker open")

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            side_effect=mock_process_intent_error,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            # Should return 200 with degradation response (Pattern-007)
            assert response.status_code == 200
            data = response.json()

            # Verify structured degradation response
            assert "message" in data
            assert "intent" in data
            assert "error" in data
            assert data["intent"]["action"] == "clarify"  # Degradation response defaults to clarify
            assert data["requires_clarification"] is True
            assert data["clarification_type"] == "service_unavailable"

    def test_api_handles_context_validation_errors(self, test_client):
        """Test API properly handles context validation errors"""

        # Mock IntentService to return a validation error result
        from services.intent.intent_service import IntentProcessingResult

        # Create a mock that returns validation error result
        mock_result = IntentProcessingResult(
            success=False,
            message="Unable to process",
            intent_data={
                "type": "unknown",
                "confidence": 0,
                "action": "clarify",
            },
            workflow_id=None,
            requires_clarification=True,
            clarification_type="missing_context",
            suggestions=[],
            preferences={},
            error="Missing required context: project_id",
            error_type="validation_error",
        )

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            return_value=mock_result,
            new_callable=AsyncMock,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "Get project details"})

            # Issue #875: Business errors return 200 OK (conversational, not HTTP error)
            assert response.status_code == 200
            data = response.json()

            # Conversational message is in the response body
            assert "message" in data
            # Error metadata present for frontend to optionally use
            assert data.get("error") == "Missing required context: project_id"
            assert data.get("error_type") == "validation_error"

    def test_api_handles_file_service_degradation(self, test_client):
        """Test API handles file service exceptions gracefully"""

        # Mock IntentService.process_intent to throw file service exception
        async def mock_process_intent_file_error(*args, **kwargs):
            raise Exception("File service unavailable")

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            side_effect=mock_process_intent_file_error,
        ):
            response = test_client.post(
                "/api/v1/intent",
                json={"message": "Read file contents", "context": {"resolved_file_id": "test-id"}},
            )

            # Should return 200 with degradation response (Pattern-007)
            assert response.status_code == 200
            data = response.json()

            # Verify structured degradation response (can't determine intended action from exception)
            assert "message" in data
            assert "intent" in data
            assert data["intent"]["action"] == "clarify"  # Degradation defaults to clarify
            assert data["requires_clarification"] is True
            assert data["error_type"] == "service_unavailable"

    def test_api_handles_conversation_service_degradation(self, test_client):
        """Test API handles conversation service exceptions gracefully"""

        # Mock IntentService.process_intent to throw conversation service exception
        async def mock_process_intent_conv_error(*args, **kwargs):
            raise Exception("Conversation service unavailable")

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            side_effect=mock_process_intent_conv_error,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "Hello"})

            # Should return 200 with degradation response (Pattern-007)
            assert response.status_code == 200
            data = response.json()

            # Verify structured degradation response
            assert "message" in data
            assert "intent" in data
            assert data["intent"]["action"] == "clarify"  # Degradation defaults to clarify
            assert data["error_type"] == "service_unavailable"

    def test_api_maintains_response_structure_consistency(self, test_client):
        """Test API maintains consistent response structure when IntentService unavailable"""

        messages = [
            "List all projects",
            "How many projects do we have?",
            "Show me the default project",
        ]

        # Test that all scenarios return consistent degradation response structure
        with patch.object(test_client.app.state, "intent_service", None):
            for message in messages:
                response = test_client.post("/api/v1/intent", json={"message": message})

                # All should return 200 with consistent structure (Pattern-007)
                assert response.status_code == 200
                data = response.json()

                # Verify consistent IntentResponse structure for degradation
                assert "message" in data
                assert "intent" in data
                assert "workflow_id" in data
                assert "requires_clarification" in data
                assert "clarification_type" in data
                assert "error" in data  # Degradation response includes error field

                # Verify degradation intent structure (no specific action can be determined)
                assert data["intent"]["action"] == "clarify"  # Degradation defaults to clarify
                assert data["requires_clarification"] is True
                assert data["clarification_type"] == "service_unavailable"
                assert "confidence" in data["intent"]
                assert data["intent"]["confidence"] == 0  # No confidence when degraded

    def test_api_handles_mixed_response_types(self, test_client):
        """Test API properly handles different error scenarios"""

        from services.intent.intent_service import IntentProcessingResult

        # Test 1: Service returns successful result without errors
        success_result = IntentProcessingResult(
            success=True,
            message="Found 3 projects in your workspace",
            intent_data={
                "type": "query",
                "confidence": 0.95,
                "action": "list_projects",
            },
            workflow_id=None,
            requires_clarification=False,
            clarification_type=None,
            suggestions=[],
            preferences={},
            error=None,
            error_type=None,
        )

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            return_value=success_result,
            new_callable=AsyncMock,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            assert response.status_code == 200
            data = response.json()
            assert "3 projects" in data["message"]
            assert data["intent"]["action"] == "list_projects"

        # Test 2: Service returns business error (Issue #875: returns 200 OK, not 422)
        validation_result = IntentProcessingResult(
            success=False,
            message="Cannot process request",
            intent_data={
                "type": "unknown",
                "confidence": 0,
                "action": "clarify",
            },
            workflow_id=None,
            requires_clarification=True,
            clarification_type="missing_context",
            suggestions=[],
            preferences={},
            error="File service temporarily unavailable",
            error_type="validation_error",
        )

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            return_value=validation_result,
            new_callable=AsyncMock,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "Read file contents"})

            # Issue #875: Business errors return 200 OK (conversational response)
            assert response.status_code == 200
            data = response.json()
            assert data.get("error") == "File service temporarily unavailable"
            assert "message" in data

    def test_api_error_recovery_mechanism(self, test_client):
        """Test API can recover from temporary failures"""

        from services.intent.intent_service import IntentProcessingResult

        # First call: IntentService returns degradation result
        degradation_result = IntentProcessingResult(
            success=False,
            message="Service error detected",
            intent_data={
                "type": "unknown",
                "confidence": 0,
                "action": "clarify",
            },
            workflow_id=None,
            requires_clarification=True,
            clarification_type="service_unavailable",
            suggestions=[],
            preferences={},
            error="Database temporarily unavailable. Please ensure Docker is running and try again.",
            error_type="service_unavailable",
        )

        success_result = IntentProcessingResult(
            success=True,
            message="Found 3 projects",
            intent_data={
                "type": "query",
                "confidence": 0.95,
                "action": "list_projects",
            },
            workflow_id=None,
            requires_clarification=False,
            clarification_type=None,
            suggestions=[],
            preferences={},
            error=None,
            error_type=None,
        )

        # Mock to return degradation first, then success
        mock_responses = [degradation_result, success_result]
        call_count = [0]

        async def side_effect(*args, **kwargs):
            result = mock_responses[call_count[0]]
            call_count[0] += 1
            return result

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            side_effect=side_effect,
        ):
            # First call returns degradation result with error (Issue #875: 200 OK, not 422)
            response1 = test_client.post("/api/v1/intent", json={"message": "List all projects"})
            assert response1.status_code == 200  # Business error is conversational response
            data1 = response1.json()
            assert (
                data1.get("error")
                == "Database temporarily unavailable. Please ensure Docker is running and try again."
            )

            # Second call should work normally (200 with success response)
            response2 = test_client.post("/api/v1/intent", json={"message": "List all projects"})
            assert response2.status_code == 200
            data2 = response2.json()
            # Should not contain degradation message
            assert "3 projects" in data2["message"]
            assert data2["intent"]["action"] == "list_projects"

    def test_api_graceful_degradation_message_quality(self, test_client):
        """Test degradation messages are user-friendly and actionable"""

        # Mock IntentService to throw exception with database error
        async def mock_database_error(*args, **kwargs):
            raise Exception("Database connection failed")

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            side_effect=mock_database_error,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            assert response.status_code == 200
            data = response.json()
            error_message = data["error"]

            # Verify message quality criteria
            assert "temporarily unavailable" in error_message.lower()
            assert any(
                word in error_message.lower()
                for word in ["docker", "try again", "ensure", "containers"]
            )
            assert len(error_message) > 20  # Should be informative
            assert not any(
                word in error_message.lower() for word in ["traceback"]
            )  # No raw exception info

    def test_api_maintains_backward_compatibility(self, test_client):
        """Test API maintains backward compatibility with existing response patterns"""

        from services.intent.intent_service import IntentProcessingResult

        # Test successful query maintains existing response structure
        success_result = IntentProcessingResult(
            success=True,
            message="I found 2 projects: project1, project2",
            intent_data={
                "type": "query",
                "confidence": 0.95,
                "action": "list_projects",
            },
            workflow_id="workflow-123",
            requires_clarification=False,
            clarification_type=None,
            suggestions=[
                {"title": "View details", "message": "Get more details about a project"},
            ],
            preferences={},
            error=None,
            error_type=None,
        )

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            return_value=success_result,
            new_callable=AsyncMock,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            assert response.status_code == 200
            data = response.json()

            # Verify existing response structure is maintained
            assert "message" in data
            assert "intent" in data
            assert "workflow_id" in data
            assert "requires_clarification" in data
            assert "clarification_type" in data
            assert "suggestions" in data
            assert "preferences" in data

            # Verify successful response content
            assert "I found 2 projects" in data["message"]
            assert "project1" in data["message"]
            assert "project2" in data["message"]
            assert data["intent"]["action"] == "list_projects"
            # Issue #878: workflow_id is stripped for sync handlers (async_work_started=False)
            assert data["workflow_id"] is None

    def test_intent_business_error_returns_200_not_422(self, test_client):
        """Contract: IntentService business errors are conversational, not HTTP errors.

        Issue #875: The Nov 2025 refactor (#385) accidentally converted business-logic
        errors to HTTP 422 via validation_error(). This test prevents that regression.

        Design decision: The intent endpoint returns 200 OK for ALL responses from
        IntentService. Errors are conversational responses displayed in the chat window,
        not HTTP error codes.
        """
        from services.intent.intent_service import IntentProcessingResult

        mock_result = IntentProcessingResult(
            success=False,
            message="I'd love to help with planning! Are you thinking sprint planning, a feature roadmap, or something else?",
            intent_data={"type": "strategy", "confidence": 0.8, "action": "plan"},
            error="planning_type_not_specified",
            error_type="validation",
        )
        mock_service = AsyncMock()
        mock_service.process_intent = AsyncMock(return_value=mock_result)

        with patch.object(test_client.app.state, "intent_service", mock_service):
            response = test_client.post(
                "/api/v1/intent",
                json={"message": "Help me plan Q3"},
            )

        # MUST be 200 OK — this is a conversational response, not an HTTP error
        assert response.status_code == 200
        data = response.json()

        # Response contains the conversational message
        assert "message" in data
        assert "planning" in data["message"].lower()

        # Error metadata is present for frontend to optionally use
        assert data.get("error") == "planning_type_not_specified"
        assert data.get("error_type") == "validation"

    def test_make_error_result_produces_conversational_messages(self):
        """Contract: Handler exceptions never leak raw error text to users.

        Issue #876: All handler except blocks use _make_error_result()
        which routes through UserFriendlyErrorService for conversational messages.
        Raw exception text is preserved in the `error` field for debugging only.
        """
        from services.intent.intent_service import IntentProcessingResult, IntentService

        service = IntentService()

        # Simulate a raw exception that would be caught by a handler
        class FakeIntent:
            category = type("C", (), {"value": "query"})()
            action = "list_issues"
            confidence = 0.9

        result = service._make_error_result(
            intent=FakeIntent(),
            workflow_id="test-wf-876",
            error=ConnectionError("Connection refused"),
            context="fetching GitHub issues",
            error_type="GitHubError",
        )

        assert isinstance(result, IntentProcessingResult)
        # Message should NOT contain raw exception text
        assert "Connection refused" not in result.message
        # Message SHOULD be conversational (not empty, not just a technical snippet)
        assert len(result.message) > 20
        # Raw error preserved for debugging in the error field
        assert "Connection refused" in result.error
        assert result.error_type == "GitHubError"
        assert result.success is False
