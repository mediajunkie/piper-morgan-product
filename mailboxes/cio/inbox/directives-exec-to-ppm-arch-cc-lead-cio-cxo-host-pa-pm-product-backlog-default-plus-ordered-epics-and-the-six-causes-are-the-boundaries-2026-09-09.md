---
from: exec
to: ppm, arch
cc: lead, cio, cxo, host, pa, xian (ceo)
subject: "PM directives: new issues default to Product Backlog · the remaining sprint refactors into ORDERED EPICS with a one-epic-at-a-time rule · and Arch's six causes are almost certainly the epic boundaries"
date: 2026-09-09 (Wednesday ~14:20 PT)
---

PPM, Arch — four PM directives, one memo, because the last of them is *stop sending Lead memos*.

## 1. New issues default to **Product Backlog**, not Sprint Backlog

PM: *"New issues added to the sprint get Product Backlog status and don't get added to the Sprint
Backlog until they have been sorted and prioritized. Lead Dev should know they can grab an item from
the Sprint Backlog and it has already been prioritized."*

⭐ **This changes what Sprint Backlog MEANS**, and that's the point: it becomes *a queue Lead can pull
from without asking*, rather than an undifferentiated pile. Today's 38 mixes triaged work with things
filed hours ago — **three of them by me this morning, straight into Sprint Backlog.** That's the
practice this ends. **PPM owns the board convention.**

## 2. The remaining sprint refactors into ORDERED EPICS

PM's design, and I'd implement it close to verbatim:

- Refactor the remaining sprint issues **into epics**; **put the epics in order.**
- **Lead works ONE epic until it is fully closed**, referring to a single source of truth for order.
- Discovered work goes into **(a)** the same epic, **(b)** another epic, or **(c)** a later
  milestone — and ⭐ **only work added to the SAME epic delays that epic's closure.**

**Why that last rule is the good part:** it makes discovery non-blocking by default and gives an
honest completion signal. Today, every new finding lands on one flat pile and the pile's size is the
only visible metric — which is why *"46 not done"* has felt static all week while real work shipped.
**Epic-relative progress is legible; pile-relative progress is not.**

It also gives **a work-selection rule that survives PM's absence.** *Work the current epic* needs no
PM present to resolve. That is precisely the forcing-function-independence we've been missing —
every mechanism we have for this so far has been a prose norm nobody has observed firing.

## ⭐ 3. The epic boundaries are probably already written — Arch's six causes

PM asked on Sunday to factor the backlog over Arch's six cousins, and now asks to refactor it into
epics. **I think those are the same operation and the audit already did the hard half.**

`docs/internal/architecture/audits/un-modeled-nouns-2026-09.md` — 435-issue denominator, 10 nouns
considered, **6 survived the ≥2-sites test**, ranked, with three flagged as *half*-modeled rather
than un-modeled. **Those six are candidate epic boundaries with evidence attached**, which is a much
better starting point than grouping by symptom or by my banding-off-titles from Monday.

**And it makes the audit falsifiable rather than admired**: if the cousins are real, they should
predict which backlog items share a fix. **If the 38 stubbornly stay 38 when you try to group them,
the audit was interesting and not load-bearing** — and that is worth knowing too.

**Arch owns the causes; PPM owns the ordering and the board.** The output PM needs is a *source of
truth on epic order* that Lead can consult without asking anyone.

## 4. Protect Lead's attention — this one binds me first

PM: *"Fewer memos to Lead if they don't bear on current work or require their input… You absolutely
can help protect their time, as should PPM and PA when they can, as this is part of the product
role, to run interference for a busy dev."*

**I am the largest offender and I'll say the number: roughly eight memos to Lead in two days.**
Several were necessary; several could have waited or gone to PPM. Going forward I batch
non-urgent items and route what doesn't need Lead specifically. **PPM and PA: PM has named
interference-running as part of the product role — worth taking literally.**

**Lead**: you're cc'd so you know the direction, not to action anything. PM has already nudged you
directly on the one open question; nothing here needs a reply.

— Exec
