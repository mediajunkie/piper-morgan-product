"""#1657 — chat summarize sees the SAME document set the Files listing shows.

The live wrong-empty (PM, 2026-08-18): the Files page listed one document —
``artifact-8b029c94.md`` — while "summarize artifact-8b029c94.md" answered
"I don't see any uploaded documents". The divergence was TABLE divergence:

  Listing  (web/api/routes/files.py):   uploaded_files WHERE owner_id = user
                                        ∪ artifacts WHERE owner_id = user
                                          AND source_type = 'generated'
  Resolver (services/repositories/file_repository.py, pre-fix):
                                        uploaded_files WHERE owner_id = user
                                        (artifacts: never read)

An account whose only "document" was a saved artifact was therefore listing-
visible and resolver-invisible. The fixtures never caught it because every
fixture seeds a fresh uploaded_files row — the m-44 education the issue names.

What this file pins (all deterministic, no DB, no LLM):
  1. FileResolver with an artifact repository resolves an artifact-only
     account's document — by exact projected filename AND by bare reference.
  2. Filename-form matching: a stored filename typed verbatim wins outright
     (0.98), is boundary-safe ('report.pdf' never matches inside
     'old-report.pdf'), and a named-but-absent filename answers None
     (honest) instead of summarizing the best-scoring OTHER document.
  3. Ownership: the artifact read is list_for_owner(owner, generated) — the
     resolver never widens scoping to make resolution pass.
  4. handle_analyze_document/handle_summarize_document take the artifact
     branch for an owned artifact id (projected filename, text-path summary)
     and still raise FileNotFoundError for a cross-owner id.
  5. The rail constructs the resolver WITH the artifact repository.
  6. The filename projection is single-sourced: the route helper and the
     services-layer function produce identical names (the two reads cannot
     drift apart again).
"""

from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Artifact, Intent, UploadedFile
from services.file_context.artifact_view import artifact_as_file_view, artifact_filename
from services.file_context.exceptions import AmbiguousFileReferenceError
from services.file_context.file_resolver import FileResolver
from services.shared_types import IntentCategory

_OWNER = "3f7b8a52-1657-4b00-9e00-000000001657"
_ARTIFACT_ID = "8b029c94-1657-4c00-9e00-000000001657"
_YEAR_AGO = datetime.now() - timedelta(days=365)


def _intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.SYNTHESIS,
        action="summarize_document",
        original_message=message,
        confidence=0.9,
        context={"original_message": message},
    )


def _aged_artifact(artifact_id: str = _ARTIFACT_ID, title=None) -> Artifact:
    """PM's row shape: a year-old generated artifact with NO title — its /files
    name is the id-derived projection ('artifact-8b029c94.md')."""
    return Artifact(
        id=artifact_id,
        content="# Q3 plan\n\nShip the beta. Then rest.",
        owner_id=_OWNER,
        payload={"title": title} if title else {},
        created_at=_YEAR_AGO,
        updated_at=_YEAR_AGO,
    )


def _upload(filename: str, file_id: str, age_days: int = 0) -> UploadedFile:
    return UploadedFile(
        id=file_id,
        owner_id=_OWNER,
        filename=filename,
        file_type="application/pdf",
        upload_time=datetime.now() - timedelta(days=age_days),
    )


def _resolver(uploads, artifacts):
    file_repo = MagicMock()
    file_repo.get_files_for_session = AsyncMock(return_value=uploads)
    file_repo.get_recent_files_all_sessions = AsyncMock(return_value=uploads)
    artifact_repo = MagicMock()
    artifact_repo.list_for_owner = AsyncMock(return_value=artifacts)
    return FileResolver(file_repo, artifact_repository=artifact_repo), file_repo, artifact_repo


# ---------------------------------------------------------------------------
# 1 + 2 + 3 — resolver sees the listing's set; filename forms; ownership
# ---------------------------------------------------------------------------


