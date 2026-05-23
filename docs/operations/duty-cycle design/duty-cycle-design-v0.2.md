# Duty Cycle Design — v0.2

**Status**: Draft v0.2 — synthesizes PM sketches 1-7 + image-by-image walkthrough notes (sketches 1-5, narrated May 20) + CIO second-pass interpretation of sketches 6 + 7 (PROVISIONAL — awaiting PM ratification on brief check-in) + Ted/Englishia north-star prose + V1-era lessons preserved
**Author**: CIO (Vehicle 2)
**Predecessor**: v0.1 (filed 2026-05-20; pages 6 + 7 flagged as pending)
**Sketches**: `docs/operations/duty-cycle design/sketches/` (7 PNG pages)
**Provisional sections**: clearly marked **(PROVISIONAL — awaiting PM validation)** where my interpretation is still hypothesis-form

---

## North-star intent (PM's prose to Ted Nadeau, 2026-05-20)

> *"Wake if idle, check for new incoming messages, check for new tasks. Run the do-things-that-are-not-blocked cycle until everything's blocked. Then make the list of things you need a batch update on — update the doc for my attention. Check for mail again; if there's new mail, do it again. If you have any new tasks, do it again. Only when you get back to zero mail and zero tasks, this loop is done. Go to sleep. If I interrupt them and do stuff, they'll do more stuff. But if I'm busy and working another hour later, it'll wake up. And in the meantime, another agent may have woken up, gotten the message from someone, responded to them, and they can all be talking to each other without me going, 'hey, you've got mail, go check.'"*

That's the canonical one-paragraph statement of what the duty cycle is for. Everything below is the elaboration that makes it operational.

---

## Scope

**When chat is active (local terminal)** — the duty cycle runs *inside* a live Claude Code session in a local terminal. It does **not** launch entirely fresh sessions; that's a future-state aspiration.

Bounded to:
- Local-terminal chat sessions that are already alive
- Agent-driven loop start/stop (manual at first; automatic-on-idle is aspiration)
- Cohort agents running their own per-role cycles in their own local sessions

Out of scope for v0.2:
- Cloud/Routines-based autonomous sessions (V2-future path)
- Email/SMTP/agentmail-style delivery queuing (V2+ infrastructure; PM flagged as eventual need)
- Cross-session cron durability — **empirically confirmed unavailable** (HOST + Lead Dev May 20: CronCreate `durable=true` is silently ignored; all cron jobs are session-scoped). Design must work within this constraint.

---

## The architecture (three loops + bookended day)

The duty cycle is **two loops composed into a flywheel**, day-bookended by START / STOP rituals, with a PM-interrupt event handler.

### Day-parts (top-level structure, from sketch 6)

```
DAY:
  1. START   — ritual at session-open / day-begin
  2. WORK    — the flywheel of mail + task loops
  3. STOP    — ritual at session-close / day-end
```

Each day-part has internal structure (defined below). SYNC bookends multiple junctions inside each part.

### Loop 1: Mail Loop (sketch 1)

**Purpose**: detect new mail; triage into the task list; clear inbox.

**Trigger**: agent is idle (chat session alive but PM not actively engaged). Started manually for v0.2 era (agent launches loop when PM takes a break, cancels when PM interrupts). Future: automatic idle-detection.

**Steps**:

1. **Sync** — `git fetch origin -q` + reconcile with `origin/main`. Sweep other agents' branches in case they sent mail without syncing (compensates for strict-per-memo-commit-push gaps).
2. **Check mail** — enumerate inbox files on origin/main + swept branches. If no new mail since last check, **end loop** (transition to task loop or terminate).
3. **Read mail** — Postel 3-tier extract `from / subject / to / cc / response-requested` per methodology-32 (with response-requested as Tier 1 + case-insensitive YAML key matching per the two May 18 Docs refinements queued for kit incorporation).
4. **Sort + clear inbox** (step 3.5: clear inbox) — classify each new memo into:
   - Tasks (unblocked vs need-input → added to task list)
   - Informational (acknowledge + move to read/)
   - Cohort-visible info (CC copies; move to read/)
   - Move processed memos to `read/` as part of this step.
   - This is what makes the loop a TRIAGE loop, not just detection.
5. **Update task list** — prioritize new tasks against existing task list. Use judgment based on familiar criteria (sprint position, blocker status, role lane priorities, deadlines-as-triage-tools).
6. **Loop back to step 1** — re-sync and check again in case new mail arrived during steps 3-5.

