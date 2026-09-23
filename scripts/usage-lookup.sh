#!/usr/bin/env bash
# usage-lookup.sh — the reader-side lookup, and the reason dev/heartbeats/usage-per-account.tsv
# exists (build spec D4, issue #1862).
#
# Answers, in one command, the question the 2026-09-14 incident took a forensic reconstruction to
# get: "was this account near ceiling when a seat went quiet?"
#
# USAGE
#   scripts/usage-lookup.sh "<YYYY-MM-DD HH:MM>" [account]
#
# Prints the most recent row at or before the given local timestamp, for the given account
# (default: pipermorgan.ai). Prints the literal string NO-ROW (never empty output — silence must
# stay diagnostic, same G6 principle the surface itself is built on) if no such row exists.
#
# Skips `#`-prefixed comment lines and the header row. Does NOT integrate with
# duty-cycle-freeze-check.sh — that's a separate, CIO/HOST-owned decision (build spec D4); this is
# a one-line change for them to make later, not made here.
set -uo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 \"<YYYY-MM-DD HH:MM>\" [account]" >&2
  exit 2
fi
TARGET="$1"
ACCOUNT="${2:-pipermorgan.ai}"

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$ROOT" ] || { echo "usage-lookup: not inside a git repo — cannot locate dev/heartbeats/" >&2; exit 2; }
TSV="$ROOT/dev/heartbeats/usage-per-account.tsv"

if [ ! -f "$TSV" ]; then
  echo "NO-ROW"
  exit 0
fi

best_ts=""
best_line=""
while IFS=$'\t' read -r ts acct rest; do
  [ -n "${ts:-}" ] || continue
  case "$ts" in
    \#*) continue ;;
  esac
  [ "$ts" = "ts_local" ] && continue   # header
  [ "$acct" = "$ACCOUNT" ] || continue

  ts_prefix="${ts:0:16}"               # "YYYY-MM-DD HH:MM" — comparable lexically, same width
  [[ "$ts_prefix" > "$TARGET" ]] && continue   # strictly after target — not eligible

  if [ -z "$best_ts" ] || [[ "$ts_prefix" > "$best_ts" ]] || [[ "$ts_prefix" == "$best_ts" ]]; then
    best_ts="$ts_prefix"
    best_line="$ts	$acct	$rest"
  fi
done < "$TSV"

if [ -z "$best_line" ]; then
  echo "NO-ROW"
else
  printf '%s\n' "$best_line"
fi
