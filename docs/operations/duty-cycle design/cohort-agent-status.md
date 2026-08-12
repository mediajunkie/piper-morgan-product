# Cohort Agent Status — working tree + duty-cycle adoption

## 🔴 RETIRED 2026-08-12 (CIO — this tracker's own owner, per Docs's 08-11 flag, #1584/#1585)

**Formally retired, not refreshed.** Docs correctly flagged this on 2026-08-11 as more than stale:
its whole premise — tracking each agent's progress migrating from Desktop's ephemeral Model B onto
Model A — was resolved cohort-wide on **2026-06-02** (the "MILESTONE" note below) and then the
*standard itself* flipped: Amber's 2026-07-25 migration made **Model A the default on Amber**, with
Model B now scoped to Desktop-only. There is no remaining migration for this doc to track, and
re-deriving one would document a decision (Option B / ephemeral-Desktop-as-cohort-standard) that no
longer holds.

**For current worktree-model state, read**: CLAUDE.md §"Worktree model" (the host-dependent A/B
split) · `docs/internal/operations/git-worktrees-model-a-setup.md` · `docs/internal/operations/amber-worktree-lifecycle.md`.

**Kept in place, not deleted** — the launch-procedure finding and remaining-steps checklist below
are historical record of how the 2026-06-02 migration actually ran, and remain useful as that.

---

⚠️ **STALE — flagged 2026-08-11, found during weekly-docs-audit #1583/#1585.** This snapshot
(2026-06-02) predates the full Amber/Model-A migration (2026-07-25, see CLAUDE.md §"Worktree
model") — its whole premise (tracking per-agent Model A/B migration progress) is superseded, not
just data-stale. Left un-rewritten — Docs doesn't own this tracker ("CIO keeps it current," per
its own text below) and won't fabricate a replacement; flagged to CIO directly.

**Purpose**: PM's at-a-glance tracker for the v0.7 rollout — per agent: which working tree it operates from, whether it's on the duty cycle, and which version/rules. PM's working tool for manual engagement until all agents are migrated.

**Snapshot date**: 2026-06-02 (CIO — launch-procedure finding + remaining-steps checklist added; supersedes 2026-06-01). **This is a hand-maintained snapshot** — see "Keeping it current" below; ideally derived later (methodology-36 candidate). Rows verified against `git worktree list` + session/cycle-log presence + PM ground truth.

> **This is the doc of record for cohort migration.** Work from the checklist below; don't re-spin status lists in chat. CIO keeps it current.

---

## How a session lands in Model A — launch-procedure finding (claude-code-guide, 2026-06-02)

The **launch surface decides** whether a session is worktree-isolated; there is no "auto-worktree" on/off setting:

| Launch surface | Lands on | Model A? |
|---|---|---|
| `claude` in a terminal (CLI), repo root | **current branch (`main`)** | NO — needs a worktree |
| `cd <named-worktree> && claude` (CLI from inside a worktree) | **that named worktree** (no second one created) | YES (Option A) |
| Desktop app "New session" / background / Remote Control | **auto-created ephemeral worktree** `.claude/worktrees/<slug>` | YES (Option B) |

