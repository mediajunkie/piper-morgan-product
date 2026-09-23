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
#   0  — ran to completion. A per-account READ FAULT (UNREADABLE/UNMEASURABLE) is recorded as a
#        row, not treated as failure (a cron driver must not see a crash for that).
#   2  — SETUP FAULT: the reader itself is missing/not executable, or this isn't a git checkout.
#        Distinct from a read fault on purpose — nothing is written in this case, for either
#        account, because the writer couldn't run at all.
#
# WHAT'S DELIBERATELY NOT HERE YET (PA review gate, 2026-09-23): this build appends only. It does
# NOT commit or push. See the TODO block below the append for the intended pattern (mirrors
# duty-cycle-heartbeat.sh's commit handling) — do not wire it up until PA has reviewed the append
# logic above it.
#
# D3 — crontab line (NOT installed by this script; a host-level change, Pard's/PM's to make).
# Suggested cadence: every 3h, off-minute, matching "daily, more often near a ceiling" without
# polling. Paste into a real system crontab on Amber (or Pard's equivalent) once approved:
#   23 */3 * * * /Users/xian/Development/piper-morgan-worktrees/pa/scripts/usage-capture.sh >> /tmp/usage-capture.log 2>&1
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
# read fault (UNREADABLE/UNMEASURABLE), which IS recorded (see build_row below).
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
#   (b) UNREADABLE (3-field token)     -> failure row, token verbatim, reason in note
#   (c) UNMEASURABLE (3-field token)   -> failure row, token verbatim, reason in note
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
  elif [ "$n" -eq 3 ] && { [ "${f[1]}" = "UNREADABLE" ] || [ "${f[1]}" = "UNMEASURABLE" ]; }; then
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

# TODO(#1862): commit+push step, deferred to PA review — do NOT wire this up until PA has
# reviewed the append logic above. Once approved, mirror duty-cycle-heartbeat.sh's own commit
# handling (read that script's tail before implementing: explicit-path staging, verify-something-
# staged before claiming success, commit, then fetch+merge+push with retry and a loud, non-silent
# failure — never a broad `git add -A`). Sketch of the intended shape, commented out on purpose:
#
#   git add -- "$TSV"
#   if git diff --cached --quiet -- "$TSV" 2>/dev/null; then
#     echo "usage-capture: nothing staged for $TSV — refusing to report success (m-44)" >&2
#     exit 1
#   fi
#   if git commit -q -m "usage(capture): $(date '+%Y-%m-%d %H:%M %Z')" -- "$TSV" \
#      && git fetch origin main -q \
#      && git merge origin/main --no-edit -q \
#      && git push -q origin HEAD:main; then
#     echo "usage-capture: appended row(s) landed on origin/main"
#   else
#     echo "usage-capture: FAILED to land $TSV on origin/main — investigate now" >&2
#     exit 1
#   fi

exit 0
