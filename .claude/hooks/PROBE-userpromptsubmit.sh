#!/usr/bin/env bash
# SEAT-LOCAL PROBE (CIO 2026-08-05). Pure observation: does UserPromptSubmit fire, and what does it see?
# Writes only to a scratch log. Never blocks, never edits, always exit 0.
# Purpose: establish whether a WRAPPER-WRITTEN heartbeat is possible before proposing one to 11 roles.
# 2026-09-28 (standing items 8d/8e): original question answered 08-05. KEPT as a SUBMISSION ledger:
# it timestamps every prompt that was actually SUBMITTED to the model, from outside the model's own
# discipline. ⚠️ LAYER (corrected 09-29 after Pard's evidence): it does NOT see LaunchAgent
# INJECTION. Text typed into a dialog or wizard is never submitted, so it never reaches this hook.
# A gap here means "nothing was submitted," not "nothing fired." Pard's agent log is the injection
# layer. Real case: 09-27 16:07 → 09-28 10:07, three fires were injected into an auto-mode wizard
# and this log showed nothing. Moved from dev/active/ (sprint-cleaned) to dev/state/ (durable).
# RETIRE when the full cohort is on LaunchAgents and Pard's side covers submission too, or on a
# PM/Pard ruling.
L="dev/state/probe-userpromptsubmit-cio.log"
{ printf '%s\tfired\tbytes=%s\tmatches_tick=%s\n' \
    "$(date '+%Y-%m-%d %H:%M:%S %Z')" "${#IN}" \
    "$(printf '%s' "$IN" | grep -qi 'DUTY CYCLE TICK' && echo yes || echo no)"
} >> "$L" 2>/dev/null
exit 0
