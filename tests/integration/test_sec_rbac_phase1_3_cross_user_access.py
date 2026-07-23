"""
Integration tests for SEC-RBAC Phase 1.3: Cross-User Access Blocking

Tests that users cannot access resources owned by other users across all endpoints.
Verifies that 404 responses are returned when trying to access non-owned resources.

Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
"""

from uuid import UUID

import pytest
import structlog
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from services.database.models import FeedbackDB, KnowledgeNodeDB, ListDB, ProjectDB, TodoDB

logger = structlog.get_logger(__name__)


@pytest.fixture
def jwt_service():
    """Create a JWT service instance for testing."""
    return JWTService()


class TestCrossUserAccessBlocking:
    """Verify users cannot access each other's resources."""

    def test_list_cross_user_access_blocked(
        self, client_with_intent: TestClient, db_session, jwt_service: JWTService
    ):
        """
        Test that User A cannot read/update/delete lists owned by User B.
        Returns 404 for non-owned resources.
        """
        user_a_uuid = UUID("550e8400-e29b-41d4-a716-446655440000")
        user_b_uuid = UUID("550e8400-e29b-41d4-a716-446655440001")
        user_a_id = str(user_a_uuid)
        user_b_id = str(user_b_uuid)

        # Create lists for both users
        user_b_list = ListDB(
            name="User B List",
            description="Owned by B",
            owner_id=user_b_id,
        )

        db_session.add(user_b_list)
        db_session.commit()
        user_b_list_id = str(user_b_list.id)

        # Generate token for User A
        user_a_token = jwt_service.generate_access_token(
            user_id=user_a_uuid,
            user_email="user-a@test.com",
            scopes=["read", "write"],
        )

        # User A tries to read User B's list (should get 404)
        response = client_with_intent.get(
            f"/api/v1/lists/{user_b_list_id}",
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot read User B's list (404 response)")

        # User A tries to update User B's list (should get 404)
        response = client_with_intent.put(
            f"/api/v1/lists/{user_b_list_id}",
            json={"name": "Hacked Name"},
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot update User B's list (404 response)")

        # User A tries to delete User B's list (should get 404)
        response = client_with_intent.delete(
            f"/api/v1/lists/{user_b_list_id}",
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot delete User B's list (404 response)")

    def test_todo_cross_user_access_blocked(
        self, client_with_intent: TestClient, db_session, jwt_service: JWTService
    ):
        """
        Test that User A cannot read/update/delete todos owned by User B.
        Returns 404 for non-owned resources.
        """
        user_a_uuid = UUID("550e8400-e29b-41d4-a716-446655440010")
        user_b_uuid = UUID("550e8400-e29b-41d4-a716-446655440011")
        user_b_id = str(user_b_uuid)

        # Create todo for User B
        user_b_todo = TodoDB(
            description="User B Todo",
            status="in_progress",
            priority="low",
            owner_id=user_b_id,
        )

        db_session.add(user_b_todo)
        db_session.commit()
        user_b_todo_id = str(user_b_todo.id)

        # Generate token for User A
        user_a_token = jwt_service.generate_access_token(
            user_id=user_a_uuid,
            user_email="user-a@test.com",
            scopes=["read", "write"],
        )

        # User A tries to read User B's todo (should get 404)
        response = client_with_intent.get(
            f"/api/v1/todos/{user_b_todo_id}",
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot read User B's todo (404 response)")

        # User A tries to update User B's todo (should get 404)
        response = client_with_intent.put(
            f"/api/v1/todos/{user_b_todo_id}",
            json={"status": "completed"},
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot update User B's todo (404 response)")

        # User A tries to delete User B's todo (should get 404)
        response = client_with_intent.delete(
            f"/api/v1/todos/{user_b_todo_id}",
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot delete User B's todo (404 response)")

    def test_project_cross_user_access_blocked(
        self, client_with_intent: TestClient, db_session, jwt_service: JWTService
    ):
        """
        Test that User A cannot read/update/delete projects owned by User B.
        Returns 404 for non-owned resources.
        """
        user_a_uuid = UUID("550e8400-e29b-41d4-a716-446655440020")
        user_b_uuid = UUID("550e8400-e29b-41d4-a716-446655440021")
        user_b_id = str(user_b_uuid)

        # Create project for User B
        user_b_project = ProjectDB(
            name="User B Project",
            description="Owned by B",
            owner_id=user_b_id,
        )

        db_session.add(user_b_project)
        db_session.commit()
        user_b_project_id = str(user_b_project.id)

        # Generate token for User A
        user_a_token = jwt_service.generate_access_token(
            user_id=user_a_uuid,
            user_email="user-a@test.com",
            scopes=["read", "write"],
        )

        # User A tries to read User B's project (should get 404)
        response = client_with_intent.get(
            f"/api/v1/projects/{user_b_project_id}",
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot read User B's project (404 response)")

        # User A tries to update User B's project (should get 404)
        response = client_with_intent.put(
            f"/api/v1/projects/{user_b_project_id}",
            json={"name": "Hacked Project"},
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot update User B's project (404 response)")

        # User A tries to delete User B's project (should get 404)
        response = client_with_intent.delete(
            f"/api/v1/projects/{user_b_project_id}",
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot delete User B's project (404 response)")

    def test_feedback_cross_user_access_blocked(
        self, client_with_intent: TestClient, db_session, jwt_service: JWTService
    ):
        """
        Test that User A cannot read feedback owned by User B.
        Returns 404 for non-owned resources.
        """
        user_a_uuid = UUID("550e8400-e29b-41d4-a716-446655440030")
        user_b_uuid = UUID("550e8400-e29b-41d4-a716-446655440031")
        user_b_id = str(user_b_uuid)

        # Create feedback for User B
        from uuid import uuid4 as _uuid4

        user_b_feedback = FeedbackDB(
            id=str(_uuid4()),
            session_id="rbac-test-session-b",
            comment="Feedback from B",
            feedback_type="bug",
            user_id=user_b_id,
            owner_id=user_b_id,
        )

        db_session.add(user_b_feedback)
        db_session.commit()
        user_b_feedback_id = str(user_b_feedback.id)

        # Generate token for User A
        user_a_token = jwt_service.generate_access_token(
            user_id=user_a_uuid,
            user_email="user-a@test.com",
            scopes=["read", "write"],
        )

        # User A tries to read User B's feedback (should get 404)
        response = client_with_intent.get(
            f"/api/v1/feedback/{user_b_feedback_id}",
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot read User B's feedback (404 response)")

    def test_knowledge_graph_cross_user_access_blocked(
        self, client_with_intent: TestClient, db_session, jwt_service: JWTService
    ):
        """
        Test that User A cannot access knowledge nodes owned by User B.
        Returns 404 for non-owned resources.
        """
        user_a_uuid = UUID("550e8400-e29b-41d4-a716-446655440040")
        user_b_uuid = UUID("550e8400-e29b-41d4-a716-446655440041")
        user_b_id = str(user_b_uuid)

        # Create knowledge node for User B
        user_b_node = KnowledgeNodeDB(
            name="User B Concept",
            node_type="CONCEPT",
            description="Owned by B",
            properties={},
            owner_id=user_b_id,
        )

        db_session.add(user_b_node)
        db_session.commit()
        user_b_node_id = str(user_b_node.id)

        # Generate token for User A
        user_a_token = jwt_service.generate_access_token(
            user_id=user_a_uuid,
            user_email="user-a@test.com",
            scopes=["read", "write"],
        )

        # User A tries to read User B's knowledge node (should get 404)
        response = client_with_intent.get(
            f"/api/v1/knowledge/nodes/{user_b_node_id}",
            headers={"Authorization": f"Bearer {user_a_token}"},
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        logger.info("✅ User A cannot read User B's knowledge node (404 response)")