**Terminates when**: step 2 finds no new mail (steady state achieved). Hands off to task loop.

### Loop 2: Task Loop (sketch 4)

**Purpose**: do unblocked work; capture blockers + send memos to other agents; report when fully blocked.

**Trigger**: mail loop ends (passes control here). OR explicit task-loop entry from flywheel.

**Steps**:

0. **Sync** (canonical anchor — every loop begins with sync)
1. **Unblocked task loop**:
   - 1.1. Do task at top of task list (or task on cron)
   - 1.2. *While doing the task*: capture questions / blockers for PM attention (to per-agent attention doc) AND send memos to other agents as needed
   - 1.3. Repeat until fully blocked
2. **Report when fully blocked** — surface to PM via attention doc

**Termination logic (2-bit state machine)**:

Set two bits at loop entry: `new_mail_at_last_check = 0`, `new_tasks_at_last_check = 0`.

After one cycle:
- If either bit is non-zero → repeat cycle
- If both bits are zero → **terminate loop**

### Loop-tick decision table (sketch 5)

At each loop tick, count `(new_mail, new_tasks)` and pick action:

| new_mail | new_tasks | Action | Set bits |
|---|---|---|---|
| 0 | 0 | **end loop** | (terminate) |
| 1 | 0 | **read mail** | (1, 0) repeat |
| 1 | 1 | **read mail, then do tasks until blocked** | (1, 1) repeat |
| 0 | 1 | **do task** (PM may have added since last check) | (0, 1) repeat |

The (0, 1) row is load-bearing for PM-injected tasks — PM can drop a task into the task list while the loop is running, and the next tick picks it up without requiring new mail.

### The Flywheel (sketch 6 — composition)

The Flywheel is the orchestrator that composes the mail loop + task loop into the WORK part of the day.

**Elements** (six named sub-procedures + states):

| Name | Type | Role |
|---|---|---|
| SYNC | sub-procedure | Canonical save-to-origin anchor; bookends junctions |
| CHECK | sub-procedure | Detect state (new mail? new tasks? priorities?) → branch |
| START | sub-procedure | Day-start ritual: sync, identify ready tasks, open logs, go to WORK |
| WORK | state + sub-loop | Run mail loop + task loop flywheel + idle waits |
| IDLE | state | Wait for new mail / task / PM interrupt |
| STOP | sub-procedure | Day-end ritual: sync, close out logs, sync |

**(PROVISIONAL — awaiting PM validation)** Page 6 sub-procedure breakdown:

**CHECK sub-procedure** (from sketch 6):
1. Is new mail since last check?
2. Yes → start (the START sub-procedure)
3. Is mail || priority → ?
4. Yes → check (recursive self-call)
5. Work

**START sub-procedure** (from sketch 6):
1. Sync
2. Work on task (ready, due)
3. Check from log → where to act (it / outside / not found)
4. Start new logs
5. Go to work

**STOP sub-procedure** (from sketch 6):
0. Sync
1. Close out logs
2. Sync

The SYNC-at-both-ends-of-STOP is a deliberate brackets-the-rest pattern.

### CIO Cycle instance (sketch 7) **(PROVISIONAL — awaiting PM validation)**

The concrete daily orchestration for CIO:

```
TRIGGER: @9:00 — if loop not already running, start loop

procedure day_cycle():
    CHECK
    START
    WORK
      [idle...]
      
    loop:
        CHECK
        WORK
        IDLE      # wait for arrival or interrupt
        # back to CHECK (arrow loops)
    
    CHECK         # final check at end-of-day
    STOP

EVENT HANDLER (any time during WORK or IDLE):
  on PM_interrupt:
      1. review blockers
      2. plans
      → return to idle
```

Sequence numbering on the sketch (1→2→3→loop[4→5→6]→4→5) makes the loop structure explicit: initial entry path (CHECK→START→WORK), inner repeating body (CHECK→WORK→IDLE), final termination (CHECK→STOP).

PM-interrupt is an event handler that can fire any time during WORK or IDLE, routing to blocker-review + plans, then returning to idle.

---

## Three per-agent documents

Each cohort agent (in cycle scope) maintains three docs related to the duty cycle, separate from but coordinated with their existing session log:

### Doc 1: Daily Tracker

- **Purpose**: where the agent is in the loop + primary agenda for the day
- **Renewed daily** (fresh doc per day)
- **Not duplicative with session log** — session log is detailed turn-by-turn record; tracker is at-a-glance current state
- **Filename convention (proposed)**: `dev/YYYY/MM/DD/{role}-tracker-YYYY-MM-DD.md`

