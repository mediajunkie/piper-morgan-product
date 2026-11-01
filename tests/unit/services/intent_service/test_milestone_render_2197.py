"""#2197 — CXO's one-milestone render (2026-11-01 11:17), verbatim, from the read dict."""

from __future__ import annotations

import pytest

from services.intent_service import milestone_render as mr

MVP = {
    "title": "MVP",
    "state": "open",
    "due_on": "2026-11-20T00:00:00Z",
    "open_issues": 4,
    "closed_issues": 6,
}


def test_one_milestone_carries_title_and_counts_from_the_read():
    assert mr.render_one_milestone(MVP) == (
        "**MVP**: 6 of 10 issues closed, 4 still open. Due 2026-11-20."
    )


def test_due_date_is_the_date_part_exactly_never_shifted():
    # CXO's pin: 20, not 19 — no timezone conversion.
    out = mr.render_one_milestone({**MVP, "due_on": "2026-11-20T00:00:00Z"})
    assert "Due 2026-11-20." in out and "2026-11-19" not in out
    assert mr.due_date_part("2026-11-20T07:00:00Z") == "2026-11-20"


@pytest.mark.parametrize("due", [None, "", 12345])
def test_no_due_date(due):
    out = mr.render_one_milestone({**MVP, "due_on": due})
    assert out.endswith("No due date is set.") and "Due " not in out


def test_closed_milestone():
    out = mr.render_one_milestone({**MVP, "state": "closed", "open_issues": 0})
    assert out == "**MVP** is closed: 6 of 6 issues done."


def test_no_issues_yet_keeps_the_due_clause():
    out = mr.render_one_milestone({**MVP, "open_issues": 0, "closed_issues": 0})
    assert out == "**MVP** has no issues yet. Due 2026-11-20."
    out = mr.render_one_milestone({**MVP, "open_issues": 0, "closed_issues": 0, "due_on": None})
    assert out == "**MVP** has no issues yet. No due date is set."


def test_degenerate_title_goes_through_display_title():
    out = mr.render_one_milestone({**MVP, "title": "   "})
    assert out.startswith("**(untitled milestone)**")


def test_fixed_lines_verbatim():
    assert mr.OPEN_ISSUES_OFFER_QUESTION == "Want to see the open issues?"
    assert mr.NAMED_ABSENT_LINE == "I couldn't find a milestone matching that in this project."
    assert mr.TIE_LINE == "That could mean more than one milestone, so I haven't picked one."
    assert mr.STATUS_LEAD_IN == "Here's the project as a whole:"
    assert mr.LIST_LEAD_IN == "Here are the milestones I can see:"
    assert mr.prefix_lines(mr.TIE_LINE, mr.LIST_LEAD_IN) == (
        mr.TIE_LINE + "\n" + mr.LIST_LEAD_IN + "\n\n"
    )
