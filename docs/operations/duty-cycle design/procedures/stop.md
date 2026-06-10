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

2. **Close out BOTH logs + emit the canonical marker** *(skill v1.4/v1.5)*
   - **Wrap the session log** (the durable surface): the day-arc summary (what shipped; what's queued for tomorrow; open threads) + the **memory-eval 3-bucket** (#974: referenced / loaded-but-not-referenced / wanted-but-not-found) *filled, not left as "(fill at wrap)"*.
   - **Emit the canonical close-out marker**: the session-log sign-off section MUST include a literal **`<!-- DAY-CLOSED: {YYYY-MM-DD} -->`** line. This is the grep-able sentinel that START's Step-0 self-heal (and the Lead-owned session-start hook + Docs's merge-keeper sweep) check for to confirm a proper STOP happened. *Without this line, tomorrow's START will treat the day as un-closed and re-run the close.*
   - **Add the day-close entry to the cycle log** too (the ephemeral per-fire record). *A cycle-log day-close is NOT a session-log wrap* — both surfaces get closed (the displacement lesson, m-41).
   - **If the session spanned a day boundary without a STOP** (ran continuously / compacted overnight), the retroactive close MUST still wrap the *prior day's* session log (memory-eval + sign-off + marker), not only its cycle log.
   - Per sign-off-discipline in CLAUDE.md: verify no uncommitted work in tracked surfaces; verify branch fully pushed (`@{u}..HEAD` empty); verify reachable from main (`main..HEAD` empty).
   - Update the attention doc with end-of-day items still pending PM.
   - Commit + push session log + cycle log + attention doc updates.

3. **Sync**
   - `git push origin main` (if there are local commits)
   - `git fetch origin -q` final verification

4. **LEAVE THE CRON ARMED** (added 2026-06-03 — the overnight self-wake fix)
   - **Do NOT end the night cron-deleted.** If you applied Rule-1 CronDelete-FIRST anywhere in this STOP fire, **CronCreate the SAME expression again** (`{offset} 2,4-23 * * *`) as your final action.
   - That static cron then fires the **2am WATCH** and **4am START** on its own — the agent self-wakes next morning, no operator action.
   - **This is the gap that broke the cohort's first overnight (2026-06-02)**: agents ran STOP but several CronDelete'd and never re-armed → no morning fire. Premise: persistent local sessions stay alive overnight (current architecture).
   - **Applies to ALL agents, including Lead** (PM directive 2026-06-03): the workhorse adopts the STOP day-part too — "never STOP" is not the model; "STOP-but-stay-armed" is.

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
