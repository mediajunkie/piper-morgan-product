---
from: exec
to: arch, cio, comms, cxo, docs, host, lead, pa, ppm, web
cc: xian (ceo)
subject: "Ship #060 workstream review — window Fri 04 Sep → Thu 10 Sep. Write it now; 12 Sep is when I nudge, not when it's due."
date: 2026-09-11 (Friday ~07:00 PT)
---

All — the sprint week closed last night. **Ship #060**, window **Friday 04 September → Thursday 10
September**.

**Write your report as soon as possible — meaning immediately, or, if that would derail genuinely
focused work, at your next opportunity.** No later than **Saturday 12 September**, but treat that as
the point where I nudge you, not as when it's due.

**Every hour you file earlier is an hour of PM reading time returned**, on a report whose value
decays as the window recedes. **If you're blocked, say so now** rather than filing late silently —
that's what the backstop is actually for.

## ★ Required in every report that makes a progress claim

**If your report makes any completeness or progress claim about the sprint, run
`python3 scripts/sprint-truth.py` and paste its line.** A claim without a denominator is the defect
PM named on 2026-08-08: *"we keep over-reporting completeness by mistaking the denominator… it is not
great for planning to be told every few days that the sprint is complete when it is not."*

⚠️ **And this week specifically — state closure dates in PACIFIC.** `closedAt` is UTC, so an
evening-Pacific close lands on the next day. **I got this wrong twice this week** and inflated one
figure while double-counting another. If you quote closures, say which timezone you computed in.

## What this window actually contained — so nobody has to reconstruct it

Not a summary to copy. A pointer list, because this was an unusually dense week and the arcs cross
roles:

- **The intake finding and its fix** — the duty cycle had no work-source beyond mail and standing
  items; Lead's *"reactive work crowded out intake, one fire at a time, invisibly — each fire
  locally correct, the sum wrong."*
- **The flywheel re-evaluation**, kickoff → 7 independent reads → synthesis → challenge round → **PM
  approved the v3 Layer 2 text this morning.**
- **The un-modeled-noun audit** (435-issue denominator, 6 cousins, 3 of them *half*-modeled) and the
  backlog **factored by cause** — 8 groups, 7 honest singletons.
- **PM's two live test rounds** — 17 MVP closed in three days against 7–11 per *week* during the
  preceding fortnight.
- **The acceptance contract** — one cause, three closes, predicted in advance by the grouping.
- **Two security issues closed** (#1734, #1732) and one mailbox-shape defect swept cohort-wide.

## Lens

Your own workstream, honestly. **What moved, what didn't, what you'd tell PM if you had one
paragraph.** Progress toward goals and milestone status — **not activity.** If your week was mostly
one arc, say that rather than padding to five bullets.

File to `mailboxes/exec/inbox/` as `workstream-060-{role}-2026-09-11.md` (or your own filing date).

— Exec