class TestResolverSeesTheFilesViewSet:
    @pytest.mark.asyncio
    async def test_artifact_only_account_resolves_by_projected_filename(self):
        """THE #1657 shape: zero uploads, one aged artifact, the exact message
        PM typed. Pre-fix this returned (None, 0.0) → the honest-empty reply."""
        resolver, _files, artifact_repo = _resolver([], [_aged_artifact()])
        file_id, confidence = await resolver.resolve_file_reference(
            _intent("summarize artifact-8b029c94.md"), _OWNER
        )
        assert file_id == _ARTIFACT_ID
        assert confidence >= 0.9
        # Ownership honored: the artifact read is the listing's own query
        # shape — this owner, generated only. Never widened.
        args, kwargs = artifact_repo.list_for_owner.await_args
        assert args[0] == _OWNER
        assert kwargs.get("source_type") == "generated"

    @pytest.mark.asyncio
    async def test_artifact_only_account_resolves_bare_reference(self):
        """'summarize the document' with one artifact and no uploads must bind
        to the artifact via scoring — not fall to honest-empty."""
        resolver, _files, _arts = _resolver([], [_aged_artifact()])
        file_id, _confidence = await resolver.resolve_file_reference(
            _intent("summarize the document"), _OWNER
        )
        assert file_id == _ARTIFACT_ID

    @pytest.mark.asyncio
    async def test_without_artifact_repo_behavior_is_unchanged(self):
        """Legacy construction (no artifact repo) stays uploads-only — the
        pre-#1657 callers and tests see identical behavior."""
        file_repo = MagicMock()
        file_repo.get_files_for_session = AsyncMock(return_value=[])
        resolver = FileResolver(file_repo)
        file_id, confidence = await resolver.resolve_file_reference(
            _intent("summarize artifact-8b029c94.md"), _OWNER
        )
        assert (file_id, confidence) == (None, 0.0)

    @pytest.mark.asyncio
    async def test_artifact_fetch_failure_degrades_to_uploads_only(self):
        """files.py degrades its artifact half the same way (artifacts = []):
        an artifact-store error must not take uploads resolution down."""
        upload = _upload("report.pdf", "file-r1")
        resolver, _files, artifact_repo = _resolver([upload], [])
        artifact_repo.list_for_owner = AsyncMock(side_effect=RuntimeError("store down"))
        file_id, _confidence = await resolver.resolve_file_reference(
            _intent("summarize report.pdf"), _OWNER
        )
        assert file_id == "file-r1"


class TestExplicitFilenameForms:
    @pytest.mark.asyncio
    async def test_exact_filename_beats_recency_scoring(self):
        """A verbatim stored filename wins outright — a year-old hash-shaped
        name must not lose to a fresher upload on recency/type noise."""
        fresh = _upload("todays-notes.pdf", "file-fresh", age_days=0)
        old = _upload("q3-roadmap-2025.pdf", "file-old", age_days=365)
        resolver, _f, _a = _resolver([fresh, old], [])
        file_id, confidence = await resolver.resolve_file_reference(
            _intent("summarize q3-roadmap-2025.pdf"), _OWNER
        )
        assert file_id == "file-old"
        assert confidence == 0.98

    @pytest.mark.asyncio
    async def test_filename_match_is_boundary_safe(self):
        """'old-report.pdf' in the message must match ONLY old-report.pdf —
        'report.pdf' is a substring of it and must not co-match (which would
        raise a bogus ambiguity)."""
        a = _upload("old-report.pdf", "file-a")
        b = _upload("report.pdf", "file-b")
        resolver, _f, _arts = _resolver([a, b], [])
        file_id, _confidence = await resolver.resolve_file_reference(
            _intent("summarize old-report.pdf"), _OWNER
        )
        assert file_id == "file-a"

    @pytest.mark.asyncio
    async def test_named_but_absent_filename_answers_honestly(self):
        """If the user names a specific file nobody owns, the resolver must
        return None (→ the honest reply) — never confidently summarize the
        best-scoring OTHER document."""
        resolver, _f, _arts = _resolver([_upload("report.pdf", "file-r1")], [])
        file_id, confidence = await resolver.resolve_file_reference(
            _intent("summarize artifact-deadbeef.md"), _OWNER
        )
        assert (file_id, confidence) == (None, 0.0)

    @pytest.mark.asyncio
    async def test_duplicate_exact_matches_raise_ambiguity(self):
        a = _upload("notes.md", "file-a")
        b = _upload("notes.md", "file-b")
        resolver, _f, _arts = _resolver([a, b], [])
        with pytest.raises(AmbiguousFileReferenceError):
            await resolver.resolve_file_reference(_intent("summarize notes.md"), _OWNER)


# ---------------------------------------------------------------------------
# 4 — handler layer: the artifact branch, owner-scoped
# ---------------------------------------------------------------------------


@asynccontextmanager
async def _fake_scope():
    yield MagicMock()