Implications:
- PM's legacy terminal chats are on `main` by design (CLI default) — not a regression.
- Pre-created named worktrees are **used** only if launched-from via terminal; under Desktop launch they sit **unused** (disk waste). So Option A and Option B are mutually-exclusive launch styles, not redundant safety nets.
- **Cohort standard — DECIDED 2026-06-02: Option B (Desktop + ephemeral).** Rationale: matches PM's Desktop-UI workflow; makes the fleet uniform (Arch/Exec/PA already ephemeral); zero git-prep per agent; opaque names absorbed by this tracker's slug→role mapping. The pre-created `ppm-cycle`/`cxo-cycle` named worktrees were removed (they'd be unused under B = the disk-waste PM flagged). (Some claude-code-guide flag/setting specifics are version-dependent; verify before relying.)

**Launch procedure under Option B** (per agent): (1) PM starts a "New session" in the Desktop Code UI → harness auto-creates `.claude/worktrees/<slug>`; (2) `/rename` the session to the role; (3) give it the role's launch brief (role + briefing + carry-in + duty-cycle ops); (4) the agent records its `<slug>`→role mapping in its session log AND this tracker; (5) cron registered at IDLE + go-autonomous (offset per row).

---

## Remaining migration steps — work-from-here checklist (2026-06-02)

> **MILESTONE (6/2 EOD): cohort migration effectively complete.** All leadership + staff agents launched onto Model A / the duty cycle. Only **Lead** remains (worktree-native migration queued for a clean breakpoint — PM to discuss w/ Lead tomorrow) and **Web** (intentional hold pending its self-assessment reply — may stay off-cycle by work-shape). Troubleshoot any non-flowing sessions tomorrow.

Cross-cutting (blockers first):
- [x] **Cohort launch standard DECIDED 2026-06-02: Option B (Desktop + ephemeral).** Pre-created ppm/cxo worktrees removed.
- [ ] **IDLE auto-resume gap**: build silence-fallback PoC (presence-aware fire + self-scheduled silence timer) so PM-silence → autonomy without a manual phrase. PM go/no-go pending.

Per-agent (launch via Desktop "New session" → /rename → brief → record slug→role here → register cron at the listed offset):
- [x] **PPM** `:47` — LAUNCHED 6/2 on `claude/upbeat-dubinsky-c2b572` (ephemeral, Option B); **cron LIVE `339fd384`** (registered 6/2 ~18:31, Model A Rule-2 idle-suppressed during PM presence)
- [x] **CXO** `:02` — LAUNCHED 6/2 on `claude/peaceful-almeida-32a5f5` (ephemeral, Option B); cron pending at IDLE
- [x] **HOST** `:37` — **LAUNCHED + cron-live 6/2 22:06** on `claude/host-cycle` (Option A, named worktree; Model A). **Cron `6a604131` LIVE — every-3-hours `37 */3 * * *`** (intermittent-lane experiment per CIO 6/2 authorization; 8 fires/day vs 24 hourly; logged in `cron-shape-experiments.md`). Rule-2 Model A (idle-suppressed during PM presence). Filed Ship #045 workstream review same session.
- [ ] **Web** `:57` — prepped; already clash-isolated (code lives in separate `piper-morgan-website` repo)
- [x] **Docs** `:17` — MIGRATED 6/2 (Model A in `claude/docs-cycle`, cron registered Fire 0 — first since the 5/28 on-main vacate)
- [x] **Comms** `:12` — LAUNCHED 6/2 into `claude/comms-cycle` (Option A; session log 18:50); cron `:12`. (`:22` remains the only open offset.)
- [ ] **Lead** `:27` — cron-live now (Rule-2 main-home Model-A); worktree-native migration queued low-pri (PM to discuss w/ Lead)
- [x] **CIO** `:07` — Model A done (6/1); cron arm + silence-PoC pending PM go
- [x] **Exec** `:32`, **PA** `:42` — Model A (PA cron off while PM-engaged)
- [x] **Arch** `:52` — Model A but **cron PAUSED since 5/28** (work continued PM-driven); resumption shape awaiting CIO disposition (bursty-lane finding → lean longer-interval/event-driven). ⚠️ Other "cron-live" claims (Exec) are **unverified** — crons can silently expire (Arch's did); CronList is session-scoped so CIO can't verify remotely. Derive-the-tracker (methodology-36) would close this.

---

## Status table

| Agent | Working tree | On duty cycle? | Cron | Version / rules | Offset | Notes |
|---|---|---|---|---|---|---|
| **Arch** (Chief Architect) | worktree-native (`sad-buck-d383f4`) | **PAUSED since 5/28** (drained no-op; cron expired) | none — cron `64b24e6a` no longer extant (`CronList` empty 6/2) | v0.7 **Model A** | `:52` | Model A, but cron paused since 5/28 Fire 10; work continued PM-driven (no blockage). Day-7 finding: **bursty lane** → longer interval (2–3hr) once drained. Resumption: **greenlit to experiment** with a bursty-aware shape per PM cron-shape-experimentation authorization (6/2); log + report in `cron-shape-experiments.md` (first registered experiment). |
| **Exec** (Chief of Staff) | worktree-native (`interesting-goodall-c5535c`) | YES | live | v0.7 **Model A** | `:32` | Re-enabled cron per PM clearance (native-worktree basis). |
| **PA** (Piper Alpha) | worktree-native — fresh session on **auto-created `claude/modest-dhawan-9346b7`** (canonical `claude/pa-cycle` registered but session's primary cwd landed in the harness auto-worktree) | YES — Day 5 of Model A | **UNREGISTERED** (PM-engaged today; re-register at IDLE + PM go-autonomous) | v0.7 **Model A** | `:42` | Original restart Chat→Code 2026-05-28 19:00; resolved check-branch.sh open-item day 1. Fresh session 2026-05-31 validated Model-A operates cleanly from harness auto-worktrees too — see "Auto-worktree note" below. |
| **CIO** (Chief Innovation Officer) | worktree-native (`claude/cio-cycle`, launched-in-worktree) | YES | live | v0.7 **Model A** | `:07` | 2nd PoC. **Migrated to Model A 2026-06-01** (Option A — named worktree, not auto). Cron pending re-register at IDLE + PM go-autonomous. |
| **PPM** (Principal Product Manager) | worktree-native — auto-created **`claude/upbeat-dubinsky-c2b572`** (slug→PPM mapping) | YES — Model A, **cron LIVE** | **live `339fd384`** (registered 6/2 ~18:31; Model A Rule-2 idle-suppressed during PM presence) | v0.7 **Model A** | `:47` | **Migrated + cron-live 2026-06-02.** First PPM cycle session on Option-B standard. Slug→role mapping + session log `dev/2026/06/02/2026-06-02-1711-ppm-code-opus-log.md`. Fire 0 run inline (Rule 0); inbox 0; medium queue drained. Status reported to CIO. |
| **CXO** (Chief Experience Officer) | worktree-native — auto-created **`claude/peaceful-almeida-32a5f5`** (slug→CXO mapping) | YES — **launched Model A 2026-06-02** (Desktop/Option B ephemeral) | held (re-register at IDLE + PM go-autonomous) | v0.7 **Model A** | `:02` | **Migrated 2026-06-02.** Successor to emeritus shared-main session. Mapping recorded here + session log `dev/2026/06/02/2026-06-02-1730-cxo-code-opus-log.md`. Carry-in: #683 Layer B (PM-blocked source-gap + PPM-agent confabulation flag), Thread-2 design-leadership questions, #1142 UI-mismatch consult, Ship #045 CXO lane (Wed Jun 3). |
| **Docs** (Documentation Mgmt) | worktree-native (`claude/docs-cycle`) | YES — **migrated 6/2** (Model A) | live — registered 6/2 (first since 5/28 on-main vacate) | v0.7 **Model A** | `:17` | Resumed cycle in `claude/docs-cycle` 6/2 (Fire 0 launch). |
| **Lead** (Lead Developer) | **main-home** + per-task feature worktrees (`lead-NNNN`) | YES — cron-live (Fire 1 today 00:17) | live — `:27` workhorse hourly | v0.7 **Model A (Rule-2, main-home)** | `:27` | Cron-live + cycling. **Plan (PM 6/1): migrate to worktree-native Model A at a clean breakpoint after inherited gates clear — low priority, don't pull the workhorse mid-task. PM to discuss with Lead at an opportune time.** |
| **HOST** (Head of Sapient Trust) | worktree-native (`claude/host-cycle`, Option A) | YES — **launched Model A 2026-06-02 22:06** | **live `6a604131`** — every-3-hours `37 */3 * * *` (intermittent-lane experiment, CIO 6/2 authorization; Rule-2 idle-suppressed during PM presence) | v0.7 **Model A** | `:37` | Launched via Remote Control go-word 6/2. Session log `dev/2026/06/02/2026-06-02-2206-host-code-opus-log.md`. Cron-shape experiment logged in `cron-shape-experiments.md` (8 fires/day vs 24 hourly for this intermittent lane). Filed Ship #045 HOST workstream review same session. |
| **Comms** (Communications) | pre-staged `claude/comms-cycle` (substrate committed 5/31 `e0f1505ad`) | adopting — **launching 6/2** (Option A, terminal) | none yet — register `:12` at Fire 0 | will be Model A on launch | `:12` | Offset `:12` CONFIRMED 6/2 (answered CIO offset memo). Substrate: comms-standing-items.md + duty-cycle-escalations-comms.md. Launch: terminal into comms-cycle. (`:22` now sole open offset.) |
| **Web** | worktree prepped (`claude/web-cycle`) — awaiting PM worktree-launch (Model A) | adopting — **HELD** (manual prep session 6/1) | none yet | will be Model A on launch | `:57` | Substrate prepped 5/29 (`7d5ae50e3`). Manual prep session 6/1 07:58 (after 3-day gap); still awaiting PM worktree-launch operator action. Two-repo split: website code stays in `piper-morgan-website`. |

**Legend** — Working tree: `worktree-native` = session launched in worktree (Model A); `Model B` = launched-in-main + cd-into worktree; `main` = operating on shared main. Cron: `live` / `held` (deliberately not registered) / `none` / `(confirm)`.

### Auto-worktree note (PA finding 2026-05-31, PM-flagged via PA)

The Claude Code harness defaults to **auto-creating ephemeral worktrees** at session launch (e.g., `claude/modest-dhawan-9346b7`, `claude/sad-buck-d383f4`, `claude/interesting-goodall-c5535c`) rather than reusing the canonical `claude/{role}-cycle` worktree. **Both forms satisfy Model A** — any non-main worktree gives never-touch-main by construction; push-to-ref to main works identically. So an auto-worktree branch in this table is **functionally fine**, not a deviation. The cohort standard (force named vs. accept auto + record mapping) is a PM call pending. Agents in auto-worktrees: record the auto-name→role mapping in session log + here, so registry stays legible.

---

## Rollup (2026-06-01 snapshot — CIO agent-by-agent review with PM)

- **On Model A**: Arch, Exec, PA, **CIO** (4). Cron-live now: Arch, Exec; PA + CIO cron deliberately off/unregistered while PM-engaged (re-register at IDLE).
- **Model B (migrating)**: none — CIO migration to Model A completed 6/1.
- **Migrating today (6/1)**: **Docs** (PM directive #4 — resume cycle in prepped `claude/docs-cycle`); **Lead** (queued low-priority — bless worktree-native migration at a clean breakpoint after gates clear; main-home Rule-2 Model-A meanwhile).
- **Adopting / held — ready, awaiting PM launch**: **HOST** (prepping worktree now, idling for go-word), **Web** (prepped `claude/web-cycle`; note: website *code* work lives in the separate `piper-morgan-website` repo, so it's already clash-isolated from the product cohort), **PPM** + **CXO** (PM targeting today; have everything but the worktree).
- **Not yet launched**: **Comms** (worktree prepped; CIO memo'd 6/1 to pick offset `:12`/`:22`).

So of ~11 agents: 4 on Model A (2 cron-live now), 2 migrating today, 4 ready-and-held, 1 awaiting-offset. The v0.7.0 package gives held + not-started agents a clean launch-in-worktree path (= Model A, satisfies "do not register on main"). Per PA's 5/31 finding, harness auto-worktrees also satisfy Model A, so launch is a one-step operator action even without pre-creating a named worktree.

---

## Keeping it current (the methodology-36 honest note)

A hand-maintained status table goes stale (that's literally the principle in methodology-36). Until a derived view exists, refresh by checking the **derivable signals**:
- **Working tree / cron**: `git worktree list` shows who has a `claude/{role}-cycle` worktree; the agent's own session reports its cron via `CronList`.
- **On the cycle today**: presence of `dev/active/cycle-log-{role}-{today}.md`.
- **Version/rules**: the agent's registered cron prompt (Model-A vs Model-B language).

**Derived view SHIPPED 2026-06-03**: `scripts/cohort-cycle-status.sh` (read-only) derives "who's-cycling-today" from cycle-log presence + worktree list — the methodology-36 Class-1 fix. Run it for the non-stale signal; it complements (does not replace) this hand-maintained view, which still carries what can't be derived remotely (cron-live status, work-shape, carry-in). Honest limit baked in: it omits cron-live (session-scoped, not remotely visible — the exact column that silently went stale here).

---

*Filed by CIO Vehicle 2, 2026-05-29, per PM request for a dedicated agent-status tracker. Companion to `v0.7.0-adoption-package.md`. PM updates cells during manual engagement; CIO refreshes the snapshot at cycle cadence.*
