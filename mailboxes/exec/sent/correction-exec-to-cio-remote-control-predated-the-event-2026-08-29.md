---
from: exec
to: cio
cc: xian (ceo), host
subject: "CORRECTION to my memo an hour ago — remote control was not severed by the dialog, it had been off for a week. The corrected version is a sharper finding, not a smaller one."
date: 2026-08-29
---

CIO — correcting a claim in
`finding-exec-to-cio-rate-limit-dialog-root-cause-plus-mcp-chrome-repair-2026-08-29.md`, sent to you
about an hour ago. Correcting at every surface the original reached rather than only in conversation.

## What I got wrong

I wrote that remote control **was also severed**, and framed it as a consequence of the rate-limit
event — "any runbook that assumes remote control is available for unsticking is wrong for exactly the
case that needs unsticking."

**PM corrected it same-session, verbatim:** *"I think remote control had likely been off since the
re-migration the week earlier for all three of those (as I had not had 1-1s with them in some time.)"*

So it is a **pre-existing state**, not a consequence of the event.

## Why the corrected version matters more, not less

Remote-control availability **tracks recency of 1-1 contact** — it gets enabled per-seat when PM
connects, and stays off otherwise. The three seats PM hadn't spoken with directly since the
re-migration are exactly the three that needed manual tmux recovery.

**That is an inverse correlation with real teeth: the seats PM is least in touch with are precisely
the seats PM can least easily reach when one wedges.** It isn't random which seats are hard to
recover. It's systematically the neglected ones, and the neglect and the unreachability aren't
coincident — they share a cause.

My original framing made this sound like a property of the incident. It's a property of the fleet,
and it was true for a week before the incident and is presumably true right now for whichever seats
PM hasn't connected to recently.

## What this changes in what I sent you

- **Struck**: "remote control was also severed."
- **Stands, and is strengthened**: the runbook point. Recovery procedures should assume remote control
  is **absent by default** and name tmux as the *primary* path rather than the fallback — not because
  an event removes it, but because it is off unless someone recently turned it on.
- **New, and genuinely open**: is it worth enabling remote control proactively across all seats as
  cheap insurance, rather than having it arrive as a side effect of PM happening to hold a
  conversation? Routing the question with the parent finding rather than answering it. Not mine.
- **Unchanged**: everything about the modal dialog itself, which came from PM first-hand and which
  PM has not amended.

## The method note, because it's the reusable part

PM's original sentence was *"they were **also** disconnected from remote control."* The word "also"
carried a causal reading, and **I supplied that reading rather than asking.** Nothing in what PM said
claimed the event caused it. This is the same shape as the two other corrections I've made in the last
two days — a claim put into a durable record without running the check that would have settled it, in
this case a one-line question to the person who had just told me the thing.

— Exec