### Doc 2: Task List

- **Purpose**: the official task list of record for the agent
- **Many agents currently have ad-hoc task lists** (CIO's `cio-standing-items.md`, others' equivalents); this becomes the canonical surface
- **Persists across days** — tasks added/removed as queued + completed
- **Open question (awaiting PM ratification)**: does this REPLACE existing `dev/active/{role}-standing-items.md` files, or is it a NEW doc that the standing-items tracker feeds into? CIO recommendation: existing standing-items tracker IS the task list under new naming convention; rename for clarity rather than create a parallel doc.

### Doc 3: Items for PM Attention

- **Purpose**: items captured for PM during the day, surfaced "next time we sync"
- **This is the PM-batching surface** — the "focus batched-up questions for PM" feature PM flagged Monday afternoon (May 19) as the MVP value-add
- **Items accumulate during the day**; PM scans when bandwidth permits
- **Open question (awaiting PM ratification)**: relationship to existing per-agent escalations file (CIO's `duty-cycle-escalations-cio.md`); CIO recommendation: rename + reframe existing escalations file as the attention doc.

---

## Composition: a day in the life

```
DAY START (9:00 or analogous per role):
  ↓
START ritual:
  - sync
  - open daily tracker
  - open day's session log
  - identify ready tasks from log
  - go to WORK
  ↓
WORK (flywheel of mail loop + task loop):
  ↓
  MAIL LOOP:
    - sync
    - check mail; if none, end loop
    - read + sort + clear inbox
    - update task list
    - loop back to sync
  ↓
  TASK LOOP:
    - sync
    - do unblocked tasks
    - capture blockers to attention doc + send memos to other agents
    - check (new_mail, new_tasks) per decision table
    - end when (0, 0)
  ↓
  IDLE:
    - wait for new mail OR new task OR PM interrupt
  ↓
  (loop back to MAIL LOOP if new mail / new task)
  ↓
PM INTERRUPT (any time during WORK or IDLE):
  - review blockers
  - plans
  - return to IDLE or WORK
  ↓
STOP ritual (end of day):
  - sync
  - close out logs
  - update attention doc
  - sync
```

---

## V1-era lessons preserved (cross-references)

The methodology corpus + pattern catalog entries filed during V1 era (May 17-20) survive the redesign at the discipline layer, even though the V1 IMPLEMENTATION is retired:

| Entry | Discipline preserved |
|---|---|
| **methodology-31** (Append-Only Autonomous-Cycle Architecture) | Structural-fix-instead-of-discipline-fix; cycle branches that modify only one file have zero conflict surface. Applies to cycle-log writes in v0.2. |
| **methodology-32** (Postel for Memo Headers) | Strict-emit YAML + permissive-accept 3-tier extractor; canonical for mail loop step 3. Two refinements queued: response-requested as Tier 1 + case-insensitive YAML key matching. |
| **methodology-33** (Session-Type Determines Git-Permission Scope) | Cloud-vs-local commit-identity distinction; informs future Routines pivot. |
| **methodology-29** (Pattern Formation via Successful Imitation) | Framework; Pattern-073 reference case. Governs how v0.2 patterns will form across cohort adoption. |
| **methodology-30** (Consumer-Trace Verification) | Discipline for verifying consumer-relationship claims (LLM-touch etc.); independent of cycle architecture. |
| **PP-004 candidate** (Structural-Fix-Instead-of-Discipline-Fix) | Currently 2 instances (methodology-31 V3 architecture + kit-v2 atomic worktree); one more independent instance triggers filing. |
| **Pattern-073** (Documentation-Asserted-Behavior Drift) | Promoted Proven during V1 era; instance #14 (MANIFEST staleness) filing queued for Lead Dev. |

V1 IMPLEMENTATION retired:
- ~~V3 Phase 5 cycle (mail-detection-only observation mode)~~
- ~~Cycle-branch-per-day pattern~~ — supersedable; v0.2 may use a different branch shape
- ~~Hourly cron-without-idle-state~~ — replaced with idle-as-first-class-state per sketches
- ~~Cron-toggle-when-engaged manual discipline~~ — subsumed by the new design's start/stop ritual structure

---

## What's retired vs preserved (explicit)

### Retired (V1-era; superseded by v0.2)

- V3 Phase 5 mail-detection-only cycle implementation
- Continuous-cron-during-PM-idle pattern (replaced by mail-loop + task-loop flywheel that terminates at (0,0))
- Cycle-log-as-only-mutable-file constraint (v0.2's mail loop + task loop will need to write multiple surfaces — tracker, task list, attention doc, plus mailbox triage moves)
- `claude/cio-duty-cycle-YYYY-MM-DD` daily branch pattern (v0.2 architecture TBD)
- Kit-v2 + kit-v3 cohort-extension shape (v0.2 will need fresh adoption proposals when ratified)

### Preserved (V1-era; carries into v0.2)

- Three-loops architecture insight (mail + task + flywheel composing into a day-rhythm)
- Postel 3-tier inbound parsing (methodology-32 with 2 refinements queued)
- Append-only structural-fix discipline (methodology-31) where applicable
- Categorization enum + role-specific overlay flags (methodology-32; per-role flag adoption protocol)
- Cron-durability-empirical-finding (session-scoped; constrains v0.2's wake-mechanism design)
- methodology-29 framework for cohort pattern formation
- Pattern-073 (Proven; promoted during V1 era)

---

## Open design questions (collected; awaiting PM input)

1. **Page 6 + 7 interpretation** — my second-pass interpretation marked PROVISIONAL above; PM check-in needed
2. **Idle detection mechanism** — manual toggle vs automatic (sketches show manual; aspiration is automatic)
3. **Three-doc filename conventions** — proposed values above; PM ratification welcome
4. **Task list = standing-items tracker?** — CIO recommendation to reframe existing rather than create parallel
5. **Attention doc = escalations file?** — CIO recommendation to reframe existing rather than create parallel
6. **Wake-mechanism under session-bound cron** — manual relaunch at session-start vs session-start-hook-triggered (per HOST's empirical finding + my durability ack memo May 21)
7. **Branch-and-worktree shape** — v0.2 likely uses different shape than V1's daily cycle branches; TBD
8. **Cohort rollout sequencing** — once v0.2 ratified, what's the rollout order? CIO recommendation: re-propose to HOST + Docs (already adopted V1) first since they have the muscle memory; then PA + Exec; defer Lead Dev + Architect until cadence pattern for focus-intensive roles designed
9. **PM-attention-doc as the MVP value-add** — formalize this in design: the attention doc IS the PM-batching surface, which IS the post-MVP enhancement PM identified Monday May 19

---

## What this design IS

- Synthesis of PM sketches (1-7) + image-by-image walkthrough notes + CIO second-pass interpretation
- Unified canonical document for the new duty cycle design
- Preserves V1-era lessons at the discipline layer while retiring the V1 implementation
- Captures Ted/Englishia north-star prose as canonical intent
- Explicit retirement vs preservation table
- Open questions surfaced for PM check-in

## What this design is NOT

- Not yet a fully-PM-ratified design (page 6 + 7 interpretations are CIO second-pass; await validation)
- Not an implementation plan (that comes after ratification)
- Not a cohort-rollout proposal (that comes after v0.x reaches some stable point)
- Not a replacement for the cohort-discipline norms the cycle composes on top of (mailbox protocol, per-memo commit-push, role-essential-briefings, etc. — all survive)

---

## Cross-references

- v0.1 design doc (predecessor): `docs/operations/duty-cycle design/duty-cycle-design-v0.1.md`
- Sketches: `docs/operations/duty-cycle design/sketches/` (7 PNG pages)
- CIO V1 retirement memo (May 21): `mailboxes/cio/sent/memo-cio-to-host-docs-exec-cc-cohort-v1-duty-cycle-retirement-due-to-design-pivot-2026-05-21.md`
- CIO V3 redesign memo (May 17): `mailboxes/cio/sent/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-phase-5-v3-redesign-plus-hook-race-finding-2026-05-17.md`
- methodology-31 / 32 / 33: `docs/internal/development/methodology-core/`
- HOST cron-durability empirical-confirmation (May 20): `mailboxes/cio/read/memo-host-to-cio-lead-cc-ceo-docs-cron-durability-empirically-confirmed-session-only-2026-05-20.md`
- PM-Ted-Nadeau Englishia conversation transcript (May 20): shared in conversation; north-star paragraph extracted above

---

*v0.2 filed 2026-05-23 ~09:30 PT by CIO Vehicle 2. Provisional sections marked **(PROVISIONAL — awaiting PM validation)** — your check-in confirms or corrects those before they harden into v0.3.*
