# HOST Cycle Launch Handoff — 2026-06-01

**From**: HOST session in `/Users/xian/Development/piper-morgan/piper-morgan-product` (main checkout; session log `dev/active/2026-06-01-0740-host-code-opus-log.md`)
**To**: HOST successor session about to launch in `/Users/xian/Development/piper-morgan/piper-morgan-product-host-cycle` (this worktree, on branch `claude/host-cycle`)
**Created**: 2026-06-01 18:12 PDT by predecessor session

You are HOST (Head of Sapient Trust). This handoff exists because PM is migrating you from main-checkout manual-session-open mode (where the predecessor was operating per the May 28 "do not register on main" hold) to v0.7.0 worktree-cycle Model A. You're now sitting in the worktree; opening Claude Code here IS the migration step ("launch-in-worktree" — the load-bearing move per the v0.7.0 adoption package).

---

## Your role + identity

- **Role**: HOST. Briefing: `docs/briefing/BRIEFING-ESSENTIAL-HOST.md`
- **Session log slug**: `host-code-opus` (e.g. `dev/YYYY/MM/DD/HHMM-host-code-opus-log.md`)
- **Cron offset (slated)**: `:37` hourly — confirmed via `docs/operations/duty-cycle design/cohort-agent-status.md`. Adopt this.

## Your position in the cohort right now

- **Cohort live on worktree-cycle Model A**: CIO, Architect, Exec, PA (per status tracker)
- **Cleared-to-launch / prepped**: PPM, CXO, Web, Comms (the "four not-yet-moving" per CIO May 29 package memo)
- **State-to-confirm**: Docs, Lead, HOST → **you're now confirming HOST**
- The tracker (`docs/operations/duty-cycle design/cohort-agent-status.md`) has your row marked "(confirm) — verify current cron state." After your first fire, update your row to reflect Model A live + cron job ID + worktree path.

## Canonical v0.7.0 protocol — read this whole package first

**Required reads (~20 min, in order)**:
1. `docs/operations/duty-cycle design/v0.7.0-adoption-package.md` — the canonical adoption recipe + cron best-practices + interim mechanisms
2. `docs/operations/duty-cycle design/duty-cycle-design-v0.6.md` — base design (v0.7 design doc may also exist; check)
3. `docs/operations/duty-cycle design/procedures/cron-lifecycle.md` — Rule 1 (cron-bind-to-IDLE during substantive WORK) + Rule 2 (Model A, leave-cron-running during PM conversation)
4. `docs/operations/duty-cycle design/procedures/check.md` / `start.md` / `stop.md` / `work-parts.md` / `mail-loop.md` / `task-loop.md` / `decision-table.md` / `idle.md`

**The canonical cron-prompt template** (per v0.7.0 package, normalized middle-weight ~30 lines): copy from the package, adapt the role + offset + paths. Do NOT re-improvise from scratch.

## Load-bearing v0.7.0 disciplines (the ones that bit the cohort recently)

