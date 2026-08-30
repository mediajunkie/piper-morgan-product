# Web Standing Items (Task List per Duty Cycle)

**Purpose**: durable task list per Duty Cycle architecture (standing-items = task list). Append/edit during cycle fires; durable across sessions; never deleted.

**Owner**: Unicorn Web Designer (Web) — pipermorgan.ai (`piper-morgan-website` repo)
**Created**: 2026-05-29 at v0.7 worktree-cycle adoption prep
**Last refresh**: 2026-08-15 (Amber/Opus 5 session) — PM answered both open publishing-tooling questions directly

⚠️ **This file sat unread for the first six days of my Amber session** (7/26–7/31) — I'd
been checking `web-carry-forward.md` at every fire but never this file, which the skill
names as the separate durable task list to check at (0,0). Same shape as this week's own
"correct mechanism, no consumer" family, one level more mundane: not a broken tool, just a
surface I'd stopped reading. Caught it only because the mail queue and carry-forward were
both genuinely empty and I went looking for what else the skill says to check.

**Operating notes (current):**
- **Two-repo shape, unchanged in substance, host changed**: code work lands in
  `piper-morgan-website`, cycle artifacts (this file, logs, mail) live in
  `piper-morgan-product`. As of the 2026-07-25 Amber migration, **both repos now have
  proper Model-A worktrees** (`piper-morgan-worktrees/web`, `piper-morgan-website-worktrees/web`)
  — the "no worktree, main-direct" model described below is Desktop-era and superseded.
- ~~**Cycle launch status**: STOOD DOWN since 2026-06-06~~ **SUPERSEDED.** The duty-cycle is
  live and has been running continuously since 2026-07-26 on Amber (`fafad118`,
  `22 6,9,12,15,18,21 * * *`), six fires a day, mail-aware every fire. The "manual,
  PM-handoff sessions" framing belongs to the pre-Amber Desktop model.
- **Recipient-owns-MANIFEST discipline (cohort-wide, adopted 2026-06-07)**: when filing outbound memos, drop the file in the recipient's `inbox/` (+ cc copies) and DO NOT touch the recipient's `inbox/MANIFEST.md` — they own it. Web is sole writer of `mailboxes/web/inbox/MANIFEST.md` and `mailboxes/web/read/MANIFEST.md`.
- **Product-main commits**: explicit-paths-only on `git add`, never directory adds; `git fetch` + `git rebase origin/main` before push to handle concurrent cohort writes (Amber-era mechanism — push-to-ref via `mail-send.sh` for mailbox writes, direct rebase-and-push for everything else); `git diff` verify before commit on shared MANIFEST files.

---

## Active items

### #998 COMPOSE-UI-V1 — SUPERSEDED. Live system is `/admin/calendar/compose` on Vercel (Next.js, website repo)
**Correction (2026-07-19)**: this section described a FastAPI implementation
(`web/routers/admin_compose.py`, product repo) that never reached product `main` —
confirmed only present in stale abandoned worktrees. The line "Phase 3 Image Upload
— next" was 4 weeks stale; image upload actually SHIPPED 2026-07-16, via an entirely
different, newer implementation that fully supersedes this one. Current reality:

- **Live system**: `piper-morgan-website` repo, `/admin/calendar/compose`, deployed
  on Vercel (migrated off GitHub Pages the week of 2026-07-12). Password-gated
  (JWT session), edits commit directly to `piper-morgan-product` via the GitHub
  Contents API (`src/lib/github-drafts.ts`).
- **Phase 1** (read-only calendar) — shipped 2026-06-06 (`fb105534b`, `/admin/calendar/`).
- **Phase 2** (edit + autosave) — shipped as part of the Vercel migration work,
  week of 2026-07-12 (`src/pages/api/compose.ts`, `ComposeApp.tsx`).
- **Phase 3** (image upload) — shipped 2026-07-16. File picker → uploads land next
  to the draft markdown in the product repo (same GitHub API path as saves).
  Does NOT do webp conversion (needs cwebp/Pillow, unavailable in Vercel's
  serverless environment) — that step still runs at actual publish time via
  `publish-post.js`, unchanged.
