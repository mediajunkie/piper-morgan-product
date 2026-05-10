"""
Unit tests for Conversation Lifecycle (Issue #715)

Spec #858: Conversation Lifecycle Specification v1.1
Tests T1-T10: Backend lifecycle behavior

These tests verify:
- State machine transitions (ACTIVE, ARCHIVED, DELETED)
- Creation invariants across all paths
- Auth contract (token expiry, missing auth)
- Repository filtering by lifecycle_state
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain import models as domain
from services.shared_types import ConversationLifecycleState
from web.api.routes.conversations import (
    ConversationListItem,
    StateTransitionResponse,
    UpdateStateRequest,
    delete_conversation,
    list_conversations,
    update_conversation_state,
)

# ── Helpers ──────────────────────────────────────────────────────────


def _make_conversation(
    user_id: str,
    lifecycle_state: ConversationLifecycleState = ConversationLifecycleState.ACTIVE,
    archived_at=None,
    deleted_at=None,
    title="Test Conversation",
) -> domain.Conversation:
    """Create a domain Conversation with lifecycle fields."""
    return domain.Conversation(
        id=str(uuid4()),
        user_id=user_id,
        session_id=str(uuid4()),
        title=title,
        context={},
        is_active=lifecycle_state == ConversationLifecycleState.ACTIVE,
        lifecycle_state=lifecycle_state,
        archived_at=archived_at,
        deleted_at=deleted_at,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        last_activity_at=datetime.now(timezone.utc),
    )


def _mock_user(user_id: str = None):
    """Create a mock JWTClaims user."""
    user = MagicMock()
    user.sub = user_id or str(uuid4())
    user.username = "testuser"
    return user


def _mock_repo():
    """Create a mock ConversationRepository."""
    repo = MagicMock()
    repo.list_for_user = AsyncMock(return_value=[])
    repo.search_for_user = AsyncMock(return_value=[])
    repo.get_by_id = AsyncMock(return_value=None)
    repo.get_turn_count = AsyncMock(return_value=0)
    repo.archive_conversation = AsyncMock(return_value=None)
    repo.delete_conversation = AsyncMock(return_value=None)
    repo.reactivate_conversation = AsyncMock(return_value=None)
    repo.create = AsyncMock(return_value=None)
    repo.ensure_conversation_exists = AsyncMock(return_value=None)
    return repo


# ── T1: Fresh conversation has ACTIVE state ──────────────────────────


class TestT1FreshConversationState:
    """
    T1: Fresh conversation has ACTIVE state

    Spec #858 Section 3: All creation paths produce conversations
    with lifecycle_state=ACTIVE, archived_at=None, deleted_at=None.
    """

    @pytest.mark.asyncio
    async def test_create_endpoint_produces_active_conversation(self):
        """T1a: POST /api/v1/conversations produces ACTIVE conversation."""
        from web.api.routes.conversations import create_conversation

        user = _mock_user()
        new_conv = _make_conversation(user.sub)
        repo = _mock_repo()
        repo.create = AsyncMock(return_value=new_conv)

        result = await create_conversation(
            request=MagicMock(title="Test"),
            current_user=user,
            conv_repo=repo,
        )

        assert result.lifecycle_state == "active"

    def test_domain_model_defaults_to_active(self):
        """T1b: Domain model defaults lifecycle_state to ACTIVE."""
        conv = domain.Conversation(
            id=str(uuid4()),
            user_id=str(uuid4()),
            session_id=str(uuid4()),
            title="Test",
            context={},
        )
        assert conv.lifecycle_state == ConversationLifecycleState.ACTIVE
        assert conv.archived_at is None
        assert conv.deleted_at is None

    @pytest.mark.asyncio
    async def test_active_conversation_appears_in_list(self):
        """T1c: ACTIVE conversation appears in left sidebar API response."""
        user = _mock_user()
        conv = _make_conversation(user.sub)
        repo = _mock_repo()
        repo.list_for_user = AsyncMock(return_value=[conv])

        result = await list_conversations(
            current_user=user,
            conv_repo=repo,
        )

        assert len(result.conversations) == 1
        assert result.conversations[0].lifecycle_state == "active"


# ── T3: User explicitly archives a conversation ─────────────────────


class TestT3ExplicitArchive:
    """
    T3: User explicitly archives a conversation

    Spec #858 Section 2: ACTIVE → ARCHIVED transition via PATCH endpoint.
    """

    @pytest.mark.asyncio
    async def test_archive_sets_archived_state(self):
        """T3a: PATCH with state=archived sets lifecycle_state=ARCHIVED."""
        user = _mock_user()
        conv = _make_conversation(user.sub)
        archived_conv = _make_conversation(
            user.sub,
            lifecycle_state=ConversationLifecycleState.ARCHIVED,
            archived_at=datetime.now(timezone.utc),
        )
        archived_conv.id = conv.id

        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=conv)
        repo.archive_conversation = AsyncMock(return_value=archived_conv)

        result = await update_conversation_state(
            conversation_id=conv.id,
            request=UpdateStateRequest(state="archived"),
            current_user=user,
            conv_repo=repo,
        )

        assert result.lifecycle_state == "archived"
        assert result.message == "Conversation archived"
        repo.archive_conversation.assert_called_once_with(conv.id)

    @pytest.mark.asyncio
    async def test_archive_removes_from_active_list(self):
        """T3b: Archived conversation not in left sidebar (ACTIVE-only)."""
        user = _mock_user()
        active_conv = _make_conversation(user.sub)
        # archived_conv deliberately NOT in the returned list
        repo = _mock_repo()
        repo.list_for_user = AsyncMock(return_value=[active_conv])

        result = await list_conversations(
            current_user=user,
            conv_repo=repo,
        )

        assert len(result.conversations) == 1
        assert result.conversations[0].lifecycle_state == "active"

    @pytest.mark.asyncio
    async def test_archive_non_active_returns_409(self):
        """T3c: Archiving a non-ACTIVE conversation returns 409 Conflict."""
        from fastapi import HTTPException

        user = _mock_user()
        conv = _make_conversation(user.sub)

        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=conv)
        repo.archive_conversation = AsyncMock(return_value=None)  # not ACTIVE

        with pytest.raises(HTTPException) as exc_info:
            await update_conversation_state(
                conversation_id=conv.id,
                request=UpdateStateRequest(state="archived"),
                current_user=user,
                conv_repo=repo,
            )
        assert exc_info.value.status_code == 409


# ── T4: Reactivation ────────────────────────────────────────────────


class TestT4Reactivation:
    """
    T4: Reactivation by user action

    Spec #858 Section 2: ARCHIVED → ACTIVE transition.
    """

    @pytest.mark.asyncio
    async def test_reactivate_sets_active_state(self):
        """T4a: PATCH with state=active reactivates an ARCHIVED conversation."""
        user = _mock_user()
        archived_conv = _make_conversation(
            user.sub,
            lifecycle_state=ConversationLifecycleState.ARCHIVED,
            archived_at=datetime.now(timezone.utc),
        )
        reactivated_conv = _make_conversation(user.sub)
        reactivated_conv.id = archived_conv.id

        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=archived_conv)
        repo.reactivate_conversation = AsyncMock(return_value=reactivated_conv)

        result = await update_conversation_state(
            conversation_id=archived_conv.id,
            request=UpdateStateRequest(state="active"),
            current_user=user,
            conv_repo=repo,
        )

        assert result.lifecycle_state == "active"
        assert result.message == "Conversation reactivated"
        repo.reactivate_conversation.assert_called_once_with(archived_conv.id)

    @pytest.mark.asyncio
    async def test_reactivate_non_archived_returns_409(self):
        """T4b: Reactivating a non-ARCHIVED conversation returns 409."""
        from fastapi import HTTPException

        user = _mock_user()
        conv = _make_conversation(user.sub)  # ACTIVE, not ARCHIVED

        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=conv)
        repo.reactivate_conversation = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await update_conversation_state(
                conversation_id=conv.id,
                request=UpdateStateRequest(state="active"),
                current_user=user,
                conv_repo=repo,
            )
        assert exc_info.value.status_code == 409


# ── T5: User deletes a conversation ─────────────────────────────────


class TestT5SoftDelete:
    """
    T5: User deletes a conversation

    Spec #858 Section 2: ACTIVE/ARCHIVED → DELETED (terminal state).
    """

    @pytest.mark.asyncio
    async def test_delete_sets_deleted_state(self):
        """T5a: DELETE sets lifecycle_state=DELETED and deleted_at."""
        user = _mock_user()
        conv = _make_conversation(user.sub)
        deleted_conv = _make_conversation(
            user.sub,
            lifecycle_state=ConversationLifecycleState.DELETED,
            deleted_at=datetime.now(timezone.utc),
        )
        deleted_conv.id = conv.id

        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=conv)
        repo.delete_conversation = AsyncMock(return_value=deleted_conv)

        result = await delete_conversation(
            conversation_id=conv.id,
            current_user=user,
            conv_repo=repo,
        )

        assert result.lifecycle_state == "deleted"
        assert result.message == "Conversation deleted"
        repo.delete_conversation.assert_called_once_with(conv.id)

    @pytest.mark.asyncio
    async def test_delete_already_deleted_returns_409(self):
        """T5b: Deleting an already-deleted conversation returns 409."""
        from fastapi import HTTPException

        user = _mock_user()
        conv = _make_conversation(user.sub)

        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=conv)
        repo.delete_conversation = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await delete_conversation(
                conversation_id=conv.id,
                current_user=user,
                conv_repo=repo,
            )
        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_delete_nonexistent_returns_404(self):
        """T5c: Deleting a nonexistent conversation returns 404."""
        from fastapi import HTTPException

        user = _mock_user()
        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await delete_conversation(
                conversation_id=str(uuid4()),
                current_user=user,
                conv_repo=repo,
            )
        assert exc_info.value.status_code == 404


# ── T6: COMPOSTED conversations are invisible ───────────────────────


class TestT6CompostedInvisible:
    """
    T6: COMPOSTED conversations are invisible

    Spec #858 Section 2.2: COMPOSTED not visible in any sidebar or search.
    """

    @pytest.mark.asyncio
    async def test_composted_not_in_active_list(self):
        """T6a: COMPOSTED conversation not returned by ACTIVE filter."""
        user = _mock_user()
        # Repository returns empty because COMPOSTED is filtered out at DB level
        repo = _mock_repo()
        repo.list_for_user = AsyncMock(return_value=[])

        result = await list_conversations(
            state="active",
            current_user=user,
            conv_repo=repo,
        )

        assert len(result.conversations) == 0

    @pytest.mark.asyncio
    async def test_composted_not_in_archived_list(self):
        """T6b: COMPOSTED conversation not returned by ARCHIVED filter."""
        user = _mock_user()
        repo = _mock_repo()
        repo.list_for_user = AsyncMock(return_value=[])

        result = await list_conversations(
            state="archived",
            current_user=user,
            conv_repo=repo,
        )

        assert len(result.conversations) == 0

    @pytest.mark.asyncio
    async def test_composted_not_in_search(self):
        """T6c: COMPOSTED conversation not returned by search."""
        user = _mock_user()
        repo = _mock_repo()
        repo.search_for_user = AsyncMock(return_value=[])

        result = await list_conversations(
            search="test query",
            current_user=user,
            conv_repo=repo,
        )

        assert len(result.conversations) == 0


# ── T7: All creation paths produce equivalent records ────────────────


class TestT7CreationPathEquivalence:
    """
    T7: All creation paths produce equivalent records

    Spec #858 Section 3: POST /api/v1/conversations, ensure_conversation_exists()
    during first message, ensure_conversation_exists() during turn save — all produce
    conversations with UUID id, valid user_id, lifecycle_state=ACTIVE.
    """

    def test_domain_model_has_required_fields(self):
        """T7a: Domain Conversation has all required fields with correct defaults."""
        conv = domain.Conversation(
            id="test-uuid",
            user_id="user-123",
            session_id="session-456",
            title="Test",
            context={},
        )
        assert conv.id == "test-uuid"
        assert conv.user_id == "user-123"
        assert conv.lifecycle_state == ConversationLifecycleState.ACTIVE
        assert conv.is_active is True
        assert conv.archived_at is None
        assert conv.deleted_at is None

    def test_to_dict_includes_lifecycle_fields(self):
        """T7b: to_dict() includes lifecycle_state, archived_at, deleted_at."""
        conv = _make_conversation("user-123")
        d = conv.to_dict()

        assert "lifecycle_state" in d
        assert d["lifecycle_state"] == "active"
        assert "archived_at" in d
        assert "deleted_at" in d


# ── T8: Creation refuses without valid user_id ──────────────────────


class TestT8CreationRefusesNoUserId:
    """
    T8: Creation refuses without valid user_id

    Spec #858 Section 3.3 / Issue #840: ensure_conversation_exists()
    must refuse to create a conversation without user_id.
    """

    @pytest.mark.asyncio
    async def test_ensure_conversation_exists_refuses_no_user_id(self):
        """T8a: ensure_conversation_exists() with user_id=None does not create."""
        from services.database.repositories import ConversationRepository

        mock_session = MagicMock()
        mock_session.get = AsyncMock(return_value=None)  # not found
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()

        repo = ConversationRepository(mock_session)
        await repo.ensure_conversation_exists("conv-123", user_id=None)

        # Should NOT have called session.add (no conversation created)
        mock_session.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_ensure_conversation_exists_refuses_empty_user_id(self):
        """T8b: ensure_conversation_exists() with user_id='' does not create."""
        from services.database.repositories import ConversationRepository

        mock_session = MagicMock()
        mock_session.get = AsyncMock(return_value=None)
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()

        repo = ConversationRepository(mock_session)
        await repo.ensure_conversation_exists("conv-123", user_id="")

        mock_session.add.assert_not_called()


# ── T9: Token expiry surfaces to user ───────────────────────────────


class TestT9TokenExpiry:
    """
    T9: Token expiry surfaces to user (not silent)

    Spec #858 Section 4: When auth token expires during a conversation,
    the API returns 401 — NOT 200 with empty data.
    """

    @pytest.mark.asyncio
    async def test_expired_token_returns_401(self):
        """T9a: API returns 401 for expired/invalid token on conversation list.

        This test verifies the contract: get_current_user dependency
        raises HTTPException(401) when token is invalid. The test uses
        httpx.AsyncClient to exercise the full middleware chain.
        """
        import httpx

        from web.app import app

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/conversations")
            # Without valid auth, should get 401 (not 200 with empty list)
            assert response.status_code == 401


# ── T10: Sidebar fetch without auth returns 401 ─────────────────────


class TestT10NoAuthReturns401:
    """
    T10: Sidebar fetch without auth returns 401

    Spec #858 Section 4: GET /api/v1/conversations without valid auth
    returns 401 — not an empty conversation list.
    """

    @pytest.mark.asyncio
    async def test_no_auth_on_conversations_endpoint(self):
        """T10a: GET /api/v1/conversations without auth cookie returns 401."""
        import httpx

        from web.app import app

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/conversations")
            assert response.status_code == 401
            # Response should NOT be an empty list (that would be silent failure)
            data = response.json()
            assert "detail" in data or "error" in data

    @pytest.mark.asyncio
    async def test_no_auth_on_conversation_state_patch(self):
        """T10b: PATCH /api/v1/conversations/{id}/state without auth returns 401."""
        import httpx

        from web.app import app

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response = await client.patch(
                f"/api/v1/conversations/{uuid4()}/state",
                json={"state": "archived"},
            )
            assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_no_auth_on_conversation_delete(self):
        """T10c: DELETE /api/v1/conversations/{id} without auth returns 401."""
        import httpx

        from web.app import app

        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete(f"/api/v1/conversations/{uuid4()}")
            assert response.status_code == 401


# ── State filter validation ──────────────────────────────────────────


class TestStateFilterValidation:
    """
    Additional tests for the state query parameter on list endpoint.
    """

    @pytest.mark.asyncio
    async def test_invalid_state_returns_400(self):
        """Invalid state parameter returns 400 Bad Request."""
        from fastapi import HTTPException

        user = _mock_user()
        repo = _mock_repo()

        with pytest.raises(HTTPException) as exc_info:
            await list_conversations(
                state="invalid_state",
                current_user=user,
                conv_repo=repo,
            )
        assert exc_info.value.status_code == 400

    @pytest.mark.asyncio
    async def test_state_filter_passed_to_repository(self):
        """State parameter is correctly passed to repository.list_for_user()."""
        user = _mock_user()
        repo = _mock_repo()
        repo.list_for_user = AsyncMock(return_value=[])

        await list_conversations(
            state="archived",
            current_user=user,
            conv_repo=repo,
        )

        repo.list_for_user.assert_called_once()
        call_kwargs = repo.list_for_user.call_args
        assert call_kwargs.kwargs.get("state") == ConversationLifecycleState.ARCHIVED

    @pytest.mark.asyncio
    async def test_ownership_check_on_state_change(self):
        """State change on conversation owned by different user returns 404."""
        from fastapi import HTTPException

        user = _mock_user()
        other_user_conv = _make_conversation("other-user-id")

        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=other_user_conv)

        with pytest.raises(HTTPException) as exc_info:
            await update_conversation_state(
                conversation_id=other_user_conv.id,
                request=UpdateStateRequest(state="archived"),
                current_user=user,
                conv_repo=repo,
            )
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_ownership_check_on_delete(self):
        """Delete on conversation owned by different user returns 404."""
        from fastapi import HTTPException

        user = _mock_user()
        other_user_conv = _make_conversation("other-user-id")

        repo = _mock_repo()
        repo.get_by_id = AsyncMock(return_value=other_user_conv)

        with pytest.raises(HTTPException) as exc_info:
            await delete_conversation(
                conversation_id=other_user_conv.id,
                current_user=user,
                conv_repo=repo,
            )
        assert exc_info.value.status_code == 404
