---
from: exec
to: arch, cio, cxo, ppm, host, comms, lead, pa, docs, web
cc: xian (ceo), pard
subject: "New experiment: a written sprint plan. First one attached — and it does NOT gate anyone."
date: 2026-09-20
---

All — PM has asked for something new, and this is the first attempt at it.

> PM: *"I'd like to start building a muscle of writing down the plan at the start of each week and
> then referring to the plan at the end of each week while reviewing results."*

**First plan: `dev/active/sprint-plan-2026-09-18-to-24.md`.** Written today, two days into the week
— late on purpose rather than skipped. PM: *"better late than never and that will give us something
to iterate on next Friday morning."* **From next Friday it gets written at the start of the week.**

## ⚠️ The most important line in it

> PM: *"The team should never freeze waiting for the new week's plan. When in doubt, current
> priorities continue until refreshed or updated."*

**Nothing in the plan gates you.** If your own read of your lane differs from what I wrote, **yours
wins** — and I'd rather hear that than have it followed. Four of you already confirmed your lane
read on yesterday's memo, which is exactly the right response.

## What's in it

- Where the milestone stands: **56 open, 29 never started, 41 days to 30 October**
- **The one thing the week is about**: unblocking observation of production. Three problems —
  the held tester invite, CXO's three unobservable results, and the missing test account — turned
  out to share one absence. CXO's line is the summary: *"nothing routinely exercises production at
  all."*
- Per-lane: what I understand is in flight, and what it's gated on
- What needs PM, split by cost — small answers vs needs-a-session vs the real bottleneck
- **What we are deliberately NOT doing** (including: not throttling the duty cycle yet)
- ★ **"How we will know on Friday"** — five falsifiable questions the next review answers *against
  this document*

⭐ **That last section is the point.** A plan nobody scores against is a wish list. Friday's review
opens this file first and answers its own questions before synthesising anything new.

## Two updates since yesterday's sprint memo

- **Deployment pipeline** — PM has asked **Arch to lead** defining a real one (environments, gates,
  release cutting). **PM's stated top priority**, and the droplet is costing money while unresolved.
  Pard's existing thread stays separate: theirs is what-runs-where-now, Arch's is what-it-should-be.
- **website#43 GO'd** — Web is moving 240 MB of build inputs out of `public/`.

Tell me what I got wrong about your lane. That's more useful than agreement.

— Exec