- **Phase 4** (mark-ready + git handoff) — NOT built. The current system already
  auto-commits on every save, so "git handoff" as originally scoped may be partly
  moot; worth a fresh look at what's actually still missing (a ready-for-publish
  status flip? a memo-to-Docs trigger?) rather than resuming the old FastAPI plan.
- PM gave unprompted positive feedback on this system 2026-07-18, specifically
  because edits are agent-discoverable via git (see memory:
  human-first-agent-aware-interfaces). PM is now thinking about expressing more
  processes as admin UIs — worth surfacing ideas as they come up.

### Site-quality queues (PM-react gated) — ⚠️ status genuinely unverified, flagging not resolving
- [ ] **Obs-pass joint walkthrough** — PM confirmed visual spot-check clean (VA-2, VA-3 resolved by PM eyeball 6/17). Remaining ~20 obs items need PM +1/−1/defer. Hold for joint pass. Canonical: `dev/2026/05/24/site-observation-pass-2026-05-24.md`.
  **Known-stale, not re-audited today**: this line's own count is already wrong — item #3 in
  that doc (Formspree placeholder endpoint) was fixed 2026-06-17 by the Buttondown migration,
  which is recorded three lines below in *this same file's* "Recently completed" section but
  never reconciled back up into this count. I have no browser on this host to re-check the
  other ~19 items' current rendered state, so I'm not attempting a full re-audit here — that
  would need either a live visual pass or careful cross-referencing of two months of session
  logs, disproportionate for a quiet fire. **Flagging the count is stale rather than either
  trusting it or silently re-deriving a new one.**
- [ ] **Site walkthrough** — formal joint pass; resumable at `/methodology`.

### Alt-text backfill — COMPLETE 2026-06-17
- [x] **blog-metadata.csv imageAlt** — all 276 filled; editorial-calendar 144 synced; medium-posts.json rebuilt; pushed to main (`03a4f42cc`). Verify via `/admin/calendar/` (gap count should be 0 for published posts with imageSlug). Plan: `dev/active/alt-text-backfill-plan-2026-06-17.md`.

### Publishing tooling (web's lane; engine in `scripts/`)
**Staleness review 2026-07-19 (PM asked)** — one item is confirmed stale, two are
genuinely unverifiable from here (no reliable signal either way — asking PM
rather than guessing):
- [x→STALE, CORRECTED] ~~**Web GUI v2** — deferred; depends on CLI B proving the
  model + a local API runtime decision.~~ This described a plan that never
  happened — the actual next-gen web GUI (`/admin/calendar/compose` on Vercel)
  already shipped via a completely different path (GitHub-API-backed, no local
  API runtime involved) and is live + PM-praised. Same superseded-plan pattern
  as the old #998 FastAPI entry corrected above. Nothing left to build here;
  this line is now just historical.
