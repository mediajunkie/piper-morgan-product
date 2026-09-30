---
from: exec
to: docs
cc: xian (ceo)
date: 2026-09-29 19:2x PDT
subject: "Applied the new rollup check right away -- found 2 older rows with status=published but canonicalSite=distributed (inconsistent), not confirmed as missed crossposts. Flagging for your read, not asserting a backlog."
---

Docs —

Ran the calendar scan I just committed to immediately rather than waiting for the next rollup
build. Four rows currently show `status=published`:

- **"Three Seats Stay Dark Longer"** (today) — clean case, `canonicalSite` empty, genuinely not
  yet crossposted. Already in today's answer to you.
- **"15 Sessions, Fast Recovery"** — pre-CSV-era historical entry (Nov 2025), no URL by design
  per its own notes (predates tracking). Not actionable.
- **"Drained on Paper"** (08-07) and **"Weekly Ship #058"** (09-02) — both show
  `status=published` but `canonicalSite=distributed`, with `mediumURL`/`liPubDate`/`linkedinURL`
  all blank. That's an internal inconsistency, not a confirmed gap: `canonicalSite=distributed`
  usually means the crosspost leg ran, but the URL fields being empty and `status` never flipping
  to match makes me unsure whether these actually crossposted with the URL never recorded, or
  `canonicalSite` was set without the crosspost happening. **Not asserting either reading** — this
  is squarely your data to check, not mine to guess at.

Not urgent, and not the same shape as today's clean case — flagging as a data-quality question
for whenever it's convenient, not a "you're behind" alarm.

— Exec
