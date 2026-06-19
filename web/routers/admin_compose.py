"""Admin compose UI routes (Phase 2: Edit + Autosave).

Issue #998 — lightweight editorial compose UI.
    GET  /admin/compose            — list drafts needing finishing
    GET  /admin/compose/{slug}     — editable detail view
    POST /admin/compose/{slug}/save — autosave (JSON body)

Phases 3-4 (image upload, git operations) are NOT in this file.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from services.editorial.calendar import list_drafts_needing_finishing
from services.editorial.draft import parse_draft, resolve_draft_path, write_draft

router = APIRouter(prefix="/api/v1/admin/compose", tags=["admin", "compose"])

# Templates live at web/templates/ — sibling of this routers/ directory
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def compose_list(request: Request) -> HTMLResponse:
    """List drafts with status=drafted and pubDate today/within 7 days or blank."""
    drafts = list_drafts_needing_finishing(today=date.today(), horizon_days=7)
    return templates.TemplateResponse(
        "admin/compose_list.html",
        {"request": request, "drafts": drafts},
    )


@router.get("/{slug}", response_class=HTMLResponse)
async def compose_detail(request: Request, slug: str) -> HTMLResponse:
    """Read-only detail view of a draft markdown file."""
    path = resolve_draft_path(slug)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Draft not found: {slug}")
    frontmatter, body = parse_draft(path)
    # Derive a title from the first H1 if present, else slug
    title = _extract_title(body) or slug
    return templates.TemplateResponse(
        "admin/compose_detail.html",
        {
            "request": request,
            "slug": slug,
            "title": title,
            "frontmatter": frontmatter,
            "body": body,
        },
    )


class SavePayload(BaseModel):
    image: str = ""
    alt: str = ""
    caption: str = ""
    body: str = ""


@router.post("/{slug}/save", response_class=JSONResponse)
async def compose_save(slug: str, payload: SavePayload) -> JSONResponse:
    """Autosave endpoint — receives form fields as JSON, writes to draft file."""
    path = resolve_draft_path(slug)
    if path is None:
        raise HTTPException(status_code=404, detail=f"Draft not found: {slug}")
    frontmatter = {
        "image": payload.image,
        "alt": payload.alt,
        "caption": payload.caption,
    }
    write_draft(path, frontmatter, payload.body)
    return JSONResponse({"saved": True, "slug": slug})


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped:
            # Stop looking if we've hit non-empty non-H1 content
            break
    return ""
