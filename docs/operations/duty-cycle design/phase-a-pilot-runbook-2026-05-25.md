# Phase A Pilot Runbook — first day (2026-05-25 Monday)

**Status**: Pilot run procedure for CIO Phase A first day
**Author**: CIO (Vehicle 2) — prepared 2026-05-24
**Design reference**: `docs/operations/duty-cycle design/duty-cycle-design-v0.5.md`
**Implementation plan reference**: `docs/operations/duty-cycle design/duty-cycle-implementation-plan-v0.1.md` (Phase B item A4)

---

## The pilot run

Tomorrow morning (Monday 2026-05-25), CIO runs the v0.5 duty cycle for the first time. This runbook is the step-by-step + observation-capture for that first day.

---

## Pre-run state (today, 2026-05-24)

- ✅ Procedure docs filed (`docs/operations/duty-cycle design/procedures/*.md`)
- ✅ Task list reframed (`dev/active/cio-standing-items.md` header note added)
- ✅ Attention doc reframed (`dev/active/duty-cycle-escalations-cio.md` header note added)
- ✅ Today's daily tracker created (`dev/2026/05/24/cio-tracker-2026-05-24.md`) — Sunday's instance; tomorrow opens fresh one
- ✅ DESIGN SOLID per PM milestone

## Tomorrow morning — operational procedure

### Step 1: session-open

PM opens Claude Code → fresh CIO session starts. SessionStart hook fires (existing behavior; unread mail counts surface).

### Step 2: agent first action = CHECK

**Manual trigger** (no automatic SessionStart-hook→CHECK wiring yet — Phase C item):

CIO's first message in the new session runs **CHECK** per `procedures/check.md`:
1. Is new day since last check? → YES (May 25 vs May 24 last) → goto START

### Step 3: run START

CIO runs **START** per `procedures/start.md`:
1. Sync (`git fetch origin -q && git pull origin main --ff-only`)
2. **["work in branch"]** — working assumption; try without; observe if gap surfaces
3. Check previous log (`dev/2026/05/24/2026-05-24-0936-cio-code-opus-log.md`) — already wrapped today? if not, close it out
4. Start new log (`dev/2026/05/25/2026-05-25-{HHMM}-cio-code-opus-log.md`)
5. Create today's daily tracker (`dev/2026/05/25/cio-tracker-2026-05-25.md`)
6. Go to WORK

### Step 4: first WORK pass

CIO runs **WORK PARTS** per `procedures/work-parts.md`:
1. If idle, sync with origin/main → end if 0 new messages
2. Run flywheel (Mail Loop → Task Loop) + update log
3. Sync with origin/main → end
4. Return to CHECK (next tick)

### Step 5: subsequent ticks

After first WORK pass ends, CIO is in IDLE-passive. Either:
- PM engages → enter IDLE-engaged → review blockers / interact / plan
- New mail arrives → next CHECK dispatches to WORK → flywheel runs
- Nothing happens → cron tick fires → CHECK → typically dispatches to WORK (no-mail shortcut) → returns to IDLE

### Step 6: end of day

When CHECK detects past 11pm AND PM not actively talking → goto STOP per `procedures/stop.md`:
1. Sync
2. Close out log + tracker + attention doc
3. Sync

---

## Observations to capture (Phase B decision gates)

Throughout the day, capture observations into `dev/active/cio-duty-cycle-pilot-observations-2026-05-25.md` (running doc). Decision gates:

### Day 1 — architectural validation
- Does the basic flow work? (CHECK → START → WORK → IDLE → CHECK → ... → STOP)
- Did manual session-open wake-mechanism trigger correctly?
- Did procedures cross-reference + compose as documented?

### Day 1 calibration items
- **15-min silence threshold for IDLE-engaged → IDLE-passive** — did it feel right? Too eager (interrupted natural pauses)? Too patient (agent stayed engaged when PM clearly walked)?
- **START step 2 "work in branch"** — was there a gap that needed filling? If not, candidate for removal.
- **Daily tracker** — did it add value vs duplicate session log? Did agent actually consult/update it during the day?
- **Three-doc layout** — did the formalizing-not-proliferating principle hold? Did anything want to spawn a parallel new doc?

### Day 2-3
- Does cycle find a sustainable rhythm?
- Does PM's nudge-job reduce as predicted?
- Are blockers actually being captured to attention doc (vs lost in session log noise)?

### Day 4-5
- Is the daily tracker proving useful enough to retain?
- Any operational pain points that warrant a v0.6 design adjustment?

---

## Escape hatches

If something goes wrong:
- **Hard-abort on any step that doesn't match documented procedure** — surface to PM, capture to observations doc, defer / re-design as needed
- **PM explicit override** — PM can always say "skip the cycle for now, do X" and the agent complies; cycle resumes when PM disengages

The pilot is calibration, not commitment — design adjustments based on Phase B findings are expected and welcome.

---

## Optional: 4am cron wake (bonus)

If PM wants to also test the cron-bonus path: set up a CronCreate job at 4:00am that fires CHECK. This is OPTIONAL for Day 1 pilot — manual session-open is sufficient for primary validation. Cron adds the test of "does session persist overnight + does cron fire as expected." Defer if not testing this Day 1; reconsider for Day 2+ if PM wants the parallel evidence.

**Saved question** (for batch resolution): does PM want the 4am cron set up for tomorrow as a bonus test, or skip until manual flow is validated?

---

## Cross-references

- v0.5 design (DESIGN SOLID): `docs/operations/duty-cycle design/duty-cycle-design-v0.5.md`
- Implementation plan v0.1: `docs/operations/duty-cycle design/duty-cycle-implementation-plan-v0.1.md`
- Procedure docs: `docs/operations/duty-cycle design/procedures/*.md`

---

*Pilot runbook prepared 2026-05-24 ~12:42 PT by CIO Vehicle 2. First run targets tomorrow morning 2026-05-25.*
