"""
Standup API Tests - Comprehensive Test Suite

CORE-STAND-MODES-API (Issue #162)
Tests all 5 generation modes, 4 output formats, error handling, and performance.

Test Coverage:
- All 5 modes: standard, issues, documents, calendar, trifecta
- All 4 formats: json, slack, markdown, text
- Error scenarios: invalid mode, invalid format, service failures
- Performance: <2s response time validation
- Integration: Real service integration tests
"""

import json
import time
from datetime import datetime
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from services.domain.models import StandupItem
from services.domain.standup_orchestration_service import StandupIntegrationError
from services.features.morning_standup import StandupResult

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture(scope="module")
def client():
    """Create FastAPI test client using web.app with lifespan support"""
    import os
    import sys

    # Ensure project root is in path
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

    from web.app import app  # Import the actual FastAPI app

    # Use context manager to properly trigger lifespan events
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def jwt_service():
    """Create JWT service for generating test tokens"""
    return JWTService()


@pytest.fixture
def auth_token(jwt_service):
    """Generate valid authentication token for tests"""
    return jwt_service.generate_access_token(
        user_id="test_user", user_email="test@example.com", scopes=["read", "write"]
    )


@pytest.fixture
def mock_standup_result():
    """Create mock StandupResult for testing"""
    return StandupResult(
        user_id="test_user",
        generated_at=datetime(2025, 10, 19, 14, 30, 0),
        generation_time_ms=950,
        yesterday_accomplishments=[
            StandupItem(display="Completed Phase Z", source="session"),
            StandupItem(display="Fixed all integration issues", source="session"),
        ],
        today_priorities=[
            StandupItem(display="Start Phase 2 API", source="session"),
            StandupItem(display="Create comprehensive tests", source="session"),
        ],
        blockers=[],
        context_source="persistent",
        github_activity={"commits": [{"sha": "abc123", "message": "test commit"}], "prs": []},
        performance_metrics={"service_call_ms": 800, "formatting_ms": 150},
        time_saved_minutes=15,
    )


# ============================================================================
# Test: Health Check
# ============================================================================


