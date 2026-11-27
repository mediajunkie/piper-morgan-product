"""The one rule for "this GitHub issue is high priority" (#2458).

Before #2458 two paths each had their own label list (the priority read filtered on
six, the status gather ranked on three), and the floor was handed every open issue
under a heading that said "High-priority". On beta a reply called an issue "flagged
as high priority" that nobody had checked for a label.

Arch's condition (2026-11-27): one predicate over one constant set, read by every
path that says "high priority" or counts it. PPM's set (same day): the union of
both lists, matched by exact name, ignoring case, no substrings. CXO: a reply says
the one phrase ``high priority`` and never a label's raw name.

The tuple is ordered: its order is the ranking the status gather has always used
(critical, then urgent, then high), widened to the union's spellings.
"""

from typing import Any, Iterable, Optional

#: PPM 2026-11-27 (issue 2458). Exact names, compared lower-case. Order = rank.
HIGH_PRIORITY_LABELS = (
    "priority: critical",
    "critical",
    "p0",
    "priority: urgent",
    "urgent",
    "p1",
    "priority: high",
    "priority-high",
    "high-priority",
)

#: CXO 2026-11-27: the one phrase a person is shown, whichever label matched.
HIGH_PRIORITY_PHRASE = "high priority"


def _names(labels: Optional[Iterable[Any]]) -> list:
    """Label names, lower-cased. GitHub hands labels as strings on some reads and as
    ``{"name": ...}`` on others; anything else is not a label name."""
    names = []
    for label in labels or []:
        if isinstance(label, dict):
            label = label.get("name")
        if isinstance(label, str):
            names.append(label.strip().lower())
    return names


def priority_rank(labels: Optional[Iterable[Any]]) -> int:
    """Position of the issue's best label in ``HIGH_PRIORITY_LABELS``; an issue with
    none of them ranks after every labelled one (``len(HIGH_PRIORITY_LABELS)``)."""
    names = set(_names(labels))
    for rank, label in enumerate(HIGH_PRIORITY_LABELS):
        if label in names:
            return rank
    return len(HIGH_PRIORITY_LABELS)


def is_high_priority(labels: Optional[Iterable[Any]]) -> bool:
    """True only when the issue carries one of ``HIGH_PRIORITY_LABELS``, by exact
    name. No label, an unknown label or a near-miss ("priority: low", "p10") is not
    high priority."""
    return priority_rank(labels) < len(HIGH_PRIORITY_LABELS)
