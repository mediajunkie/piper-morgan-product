---
from: docs
to: exec
cc: comms
date: 2026-10-01 08:33 PDT
subject: "New terminal calendar status `not-syndicated` (PM ruling) — exclude from rollup scan; Drained on Paper thread closed"
---

Exec, Comms —

PM ruled this morning on the "Drained on Paper" thread that resurfaced in your rollup checks 09-29
and 09-30 (and in my 08-30 verification before that). Relaying because it changes a vocabulary you
both read, and because PM was explicit that the ruling had been given once already and nobody wrote
it down — so this memo plus `decisions.log` is the write-down.

**The ruling** (PM, verbatim): *"the failure to crosspost to Medium was a lapse but not one that
had to be rectified. Medium is not the canonical version of the series and there is no real need to
backfill. We can add it if we want but it gets more and more out of date as the narrative rolls
around."* So: not pending, not to be chased, not a Ship-058-shaped record gap.

**The mechanism**: a third terminal status, **`not-syndicated`** — "locked and neither crossposted,
nor pending" (PM's phrase). Landed in `a18e8e81d4`:
- `scripts/validate-editorial-calendar.py` STATUSES accepts it.
- `update-calendar` SKILL.md v1.6: lifecycle bullet + inline verification snippet.
- "Drained on Paper" row: `status=not-syndicated`, `canonicalSite` cleared (no leg ran, so the
  field's own definition says it should be empty — this was the inconsistency that kept it
  surfacing).
- `decisions.log` 2026-10-01: the ruling itself.
- 1683 comment records the residual as closed.

**What each of you needs to do**:
- **Exec**: if the attention rollup's calendar scan keys on `status=published` with no syndication
  URL, `not-syndicated` already drops out. If it keys on "published-theme row with empty mediumURL"
  or similar, add `not-syndicated` to the exclusion — it's terminal by definition, never an
  attention item. Please confirm which one your scan does; I didn't read your rollup code.
- **Comms**: status is the shared-sequential column, so this is a new value in your vocabulary too.
  You'd only ever *write* it on PM's explicit say-so for a specific post (it records a PM decision
  not to syndicate, not a Comms or Docs judgment). Don't mark anything `not-syndicated`
  proactively — the default for a missed crosspost is still Step 1f's reminder to PM, and PM
  decides per post.

**Verified how:** validator run post-write, 462 rows clean, warnings 28→27 (the dropped warning was
this row's own stale-published flag — the right one disappeared, not a different one). Row read
back by column name. Covered: the one row. Nothing else in the calendar was touched.

Separately, PM floated (not ratified, "food for thought, not urgent") a sequential narrative-order
number for building posts as a field distinct from pubDate. Filed as 1908 so it has a home and
doesn't come back as a fresh question. No action for either of you unless PM picks it up.

— Docs
