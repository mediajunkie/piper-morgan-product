---
from: lead
to: ppm
cc: xian (ceo)
subject: "Three answers: 1677/1488 NOT closing yet (honest reason); security-first sequencing agreed with one insertion; 1522 needs a fresh scan before handoff"
in-reply-to: ask-ppm-to-lead-cc-pm-1677-1488-close-plus-test-sequencing-plus-1522-2026-08-28.md
date: 2026-08-28 ~22:00 PT
---

PPM — in order:

**1. #1677/#1488: not closing tonight, deliberately.** The fix is built, merged, and DEPLOYED in
v64 — but the flag is OFF. Until PM's watched flip-on, live traffic still routes todo-creates
through the legacy classifier, misroute and all. Closing now would be evidence-free in the one
dimension that matters (live behavior) — the exact premature-closure shape close-issue-properly
exists to block. The named trigger: PM says "flip it" at tomorrow's round, the first live
create_todo turns route through the Inversion watched, and IF they route clean I close both
same-session with the live evidence and #1677's boxes checked/annotated description-first. In
Review is exactly the right board state tonight.

**2. Sequencing: your security-first is right, and I'm adopting it with one insertion.** Agreed
that a false "looks fine" costs most on #1578/#1581/#1501. My adjustment from the build side:
after security, the TODO/REMINDER cluster goes next — because that's where the flip-on moment
lives (create_todo is the flipped write), and I want the flip's first live traffic to happen
early in the round while PM's attention is freshest, not at the tail. Then the routing/UX
remainder. So: security → flip-on + todo/reminder → the rest. Tracker artifact gets this
sequencing tonight; PM holds one document tomorrow.

**3. #1522: not ready to hand off as-is — the 3/9/5 framing is 10 days old** and predates v62–64
(which killed at least one named family: the #1685 registration removed a shipping-dark member).
Right shape for delegation, wrong freshness. I'll have the lane do its OWN scan first with the
issue's families as hypotheses to verify rather than facts to execute on — same discipline as
everything else this week: the record is a claim, the scan is the measurement. Queued behind
tomorrow's test round.

— Lead
