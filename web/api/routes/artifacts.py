"""Artifacts API (#355 / #952) — save & list generated artifacts.

The chat "Save as artifact" affordance (#355) POSTs here to persist a chat output
as a *generated* `Artifact` (the #952 unifying-lens model) — carrying inline
content + source-conversation provenance + lifecycle, which a bare file upload
lacks. Owner-scoped via JWT (the #470 pattern), persisted via ArtifactRepository.

The /files browser surfaces these by projecting Artifact → UploadedFile through
`Artifact.to_uploaded_file()` (the #952 round-trip converter) — see files.py
(#355 slice 2). Artifact is the system-of-record; /files is a view.
"""

import re
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.repositories import ArtifactRepository
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Artifact, ArtifactSourceType
from services.mux.lifecycle import LifecycleState

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/artifacts", tags=["artifacts"])

_MIN_SAVE_LEN = (
    1  # endpoint accepts any non-empty content; the >500-char gate is a UI affordance (#355)
)


class SaveArtifactRequest(BaseModel):
    content: str
    title: Optional[str] = None
    source_conversation_id: Optional[str] = None


class RenameArtifactRequest(BaseModel):
    title: str


@router.post("")
@router.post("/")
async def save_artifact(
    body: SaveArtifactRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """Persist a chat output as a generated Artifact (owner = current user).

    Returns the saved artifact's id + metadata. The user-deliberate save marks it
    RATIFIED in the lifecycle (a kept artifact, not an emergent draft).
    """
    content = (body.content or "").strip()
    if len(content) < _MIN_SAVE_LEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot save an empty artifact.",
        )

    # Title rides in payload (Artifact has no flat title field — same place the
    # document converter keeps it), so a /files projection can show a name.
    payload = {}
    if body.title:
        payload["title"] = body.title

    artifact = Artifact(
        content=content,
        source_type=ArtifactSourceType.GENERATED,
        lifecycle_state=LifecycleState.RATIFIED,  # deliberate user save = kept/ratified
        owner_id=current_user.sub,
        source_conversation_id=body.source_conversation_id,
        payload=payload,
    )

    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            repo = ArtifactRepository(session)
            await repo.add(artifact)
    except Exception as e:
        logger.error("artifact_save_failed", error=str(e), user_id=current_user.sub)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save artifact.",
        )

    logger.info(
        "artifact_saved",
        artifact_id=artifact.id,
        user_id=current_user.sub,
        source_conversation_id=body.source_conversation_id,
        content_len=len(content),
    )
    return {
        "id": artifact.id,
        "source_type": artifact.source_type.value,
        "title": body.title or "Saved artifact",
        "size": len(content),
        "created_at": artifact.created_at.isoformat(),
    }


@router.get("/list")
async def list_artifacts(
    current_user: JWTClaims = Depends(get_current_user),
    limit: int = 50,
):
    """List the current user's artifacts (owner-scoped)."""
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            repo = ArtifactRepository(session)
            artifacts = await repo.list_for_owner(current_user.sub, limit=limit)
    except Exception as e:
        logger.error("artifact_list_failed", error=str(e), user_id=current_user.sub)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list artifacts.",
        )

    return {
        "artifacts": [
            {
                "id": a.id,
                "source_type": a.source_type.value,
                "title": (a.payload or {}).get("title", "Saved artifact"),
                "size": len(a.content or ""),
                "created_at": a.created_at.isoformat(),
            }
            for a in artifacts
        ]
    }


def _artifact_filename(title: Optional[str], artifact_id: str) -> str:
    """A safe .md filename for a saved artifact (title slug, else the id)."""
    base = (title or "").strip() or f"artifact-{artifact_id[:8]}"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", base).strip("-")[:60] or "artifact"
    return slug if slug.endswith(".md") else f"{slug}.md"


# #1184 — export formats. Content is stored once (markdown); format is a
# render/export concern. md/txt now; pdf/docx are a later enhancement.
_DOWNLOAD_FORMATS = {
    "md": ("text/markdown", ".md"),
    "txt": ("text/plain", ".txt"),
}


