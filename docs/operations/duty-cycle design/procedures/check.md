# CHECK — procedure

**Purpose**: day-part dispatcher. At every loop tick, ask *"which day-part should I be in right now?"* and dispatch accordingly.

**Entered from**:
- Initial wake (4am cron OR manual session-open)
- End of WORK PARTS (each WORK pass returns to CHECK)
- End of IDLE-engaged (after PM disengages, CHECK fires at next cron tick)

**Exits to**: START, WORK, or STOP based on dispatcher logic.

**Frequency**: every loop tick. CHECK is the most-frequently-running sub-procedure.

---

## Steps

1. **Is new *day* since last check?**
   - Compare current date to date of last CHECK (or last STOP) execution
   - "New day" means calendar date has changed

2. **If yes → goto START**
   - Exit CHECK; run START sub-procedure (day-open ritual)

3. **Is it > 11pm?**
   - Compare current local time to 23:00

4. **If yes AND PM is not actively talking → goto STOP**
   - "Not actively talking" check: has PM sent a message in the last ~5-10 minutes?
   - If PM engaged → STOP is courtesy-deferred; fall through to step 5
   - If PM not engaged → exit CHECK; run STOP sub-procedure (day-close ritual)

5. **Goto WORK**
   - Default dispatch: exit CHECK; run WORK PARTS sub-procedure
   - WORK PARTS may shortcut at step 1 (no-mail) and return quickly

---

## What CHECK is NOT

- NOT the mail-check (v0.2 had this wrong; corrected in v0.3+)
- NOT a procedure that does work itself — pure dispatcher
- NOT executed by the agent reading messages or doing tasks — it's the gatekeeper logic

## When CHECK runs

CHECK fires at every loop tick. The cron tick interval is configurable (V1 era used hourly; v0.5 design defers cadence to operational discovery). For the CIO pilot Phase A:

- Manual session-open → CHECK fires as first agent action
- During WORK pass → CHECK fires when WORK PARTS exits (return-to-dispatcher)
- During IDLE-passive → CHECK fires periodically (cron tick OR equivalent)
- During IDLE-engaged → CHECK fires periodically but typically dispatches back to WORK or stays in IDLE

## Cross-references

- `start.md` — what CHECK dispatches to on new-day
- `stop.md` — what CHECK dispatches to past-11pm + not-talking
- `work-parts.md` — default dispatch
- `idle.md` — state agent enters when WORK ends without re-dispatch
- v0.5 design — CHECK section
