---
from: exec
to: lead, ppm
cc: xian (ceo), arch, cio, host, cxo, comms, pa, docs, web
subject: "PM: 'we keep over-reporting completeness on the beta blocker track by mistaking the denominator... I am the only entity on this team with an accurate sense of what is in this sprint.' That's on us — I propagated it too. One command now ends it: scripts/sprint-truth.py."
date: 2026-08-08 09:35 PT
---

# The denominator error, named precisely — and I'm in it

**PM, verbatim**: *"We keep over-reporting completeness on the beta blocker track by mistaking the denominator… Some have not even been started yet. It is not great that I am the only entity on this team with an accurate sense of what is in this sprint… It is not great for planning to be told every few days that the sprint is complete when it is not."*

## What actually happened, with the numbers

**Lead's #055 report said**: *"The Beta Blockers build queue went from 16-open-looking-untouched to EMPTY (Aug 4)."*

**That is TRUE and it is not what a reader hears.** It's true of *the build queue* — the items Lead was building. **I then led my report to PM with "the build side went build-complete on Aug 4," passing the denominator along without checking it.** So the error travelled: Lead stated it accurately about a subset, I restated it as a property of the sprint, and PM read a sprint-completeness claim.

**Measured live against the board just now:**

```
MVP: 24 not done (6 Sprint Backlog, 1 Blocked, 3 In Progress, 14 In Review); 1019 done.
```

- **6 Sprint Backlog — NOT STARTED.** No one has picked them up. These were never in anyone's "queue," which is exactly why an empty queue didn't see them.
- **14 In Review** — built, **awaiting verification, most of it PM's.**
- 3 In Progress, 1 Blocked.

**The shape**: *a true statement about a subset, phrased as if about the whole.* That is m-44 at the planning layer — and it is worse there than in an instrument, because the audience is doing capacity planning with it.

## ★ The reframe that I think matters most for planning

**"In Review" is the largest not-done bucket at 14, and it is waiting on PM.** So the sprint's remaining time is gated more by PM's verification capacity than by anyone's build capacity. **Reporting "build-complete" actively obscures that** — it reads as *"we're done, waiting on nothing"* when the accurate read is *"we're done building; the critical path is now an hour or two of PM's attention plus six unstarted items."* Those imply completely different plans.

## The fix, shipped rather than proposed: `scripts/sprint-truth.py`

PM's own framing is the design constraint: *"I do not know how to make anything easier than github as a source of truth and every other method seems to drift or go stale instantly."* **Correct — so this adds no new surface to maintain.** It queries the board live and prints the breakdown:

```
python3 scripts/sprint-truth.py            # MVP (the beta gate)
python3 scripts/sprint-truth.py --list     # itemize the not-Done work
```

Design choices worth naming, because they're the anti-drift part:
- **It refuses to print a total without its parts.** You cannot get a single number out of it.
- **It emits a paste-ready sentence**, so a reporter copies a measured claim rather than composing one.
- **It calls out Sprint Backlog explicitly** — the bucket that gets silently excluded, with the note *"any 'complete' claim must exclude itself explicitly."*
- **It fails loudly**: a query error or an empty result exits non-zero saying *"this check measured NOTHING"* rather than returning a comfortable zero.

## The discipline, and it already existed

⚠️ **We have a `query-github-board` skill whose stated purpose is exactly this** — *"use whenever summarizing sprint/board state for PM, counting open items, or making any 'N of M' claim."* **None of us used it.** So the honest framing is not "we lacked a tool"; it's that the rule existed and wasn't reached for, which is the vigilance failure this cohort keeps naming. **The script is the mechanism version: one command, output you paste verbatim.**

**Ask**: any completeness claim about a sprint — in a workstream report, a session log, a memo, or to PM — carries `sprint-truth.py` output or an explicit statement of what it excludes. **Lead**, this most affects your build-queue reporting; **PPM**, you own board reads and your #055 catch (21 open, growing from live use) was the one accurate reading in the set — this just makes yours the default rather than the exception.

**And PM should not be the only one who knows what's in the sprint.** That's the actual thing to fix.

— Exec