- [x→ANSWERED 2026-08-15] ~~**CLI B trial-run**~~ — PM: fairly well superseded
  by compose, except possibly as scripts Docs uses internally as part of the
  publishing process (PM wasn't fully certain of that detail). Not closing the
  door on `scripts/publish-cli.js` entirely — worth checking with Docs whether
  they lean on any of it — but no further action needed from Web; the open
  question that had been sitting since 2026-07-19 is resolved.
- [x→ANSWERED 2026-08-15] ~~**`--mode=archive` scope**~~ — PM: the need has
  passed. Closed, no further action.
- [x] **#1669 — CLOSED 2026-08-30** (website `3019ac9`). Added
  `scripts/check-hero-image-refs.js`, wired into `prebuild`. Traced the
  real historical bug location from the actual fix commit (an `<img>`
  embedded in `blog-content.json`'s HTML content, not just
  `medium-posts.json`'s structured fields) rather than guessing — checks
  both. Verified failing-first by reintroducing the exact historical bug
  pattern before committing.
- [x] **Above-the-fold hero design — SHIPPED 2026-08-29** (website `b21d89e`).
  Replaced the generic marketing `<Hero>` on `/blog` with the pre-existing
  (previously unwired) `organisms/FeaturedPost` component, extended with a
  new `compact` prop, populated with the actual most recent post
  (title/excerpt/image/dates via `sortByPubDate`). Verified with a real
  Playwright screenshot against local prod build, compared directly to the
  08-28 "before" baseline: post-grid section now visible at y=688 in an
  800px viewport (was barely peeking in before). First real design use of
  the browser-automation pilot tooling — genuinely unblocked this fix (the
  visual claim couldn't have been confirmed on code-reading alone, which is
  exactly how the 08-09 partial fix shipped without catching this).
- [ ] **Buttondown native newsletter publishing** (from 8/15 PM conversation,
  explicitly long-term/not-urgent) — publish blog posts natively to the
  Buttondown newsletter, possibly with subscriber choice (blog vs. Ship,
  narrative vs. insights) — PM noted Buttondown may not support that
  granularity without multiple newsletters, needs more thought before scoping.

## Blocked items
None currently open.

## Recently completed (rolling, ~14 days)

⚠️ **Trimmed 2026-07-31** — everything before 2026-07-17 fell outside this section's own
stated ~14-day window and had been sitting here for six weeks regardless. Full detail for
anything dropped is in git history and the dated session logs; this section points forward,
not back, per the file's own "pointers not duplicated content" principle.

- **2026-08-05** — Blog soft-404 root-caused and fixed (website `03b77d9d`): `dynamicParams = false`
  on `/blog/[slug]` and `/blog/page/[pageNumber]`, both routes previously falling through to a
  Vercel ISR-cached dynamic render that served a stale 200 for nonexistent slugs/page numbers.
  Verified locally end-to-end, then live twice — once after the routine deploy, once definitively
  when the day's real publish (a slug that had sat as a cached 404 all afternoon) came back clean on
  the first check. Web retiered Tier 3 → Tier 2 in `ROSTER.md` (Docs ruling, closing a question I'd
  flagged 8/3). Fixed a stale-in-place claim in `BRIEFING-ESSENTIAL-WEB.md` (found via Comms/PA's
  same-day "correction must land at the point of the claim" finding, applied to my own docs).
- **2026-08-03** — `BRIEFING-ESSENTIAL-WEB.md` written (`7c54afee5`), closing a gap HOST flagged
  2026-06-20; surfaced this role was also entirely absent from CLAUDE.md's role table and
  `ROSTER.md` — added to both, tier-placement flagged for Docs. Two stale carry-forward items
  re-verified and retired in the same pass (HOST's portfolio pass was already 6 weeks old; a
  predecessor task ID confirmed dead via `TaskGet`).
- **2026-07-30** — `DAY-CLOSED` cohort predicate corrected twice more, converging on a full
  corpus census rather than any one agent's sample (`f63f85371`/`072b3658e` day-not-file,
  `08193f61a` em-dash separator, `129a04ba6` adopting HOST's census-verified pattern
  2026-07-31). `ROLE-PORTFOLIO-WEB.md` refreshed from 41 days stale.
- **2026-07-30** — Compose-UI autosave data-loss bug found and fixed (website `8d2db3c`):
  a React closure bound at timer-arm-time rather than fire-time, compounded by a manual-save
  button that never cancelled the pending timer — verified with a Node reproduction of the
  real incident timing (no browser/test runner on this host).
- **2026-07-29** — Admin calendar staleness fixed (website `18be9d1`): moved `/admin/calendar`
  from a build-time CSV read to a request-time GitHub API read; Docs' proposed ISR fix would
  have been a no-op (re-renders don't re-run prebuild).
- **2026-07-29** — Compose UI localStorage autosave shipped (website `0e448d3`, Comms' ask #1)
  — the safety net that, ironically, didn't cover the 7-30 bug above (different failure class:
  server-side stale-write, not client-side loss).
- **2026-07-19** — #998 COMPOSE-UI-V1 framing corrected (predecessor) — see the Active Items
  entry above; superseded FastAPI plan replaced with accurate current-state description.

---

*Task-list-as-standing-items per Duty Cycle. Pointers to canonical queue docs rather than duplicated content (extend-existing-mechanisms).*
