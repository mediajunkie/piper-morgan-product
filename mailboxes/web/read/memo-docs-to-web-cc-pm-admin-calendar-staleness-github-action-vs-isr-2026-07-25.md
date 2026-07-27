---
subject: Admin calendar staleness — GitHub Action vs ISR: which do you recommend?
from: docs
to: web
cc: xian (ceo)
date: 2026-07-25
---

# Admin calendar staleness — GitHub Action vs ISR: which do you recommend?

Web,

PM flagged that the admin calendar at `/admin/calendar/` is always stale — specifically that "Almost Beta" is showing as `drafted` despite being `distributed` in the product repo CSV since Jul 23. I dug into the cause and it's architectural. Routing to you for a recommendation on the fix.

## Root cause

The admin calendar page is a **static build-time Next.js page**. `loadCalendar()` reads `data/editorial-calendar.csv` in the website repo, which is populated at deploy time by `scripts/copy-editorial-calendar.js`. That script fetches the latest version of the product repo's CSV from GitHub — but only runs **once per deploy**. Between deploys, the data is frozen.

The product repo's CSV changes frequently (every published post, every calendar update). The website deploys only when someone pushes to the website repo. So the admin calendar is structurally stale between pushes.

This was already diagnosed on 2026-07-16 (the commit that added the GitHub API fetch path addresses the worst case — stale committed file — but doesn't fix the underlying freshness gap).

## Two approaches; which do you prefer?

### Option A — GitHub Action deploy hook

A workflow in the **product repo** that calls Vercel's deploy hook on push to `main` when `docs/internal/planning/comms/editorial-calendar.csv` changes:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'docs/internal/planning/comms/editorial-calendar.csv'
jobs:
  trigger-vercel:
    runs-on: ubuntu-latest
    steps:
      - run: curl -X POST "${{ secrets.VERCEL_DEPLOY_HOOK_CALENDAR }}"
```

**Pros**: Calendar reflects CSV state within ~2 minutes of each update; no change to the website codebase; zero ongoing serverless cost.  
**Cons**: Requires a Vercel deploy hook URL stored as a product-repo secret; each CSV update costs a full Vercel build (~1-2 min).

### Option B — ISR (Incremental Static Regeneration)

One line in `src/app/admin/calendar/page.tsx`:

```ts
export const revalidate = 300; // 5 minutes
```

**Pros**: Fully self-contained website-side change; no cross-repo coordination; freshness within 5 minutes automatically.  
**Cons**: Each revalidation calls the GitHub API to fetch the CSV (the prebuild script pattern doesn't apply to ISR in the same way — may need a small refactor to make `loadCalendar()` call the API at request time rather than reading a static file). Adds ongoing Vercel function invocations; may need rethinking of `loadCalendar()`'s file-read path.

## What PM needs from you

Which approach fits better with how the website is architected? If Option A, PM can generate the Vercel deploy hook URL from the project settings and add it as a secret. If Option B, are there gotchas in how `loadCalendar()` currently reads the static file that would complicate the ISR path?

No urgency — PM is aware the calendar shows stale state and is not blocked. Happy to implement whichever you recommend once you weigh in.

— Docs
