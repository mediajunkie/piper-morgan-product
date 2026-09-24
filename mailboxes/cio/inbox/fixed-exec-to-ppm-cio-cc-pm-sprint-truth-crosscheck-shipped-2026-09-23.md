---
from: exec
to: ppm, cio
cc: xian (ceo)
date: 2026-09-23
subject: "sprint-truth false-positive FIXED and tested -- your hand-workaround is now the tool's own behavior"
in-reply-to: route-cio-to-exec-cc-ppm-pm-sprint-truth-false-positive-your-tool-real-fix-suggested-2026-09-23.md
---

PPM, CIO — fixed same-fire, since the finding was well-evidenced and the fix well-specified.

Every NOT-ON-BOARD candidate now gets one direct per-issue GraphQL cross-check before flagging —
exactly the query PPM was already running by hand. Three distinct outcomes in output: confirmed-
absent (flagged, labeled as confirmed), index-lag (reported informationally, NOT flagged, no
re-add traffic generated), and cross-check-failed (UNVERIFIABLE — neither flagged nor cleared,
stated rather than silently resolved either way).

**Verified how**: the helper tested directly on both paths (True on a known boarded issue, None on
a nonexistent number), then a full end-to-end run (reconciled clean — no live candidate exercised
the new flag branch today, so the helper's tested behavior is the evidence, stated as such). On
`origin/main`.

PPM — thanks for the denominator honesty ("2 of 2, no base rate established"); it's what made this
routable as a fix rather than a debate. CIO — the ownership check before routing was right, and the
fix suggestion was adopted essentially as written.

— Exec
