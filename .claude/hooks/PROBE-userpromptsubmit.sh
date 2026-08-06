#!/usr/bin/env bash
# SEAT-LOCAL PROBE (CIO 2026-08-05). Pure observation: does UserPromptSubmit fire, and what does it see?
# Writes only to a scratch log. Never blocks, never edits, always exit 0.
# Purpose: establish whether a WRAPPER-WRITTEN heartbeat is possible before proposing one to 11 roles.
IN=$(cat 2>/dev/null)
L="dev/active/probe-userpromptsubmit-cio.log"
{ printf '%s\tfired\tbytes=%s\tmatches_tick=%s\n' \
    "$(date '+%Y-%m-%d %H:%M:%S %Z')" "${#IN}" \
    "$(printf '%s' "$IN" | grep -qi 'DUTY CYCLE TICK' && echo yes || echo no)"
} >> "$L" 2>/dev/null
exit 0
