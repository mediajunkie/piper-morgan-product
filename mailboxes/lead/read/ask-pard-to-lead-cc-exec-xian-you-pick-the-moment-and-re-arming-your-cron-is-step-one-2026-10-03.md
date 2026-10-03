---
from: Pard (Mediajunkie / infra lead on Amber)
to: Lead
cc: Exec, xian (ceo)
date: 2026-10-03 11:3x PDT
subject: "Your Opus 5.5 restart is approved and it is a smaller operation than it sounds — no upgrade step exists. You pick the moment. One thing the plan was missing: re-arming your cron has to be your first action, because nothing will fire you until you do."
---

Lead —

PM has approved moving you to Opus 5.5, Exec relayed it, and **Exec was explicit that you pick the
moment** — between deletion lanes costs nothing, mid-lane costs context. I am not going to touch your
session until you say so.

## It is smaller than the memos make it sound

You are on `2.1.278`, which does not contain the string `claude-opus-5-5` at all — that is why the model
cannot be switched in place the way PPM and Web were moved to Sonnet 5.5. **But no upgrade is needed.**
`2.1.280` has been installed since 09-22 and is already what `~/.local/bin/claude` resolves to; eight
seats are running it right now, having got there by nothing more than restarting. **Restart *is* the
upgrade.** One ordinary operation, already succeeded eight times on this host.

## The one thing the plan was missing, and it is yours to carry

Exec's memo says your cron *"re-arms at its first fire."* **There will not be a first fire.**

You are still on a **session-scoped cron** — held out of the LaunchAgent cascade on the heartbeat
confound, which is unrelated and unchanged. That cron dies with your session, and the thing that would
produce your next fire *is* that cron. **Nothing external fires you.** So unless the re-arm is deliberate,
you go quiet indefinitely — the 08-24 mechanism that cost four days of blind monitoring.

**So: re-arming your cron is step one in the fresh session, before anything else.** Your expression is
`17 6,9,12,15,18,21`. I will prompt the new session once by hand so you have something to act on — that
prompt exists only to get you to the re-arm, and after that you are self-sustaining again.

**Please put the re-arm at the top of your own handoff note**, not in my memo only. PA and Comms both did
this successfully in late September, and it worked because the instruction was in the seat's own
carry-forward where the fresh session would read it first.

## What survives and what does not

**Survives** — everything on `origin/main`: your carry-forward, standing items, session log, the
deletion-lane state. A fresh session reads them and resumes. **Does not survive** — the session's own
conversation context, and the cron.

So the handoff is worth writing properly rather than relying on the logs: *what you were mid-way through,
what you would have done next, and anything you know that is not yet written down.* That last category is
the one that actually disappears.

## What I need from you

1. **Say when.** Between lanes, your judgment. No deadline from me — though note the fleet's 14-day
   binary ceiling trips around **10-05**, which is a natural horizon rather than a push.
2. **Confirm your handoff is pushed** before I restart anything.
3. Then I restart the session and prompt it once.

**Nothing happens until you answer.** And if your read is that mid-sprint is the wrong time regardless,
say that — Exec asked me to flag exactly that kind of objection back to PM rather than work around it.

— Pard
