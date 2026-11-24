"""
Unit tests for list item endpoints (Issue #474: MUX-TECH-LISTS)

Tests for:
- POST /api/v1/lists/{list_id}/items - Add item to list
- GET /api/v1/lists/{list_id}/items - Get items in list
- PUT /api/v1/lists/{list_id}/items/{item_id} - Update item
- DELETE /api/v1/lists/{list_id}/items/{item_id} - Delete item
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTClaims


class TestListItemEndpoints:
    """Test list item CRUD endpoints"""

    @pytest.fixture
    def mock_current_user(self):
        """Create mock authenticated user"""
        return JWTClaims(
            iss="piper-morgan",
            aud="piper-morgan-api",
            sub="test-user-id-123",
            exp=9999999999,
            iat=1234567890,
            jti="test-jti-123",
            user_id=UUID("00000000-0000-0000-0000-000000000001"),
            user_email="test@example.com",
            username="test",  # Issue #730
            scopes=["read", "write"],
            token_type="access",
        )

    @pytest.fixture
    def mock_list_repository(self):
        """Create mock list repository"""
        mock_repo = MagicMock()
        mock_repo.get_list_by_id = AsyncMock()
        return mock_repo

    @pytest.fixture
    def mock_list(self):
        """Create mock list object"""
        mock = MagicMock()
        mock.id = "test-list-id"
        mock.name = "Test List"
        mock.owner_id = "test-user-id-123"
        return mock

    @pytest.fixture
    def mock_item_db(self):
        """Create mock ItemDB object"""
        mock = MagicMock()
        mock.id = "test-item-id"
        mock.text = "Test Item"
        mock.position = 0
        mock.list_id = "test-list-id"
        mock.created_at = datetime(2026, 1, 22, 12, 0, 0)
        mock.updated_at = datetime(2026, 1, 22, 12, 0, 0)
        return mock

    @pytest.mark.asyncio
    async def test_add_item_to_list_success(
        self, mock_current_user, mock_list_repository, mock_list, mock_item_db
    ):
        """POST /lists/{id}/items creates item successfully"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        # Mock list ownership check returns the list
        mock_list_repository.get_list_by_id.return_value = mock_list

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        # Mock the database session
        with patch(
            "web.api.routes.lists.AsyncSessionFactory.session_scope_fresh"
        ) as mock_session_factory:
            mock_session = AsyncMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session_factory.return_value = mock_session

            # Mock select query for max position
            mock_result = MagicMock()
            mock_result.scalar.return_value = -1  # No existing items
            mock_session.execute = AsyncMock(return_value=mock_result)
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()

            # Mock refresh to populate item
            async def mock_refresh(item):
                item.id = "new-item-id"
                item.created_at = datetime(2026, 1, 22, 12, 0, 0)
                item.updated_at = datetime(2026, 1, 22, 12, 0, 0)

            mock_session.refresh = mock_refresh

            client = TestClient(app)
            response = client.post(
                "/api/v1/lists/test-list-id/items",
                json={"text": "New Item"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["text"] == "New Item"
            assert data["position"] == 0
            assert data["list_id"] == "test-list-id"

    @pytest.mark.asyncio
    async def test_add_item_to_nonexistent_list(self, mock_current_user, mock_list_repository):
        """POST /lists/{id}/items returns 404 for nonexistent list"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        # List not found
        mock_list_repository.get_list_by_id.return_value = None

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        client = TestClient(app)
        response = client.post(
            "/api/v1/lists/nonexistent-list/items",
            json={"text": "New Item"},
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_add_item_empty_text_rejected(self, mock_current_user, mock_list_repository):
        """POST /lists/{id}/items rejects empty text"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        client = TestClient(app)
        response = client.post(
            "/api/v1/lists/test-list-id/items",
            json={"text": ""},
        )

        assert response.status_code == 400
        # Issue 2432 (CXO): reworded and marked.
        assert response.json()["detail"] == "Write the item first."

    @pytest.mark.asyncio
    async def test_get_items_in_list_success(
        self, mock_current_user, mock_list_repository, mock_list, mock_item_db
    ):
        """GET /lists/{id}/items returns items"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        mock_list_repository.get_list_by_id.return_value = mock_list

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        with patch(
            "web.api.routes.lists.AsyncSessionFactory.session_scope_fresh"
        ) as mock_session_factory:
            mock_session = AsyncMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session_factory.return_value = mock_session

            # Mock select query for items
            mock_result = MagicMock()
            mock_scalars = MagicMock()
            mock_scalars.all.return_value = [mock_item_db]
            mock_result.scalars.return_value = mock_scalars
            mock_session.execute = AsyncMock(return_value=mock_result)

            client = TestClient(app)
            response = client.get("/api/v1/lists/test-list-id/items")

            assert response.status_code == 200
            data = response.json()
            assert data["count"] == 1
            assert len(data["items"]) == 1
            assert data["items"][0]["text"] == "Test Item"

    @pytest.mark.asyncio
    async def test_get_items_nonexistent_list(self, mock_current_user, mock_list_repository):
        """GET /lists/{id}/items returns 404 for nonexistent list"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        mock_list_repository.get_list_by_id.return_value = None

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        client = TestClient(app)
        response = client.get("/api/v1/lists/nonexistent-list/items")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_item_success(
        self, mock_current_user, mock_list_repository, mock_list, mock_item_db
    ):
        """PUT /lists/{id}/items/{item_id} updates item"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        mock_list_repository.get_list_by_id.return_value = mock_list

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        with patch(
            "web.api.routes.lists.AsyncSessionFactory.session_scope_fresh"
        ) as mock_session_factory:
            mock_session = AsyncMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session_factory.return_value = mock_session

            # Mock select query for item
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = mock_item_db
            mock_session.execute = AsyncMock(return_value=mock_result)
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()

            client = TestClient(app)
            response = client.put(
                "/api/v1/lists/test-list-id/items/test-item-id",
                json={"text": "Updated Item"},
            )

            assert response.status_code == 200
            # The mock item text would be updated
            assert mock_item_db.text == "Updated Item"

    @pytest.mark.asyncio
    async def test_update_nonexistent_item(
        self, mock_current_user, mock_list_repository, mock_list
    ):
        """PUT /lists/{id}/items/{item_id} returns 404 for nonexistent item"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        mock_list_repository.get_list_by_id.return_value = mock_list

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        with patch(
            "web.api.routes.lists.AsyncSessionFactory.session_scope_fresh"
        ) as mock_session_factory:
            mock_session = AsyncMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session_factory.return_value = mock_session

            # Item not found
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = None
            mock_session.execute = AsyncMock(return_value=mock_result)

            client = TestClient(app)
            response = client.put(
                "/api/v1/lists/test-list-id/items/nonexistent-item",
                json={"text": "Updated"},
            )

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_item_success(
        self, mock_current_user, mock_list_repository, mock_list, mock_item_db
    ):
        """DELETE /lists/{id}/items/{item_id} removes item"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        mock_list_repository.get_list_by_id.return_value = mock_list

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        with patch(
            "web.api.routes.lists.AsyncSessionFactory.session_scope_fresh"
        ) as mock_session_factory:
            mock_session = AsyncMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session_factory.return_value = mock_session

            # Mock select query for item
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = mock_item_db
            mock_session.execute = AsyncMock(return_value=mock_result)
            mock_session.delete = AsyncMock()
            mock_session.commit = AsyncMock()

            client = TestClient(app)
            response = client.delete("/api/v1/lists/test-list-id/items/test-item-id")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "deleted"
            assert data["item_id"] == "test-item-id"

    @pytest.mark.asyncio
    async def test_delete_nonexistent_item(
        self, mock_current_user, mock_list_repository, mock_list
    ):
        """DELETE /lists/{id}/items/{item_id} returns 404 for nonexistent item"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        mock_list_repository.get_list_by_id.return_value = mock_list

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        with patch(
            "web.api.routes.lists.AsyncSessionFactory.session_scope_fresh"
        ) as mock_session_factory:
            mock_session = AsyncMock()
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=None)
            mock_session_factory.return_value = mock_session

            # Item not found
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = None
            mock_session.execute = AsyncMock(return_value=mock_result)

            client = TestClient(app)
            response = client.delete("/api/v1/lists/test-list-id/items/nonexistent-item")

            assert response.status_code == 404


class TestItemOwnershipValidation:
    """Test that item operations respect list ownership"""

    @pytest.fixture
    def mock_current_user(self):
        """Create mock authenticated user"""
        return JWTClaims(
            iss="piper-morgan",
            aud="piper-morgan-api",
            sub="user-a-id",
            exp=9999999999,
            iat=1234567890,
            jti="test-jti-456",
            user_id=UUID("00000000-0000-0000-0000-000000000002"),
            user_email="usera@example.com",
            username="usera",  # Issue #730
            scopes=["read", "write"],
            token_type="access",
        )

    @pytest.fixture
    def mock_list_repository(self):
        """Create mock list repository"""
        mock_repo = MagicMock()
        mock_repo.get_list_by_id = AsyncMock()
        return mock_repo

    @pytest.mark.asyncio
    async def test_cannot_add_item_to_others_list(self, mock_current_user, mock_list_repository):
        """Cannot add items to lists owned by other users"""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_list_repository
        from web.api.routes.lists import router

        # get_list_by_id with owner_id filter returns None (not owned)
        mock_list_repository.get_list_by_id.return_value = None

        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_list_repository] = lambda: mock_list_repository

        client = TestClient(app)
        response = client.post(
            "/api/v1/lists/other-users-list/items",
            json={"text": "Trying to add to others list"},
        )

        assert response.status_code == 404
        # Ownership validation happens via get_list_by_id(owner_id=current_user.sub)
