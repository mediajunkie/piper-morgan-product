# IDLE — state definition

**IDLE is a state, not a procedure.** It has no steps to execute; it has entry conditions, behavior in state, and exit conditions.

**The load-bearing framing**: IDLE is the **PM-collaboration-available state**. Not passive cron-waiting; not "agent is doing nothing." Agent is alive, available, has prepared materials (blockers captured in attention doc), ready for PM to engage.

---

## Entry conditions (how IDLE is reached)

- Mail Loop + Task Loop flywheel terminates at Decision Table state (0, 0): no new mail, no new tasks. Agent has done all available unblocked work.
- WORK pass ends naturally per WORK PARTS step 1 (no-mail shortcut) or step 3 (post-flywheel termination).
- PM-engaged interaction completes (per directed-work-done signal — see below).

## Behavior while in IDLE

### Two sub-states

- **IDLE-passive**: agent is alive, cron-ticking, ready for PM. No active work happening. Cycle log shows "no new arrivals" / "task list at steady state."
- **IDLE-engaged**: PM has engaged with the agent. Agent is responsive, running whatever PM directs:
  - Reviewing blockers in the attention doc together
  - Conversational interaction (Q&A, decisions, design discussions)
  - Joint planning (sprint adjustments, item disposition, etc.)

### Cron continues ticking during IDLE

- CHECK fires at each tick regardless of IDLE sub-state
- During IDLE-passive: CHECK typically dispatches back to WORK PARTS (which runs the no-mail-shortcut quickly and returns to IDLE if nothing changed)
- During IDLE-engaged: CHECK still fires but PM-conversational mode takes precedence over WORK dispatch

## Exit conditions

- **CHECK detects new day** → goto START (transition out of IDLE entirely)
- **CHECK detects > 11pm AND PM not actively talking** → goto STOP (day-close)
- **CHECK detects normal mid-day** → goto WORK PARTS (which usually shortcuts at step 1 and returns to IDLE if still steady state)
- **PM engages during IDLE-passive** → transition to IDLE-engaged
- **PM disengages during IDLE-engaged** → transition to IDLE-passive (per directed-work-done signal)

## Directed-work-done signal (IDLE-engaged → IDLE-passive)

**Tactic for first try (v0.4 decision)**: **infer from silence (~15 min threshold)** + **PM explicit escape hatch**.

- 15-minute silence after last PM message → agent treats as "PM has moved on for now" → returns to IDLE-passive
- PM can say "ok back to idle" / "done for now" / similar at any time to mark a sharper boundary
- If 15 min proves too eager (interrupts mid-thought pauses): lengthen threshold OR require explicit signal only
- If 15 min proves too patient (agent stays engaged when PM has clearly walked): shorten OR add agent "anything else?" probe

## Duration

Indefinite. IDLE can span minutes to hours depending on PM engagement + cohort traffic + cron tick interval.

## Relationship to session lifetime

Under session-scoped cron (HOST + Lead Dev confirmed May 20):
- IDLE persists as long as the Claude Code session persists
- Across a session boundary (app close, machine restart), IDLE state is lost
- On next session-open, agent re-enters via CHECK (typically dispatches to START on new-day morning)

## Cross-references

- `check.md` — the dispatcher that determines when IDLE → some other state
- `work-parts.md` — what CHECK typically dispatches to during IDLE-passive
- `mail-loop.md` / `task-loop.md` — what runs INSIDE WORK PARTS (not in IDLE)
- v0.4 design (where IDLE was reframed) + v0.5 (current canonical)
- Sketch 7 right column — PM activities during IDLE (review blockers, interact, plan)
