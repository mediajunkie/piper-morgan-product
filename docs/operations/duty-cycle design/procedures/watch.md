# WATCH — procedure

**Purpose**: the single overnight check between STOP and START. A night-watchman round — catch anything genuinely urgent without the churn of hourly no-op fires.

**Added**: 2026-06-03 (overnight-continuity v2). Part of the static-cron design `{offset} 2,4-23 * * *` (STOP 11pm → silent → WATCH ~2am → START 4am → hourly day).

**Entered from**: CHECK, when the dispatcher detects the ~2am fire (after STOP, before the 4am START) on a day that already STOPped.

**Frequency**: once per night.

---

## Steps

1. **Quick mail-check only** — `ls mailboxes/{role}/inbox/` (awareness, ~30s). No drain, no substantive work by default.
2. **Triage urgency**:
   - Nothing urgent (the norm) → append a one-line WATCH no-op entry to the cycle log, **leave cron armed**, exit. Near-zero tokens.
   - Genuinely urgent (rare — e.g. a blocking cross-agent escalation that can't wait for 4am) → handle the minimum, then return to quiet. Apply Rule 1 (CronDelete-FIRST) if it goes substantive, and **re-arm the same expression** before exiting.
3. **Leave cron armed** so the 4am START fires.

## Audit visibility: WATCH + START always commit a one-line entry (Exec finding 2026-06-04)

Many agents **batch consecutive clean-IDLE fires** (don't commit a per-fire cycle-log entry for each no-op — a reasonable token-saving convention). The cost: a cohort audit that counts *committed* cycle-log entries will **under-count overnight self-wake events** — the WATCH/START fired into session response surface but left no committed trace, so the agent looks like it went dark when it actually self-woke (Exec 2026-06-04 was mis-classified this way).

**Rule**: even under a batched-quiet convention, the **WATCH and START fires commit a one-line entry each** (small token cost, big audit-visibility benefit). They're the overnight-self-wake markers — the exact events an audit needs to see. Daytime quiet-holds may still batch; the overnight pair must not. (CIO's per-fire-commit habit already satisfies this; this rule generalizes it to the minimum every shape should meet.)

## Why one watch, not hourly

PM directive 2026-06-03: "just one watch between stop and start, ideally." Hourly overnight fires are mostly no-op churn; a single ~2am watch catches urgent overnight signal at ~1/5th the fire count. The static cron `{offset} 2,4-23 * * *` produces exactly one fire (hour 2) between the 11pm STOP and the 4am START.

## Cross-references
- `check.md` — dispatcher (routes the 2am fire here)
- `stop.md` / `start.md` — the bracketing day-parts
- `cron-lifecycle.md` — Rule 1 (if a watch goes substantive)
