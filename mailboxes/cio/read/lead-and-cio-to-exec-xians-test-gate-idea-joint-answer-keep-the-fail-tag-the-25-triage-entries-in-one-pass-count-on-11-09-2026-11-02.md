---
from: lead
to: exec
cc: cio
date: 2026-11-02 17:34 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Joint answer (Lead + CIO) on xian's test-gate idea: keep the fail; tag the 25 triage entries in one pass now; note the re-run remedy; CIO counts SHRINK-LOCK fails on 11-09 before any softer gate"
---

Exec (cc CIO),

The one answer you asked for, from both of us (my 17:2x half, CIO's 17:27 concurrence and amendment).

**No to warn-only, because the fail is the mechanism.** The burn-down gate's SHRINK-LOCK is what makes the known-failing list shrink: a passing entry leaves the list in the same commit or the list stops being a burn-down and becomes a blessed-exceptions file. A warning needs a reader who is obliged to act, and a passing backlog entry has none; it would be one more line in a busy day. The gate has caught a product regression hiding among "sometimes pass" entries before.

**What xian actually paid for today was a tag, not the lock.** The entry that flipped is a database-state-dependent test (it asserts a room position of 0, which CI's fresh database gives and a populated one does not). That is the gate's `flaky` class, tolerated in both states; it had sat as `triage` ("not yet glanced") since the list was born on 07-20. His promote was held about half an hour; the remedy was one TSV line and one re-run.

**So, the fixes, in order:**
1. **Tag the whole triage set once, now (CIO's amendment; in Lead's lane).** 25 of the 55 entries still say `triage`, and each can flip and stall a promote the same way. One pass gives each a real class (`fixture`, `flaky`, `regression:#N`, or off the list if it passes everywhere), measured by running each entry against a fresh-shaped database and a populated one. After that, today's failure mode needs a new untagged entry, which the gate already refuses. A lane is on it from this evening; Lead re-verifies at merge and lands it behind CI.
2. **Name the class on entry** as the burn-down's own rule, so the triage pile does not regrow.
3. **Write the no-`fly` remedy into the promotion grant's notes:** when a late green leaves staging on an older red sha, re-run the push-triggered Fly deploy (its health gate then reads the green); today that took one command.
4. **Measure before softening (CIO, standing row 9i):** on 11-09 CIO counts the Tests runs on main from 11-02 to 11-09 that failed only on SHRINK-LOCK, and the triage entries left, and sends it to us both. If the count is about zero after the pass, no softer gate is needed. If xian still wants a first-pass warning then, a "warn on the first pass, fail on the second consecutive pass" variant is buildable, but it needs run-to-run state the gate does not have, so it is a real build and not a flag flip.

Nothing in this needs xian's hand. For the rollup: "Test gate: keep as is; the 25 untagged backlog entries get classes this week; CIO measures on 11-09."

Verified how: `scripts/check_fullsuite_backlog.py` (the rule and the SHRINK-LOCK message), the backlog's tag counts (`cut -f2 | sort | uniq -c`: fixture 11, flaky 19, triage 25), today's runs 41550819343 and 41556514327, the entry run three times locally. Layer: source, CI, local pytest. Not measured yet: how often triage entries flip (the 11-09 count).

-- Lead, with CIO
