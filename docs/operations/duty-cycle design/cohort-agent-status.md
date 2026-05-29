# Cohort Agent Status — working tree + duty-cycle adoption

**Purpose**: PM's at-a-glance tracker for the v0.7 rollout — per agent: which working tree it operates from, whether it's on the duty cycle, and which version/rules. PM's working tool for manual engagement until all agents are migrated.

**Snapshot date**: 2026-05-29 (CIO). **This is a hand-maintained snapshot** — see "Keeping it current" below; ideally derived later (methodology-36 candidate). Cells marked **(confirm)** are CIO's best inference, not verified — verify on engagement.

---

## Status table

| Agent | Working tree | On duty cycle? | Cron | Version / rules | Offset | Notes |
|---|---|---|---|---|---|---|
| **Arch** (Chief Architect) | worktree-native (`sad-buck-d383f4`) | YES | live | v0.7 **Model A** | `:52` | First worktree PoC; native-launch reference. |
| **Exec** (Chief of Staff) | worktree-native (`interesting-goodall-c5535c`) | YES | live | v0.7 **Model A** | `:32` | Re-enabled cron per PM clearance (native-worktree basis). |
| **PA** (Piper Alpha) | worktree-native (`claude/pa-cycle`) | YES | live | v0.7 **Model A** | `:42` | Restarted Chat→Code 2026-05-28 19:00; resolved check-branch.sh open-item day 1. |
| **CIO** (Chief Innovation Officer) | worktree (`claude/cio-cycle`) but **Model B** (launched-in-main; cd-into) | YES | live | v0.7 **Model B** → migrating to A | `:07` | 2nd PoC. Converts to Model A at next session boundary (relaunch-in-worktree). |
| **PPM** (Principal Product Manager) | main (confirm) | adopting — **HELD** | held (deleted `2aba0768`) | will be Model A on launch | `:47` | Confirmed adoption + offset; holding per "do not register on main." Unblocked now by the v0.7.0 package (launch-in-worktree path). |
| **CXO** (Chief Experience Officer) | main (confirm) | adopting — **HELD** | none yet | will be Model A on launch | `:02` | Confirmed adoption + offset; was finishing interactive design work. Unblocked by package. |
| **Docs** (Documentation Mgmt) | (confirm) | (confirm) | (confirm) | (confirm) | `:17` (slate) | Active 2026-05-29 session. Early invitee; verify current cron/worktree state. |
| **Lead** (Lead Developer) | (confirm) | (confirm) | (confirm) | (confirm) | `:27` (slate) | Deep in worktree-mechanism + hook design. Verify current cycle state. |
| **HOST** (Head of Sapient Trust) | (confirm) | (confirm) | (confirm) | (confirm) | `:37` (slate) | Early invitee (HOST-first wave). Verify current cron state. |
| **Comms** (Communications) | main (confirm) | NO — not launched | none | — | open (`:12`/`:22`/`:57`) | Last cohort role not yet on cycle. Nudged via v0.7.0 package. |
| **Web** | main (confirm) | NO — not launched | none | — | open (`:12`/`:22`/`:57`) | Invited, not started. Nudged via v0.7.0 package. |

**Legend** — Working tree: `worktree-native` = session launched in worktree (Model A); `Model B` = launched-in-main + cd-into worktree; `main` = operating on shared main. Cron: `live` / `held` (deliberately not registered) / `none` / `(confirm)`.

---

## Rollup (2026-05-29 snapshot)

- **Cron-live on Model A**: Arch, Exec, PA (3).
- **Cron-live on Model B (migrating)**: CIO (1).
- **Adopting, held (unblocked by package)**: PPM, CXO (2).
- **State to confirm**: Docs, Lead, HOST (3).
- **Not yet launched**: Comms, Web (2).

So of ~11 agents: 4 cron-live, 2 held-but-cleared, 3 to-confirm, 2 not-started. The v0.7.0 package gives the held + not-started agents a clean launch-in-worktree path (= Model A, satisfies "do not register on main").

---

## Keeping it current (the methodology-36 honest note)

A hand-maintained status table goes stale (that's literally the principle in methodology-36). Until a derived view exists, refresh by checking the **derivable signals**:
- **Working tree / cron**: `git worktree list` shows who has a `claude/{role}-cycle` worktree; the agent's own session reports its cron via `CronList`.
- **On the cycle today**: presence of `dev/active/cycle-log-{role}-{today}.md`.
- **Version/rules**: the agent's registered cron prompt (Model-A vs Model-B language).

**Tooling candidate**: a `scripts/cohort-cycle-status.py` that derives this table from worktree list + cycle-log presence would retire the hand-maintenance (methodology-36 Class-1 fix). Filed as a future-tooling note.

---

*Filed by CIO Vehicle 2, 2026-05-29, per PM request for a dedicated agent-status tracker. Companion to `v0.7.0-adoption-package.md`. PM updates cells during manual engagement; CIO refreshes the snapshot at cycle cadence.*
