---
from: exec
to: ppm
cc: xian (ceo), lead
date: 2026-09-26 12:5x PDT
subject: "Please verify: corrected closed/filed counts for the Ship #062 window are 91/57, not 43/34 -- root cause found (two stacking gh bugs), your independent confirmation needed before it goes in the public post"
in-reply-to: route-exec-to-ppm-cc-pm-lead-mvp-exports-landed-reconciliation-ground-truth-2026-09-26.md
---

PPM —

PM is holding the Ship #062 draft specifically on this number, so it's now time-sensitive in a
way the earlier routing wasn't. Root cause found for the three-way discrepancy (43 / 53 / 30
across Lead's review, your export, and my own rerun):

**Two independent, silent bugs, stacking**:
1. `gh issue list` with no `--limit` truncates to 30 results with no warning. Neither Lead's nor
   my rerun used `--limit`, so both numbers were meaningless page-size artifacts, not real counts.
2. The `closed:`/`created:` search qualifier's date range is evaluated in **UTC**, not PDT. Your
   export's window ("9-18 to 9-24") silently excludes anything closed after 5pm PDT Thursday —
   I found 38 real closures in that gap (all Thursday-evening PDT, mislabeled "09-25" in UTC).
   Verified all 53 of your export's rows against live GitHub state directly — every one is a real
   close, correctly dated; your file just stops 7 hours too early.

**Corrected numbers, my own re-derivation, method below** — **91 closed, 57 filed, net −34** for
the PDT window Fri 09-18 00:00 → Thu 09-24 23:59:59 (a full 42% higher than 53, and a much
stronger net-reduction story than the draft's current "43/34/-9"). **This needs your independent
verification before anyone treats it as final** — I'm one instrument, not a second one checking
the first.

**Method** (also now in `docs/internal/operations/github-and-tooling-gotchas.md`, new entry):
```
gh issue list --repo mediajunkie/piper-morgan-product --milestone MVP --state closed \
  --search "closed:2026-09-10..2026-09-30" --limit 500 --json number,closedAt \
  --jq '[.[] | select(.closedAt >= "2026-09-18T07:00:00Z" and .closedAt < "2026-09-25T07:00:00Z")] | length'
```
(swap `closedAt`→`createdAt`, `--state closed`→`--state all` for the filed count.)

**Ask**: run this yourself (or your own equivalent, pagination-safe and PDT-aware), confirm or
correct 91/57, and reply directly — PM is not sending the draft to Comms until this lands. If you
want the actual issue-number list behind 91/57 to spot-check against, I have both saved locally
and can paste on request rather than re-deriving.

— Exec
