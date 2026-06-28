"""
Integration Tests for Standup API

CORE-STAND-MODES-API (Issue #162) - Task 7
Tests end-to-end workflows with real API server and integrations.

Test Coverage:
- End-to-end workflows (complete request/response cycles)
- All 5 modes: standard, issues, documents, calendar, trifecta
- All 4 formats: json, slack, markdown, text
- Authentication flow (no auth, invalid auth, valid auth)
- Error handling (validation errors, server errors)
- Performance baseline (<2s response time)
"""

import time
from typing import Dict

import pytest
import requests

from services.auth.jwt_service import JWTService

# ============================================================================
# Configuration
# ============================================================================

BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api/v1/standup"

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture(scope="module")
def base_url():
    """Base URL for API server"""
    return BASE_URL


@pytest.fixture(scope="module")
def api_client(base_url):
    """HTTP client for API requests with server verification"""
    # Verify server is running
    try:
        response = requests.get(f"{base_url}/api/v1/standup/health", timeout=5)
        assert response.status_code == 200, "API server not healthy"
    except requests.exceptions.RequestException as e:
        pytest.skip(f"API server not running on port 8001: {e}")

    return requests.Session()


@pytest.fixture(scope="module")
def jwt_service():
    """JWT service for creating auth tokens"""
    return JWTService()


@pytest.fixture(scope="module")
def auth_token(jwt_service):
    """Valid authentication token"""
    return jwt_service.generate_access_token(
        user_id="test_user", user_email="test@example.com", scopes=["read", "write"]
    )


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    """Headers with valid authentication"""
    return {"Authorization": f"Bearer {auth_token}"}


# ============================================================================
# Test: End-to-End Workflows
# ============================================================================


def test_complete_standup_generation_workflow(api_client, auth_headers):
    """Test complete standup generation workflow end-to-end"""
    # 1. Generate standup
    response = api_client.post(
        f"{API_BASE}/generate",
        json={"mode": "standard", "format": "json"},
        headers=auth_headers,
    )

    # 2. Verify success
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "standup" in data
    assert "metadata" in data
    assert "performance_metrics" in data

    # 3. Verify metadata
    metadata = data["metadata"]
    assert metadata["mode"] == "standard"
    assert metadata["format"] == "json"
    assert "user_id" in metadata
    assert "timestamp" in metadata

    # 4. Verify performance metrics exist
    perf = data["performance_metrics"]
    assert "generation_time_ms" in perf
    assert "service_time_ms" in perf


def test_multi_step_workflow(api_client, auth_headers):
    """Test workflow with multiple sequential API calls"""
    # 1. Check health
    health_response = api_client.get(f"{API_BASE}/health")
    assert health_response.status_code == 200
    health_data = health_response.json()
    assert health_data["status"] == "healthy"

    # 2. Get available modes
    modes_response = api_client.get(f"{API_BASE}/modes")
    assert modes_response.status_code == 200
    modes = modes_response.json()["modes"]
    assert len(modes) == 5

    # 3. Get available formats
    formats_response = api_client.get(f"{API_BASE}/formats")
    assert formats_response.status_code == 200
    formats = formats_response.json()["formats"]
    assert len(formats) == 4

    # 4. Generate standup using discovered capabilities
    for mode in ["standard", "issues", "documents"]:
        response = api_client.post(
            f"{API_BASE}/generate",
            json={"mode": mode, "format": "json"},
            headers=auth_headers,
            timeout=30,  # Modes may take longer
        )
        assert response.status_code == 200
        assert response.json()["success"] is True


# ============================================================================
# Test: All Modes Integration
# ============================================================================


