#!/usr/bin/env bash
# log-entry.sh — append a session-log heading with the time read from the clock.
# Concept: docs/internal/operations/hooks-registry.md (the check-branch.sh row). The clock rule: xian's yes
# 2026-11-18, relayed by Comms, on CIO's 11-13 proposal.
# A time nobody types can't be a guess. scripts/stamp_check.py refuses the guesses that are left.
#
#   scripts/log-entry.sh "Mail wake: Exec 01M7..."          -> "## 10:48 Mail wake: Exec 01M7..."
#   scripts/log-entry.sh --role cio "START"                 role given (default: from the worktree name)
#   scripts/log-entry.sh --level 3 "Step A results"         "### 10:48 Step A results"
#
# It writes to today's log for the role, dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-<role>-code-log.md (Pacific),
# and prints the heading it wrote. It never creates a log: with none for today it stops (exit 2), so
# the create-session-log skill stays the one way a log starts. Write the entry's body after it.
# Exit 0 = written; 2 = usage, no log for today, or more than one.

set -euo pipefail

role=""
level=2
while [ $# -gt 0 ]; do
    case "$1" in
        --role) role="${2:-}"; shift 2 ;;
        --level) level="${2:-}"; shift 2 ;;
        -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
        --) shift; break ;;
        -*) echo "log-entry: unknown option $1" >&2; exit 2 ;;
        *) break ;;
    esac
done
title="${*:-}"
if [ -z "$title" ]; then
    echo "log-entry: give the heading's title" >&2
    exit 2
fi
case "$level" in 2|3|4) ;; *) echo "log-entry: --level is 2, 3 or 4" >&2; exit 2 ;; esac

top=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "log-entry: not in a git worktree" >&2; exit 2; }
if [ -z "$role" ]; then
    role=$(basename "$top")
fi
case "$role" in
    *[!a-z]*|"") echo "log-entry: role '$role' is not a plain slug; pass --role" >&2; exit 2 ;;
esac

day=$(TZ=America/Los_Angeles date +%Y-%m-%d)
hhmm=$(TZ=America/Los_Angeles date +%H:%M)
dir="$top/dev/${day:0:4}/${day:5:2}/${day:8:2}"
logs=()
for f in "$dir/$day"-[0-9][0-9][0-9][0-9]-"$role"-code-log.md; do
    [ -f "$f" ] && logs+=("$f")
done
if [ "${#logs[@]}" -eq 0 ]; then
    echo "log-entry: no session log for $role on $day; start one with the create-session-log skill" >&2
    exit 2
fi
if [ "${#logs[@]}" -gt 1 ]; then
    echo "log-entry: more than one $role log for $day: ${logs[*]##*/}" >&2
    exit 2
fi

hashes=$(printf '%*s' "$level" '' | tr ' ' '#')
heading="$hashes $hhmm $title"
printf '\n%s\n\n' "$heading" >> "${logs[0]}"
echo "$heading  -> ${logs[0]#"$top"/}"
