"""#355 slice 1 — artifacts API (save & list generated artifacts).

Calls the route handlers directly with a mocked JWTClaims + mocked
AsyncSessionFactory/ArtifactRepository (the established route-unit pattern) —
verifies the save path persists a generated Artifact owner-scoped, and list
returns the owner's artifacts. No DB / no HTTP.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes import artifacts as artifacts_route
from web.api.routes.artifacts import (
    RenameArtifactRequest,
    SaveArtifactRequest,
    _artifact_filename,
    delete_artifact,
    download_artifact,
    list_artifacts,
    rename_artifact,
    save_artifact,
)
from services.domain.models import Artifact, ArtifactSourceType
from services.mux.lifecycle import LifecycleState

_USER = SimpleNamespace(sub="user-355")


def _mock_session_ctx():
    factory = MagicMock()
    factory.session_scope_fresh.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
    factory.session_scope_fresh.return_value.__aexit__ = AsyncMock(return_value=None)
    return factory


class TestSaveArtifact:
    @pytest.mark.asyncio
    async def test_save_persists_generated_artifact_owner_scoped(self):
        repo = MagicMock()
        repo.add = AsyncMock()
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            resp = await save_artifact(
                SaveArtifactRequest(
                    content="A meaningful saved chat summary.",
                    title="My summary",
                    source_conversation_id="conv-42",
                ),
                current_user=_USER,
            )

        repo.add.assert_awaited_once()
        saved = repo.add.call_args.args[0]
        assert saved.source_type == ArtifactSourceType.GENERATED
        assert saved.owner_id == "user-355"
        assert saved.source_conversation_id == "conv-42"
        assert saved.lifecycle_state is LifecycleState.RATIFIED
        assert saved.content == "A meaningful saved chat summary."
        assert saved.payload["title"] == "My summary"
        # response shape
        assert resp["id"] == saved.id
        assert resp["source_type"] == "generated"
        assert resp["title"] == "My summary"

    @pytest.mark.asyncio
    async def test_empty_content_rejected_400(self):
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as ei:
            await save_artifact(SaveArtifactRequest(content="   "), current_user=_USER)
        assert ei.value.status_code == 400

    @pytest.mark.asyncio
    async def test_title_optional_defaults(self):
        repo = MagicMock()
        repo.add = AsyncMock()
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            resp = await save_artifact(
                SaveArtifactRequest(content="body only"), current_user=_USER
            )
        saved = repo.add.call_args.args[0]
        assert "title" not in saved.payload  # no title → not injected
        assert resp["title"] == "Saved artifact"  # response default


class TestListArtifacts:
    @pytest.mark.asyncio
    async def test_list_returns_owner_artifacts(self):
        from services.domain.models import Artifact

        a = Artifact(
            id="art-1", content="x" * 12, source_type=ArtifactSourceType.GENERATED,
            owner_id="user-355", payload={"title": "T"},
        )
        repo = MagicMock()
        repo.list_for_owner = AsyncMock(return_value=[a])
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            resp = await list_artifacts(current_user=_USER)

        repo.list_for_owner.assert_awaited_once_with("user-355", limit=50)
        assert len(resp["artifacts"]) == 1
        assert resp["artifacts"][0]["id"] == "art-1"
        assert resp["artifacts"][0]["title"] == "T"
        assert resp["artifacts"][0]["size"] == 12


class TestDownloadArtifact:
    @pytest.mark.asyncio
    async def test_download_returns_markdown_attachment(self):
        art = Artifact(id="art-d", content="# Summary\nbody", owner_id="user-355",
                       source_type=ArtifactSourceType.GENERATED, payload={"title": "My Notes"})
        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=art)
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            resp = await download_artifact("art-d", current_user=_USER)
        repo.get_by_id.assert_awaited_once_with("art-d", owner_id="user-355")
        assert resp.media_type == "text/markdown"
        assert resp.body == b"# Summary\nbody"
        assert "My-Notes.md" in resp.headers["content-disposition"]

    @pytest.mark.asyncio
    async def test_download_missing_or_cross_owner_404(self):
        from fastapi import HTTPException

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=None)  # not found / not owner
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            with pytest.raises(HTTPException) as ei:
                await download_artifact("nope", current_user=_USER)
        assert ei.value.status_code == 404

    @pytest.mark.asyncio
    async def test_download_format_txt_serves_plain_text(self):
        """#1184 — format=txt serves the same content as text/plain + .txt."""
        art = Artifact(id="art-d", content="# Summary\nbody", owner_id="user-355",
                       source_type=ArtifactSourceType.GENERATED, payload={"title": "My Notes"})
        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=art)
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            resp = await download_artifact("art-d", format="txt", current_user=_USER)
        assert resp.media_type == "text/plain"
        assert "My-Notes.txt" in resp.headers["content-disposition"]
        assert resp.body == b"# Summary\nbody"  # content stored once; format is an export concern

    @pytest.mark.asyncio
    async def test_download_unknown_format_400_fail_fast(self):
        """#1184 — unknown format → 400 before any fetch (pdf/docx are later)."""
        from fastapi import HTTPException

        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=None)
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            with pytest.raises(HTTPException) as ei:
                await download_artifact("art-d", format="pdf", current_user=_USER)
        assert ei.value.status_code == 400
        repo.get_by_id.assert_not_awaited()  # fail-fast: no fetch on a bad format


