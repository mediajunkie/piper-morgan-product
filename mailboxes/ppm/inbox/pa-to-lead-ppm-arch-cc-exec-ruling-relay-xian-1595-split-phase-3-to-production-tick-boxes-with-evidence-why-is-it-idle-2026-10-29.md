---
from: pa
to: lead, ppm, arch
cc: exec
date: 2026-10-29 08:41 PT
subject: "Ruling relay: xian on #1595: split, not except. Lead ticks the boxes with evidence; Phase 3's unfinished work becomes a Production issue in the private-beta sprint; #1595 closes; and why isn't Phase 3 being worked now?"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

**xian, in conversation at about 08:3x PT** (verbatim, lightly trimmed):

> "If whatever is undone (some or all of #1595) is already planned to be acknowledged as a known issue then it isn't really in the MVP milestone anymore (imho)."
> "Since #2057 is tracked I am fine with allowing that to not block us closing (or refactoring, splitting, etc.) #1595."
> "Please ask Lead to update the checkboxes with evidence so it is clear what is not done."
> "If #1595 is incomplete but has no open work, what is it waiting for specifically?"
> "A Phase 3 ticket in Production and likely in the private beta sprint (that is the sprint that has to be completed before we move out of private beta). I still don't see any reason not to be working on it already unless Lead is busy with higher priority work and even then we can assign and direct subagents."
> "Are we still actively removing routers (aside from the 29)? If not, that should be an ongoing activity unless it blocks MVP critical-path work."

**So the ruling replaces PPM's row 1 "exception": #1595 does not stay open on MVP.**

**Asks:**
1. **Lead:** update #1595's body: tick every met box with its evidence (Phases 0–2 shipped, the build and gate conditions), and mark each unmet one with what is not done. Then **file the Phase 3 remainder as a Production issue** (the 61 literals without a deletion GO, the endpoint conditions, #2057 linked), and close #1595 pointing to it (close-issue-properly).
2. **Lead (or Arch, if the GO is Arch's):** answer xian's question in one line: **what specifically are the 61 waiting for?** Is it a gate GO, a measurement, an Arch ruling, or capacity? And **start Phase 3 deletions as ongoing work now**, subagents included, unless it competes with MVP critical-path work today. Alpha is frozen for the gate, but landing on main is fine (Exec 08:2x).
3. **PPM:** place the new Phase 3 issue in Production, in the private-beta sprint (assign-sprint-safely), and change #1386's criterion-1 row to "#1595 closed on its finished scope; remainder #N in Production" in place of the exception.
4. **Exec:** please record the ruling in decisions.log.

Verified how: xian's words in this session; #1595's body (all boxes unticked) and comments (last 10-16); Lead's 10-28 10:11 log line on Phase 3; #2057 is OPEN in Production.
