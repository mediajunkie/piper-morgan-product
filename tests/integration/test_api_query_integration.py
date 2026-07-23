import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from web.app import app

# #1452 wave 21: these post natural language to /api/v1/intent and assert the
# LIVE classification outcome (category/action) — keyed llm lane. NOTE for the
# llm-lane burn-down: some pinned actions (count_projects) already diverge
# from live behavior even keyed; revisit when the llm lane runs.
pytestmark = pytest.mark.llm


@pytest.fixture(scope="module")
def setup_projects():
    # This fixture could be expanded to set up test data in the DB if needed
    # For now, assumes DB is seeded or uses in-memory/test DB
    pass


def test_list_projects_query(test_client, setup_projects):
    response = test_client.post("/api/v1/intent", json={"message": "List all projects"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"]["category"] == "query"
    assert data["intent"]["action"] == "list_projects"
    assert isinstance(data["message"], str)
    assert "projects" in data["message"].lower() or "project" in data["message"].lower()


def test_get_project_query(test_client, setup_projects):
    # Replace 'test-project-id' with a real project ID from your test DB
    response = test_client.post(
        "/api/v1/intent",
        json={
            "message": "Get project details",
            "context": {"project_id": "test-project-id"},
        },
    )
    # Accepts 200, 404, or 422 depending on DB state and context validity
    assert response.status_code in (200, 404, 422)
    if response.status_code == 422:
        data = response.json()
        assert "project_id" in data.get("detail", "")


def test_get_default_project_query(test_client, setup_projects):
    response = test_client.post("/api/v1/intent", json={"message": "Show me the default project"})
    # Piper now correctly identifies this needs a specific project context
    # Returns 422 when project_id missing rather than assuming "default"
    assert response.status_code == 422
    # Verify it tried the right action but lacked context
    data = response.json()
    assert "get_project_details" in str(data)
    # Piper is now more precise and context-aware, requiring explicit project_id for details


def test_find_project_query(test_client, setup_projects):
    response = test_client.post(
        "/api/v1/intent",
        json={
            "message": "Find project named Web Platform",
            "context": {"name": "Web Platform"},
        },
    )
    # Accepts 200, 404, or 422 depending on DB state and context validity
    assert response.status_code in (200, 404, 422)
    if response.status_code == 422:
        data = response.json()
        assert "name" in data.get("detail", "")


def test_count_projects_query(test_client, setup_projects):
    response = test_client.post("/api/v1/intent", json={"message": "How many projects do we have?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"]["action"] == "count_projects"


def test_get_project_query_missing_id(test_client, setup_projects):
    response = test_client.post("/api/v1/intent", json={"message": "Get project details"})
    assert response.status_code == 422
    # Should return a user-friendly error message
    data = response.json()
    assert "project_id" in data.get("detail", "")


def test_find_project_query_missing_name(test_client, setup_projects):
    response = test_client.post("/api/v1/intent", json={"message": "Find project"})
    assert response.status_code == 422
    data = response.json()
    assert "name" in data.get("detail", "")
