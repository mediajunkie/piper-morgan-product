"""#2197 — the one-milestone render (CXO's words 2026-11-01 11:17, verbatim).

Pure functions, no I/O. Every value comes from the milestone dict code READ
this turn (``GitHubMCPSpatialAdapter.list_milestones``'s normalized shape:
title, state, due_on, open_issues, closed_issues). Nothing a model wrote is
ever rendered here: the resolver (``milestone_resolve``) only says WHICH read
milestone was meant, by index, and these functions render that read.

The due date is the DATE PART of ``due_on`` exactly as GitHub gives it
(``2026-11-20T00:00:00Z`` → ``2026-11-20``): no timezone conversion, no
"in N days". A ``due_on`` that is not a string renders as no due date.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from services.utils.text_sanitation import display_title

UNTITLED_MILESTONE = "(untitled milestone)"

# CXO 2026-11-01 11:17: appended on its own line when the milestone has open
# issues, never when it has none. Named *_QUESTION: the #1766 census's
# named-question-holder rule (the status/list branches arm the one-title pick
# whenever they render it).
OPEN_ISSUES_OFFER_QUESTION = "Want to see the open issues?"
# The named-absent and tie lines never carry the model's string.
NAMED_ABSENT_LINE = "I couldn't find a milestone matching that in this project."
TIE_LINE = "That could mean more than one milestone, so I haven't picked one."
# CXO 2026-11-02 19:09: "as a whole" promised a project status the floor did not keep on the
# named-absent branch; "what I can see" is true of whatever the floor then writes.
STATUS_LEAD_IN = "Here's what I can see in the project:"
LIST_LEAD_IN = "Here are the milestones I can see:"


def due_date_part(due_on: Any) -> Optional[str]:
    """``2026-11-20T00:00:00Z`` → ``2026-11-20``; anything else falsy → None."""
    if not isinstance(due_on, str) or not due_on.strip():
        return None
    return due_on.strip().split("T")[0]


def _count(m: Dict[str, Any], key: str) -> int:
    value = m.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else 0


def open_count(m: Dict[str, Any]) -> int:
    return _count(m, "open_issues")


def render_one_milestone(m: Dict[str, Any]) -> str:
    """CXO's one-milestone line from the read dict."""
    title = display_title(m.get("title"), UNTITLED_MILESTONE)
    opened = _count(m, "open_issues")
    closed = _count(m, "closed_issues")
    total = opened + closed
    if m.get("state") == "closed":
        return f"**{title}** is closed: {closed} of {total} issues done."
    due = due_date_part(m.get("due_on"))
    due_clause = f"Due {due}." if due else "No due date is set."
    if total == 0:
        return f"**{title}** has no issues yet. {due_clause}"
    return f"**{title}**: {closed} of {total} issues closed, {opened} still open. {due_clause}"


def prefix_lines(line: str, lead_in: str) -> str:
    """The named-absent / tie prefix placed before a default answer."""
    return f"{line}\n{lead_in}\n\n"


__all__ = (
    "OPEN_ISSUES_OFFER_QUESTION",
    "NAMED_ABSENT_LINE",
    "TIE_LINE",
    "STATUS_LEAD_IN",
    "LIST_LEAD_IN",
    "due_date_part",
    "open_count",
    "render_one_milestone",
    "prefix_lines",
)
