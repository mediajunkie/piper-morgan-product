#!/usr/bin/env bash
# seat-prompt.sh — print a seat's exact duty-cycle prompt from its stored file, so a re-arm copies it
# instead of rebuilding it from memory.
#
# Why: 10-29, Exec re-created a dead session cron from memory and dropped a line; Ship #067's kickoff
# went late (xian 10-30: "Let's not rebuild cron jobs from memory!"). The verbatim prompt for every PM
# seat already exists, generated from the registry by Pard's scripts/pm-cascade-provision.sh:
# mediajunkie docs/seat-prompts/pm-<role>.md, between the PROMPT:BEGIN and PROMPT:END markers.
# This reads it from mediajunkie's origin/main (fetched first), never a working copy or anyone's recall.
#
#   scripts/seat-prompt.sh <role>                 # print the prompt (one line), ready for CronCreate
#   scripts/seat-prompt.sh <role> --check <file>  # compare a live prompt (e.g. from CronList) with it
#
# Exit: 0 printed or matched; 1 mismatch (diff shown); 3 couldn't read the stored prompt.
#
# Cost:    one fetch of mediajunkie per call
# Benefit: a re-arm is a copy; a drifted live prompt is caught by a check, not by xian
# Review:  2026-12-14
# Owner:   CIO
# Concept: .claude/skills/duty-cycle-tick/SKILL.md (Step 1, re-arm)
set -euo pipefail

ROLE="${1:-}"; [ -n "$ROLE" ] || { echo "usage: $0 <role> [--check <file>]" >&2; exit 2; }
MJ="${MEDIAJUNKIE:-$HOME/Development/mediajunkie}"
git -C "$MJ" fetch -q origin main 2>/dev/null || { echo "seat-prompt: could not fetch $MJ; stored prompt UNREAD" >&2; exit 3; }
PROMPT="$(git -C "$MJ" show "origin/main:docs/seat-prompts/pm-${ROLE}.md" 2>/dev/null \
  | sed -n '/PROMPT:BEGIN/,/PROMPT:END/p' | sed '1d;$d')" || true
LINES="$(printf '%s' "$PROMPT" | grep -c . || true)"
[ "$LINES" = 1 ] || { echo "seat-prompt: docs/seat-prompts/pm-${ROLE}.md has $LINES prompt lines on origin/main (want 1)" >&2; exit 3; }

if [ "${2:-}" = "--check" ]; then
  [ -f "${3:-}" ] || { echo "usage: $0 <role> --check <file>" >&2; exit 2; }
  if [ "$(tr -d '\n' < "$3")" = "$PROMPT" ]; then
    echo "seat-prompt: $ROLE live prompt matches the stored one"
  else
    echo "seat-prompt: $ROLE live prompt DIFFERS from docs/seat-prompts/pm-${ROLE}.md — re-arm from the stored one" >&2
    diff <(printf '%s\n' "$PROMPT" | tr '.' '\n') <(tr -d '\n' < "$3" | tr '.' '\n') >&2 || true
    exit 1
  fi
else
  printf '%s\n' "$PROMPT"
fi
