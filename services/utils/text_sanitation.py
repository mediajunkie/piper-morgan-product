"""Display-text sanitation helpers — #1622 / #1628.

``display_title`` began life as ``_display_title`` in ``services/radar/sources.py``
(#1622), guarding the Radar entity-derivation seam. #1628 found the same
degenerate-title class reaching chat output verbatim through every other
listing surface (open-issues listings, PR listings, status/priority previews,
first-contact demo block …) — a guard placed at one seam had been read as
global. It now lives here so every render site applies the same rule.
"""

from typing import Any


def display_title(value: Any, fallback: str) -> str:
    """Backing-store title → safe display title; ``fallback`` when degenerate (#1622).

    A degenerate title — empty, whitespace-only, a single glyph, or pure
    punctuation (e.g. the literal ``{`` of a JSON-fragment issue title) — is
    garbage-in that must not render as signal: PM's standup Watch list showed
    ``'"{"' hasn't moved in 380 days``. Callers pass a fallback that carries the
    item's identifier where one exists (e.g. ``(untitled work item #100)``) so
    the item stays findable/fixable rather than silently dropped — these are
    real observed entities; hiding them would fabricate an all-clear.
    """
    text = str(value).strip() if value is not None else ""
    if len(text) <= 1 or not any(ch.isalnum() for ch in text):
        return fallback
    return text
