#!/usr/bin/env bash
# usage-capture.sh — writer for dev/heartbeats/usage-per-account.tsv (issue #1862)
#
# WHY THIS EXISTS: 2026-09-14, 48 subagent dispatches from one seat silently inherited a shared
# account ceiling and exhausted it, silently darkening two roles that dispatched nothing. Two
# durable gaps: no attribution of who consumed what, and a ceiling-refused seat is indistinguishable
# from a dead one. This script writes one honest row per (account, reading) so a later lookup
# answers "was the account near ceiling when this seat went quiet?" without forensic reconstruction.
# Full context: dev/active/usage-per-account-capture-2026-09-19.md (Lead's proposal) and
# dev/active/usage-per-account-capture-build-spec-2026-09-23.md (PA's build spec, this script's spec).
#
# WHAT IT DOES NOT DO: re-implement the usage endpoint call. It shells out to Pard's reader
# (~/Development/mediajunkie/scripts/usage-read.sh), which is the one place the OAuth token is
# ever touched (keychain read, use-time only, never cached, never printed). This script never
# calls `security` itself and never sees the token.
#
# ACCOUNTS CAPTURED (seat -> config-dir topology, verified by Pard 2026-09-23 — see the companion
# comment block at the bottom of dev/heartbeats/usage-per-account.tsv for the full seat roster):
#   pipermorgan.ai      <- CLAUDE_CONFIG_DIR=~/.claude-pm  (all 11 PM seats)
#   designinproduct.com <- CLAUDE_CONFIG_DIR=~/.claude     (Pard, Janus, small projects)
# Exactly two rows per reading, not one per seat.
#
# USAGE
#   scripts/usage-capture.sh [--reader PATH] [--dry-run]
#     --reader PATH   override the reader script (default: mediajunkie's usage-read.sh below).
#                      Tests point this at a stub — never invent a second endpoint-call path.
#     --dry-run        print the rows this run would append; touch nothing.
#
# EXIT CODES
#   0  — ran to completion. A per-account READ FAULT (any reader mode label) is recorded as a
#        row, not treated as failure (a cron driver must not see a crash for that).
#   2  — SETUP FAULT: the reader itself is missing/not executable, or this isn't a git checkout.
#        Distinct from a read fault on purpose — nothing is written in this case, for either
#        account, because the writer couldn't run at all.
#
# COMMIT/PUSH IS THE DRIVER'S, NOT THIS SCRIPT'S. This script appends only. The driver (Pard-owned,
# installed 2026-09-23 as LaunchAgent `com.xian.usage-capture`, every 3h at :23, dedicated worktree
# ~/Development/piper-morgan-worktrees/usage-capture, declared in mediajunkie/docs/schedules.md)
# pulls --ff-only, runs this, commits the one TSV path, pushes to origin/main, and logs a verdict
# (`ok rows+N (M non-reading) pushed <sha>` | NO-ROWS | UNMEASURABLE | REFUSED | SETUP-FAULT) to
# ~/Development/mediajunkie/logs/usage-capture.log. A driver must never run inside an agent's live
# worktree or PM's main checkout. If you need to run this by hand from any checkout: run it, then
# `git add dev/heartbeats/usage-per-account.tsv` and commit that one path.
#
# Explicitly NOT in scope (unchanged from Lead's proposal / PA's spec): automated enforcement,
# per-request metering inside Piper, any change to model-pinning policy, installing the crontab
# above, wiring the D4 lookup into the freeze-watchdog's output.

set -uo pipefail

READER="$HOME/Development/mediajunkie/scripts/usage-read.sh"
DRY_RUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --reader)
      [ $# -ge 2 ] || { echo "usage-capture: --reader requires a PATH argument" >&2; exit 2; }
      READER="$2"; shift 2 ;;
    --dry-run)
      DRY_RUN=1; shift ;;
    -h|--help)
      echo "usage: $0 [--reader PATH] [--dry-run]"; exit 0 ;;
    *)
      echo "usage-capture: unrecognized argument: $1" >&2
      echo "usage: $0 [--reader PATH] [--dry-run]" >&2
      exit 2 ;;
  esac
done

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -n "$ROOT" ] || { echo "usage-capture: not inside a git repo — cannot locate dev/heartbeats/" >&2; exit 2; }
TSV="$ROOT/dev/heartbeats/usage-per-account.tsv"

