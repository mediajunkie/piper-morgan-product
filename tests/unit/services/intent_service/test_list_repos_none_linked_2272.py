"""#2272 (CXO 11-06 15:58, on PA's served quote from 7ffd460640): a project with no
linked repository points at its project page, not at a chat phrase, while #2271's
link loop exists (a sibling phrasing declined served that day)."""

import contextlib
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory


@contextlib.asynccontextmanager
async def _scope():
    yield MagicMock()


@pytest.mark.asyncio
async def test_no_linked_repo_points_at_the_project_page():
    project = SimpleNamespace(id="p1", name="Mobile Redesign")
    intent = Intent(
        category=IntentCategory.PORTFOLIO,
        action="list_repos",
        confidence=0.9,
        context={"original_message": "show repos for Mobile Redesign"},
    )
    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            new=staticmethod(_scope),
        ),
        patch(
            "services.database.repositories.ProjectRepository.find_by_name",
            new=AsyncMock(return_value=project),
        ),
        patch(
            "services.database.repositories.RepositoryRepository.list_by_project",
            new=AsyncMock(return_value=[]),
        ),
    ):
        result = await CanonicalHandlers()._handle_list_repos(intent, "s-2272", user_id="u1")
    assert result["message"] == (
        "Mobile Redesign has no repository linked yet. You can link one on its project page."
    )
    assert "link owner/repo" not in result["message"]
