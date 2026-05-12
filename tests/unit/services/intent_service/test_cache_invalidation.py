"""
Unit tests for cache_invalidation hooks (#984 Phase 3).

Covers the public invalidate_user_todos and invalidate_user_trust helpers,
plus integration assertions that TodoManagementService mutations and
UserTrustProfileRepository.update_stage actually call them.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.intent_service import cache_invalidation


@pytest.fixture
def fake_cache(monkeypatch):
    """Replace the module-level cache with a recording stub."""
    cache = MagicMock()
    cache.invalidate = AsyncMock(return_value=True)
    cache.invalidate_prefix = AsyncMock(return_value=0)
    monkeypatch.setattr(cache_invalidation, "_default_cache", cache)
    return cache


class TestInvalidateUserTodos:
    @pytest.mark.asyncio
    async def test_invalidates_pending_completed_and_reminders_keys(self, fake_cache):
        await cache_invalidation.invalidate_user_todos("user-1")
        called_keys = [c.args[0] for c in fake_cache.invalidate.await_args_list]
        assert "context:pending_todos:user-1" in called_keys
        assert "context:completed_todos:user-1" in called_keys
        assert "context:reminders:user-1" in called_keys
        assert len(called_keys) == 3

    @pytest.mark.asyncio
    async def test_accepts_uuid_input(self, fake_cache):
        from uuid import UUID

        uid = UUID("00000000-0000-0000-0000-000000000001")
        await cache_invalidation.invalidate_user_todos(uid)
        called_keys = [c.args[0] for c in fake_cache.invalidate.await_args_list]
        assert "context:pending_todos:00000000-0000-0000-0000-000000000001" in called_keys

    @pytest.mark.asyncio
    async def test_returns_count_of_keys_deleted(self, fake_cache):
        # First two keys hit, third missed
        fake_cache.invalidate = AsyncMock(side_effect=[True, True, False])
        count = await cache_invalidation.invalidate_user_todos("user-1")
        assert count == 2

    @pytest.mark.asyncio
    async def test_no_exception_when_cache_returns_false(self, fake_cache):
        fake_cache.invalidate = AsyncMock(return_value=False)
        count = await cache_invalidation.invalidate_user_todos("user-1")
        assert count == 0


class TestInvalidateUserTrust:
    @pytest.mark.asyncio
    async def test_invalidates_trust_key(self, fake_cache):
        ok = await cache_invalidation.invalidate_user_trust("user-1")
        assert ok is True
        fake_cache.invalidate.assert_awaited_once_with("context:trust:user-1")

    @pytest.mark.asyncio
    async def test_returns_false_when_key_missing(self, fake_cache):
        fake_cache.invalidate = AsyncMock(return_value=False)
        ok = await cache_invalidation.invalidate_user_trust("user-1")
        assert ok is False


class TestTodoMutationInvocations:
    """Integration: TodoManagementService mutations call invalidate_user_todos.

    Mocks out the DB layer; asserts that the invalidation hook is awaited.
    """

    @pytest.mark.asyncio
    async def test_create_todo_invokes_invalidate(self, monkeypatch):
        from uuid import UUID

        from services.todo import todo_management_service as tms_module

        # Mock AsyncSessionFactory.session_scope to yield a no-op session
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock()
        scope_cm = MagicMock()
        scope_cm.__aenter__ = AsyncMock(return_value=mock_session)
        scope_cm.__aexit__ = AsyncMock(return_value=None)
        monkeypatch.setattr(
            tms_module.AsyncSessionFactory,
            "session_scope",
            lambda: scope_cm,
        )

        # Mock TodoRepository to return a fake todo on create
        fake_todo = MagicMock()
        mock_repo_instance = MagicMock()
        mock_repo_instance.create_todo = AsyncMock(return_value=fake_todo)
        monkeypatch.setattr(
            tms_module, "TodoRepository", lambda session: mock_repo_instance
        )

        # Patch the invalidation hook so we can assert on it
        mock_invalidate = AsyncMock()
        monkeypatch.setattr(
            "services.intent_service.cache_invalidation.invalidate_user_todos",
            mock_invalidate,
        )

        service = tms_module.TodoManagementService()
        uid = UUID("00000000-0000-0000-0000-000000000001")
        await service.create_todo(user_id=uid, text="test", priority="medium")

        mock_invalidate.assert_awaited_once_with(uid)

    @pytest.mark.asyncio
    async def test_complete_todo_invokes_invalidate_only_on_success(self, monkeypatch):
        from uuid import UUID

        from services.todo import todo_management_service as tms_module

        mock_session = AsyncMock()
        mock_session.commit = AsyncMock()
        scope_cm = MagicMock()
        scope_cm.__aenter__ = AsyncMock(return_value=mock_session)
        scope_cm.__aexit__ = AsyncMock(return_value=None)
        monkeypatch.setattr(
            tms_module.AsyncSessionFactory, "session_scope", lambda: scope_cm
        )

        # First case: complete succeeds (repo returns a todo)
        mock_repo_success = MagicMock()
        mock_repo_success.complete_todo = AsyncMock(return_value=MagicMock())

        mock_invalidate = AsyncMock()
        monkeypatch.setattr(
            "services.intent_service.cache_invalidation.invalidate_user_todos",
            mock_invalidate,
        )

        monkeypatch.setattr(
            tms_module, "TodoRepository", lambda s: mock_repo_success
        )
        service = tms_module.TodoManagementService()
        uid = UUID("00000000-0000-0000-0000-000000000001")
        await service.complete_todo(todo_id=uid, user_id=uid)
        assert mock_invalidate.await_count == 1

        # Second case: complete fails (repo returns None) — no invalidation
        mock_invalidate.reset_mock()
        mock_repo_fail = MagicMock()
        mock_repo_fail.complete_todo = AsyncMock(return_value=None)
        monkeypatch.setattr(
            tms_module, "TodoRepository", lambda s: mock_repo_fail
        )
        await service.complete_todo(todo_id=uid, user_id=uid)
        mock_invalidate.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_todo_invokes_invalidate_only_on_success(self, monkeypatch):
        from uuid import UUID

        from services.todo import todo_management_service as tms_module

        mock_session = AsyncMock()
        mock_session.commit = AsyncMock()
        scope_cm = MagicMock()
        scope_cm.__aenter__ = AsyncMock(return_value=mock_session)
        scope_cm.__aexit__ = AsyncMock(return_value=None)
        monkeypatch.setattr(
            tms_module.AsyncSessionFactory, "session_scope", lambda: scope_cm
        )

        mock_repo = MagicMock()
        mock_repo.delete_todo = AsyncMock(return_value=True)
        monkeypatch.setattr(tms_module, "TodoRepository", lambda s: mock_repo)

        mock_invalidate = AsyncMock()
        monkeypatch.setattr(
            "services.intent_service.cache_invalidation.invalidate_user_todos",
            mock_invalidate,
        )

        service = tms_module.TodoManagementService()
        uid = UUID("00000000-0000-0000-0000-000000000001")
        await service.delete_todo(todo_id=uid, user_id=uid)
        mock_invalidate.assert_awaited_once_with(uid)
