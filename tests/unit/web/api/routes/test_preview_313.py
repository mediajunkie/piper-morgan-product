"""#313 slice 2 — in-browser preview endpoints (artifacts + files).

Artifacts are always text/markdown → always previewable. Files preview returns
content for text types and previewable=false for binary. Route handlers called
directly with mocked session/repo (the established route-unit pattern); the
template Preview button + modal are asserted via content + verified live (#1165).
"""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes import artifacts as artifacts_route
from web.api.routes import files as files_route
from web.api.routes.artifacts import preview_artifact
from web.api.routes.files import preview_file
from services.domain.models import Artifact, ArtifactSourceType

_USER = SimpleNamespace(sub="user-313")


def _artifact_session_ctx():
    factory = MagicMock()
    factory.session_scope_fresh.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
    factory.session_scope_fresh.return_value.__aexit__ = AsyncMock(return_value=None)
    return factory


class TestArtifactPreview313:
    @pytest.mark.asyncio
    async def test_artifact_always_previewable_returns_content(self):
        art = Artifact(
            id="art-1",
            content="# Summary\nbody text",
            source_type=ArtifactSourceType.GENERATED,
            owner_id="user-313",
            payload={"title": "My Notes"},
        )
        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=art)
        with (
            patch.object(artifacts_route, "AsyncSessionFactory", _artifact_session_ctx()),
            patch.object(artifacts_route, "ArtifactRepository", return_value=repo),
        ):
            resp = await preview_artifact("art-1", current_user=_USER)
        repo.get_by_id.assert_awaited_once_with("art-1", owner_id="user-313")
        assert resp["previewable"] is True
        assert resp["content"] == "# Summary\nbody text"
        assert resp["content_type"] == "text/markdown"
        assert "My-Notes" in resp["filename"]

    @pytest.mark.asyncio
    async def test_artifact_missing_or_cross_owner_404(self):
        from fastapi import HTTPException

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=None)
        with (
            patch.object(artifacts_route, "AsyncSessionFactory", _artifact_session_ctx()),
            patch.object(artifacts_route, "ArtifactRepository", return_value=repo),
        ):
            with pytest.raises(HTTPException) as ei:
                await preview_artifact("nope", current_user=_USER)
        assert ei.value.status_code == 404


def _files_session_ctx(file_row):
    """AsyncSessionFactory.session_scope_fresh() ctx whose session.execute(...).
    scalar_one_or_none() returns file_row."""
    session = MagicMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = file_row
    session.execute = AsyncMock(return_value=result)
    factory = MagicMock()
    factory.session_scope_fresh.return_value.__aenter__ = AsyncMock(return_value=session)
    factory.session_scope_fresh.return_value.__aexit__ = AsyncMock(return_value=None)
    return factory


def _req(user_id="u1", is_admin=False):
    return SimpleNamespace(state=SimpleNamespace(user_id=user_id, is_admin=is_admin))


class TestFilePreview313:
    @pytest.mark.asyncio
    async def test_text_file_returns_content(self, tmp_path):
        p = tmp_path / "notes.md"
        p.write_text("# Hello\nsome notes", encoding="utf-8")
        row = SimpleNamespace(
            id="f1",
            filename="notes.md",
            file_type="text/markdown",
            owner_id="u1",
            storage_path=str(p),
        )
        with (
            patch.object(
                files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())
            ),
            patch.object(files_route, "AsyncSessionFactory", _files_session_ctx(row)),
        ):
            resp = await preview_file("f1", _req())
        assert resp["previewable"] is True
        assert resp["content"] == "# Hello\nsome notes"
        assert resp["truncated"] is False

    @pytest.mark.asyncio
    async def test_binary_file_not_previewable_no_disk_read(self):
        # application/pdf → previewable=false; storage_path intentionally bogus to
        # prove the binary branch returns BEFORE any disk read.
        row = SimpleNamespace(
            id="f2",
            filename="doc.pdf",
            file_type="application/pdf",
            owner_id="u1",
            storage_path="/nonexistent/doc.pdf",
        )
        with (
            patch.object(
                files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())
            ),
            patch.object(files_route, "AsyncSessionFactory", _files_session_ctx(row)),
        ):
            resp = await preview_file("f2", _req())
        assert resp["previewable"] is False
        assert "download" in resp["message"].lower()

    @pytest.mark.asyncio
    async def test_cross_owner_403(self):
        from fastapi import HTTPException

        row = SimpleNamespace(
            id="f3",
            filename="x.txt",
            file_type="text/plain",
            owner_id="someone-else",
            storage_path="/x",
        )
        with (
            patch.object(
                files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())
            ),
            patch.object(files_route, "AsyncSessionFactory", _files_session_ctx(row)),
        ):
            with pytest.raises(HTTPException) as ei:
                await preview_file("f3", _req(user_id="u1", is_admin=False))
        assert ei.value.status_code == 403

    @pytest.mark.asyncio
    async def test_missing_file_404(self):
        from fastapi import HTTPException

        with (
            patch.object(
                files_route, "db", SimpleNamespace(_initialized=True, initialize=AsyncMock())
            ),
            patch.object(files_route, "AsyncSessionFactory", _files_session_ctx(None)),
        ):
            with pytest.raises(HTTPException) as ei:
                await preview_file("nope", _req())
        assert ei.value.status_code == 404


class TestPreviewTemplate313:
    @pytest.fixture
    def files_html(self) -> str:
        return (Path(__file__).resolve().parents[5] / "templates" / "files.html").read_text()

    def test_preview_button_and_modal_present(self, files_html):
        assert 'onclick="previewFile(' in files_html
        assert "function previewFile(" in files_html
        assert "function showPreviewModal(" in files_html
        assert "function closePreviewModal(" in files_html
        # kind-aware: artifacts vs files preview endpoint
        assert "/preview" in files_html
        assert "file-preview-content" in files_html
