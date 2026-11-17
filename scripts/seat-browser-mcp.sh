#!/bin/bash
# The browser tool's launcher for .mcp.json (ADR-084 D3 browser half, issue 2400).
#
# A seat with a row in scripts/seat-browser.conf, whose seat browser answers on that row's
# port, gets the browser tool ATTACHED to that browser (--browserUrl): a dedicated browser on
# 127.0.0.1 with a profile that keeps a seeded account's session (scripts/seat_browser.py
# places it). Every other seat, and a seat whose browser is down, gets what .mcp.json started
# before this script existed: a throwaway browser, signed out (--isolated). A seat whose
# browser is down is told so on stderr; Pard's cycle-check arm is what reports it.
#
# The port is read from the conf and nowhere else. `--print` prints the command and exits.
#
# Concept: docs/internal/operations/adr-084-one-time-steps.md. Owner: CIO. Review: 2026-12-16.
set -u
here="$(cd "$(dirname "$0")/.." && pwd -P)"
seat="$(basename "$here")"
conf="$here/scripts/seat-browser.conf"
pin="chrome-devtools-mcp@1.10.1"
binary="/Users/xian/.claude-pm/chrome-for-testing.app/Contents/MacOS/Google Chrome for Testing"

port=""
if [ -r "$conf" ]; then
  port="$(awk -v s="$seat" '{ sub(/#.*/, "") } $1 == s && $2 ~ /^[0-9]+$/ { print $2; exit }' "$conf")"
fi

if [ -n "$port" ] && curl -s -o /dev/null -m 2 --noproxy '*' "http://127.0.0.1:$port/json/version"; then
  mode=(--browserUrl "http://127.0.0.1:$port")
else
  if [ -n "$port" ]; then
    echo "seat-browser-mcp: the seat browser for '$seat' is not answering on 127.0.0.1:$port; starting a throwaway browser (signed out)" >&2
  fi
  mode=("--executablePath=$binary" --isolated --viewport=1280x720)
fi

if [ "${1:-}" = "--print" ]; then
  printf '%s\n' npx "$pin" "${mode[@]}"
  exit 0
fi
exec npx "$pin" "${mode[@]}"
