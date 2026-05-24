# Duty Cycle Design — v0.4

**Status**: Draft v0.4 — page 7 (CIO CYCLE) **RATIFIED** by PM walkthrough 2026-05-24 ~10:30 PT; IDLE redefined as PM-collaboration-available state; directed-work-done signal tactic selected; session-boundary note added; full initial-ideas set now PM-ratified
**Author**: CIO (Vehicle 2)
**Predecessor**: v0.3 (filed 2026-05-23 ~23:55 PT; page 7 was PROVISIONAL)
**Changes from v0.3**: page 7 RATIFIED; IDLE reframed; right-column reinterpretation (PM activities, not agent procedure); 4:00am trigger time (was 9:00 misread); conditional-STOP-at-11pm; directed-work-done tactic; session-boundary note

---

## North-star intent (unchanged)

> *"Wake if idle, check for new incoming messages, check for new tasks. Run the do-things-that-are-not-blocked cycle until everything's blocked. Then make the list of things you need a batch update on — update the doc for my attention. Check for mail again; if there's new mail, do it again. If you have any new tasks, do it again. Only when you get back to zero mail and zero tasks, this loop is done. Go to sleep. If I interrupt them and do stuff, they'll do more stuff. But if I'm busy and working another hour later, it'll wake up. And in the meantime, another agent may have woken up, gotten the message from someone, responded to them, and they can all be talking to each other without me going, 'hey, you've got mail, go check.'"*
>
> — PM to Ted Nadeau, 2026-05-20

---

## Scope (carries from v0.2/v0.3 with session-boundary note added)

When chat is active (local terminal). Cron is session-scoped (HOST + Lead Dev confirmed May 20). Manual loop start/stop; automatic-idle-detection is aspiration.

### Session boundaries (NEW in v0.4)

Per PM question 2026-05-24: how does a Claude Code session end?

- **PM walks away from laptop**: session persists. REPL stays alive; cron keeps firing.
- **PM closes Claude Code app**: session ends. Cron dies.
- **Laptop sleeps briefly**: session usually persists through wake.
- **Laptop sleeps for hours, especially with network change**: uncertain — empirically observed (HOST/Lead Dev) that cron does not survive overnight gaps.
- **Machine restart / app crash / force-quit**: session ends.

**Practical implication for the duty cycle**: the 4:00am wake is reliable only IF the previous session genuinely persisted overnight. Realistic morning entry is "PM opens Claude Code → session starts → CHECK fires at session-open → START runs if new day." The 4am cron trigger is best-effort for the persistent-session case.

---

## The architecture — page 6 + page 7 BOTH RATIFIED

### Day-parts (top-level)

```
DAY:
  1. START   — day-open ritual (previous-day close + new-day open)
  2. WORK    — the flywheel of mail + task loops
  3. STOP    — day-close ritual (sync + log close + sync)
```

### CHECK — the day-part dispatcher (RATIFIED v0.3)

CHECK is the **dispatcher at the top of every loop tick**, asking *"which day-part should I be in right now?"* and routing accordingly. NOT the mail-check (mail-check happens inside WORK).

**Steps**:
1. Is new *day* since last check?
2. If yes → goto **START**
3. Is it > 11pm?
4. If yes AND PM is not actively talking → goto **STOP** (new in v0.4: conditional on PM-engagement state)
5. Goto **WORK**

The 11pm STOP is courtesy-deferred when PM is engaged. Day ends gracefully when PM disengages.

### WORK PARTS — internal structure of the WORK day-part (RATIFIED v0.3)

1. **If idle, sync with origin/main** → **end if 0 new messages** (no-mail shortcut)
2. **Run flywheel** (mail loop + task loop per sketches 1 + 4) + **update log**
3. **Sync with origin/main** → **end**

Each WORK pass returns to CHECK after ending.

### START — the day-open ritual (RATIFIED v0.3)

