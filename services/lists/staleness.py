"""
List staleness computation (#714 MUX-LISTS-STALENESS-UI).

Per #714 audit dispositions May 3:
- Q2 Option C: lazy effective timestamp = max(List.updated_at, max(ListItem.added_at))
- Q3: single 60-day default threshold, env-configurable via PIPER_LIST_STALENESS_DAYS
- Q5 conceptual integrity: vocabulary uses "stale" / "old" / "untouched" /
  "last updated"; NEVER "archived" / lifecycle stage names

Pure functions; trivial unit tests at
`tests/unit/services/lists/test_staleness_714.py`.

Per `dev/2026/05/03/714-staleness-design-v0.md` for design rationale.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional

# Default threshold in days. Override with PIPER_LIST_STALENESS_DAYS env var.
DEFAULT_STALENESS_THRESHOLD_DAYS = 60


def get_staleness_threshold() -> int:
    """Read the staleness threshold (in days) from env, with default fallback."""
    raw = os.environ.get("PIPER_LIST_STALENESS_DAYS")
    if raw is None:
        return DEFAULT_STALENESS_THRESHOLD_DAYS
    try:
        value = int(raw)
        if value <= 0:
            return DEFAULT_STALENESS_THRESHOLD_DAYS
        return value
    except (ValueError, TypeError):
        return DEFAULT_STALENESS_THRESHOLD_DAYS


@dataclass
class StalenessSignal:
    """Per-list staleness state for the API response.

    Field names use the audit-Q5 OK vocabulary: `stale`, `last_updated`.
    No "archived" / lifecycle terms.
    """

    is_stale: bool
    days_since_update: int
    last_updated_human: str

    def to_dict(self) -> dict:
        return {
            "is_stale": self.is_stale,
            "days_since_update": self.days_since_update,
            "last_updated_human": self.last_updated_human,
        }


def _ensure_aware(dt: datetime) -> datetime:
    """Promote a naive datetime to UTC-aware. List/ListItem timestamps
    are TIMESTAMPTZ at the DB level so this is mostly defensive."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def effective_updated_at(
    list_updated_at: datetime,
    item_added_at_values: Iterable[datetime],
) -> datetime:
    """Compute the effective last-touched timestamp for a list.

    `max(List.updated_at, max(ListItem.added_at for items, default=list_updated_at))`

    Empty item lists fall back to `List.updated_at`.
    """
    list_ts = _ensure_aware(list_updated_at)
    items_aware = [_ensure_aware(d) for d in item_added_at_values]
    if not items_aware:
        return list_ts
    return max(list_ts, max(items_aware))


def format_last_updated_human(days_since: int) -> str:
    """Human-readable "last updated" label per Q5 vocabulary.

    Bands:
    - 0 days → "today"
    - 1 day → "yesterday"
    - 2-29 days → "N days ago"
    - 30-59 days → "about a month ago" / "N months ago" approx
    - 60+ days → "N months ago" or "over a year ago"
    """
    if days_since <= 0:
        return "today"
    if days_since == 1:
        return "yesterday"
    if days_since < 30:
        return f"{days_since} days ago"
    if days_since < 60:
        return "about a month ago"
    if days_since < 365:
        months = days_since // 30
        return f"{months} months ago"
    if days_since < 730:
        return "over a year ago"
    years = days_since // 365
    return f"over {years} years ago"


def compute_staleness(
    list_updated_at: datetime,
    item_added_at_values: Iterable[datetime],
    threshold_days: Optional[int] = None,
    now: Optional[datetime] = None,
) -> StalenessSignal:
    """Compute the staleness signal for a list given its updated_at + items.

    Args:
        list_updated_at: List.updated_at (TIMESTAMPTZ from DB)
        item_added_at_values: iterable of ListItem.added_at for items in the list
        threshold_days: override the env-driven default
        now: override the wall-clock now (test injection)

    Returns:
        StalenessSignal with is_stale + days_since_update + human label.
    """
    threshold = threshold_days if threshold_days is not None else get_staleness_threshold()
    now_aware = _ensure_aware(now or datetime.now(timezone.utc))

    effective = effective_updated_at(list_updated_at, item_added_at_values)
    delta = now_aware - effective
    days_since = max(0, delta.days)
    is_stale = days_since > threshold
    return StalenessSignal(
        is_stale=is_stale,
        days_since_update=days_since,
        last_updated_human=format_last_updated_human(days_since),
    )
