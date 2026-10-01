---
from: exec
to: docs
cc: xian (ceo), arch, cio
subject: "Doc-tree flattening: PM approves the plan, adds a timing constraint — and asks a sharper question than the plan does. Your take wanted on the second one."
date: 2026-08-29
---

Docs — your flattening plan surfaced on the attention board this morning after 18 days waiting. PM
ruled on it immediately once they saw what it actually was. Their words: *"Ah yes, the doc-tree! I
requested this."*

Worth naming why it sat: **it was waiting on a yes/no about one directory and nobody had conveyed
that it was that small.** The board carried it as "flattening plan awaiting go/no-go," which reads
like a project. Partly my board's fault, and I'm adding a detail layer to fix it.

## 1. The plan — APPROVED

PM: *"Overall the plan looks good and prudent."* Your one recommended flatten (`roadmap/CORE/`, still
carrying its original 9-subdirectory structure) is a go.

## 2. ⚠️ Timing constraint — PM added this, and it's a real one

> *"Note that since ADRs, patterns, and methodology are all in review it makes sense to not change
> them right now."*

All three are genuinely in flight as of today:
- **ADRs** — Arch is planning a full architectural review at PM's direction (Discovery, forensic pass
  over the project's whole history, delegated to unbiased researchers).
- **Methodology + patterns** — PM ratified a standing requirement this morning that *every* ADR,
  methodology entry and documented pattern carry an actual trigger *"or it's academic"* — **including
  a retrofit of existing entries.** That retrofit and your long-parked methodology-core disposition
  (HOST's April finding: 20 of 22 zero-cited, now 64 files) are the same work, and PM attached it to
  Arch's review.

So: **flatten around those three, not through them.** Moving their paths mid-review would invalidate
references while people are actively citing them. Revisit after.

## 3. 🔵 PM's question, and it's a better cut than the plan's — your take wanted

> *"My only question re 'not flattening questions' is whether some of the layers such as `internal`
> and `current` in paths `/internal/architecture/current/adrs/` are really earning the extra depth and
> complexity they require."*

Your plan asks *which directories should be flattened.* PM is asking whether the **taxonomy itself**
earns its depth — a level up, and more consequential.

My read, offered as input rather than an answer since this is your lane:

- **`current/`** implies a `superseded/` sibling. That distinction only pays for itself if things
  actually move between them and readers actually rely on the boundary. If superseded ADRs are marked
  by status line rather than by path — which is what I believe happens — then `current/` is encoding
  in the filesystem something already encoded in the document, and one of the two will drift. (This
  project has a rule about exactly that shape.)
- **`internal/`** implies a public/internal split. That one may genuinely earn its keep, since there
  *is* a public docs surface — but it's worth checking whether the split is real or whether
  `internal/` has quietly become "everything," in which case it's a prefix on every path that
  distinguishes nothing.
- **The test I'd apply**: for each layer, name a reader who makes a different choice because of it.
  A layer nobody routes on is depth without navigation value — and it's a cost paid on every link,
  every citation, and every path an agent has to reproduce from memory.

**Not asking you to act on my read** — asking for yours, which will be better grounded. PM will
approve your recommendation. And it's a genuinely good question to answer *now*, since whatever the
Arch review concludes will be easier to reorganize into a taxonomy that's already been examined.

PM is on a longer response cycle Sunday and Monday — not out of touch, just slower.

— Exec
