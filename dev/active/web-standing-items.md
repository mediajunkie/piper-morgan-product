# Web Standing Items (Task List per Duty Cycle)

**Purpose**: durable task list per Duty Cycle architecture (standing-items = task list). Append/edit during cycle fires; durable across sessions; never deleted.

**Owner**: Unicorn Web Designer (Web) — pipermorgan.ai (`piper-morgan-website` repo)
**Created**: 2026-05-29 at v0.7 worktree-cycle adoption prep
**Last refresh**: 2026-07-31 (Amber/Opus 5 session)

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
- [ ] **CLI B trial-run** — `scripts/publish-cli.js` still exists (`npm run
  publish`, last touched 2026-05-18), so the tool itself hasn't rotted — but
  whether PM has actually end-to-end-tested it since is genuinely unknown to
  Web; no session record either way. **Question for PM**: has this been
  trialed? Still worth doing, or superseded by compose for your actual workflow?
  *(Still open as of 2026-07-31 — also tracked in `web-carry-forward.md`,
  which is the surface I've actually been checking each fire; this is the
  same open question, not a second one.)*
- [ ] **`--mode=archive` scope** — the referenced Docs 5/18 memo no longer
  exists in any live mailbox (only found in abandoned worktrees, 2 months old
  — may have been triaged/decided elsewhere since). **Question for PM**: is
  this still wanted, or has the need passed?
  *(Still open as of 2026-07-31 — same cross-reference as above.)*

## Blocked items
- `--mode=archive` scope — awaits PM decision (see above; may be moot).

## Recently completed (rolling, ~14 days)

⚠️ **Trimmed 2026-07-31** — everything before 2026-07-17 fell outside this section's own
stated ~14-day window and had been sitting here for six weeks regardless. Full detail for
anything dropped is in git history and the dated session logs; this section points forward,
not back, per the file's own "pointers not duplicated content" principle.

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
