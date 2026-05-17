"""Tag-to-topic mapping for the Insight Journal topic filter (#1037).

The Insight Journal page (`templates/insights.html`) defines 6 topic tabs:
All / Work Patterns / Projects / Preferences / Relationships / Scheduling.
The `SurfaceableInsight`'s `Learning` has free-form `topic_tags: List[str]`.
This module derives one of the 5 specific topic categories (or None for
"All") from those tags via a heuristic mapping config.

Approach chosen from #1037 implementation options: **Option B** — derive
topic from tags at read time. No schema migration; mapping config is
tunable as real-user observation data accrues.

Per Pattern-073 discipline: the mapping returns `None` (uncategorized)
rather than guessing when no tags match — bounded observation, not
categorical claim.

Note on taxonomy correctness: with no real-user data at filing time
(2026-05-17), the keyword sets below are best-effort. Trigger conditions
in #1037 explicitly call out "validation that 5 spec categories are the
right cuts" as un-deferral criteria; this mapping is the working draft
that real-data observation will refine.
"""

from __future__ import annotations

from typing import Iterable, Optional


# Mapping: topic-id (matches templates/insights.html `data-topic="..."`)
# → set of keyword fragments that, when present in any tag, map the
# insight to that topic. Keywords are matched case-insensitively as
# substrings of each tag.
_TOPIC_KEYWORDS = {
    "work-patterns": {
        "pattern", "workflow", "routine", "habit", "rhythm",
        "behavior", "tendency", "approach",
    },
    "projects": {
        "project", "milestone", "feature", "epic", "sprint",
        "deliverable", "release",
    },
    "preferences": {
        "preference", "style", "tone", "voice", "format",
        "favorite", "preferred", "dislike",
    },
    "relationships": {
        "person", "people", "team", "relationship", "collaborator",
        "user", "contact", "stakeholder",
    },
    "scheduling": {
        "calendar", "schedule", "meeting", "time", "deadline",
        "agenda", "appointment", "availability",
    },
}


def derive_topic_from_tags(tags: Optional[Iterable[str]]) -> Optional[str]:
    """Derive one of the 5 Insight Journal topic categories from free-form tags.

    Returns the topic-id (e.g. "work-patterns") on the first matched
    category — categories are checked in declaration order. Returns None
    when no tag matches (uncategorized; user sees the insight in "All"
    only).

    Per Pattern-073 discipline: bounded observation. We DON'T guess a
    topic when tags are empty or no keyword matches — we surface "no
    category for this insight" honestly, which the UI renders as
    All-only-visibility.

    Args:
        tags: Iterable of free-form tag strings (typically from
            `Learning.topic_tags`). None or empty → None.

    Returns:
        One of "work-patterns", "projects", "preferences", "relationships",
        "scheduling", or None.

    Examples:
        >>> derive_topic_from_tags(["calendar", "deadline"])
        'scheduling'
        >>> derive_topic_from_tags(["coding", "implementation"])
        # → None (no keywords match)
        >>> derive_topic_from_tags(None)
        # → None
    """
    if not tags:
        return None

    # Normalize all tags to lowercase for substring matching
    normalized = [t.lower() for t in tags if t]
    if not normalized:
        return None

    for topic_id, keywords in _TOPIC_KEYWORDS.items():
        for tag in normalized:
            for kw in keywords:
                if kw in tag:
                    return topic_id

    return None


# Re-exported for tests + future config-driven extension
KNOWN_TOPICS = tuple(_TOPIC_KEYWORDS.keys())
