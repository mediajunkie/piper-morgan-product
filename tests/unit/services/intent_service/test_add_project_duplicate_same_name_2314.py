"""#2314 (PA, served on 06c71d53e2): "add project zz link test" was refused as a duplicate
of "zz share-hide project". The guard used the lookup's prefix/substring tier; a duplicate
is now only the SAME name, exact or #1857-normalized (CXO's #2297 rule)."""

import contextlib
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers


@contextlib.asynccontextmanager
async def _scope():
    yield MagicMock()


async def _create_with_existing(name, existing_name):
    existing = SimpleNamespace(id="p-old", name=existing_name) if existing_name else None
    created = SimpleNamespace(id="p-new", name=name, description=None)
    create = AsyncMock(return_value=created)
    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            new=staticmethod(_scope),
        ),
        patch(
            "services.database.repositories.ProjectRepository.find_by_name",
            new=AsyncMock(return_value=existing),
        ),
        patch("services.database.repositories.ProjectRepository.create", new=create),
    ):
        result = await CanonicalHandlers()._create_or_report_project(name, None, "s-2314", "u-2314")
    return result, create


@pytest.mark.asyncio
async def test_a_prefix_match_is_not_a_duplicate():
    """The lookup's prefix tier returned another project: create the named one."""
    result, create = await _create_with_existing("zz", "zz share-hide project")
    assert "already have" not in result["message"]
    create.assert_awaited_once()


@pytest.mark.asyncio
async def test_the_same_normalized_name_is_a_duplicate():
    result, create = await _create_with_existing("the One Job project", "One Job")
    assert result["message"].startswith("You already have a project called One Job")
    create.assert_not_awaited()


@pytest.mark.asyncio
async def test_the_same_name_in_another_case_is_a_duplicate():
    result, create = await _create_with_existing("harbor pilot", "Harbor Pilot")
    assert result["message"].startswith("You already have a project called Harbor Pilot")
    create.assert_not_awaited()
