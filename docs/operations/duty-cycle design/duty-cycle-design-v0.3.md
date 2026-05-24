# Duty Cycle Design — v0.3

**Status**: Draft v0.3 — page 6 sub-procedures **RATIFIED** by PM walkthrough 2026-05-23 ~23:42 PT (WORK PARTS / CHECK / START / STOP); **IDLE formally defined** new in v0.3; page 7 (CIO CYCLE pseudo-code) walkthrough deferred to 2026-05-24
**Author**: CIO (Vehicle 2)
**Predecessor**: v0.2 (filed 2026-05-23 ~09:30 PT; page 6 sections were PROVISIONAL)
**Changes from v0.2**: WORK PARTS / CHECK / START corrected per PM walkthrough; IDLE section added; v0.2's PROVISIONAL flag on page 6 lifted; page 7 still PROVISIONAL pending tomorrow's walkthrough

---

## North-star intent (unchanged from v0.2)

> *"Wake if idle, check for new incoming messages, check for new tasks. Run the do-things-that-are-not-blocked cycle until everything's blocked. Then make the list of things you need a batch update on — update the doc for my attention. Check for mail again; if there's new mail, do it again. If you have any new tasks, do it again. Only when you get back to zero mail and zero tasks, this loop is done. Go to sleep. If I interrupt them and do stuff, they'll do more stuff. But if I'm busy and working another hour later, it'll wake up. And in the meantime, another agent may have woken up, gotten the message from someone, responded to them, and they can all be talking to each other without me going, 'hey, you've got mail, go check.'"*
>
> — PM to Ted Nadeau, 2026-05-20

---

## Scope (unchanged from v0.2)

When chat is active (local terminal). Cron is session-scoped (HOST + Lead Dev confirmed May 20 that `durable=true` is silently ignored). Manual loop start/stop; automatic-idle-detection is aspiration.

---

## The architecture — page 6 sub-procedures RATIFIED

### Day-parts (top-level)

```
DAY:
  1. START   — day-open ritual (previous-day close + new-day open)
  2. WORK    — the flywheel of mail + task loops
  3. STOP    — day-close ritual (end-of-day sync + log close)
```

### CHECK — the day-part dispatcher (RATIFIED — significant reframing from v0.2)

CHECK is the **dispatcher at the top of every loop tick**, asking *"which day-part should I be in right now?"* and routing accordingly. It is NOT the mail-check (v0.2 had that wrong); the mail-check happens inside the WORK flywheel.

**Steps**:
1. Is new *day* since last check?
2. If yes → goto **START**
3. Is it > 11pm?
4. If yes → goto **STOP** (END)
5. Goto **WORK**

CHECK runs at every loop tick. The Page 7 CIO Cycle pseudo-code's repeated CHECK calls are this dispatcher firing each iteration.

### WORK PARTS — internal structure of the WORK day-part (RATIFIED)

When dispatched to WORK by CHECK, the agent runs:

1. **If idle, sync with origin/main** → **end if 0 new messages** (no-mail shortcut)
2. **Run flywheel** (mail loop + task loop per sketches 1 + 4) + **update log**
3. **Sync with origin/main** → **end**

Each WORK pass has explicit termination at step 1 (shortcut when nothing to do) or step 3 (after flywheel completes). The agent returns to CHECK after WORK ends.

### START — the day-open ritual (RATIFIED — corrected from v0.2)

Triggered when CHECK detects a new day. START handles previous-day cleanup + new-day open:

1. **Sync**
2. **[Step 2 working assumption: "work in branch"]** — PM's best-guess on handwriting; not certain; **may turn out to be a no-op step** (if things work without it, we didn't need it; if needed, the gap will become visible operationally)
3. **Check previous log** → close it out if not finished
4. **Start new log**
5. **Go to WORK**

START's purpose is day-rollover housekeeping. Task work is in WORK, not START.

### STOP — the day-close ritual (RATIFIED)

Triggered when CHECK detects time > 11pm:

1. **Sync**
2. **Close out log**
3. **Sync** (the sync-bracketing pattern — sync, do close-out, sync again)

### IDLE — the waiting state (NEW in v0.3)

IDLE is a **state**, not a sub-procedure (distinct from CHECK/START/WORK/STOP which are procedures). Formal definition:

**Entry conditions** (how IDLE is reached):
- Mail loop + task loop terminate at decision-table state (0, 0) — no new mail, no new tasks
- WORK pass ends naturally (per WORK PARTS step 1 or 3)
- PM interrupt completes (after review-blockers + plans, returns to IDLE)

**Behavior while in IDLE**:
- Passive waiting; no active work
- Periodically (on cron tick or analog), CHECK fires to re-dispatch
- Agent does not consume cycle resources beyond the cron-tick wake

**Exit conditions** (what takes the agent out of IDLE):
- CHECK detects new day → goto START
- CHECK detects time > 11pm → goto STOP
- CHECK detects no day-boundary → goto WORK (which immediately runs the mail-loop-shortcut test; if no new mail, returns to IDLE)
- PM interrupt event (any time) → goto interrupt handler

**Duration**: indefinite. IDLE persists between work bursts; can span minutes to hours depending on PM engagement + cohort traffic.

**Relationship to cron**: under session-scoped cron (current empirically-confirmed reality), IDLE persists only as long as the session persists. When the session ends, IDLE state is lost; on next session-open, the agent re-enters via CHECK at session-start.

---

## Page 7 — CIO CYCLE pseudo-code (PROVISIONAL — walkthrough deferred to 2026-05-24)

My v0.2 second-pass interpretation needs revision now that CHECK is correctly understood as the day-part dispatcher. Tomorrow's walkthrough validates / corrects the orchestration shape. Holding the prior interpretation in v0.2 as historical; v0.3 leaves this section explicitly PROVISIONAL.

---

## Loop 1 (Mail Loop), Loop 2 (Task Loop), Loop-tick Decision Table, Three Per-Agent Docs

Unchanged from v0.2. See `duty-cycle-design-v0.2.md` for full content.

---

## What's retired vs preserved

Unchanged from v0.2. See `duty-cycle-design-v0.2.md`.

---

## Open design questions (status updates from v0.2)

1. ~~Page 6 interpretation~~ — **RATIFIED** v0.3 (with START step 2 as working assumption)
2. **Page 7 interpretation** — deferred to 2026-05-24 walkthrough
3. **Idle detection mechanism** — manual toggle vs automatic (unchanged; aspiration)
4. **Three-doc filename conventions** — unchanged; awaiting PM ratification
5. **Task list = standing-items tracker?** — unchanged; CIO recommendation to reframe existing
6. **Attention doc = escalations file?** — unchanged; CIO recommendation to reframe existing
7. **Wake-mechanism under session-bound cron** — unchanged; manual relaunch at session-start OR session-start-hook-triggered
8. **Branch-and-worktree shape** — TBD; v0.2 architecture pending
9. **Cohort rollout sequencing** — TBD; post-v0.x ratification
10. **PM-attention-doc as MVP value-add** — unchanged; formalize in v0.2+ as canonical

---

## Cross-references

- v0.2 (predecessor): `docs/operations/duty-cycle design/duty-cycle-design-v0.2.md`
- v0.1 (initial draft): `docs/operations/duty-cycle design/duty-cycle-design-v0.1.md`
- Sketches: `docs/operations/duty-cycle design/sketches/` (7 PNG pages)

---

*v0.3 filed 2026-05-23 ~23:55 PT by CIO Vehicle 2. Page 6 RATIFIED; IDLE NEW; page 7 walkthrough deferred to 2026-05-24.*
