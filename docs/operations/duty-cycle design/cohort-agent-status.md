# Cohort Agent Status — working tree + duty-cycle adoption

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

Cross-cutting (blockers first):
- [x] **Cohort launch standard DECIDED 2026-06-02: Option B (Desktop + ephemeral).** Pre-created ppm/cxo worktrees removed.
- [ ] **IDLE auto-resume gap**: build silence-fallback PoC (presence-aware fire + self-scheduled silence timer) so PM-silence → autonomy without a manual phrase. PM go/no-go pending.

Per-agent (launch via Desktop "New session" → /rename → brief → record slug→role here → register cron at the listed offset):
- [x] **PPM** `:47` — LAUNCHED 6/2 on `claude/upbeat-dubinsky-c2b572` (ephemeral, Option B); cron pending at IDLE
- [ ] **CXO** `:02` — ready to launch
- [ ] **HOST** `:37` — `claude/host-cycle` self-prepped; awaiting PM go-word
- [ ] **Web** `:57` — prepped; already clash-isolated (code lives in separate `piper-morgan-website` repo)
- [ ] **Docs** `:17` — self-migrating today (own directive); confirm landed + cron
- [ ] **Comms** `:12` or `:22` — awaiting offset-pick reply to CIO memo (6/1), then launch
- [ ] **Lead** `:27` — cron-live now (Rule-2 main-home Model-A); worktree-native migration queued low-pri (PM to discuss w/ Lead)
- [x] **CIO** `:07` — Model A done (6/1); cron arm + silence-PoC pending PM go
- [x] **Arch** `:52`, **Exec** `:32`, **PA** `:42` — already Model A, cron-live (PA cron off while PM-engaged)

---

## Status table

| Agent | Working tree | On duty cycle? | Cron | Version / rules | Offset | Notes |
|---|---|---|---|---|---|---|
| **Arch** (Chief Architect) | worktree-native (`sad-buck-d383f4`) | YES | live | v0.7 **Model A** | `:52` | First worktree PoC; native-launch reference. |
| **Exec** (Chief of Staff) | worktree-native (`interesting-goodall-c5535c`) | YES | live | v0.7 **Model A** | `:32` | Re-enabled cron per PM clearance (native-worktree basis). |
| **PA** (Piper Alpha) | worktree-native — fresh session on **auto-created `claude/modest-dhawan-9346b7`** (canonical `claude/pa-cycle` registered but session's primary cwd landed in the harness auto-worktree) | YES — Day 5 of Model A | **UNREGISTERED** (PM-engaged today; re-register at IDLE + PM go-autonomous) | v0.7 **Model A** | `:42` | Original restart Chat→Code 2026-05-28 19:00; resolved check-branch.sh open-item day 1. Fresh session 2026-05-31 validated Model-A operates cleanly from harness auto-worktrees too — see "Auto-worktree note" below. |
| **CIO** (Chief Innovation Officer) | worktree-native (`claude/cio-cycle`, launched-in-worktree) | YES | live | v0.7 **Model A** | `:07` | 2nd PoC. **Migrated to Model A 2026-06-01** (Option A — named worktree, not auto). Cron pending re-register at IDLE + PM go-autonomous. |
| **PPM** (Principal Product Manager) | worktree-native — `claude/upbeat-dubinsky-c2b572` (ephemeral, Option B) | YES — **launched 6/2** (Model A) | UNREGISTERED (register at IDLE + go-autonomous) | v0.7 **Model A** | `:47` | Launched 6/2 via Desktop into harness auto-worktree. Carry-in: #683 Layer A, #1128 v17→canonical, PDR-005, Ship #045 lane review (Wed Jun 3). |
| **CXO** (Chief Experience Officer) | old task worktrees only; no cycle worktree | adopting — **HELD**; PM targeting migration today (6/1) | none yet | will be Model A on launch | `:02` | **Ready to migrate**: offset confirmed, briefing + v0.7.0 package + cron template all in place; only operator action is create/launch worktree (named `claude/cxo-cycle` or accept harness auto-worktree). |
| **Docs** (Documentation Mgmt) | on **main** (session); `claude/docs-cycle` worktree prepped | adopting — **migrating today** | off-cron since 5/28 (do-not-register-on-main) | will be Model A on launch | `:17` | PM-engaged session 6/1 07:05; worktree migration is PM directive #4 today (resume cycle in `claude/docs-cycle`). |
| **Lead** (Lead Developer) | **main-home** + per-task feature worktrees (`lead-NNNN`) | YES — cron-live (Fire 1 today 00:17) | live — `:27` workhorse hourly | v0.7 **Model A (Rule-2, main-home)** | `:27` | Cron-live + cycling. **Plan (PM 6/1): migrate to worktree-native Model A at a clean breakpoint after inherited gates clear — low priority, don't pull the workhorse mid-task. PM to discuss with Lead at an opportune time.** |
| **HOST** (Head of Sapient Trust) | prepping new worktree (6/1 18:10) | adopting — **idling, awaiting go-word** | none yet | will be Model A on launch | `:37` | PM-confirmed 6/1 18:10: prepping new worktree, idled today waiting for the word. |
| **Comms** (Communications) | main (confirm) | NO — not launched | none | — | open (`:12`/`:22`) | Nudged via v0.7.0 package. **Pick `:12` or `:22`** — Web claimed `:57` on 2026-05-29. |
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

**Tooling candidate**: a `scripts/cohort-cycle-status.py` that derives this table from worktree list + cycle-log presence would retire the hand-maintenance (methodology-36 Class-1 fix). Filed as a future-tooling note.

---

*Filed by CIO Vehicle 2, 2026-05-29, per PM request for a dedicated agent-status tracker. Companion to `v0.7.0-adoption-package.md`. PM updates cells during manual engagement; CIO refreshes the snapshot at cycle cadence.*
