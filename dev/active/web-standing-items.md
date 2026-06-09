# Web Standing Items (Task List per Duty Cycle)

**Purpose**: durable task list per Duty Cycle architecture (standing-items = task list). Append/edit during cycle fires; durable across sessions; never deleted.

**Owner**: Unicorn Web Designer (Web) — pipermorgan.ai (`piper-morgan-website` repo)
**Created**: 2026-05-29 at v0.7 worktree-cycle adoption prep
**Last refresh**: 2026-06-09 (housekeeping pass — cycle stand-down + cohort discipline updates)

**Operating notes (current):**
- **Two-repo shape**: code work lands in `piper-morgan-website` (separate repo, commits on its own `main`, push triggers GitHub Pages deploy). Cycle artifacts (this file, logs, cycle-log, mail) live in `piper-morgan-product` and commit directly to its `main` (no worktree — see below).
- **Cycle launch status (2026-06-09)**: STOOD DOWN since 2026-06-06 (PM "doppleganger" mental-model mismatch). The main-direct variant remains ratified as `cron-shape-experiments.md` row 5; the `claude/web-cycle` worktree was cleaned up 2026-06-09. See shelved cron prompt at `dev/active/web-cron-prompt-v0.7.md` for design content if revisited. Mail-awareness is manual (PM-handoff sessions) until the launch-gesture-drift PM↔CIO discussion lands.
- **Recipient-owns-MANIFEST discipline (cohort-wide, adopted 2026-06-07)**: when filing outbound memos, drop the file in the recipient's `inbox/` (+ cc copies) and DO NOT touch the recipient's `inbox/MANIFEST.md` — they own it. Web is sole writer of `mailboxes/web/inbox/MANIFEST.md` and `mailboxes/web/read/MANIFEST.md`.
- **Product-main commits**: explicit-paths-only on `git add`, never directory adds; `git pull --rebase --autostash origin main` before push to handle concurrent cohort writes; `git diff` verify before commit on shared MANIFEST files.

---

## Active items

### Site-quality queues (PM-react gated)
- [ ] **Visual-scan re-walk** — canonical list: `dev/active/visualscanpipermorgan20260525.md`. Tailwind `@config` deploy is LIVE (since 2026-05-29 `0d406ad3f`); VA-1 (invisible beta button) + VA-22 (alpha/beta orange) root-cause-fixed. **Action**: re-walk the live site with PM to confirm fix coverage; several P1/P2/P3 items were Tailwind-token casualties and likely resolved. VA-2 (hero logo white-bg in dark mode) + VA-3 (dark-mode heading contrast) still need attention.
- [ ] **Obs-pass queue** — canonical list: `dev/active/site-observation-pass-2026-05-24.md`. 25/31 awaiting PM `+1`/`-1`/`?`/`defer`.
- [ ] **Site walkthrough** — formal joint pass; resumable at `/methodology` (A–E order in the 2026-05-28 web log).

### Publishing tooling (web's lane; engine in `scripts/`)
- [ ] **CLI B trial-run** — PM still hasn't end-to-end-tested the enriched `npm run publish` flow.
- [ ] **`--mode=archive` scope** — awaiting PM approval (Docs 5/18 memo signal #6).
- [ ] **Web GUI v2** — deferred; depends on CLI B proving the model + a local API runtime decision.

### PM-side decisions (web blocked-pending)
- [ ] **Lint policy** — `react/no-unescaped-entities` (74 warnings): disable rule project-wide vs. mechanically escape. 10-sec PM call.
- [ ] **Formspree form ID** — held per PM "too distracted"; revisit post-Tailwind-deploy.

## Blocked items
- Lint policy + `--mode=archive` scope — both await a PM decision (above).

## Recently completed (rolling, ~14 days)
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
