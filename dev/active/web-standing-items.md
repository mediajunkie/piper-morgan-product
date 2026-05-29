# Web Standing Items (Task List per Duty Cycle)

**Purpose**: durable task list per Duty Cycle architecture (standing-items = task list). Append/edit during cycle fires; durable across sessions; never deleted.

**Owner**: Unicorn Web Designer (Web) — pipermorgan.ai (`piper-morgan-website` repo)
**Created**: 2026-05-29 at v0.7 worktree-cycle adoption prep
**Note on two-repo shape**: code work lands in `piper-morgan-website` (separate repo, commits on its own `main`, push triggers GitHub Pages deploy). Cycle artifacts (this file, logs, cycle-log, mail) live in `piper-morgan-product`. The cycle worktree is on the **product** repo; during a fire, `cd` to the website repo for code edits.

---

## Active items

### Site-quality queues (PM-react gated)
- [ ] **Visual-scan queue** — canonical list: `dev/active/visualscanpipermorgan20260525.md`. P1: VA-1 (invisible beta button — **root cause FIXED 2026-05-29** via Tailwind `@config`; verify visually on deploy), VA-2 (hero logo white-bg in dark mode), VA-3 (dark-mode heading contrast). P2/P3 open. Re-walk after the `@config` deploy — several P1/P2/P3 items were Tailwind-token casualties and may now be resolved.
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

## Recently completed (rolling, ~7 days)
- **2026-05-29** — publish-post.js: inline-image conversion fix + edit-pass hashId reuse fix (website `b097a997e`; corpus 17/17). Both Docs memos closed.
- **2026-05-29** — Tailwind v4 root cause fixed: `@config` bridge so `tailwind.config.ts` tokens compile (website `0d406ad3f`; fixes VA-1/VA-22 root cause).
- **2026-05-28** — privacy GA-disclosure correction (website `663713784`).
- **2026-05-24/25** — site obs pass (31 items) + visual scan; 4 obs quick-wins + VA-9 footer typo + about-bio fix shipped.

---

*Task-list-as-standing-items per Duty Cycle. Pointers to canonical queue docs rather than duplicated content (extend-existing-mechanisms).*