1. **Sync**
2. **[Step 2 working assumption: "work in branch"]** — PM uncertain on handwriting; may be no-op operationally
3. **Check previous log** → close it out if not finished
4. **Start new log**
5. **Go to WORK**

### STOP — the day-close ritual (RATIFIED v0.3)

1. **Sync**
2. **Close out log**
3. **Sync**

### IDLE — the PM-collaboration-available state (RATIFIED + REFRAMED v0.4)

IDLE is **NOT just passive waiting for cron**. IDLE is the **PM-collaboration-available state** — the agent is alive, available, and has prepared materials (blockers captured in attention doc) ready for PM to engage with.

**Entry conditions**:
- Mail loop + task loop flywheel terminates at (0, 0) — no new mail, no new tasks
- WORK pass ends naturally (per WORK PARTS step 1 or 3)
- PM-engaged interaction completes (per directed-work-done signal)

**Behavior while in IDLE**:
- **PM-available**: PM may engage at any time during IDLE for:
  - Reviewing blockers prepared in the attention doc
  - Interactive conversation with the agent
  - Joint planning
- **Agent-available**: agent is responsive to PM messages; runs whatever PM directs
- **Cron-ticking**: periodically, CHECK fires (cron-driven heartbeat) to re-dispatch per day-part
- **When PM engages → agent is in IDLE-engaged sub-state**
- **When PM disengages → agent returns to IDLE-passive sub-state**

