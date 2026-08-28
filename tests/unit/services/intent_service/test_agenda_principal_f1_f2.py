"""Principal-audit F1/F2 (2026-08-08): the agenda query read todos with
owner_id=session_id (sessions never own todos → Tasks structurally empty for
every authenticated user) and read user context session-only (priorities always
generic). Pins: the authenticated principal reaches both reads; anonymous gets
honest emptiness, never a session-keyed query.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers


class TestAgendaPrincipalThreading:
    @pytest.mark.asyncio
    async def test_todos_queried_by_user_id_never_session(self):
        uid = str(uuid4())
        repo = MagicMock()
        repo.get_todos_by_owner = AsyncMock(return_value=[])
        scope = MagicMock()
        scope.__aenter__ = AsyncMock(return_value=MagicMock())
        scope.__aexit__ = AsyncMock(return_value=False)
        with (
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope",
                return_value=scope,
            ),
            patch("services.repositories.todo_repository.TodoRepository", return_value=repo),
        ):
            await CanonicalHandlers()._get_todays_todos(user_id=uid)
        assert repo.get_todos_by_owner.await_args.kwargs["owner_id"] == uid

    @pytest.mark.asyncio
    async def test_anonymous_gets_empty_without_query(self):
        """No principal → no todos exist for you; must NOT fall back to a
        session-keyed query (the F1 bug shape)."""
        with patch("services.repositories.todo_repository.TodoRepository") as repo_cls:
            out = await CanonicalHandlers()._get_todays_todos(user_id=None)
        assert out == []
        repo_cls.assert_not_called()