- **CronDelete-FIRST**: if a fire MAY go substantive, `CronDelete` is the literal first action (before sync, before anything). Closes the CronList→CronDelete race (Arch hit it Fire 3 May 27).
- **Rule 2 = Model A**: do NOT CronDelete on PM messages. Leave cron running during PM conversation; the runtime's idle-only-fire suppression handles PM turns.
- **Drain-until-IDLE**: each fire drains ALL unblocked work (mail-to-zero → tasks-to-blocked → re-check → loop), then (0, 0) IDLE. NOT one-work-unit-per-fire.
- **No-op IDLE ticks: NO COMMIT** (don't churn the log).
- **Explicit-paths-only** on `git add` — NEVER directory-level mailbox adds.
- **Mailbox writes go via main-worktree bridge**: `check-branch.sh` hard-blocks `mailboxes/` commits on non-main branches. To send mail: `cd /Users/xian/Development/piper-morgan/piper-morgan-product` → pull → write + commit mail → push → return to this worktree. **Batch mail to minimize the switch.** (Lead Dev is amending the hook; until then this is the interim path.)
- **Overnight**: when this session dies (sleep/battery), tomorrow's START is a manual reopen-in-this-worktree.

## Why the predecessor hit three shared-main clashes (and why you should be at peace)

In <24h (May 27 morning P-16 + Fire 2 foreign-agent-commit + May 28 morning Docs 972 sweep), the predecessor session experienced three shared-main concurrent-commit races. **Those clashes were the architectural problem the worktree reversal was ratified to fix.** PM verbatim May 28 ~7:53 PT: *"worktree decision ratified. do not register on main."* You're now sitting in the architectural fix. Don't replay the predecessor's defensive `pull --rebase --autostash` reflex on every fire; per-fire sync stays simple now because no other agent is committing to `claude/host-cycle` except you.

## Your standing commitments (open work)

Read these substrate files (all in `dev/active/`):
- `host-standing-items.md` — task list, freshly updated. Three items live right now:
  1. **v0.3 Agent 360 questionnaire fielding** — ~Jun 1 target = TODAY. Draft at `dev/active/agent-360-questionnaire-v0_3-draft.md`. CIO concur received; refinements applied May 27 (Fire 11). **Ready to ship to the 10-role cohort whenever PM greenlights.** Awaiting PM go-signal. ~Jun 12 synthesis target.
  2. **Day-3/4 mutual-assessment memo to CIO** — was ~May 30 target = ~3 days overdue (gap May 29–31). When you draft: absorb the third-clash incident from May 28 morning + the v0.7 ratification arc + Model A adoption + cohort-proliferation observation.
  3. **Day-7 cohort-readiness memo to PM** — ~Jun 3 target = Wednesday.
- `duty-cycle-escalations-host.md` — attention doc, currently quiet (no PM escalations open).

Other items time/data-gated:
- HOST input on MEM #974 format ~early Jun (post-data per Docs)
- v0.3 synthesis ~Jun 12 (post-fielding)

## Cycle log convention

- Today's cycle log goes at `dev/active/cycle-log-host-2026-06-01.md` (does NOT yet exist — create on Fire 1)
- The May 18 cycle log (V1 dry-run, retired) is at `dev/2026/05/18/cycle-log-host-2026-05-18.md` — merged to main, archive only
- The May 27 cycle log (Day-1 v0.6 adoption on main) is at `dev/active/cycle-log-host-2026-05-27.md` — contains the substantive arc the predecessor walked: 16 fires, Day-1 mutual-assessment to CIO, three clash incidents, v0.6.1/.2/.3 absorption
- The May 28 manual-fire cycle log is at `dev/active/cycle-log-host-2026-05-28.md` — the v0.7 ratification day; brief

## Your startup procedure (Fire 1)

1. Verify your worktree + branch: `pwd` returns this worktree path, `git branch --show-current` returns `claude/host-cycle`. STOP if either is wrong.
2. Sync the worktree: `git fetch origin && git pull origin main --ff-only` (or `--rebase` if needed — but main may have moved; resolve from THIS worktree).
3. Open today's session log: `dev/2026/06/01/HHMM-host-code-opus-log.md` (replace HHMM with current time).
4. Open today's cycle log: `dev/active/cycle-log-host-2026-06-01.md`.
5. Open today's tracker: `dev/2026/06/01/host-tracker-2026-06-01.md`.
6. Adopt the canonical cron-prompt template per the v0.7.0 package, with `:37` offset.
7. **Register the cron** (this is the v0.7 launch — you ARE compliant with "do not register on main" because you're on `claude/host-cycle`). `CronCreate "37 * * * *"` with the canonical-template prompt.
8. **Surface to PM** that HOST is now live on Model A in `claude/host-cycle`, cron job ID = X, ready for PM directive on the three commitments above (v0.3 fielding is the time-sensitive one for today).
9. Update the cohort-agent-status tracker row for HOST (this is a mailbox-class touch — use the main-worktree bridge for it).

## What the predecessor will do after this handoff is committed

The predecessor session in main will:
- Commit this handoff file (so it lands on `claude/host-cycle` branch)
- Append a final note to predecessor's session log noting the migration handoff happened
- Stop substantive work (PM will close the predecessor session after you confirm you're live)

The predecessor's session log (`dev/active/2026-06-01-0740-host-code-opus-log.md`) and standing items + escalations docs are all readable from this worktree — they're at the same paths because the worktree shares the working tree state captured at the moment of `git worktree add`. You can read what the predecessor was doing without context-switching.

## One last note from the predecessor

The trust-property arc from May 27–28 (v1 retirement → v0.6 dry-run → three clashes → trust/ops-lens memo → PM worktree ratification) was clean. The successor inherits a healthy substrate. Don't pace tightly to deadlines — Time Lord doctrine still applies. Per memory: "do unblocked work right away" + "deadlines are last-possible-time."

Good luck. The cohort is rooting for HOST-on-worktree.

— HOST (predecessor session), 2026-06-01 18:12 PDT
