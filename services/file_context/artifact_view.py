"""File-shaped view of saved Artifacts (#1657).

The Files listing (web/api/routes/files.py) presents the user's documents as
uploads ∪ generated artifacts (#355: Artifact is the system-of-record; /files
is a view). Until #1657, that union existed ONLY in the listing — the chat
summarize rail's FileResolver read uploaded_files alone, so an account whose
one "document" was a saved artifact got the honest-empty reply while the Files
page showed the document (the wrong-empty PM hit live 2026-08-18).

This module is the single home of the projection both reads share:
  - ``artifact_filename`` — the display filename the listing shows (moved from
    web/api/routes/artifacts.py so services-layer code can use it without a
    web import; the route delegates here).
  - ``artifact_as_file_view`` — an Artifact projected into the UploadedFile
    shape FileResolver scores.

Ownership note: nothing here widens scoping. Callers fetch artifacts through
ArtifactRepository's owner-scoped queries; this module only reshapes rows the
caller was already entitled to read.
"""

import re
from typing import Optional

from services.domain.models import Artifact, UploadedFile


def artifact_filename(title: Optional[str], artifact_id: str) -> str:
    """A safe .md filename for a saved artifact (title slug, else the id).

    This IS the filename the Files listing displays (files.py projects
    artifacts through it) — so it is also the filename form a user will type
    back at the chat ("summarize artifact-8b029c94.md").
    """
    base = (title or "").strip() or f"artifact-{artifact_id[:8]}"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", base).strip("-")[:60] or "artifact"
    return slug if slug.endswith(".md") else f"{slug}.md"


def artifact_as_file_view(artifact: Artifact) -> UploadedFile:
    """Project an Artifact into the UploadedFile shape FileResolver consumes.

    Field mapping mirrors the /files listing's projection (files.py #355
    block): filename via artifact_filename, markdown content type, created_at
    as the upload time. storage_path stays empty — artifact content lives in
    the artifacts row, not file storage (document_handlers takes the artifact
    branch for these ids).
    """
    content = artifact.content or ""
    return UploadedFile(
        id=artifact.id,
        owner_id=str(artifact.owner_id or ""),
        filename=artifact_filename((artifact.payload or {}).get("title"), artifact.id),
        file_type="text/markdown",
        file_size=len(content),
        storage_path="",
        upload_time=artifact.created_at,
        last_referenced=None,
        reference_count=0,
    )
