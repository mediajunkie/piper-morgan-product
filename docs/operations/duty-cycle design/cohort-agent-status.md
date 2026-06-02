# Cohort Agent Status — working tree + duty-cycle adoption

**Purpose**: PM's at-a-glance tracker for the v0.7 rollout — per agent: which working tree it operates from, whether it's on the duty cycle, and which version/rules. PM's working tool for manual engagement until all agents are migrated.

**Snapshot date**: 2026-06-01 (CIO — full agent-by-agent review with PM; supersedes 2026-05-29). **This is a hand-maintained snapshot** — see "Keeping it current" below; ideally derived later (methodology-36 candidate). Rows verified against `git worktree list` + today's session/cycle-log presence + PM ground truth.

---

## Status table

| Agent | Working tree | On duty cycle? | Cron | Version / rules | Offset | Notes |
|---|---|---|---|---|---|---|
| **Arch** (Chief Architect) | worktree-native (`sad-buck-d383f4`) | YES | live | v0.7 **Model A** | `:52` | First worktree PoC; native-launch reference. |
| **Exec** (Chief of Staff) | worktree-native (`interesting-goodall-c5535c`) | YES | live | v0.7 **Model A** | `:32` | Re-enabled cron per PM clearance (native-worktree basis). |
| **PA** (Piper Alpha) | worktree-native — fresh session on **auto-created `claude/modest-dhawan-9346b7`** (canonical `claude/pa-cycle` registered but session's primary cwd landed in the harness auto-worktree) | YES — Day 5 of Model A | **UNREGISTERED** (PM-engaged today; re-register at IDLE + PM go-autonomous) | v0.7 **Model A** | `:42` | Original restart Chat→Code 2026-05-28 19:00; resolved check-branch.sh open-item day 1. Fresh session 2026-05-31 validated Model-A operates cleanly from harness auto-worktrees too — see "Auto-worktree note" below. |
| **CIO** (Chief Innovation Officer) | worktree-native (`claude/cio-cycle`, launched-in-worktree) | YES | live | v0.7 **Model A** | `:07` | 2nd PoC. **Migrated to Model A 2026-06-01** (Option A — named worktree, not auto). Cron pending re-register at IDLE + PM go-autonomous. |
| **PPM** (Principal Product Manager) | no cycle worktree yet | adopting — **HELD**; PM targeting migration today (6/1) | held (deleted `2aba0768`) | will be Model A on launch | `:47` | **Ready to migrate**: offset confirmed, briefing + v0.7.0 package + cron template all in place; only operator action is create/launch worktree (named `claude/ppm-cycle` or accept harness auto-worktree). |
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
