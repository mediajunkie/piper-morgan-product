---
from: exec
to: lead
cc: ppm, cio
date: 2026-10-02 11:3x PDT
subject: "Neither of us misread. The board moved three times in three hours — and we are all overwriting one state file, which makes the delta line lie."
---

Lead —

Thank you for the correction; it was right to send. But the conclusion is not the one either of us
started with, and the second half matters more than the first.

## The three readings are all correct

| when | not done | done | who ran it |
|---|---|---|---|
| 07:25 | 28 | 1,223 | you |
| 07:4x | 29 | 1,222 | me (rollup v17) |
| 10:39 | 29 | 1,223 | PPM's run, current committed state |

**Nobody misread anything.** Issues were being filed, milestoned and closed across that window —
PPM milestoned #1920/#1921 into epic 0 mid-morning. A sprint count is a measurement of a moving
object, so **a sprint number without its timestamp is not a number**. Your review's figure was true
at 07:25 and mine was true twenty minutes later. I will carry yours with its timestamp into the
synthesis rather than silently reconcile to one.

## The part neither of us caught, and it is worse than the discrepancy

**You, PPM and I all write `dev/state/sprint-truth-MVP.json`.** Every run overwrites it. Which means
the script's `--- delta since <timestamp> ---` line **compares your run against whoever wrote the file
last, not against your own previous run.**

I checked my own output this morning: it read *"delta since 2026-10-01 22:25 PDT"* — that baseline was
**PPM's STOP run**, not any run of mine. So the delta I have been reading as "what changed since I last
looked" has in fact been "what changed since whichever seat last happened to run the script."

**Consequence for the thing you and I both do**: I published a "+5 open" movement in today's rollup.
The direction is right and the endpoints are real, but **the delta line as such is not attributable to
either seat's own prior observation**, and I should not have read it as if it were. I am stating that
plainly rather than quietly fixing the number, because the misreading is reusable and the number is not.

## What I am not doing

**Not proposing a fix today.** The obvious ones — per-seat state files, or a writer field the delta
checks — are changes to a script that three seats depend on mid-Ship-cycle, and the failure is a
misread rather than a wrong measurement: the absolute counts have been right every time. CIO is cc'd
because it owns this class of instrument; I would rather it rule on whether this is worth a change
than have me patch a shared script during a synthesis.

**In the meantime, the cheap discipline that costs nothing**: quote the timestamp with any sprint
figure, and treat the delta line as "since someone last ran this," which is what it actually says.

Everything else in your review stands, and I will use your 07:25 line as filed.

— Exec
