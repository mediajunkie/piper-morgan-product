"""
Issue #559: Integration Tests for Real Intent Wiring Verification

These tests verify that REAL code paths work - no mocking of internal methods.
This addresses Pattern-045 ("Green Tests, Red User") where mocked tests passed
but the actual feature was broken.

Tests verify:
1. Import paths are correct (not mocked modules)
2. Method names exist (not mocked methods)
3. HTTP -> Service -> Handler chain works end-to-end
4. Auth middleware exclusions work correctly

Anti-Pattern Detection:
- If these tests pass but features don't work, we have a TEST GAP
- Never mock _check_portfolio_onboarding, _get_onboarding_components, etc.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

import httpx
import pytest
from httpx import ASGITransport
from sqlalchemy import text

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


class TestImportWiringVerification:
    """
    Verify that all import paths used in production code actually work.

    These tests catch bugs like:
    - Wrong import paths (module doesn't exist)
    - Wrong class/function names (symbol doesn't exist)
    - Circular import issues
    """

    def test_onboarding_imports_from_conversation_handler(self):
        """
        Issue #559: Verify _get_onboarding_components can import successfully.

        This catches the bug where we mocked this function, hiding that
        the actual imports were broken.
        """
        # This import should NOT fail if the code is correctly wired
        from services.conversation.conversation_handler import _get_onboarding_components

        # Actually call it to verify the lazy imports work
        manager, handler = _get_onboarding_components()

        # Verify we got real objects, not mocks
        assert manager is not None
        assert handler is not None
        assert hasattr(manager, "create_session")
        assert hasattr(handler, "start_onboarding")
        assert hasattr(handler, "handle_turn")

    def test_intent_service_onboarding_imports(self):
        """
        Issue #559: Verify IntentService._check_active_onboarding imports work.

        The method uses inline imports - verify they resolve correctly.
        """
        # Verify the import chain works
        from services.conversation.conversation_handler import _get_onboarding_components
        from services.shared_types import IntentCategory, PortfolioOnboardingState

        # Verify PortfolioOnboardingState exists and has expected values
        assert hasattr(PortfolioOnboardingState, "INITIATED")
        assert hasattr(PortfolioOnboardingState, "GATHERING_PROJECTS")
        assert hasattr(PortfolioOnboardingState, "COMPLETE")
        assert hasattr(PortfolioOnboardingState, "DECLINED")

        # Verify IntentCategory.GUIDANCE exists (used in onboarding responses)
        assert hasattr(IntentCategory, "GUIDANCE")

    def test_first_meeting_detector_imports(self):
        """
        Issue #559: Verify FirstMeetingDetector can be imported and used.
        """
        from services.onboarding import FirstMeetingDetector

        # Verify the class exists and has the expected interface
        assert hasattr(FirstMeetingDetector, "should_trigger")

    def test_project_repository_imports(self):
        """
        Issue #559: Verify ProjectRepository imports work.

        This is used in _check_portfolio_onboarding.
        """
        from services.database.repositories import ProjectRepository

        # Verify the class exists
        assert ProjectRepository is not None

    def test_intent_service_can_instantiate(self):
        """
        Issue #559: Verify IntentService can be instantiated without mocks.
        """
        from services.intent.intent_service import IntentService

        # This should not raise if dependencies are correctly wired
        service = IntentService()

        # Verify key methods exist
        assert hasattr(service, "process_intent")
        assert hasattr(service, "_check_active_onboarding")
        assert callable(service.process_intent)


class TestMethodExistence:
    """
    Verify that internal methods used in tests actually exist.

    These tests catch bugs where we mocked methods that didn't exist,
    or methods that were renamed/removed.
    """

    def test_conversation_handler_methods_exist(self):
        """
        Issue #559: Verify ConversationHandler has expected methods.
        """
        from services.conversation.conversation_handler import ConversationHandler

        handler = ConversationHandler()

        # Methods that were being mocked - verify they actually exist
        assert hasattr(handler, "_check_portfolio_onboarding")
        assert hasattr(handler, "_get_calendar_summary")
        assert hasattr(handler, "_persist_onboarding_projects")
        assert hasattr(handler, "respond")

        # Verify they're callable
        assert callable(handler._check_portfolio_onboarding)
        assert callable(handler._get_calendar_summary)
        assert callable(handler._persist_onboarding_projects)

    def test_intent_service_methods_exist(self):
        """
        Issue #559: Verify IntentService has expected internal methods.
        """
        from services.intent.intent_service import IntentService

        service = IntentService()

        # Methods that MUST exist for onboarding to work
        assert hasattr(service, "_check_active_onboarding")
        assert hasattr(service, "_persist_onboarding_projects")

    def test_onboarding_handler_methods_exist(self):
        """
        Issue #559: Verify PortfolioOnboardingHandler has expected methods.
        """
        from services.onboarding import PortfolioOnboardingHandler, PortfolioOnboardingManager

        manager = PortfolioOnboardingManager()
        handler = PortfolioOnboardingHandler(manager)

        # Methods used in the integration
        assert hasattr(handler, "start_onboarding")
        assert hasattr(handler, "handle_turn")

        # Manager methods
        assert hasattr(manager, "create_session")
        assert hasattr(manager, "get_session_by_user")
        assert hasattr(manager, "get_session_by_session_id")


class TestAuthMiddlewareExclusions:
    """
    Verify auth middleware correctly excludes/includes expected paths.

    These tests catch the bug where /api/v1/intent wasn't excluded,
    causing authenticated user_id to be None even when cookies were present.
    """

    def test_intent_endpoint_excluded_from_auth(self):
        """
        Issue #559: Verify /api/v1/intent is in middleware exclude list.

        This is critical for optional auth pattern - intent endpoint should
        be accessible without auth, but should get user_id when auth present.
        """
        from services.auth.auth_middleware import AuthMiddleware
        from services.auth.jwt_service import JWTService

        # Create middleware with default exclusions
        class MockApp:
            pass

        jwt_service = JWTService()
        middleware = AuthMiddleware(MockApp(), jwt_service)

        # Verify /api/v1/intent is excluded
        assert middleware._should_exclude_path("/api/v1/intent")

    def test_auth_required_paths_not_excluded(self):
        """
        Issue #559: Verify protected paths are NOT excluded.
        """
        from services.auth.auth_middleware import AuthMiddleware
        from services.auth.jwt_service import JWTService

        class MockApp:
            pass

        jwt_service = JWTService()
        middleware = AuthMiddleware(MockApp(), jwt_service)

        # These paths should require auth
        assert not middleware._should_exclude_path("/api/v1/todos")
        assert not middleware._should_exclude_path("/api/v1/projects")
        assert not middleware._should_exclude_path("/api/v1/settings")

    def test_setup_endpoints_excluded(self):
        """
        Issue #559: Verify setup endpoints are excluded for FTUX.
        """
        from services.auth.auth_middleware import AuthMiddleware
        from services.auth.jwt_service import JWTService

        class MockApp:
            pass

        jwt_service = JWTService()
        middleware = AuthMiddleware(MockApp(), jwt_service)

        # Setup endpoints should be excluded
        assert middleware._should_exclude_path("/setup")
        assert middleware._should_exclude_path("/api/v1/setup")
        assert middleware._should_exclude_path("/api/v1/auth/login")


@pytest.fixture
async def full_app_client():
    """
    HTTP client that uses the REAL app with full startup lifecycle.

    This is a TRUE integration client - boots the real FastAPI app with all
    middleware, routes, services, and database connections exactly as
    they would be in production.
    """
    from contextlib import asynccontextmanager

    from web.app import app

    @asynccontextmanager
    async def lifespan_wrapper():
        async with app.router.lifespan_context(app):
            yield

    async with lifespan_wrapper():
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.fixture
async def integration_db_session():
    """
    Create database session for integration tests.
    Uses real database, commits changes, and cleans up.
    """
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker

    db_url = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"
    engine = create_async_engine(db_url, echo=False)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def test_user_no_projects(integration_db_session):
    """
    Create a test user with NO projects for onboarding testing.
    Returns (user_id, username, password) tuple.
    Cleans up after test.
    """
    from services.auth.password_service import PasswordService

    user_id = str(uuid4())
    username = f"integration_test_{user_id[:8]}"
    email = f"{username}@test.example.com"
    password = "testpass123"

    ps = PasswordService()
    password_hash = ps.hash_password(password)

    # Insert user
    await integration_db_session.execute(
        text(
            """
            INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                               created_at, updated_at, role, is_alpha)
            VALUES (:id, :username, :email, :password_hash, true, true, :now, :now, 'user', true)
        """
        ),
        {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "now": datetime.now(timezone.utc),
        },
    )
    await integration_db_session.commit()

    yield user_id, username, password

    # Cleanup — the app creates dependent rows (personalization_contexts etc.)
    # for the user mid-test; a bare users DELETE hits FK violations (#1452).
    from tests.conftest import delete_test_user_fully

    await delete_test_user_fully(integration_db_session, user_id)
    await integration_db_session.commit()


class TestHTTPIntentWiring:
    """
    Test the full HTTP -> Service -> Handler chain.

    These tests verify that HTTP requests actually reach the correct handlers
    without any mocking of internal methods.
    """

    async def test_intent_endpoint_returns_200(self, full_app_client):
        """
        Issue #559: Verify intent endpoint is reachable.
        """
        response = await full_app_client.post(
            "/api/v1/intent",
            json={"message": "Hello", "session_id": "test-session"},
        )

        # Should return 200 (even without auth - optional auth pattern)
        assert response.status_code == 200

    async def test_intent_response_structure(self, full_app_client):
        """
        Issue #559: Verify intent response has expected structure.
        """
        response = await full_app_client.post(
            "/api/v1/intent",
            json={"message": "Hello", "session_id": "test-session"},
        )

        assert response.status_code == 200
        result = response.json()

        # Response should have expected fields
        assert "message" in result
        assert "intent" in result

        # Message should not be empty
        assert len(result["message"]) > 0

    async def test_authenticated_request_has_user_context(
        self, full_app_client, test_user_no_projects
    ):
        """
        Issue #559: Verify authenticated requests pass user_id to service.

        This tests the middleware -> route -> service chain with real auth.
        """
        user_id, username, password = test_user_no_projects

        # Login to get auth cookie
        login_response = await full_app_client.post(
            "/api/v1/auth/login",
            data={"username": username, "password": password},
        )

        # Should be able to login
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"

        # Get cookies from login
        cookies = login_response.cookies

        # Make intent request with auth
        intent_response = await full_app_client.post(
            "/api/v1/intent",
            json={"message": "Hello there!", "session_id": f"test-{uuid4()}"},
            cookies=cookies,
        )

        assert intent_response.status_code == 200
        result = intent_response.json()

        # Should get a valid response (not an error)
        assert "message" in result
        # Message should not be empty
        assert len(result.get("message", "")) > 0


class TestOnboardingWiringIntegration:
    """
    Test onboarding wiring without mocking internal methods.

    These tests verify the REAL onboarding flow works.
    """

    async def test_onboarding_manager_session_lifecycle(self):
        """
        Issue #559: Verify onboarding manager can create/retrieve sessions.
        """
        from services.onboarding import PortfolioOnboardingManager

        manager = PortfolioOnboardingManager()
        session_id = f"test-session-{uuid4()}"
        user_id = str(uuid4())

        # Create session
        session = manager.create_session(session_id, user_id)
        assert session is not None
        assert session.session_id == session_id
        assert session.user_id == user_id

        # Retrieve by user
        retrieved = manager.get_session_by_user(user_id)
        assert retrieved is not None
        assert retrieved.id == session.id

        # Retrieve by session
        retrieved2 = manager.get_session_by_session_id(session_id)
        assert retrieved2 is not None
        assert retrieved2.id == session.id

    async def test_onboarding_handler_flow(self):
        """
        Issue #559: Verify onboarding handler can process full flow.
        """
        from services.onboarding import PortfolioOnboardingHandler, PortfolioOnboardingManager
        from services.shared_types import PortfolioOnboardingState

        manager = PortfolioOnboardingManager()
        handler = PortfolioOnboardingHandler(manager)

        session_id = f"test-session-{uuid4()}"
        user_id = str(uuid4())

        # Start onboarding
        response = handler.start_onboarding(session_id, user_id)
        assert response.state == PortfolioOnboardingState.INITIATED
        onboarding_id = response.metadata.get("onboarding_id")
        assert onboarding_id is not None

        # Handle acceptance
        response = handler.handle_turn(onboarding_id, "Yes please!")
        assert response.state == PortfolioOnboardingState.GATHERING_PROJECTS

        # Handle project info
        response = handler.handle_turn(onboarding_id, "I'm building TestApp")
        assert "testapp" in response.message.lower()

        # Handle done
        response = handler.handle_turn(onboarding_id, "That's all")
        assert response.state == PortfolioOnboardingState.CONFIRMING

        # Handle confirmation — flow now proceeds to the optional repo-linking step (#863)
        # before completing, instead of going straight to COMPLETE.
        response = handler.handle_turn(onboarding_id, "Yes save them")
        assert response.state == PortfolioOnboardingState.GATHERING_REPOS

        # Link a GitHub repo to the (single) project — exercises the #863 repo-linking
        # step end-to-end, then completes onboarding.
        response = handler.handle_turn(onboarding_id, "mediajunkie/testapp")
        assert response.state == PortfolioOnboardingState.COMPLETE
        assert response.is_complete is True
        # The linked repo was captured on the project.
        assert response.captured_projects[0]["repo"] == "mediajunkie/testapp"

    async def test_singleton_manager_consistency(self):
        """
        Issue #559: Verify _get_onboarding_components returns singleton.

        Bug: Creating new PortfolioOnboardingManager() loses session state.
        Fix: Use _get_onboarding_components() which returns singleton.
        """
        from services.conversation.conversation_handler import _get_onboarding_components

        # Get components twice
        manager1, handler1 = _get_onboarding_components()
        manager2, handler2 = _get_onboarding_components()

        # Should be the SAME objects (singleton)
        assert manager1 is manager2
        assert handler1 is handler2

        # Create session through manager1
        session_id = f"singleton-test-{uuid4()}"
        user_id = str(uuid4())
        session = manager1.create_session(session_id, user_id)

        # Should be retrievable through manager2 (same manager)
        retrieved = manager2.get_session_by_user(user_id)
        assert retrieved is not None
        assert retrieved.id == session.id


class TestIntentServiceOnboardingIntegration:
    """
    Test IntentService onboarding integration without mocking.
    """

    async def test_check_active_onboarding_no_session(self):
        """
        Issue #559: Verify _check_active_onboarding returns None when no session.
        """
        from services.intent.intent_service import IntentService

        service = IntentService()

        # With no active session, should return None
        result = await service._check_active_onboarding(
            user_id=str(uuid4()),
            session_id=f"test-{uuid4()}",
            message="Hello",
        )

        assert result is None

    async def test_check_active_onboarding_with_session(self):
        """
        Issue #559: Verify _check_active_onboarding routes to active session.
        """
        from services.conversation.conversation_handler import _get_onboarding_components
        from services.intent.intent_service import IntentService
        from services.shared_types import PortfolioOnboardingState

        # Create an active onboarding session
        manager, handler = _get_onboarding_components()
        session_id = f"test-{uuid4()}"
        user_id = str(uuid4())

        # Start onboarding (creates session in INITIATED state)
        response = handler.start_onboarding(session_id, user_id)
        assert response.state == PortfolioOnboardingState.INITIATED

        # Transition to GATHERING (active state)
        handler.handle_turn(response.metadata["onboarding_id"], "Yes!")

        # Now IntentService should detect the active session
        service = IntentService()
        result = await service._check_active_onboarding(
            user_id=user_id,
            session_id=session_id,
            message="I'm working on TestProject",
        )

        # Should return an IntentProcessingResult (not None)
        assert result is not None
        assert result.success is True
        assert result.intent_data["action"] == "portfolio_onboarding"
        assert result.intent_data["context"]["bypassed_classification"] is True
