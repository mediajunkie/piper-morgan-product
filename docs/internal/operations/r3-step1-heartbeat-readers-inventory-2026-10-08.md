# R3 step 1: who reads `dev/heartbeats/` (Exec's half, 2026-10-08)

Purpose: CIO's new reader must replace every consumer below before the git write stops
(`r3-metric.md`: reader agrees with the git reader on 11/11 roles for 3 consecutive days). This is the
list for the rollup build and the START freeze check (Exec's lane), plus the other consumers found on the way.

Method: `git grep -n -E "heartbeats/"` over tracked files, minus dated logs, mailboxes and decisions
history; then opened each hit to classify reader vs writer. Layer measured: source text, not runtime.
Denominator: all tracked non-archive files under `scripts/`, `.claude/`, `docs/internal/`. Not covered:
untracked scripts on PM's desktop, cron/launchd plists outside the repo, and any reader that builds the
path from a variable without the literal `heartbeats/` (grep cannot see those).

## Readers in Exec's two paths

| Path | Reader | Exact read | What it needs from the new surface |
|---|---|---|---|
| START freeze check (duty-cycle-tick Step 2c) | `scripts/cohort-freeze-detect.sh` | line 51 local `HB` dir; line 127 `git ls-tree -r origin/main -- dev/heartbeats/` filtered to `*.tsv` | per-role emission rows inside a window, readable from `origin/main` equivalent (it was changed on 2026-08-09 specifically to stop reading a stale local checkout) |
| Rollup build (cohort-attention-rollup SKILL, ~line 97) | `scripts/duty-cycle-freeze-check.sh` | line 195 `git log origin/main -1 --format=%ct -- dev/heartbeats/*/{role}.tsv` (newest of three liveness signals); lines 383-384 `ls-tree` count of today's files and a 9-day "has the surface ever been written" probe (HEARTBEAT-WRITER-SILENT); line 614 `cat-file -e origin/main:dev/heartbeats/{day}/{role}.tsv` (BELT-INVISIBLE); line 624 `git show origin/main:dev/heartbeats/last-invoked/{role}.txt` | newest-emission timestamp per role; whether today's file exists per role; the last-invoked marker per role; a "surface has ever been written" signal |
| Rollup build (position section) | `scripts/cohort-position.sh` | line 67 `HB_DIR`, lines 116-121 scan `dev/heartbeats/*/{role}.tsv` for the newest timestamp | newest timestamp per role |

Note the freeze check uses commit time (`%ct`) of the file, not the row timestamp. A reader that changes
where rows live changes what "newest" means; the parity test must compare like with like.

## Other consumers (not Exec's lane, listed so none is missed)

- `scripts/usage-lookup.sh` reads `dev/heartbeats/usage-per-account.tsv`; `scripts/usage-capture.sh` writes it (#1862). This file is not a heartbeat; decide whether it stays in git.
- `.claude/skills/duty-cycle-tick/SKILL.md` Step 2c prose describes the reader; update it at cutover.
- Tests that pin the current layout: `scripts/test-duty-cycle-freeze-check.sh` (lines 115-217), `scripts/test-duty-cycle-heartbeat.sh` (lines 41-83), `scripts/test-cohort-position.sh`.
- `scripts/check-unboarded-pm-items.sh` line 65 mentions the directory in a comment only.
- Handoff docs (`docs/handoff-comms-2026-09-29.md:117`) tell agents to verify a heartbeat push with `git show origin/main:dev/heartbeats/...`; stale once the git write stops.

## Writer

`scripts/duty-cycle-heartbeat.sh` (lines 107, 121): writes `dev/heartbeats/{day}/{role}.tsv` and
`dev/heartbeats/last-invoked/{role}.txt`. The `--if-quiet` suppression reads recent commits, so the
new writer needs its own quiet-test or that suppression stops working.

## Parity test Exec can run once CIO has a new reader

For each of the 11 roles, compare the new reader's newest-emission time with
`git log origin/main -1 --format=%ct -- dev/heartbeats/*/{role}.tsv`, three consecutive days. Exec will
run it on request and report the denominator (roles compared out of 11).
