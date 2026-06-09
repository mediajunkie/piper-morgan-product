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
from web.api.routes.artifacts import SaveArtifactRequest, list_artifacts, save_artifact
from services.domain.models import ArtifactSourceType
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
