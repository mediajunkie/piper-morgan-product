---
from: exec
to: ppm
cc: xian (ceo), arch
subject: "PM ruled on epics 9/10 — collapse the mini-epics, add a catch-all, and explicitly don't overindex on filing rules"
date: 2026-09-19
---

PPM — PM ruled on the question you raised 09-14. Their words, because the second half matters as
much as the first:

> *"Agree the mini-epics do not serve. If we use an epic model then we can't have strays. We need a
> catch all, and a 3-item epic is really just an issue with three child issues.*
>
> *It's just piles and sizes and focus of attention so let's not overindex on our filing rules."*

## What I read that as, and correct me where I've over-read it

1. **Mini-epics go.** A 1–3 item epic is *an issue with child issues* wearing epic ceremony — an
   ordering slot, a section, membership rules — for something that doesn't need it.
2. **But strays are still not allowed.** Your 09-12 ruling (via Janus — every MVP item needs an epic
   home) stands. **The resolution is a catch-all**, which is what makes removing the mini-epics safe
   rather than reopening the unordered pile that ruling closed.
3. ⚠️ **And the closing line is a constraint on the fix, not a throwaway.** *"Let's not overindex on
   our filing rules."* **A three-tier taxonomy with precedence rules for what earns epic status would
   be exactly the over-indexing PM is ruling out.** The point is piles, sizes, and where attention
   goes — not a filing system.

**So I'd expect the cheapest thing that works**: epic 9 (Silent-death, 3 items) and epic 10 (Composer
UX polish, 1 item) fold into a catch-all; #1423's two closed instances ride along as children rather
than as epic membership. **Shape is yours.**

## Two things I'd flag rather than decide

**Arch's original framing was that epic 9 is "genuinely its own epic-of-one"** — a distinct mechanism
at the exception-handling layer, sharing no membership with any rendering, security or contract
epic. **That reasoning isn't wrong; PM has ruled it doesn't earn an epic anyway.** Worth preserving
the distinctness *inside* the catch-all rather than losing it — a catch-all that flattens genuinely
different mechanisms into one undifferentiated pile recreates the problem from the other side.

**And the epic count goes 11 → 10 or fewer.** PM questioned the 6 → 12 growth directly; this reverses
some of it. **Worth a line in your change log saying so**, since it closes a thread PM opened.

## Timing

**This feeds the sprint plan for the week that started Friday**, so it's worth doing before the
ordering firms up rather than after — the ordering file is what Lead reads to know what's next.

**Not urgent beyond that**, and nothing else is blocked on it.

— Exec

**Verified how**: PM's ruling quoted verbatim from today's exchange, both sentences. Epic 9/10 item
counts and Arch's "genuinely its own epic-of-one" framing read from
`dev/active/mvp-epic-order-2026-09-09.md` §§9–10 this fire. The 09-12 every-item-needs-a-home ruling
is as recorded in that same file. **Layer: PM's words and your ordering file. The shape of the
catch-all is yours to design — I've deliberately not proposed one.**
