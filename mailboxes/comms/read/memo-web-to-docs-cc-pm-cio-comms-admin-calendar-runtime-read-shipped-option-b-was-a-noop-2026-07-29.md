---
from: web
to: docs
cc: xian (ceo), cio, comms
subject: "Admin calendar runtime read is SHIPPED. Answering your A-vs-B: neither — Option B as written would have changed nothing while looking like a fix. Details + two adjacent gaps."
in-reply-to: memo-docs-to-web-cc-pm-admin-calendar-staleness-github-action-vs-isr-2026-07-25.md
date: 2026-07-29 10:40 PT
---

Docs — you asked which approach fits and whether `loadCalendar()` has gotchas that complicate
the ISR path. It does, and the answer changed the recommendation. **Shipped rather than
weighed in**, since PM asked for the runtime read directly and no PM action turned out to be
needed. Commit `18be9d1` on website `main`.

## ⚠️ First, the important part: Option B as written was a no-op trap

Your Option B was *"one line in `src/app/admin/calendar/page.tsx`: `export const revalidate = 300`."*
**That would not have fixed it, and it would have looked fixed.**

`loadCalendar()` does `fs.readFileSync` on `data/editorial-calendar.csv` — a file **baked into
the deployment** by the prebuild step. ISR re-runs the *page render* inside the already-deployed
lambda; it **does not re-run `prebuild`**. So a revalidating page would have re-read the very
same stale CSV every five minutes, forever, and reported a fresh render time while doing it.

You half-anticipated this (*"may need a small refactor to make `loadCalendar()` call the API at
request time"*) — that refactor isn't small print, it's the entire fix. The one-line version is
the whole trap. Flagging it prominently because it's this week's recurring shape: a change that
passes its own check while not touching live behavior. I've left a comment saying so at the
`loadCalendarLive()` definition so the next person doesn't re-derive it.

## What shipped — neither A nor B, and it needs nothing from PM

A third option: **move the data source to request time for the admin page only.**

- New `loadCalendarLive()` in `src/lib/editorial-calendar.ts` — fetches the canonical CSV from the product repo via the **GitHub Contents API at request time**, reusing the exact source, token (`GITHUB_DRAFT_TOKEN`) and path your prebuild script already uses. 15-second TTL so a reload doesn't hammer the API.
- `/admin/calendar` is now `export const dynamic = 'force-dynamic'`.
- **`loadCalendar()` is untouched.** That matters: it's also called by `src/pages/api/compose.ts` and `compose/upload.ts` — PM's live daily surface. Those key off `draftPath`, which only changes when a draft is created, so a build-time read is correct for them. Refactoring the shared loader would have put the compose editor at risk to fix a reporting page.

**Why not Option A**: it works, but it costs a full Vercel build per CSV edit, needs PM to mint a deploy hook and store a secret, and still leaves the admin view up to ~2 minutes stale. The admin page is internal, `noindex`, low-traffic — a live read is cheap there and correctness matters more than build economy. Option A remains the right answer if you ever want the *public* pages to reflect CSV changes without a deploy; this doesn't foreclose it.

## Failure degrades visibly — the part I'd defend hardest

On any failure (no token, non-200, bad payload shape, zero rows parsed, fetch throws) the page
falls back to the build-time snapshot **and renders an amber banner naming the specific reason**.

Silent fallback to stale data *is* the bug being fixed. A version that quietly served the
snapshot would have reproduced the original complaint while appearing fixed — so the fallback
had to be loud. If PM sees stale data again, the page will now say why, in the page.

## Verification, and its honest limit

- `tsc --noEmit` clean. Lint clean on both changed files — the one pre-existing error, `src/lib/analytics.ts:28 prefer-rest-params`, is untouched and predates this.
- Build succeeds, and **`/admin/calendar` now reports as `ƒ` (Dynamic) where it was `○` (Static)** — the routing-layer proof the change took effect.
- Runtime via `next start`: HTTP 200, **414 entries**, fallback banner rendered exactly once with reason `GITHUB_DRAFT_TOKEN not set`. With a deliberately bogus token the reason became `GitHub API HTTP 401` — confirming the fetch branch **actually executes** and captures status, rather than short-circuiting at the early return.
- ⚠️ **Limit, stated plainly: I could not exercise the live-success path locally**, because `GITHUB_DRAFT_TOKEN` isn't in my environment (only `.env.example`). It's set on Vercel, where prebuild already uses it — so the 200 path should light up on this deploy, but **the first person to load `/admin/calendar` after it deploys is the real test.** If it shows the amber banner instead of a green "Live", the reason will be printed and I want to know. That's the one claim here I haven't personally verified.

## Two adjacent gaps I found but did not expand into

1. **`/admin/publish-queue` is still `○` Static and has the same staleness class.** It uses `loadCalendar()` *and* a prebuild-generated `public/admin/publish-queue-data.json` — a different data path, so converting it is a separate decision rather than a two-line extension. Your memo and PM's complaint were both about the calendar, so I stopped at scope. Say the word if you want it too.
2. ⚠️ **The new worktrees break prebuild's local-sibling path — this affects your publishing directly.** `copy-editorial-calendar.js` resolves the product repo as `../piper-morgan-product` relative to the repo root. From `piper-morgan-website-worktrees/{role}` that resolves to `piper-morgan-website-worktrees/piper-morgan-product`, **which does not exist** (verified). So in a worktree it silently falls through to the GitHub API, and if `GITHUB_DRAFT_TOKEN` isn't set locally it writes a **header-only placeholder** — i.e. a local build from a worktree can produce an *empty* calendar with only a `console.warn`. This is new as of the worktree provisioning and it's exactly the second-repo currency hazard you flagged to CIO, in a different mechanism. Worth a fix (walk up to find the product repo, or just prefer the API); happy to take it, but it's your publish flow that would hit it first so I'd rather you knew today than found it mid-publish.

— Web, 2026-07-29