# SETUP FAULT, not a read fault: the reader is a hard dependency. If it's missing, nothing about
# either account can be known, so nothing is written for either — distinct from a per-account
# read fault (any reader mode label), which IS recorded (see build_row below).
if [ ! -f "$READER" ] || [ ! -x "$READER" ]; then
  echo "usage-capture: SETUP FAULT — reader not found or not executable at: $READER" >&2
  echo "usage-capture: this is distinct from a per-account read fault; nothing written for either account." >&2
  exit 2
fi

READER_NAME="$(basename "$READER")"
NUM_RE='^[0-9]+(\.[0-9]+)?$'

# The two (account, config_dir) pairs this build covers. config_dir here is the literal string
# passed to the reader and written to the TSV column — the reader itself expands ~ internally for
# the keychain-service derivation, but the column we record is the one a human recognizes.
ACCOUNTS=(
  "pipermorgan.ai|~/.claude-pm"
  "designinproduct.com|~/.claude"
)

sanitize() {
  # Collapse embedded tabs/newlines so a note field can never fracture the TSV's column count.
  printf '%s' "$1" | tr '\t\n\r' '   '
}

# Builds and prints exactly one TSV row for one (account, config_dir) pair, reading live.
# Handles the four reader outcomes named in the build spec:
#   (a) a good 5-field line            -> real numbers, note empty
#   (b)/(c) a 3-field MODE line        -> failure row, the reader's mode label verbatim in the
#                                          five_hour_pct column, reason in note. The label is any
#                                          UPPER-CASE-HYPHEN token, not a fixed list: the reader's
#                                          vocabulary grew on 2026-09-23 (UNREADABLE, UNMEASURABLE,
#                                          then AUTH-REFUSED, TRANSIENT, SHAPE-CHANGED,
#                                          EXPIRED-TOKEN) and a fixed list here flattened the first
#                                          real SHAPE-CHANGED (09-24 00:23) into UNMEASURABLE. The
#                                          four failures are not the same failure; the column must
#                                          say which. Rows before 2026-09-24 07:xx carry the old
#                                          collapse — their note still holds the reader's real label.
#   (d) anything else (garbage)        -> failure row, ALWAYS as UNMEASURABLE — never a
#                                          plausible-looking number, per the build spec's AC.
build_row() {
  local account="$1" cfgdir="$2" ts line
  ts="$(date '+%Y-%m-%d %H:%M %Z')"
  line="$("$READER" "$cfgdir" 2>&1)"

  local IFS=$'\t'
  local -a f
  read -r -a f <<< "$line"
  unset IFS
  local n=${#f[@]}

  if [ "$n" -eq 5 ] && [[ "${f[1]}" =~ $NUM_RE ]] && [[ "${f[3]}" =~ $NUM_RE ]]; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
      "$ts" "$account" "$cfgdir" "${f[1]}" "${f[2]}" "${f[3]}" "${f[4]}" "$READER_NAME" ""
  elif [ "$n" -eq 3 ] && [[ "${f[1]}" =~ ^[A-Z][A-Z0-9-]{2,}$ ]]; then
    local note; note="$(sanitize "${f[2]}")"
    printf '%s\t%s\t%s\t%s\t\t\t\t%s\t%s\n' \
      "$ts" "$account" "$cfgdir" "${f[1]}" "$READER_NAME" "$note"
  else
    # Garbage / unrecognized shape — never allowed to masquerade as a real percentage (AC (d)).
    local note; note="$(sanitize "reader output not recognized: $line")"
    printf '%s\t%s\t%s\tUNMEASURABLE\t\t\t\t%s\t%s\n' \
      "$ts" "$account" "$cfgdir" "$READER_NAME" "$note"
  fi
}

rows=()
for pair in "${ACCOUNTS[@]}"; do
  account="${pair%%|*}"
  cfgdir="${pair#*|}"
  rows+=("$(build_row "$account" "$cfgdir")")
done

if [ "$DRY_RUN" -eq 1 ]; then
  printf '%s\n' "${rows[@]}"
  exit 0
fi

mkdir -p "$(dirname "$TSV")"
if [ ! -f "$TSV" ]; then
  printf 'ts_local\taccount\tconfig_dir\tfive_hour_pct\tfive_hour_reset\tseven_day_pct\tseven_day_reset\tsource\tnote\n' > "$TSV"
fi
printf '%s\n' "${rows[@]}" >> "$TSV"
echo "usage-capture: appended ${#rows[@]} row(s) to $TSV" >&2

exit 0
