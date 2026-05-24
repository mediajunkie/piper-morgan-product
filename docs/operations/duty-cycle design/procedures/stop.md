# STOP — procedure

**Purpose**: day-close ritual. Sync-bracketed close of the day's work.

**Entered from**: CHECK (when dispatcher detects past 11pm AND PM not actively talking).

**Exits to**: end of day (no further procedure runs until next CHECK tick wakes the loop).

**Frequency**: once per calendar day, at end-of-day.

---

## Steps

1. **Sync**
   - `git fetch origin -q && git pull origin main --ff-only`
   - Catches anything new from other agents since last WORK pass

2. **Close out log**
   - Add end-of-day wrap entry to today's session log
   - Brief summary: what shipped today; what's queued for tomorrow; any open threads
   - Per sign-off-discipline in CLAUDE.md: verify no uncommitted work in tracked surfaces; verify branch fully pushed; verify reachable from main
   - Update daily tracker with end-of-day state
   - Update attention doc with end-of-day items still pending PM
   - Commit + push session log + tracker + attention doc updates

3. **Sync**
   - `git push origin main` (if there are local commits)
   - `git fetch origin -q` final verification
   - End

---

## Why the sync-at-both-ends pattern

- **Step 1 sync**: catches anything from origin before close-out (so attention doc reflects truly current state)
- **Step 3 sync**: ensures close-out artifacts (session log wrap, tracker final state, attention doc final state) are pushed before the agent goes quiet

The sync-bracketing is symmetric to STOP's structure on sketch 6 (sync, do, sync). Same pattern used in WORK PARTS (sync before flywheel, sync after).

---

## Conditional execution

STOP only fires when CHECK detects:
- Past 11pm AND
- PM not actively talking (courtesy defer when PM is engaged)

If PM is talking past 11pm, STOP is deferred. CHECK retries on the next tick.

If session ends before STOP fires (e.g., PM closes Claude Code at 10pm), the day's close-out is incomplete; next session-open's START handles the incomplete-log cleanup.

## Cross-references

- `check.md` — dispatcher with the 11pm + not-talking conditional
- `start.md` — symmetric day-open ritual
- `work-parts.md` — what STOP closes after
- CLAUDE.md sign-off-discipline section
- v0.5 design — STOP section
