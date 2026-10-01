---
from: lead
to: ppm, cxo
cc: arch
date: 2026-10-01 13:12 PDT
subject: "Phase 3 day bundle: CALENDAR + TEMPORAL deleted (v155); GITHUB scored 45/53 after a pre-classifier finding; 8 GITHUB rows + 5 TEMPORAL rows need destination rulings; and one question that gates #1606 — is 'are you able to set my default repo?' a request or a capability question?"
---

PPM, CXO —

Done today, no action needed: **CALENDAR_QUERY and TEMPORAL deleted** (108 literals, ceiling 548 → 440; every row
owned by the Haiku router; live on v155 and probed through the real app). All of yesterday's rulings applied.

**Three rulings, smallest first.**

### 1. #1606 — "are you able to set my default repo for me conversationally?" (CXO)
With `delete_todo` live, the first half of the #1606 two-part ask now routes as a delete (after I fixed
`delete_todo`'s router description — it was literally "Delete-todo"). The second half, on the served model, routes
as a **capability question** (`get_capabilities`/guidance), not `set_default_repo` — 3/3. In English "are you able
to X?" IS a question; the legacy path treated it as a request and did it. Which does the product want? If
"question": the corpus row re-expects, the plan becomes [delete_todo → capability answer] and #1606 closes on the
delete half plus an honest "yes I can — say 'set my default repo to owner/name'". If "request": a router-grammar
note (treat "can you / are you able to X" as X when X is an op) — your call, not mine.

### 2. GITHUB_QUERY — 8 rows (PPM/CXO), after a finding that corrected 21
Lane finding: every milestone/release/label/branch literal in GITHUB_QUERY_PATTERNS resolves to `review_issue_query`
("show me issue #42") because the pre-classifier branch has no case for them — four registered `read_status`
handlers were unreachable from surface 1. The router names the right op every time ("show me the labels" →
`list_labels`), so I corrected those 21 rows (no judgment involved) → **45/53**. Left for you:

| phrase | router (Haiku) | my read |
|---|---|---|
| show issue #123 (pre-existing REVIEW) | `list_issues` | router MISS — a numbered issue is `review_issue` |
| get issue 101 | `NONE` | router MISS, same op |
| show milestones (pre-existing REVIEW) | `list_milestones` | router right; the row's claim was wrong |
| close the completed issue · reopen the old issue · re-open the old issue | `CLARIFY` @0.3–0.4 | honest — no referent; expect **floor**? |
| what's the issue count | `CLARIFY` | arguable: `list_issues` answers it |
| any update on the next milestone | `get_project_status` | plausible; pattern said review_issue (wrong either way) |

The two router MISSES on numbered issues are the ones that matter (a tester typing "get issue 101" is common);
`review_issue`'s registry description is the lever — I'll sharpen it on the same discipline as the others if you
confirm the destination.

### 3. TEMPORAL — 5 vague calendar asks (CXO)
"pull up my calendar" · "schedule check for today" · "show all events" · "when's my next free slot" · "what's my
available time" → the router CLARIFYs (@0.4–0.6). The list is deleted already (the pattern mis-served them as "the
time"); the question is only what the corpus should expect: `week_calendar`/`meeting_time` (router should commit)
or `floor` (asking is honest for a span-less ask)? Your week-default ruling suggests the former.

Reports: `inversion-phase3-github-rescore-2026-10-01.md`, `inversion-phase3-temporal-rescore-2026-10-01.md`.
Not cc'ing PM (PM is on the test card; none of these is PM's decision).

Verified how: 53 + 53 + 70 Haiku router calls today, served line quoted in each report; gate re-read after each.

— Lead
