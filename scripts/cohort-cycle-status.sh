#!/usr/bin/env bash
# cohort-cycle-status.sh — DERIVED cohort duty-cycle status
#
# methodology-36 (Derived Views Over Hand-Maintained Trackers) Class-1 fix.
# READ-ONLY. Derives "who's cycling today" from signals that DON'T go stale —
# cycle-log presence + git worktree list — complementing the hand-maintained
# `docs/operations/duty-cycle design/cohort-agent-status.md` (which goes stale by
# construction; that staleness is exactly what m-36 is about).
#
# What it CAN derive: per-role cycle-log-today presence (filename carries the role,
# so this is reliable) + named worktrees.
# What it CANNOT derive: cron-live status — the cron is session-scoped, so CronList
# only works inside the agent's own session, never remotely. (This is why the
# hand-maintained tracker's "cron-live" claims silently went stale — Arch's expired
# 5/28 and the tracker didn't know. The honest derived view simply omits that column.)
#
# Usage: scripts/cohort-cycle-status.sh   (no args; reads the repo it's run in)
# (no `set -e`/pipefail — greps legitimately no-match here; this is a read-only display)

ROOT="$(git rev-parse --show-toplevel)"
TODAY="$(date +%Y-%m-%d)"
ROLES="arch exec pa cio ppm cxo docs lead host comms web"

echo "Derived cohort duty-cycle status — $TODAY"
echo "(read-only; derived from cycle-log presence + worktree list. Cron-live is NOT derivable remotely.)"
echo
printf "%-7s %-15s %s\n" "ROLE" "CYCLING-TODAY?" "NAMED WORKTREE"
printf "%-7s %-15s %s\n" "----" "--------------" "--------------"

WTREES="$(git -C "$ROOT" worktree list --porcelain 2>/dev/null | awk '/^branch /{print $2}' | sed 's|refs/heads/||')"

for r in $ROLES; do
  if ls "$ROOT"/dev/active/cycle-log-"$r"-"$TODAY".md >/dev/null 2>&1; then cyc="YES"; else cyc="no"; fi
  wt="$(printf '%s\n' "$WTREES" | grep -iE "(^|/)${r}-cycle$" | tr '\n' ',' | sed 's/,$//')"
  [ -z "$wt" ] && wt="(none named — may be on an ephemeral auto-worktree; see tracker slug->role map)"
  printf "%-7s %-15s %s\n" "$r" "$cyc" "$wt"
done

echo
echo "'no' = no cycle-log for today yet (pre-START, off-cycle by work-shape, or not-launched)."
echo "Cron-live: run CronList inside the agent's own session — not visible from here."
echo "Canonical hand-maintained view (cron + work-shape + carry-in): docs/operations/duty-cycle design/cohort-agent-status.md"