**Exit conditions**:
- CHECK detects new day → goto START
- CHECK detects >11pm AND PM not actively talking → goto STOP
- CHECK detects normal day-mid → goto WORK (which runs mail-shortcut test; if no new mail, returns to IDLE)
- (PM-interaction during IDLE doesn't "exit" IDLE — it puts agent in IDLE-engaged sub-state; agent returns to IDLE-passive when directed work is done)

**Duration**: indefinite. IDLE can span minutes to hours depending on PM engagement + cohort traffic + cron tick interval.

**Relationship to cron**: under session-scoped cron, IDLE persists only as long as session persists. Across session boundary, IDLE state is lost; re-entered via CHECK at session-open.

### Right column of page 7 — PM activities during IDLE (RATIFIED v0.4)

The right column of sketch 7 ("review blockers" + "plans") is **NOT an agent-side event handler**. It depicts what **PM does during IDLE**:

```
PM during IDLE:
  - reviews blockers prepared in attention doc
  - interacts with agent
  - makes plans
  → agent returns to IDLE-passive when PM disengages
```

This is the load-bearing **PM-batching surface** — PM scans the attention doc + interacts when bandwidth permits. The IDLE state is what makes this collaboration mode possible.

---

## Page 7 — CIO CYCLE pseudo-code (RATIFIED v0.4)

```
TRIGGER: @4:00am — if loop not already running, start loop
         (idempotent restart guard kept as defensive; session-scoped cron
          means previous day's loop typically already dead, but cheap insurance)

procedure day_cycle():
    CHECK    # initial dispatch: detects new day → goto START
    START    # day-open ritual
    WORK     # first WORK pass
    [idle...]  # clock icon = automatic-cycle-repeat indicator
    
    loop:
        CHECK    # tick dispatcher: not new day, not past 11pm → goto WORK
        WORK     # another WORK pass (may shortcut at step 1 no-mail)
        IDLE     # PM-collaboration-available state
        # back to CHECK (cron tick fires)
    
    CHECK    # terminal tick: detects past 11pm AND PM not actively talking
    STOP     # day-close ritual

EVENT during IDLE (not an interrupt; PM-collaboration mode):
  PM may engage with agent:
    - review blockers (from attention doc)
    - interact with agent
    - make plans together
  PM disengages → agent returns to IDLE-passive
  (signaled by: silence > ~15 min threshold; or PM explicit "back to idle";
   see "Directed-Work-Done Signal" section below)
```

The clock/pie-chart icon between WORK and IDLE (and the curved arrow back from IDLE up to CHECK) confirms the inner-loop body is **CHECK → WORK → IDLE** repeating automatically through the day.

### Directed-work-done signal (NEW in v0.4)

When PM engages during IDLE, agent enters IDLE-engaged sub-state. When does agent return to IDLE-passive?

**Tactic chosen for first try**: **infer from silence (~15-min threshold)** + **PM explicit signal as escape hatch**.

Rationale: 15-min silence requires no new ritual; uses the existing conversational rhythm. Generous enough to not interrupt natural reading/thinking pauses; short enough that agent returns within a coffee break.

**Escape hatch**: PM can say "ok back to idle" / "done for now" / similar at any time for a sharper boundary.

**If 15 min proves too eager**: shift to longer threshold OR require PM explicit signal (tactic a).
**If 15 min proves too patient**: shorten threshold OR add agent "anything else?" probe (tactic d).

---

## Loop 1 (Mail Loop), Loop 2 (Task Loop), Loop-tick Decision Table, Three Per-Agent Docs

Unchanged from v0.2 / v0.3. See `duty-cycle-design-v0.2.md` for the canonical Mail/Task/Decision-Table/Three-Doc content (all carried forward; not duplicated here).

---

## What's retired vs preserved

Unchanged from v0.2 / v0.3.

---

## Open design questions (status updates)

1. ~~Page 6 interpretation~~ — **RATIFIED** v0.3
2. ~~Page 7 interpretation~~ — **RATIFIED** v0.4 (this version)
3. ~~Directed-work-done signal~~ — **DECIDED** v0.4 (silence + explicit escape hatch)
4. ~~Session-boundary semantics~~ — **DOCUMENTED** v0.4 (session ≠ PM presence at laptop)
5. **Idle detection mechanism for cycle-launch** — unchanged; manual toggle vs automatic (aspiration)
6. **Three-doc filename conventions** — unchanged; awaiting PM ratification
7. **Task list = standing-items tracker?** — unchanged; CIO recommendation to reframe existing
8. **Attention doc = escalations file?** — unchanged; CIO recommendation to reframe existing
9. **Wake-mechanism under session-bound cron** — unchanged; manual relaunch at session-start OR session-start-hook-triggered (4am cron is best-effort)
10. **Branch-and-worktree shape** — TBD; v0.4 architecture TBD
11. **Cohort rollout sequencing** — TBD; post-stable-canonical
12. **START step 2 ("work in branch" working assumption)** — may turn out to be no-op; revisit operationally

---

## Status of initial-ideas-set

With page 6 RATIFIED (v0.3) + page 7 RATIFIED (v0.4) + IDLE reframed + directed-work-done tactic decided + session-boundary documented, **PM's initial ideas are now fully set and clear to both CIO and PM** per PM's stated milestone.

Next-stage work (post-PM-review of v0.4):

- Resolve the remaining open design questions (5-12 above) — most are operational specifications rather than architectural choices
- Translate v0.4 into an implementation plan (cohort adoption proposal; per-role parameterization; rollout sequence)
- Re-engage cohort adopters (HOST + Docs) with the new design once v0.x stabilizes
- Build the canonical templates for the three per-agent docs (tracker / task list / attention)

---

## Cross-references

- v0.3 (predecessor): `docs/operations/duty-cycle design/duty-cycle-design-v0.3.md`
- v0.2: `docs/operations/duty-cycle design/duty-cycle-design-v0.2.md`
- v0.1 (initial draft): `docs/operations/duty-cycle design/duty-cycle-design-v0.1.md`
- Sketches: `docs/operations/duty-cycle design/sketches/` (7 PNG pages)

---

*v0.4 filed 2026-05-24 ~10:45 PT by CIO Vehicle 2. Page 7 RATIFIED; IDLE reframed as PM-collaboration-available; directed-work-done tactic = silence threshold + escape hatch; session-boundary documented; initial-ideas set CLEAR per PM stated milestone.*
