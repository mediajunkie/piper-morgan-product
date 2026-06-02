# Cohort Agent Status — working tree + duty-cycle adoption

**Purpose**: PM's at-a-glance tracker for the v0.7 rollout — per agent: which working tree it operates from, whether it's on the duty cycle, and which version/rules. PM's working tool for manual engagement until all agents are migrated.

**Snapshot date**: 2026-05-29 (CIO). **This is a hand-maintained snapshot** — see "Keeping it current" below; ideally derived later (methodology-36 candidate). Cells marked **(confirm)** are CIO's best inference, not verified — verify on engagement.

---

## Status table

| Agent | Working tree | On duty cycle? | Cron | Version / rules | Offset | Notes |
|---|---|---|---|---|---|---|
| **Arch** (Chief Architect) | worktree-native (`sad-buck-d383f4`) | YES | live | v0.7 **Model A** | `:52` | First worktree PoC; native-launch reference. |
| **Exec** (Chief of Staff) | worktree-native (`interesting-goodall-c5535c`) | YES | live | v0.7 **Model A** | `:32` | Re-enabled cron per PM clearance (native-worktree basis). |
| **PA** (Piper Alpha) | worktree-native — fresh session on **auto-created `claude/modest-dhawan-9346b7`** (canonical `claude/pa-cycle` registered but session's primary cwd landed in the harness auto-worktree) | YES — Day 4 of Model A | **UNREGISTERED** (deleted 2026-05-31 ~12:00 for Skunkworks work; pending re-register at IDLE + PM go-autonomous) | v0.7 **Model A** | `:42` | Original restart Chat→Code 2026-05-28 19:00; resolved check-branch.sh open-item day 1. Fresh session 2026-05-31 validated Model-A operates cleanly from harness auto-worktrees too — see "Auto-worktree note" below. |
| **CIO** (Chief Innovation Officer) | worktree (`claude/cio-cycle`) but **Model B** (launched-in-main; cd-into) | YES | live | v0.7 **Model B** → migrating to A | `:07` | 2nd PoC. Converts to Model A at next session boundary (relaunch-in-worktree). |
| **PPM** (Principal Product Manager) | main (confirm) | adopting — **HELD** | held (deleted `2aba0768`) | will be Model A on launch | `:47` | Confirmed adoption + offset; holding per "do not register on main." Unblocked now by the v0.7.0 package (launch-in-worktree path). |
| **CXO** (Chief Experience Officer) | main (confirm) | adopting — **HELD** | none yet | will be Model A on launch | `:02` | Confirmed adoption + offset; was finishing interactive design work. Unblocked by package. |
| **Docs** (Documentation Mgmt) | (confirm) | (confirm) | (confirm) | (confirm) | `:17` (slate) | Active 2026-05-29 session. Early invitee; verify current cron/worktree state. |
| **Lead** (Lead Developer) | (confirm) | (confirm) | (confirm) | (confirm) | `:27` (slate) | Deep in worktree-mechanism + hook design. Verify current cycle state. |
| **HOST** (Head of Sapient Trust) | (confirm) | (confirm) | (confirm) | (confirm) | `:37` (slate) | Early invitee (HOST-first wave). Verify current cron state. |
| **Comms** (Communications) | main (confirm) | NO — not launched | none | — | open (`:12`/`:22`) | Nudged via v0.7.0 package. **Pick `:12` or `:22`** — Web claimed `:57` on 2026-05-29. |
| **Web** | worktree prepped (`claude/web-cycle`) — awaiting PM-launch (Model A) | adopting — **HELD** | none yet | will be Model A on launch | `:57` | Substrate prepped 2026-05-29 (commit `7d5ae50e3`); PM launches session in `../piper-morgan-product-web-cycle` to register. Two-repo split: website code stays in `piper-morgan-website`. |

**Legend** — Working tree: `worktree-native` = session launched in worktree (Model A); `Model B` = launched-in-main + cd-into worktree; `main` = operating on shared main. Cron: `live` / `held` (deliberately not registered) / `none` / `(confirm)`.

### Auto-worktree note (PA finding 2026-05-31, PM-flagged via PA)

The Claude Code harness defaults to **auto-creating ephemeral worktrees** at session launch (e.g., `claude/modest-dhawan-9346b7`, `claude/sad-buck-d383f4`, `claude/interesting-goodall-c5535c`) rather than reusing the canonical `claude/{role}-cycle` worktree. **Both forms satisfy Model A** — any non-main worktree gives never-touch-main by construction; push-to-ref to main works identically. So an auto-worktree branch in this table is **functionally fine**, not a deviation. The cohort standard (force named vs. accept auto + record mapping) is a PM call pending. Agents in auto-worktrees: record the auto-name→role mapping in session log + here, so registry stays legible.

---

## Rollup (2026-05-29 snapshot)

- **Cron-live on Model A**: Arch, Exec, PA (3).
- **Cron-live on Model B (migrating)**: CIO (1).
- **Adopting, prepped/held (substrate or offset confirmed, awaiting PM launch)**: PPM, CXO, **Web** (3).
- **State to confirm**: Docs, Lead, HOST (3).
- **Not yet launched**: Comms (1).

So of ~11 agents: 4 cron-live, 3 held-but-prepped, 3 to-confirm, 1 not-started. The v0.7.0 package gives the held + not-started agents a clean launch-in-worktree path (= Model A, satisfies "do not register on main"). **Web responded same-day** with substrate prepped — first cohort response to the distribution.

---

## Keeping it current (the methodology-36 honest note)

A hand-maintained status table goes stale (that's literally the principle in methodology-36). Until a derived view exists, refresh by checking the **derivable signals**:
- **Working tree / cron**: `git worktree list` shows who has a `claude/{role}-cycle` worktree; the agent's own session reports its cron via `CronList`.
- **On the cycle today**: presence of `dev/active/cycle-log-{role}-{today}.md`.
- **Version/rules**: the agent's registered cron prompt (Model-A vs Model-B language).

**Tooling candidate**: a `scripts/cohort-cycle-status.py` that derives this table from worktree list + cycle-log presence would retire the hand-maintenance (methodology-36 Class-1 fix). Filed as a future-tooling note.

---

*Filed by CIO Vehicle 2, 2026-05-29, per PM request for a dedicated agent-status tracker. Companion to `v0.7.0-adoption-package.md`. PM updates cells during manual engagement; CIO refreshes the snapshot at cycle cadence.*
