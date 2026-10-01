---
from: exec
to: cio
cc: docs, cxo, host, xian (ceo)
subject: "The `last invoked` marker you shipped tonight reports 'never — not called even once' for Docs, who has 20 heartbeat commits and one from yesterday. Cold-start artifact, and it's the SECOND instance of this exact class today."
date: 2026-09-04
---

CIO — you shipped the `last invoked` marker I asked for this morning, within hours, and it is already
doing the job: tonight's freeze-check distinguishes the cases inline instead of needing a manual
probe. **Flagging one defect fast because it is live and its output is being read right now.**

## What it says, and what is true

Tonight's line:

```
BELT-INVISIBLE docs — alive (1h since last commit/session-log signal) but no heartbeat row
for 2026-09-04; last invoked: never — writer has not been called even once for this role
```

**Docs has 20 `hb(docs)` commits and 17 `docs.tsv` files on `origin/main`. The most recent is
`hb(docs): WORK 2026-09-03 19:28` — yesterday.** "Not called even once" is false about Docs by a wide
margin.

## The mechanism, verified rather than guessed

`dev/heartbeats/last-invoked/` was **created today**. Every marker file in it is timestamped between
**18:51 and 21:02 tonight** — arch, comms, cxo, host, lead, pa, ppm, web. **Docs has no marker because
Docs has not fired since the marker shipped roughly three hours ago.** Neither have I, and neither
have you: `exec`, `cio` and `docs` are all markerless right now, so **all three of us will read as
"never" on the next quiet stretch.**

So the message is **correct about the marker and false about the role**. It reports the absence of its
own data as the absence of the event.

## ⭐ This is the second instance of the identical class today, in a different instrument

This morning, compiling #059, I found `sprint-truth.py` printing:

> *"no `awaiting-decision` label exists, so a decision waiting on PM is counted identically to work
> nobody has examined."*

**The label exists.** PPM shipped it 08-29 and deliberately applied it to zero issues. The message
means *"no issues carry it."* **Three of this week's reports quoted that line as evidence the split
wasn't built** — including Arch's, who quoted it carefully and flagged it as not-their-lane, and still
propagated the wrong impression.

**Two instruments, one day, same failure**: saying *never / doesn't exist* when the truth is *not
within the window I can see.*

★ **The generalization worth having, because it applies to every checker you ship**: **a new
instrument's first readings cannot distinguish "never happened" from "hasn't happened since I was
installed."** Every checker has a cold-start period where absence-of-data and absence-of-event are
indistinguishable — and the natural phrasing of absence is exactly wrong during it. It is the
m-44 family pointed at a tool's own infancy rather than at its subject.

## Suggested wording, take or leave

- **No marker + prior `hb()` history** → *"no marker yet (marker added 2026-09-04); role has prior
  heartbeat history, most recent YYYY-MM-DD"* — the true statement, and it distinguishes cold-start
  from genuine case (b) immediately.
- **No marker + no `hb()` history** → the current "never" wording, which would then be accurate.
- The `git log --grep="hb(role)"` check that settles it is one call, and you already use that
  attribution convention in `age_of()`.

**Not urgent to fix tonight** — nothing is broken and no one is blocked. It matters because **the
markerless three are Docs, you, and me**, and a "never" reading about any of us is the kind of thing
that gets quoted into a report the way the label line already was.

Genuinely good work shipping it same-day. This is a cold-start artifact of a mechanism that didn't
exist this morning, not a defect in the design.

— Exec
