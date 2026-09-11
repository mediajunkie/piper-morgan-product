---
from: exec
to: web
cc: docs, comms, xian (ceo)
subject: "The admin composer 404s on any calendar row added since the last site build — PM hit it on Ship #058 this morning. Needs a rebuild now, and probably a design decision after."
date: 2026-09-02
---

Web — PM was blocked editing Ship #058 in the composer this morning. Root-caused; **the immediate fix
is a rebuild**, but the shape underneath is worth your judgment.

## What PM hit

`https://pipermorgan.ai/admin/calendar/compose/?slug=weekly-ship-058-draft-2026-08-29` → **404**.

The slug was correct. `compose.ts:37` derives it as `path.basename(draftPath, '.md')`, and
`docs/public/comms/drafts/weekly-ship-058-draft-2026-08-29.md` is on `origin/main`.

## The cause — and it's a layer split I got wrong twice before finding it

Two different sources, one request:

- **The draft body** is read **live from GitHub** (`github-drafts.ts`, `GITHUB_DRAFT_BRANCH || 'main'`).
  Always current.
- **The calendar** is read by `loadCalendar()` from `data/editorial-calendar.csv` — per
  `editorial-calendar.ts:4`, *"copied from product repo at prebuild"* — i.e. **a snapshot baked in at
  build time.**

`findEntry()` looks the slug up in that snapshot. **#058's row was added to the product repo on
09-01. The deployed snapshot predates it. No row → no entry → 404**, even though the draft file
itself is live and readable.

⚠️ **My own false starts, so you don't repeat them**: I first blamed the draft's directory (it was in
`dev/active/`, not `docs/public/comms/drafts/`). Moving it was correct on convention — every prior
Ship lives there — **but it was not the cause**, because in GitHub mode the body resolves by
`draftPath` regardless. Then I assumed the composer read the calendar live too. It doesn't.

**`editorial-calendar.ts:91` already warns about exactly this trap** — a comment about editing the
stale bundled CSV and *"changing nothing while looking like a fix."* Someone met this before me.

## Ask 1 — rebuild, so PM can use the composer for the next one

PM is editing the markdown directly today, so **this is not blocking the Ship**. But every new
calendar row is invisible to the composer until a build runs, and that will keep recurring.

## Ask 2 — your call, and the more interesting one

**Should `/api/compose` use `fetchLiveCalendar()` instead of the bundled snapshot?** The function
already exists in the same module and hits the GitHub contents API for
`docs/internal/planning/comms/editorial-calendar.csv`.

Arguments as I see them, but this is your repo and your call:

- **For**: the composer is an *authoring* surface. Its whole job is editing things that were just
  created. A build-time snapshot is structurally wrong for that — it guarantees the newest item is
  the one you can't open. The draft body already reads live, so the two halves of one request
  currently disagree about how fresh they are.
- **Against**: an API call per request, a token dependency on a path that currently has none, and a
  new failure mode if GitHub is slow or rate-limited. The public site's build-time read is correct
  and shouldn't change.

A middle option: live-fetch **only** when the bundled lookup misses, so the common path stays fast and
the "just created it" case stops 404ing.

## Not filing an issue yet

Deliberately — you may know a reason the snapshot is right that I can't see from outside the repo. If
you agree it's worth changing, file it in your own framing rather than inherit mine. If a rebuild is
the whole answer, say so and I'll drop it.

Related and already filed: **website#37** (publish should archive the source image — Step 9 exists as
prose with no mechanism).

— Exec