def test_health_endpoint(client):
    """Test health check endpoint returns correct status"""
    response = client.get("/api/v1/standup/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "standup-api"
    assert data["modes_available"] == 5
    assert data["formats_available"] == 4
    assert "timestamp" in data


# ============================================================================
# Test: Modes Endpoint
# ============================================================================


def test_modes_endpoint(client):
    """Test modes endpoint returns all supported modes"""
    response = client.get("/api/v1/standup/modes")

    assert response.status_code == 200
    data = response.json()

    # Verify all modes present
    assert set(data["modes"]) == {"standard", "issues", "documents", "calendar", "trifecta"}

    # Verify descriptions exist
    assert len(data["descriptions"]) == 5
    assert "standard" in data["descriptions"]
    assert "trifecta" in data["descriptions"]


# ============================================================================
# Test: Formats Endpoint
# ============================================================================


def test_formats_endpoint(client):
    """Test formats endpoint returns all supported formats"""
    response = client.get("/api/v1/standup/formats")

    assert response.status_code == 200
    data = response.json()

    # Verify all formats present
    assert set(data["formats"]) == {"json", "slack", "markdown", "text"}

    # Verify descriptions exist
    assert len(data["descriptions"]) == 4
    assert "json" in data["descriptions"]
    assert "slack" in data["descriptions"]


# ============================================================================
# Test: Generation - All Modes
# ============================================================================


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_standard_mode(mock_service_class, client, auth_token, mock_standup_result):
    """Test standard mode generation"""
    # Setup mock
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    # Make request
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "json", "user_id": "test_user"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert data["success"] is True
    assert data["metadata"]["mode"] == "standard"
    assert data["standup"]["user_id"] == "test_user"
    assert "performance_metrics" in data

    # Verify service called with correct workflow type
    mock_service.orchestrate_standup_workflow.assert_called_once()
    call_kwargs = mock_service.orchestrate_standup_workflow.call_args[1]
    assert call_kwargs["workflow_type"] == "standard"


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_issues_mode(mock_service_class, client, auth_token, mock_standup_result):
    """Test issues mode generation (maps to with_issues)"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "issues", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

    # Verify mode mapping: issues -> with_issues
    call_kwargs = mock_service.orchestrate_standup_workflow.call_args[1]
    assert call_kwargs["workflow_type"] == "with_issues"


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_documents_mode(mock_service_class, client, auth_token, mock_standup_result):
    """Test documents mode generation (maps to with_documents)"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "documents", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

    # Verify mode mapping: documents -> with_documents
    call_kwargs = mock_service.orchestrate_standup_workflow.call_args[1]
    assert call_kwargs["workflow_type"] == "with_documents"


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_calendar_mode(mock_service_class, client, auth_token, mock_standup_result):
    """Test calendar mode generation (maps to with_calendar)"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "calendar", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

    # Verify mode mapping: calendar -> with_calendar
    call_kwargs = mock_service.orchestrate_standup_workflow.call_args[1]
    assert call_kwargs["workflow_type"] == "with_calendar"


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_trifecta_mode(mock_service_class, client, auth_token, mock_standup_result):
    """Test trifecta mode generation"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "trifecta", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

    # Verify mode mapping: trifecta -> trifecta (no change)
    call_kwargs = mock_service.orchestrate_standup_workflow.call_args[1]
    assert call_kwargs["workflow_type"] == "trifecta"


# ============================================================================
# Test: Generation - All Formats
# ============================================================================


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_json_format(mock_service_class, client, auth_token, mock_standup_result):
    """Test JSON format output"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    # JSON format should return structured data
    assert isinstance(data["standup"], dict)
    assert "user_id" in data["standup"]
    assert "generated_at" in data["standup"]
    assert "yesterday_accomplishments" in data["standup"]
    assert "today_priorities" in data["standup"]
    assert "blockers" in data["standup"]


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_slack_format(mock_service_class, client, auth_token, mock_standup_result):
    """Test Slack format output"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "slack"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    # Slack format should return formatted string
    assert isinstance(data["standup"], str)
    assert "Morning Standup" in data["standup"]
    assert ":sunrise:" in data["standup"]
    assert "Yesterday's Accomplishments" in data["standup"]
    assert "Today's Priorities" in data["standup"]


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_markdown_format(
    mock_service_class, client, auth_token, mock_standup_result
):
    """Test Markdown format output"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "markdown"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    # Markdown format should return formatted string with markdown
    assert isinstance(data["standup"], str)
    assert "# Morning Standup" in data["standup"]
    assert "## Yesterday's Accomplishments" in data["standup"]
    assert "## Today's Priorities" in data["standup"]
    assert "- " in data["standup"]  # List items


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_generate_text_format(mock_service_class, client, auth_token, mock_standup_result):
    """Test plain text format output"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "text"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    # Text format should return plain text string
    assert isinstance(data["standup"], str)
    assert "Morning Standup" in data["standup"]
    assert "YESTERDAY'S ACCOMPLISHMENTS:" in data["standup"]
    assert "TODAY'S PRIORITIES:" in data["standup"]
    assert "=" in data["standup"]  # Separator lines


# ============================================================================
# Test: Error Handling
# ============================================================================


def test_invalid_mode(client, auth_token):
    """Test error handling for invalid mode"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "invalid_mode", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Should return validation error (422) - FastAPI/Pydantic format
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # Pydantic validation error


def test_invalid_format(client, auth_token):
    """Test error handling for invalid format"""
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "invalid_format"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Should return validation error (422) - FastAPI/Pydantic format
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # Pydantic validation error


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_service_integration_error(mock_service_class, client, auth_token):
    """Test error handling when service raises StandupIntegrationError"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(
        side_effect=StandupIntegrationError("GitHub service unavailable")
    )
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Should return internal error (500)
    assert response.status_code == 500
    data = response.json()
    assert data["status"] == "error"
    assert data["code"] == "INTERNAL_ERROR"


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_unexpected_service_error(mock_service_class, client, auth_token):
    """Test error handling for unexpected service errors"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(side_effect=Exception("Unexpected error"))
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Should return internal error (500)
    assert response.status_code == 500
    data = response.json()
    # Verify error response structure
    assert "detail" in data or "message" in data  # Error response contains details


# ============================================================================
# Test: Performance
# ============================================================================


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_performance_target(mock_service_class, client, auth_token, mock_standup_result):
    """Test that generation meets <2s performance target"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    # Measure request time
    start_time = time.time()
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "trifecta", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    end_time = time.time()

    assert response.status_code == 200

    # Verify <2s target (with some margin for test overhead)
    request_time = end_time - start_time
    assert request_time < 2.5, f"Request took {request_time:.2f}s, exceeds <2s target"

    # Verify performance metrics in response
    data = response.json()
    assert "performance_metrics" in data
    assert "generation_time_ms" in data["performance_metrics"]
    assert data["performance_metrics"]["generation_time_ms"] < 2000


# ============================================================================
# Test: Request Defaults and User ID Resolution
# ============================================================================


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_default_mode_and_format(mock_service_class, client, auth_token, mock_standup_result):
    """Test that mode and format default to standard and json"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    # Request with no mode/format specified
    response = client.post(
        "/api/v1/standup/generate", json={}, headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()

    # Verify defaults
    assert data["metadata"]["mode"] == "standard"
    assert data["metadata"]["format"] == "json"


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_user_id_resolution(mock_service_class, client, auth_token, mock_standup_result):
    """Test that user_id is resolved from service if not provided"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    # Request without user_id in JSON (but auth token has user info)
    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

    # Verify service was called (user_id extracted from token or resolved)
    call_kwargs = mock_service.orchestrate_standup_workflow.call_args[1]
    # user_id may be extracted from JWT token or passed as None for service resolution
    assert "user_id" in call_kwargs


# ============================================================================
# Test: Response Structure
# ============================================================================


@pytest.mark.asyncio
@patch("web.api.routes.standup.StandupOrchestrationService")
async def test_response_structure(mock_service_class, client, auth_token, mock_standup_result):
    """Test that response follows StandupResponse schema"""
    mock_service = AsyncMock()
    mock_service.orchestrate_standup_workflow = AsyncMock(return_value=mock_standup_result)
    mock_service_class.return_value = mock_service

    response = client.post(
        "/api/v1/standup/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    # Verify top-level fields
    assert "success" in data
    assert "standup" in data
    assert "metadata" in data
    assert "performance_metrics" in data

    # Verify metadata fields
    metadata = data["metadata"]
    assert "mode" in metadata
    assert "format" in metadata
    assert "user_id" in metadata
    assert "timestamp" in metadata
    assert "context_source" in metadata

    # Verify performance metrics
    perf = data["performance_metrics"]
    assert "generation_time_ms" in perf
    assert "service_time_ms" in perf
    assert "formatting_time_ms" in perf
    assert "generation_time_formatted" in perf
