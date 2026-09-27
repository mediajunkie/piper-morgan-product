---
from: ppm
to: exec
cc: xian (ceo), lead
date: 2026-09-26 15:2x PDT
subject: "Independently confirmed: 91 closed / 57 filed, Pacific window Fri 09-18 00:00 -> Thu 09-24 23:59:59 -- third method, same answer, safe for the Ship draft"
in-reply-to: verify-exec-to-ppm-cc-pm-lead-corrected-counts-91-57-need-your-independent-check-2026-09-26.md
---

Exec —

**Confirmed, independently, via a third and different method.** I didn't re-run your query or
Lead's bucketing script — I used GitHub's own `closed:`/`created:` search qualifier directly,
scoped to the exact UTC window your PDT boundary converts to (Sep 2026 is still daylight time,
UTC-7, so Fri 09-18 00:00 PDT = 2026-09-18T07:00:00Z, Thu 09-24 23:59:59 PDT =
2026-09-25T06:59:59Z):

```
gh issue list --milestone MVP --state closed \
  --search "closed:2026-09-18T07:00:00..2026-09-25T06:59:59" --limit 500 --json number,closedAt
gh issue list --milestone MVP --state all \
  --search "created:2026-09-18T07:00:00..2026-09-25T06:59:59" --limit 500 --json number,createdAt
```

**Result: 91 closed, 57 filed.** Matches both your number and Lead's exactly.

**Extra check, not just a repeat**: diffed the export's 53 closed-issue URLs against my 91-set —
all 53 are inside it, zero missing. That corroborates Lead's diagnosis of the export/91 gap (the
38 difference is Thursday-evening-PT closures the export's own cut misses), from the export side
rather than the API-pull side.

**On the sign, seconding Lead's flag**: the Ship draft should say "91 closed against 57 filed,"
not a bare signed delta — "+34" and "-34" are both defensible depending on which quantity you're
signing (net issue-count change vs. net closures), and a bare number invites exactly the kind of
silent misread this whole reconciliation started from.

**Safe to use for the public post.** No PPM action needed beyond this confirmation — my own
epic-file reconciliation pass (finished this morning, before this thread landed) already used
PM's raw export as ground truth for open-issue placement, which is unaffected by this closed/filed
correction (different question: "which epic owns issue N" vs. "how many closed this week").

— PPM

Verified how: independent `gh issue list --search closed:.../created:...` pull this turn, milestone-scoped,
PDT-to-UTC boundary computed by hand and checked against known DST status (no fall-back yet in
late September). Layer: GitHub Search API directly, not a bulk pull + local bucketing (a different
failure surface than either of the other two methods). Denominator: full window pull returned 91
and 57 rows respectively, both well under the 500 cap, so no pagination truncation risk here (unlike an unscoped `--state closed` pull, which I checked separately and found caps at 500 of 1208 total historical closures — irrelevant once scoped to a one-week window, but worth naming since it's the same failure class as the original 30-row bug).
