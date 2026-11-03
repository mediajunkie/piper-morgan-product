---
type: operations
title: "Liveness, current state: how a seat wakes, proves it woke, and gets noticed when it doesn't"
valid_from: "2026-10-14"
last_updated: "2026-11-03"
---

# Liveness: current state

**Owners:**
- CIO: the duty-cycle procedure, the heartbeat, the freeze check, the watchdog script.
- Pard: everything launchd and crontab (installs, runs, measures).
- Each row below names its owner.

**Status: drafted 2026-10-14 (methodology audit R10). Pard confirmed the wake rows the same morning. Updated 2026-11-03: all 11 PM seats fire from LaunchAgents since 11-02 (Pard, 15:04), and no seat runs a session cron (duty-cycle-tick v1.62).**
**Why this page exists:** the design record (`docs/operations/duty-cycle design/`, v0.1 to v0.7) and the
registry's header prose describe the June and July system (session `CronCreate` jobs, heartbeats committed
to git). Both changed: LaunchAgent wakes from 09-24, and the heartbeat moved out of git on 10-12. Nothing
described the system as it now runs.

## The chain, end to end

```
wake ──► fire runs ──► heartbeat ──► freeze check ──► watchdog alert ──► (PM / Exec)
(launchd)  (tick skill)  (store)       (reads store+git)  (crontab, 6-hourly)
```

