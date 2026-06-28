"""#313 tags MVP: PUT /{id}/tags (files via file_metadata.tags, artifacts via
payload.tags — no migration) + normalization. Owner-only."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes import files as files_route
from web.api.routes.files import _normalize_tags, set_file_tags


def _req(user_id="u1", is_admin=False):
    return SimpleNamespace(state=SimpleNamespace(user_id=user_id, is_admin=is_admin))


def _ctx(row):
    session = MagicMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = row
    session.execute = AsyncMock(return_value=result)
    session.commit = AsyncMock()
    factory = MagicMock()
    factory.session_scope_fresh.return_value.__aenter__ = AsyncMock(return_value=session)
    factory.session_scope_fresh.return_value.__aexit__ = AsyncMock(return_value=None)
    return factory, session


class TestNormalizeTags:
    def test_lowercases_dedupes_caps(self):
        assert _normalize_tags(["Research", "research ", "Q3"]) == ["research", "q3"]

    def test_caps_at_10_and_30_chars(self):
        tags = _normalize_tags([f"tag{i}" for i in range(20)] + ["x" * 50])
        assert len(tags) == 10
        assert all(len(t) <= 30 for t in tags)

    def test_non_list_is_empty(self):
        assert _normalize_tags("nope") == []


@pytest.mark.asyncio
async def test_sets_tags_on_owned_file():
    row = SimpleNamespace(id="f1", owner_id="u1", file_metadata={})
    factory, session = _ctx(row)
    with (
        patch.object(files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())),
        patch.object(files_route, "AsyncSessionFactory", factory),
    ):
        resp = await set_file_tags("f1", _req(), {"tags": ["Research", "q3"], "kind": "file"})
    assert resp["tags"] == ["research", "q3"]
    assert row.file_metadata["tags"] == ["research", "q3"]
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_foreign_file_403():
    from fastapi import HTTPException

    row = SimpleNamespace(id="f1", owner_id="someone-else", file_metadata={})
    factory, _ = _ctx(row)
    with (
        patch.object(files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())),
        patch.object(files_route, "AsyncSessionFactory", factory),
    ):
        with pytest.raises(HTTPException) as ei:
            await set_file_tags("f1", _req(), {"tags": ["x"], "kind": "file"})
    assert ei.value.status_code == 403


@pytest.mark.asyncio
async def test_sets_tags_on_owned_artifact_payload():
    row = SimpleNamespace(id="a1", owner_id="u1", payload={"title": "T"})
    factory, session = _ctx(row)
    with (
        patch.object(files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())),
        patch.object(files_route, "AsyncSessionFactory", factory),
    ):
        resp = await set_file_tags("a1", _req(), {"tags": ["draft"], "kind": "artifact"})
    assert resp["tags"] == ["draft"]
    assert row.payload == {"title": "T", "tags": ["draft"]}
    session.commit.assert_awaited_once()