@pytest.mark.parametrize(
    "mode",
    [
        "standard",
        "issues",
        "documents",
        "calendar",
        "trifecta",
    ],
)
def test_mode_integration(api_client, auth_headers, mode):
    """Test each mode works end-to-end with real integrations"""
    response = api_client.post(
        f"{API_BASE}/generate",
        json={"mode": mode, "format": "json"},
        headers=auth_headers,
        timeout=30,  # Some modes may take longer with real integrations
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # Verify metadata contains correct mode
    assert data["metadata"]["mode"] == mode

    # Verify standup content exists
    assert "standup" in data
    standup = data["standup"]
    assert isinstance(standup, dict)


# ============================================================================
# Test: All Formats Integration
# ============================================================================


@pytest.mark.parametrize(
    "format_type",
    [
        "json",
        "slack",
        "markdown",
        "text",
    ],
)
def test_format_integration(api_client, auth_headers, format_type):
    """Test each format works end-to-end"""
    response = api_client.post(
        f"{API_BASE}/generate",
        json={"mode": "standard", "format": format_type},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # Verify metadata contains correct format
    assert data["metadata"]["format"] == format_type

    # Verify standup content exists in appropriate format
    standup = data["standup"]
    if format_type == "json":
        assert isinstance(standup, dict)
    else:
        # Slack, markdown, text are strings
        assert isinstance(standup, str)
        assert len(standup) > 0


# ============================================================================
# Test: Authentication Flow Integration
# ============================================================================


def test_authentication_flow_no_token(api_client):
    """Test request without authentication fails"""
    response = api_client.post(f"{API_BASE}/generate", json={"mode": "standard", "format": "json"})

    assert response.status_code == 401
    data = response.json()
    assert "message" in data  # APIError handler returns {"message": ...}


def test_authentication_flow_invalid_token(api_client):
    """Test request with invalid token fails"""
    response = api_client.post(
        f"{API_BASE}/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": "Bearer invalid_token_123"},
    )

    assert response.status_code == 401
    data = response.json()
    assert "message" in data  # APIError handler returns {"message": ...}


def test_authentication_flow_valid_token(api_client, auth_token):
    """Test complete authentication flow end-to-end"""
    # Request with valid token should succeed
    response = api_client.post(
        f"{API_BASE}/generate",
        json={"mode": "standard", "format": "json"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


# ============================================================================
# Test: Error Handling Integration
# ============================================================================


def test_invalid_mode_integration(api_client, auth_headers):
    """Test error handling for invalid mode end-to-end"""
    response = api_client.post(
        f"{API_BASE}/generate",
        json={"mode": "invalid_mode", "format": "json"},
        headers=auth_headers,
    )

    # Should return validation error (422)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # FastAPI/Pydantic validation error


def test_invalid_format_integration(api_client, auth_headers):
    """Test error handling for invalid format end-to-end"""
    response = api_client.post(
        f"{API_BASE}/generate",
        json={"mode": "standard", "format": "invalid_format"},
        headers=auth_headers,
    )

    # Should return validation error (422)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data  # FastAPI/Pydantic validation error


def test_malformed_request_integration(api_client, auth_headers):
    """Test error handling for malformed requests"""
    # Empty body with required auth should use defaults
    response = api_client.post(f"{API_BASE}/generate", json={}, headers=auth_headers)

    # Should succeed with defaults
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["metadata"]["mode"] == "standard"  # Default mode
    assert data["metadata"]["format"] == "json"  # Default format


# ============================================================================
# Test: Performance Baseline
# ============================================================================


def test_response_time_baseline(api_client, auth_headers):
    """Test that API responds within acceptable time (<2s for standard mode)"""
    start_time = time.time()

    response = api_client.post(
        f"{API_BASE}/generate",
        json={"mode": "standard", "format": "json"},
        headers=auth_headers,
    )

    end_time = time.time()
    response_time = end_time - start_time

    assert response.status_code == 200

    # Target: <2 seconds for standard mode
    assert (
        response_time < 2.5
    ), f"Response took {response_time:.2f}s (target <2s, allowing 0.5s margin)"

    # Verify performance metrics in response
    data = response.json()
    perf = data["performance_metrics"]
    assert "generation_time_ms" in perf


def test_concurrent_requests_baseline(api_client, auth_headers):
    """Test handling multiple concurrent requests"""
    import concurrent.futures

    def make_request():
        return api_client.post(
            f"{API_BASE}/generate",
            json={"mode": "standard", "format": "json"},
            headers=auth_headers,
            timeout=10,
        )

    # Test with 3 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(make_request) for _ in range(3)]
        responses = [f.result() for f in futures]

    # All should succeed
    assert all(r.status_code == 200 for r in responses)
    assert all(r.json()["success"] is True for r in responses)


# ============================================================================
# Test: Real Integration Verification
# ============================================================================


def test_real_api_server_integration(api_client):
    """Verify tests are running against real API server, not mocks"""
    # Health check should return real server info
    response = api_client.get(f"{API_BASE}/health")

    assert response.status_code == 200
    data = response.json()

    # Verify real server characteristics
    assert data["status"] == "healthy"
    assert data["service"] == "standup-api"
    assert data["modes_available"] == 5
    assert data["formats_available"] == 4
    assert "timestamp" in data

    # Timestamp should be valid and recent (server may return startup time)
    from datetime import datetime, timezone

    # Parse timestamp - handle both timezone-aware and naive formats
    timestamp_str = data["timestamp"]
    if timestamp_str.endswith("Z"):
        timestamp_str = timestamp_str[:-1] + "+00:00"

    timestamp = datetime.fromisoformat(timestamp_str)

    # Ensure both datetimes are timezone-aware for comparison
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    time_diff = (now - timestamp).total_seconds()

    # Verify timestamp is recent (within last 24 hours)
    # Note: Health endpoint may return server startup time, not current time
    assert 0 <= time_diff < 86400, f"Server timestamp is {time_diff:.0f}s old (should be <24h)"