@router.get("/{artifact_id}/download")
async def download_artifact(
    artifact_id: str,
    format: str = "md",
    current_user: JWTClaims = Depends(get_current_user),
):
    """Download a generated artifact's content (#355 AC) in a chosen format
    (#1184: ``md``|``txt``; pdf/docx later). Owner-scoped (not the owner → 404,
    no existence leak). Bad format → 400 (fail fast, before the fetch)."""
    fmt = (format or "md").lower()
    if fmt not in _DOWNLOAD_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format '{format}'. Supported: {', '.join(_DOWNLOAD_FORMATS)}.",
        )
    media_type, ext = _DOWNLOAD_FORMATS[fmt]
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            repo = ArtifactRepository(session)
            artifact = await repo.get_by_id(artifact_id, owner_id=current_user.sub)
    except Exception as e:
        logger.error("artifact_download_failed", error=str(e), artifact_id=artifact_id)
        raise HTTPException(status_code=500, detail="Failed to fetch artifact.")
    if artifact is None:
        raise HTTPException(status_code=404, detail="Artifact not found.")

    base = _artifact_filename((artifact.payload or {}).get("title"), artifact.id)  # always .md
    filename = (base[:-3] + ext) if base.endswith(".md") else base
    return Response(
        content=artifact.content or "",
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/{artifact_id}/preview")
async def preview_artifact(
    artifact_id: str,
    current_user: JWTClaims = Depends(get_current_user),
):
    """Preview a generated artifact's content in-browser (#313). Artifacts are
    always text/markdown, so always previewable. Owner-scoped (not the owner → 404,
    no existence leak). Returns JSON for the /files preview modal to render."""
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            repo = ArtifactRepository(session)
            artifact = await repo.get_by_id(artifact_id, owner_id=current_user.sub)
    except Exception as e:
        logger.error("artifact_preview_failed", error=str(e), artifact_id=artifact_id)
        raise HTTPException(status_code=500, detail="Failed to fetch artifact.")
    if artifact is None:
        raise HTTPException(status_code=404, detail="Artifact not found.")

    filename = _artifact_filename((artifact.payload or {}).get("title"), artifact.id)
    return {
        "filename": filename,
        "content": artifact.content or "",
        "content_type": "text/markdown",
        "previewable": True,
    }


@router.delete("/{artifact_id}")
async def delete_artifact(
    artifact_id: str,
    current_user: JWTClaims = Depends(get_current_user),
):
    """Delete a generated artifact (owner-scoped; cross-owner → 404)."""
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            repo = ArtifactRepository(session)
            deleted = await repo.delete(artifact_id, owner_id=current_user.sub)
    except Exception as e:
        logger.error("artifact_delete_failed", error=str(e), artifact_id=artifact_id)
        raise HTTPException(status_code=500, detail="Failed to delete artifact.")
    if not deleted:
        raise HTTPException(status_code=404, detail="Artifact not found.")
    logger.info("artifact_deleted", artifact_id=artifact_id, user_id=current_user.sub)
    return {"deleted": True, "id": artifact_id}


@router.patch("/{artifact_id}")
async def rename_artifact(
    artifact_id: str,
    body: RenameArtifactRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """Rename a saved artifact (#1184) — updates the title that drives the
    projected /files filename. Owner-scoped (cross-owner → 404, no existence leak)."""
    new_title = (body.title or "").strip()
    if not new_title:
        raise HTTPException(status_code=400, detail="Title cannot be empty.")
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            repo = ArtifactRepository(session)
            artifact = await repo.update_title(artifact_id, new_title, owner_id=current_user.sub)
    except Exception as e:
        logger.error("artifact_rename_failed", error=str(e), artifact_id=artifact_id)
        raise HTTPException(status_code=500, detail="Failed to rename artifact.")
    if artifact is None:
        raise HTTPException(status_code=404, detail="Artifact not found.")
    filename = _artifact_filename((artifact.payload or {}).get("title"), artifact.id)
    logger.info("artifact_renamed", artifact_id=artifact_id, user_id=current_user.sub)
    return {"id": artifact.id, "title": new_title, "filename": filename}