class TestDeleteArtifact:
    @pytest.mark.asyncio
    async def test_delete_owner_scoped(self):
        repo = MagicMock()
        repo.delete = AsyncMock(return_value=True)
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            resp = await delete_artifact("art-x", current_user=_USER)
        repo.delete.assert_awaited_once_with("art-x", owner_id="user-355")
        assert resp == {"deleted": True, "id": "art-x"}

    @pytest.mark.asyncio
    async def test_delete_missing_404(self):
        from fastapi import HTTPException

        repo = MagicMock()
        repo.delete = AsyncMock(return_value=False)
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            with pytest.raises(HTTPException) as ei:
                await delete_artifact("nope", current_user=_USER)
        assert ei.value.status_code == 404


class TestArtifactFilename:
    def test_slugifies_title(self):
        assert _artifact_filename("My Cool Summary!", "abc12345") == "My-Cool-Summary.md"

    def test_falls_back_to_id_when_no_title(self):
        assert _artifact_filename(None, "abcdef123456") == "artifact-abcdef12.md"

    def test_already_md(self):
        assert _artifact_filename("notes.md", "x") == "notes.md"


class TestRenameArtifact1184:
    """#1184 — PATCH /artifacts/{id} rename. Owner-scoped (the repo enforces it;
    the handler 404s on the None that cross-owner/missing returns)."""

    @pytest.mark.asyncio
    async def test_rename_owner_scoped_returns_new_filename(self):
        renamed = Artifact(
            id="a1", content="x", source_type=ArtifactSourceType.GENERATED,
            owner_id="user-355", payload={"title": "Q3 Planning Notes"},
        )
        repo = MagicMock()
        repo.update_title = AsyncMock(return_value=renamed)
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            resp = await rename_artifact(
                "a1", RenameArtifactRequest(title="Q3 Planning Notes"), current_user=_USER
            )
        repo.update_title.assert_awaited_once()
        # owner-scoped (no (a,3) leak — the rename passes the principal)
        assert repo.update_title.call_args.kwargs.get("owner_id") == "user-355"
        assert resp["id"] == "a1"
        assert resp["title"] == "Q3 Planning Notes"
        assert resp["filename"] == "Q3-Planning-Notes.md"  # title drives the projected filename

    @pytest.mark.asyncio
    async def test_rename_cross_owner_or_missing_404(self):
        from fastapi import HTTPException

        repo = MagicMock()
        repo.update_title = AsyncMock(return_value=None)  # repo returns None for cross-owner/missing
        with patch.object(artifacts_route, "AsyncSessionFactory", _mock_session_ctx()), patch.object(
            artifacts_route, "ArtifactRepository", return_value=repo
        ):
            with pytest.raises(HTTPException) as ei:
                await rename_artifact("a1", RenameArtifactRequest(title="X"), current_user=_USER)
        assert ei.value.status_code == 404

    @pytest.mark.asyncio
    async def test_rename_empty_title_400(self):
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as ei:
            await rename_artifact("a1", RenameArtifactRequest(title="   "), current_user=_USER)
        assert ei.value.status_code == 400
