"""
Error-handling integration tests for /api/v1/intent.

#1452 rewrite (2026-07-23): the originals patched `main.classifier` /
`main.engine` (attributes gone since the intent stack moved into services)
and pinned the pre-degradation middleware shapes (422 LOW_CONFIDENCE_INTENT,
502 GITHUB_AUTH_FAILED). The CURRENT contract for /api/v1/intent is
Pattern-007 graceful degradation: typed service errors return HTTP 200 with
a user-friendly message extracted by `_extract_degradation_message`
(web/api/routes/intent.py). These tests patch the real seam —
app.state.intent_service — and pin that contract.
"""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from services.api.errors import GitHubAuthFailedError, LowConfidenceIntentError, TaskFailedError
from web.app import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def failing_intent_service():
    """Swap app.state.intent_service for a mock; restore after."""
    original = getattr(app.state, "intent_service", None)
    mock_service = AsyncMock()
    app.state.intent_service = mock_service
    yield mock_service
    app.state.intent_service = original


def test_low_confidence_intent_error(test_client, failing_intent_service):
    """Low-confidence errors degrade to 200 with a usable message."""
    failing_intent_service.process_intent.side_effect = LowConfidenceIntentError(
        suggestions="try 'list projects'"
    )

    response = test_client.post(
        "/api/v1/intent", json={"message": "uhhh, i dunno, show me stuff?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"]
    assert "Traceback" not in data["message"]


def test_workflow_task_failed_error(test_client, failing_intent_service):
    """Task failures degrade to 200 with a friendly message."""
    failing_intent_service.process_intent.side_effect = TaskFailedError(
        task_description="create issue", recovery_suggestion="try again"
    )

    response = test_client.post("/api/v1/intent", json={"message": "create an issue"})

    assert response.status_code == 200
    assert response.json()["message"]


def test_github_auth_failed_error(test_client, failing_intent_service):
    """GitHub auth failures degrade to 200 without leaking internals."""
    failing_intent_service.process_intent.side_effect = GitHubAuthFailedError()

    response = test_client.post("/api/v1/intent", json={"message": "create GitHub issue"})

    assert response.status_code == 200
    data = response.json()
    assert data["message"]
    assert "Traceback" not in data["message"]
