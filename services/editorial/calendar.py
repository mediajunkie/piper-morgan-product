"""Read and filter the editorial calendar CSV.

Phase 1 scope: identify drafts that need finishing (status=drafted, pubDate today
or within horizon, or blank).
"""

from __future__ import annotations

import csv
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

# Repo root: services/editorial/calendar.py → two parents up is piper-morgan-product/
PIPER_ROOT = Path(__file__).resolve().parent.parent.parent
CALENDAR_PATH = PIPER_ROOT / "docs" / "internal" / "planning" / "comms" / "editorial-calendar.csv"

_DRAFTS_SUBDIR_PREFIX = "docs/public/comms/drafts/"


def slugify(title: str) -> str:
    """Lowercase, strip common punctuation, hyphenate spaces.

    Matches the simple rule in the Phase 1 brief: comma, period, apostrophe,
    colon removed; spaces → hyphens.
    """
    s = title.lower()
    s = re.sub(r"[,.':\u2019]", "", s)  # includes curly apostrophe
    s = re.sub(r"\s+", "-", s.strip())
    return s


def _derive_slug(row: dict) -> str:
    """Prefer draftPath column, else derive from title."""
    draft_path = (row.get("draftPath") or "").strip()
    if draft_path:
        # Strip the prefix and .md suffix if present
        p = draft_path
        if p.startswith(_DRAFTS_SUBDIR_PREFIX):
            p = p[len(_DRAFTS_SUBDIR_PREFIX) :]
        if p.endswith(".md"):
            p = p[:-3]
        # If file pattern is draft-<slug>-v1, strip that wrapper too
        m = re.match(r"^draft-(.+?)(?:-v\d+)?$", p)
        if m:
            return m.group(1)
        return p
    return slugify(row.get("title") or "")


def _parse_pubdate(raw: str) -> Optional[date]:
    raw = (raw or "").strip()
    if not raw:
        return None
    # Calendar uses ISO YYYY-MM-DD
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        return None


_DONE_STATUSES = frozenset({"published"})


def list_drafts_needing_finishing(
    today: date,
    horizon_days: int = 7,
    calendar_path: Path = CALENDAR_PATH,
) -> list[dict]:
    """Return all calendar rows that are not yet published, augmented with a 'slug' key.

    Includes drafted, queued, and blank-status rows. Excludes published rows only.
    The pubDate horizon filter is intentionally removed — PM wants to see all
    in-flight posts regardless of scheduled date.
    """
    if not calendar_path.exists():
        return []

    results: list[dict] = []
    with calendar_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = (row.get("status") or "").strip().lower()
            if status in _DONE_STATUSES:
                continue
            augmented = dict(row)
            augmented["slug"] = _derive_slug(row)
            results.append(augmented)
    return results
