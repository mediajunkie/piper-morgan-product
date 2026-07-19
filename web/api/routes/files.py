"""
File Upload API Routes (Issue #282: CORE-ALPHA-FILE-UPLOAD)

Provides file upload endpoint with:
- User-isolated file storage
- File validation (size, type)
- Database metadata tracking
- Progress indication support
"""

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.connection import db
from services.database.models import UploadedFileDB
from services.database.session_factory import AsyncSessionFactory
from services.file_context.storage import (  # #1306: the single byte seam
    get_upload_base,
    read_file_from_storage,
    save_file_to_storage,
    write_file_to_storage,
)

router = APIRouter(prefix="/api/v1/files", tags=["files"])
logger = structlog.get_logger(__name__)

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = {
    "text/plain",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/markdown",
    "application/json",
}
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx", ".md", ".json"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Upload a file with validation and user isolation.

    Security:
    - Max 10MB file size
    - Allowed types: text, PDF, Word, Markdown, JSON
    - User-isolated storage
    - Proper error handling

    Args:
        file: Uploaded file
        current_user: Current authenticated user (from JWT token)

    Returns:
        JSON with file_id, filename, size, and metadata

    Raises:
        HTTPException 413: File too large (>10MB)
        HTTPException 415: Unsupported file type
        HTTPException 500: Server error during upload

    Issue #282: CORE-ALPHA-FILE-UPLOAD
    """
    try:
        # 1. Validate file exists
        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is required",
            )

        # 2. Read file content
        file_content = await file.read()

        # 3. Validate file size
        file_size = len(file_content)
        if file_size > MAX_FILE_SIZE:
            logger.warning(
                "file_too_large",
                user_id=current_user.sub,
                filename=file.filename,
                size=file_size,
                max_size=MAX_FILE_SIZE,
            )
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large: {file_size} bytes (max {MAX_FILE_SIZE})",
            )

        # 4. Validate file type (MIME type)
        if file.content_type not in ALLOWED_MIME_TYPES:
            logger.warning(
                "file_type_not_allowed",
                user_id=current_user.sub,
                filename=file.filename,
                content_type=file.content_type,
            )
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file type: {file.content_type}. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}",
            )

        # 5. Validate file extension
        file_path = Path(file.filename)
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            logger.warning(
                "file_extension_not_allowed",
                user_id=current_user.sub,
                filename=file.filename,
                extension=file_path.suffix,
            )
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file extension: {file_path.suffix}. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        # 6. Create user-isolated directory
        upload_dir = get_upload_base() / current_user.sub
        upload_dir.mkdir(parents=True, exist_ok=True)

        # 7. Generate unique file ID and safe filename
        file_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file_id}_{file.filename}"
        safe_file_path = upload_dir / safe_filename

        # 8. Save file to disk — through the #1306 encrypt seam (this route
        # previously bypassed save_file_to_storage with a raw open/write).
        try:
            write_file_to_storage(safe_file_path, file_content)

            logger.info(
                "file_saved_to_disk",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
                path=str(safe_file_path),
                size=file_size,
            )
        except IOError as e:
            logger.error(
                "file_save_failed",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
                error=str(e),
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file to storage",
            )

        # 9. Store metadata in database
        try:
            # Initialize database if needed
            if not db._initialized:
                await db.initialize()

            # Create database record with SEC-RBAC owner_id
            # Use fresh session to avoid event loop mismatch (#442)
            async with AsyncSessionFactory.session_scope_fresh() as session:
                uploaded_file = UploadedFileDB(
                    id=file_id,
                    owner_id=current_user.sub,  # SEC-RBAC ownership
                    filename=file.filename,
                    file_type=file.content_type,
                    file_size=file_size,
                    storage_path=str(safe_file_path),
                    upload_time=datetime.now(timezone.utc),
                    file_metadata={
                        "original_filename": file.filename,
                        "uploaded_by": current_user.sub,
                        "uploaded_at": datetime.now(timezone.utc).isoformat(),
                    },
                )

                session.add(uploaded_file)
                await session.commit()

            logger.info(
                "file_metadata_stored",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
            )

        except Exception as e:
            logger.error(
                "file_metadata_storage_failed",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
                error=str(e),
                exc_info=True,
            )
            # Clean up the file from disk since DB write failed
            try:
                safe_file_path.unlink(missing_ok=True)
            except Exception:
                pass  # Best effort cleanup
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save file metadata to database",
            )

        # 10. Return response
        response = {
            "file_id": file_id,
            "filename": file.filename,
            "size": file_size,
            "content_type": file.content_type,
            "status": "uploaded",
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "storage_path": str(safe_file_path),  # For testing/admin only
        }

        logger.info(
            "file_upload_complete",
            user_id=current_user.sub,
            file_id=file_id,
            filename=file.filename,
            size=file_size,
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        # Unexpected errors
        logger.error(
            "file_upload_error",
            user_id=current_user.sub,
            filename=file.filename if file else "unknown",
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload file",
        )


@router.get("/list")
async def list_files(
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    List all files uploaded by current user.

    Returns:
        List of files with metadata

    Issue #282: CORE-ALPHA-FILE-UPLOAD
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Query user's files using owner_id for SEC-RBAC compliance
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(UploadedFileDB).where(UploadedFileDB.owner_id == current_user.sub)
            )
            files = result.scalars().all()

            # #355: also surface saved generated Artifacts in the browser. Artifact
            # is the system-of-record; /files is a view. Generated artifacts have no
            # file-shaped payload, so project directly (NOT via to_uploaded_file,
            # which expects file-origin payload). Actions route to /api/v1/artifacts
            # by the `kind` marker. Failure here must not break the file list.
            from services.database.repositories import ArtifactRepository

            try:
                artifacts = await ArtifactRepository(session).list_for_owner(
                    current_user.sub, source_type="generated", limit=100
                )
            except Exception:
                artifacts = []

        # Format response
        file_list = [
            {
                "file_id": f.id,
                "kind": "file",
                "filename": f.filename,
                "size": f.file_size,
                "content_type": f.file_type,
                "uploaded_at": f.upload_time.isoformat() if f.upload_time else None,
                "reference_count": f.reference_count,
                "last_referenced": (f.last_referenced.isoformat() if f.last_referenced else None),
                "tags": (f.file_metadata or {}).get("tags", []),  # #313 MVP
            }
            for f in files
        ]
        # #355: append generated-artifact entries (download/delete via /api/v1/artifacts).
        from web.api.routes.artifacts import _artifact_filename

        for a in artifacts:
            title = (a.payload or {}).get("title")
            file_list.append(
                {
                    "file_id": a.id,
                    "kind": "artifact",
                    "filename": _artifact_filename(title, a.id),
                    "owner_id": a.owner_id,  # owner-scoped query → current user; needed by files.html isOwner()
                    "size": len(a.content or ""),
                    "content_type": "text/markdown",
                    "uploaded_at": a.created_at.isoformat() if a.created_at else None,
                    "reference_count": 0,
                    "last_referenced": None,
                    "tags": (a.payload or {}).get("tags", []),  # #313 MVP
                }
            )

        logger.info(
            "files_listed",
            user_id=current_user.sub,
            count=len(file_list),
        )

        return {
            "files": file_list,
            "count": len(file_list),
        }

    except Exception as e:
        logger.error(
            "file_list_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list files",
        )


@router.get("/{file_id}")
async def get_file(
    file_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Get file metadata by ID with ownership validation (SEC-RBAC).

    Only returns file metadata if current user is the owner.

    Args:
        file_id: File ID to retrieve
        current_user: Current authenticated user

    Returns:
        File metadata (if owned by current user)

    Raises:
        HTTPException 404: File not found or not owned by current user
        HTTPException 500: Server error during retrieval

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Find file with ownership validation
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(UploadedFileDB).where(
                    UploadedFileDB.id == file_id,
                    UploadedFileDB.owner_id == current_user.sub,
                )
            )
            file = result.scalar_one_or_none()

            if not file:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File not found: {file_id}",
                )

        # Format response
        file_response = {
            "file_id": file.id,
            "filename": file.filename,
            "size": file.file_size,
            "content_type": file.file_type,
            "uploaded_at": file.upload_time.isoformat() if file.upload_time else None,
            "reference_count": file.reference_count,
            "last_referenced": file.last_referenced.isoformat() if file.last_referenced else None,
            "storage_path": file.storage_path,
        }

        logger.info(
            "file_retrieved",
            user_id=current_user.sub,
            file_id=file_id,
        )

        return file_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "file_get_error",
            user_id=current_user.sub,
            file_id=file_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve file",
        )


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> dict:
    """
    Delete a file uploaded by current user.

    Args:
        file_id: File ID to delete
        current_user: Current authenticated user

    Returns:
        Success message

    Issue #282: CORE-ALPHA-FILE-UPLOAD
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Find file using owner_id for SEC-RBAC compliance
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(UploadedFileDB).where(
                    UploadedFileDB.id == file_id,
                    UploadedFileDB.owner_id == current_user.sub,
                )
            )
            file = result.scalar_one_or_none()

            if not file:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File not found: {file_id}",
                )

            # Delete from storage
            file_path = Path(file.storage_path)
            if file_path.exists():
                try:
                    file_path.unlink()
                    logger.info(
                        "file_deleted_from_storage",
                        user_id=current_user.sub,
                        file_id=file_id,
                        path=file.storage_path,
                    )
                except OSError as e:
                    logger.warning(
                        "file_delete_from_storage_failed",
                        user_id=current_user.sub,
                        file_id=file_id,
                        path=file.storage_path,
                        error=str(e),
                    )
                    # Continue to delete from database even if file deletion fails

            # Delete from database
            await session.delete(file)
            await session.commit()

            logger.info(
                "file_deleted",
                user_id=current_user.sub,
                file_id=file_id,
                filename=file.filename,
            )

            return {
                "status": "deleted",
                "file_id": file_id,
                "filename": file.filename,
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "file_delete_error",
            user_id=current_user.sub,
            file_id=file_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file",
        )


