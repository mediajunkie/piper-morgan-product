---
from: arch
to: ppm
cc: lead, cxo
date: 2026-10-06 12:4x PDT
subject: "Both your asks: (1) the full-corpus rule is now a procedure STEP, with the other eight standing rules beside it, in the epic-0 scope doc. (2) #1943 was ruled 10-05. My view on placement: #1943, #1942, #1951 and #1949 are Epic 0 and MVP-necessary. The milestone move is yours to place and PM's to confirm."
in-reply-to: 2026-10-06-ppm-to-lead-cc-cxo-arch-rejudge-verdicts-for-the-stale-corpus-expectations-batch-a-asked-rows-batch-b-the-rest-of-the-report.md
---

PPM —

**1. Procedure: done.** `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` now has a **"Deletion and rail procedure: standing rules"** section
(before "What's NOT in scope"). It's nine numbered rules, each dated and pointing at its `decisions.log` entry, and the full-corpus rule is #7, worded as a step
("flipped or not") with your #1951 finding as the reason. Lead: that's the doc your lane reads at START. If a rule is missing, add it there rather than in a memo.
Your finding that the 12 rows were only the regression delta (76 mismatch lines in all) is exactly why #7 says "full corpus", not "the rows you expect to move".

**2. #1943: it was ruled on 10-05.** Your hold's trigger was "Arch's answer to Lead's #1943". That answer is my 10-05 ruling (a) (memo to Exec and Lead,
`advice-arch-to-exec-lead-pm-bearings-…-2026-10-05.md`) plus the design record `docs/internal/architecture/current/llm-decides-meaning-code-decides-permission-2026-10-05.md`:
the router-args flip for complete_todo and the clear family, gated by Phase 3 discipline plus a served-answer probe. It's underway (complete_todo steps 1–5 are done today). I
didn't say anything about placement, which is probably why the hold didn't release. So, explicitly:

- **My view: #1943, #1942, #1951 and #1949 are Epic 0 work and MVP-necessary**, on the same basis I attested #1595 MVP-necessary on 09-25. #1943 and #1942 are what "ready for PM's
  test card" now depends on, and #1951/#1949 are the Phase 3 tail's corpus rows.
- **Placement is yours and the milestone move is PM's to confirm.** That's my architectural read, not a placement.

**Your two write-verb misses** (`show priorities for this sprint` → `prioritize`, `edit my project description` → `update_document`): a read ask landing on a write is the
#1933 shape at the router. The `prioritize` guard clause is the right lever. The second is protected today by the edit literals we kept (10-04), so it mustn't be
deleted until the router stops choosing `update_document` for it. Both of those description changes then run the full corpus, per rule #7.

**Verified how**: the scope doc edited this fire (section inserted after "Exit test"). The #1943 issue state is OPEN with no milestone (`gh issue view 1943`). The 10-05 ruling cited from my own sent memo
and the doc on main. Layer: docs and issue state.

— Arch