class TestHandlerArtifactBranch:
    @pytest.mark.asyncio
    async def test_owned_artifact_id_summarizes_via_the_text_path(self):
        from services.intent_service import document_handlers

        artifact = _aged_artifact()
        analysis = SimpleNamespace(
            summary="Ships the beta. Rest follows. Risks are noted",
            key_findings=["Beta first"],
            recommendations=[],  # #1660: handler now surfaces this field too
            generated_at=datetime(2026, 8, 18, 12, 0, 0),
        )
        with (
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
                _fake_scope,
            ),
            patch(
                "services.intent_service.document_handlers._get_uploaded_file",
                AsyncMock(return_value=None),
            ),
            patch(
                "services.intent_service.document_handlers._get_owned_artifact",
                AsyncMock(return_value=artifact),
            ) as owned,
            patch.object(
                document_handlers._doc_analyzer,
                "analyze_text",
                AsyncMock(return_value=analysis),
            ) as analyze_text,
        ):
            result = await document_handlers.handle_summarize_document(
                file_id=_ARTIFACT_ID, format="bullet", user_id=_OWNER
            )
        # The filename is the LISTING's projection — the name PM saw and typed.
        assert result["filename"] == "artifact-8b029c94.md"
        assert result["file_id"] == _ARTIFACT_ID
        # Real handle_summarize_document formatting ran (bullet pass).
        assert result["summary"].startswith("• ")
        analyze_text.assert_awaited_once()
        assert analyze_text.await_args.args[0] == artifact.content
        # Owner-scoped fetch got THIS user.
        assert owned.await_args.args[0] == _ARTIFACT_ID
        assert owned.await_args.args[1] == _OWNER

    @pytest.mark.asyncio
    async def test_cross_owner_artifact_still_raises(self):
        """The repository's owner scoping returns None for another owner's
        artifact → FileNotFoundError, exactly like an unowned upload. The fix
        never widens ownership to make resolution pass."""
        from services.intent_service import document_handlers

        with (
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
                _fake_scope,
            ),
            patch(
                "services.intent_service.document_handlers._get_uploaded_file",
                AsyncMock(return_value=None),
            ),
            patch(
                "services.intent_service.document_handlers._get_owned_artifact",
                AsyncMock(return_value=None),
            ),
        ):
            with pytest.raises(FileNotFoundError):
                await document_handlers.handle_analyze_document(
                    file_id=_ARTIFACT_ID, user_id=_OWNER
                )

    def test_get_owned_artifact_passes_the_principal(self):
        """_get_owned_artifact hands the caller's user_id to the repository's
        owner_id filter (repositories.py D3: scoping in the SELECT)."""
        import inspect

        from services.intent_service.document_handlers import _get_owned_artifact

        src = inspect.getsource(_get_owned_artifact)
        assert "owner_id=user_id" in src


# ---------------------------------------------------------------------------
# 5 — the rail hands the resolver the artifact repository
# ---------------------------------------------------------------------------


class TestRailWiring:
    @pytest.mark.asyncio
    async def test_rail_constructs_resolver_with_artifact_repository(self):
        from services.database.repositories import ArtifactRepository
        from services.intent_service.workflow_entries import (
            run_summarize_document_workflow,
        )

        resolver_cls = MagicMock()
        resolver_cls.return_value.resolve_file_reference = AsyncMock(return_value=(None, 0.0))
        with (
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope",
                _fake_scope,
            ),
            patch("services.file_context.file_resolver.FileResolver", resolver_cls),
        ):
            result = await run_summarize_document_workflow(
                session_id="sess-1657",
                user_id=_OWNER,
                context={"intent": _intent("summarize artifact-8b029c94.md")},
            )
        assert "I don't see any uploaded documents" in result.message
        kwargs = resolver_cls.call_args.kwargs
        assert isinstance(kwargs.get("artifact_repository"), ArtifactRepository), (
            "The rail must hand FileResolver the artifact repository — without "
            "it the resolver reads uploaded_files alone and the #1657 "
            "wrong-empty comes back."
        )


# ---------------------------------------------------------------------------
# 6 — one projection, two readers
# ---------------------------------------------------------------------------


class TestProjectionUnity:
    def test_route_helper_delegates_to_the_shared_projection(self):
        from web.api.routes.artifacts import _artifact_filename

        for title, aid in [
            (None, _ARTIFACT_ID),
            ("", _ARTIFACT_ID),
            ("Q3 Roadmap!", _ARTIFACT_ID),
            ("already-named.md", _ARTIFACT_ID),
        ]:
            assert _artifact_filename(title, aid) == artifact_filename(title, aid)

    def test_untitled_projection_is_the_shape_pm_saw(self):
        assert artifact_filename(None, "8b029c94-aaaa-bbbb-cccc-000000000000") == (
            "artifact-8b029c94.md"
        )

    def test_file_view_carries_projected_filename_and_created_at(self):
        artifact = _aged_artifact()
        view = artifact_as_file_view(artifact)
        assert view.id == _ARTIFACT_ID
        assert view.filename == "artifact-8b029c94.md"
        assert view.file_type == "text/markdown"
        assert view.upload_time == artifact.created_at
        assert view.reference_count == 0
