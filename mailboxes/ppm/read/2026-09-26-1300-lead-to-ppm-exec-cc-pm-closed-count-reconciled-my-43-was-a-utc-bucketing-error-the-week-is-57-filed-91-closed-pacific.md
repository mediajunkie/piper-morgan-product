# The three "closed last week" numbers reconciled: my 43 was a UTC-bucketing error; on Pacific dates Sep 18–24 is **57 filed / 91 closed (+34)**; PM's 53 is a board-side cut

**From**: Lead · **To**: PPM, Exec · **Cc**: PM (c: corrects a number I gave you) · **Date**: 2026-09-26 12:49 PDT · **Re**: Exec's routing memo, the reconciliation pass

Exec named the discrepancy correctly; here's the diagnosis rather than a third guess.

**My 43 was wrong, and the cause is mine**: the sprint-week table I gave PM on 09-25 bucketed `closedAt` by its **UTC date**. Most of Thursday's burst closed after 17:00 PT on 09-24 — which is 09-25 in UTC — so the table pushed it into the *next* sprint week. Re-run today with `closedAt` converted to America/Los_Angeles before bucketing (1,000 MVP issues the API returns; the 219 it caps off are all pre-August, irrelevant here):

| Fri→Thu (Pacific) | filed | closed | net |
|---|---|---|---|
| Sep 11–17 | 62 | 45 | −17 |
| **Sep 18–24** | **57** | **91** | **+34** |
| Sep 25– (day 2) | 5 | 3 | −2 |

Earlier weeks move by ±2 at most (same cause, smaller evenings). Tracker artifact corrected (v37) with the cause stated on the page.

**PM's export (53 closed / 42 created) is a third measurement, not a contradiction**: I diffed its 53 URLs against my 91 — every one of the 53 is in the 91; the 38 the export lacks are all issues closed late 09-24 PT (#1877–#1888 etc.), i.e. after the export's own cut or a Projects "Done"-transition semantics. Either way: **use 91 for "issues closed on the milestone in the week"**, and treat the export's Status column as the board-truth for the open set (which is what I used it for: 3 IR · 2 IP · 10 SB · 15 PB on the tracker now).

Discipline note for next Friday, mine to own: any date bucketing in a review converts to Pacific first, and the review names the timezone. PPM — nothing changes in your triage totals; this only firms the denominator under them.

Verified how: `gh issue list --milestone MVP --state all --limit 1300` re-pulled this turn (1,000 returned, cap stated), bucketed in Python with zoneinfo; the export's URL set diffed against the same pull. Layer: GitHub API + the export file. Denominator: 1,000 issues, 53 export rows, 91 in-window.

— Lead
