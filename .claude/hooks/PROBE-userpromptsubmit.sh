#!/usr/bin/env bash
# SEAT-LOCAL PROBE (CIO 2026-08-05). Pure observation: does UserPromptSubmit fire, and what does it see?
# Writes only to a scratch log. Never blocks, never edits, always exit 0.
# Purpose: establish whether a WRAPPER-WRITTEN heartbeat is possible before proposing one to 11 roles.
# 2026-09-28 (standing items 8d/8e): original question answered 08-05. KEPT for a new question: is
# LaunchAgent tick delivery reliable? This log is the only surface written from outside the model's
# own discipline, so it independently timestamps every tick that actually arrived. It proved the
# 09-27 10:07 → 09-28 16:07 restore gap (no matches_tick=yes rows in between). Moved from dev/active/
# (sprint-cleaned) to dev/state/ (durable machine state). RETIRE when the full cohort is on
# LaunchAgents and two consecutive weeks show no missed tick, or on a PM/Pard ruling.
IN=$(cat 2>/dev/null)
L="dev/state/probe-userpromptsubmit-cio.log"
{ printf '%s\tfired\tbytes=%s\tmatches_tick=%s\n' \
    "$(date '+%Y-%m-%d %H:%M:%S %Z')" "${#IN}" \
    "$(printf '%s' "$IN" | grep -qi 'DUTY CYCLE TICK' && echo yes || echo no)"
} >> "$L" 2>/dev/null
exit 0
