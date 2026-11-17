#!/bin/bash
# The browser tool's launcher for .mcp.json (ADR-084 D3 browser half, issue 2400).
#
# A seat with a row in scripts/seat-browser.conf, whose own seat browser is up, gets the
# browser tool ATTACHED to that browser (--browserUrl): a dedicated browser on 127.0.0.1 with
# a profile that keeps a seeded account's session (scripts/seat_browser.py places it). "Its
# own" is proved by `seat_browser.py --check`, the same proof made before a cookie is placed.
# Every other seat, and a seat whose browser is down or is not provably its own, gets what
# .mcp.json started before this script existed: a throwaway browser, signed out (--isolated).
# The reason goes to stderr, which a seat does not see: Pard's cycle-check arm reports a
# browser that is down, and a seat confirms the signed-in name before any served read.
#
# The port is read from the conf, through the helper, and nowhere else. `--print` prints the command and exits.
#
# Concept: docs/internal/operations/adr-084-one-time-steps.md. Owner: CIO. Review: 2026-12-16.
set -u
here="$(cd "$(dirname "$0")/.." && pwd -P)"
seat="$(basename "$here")"
conf="$here/scripts/seat-browser.conf"
pin="chrome-devtools-mcp@1.10.1"
binary="/Users/xian/.claude-pm/chrome-for-testing.app/Contents/MacOS/Google Chrome for Testing"

# Does this seat have a row? (The port itself comes back from the helper's check below.)
has_row=""
if [ -r "$conf" ]; then
  has_row="$(awk -v s="$seat" '{ sub(/#.*/, "") } $1 == s { print "yes"; exit }' "$conf")"
fi

mode=("--executablePath=$binary" --isolated --viewport=1280x720)
if [ -n "$has_row" ]; then
  # Attach only to a browser the helper proves is this seat's own: one process on 127.0.0.1,
  # the cohort's test browser, on this seat's profile folder (Arch, 2026-11-16). Anything
  # else on the port, xian's own Chrome included, is never attached to.
  if answer="$(python3 "$here/scripts/seat_browser.py" --check "$seat" 2>&1)" && [[ "$answer" =~ ^port\ ([0-9]+)$ ]]; then
    mode=(--browserUrl "http://127.0.0.1:${BASH_REMATCH[1]}")
  else
    echo "seat-browser-mcp: not attaching for '$seat' (${answer:-no answer}); starting a throwaway browser (signed out)" >&2
  fi
fi

if [ "${1:-}" = "--print" ]; then
  printf '%s\n' npx "$pin" "${mode[@]}"
  exit 0
fi
exec npx "$pin" "${mode[@]}"
