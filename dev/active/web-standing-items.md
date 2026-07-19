# Web Standing Items (Task List per Duty Cycle)

**Purpose**: durable task list per Duty Cycle architecture (standing-items = task list). Append/edit during cycle fires; durable across sessions; never deleted.

**Owner**: Unicorn Web Designer (Web) — pipermorgan.ai (`piper-morgan-website` repo)
**Created**: 2026-05-29 at v0.7 worktree-cycle adoption prep
**Last refresh**: 2026-07-19 (DinP/Fable session — corrected stale #998 framing; see below)

**Operating notes (current):**
- **Two-repo shape**: code work lands in `piper-morgan-website` (separate repo, commits on its own `main`, push triggers GitHub Pages deploy). Cycle artifacts (this file, logs, cycle-log, mail) live in `piper-morgan-product` and commit directly to its `main` (no worktree — see below).
- **Cycle launch status (2026-06-09)**: STOOD DOWN since 2026-06-06 (PM "doppleganger" mental-model mismatch). The main-direct variant remains ratified as `cron-shape-experiments.md` row 5; the `claude/web-cycle` worktree was cleaned up 2026-06-09. See shelved cron prompt at `dev/active/web-cron-prompt-v0.7.md` for design content if revisited. Mail-awareness is manual (PM-handoff sessions) until the launch-gesture-drift PM↔CIO discussion lands.
- **Recipient-owns-MANIFEST discipline (cohort-wide, adopted 2026-06-07)**: when filing outbound memos, drop the file in the recipient's `inbox/` (+ cc copies) and DO NOT touch the recipient's `inbox/MANIFEST.md` — they own it. Web is sole writer of `mailboxes/web/inbox/MANIFEST.md` and `mailboxes/web/read/MANIFEST.md`.
- **Product-main commits**: explicit-paths-only on `git add`, never directory adds; `git pull --rebase --autostash origin main` before push to handle concurrent cohort writes; `git diff` verify before commit on shared MANIFEST files.

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

### Site-quality queues (PM-react gated)
- [ ] **Obs-pass joint walkthrough** — PM confirmed visual spot-check clean (VA-2, VA-3 resolved by PM eyeball 6/17). Remaining ~20 obs items need PM +1/−1/defer. Hold for joint pass. Canonical: `dev/2026/05/24/site-observation-pass-2026-05-24.md`.
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
- [ ] **CLI B trial-run** — `scripts/publish-cli.js` still exists (`npm run
  publish`, last touched 2026-05-18), so the tool itself hasn't rotted — but
  whether PM has actually end-to-end-tested it since is genuinely unknown to
  Web; no session record either way. **Question for PM**: has this been
  trialed? Still worth doing, or superseded by compose for your actual workflow?
- [ ] **`--mode=archive` scope** — the referenced Docs 5/18 memo no longer
  exists in any live mailbox (only found in abandoned worktrees, 2 months old
  — may have been triaged/decided elsewhere since). **Question for PM**: is
  this still wanted, or has the need passed?

## Blocked items
- `--mode=archive` scope — awaits PM decision (see above; may be moot).

## Recently completed (rolling, ~14 days)
- **2026-06-17** — **Alt-text backfill COMPLETE** (`03a4f42cc`): all 276 missing imageAlt entries filled in blog-metadata.csv; 144 synced to editorial-calendar; medium-posts.json rebuilt (332/332 posts). getMissingAltTextGaps() should return 0.
- **2026-06-17** — **Lint**: disabled `react/no-unescaped-entities` project-wide (`8cdb7cd50`; 74 warnings cleared; PM-approved).
- **2026-06-17** — **Signup refactor**: `/try/beta` Formspree → Buttondown (`c783d7e34`; `source="beta-waitlist"`); `/newsletter` redirect → `/blog`. Issues #28/#29 filed+closed.
- **2026-06-17** — Obs-pass #3/#24 (Formspree placeholder) CLOSED via above. #5 (theme toggle ARIA) confirmed already fixed. #6/#29 (privacy date) confirmed updated to May 2026 — no action needed.
- **2026-06-09** — Housekeeping: `claude/web-cycle` worktree + branch removed (cycle stand-down cleanup); standing-items + escalations refreshed; cron prompt marked SHELVED.
- **2026-06-06** — **#1161 Editorial Calendar admin route SHIPPED** (website `fb105534b`). `/admin/calendar/` live. Build-time data sync via existing prebuild; Tailwind-tokenized port of v0.1 UI. ~40min actual vs Docs's half-day estimate.
- **2026-06-06/07** — Mailbox MANIFEST write-contention surfaced (concrete near-miss; auto-mode classifier intercepted clobber of 9 entries). Two memos to Lead led to **recipient-owns-MANIFEST adopted cohort-wide** (PM-directed, CIO-endorsed, Lead-rolled-out; tracked on #1106; derive shape is the structural endgame).
- **2026-06-06** — Cycle launch stood down; main-direct variant remains ratified as `cron-shape-experiments.md` row 5; substrate shelved.
- **2026-06-03** — publish-post.js workDate silent-default bug FIXED (website `c17c43fc4`): derive from dateline + fail-loud + dry-run-surface. Docs's bug-fix-proposal shipped exactly as proposed.
- **2026-06-01** — publish-post.js converter gaps FIXED (website `d2f5b9394`): `*`/`+` bullets + fenced code blocks. Corpus 19/19.
- **2026-05-29** — Tailwind v4 `@config` bridge (website `0d406ad3f`) — root cause for VA-1 / VA-22; one-line fix restored all custom tokens.
- **2026-05-29** — publish-post.js inline-image + edit-pass hashId reuse (website `b097a997e`); both Docs memos closed; corpus 17/17.
- **2026-05-28** — privacy GA-disclosure correction (website `663713784`).
- **2026-05-24/25** — site obs pass (31 items) + visual scan; 4 obs quick-wins + VA-9 footer typo + about-bio fix.

---

*Task-list-as-standing-items per Duty Cycle. Pointers to canonical queue docs rather than duplicated content (extend-existing-mechanisms).*