1. **Wake: what makes a seat fire.**
   - *Scheduled fires.* One LaunchAgent per seat, `com.xian.pm-<role>-cycle`, for all 11 PM seats since
     2026-11-02 (Exec, Lead and CXO were the last; Pard, 15:04). Pard generates each schedule from the
     `cron_expr` column of `dev/active/duty-cycle-registry.tsv`, and it injects the seat's stored
     "DUTY CYCLE TICK" prompt (mediajunkie `docs/seat-prompts/pm-<role>.md`; `scripts/seat-prompt.sh`).
     The row and the plist can drift (11-02: Lead's row said :17, its plist fires :46), so
     `scripts/registry-plist-drift.py` compares every row's minutes, hours and `first_fire` with the plist
     (11 of 11 match on 11-03). A seat deletes any leftover session cron, since it would fire twice.
   - *Mail wakes.* `com.xian.mail-wake` (Pard; `scripts/mail-wake.py`, every 180 s). It injects "MAIL WAKE" when new mail for a role lands on
     origin/main, for both v3 files and v4 IDs.
   - *Hold.* Pard's `fire-hold.sh` can suspend fires, as during the 10-13 rewrite freeze.
     `fire-hold.sh status` reports it.
   - Until 11-02, seats ran session-scoped `CronCreate` jobs, which died silently on session exit and
     after 7 days. That history is in git and in `procedures/cron-lifecycle.md` (historical).

2. **Fire.** The `duty-cycle-tick` skill (procedure: `.claude/skills/duty-cycle-tick/SKILL.md`; history:
   `duty-cycle-tick-changelog.log`). A fire is a wake, not a time-box. It drains every unblocked item, then
   checks mail until two consecutive checks are empty.

3. **Heartbeat: "I woke up", nothing more.** `scripts/duty-cycle-heartbeat.sh <role> <fire> --if-quiet`
   ends every fire.
   - Since v2.0 (10-12) it writes **only** the local store `~/.local/state/piper-heartbeats/`, with no git
     commit: one row per invocation in `<date>/<role>.tsv`, plus the newest in `last-invoked/<role>.txt`.
   - Reader: `scripts/hb-store.py`.
   - Why it's out of git: `r3-metric.md` (about 65 heartbeat commits a day was the cost).
   - **Single-host assumption:** the store lives on Amber. A seat on another host has no store.

4. **Freeze check: who should be cycling, and isn't.** `scripts/duty-cycle-freeze-check.sh` (CIO).
   - Reads the registry from origin/main. Only roles with a row are watched: coverage is opt-in, so
     state the denominator.
   - Decides whether a role should be cycling now, from its session log: a `DAY-CLOSED` marker means
     stopped; no log before `first_fire` means not started yet.
   - Takes the newest of four signals:
     - a commit whose subject starts `<role>:`;
     - a commit to the role's session log;
     - legacy git heartbeat rows;
     - the store's `last-invoked` epoch.
   - Compares that against the role's `threshold_h`.
   - **A quiet fire still counts, because the heartbeat runs every fire.** The work-output-only inference
     that alerted on compliance in July is gone.
   - The examined line says whether the store was present.

5. **Watchdog: getting it to a human.** `scripts/duty-cycle-watchdog.sh` (CIO), run by Pard's crontab
   wrapper `mediajunkie/scripts/freeze-watchdog-amber.sh` at `46 */6 * * *`.
   - On a newly stale role it nudges by desktop notification, a mailbox memo (push-to-ref to Exec), and
     Slack if configured.
   - Since 10-14 the wrapper runs in its **own detached worktree**, `~/Development/piper-morgan-worktrees/watchdog`
     (fetch plus `checkout --detach origin/main`, no pull). Before that it pulled inside PM's live
     checkout; the history rewrite showed the danger.
   - Its liveness is Pard's heartbeat log `mediajunkie/logs/freeze-watchdog-heartbeat.log`, one line
     every run. More than 6 hours with no line means the belt is down.

5b. **Stuck-at-a-dialog alert: woken but not waking.** Inside Pard's `scripts/mail-wake.py` (mediajunkie
   fa36beb, live 2026-10-15 15:39). Pard owns it.
   - **Why:** Lead's session sat blocked from about 08:12 to 15:30 on 10-15 (a subagent's permission dialog).
     xian's promotion approval sat unread from 13:18. The mail wakes fired, but nothing checked that the
     session woke (Exec, from xian's notice).
   - **Rule:** when a seat has unread mail (v3 inbox and v4, judged together) and mail-wake has seen a dialog
     on its pane for 30 minutes (`STUCK_AFTER`), it sends one memo per episode: to Exec for PM seats, and to
     Pard for Exec and non-PM seats. The memo names the dialog's question line and says a human must open the
     pane. The signal is direct: mail-wake had been logging "dialog showing" for Lead 155 times that day,
     as a log line nobody read.
   - **Not covered:** a dialog with no mail waiting (cycle-check's `pane-dialogs` arm flags those every 2 hours,
     to xian's card), and a hang with no dialog (the freeze check, item 4).
   - **Why not a heartbeat join (CIO built one the same afternoon, then retired it):**
     `stuck-session-check.py` flagged a role with mail waiting 30 minutes and no heartbeat, role commit or v4
     ack since. Backtested over 10-14 and 10-15, it caught Lead only from 13:30. Lead's heartbeat kept
     recording post-commit rows until 12:43 while the dialog blocked the work, so "no sign of life" stayed
     false for hours. Activity rows show the session is alive, not that the work is moving
     (methodology-43). Pard's dialog signal is the direct one. The heartbeat join was removed so that one
     rule has one mechanism.

6. **Live-layer checks** (is the machinery itself running?):
   - Pard's `verify-hooks-drumbeat` (07:05 and 19:05) checks a real `claude -p` commit is blocked by
     `check-branch.sh`. Since 10-14 19:15 it tests PM's project copy, carried from origin/main
     (mediajunkie 9afa8c9). Before that it tested the user-level copy, removed at 10:43, which
     turned the 19:05 run red.
   - `scripts/whats-armed.sh` reads that verdict and probes the rest (`whats-armed.md`).
   - `scripts/main-ci-status.sh` covers CI.

## What this design cannot see (stated, not hidden)

- **A wedged session that still emits.** If a seat's session is alive but stuck, for example at a
  rate-limit dialog, an injected prompt may not run. The heartbeat then stops, and the check sees it only
  after `threshold_h`.
- **A role with no registry row**, or with no wake mechanism (see Exec, Lead and CXO above). It cannot be
  reported stale, only missed.
- **The belt itself, between 6-hourly runs.** Pard's cycle-check reads the wrapper's heartbeat log, and
  `whats-armed.sh` reads the drumbeat.
- **Another host.** The store is local.

## Stale records this page supersedes (fix at their next edit)

(The registry header row was fixed 2026-11-02, v1.62.)

| Record | What is stale |
|---|---|
| `docs/operations/duty-cycle design/` (v0.1 to v0.7) | June and July design. It predates LaunchAgents, the heartbeat store and the watchdog worktree. Keep as history. |
| `scripts/launchd/com.pipermorgan.duty-cycle-watchdog.plist` | The June laptop plist. The watchdog runs from Pard's crontab on Amber. Not loaded on Amber (not in `~/Library/LaunchAgents`, no label in `launchctl list`; Pard 10-14). On Amber it's history. The laptop isn't established. |

**Verified how:**
- Read the headers of `duty-cycle-freeze-check.sh` (lines 1 to 25, 143 to 160 and 190 to 215) and the
  `hb-store.py` docstring, and the registry header.
- Ran `launchctl list` and filtered `com.xian.*`.
- Read Pard's re-armed wrapper (lines 14 to 15).
- Committed 2026-10-14 10:27 PT. (The first version said "about 11:45 PT", which was a guess, not a reading; corrected.)
- **Layer:** files and launchctl state. No wake or alert was triggered to test the chain.
- **Denominator:** the 11 registry roles. 8 have a LaunchAgent. 3 don't yet (session crons; designated 10-14, provisioning pending).
- **Update 2026-11-03 (CIO):** the 11 registry roles, all 11 with a LaunchAgent plist in `~/Library/LaunchAgents/`, compared with their registry rows by `scripts/registry-plist-drift.py` (11 of 11 match). Layer: plist files on disk, not `launchctl print`.