@router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    request: Request,
) -> Response:
    """
    Download a file by ID with ownership validation (SEC-RBAC).

    Args:
        file_id: File ID to download
        request: FastAPI request with user_id in state

    Returns:
        File content as attachment

    Raises:
        HTTPException 404: File not found or not owned by current user
        HTTPException 403: Not authorized to download this file
        HTTPException 500: Server error during download

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        user_id = getattr(request.state, "user_id", None)
        is_admin = getattr(request.state, "is_admin", False)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )

        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Find file with ownership validation
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(UploadedFileDB).where(UploadedFileDB.id == file_id)
            )
            file = result.scalar_one_or_none()

            if not file:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File not found: {file_id}",
                )

            # Check permissions: only owner or admin can download
            if not is_admin and file.owner_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to download this file",
                )

            # Verify file exists on disk
            file_path = Path(file.storage_path)
            if not file_path.exists():
                logger.error(
                    "file_content_missing",
                    user_id=user_id,
                    file_id=file_id,
                    path=file.storage_path,
                )
                # #1401 honest-degrade: the DB row survived but the bytes are
                # gone (uploads predating the durable volume were wiped by
                # deploys). 410, not 404 — the file existed; its content is
                # permanently lost. Re-upload is the only recovery.
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail=(
                        "This file's content is no longer available — it was "
                        "uploaded before durable storage was added and did not "
                        "survive a redeploy. Please upload it again."
                    ),
                )

            logger.info(
                "file_download_started",
                user_id=user_id,
                file_id=file_id,
                filename=file.filename,
            )

            # #1450: read through the #1306 decrypt seam — FileResponse(path)
            # would stream raw disk bytes, which are PMENC1: ciphertext when
            # at-rest encryption is on (it is, on beta).
            raw = read_file_from_storage(file_path)
            return Response(
                content=raw,
                media_type=file.file_type or "application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{file.filename}"'
                },
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "file_download_error",
            user_id=getattr(request.state, "user_id", "unknown"),
            file_id=file_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download file",
        )


# #313: in-browser preview — text types return content; binary returns previewable=false.
_PREVIEWABLE_MIME_PREFIXES = ("text/",)
_PREVIEWABLE_MIME_EXACT = {"application/json", "application/x-ndjson"}
_PREVIEWABLE_EXTENSIONS = {".md", ".markdown", ".txt", ".json", ".csv", ".log"}
_PREVIEW_MAX_BYTES = 256 * 1024  # cap in-browser preview payload


@router.get("/{file_id}/preview")
async def preview_file(file_id: str, request: Request):
    """Preview an uploaded file's content in-browser (#313). Text types return their
    content (UTF-8, capped at 256KB); binary types (PDF/Word/etc.) return
    previewable=false with a download-to-view message. Owner/admin-scoped (mirrors
    download). Returns JSON for the /files preview modal."""
    try:
        user_id = getattr(request.state, "user_id", None)
        is_admin = getattr(request.state, "is_admin", False)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )
        if not db._initialized:
            await db.initialize()
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(UploadedFileDB).where(UploadedFileDB.id == file_id)
            )
            file = result.scalar_one_or_none()
            if not file:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"File not found: {file_id}",
                )
            if not is_admin and file.owner_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to view this file",
                )

            ext = Path(file.filename or "").suffix.lower()
            ctype = (file.file_type or "").lower()
            previewable = (
                ctype.startswith(_PREVIEWABLE_MIME_PREFIXES)
                or ctype in _PREVIEWABLE_MIME_EXACT
                or ext in _PREVIEWABLE_EXTENSIONS
            )
            if not previewable:
                return {
                    "filename": file.filename,
                    "previewable": False,
                    "content_type": file.file_type,
                    "message": "Preview isn't available for this file type — download it to view.",
                }

            file_path = Path(file.storage_path)
            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="File not found on disk"
                )
            raw = read_file_from_storage(file_path)  # #1306 decrypt seam
            truncated = len(raw) > _PREVIEW_MAX_BYTES
            try:
                content = raw[:_PREVIEW_MAX_BYTES].decode("utf-8")
            except UnicodeDecodeError:
                return {
                    "filename": file.filename,
                    "previewable": False,
                    "content_type": file.file_type,
                    "message": "Preview isn't available for this file (not valid text) — download it to view.",
                }
            return {
                "filename": file.filename,
                "content": content,
                "content_type": file.file_type,
                "previewable": True,
                "truncated": truncated,
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "file_preview_error",
            user_id=getattr(request.state, "user_id", "unknown"),
            file_id=file_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to preview file",
        )


@router.post("/download-bulk")
async def download_bulk(
    request: Request,
    body: dict,
):
    """Bulk download (#313 G64): zip of selected files + artifacts.

    Body: ``{"items": [{"id": "...", "kind": "file"|"artifact"}, ...]}`` (≤50).
    Per-item ownership enforced with the same rules as single download (files:
    owner or admin; artifacts: owner-scoped). Items the caller can't access or
    that are missing are SKIPPED (listed in the X-Skipped header count) rather
    than failing the whole zip.
    """
    import io
    import zipfile

    user_id = getattr(request.state, "user_id", None)
    is_admin = getattr(request.state, "is_admin", False)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    items = (body or {}).get("items") or []
    if not isinstance(items, list) or not items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="items list required")
    if len(items) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Max 50 items per bulk download"
        )

    if not db._initialized:
        await db.initialize()

    buf = io.BytesIO()
    added, skipped = 0, 0
    used_names: set = set()

    def _dedupe(name: str) -> str:
        if name not in used_names:
            used_names.add(name)
            return name
        stem, dot, ext = name.rpartition(".")
        base = stem if dot else name
        suffix_ext = f".{ext}" if dot else ""
        n = 2
        while f"{base}-{n}{suffix_ext}" in used_names:
            n += 1
        final = f"{base}-{n}{suffix_ext}"
        used_names.add(final)
        return final

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            for item in items:
                fid = (item or {}).get("id")
                kind = (item or {}).get("kind", "file")
                if not fid:
                    skipped += 1
                    continue
                try:
                    if kind == "artifact":
                        from services.database.repositories import ArtifactRepository

                        art = await ArtifactRepository(session).get_by_id(fid, owner_id=user_id)
                        if not art:
                            skipped += 1
                            continue
                        title = (art.payload or {}).get("title") if art.payload else None
                        name = _dedupe(_artifact_zip_name(title, fid))
                        zf.writestr(name, art.content or "")
                        added += 1
                    else:
                        result = await session.execute(
                            select(UploadedFileDB).where(UploadedFileDB.id == fid)
                        )
                        file = result.scalar_one_or_none()
                        if not file or (not is_admin and file.owner_id != user_id):
                            skipped += 1
                            continue
                        p = Path(file.storage_path)
                        if not p.exists():
                            skipped += 1
                            continue
                        zf.writestr(_dedupe(file.filename or fid), read_file_from_storage(p))  # #1306
                        added += 1
                except Exception as e:  # one bad item must not kill the zip
                    logger.warning("bulk_download_item_skipped", item_id=fid, error=str(e))
                    skipped += 1

    if added == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No downloadable items")

    from fastapi.responses import Response

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    logger.info("bulk_download", user_id=user_id, added=added, skipped=skipped)
    return Response(
        content=buf.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="piper-files-{stamp}.zip"',
            "X-Added": str(added),
            "X-Skipped": str(skipped),
        },
    )


def _artifact_zip_name(title, artifact_id: str) -> str:
    """Safe .md name for an artifact inside the bulk zip (mirrors artifacts.py)."""
    import re as _re

    base = (title or "").strip() or f"artifact-{artifact_id[:8]}"
    slug = _re.sub(r"[^A-Za-z0-9._-]+", "-", base).strip("-")[:60] or "artifact"
    return slug if slug.endswith(".md") else f"{slug}.md"


def _normalize_tags(raw) -> list:
    """#313 tag MVP: freeform, lowercased, deduped, ≤10 tags of ≤30 chars.
    Freeform-vs-taxonomy is deliberately deferred to the CXO design pass."""
    if not isinstance(raw, list):
        return []
    seen, out = set(), []
    for t in raw:
        if not isinstance(t, str):
            continue
        tag = t.strip().lower()[:30]
        if tag and tag not in seen:
            seen.add(tag)
            out.append(tag)
        if len(out) >= 10:
            break
    return out


@router.put("/{file_id}/tags")
async def set_file_tags(file_id: str, request: Request, body: dict):
    """Set tags on an uploaded file OR artifact (#313 G64 MVP, owner-only).

    Body: {"tags": ["...",...], "kind": "file"|"artifact"}. Stored in the
    existing JSON columns (file_metadata.tags / payload.tags) — no migration.
    """
    user_id = getattr(request.state, "user_id", None)
    is_admin = getattr(request.state, "is_admin", False)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    tags = _normalize_tags((body or {}).get("tags"))
    kind = (body or {}).get("kind", "file")
    if not db._initialized:
        await db.initialize()
    async with AsyncSessionFactory.session_scope_fresh() as session:
        if kind == "artifact":
            from services.database.models import ArtifactDB

            result = await session.execute(select(ArtifactDB).where(ArtifactDB.id == file_id))
            row = result.scalar_one_or_none()
            if not row or row.owner_id != user_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
            payload = dict(row.payload or {})
            payload["tags"] = tags
            row.payload = payload
        else:
            result = await session.execute(
                select(UploadedFileDB).where(UploadedFileDB.id == file_id)
            )
            row = result.scalar_one_or_none()
            if not row:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
            if not is_admin and row.owner_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
            meta = dict(row.file_metadata or {})
            meta["tags"] = tags
            row.file_metadata = meta
        await session.commit()
    logger.info("file_tags_set", user_id=user_id, file_id=file_id, kind=kind, tags=tags)
    return {"file_id": file_id, "tags": tags}
