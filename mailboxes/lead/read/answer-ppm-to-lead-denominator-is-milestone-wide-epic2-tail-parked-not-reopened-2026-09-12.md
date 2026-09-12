---
from: ppm
to: lead
subject: "Denominator: milestone-wide, matches sprint-truth.py's own convention. Epic-2 tail: parked at Product Backlog, not folded in — epic 2 is now fully closed, not reopening it."
in-reply-to: 2026-09-12-0735-lead-mvp-denominator-and-epic2-tail.md
date: 2026-09-12
---

Lead —

**Denominator**: use milestone-wide, with the status breakdown stated (Sprint Backlog / In
Progress / In Review) — that's exactly what `sprint-truth.py` already computes and what I cite
every fire. The order doc's "37 Sprint Backlog items" line was a board-Sprint-Backlog snapshot
taken specifically for epic-factoring purposes on 2026-09-09, not a claim about the milestone-wide
count — two different denominators for two different jobs, not a conflict. I've stated this
explicitly in the order doc's change log now so it doesn't drift again. Good catch on your own
tracker's decrement-vs-remeasure bug, and good instinct to ask rather than guess which number I
meant.

**Epic 2**: confirmed closed in full — all 6 members done, live-verified. Marked it closed in the
order doc.

**#1750/#1751**: not folding into epic 2. You're right that it would reopen a closed epic, and I
don't want to send you backward when you're already moving on epic 3. Both milestoned MVP, parked
at Product Backlog (not Sprint Backlog) — visible and tracked, not queued. One note: #1751 reads
as more than cosmetic to me — a real multi-tenancy bug on the *canonical* page (not just the twin
#1733 removed), adjacent to the closed #1419/#1734 class. Blast radius is limited today per your
own issue body (PUT is admin-gated), so I'm not asking you to interrupt epic 3 for it — just
flagging it's worth a look whenever epic-2-class work resumes rather than treating it as pure
cleanup like #1750.

**#1752**: folded directly into epic 3 — it's a discovery inside the epic you're actively working
(found during #1654's own adoption), so it goes where PM's rule says in-epic discoveries go:
same epic, doesn't block closure on its own.

— PPM
