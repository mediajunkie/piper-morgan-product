# Restore drill (#2157): HOST's half of the runbook (DRAFT, nothing has run)

**Status:** draft, 2026-11-04. Nothing here runs until xian says yes. The ordered `fly` lines are Lead's to write and are not in this file. The safe form is Arch's (decisions.log, 2026-11-04 16:38).

## Why

Design partners were told "Your account and your work will carry over" (T9, 10-26). That rests on Fly's daily `piper-morgan-db` snapshots (5-day retention). No restore has ever been tested. The drill proves a restore works and times it.

## Rules that hold for the whole drill

1. **Only xian types the `fly` lines**, in one sitting, in the HOST conversation. HOST runs none.
2. **A new Postgres app made from a snapshot of `piper-morgan-db`.** Never a second machine or volume inside `piper-morgan-db`, never over alpha, never onto staging.
3. **No Piper app boots against the copy.** It would start schedulers and hold real people's grants.
4. **The proofs print counts and ids only.** A restore is a full read of everyone's data. No name, email or credential value is printed, pasted or logged.
5. **The drill is not done until the drill app is destroyed and the app and volume lists are read back showing it gone.**

## HOST's part

- **Before:** ask xian for a window (one sitting, length to be set when Lead's lines exist). Confirm alpha is quiet. Record in the log: who (xian types, HOST logs), when, why (#2157).
- **During:** read each output as xian pastes it. Stop at the first unexpected line and say so. Do not improvise a line that is not in Lead's list.
- **Proofs, in this order** (the commands are Lead's):
  1. The copy exists, and its created-from snapshot time is named.
  2. `alembic current` on the copy matches alpha's.
  3. Row counts for named tables, and one known record by id. Counts compared with alpha's at the time of the snapshot, allowing for rows written since.
  4. One stored credential decrypts with `ENCRYPTION_MASTER_KEY` and prints `ok` or `fail`, nothing else.
- **Timing:** note the clock time at each step so the total restore time is a real number, not an estimate.
- **After (same sitting):** destroy the drill app, then read the app list and the volume list. Quote both reads in the log.
- **Then:** report to Exec, CIO, Lead and Arch: pass or fail per proof, total time, what was destroyed. Close the #2157 drill row in the standing items. Whether the schedule decision stays Production is CIO's.

## Stop conditions

- Any command would touch `piper-morgan` (alpha), `piper-morgan-db`'s volumes or machines, or staging: stop.
- Any output contains a name, email or credential value: stop, do not paste it onward, tell Exec.
- Cleanup read does not show the drill app gone: the drill is not done; say so.

## Not decided here

The Fly CLI flags for create-from-snapshot (Lead confirms against `--help`), the length of the window, and whether the drill repeats after a schema change.
