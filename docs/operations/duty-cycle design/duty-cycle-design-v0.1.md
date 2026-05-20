# Duty Cycle Design — v0.1

**Status**: Draft v0.1 capturing PM sketches + walkthrough notes 2026-05-20 ~13:15 PT
**Author**: CIO (Vehicle 2), capturing PM design conversation
**Sketches**: `docs/operations/duty-cycle design/sketches/` (7 PNG pages)
**Pending**: PM walkthrough of sketches 6 (Flywheel + Day-parts) and 7 (CIO Cycle) still to come; sections marked **(pending PM)** flag what's incomplete here.

---

## Scope

**When chat is active (local terminal)** — the duty cycle runs *inside* a live Claude Code session in a local terminal (like this CIO session). It does **not** launch entirely fresh sessions; that's a future-state aspiration. For now, the design scope is bounded to:

- Local-terminal chat sessions that are already alive
- Agent-driven loop start/stop (manual at first; ideally automatic on idle detection)
- Cohort agents who run their own per-role cycles in their own local sessions

Out of scope for v0.1:
- Cloud/Routines-based autonomous sessions (V2-future path)
- Email-/SMTP-/agentmail-style delivery queuing (V2+ infrastructure)
- Cross-session task durability beyond the per-session cron + per-day docs

## The three loops

The duty cycle is **two loops composed into a flywheel** plus a day-bookended orchestrator.

### Loop 1: Mail Loop

**Trigger**: agent is idle (chat session alive but PM not actively engaged). Started manually for now (agent launches loop when PM takes a break, cancels when PM interrupts). Future: automatic idle-detection.

**Steps**:

1. **Sync** — fetch + reconcile with `origin/main`. Optional in v0.1: sweep other agents' branches in case they sent mail without syncing (e.g., a memo committed to a feature branch that hasn't been folded). This compensates for agents who didn't follow per-memo commit-push norm strictly.
2. **Check mail** — enumerate inbox files on origin/main (and the swept branches if step 1 included sweep). If no new mail since last check, **end loop**.
3. **Read mail** — Postel 3-tier extract from/subject/to/cc/response-requested per methodology-32.
4. **Sort + clear inbox** (step 3.5: clear inbox) — classify each new memo into:
   - Tasks (unblocked vs need-input)
   - Informational (acknowledge + move to read/)
   - Cohort-visible info (cc copies)
   Move processed memos to `read/` as part of this step. This is what makes the loop a TRIAGE loop, not just a detection loop.
5. **Update task list** — prioritize new tasks against existing task list. Use judgment based on familiar criteria (sprint position, blocker status, role lane priorities, deadlines as triage tools).
6. **Loop back to step 1** — re-sync and check again in case new mail arrived during steps 3-5.

**Loop terminates when**: step 2 finds no new mail (steady state achieved).

**Critical shift from current V3 Phase 5**: today's V3 cycle is observation-only (read-and-log; doesn't triage or update task list). Mail loop v0.1 design is **action-taking** — it triages and updates state. This is a Phase 6-ish move with structural-fix safeguards needed.

### Loop 2: Task Loop

**Trigger**: mail loop ends (passes control here). Or: explicit task-loop entry from the flywheel.

**Steps**:

0. **Sync** (canonical anchor — every loop begins with sync).
1. **Unblocked task loop**:
   1. Do task at top of task list (or task on cron).
   2. **While doing the task**: capture questions / blockers for PM attention (to the per-agent attention doc) + **send memos to other agents** as needed.
   3. Repeat until fully blocked.
2. **Report when fully blocked** — surface to PM via the attention doc.

**How does the task loop know when to end?**

- Set two bits at loop entry: `new_mail_at_last_check = 0`, `new_tasks_at_last_check = 0`.
- After one cycle through, check state.
- If either bit is non-zero → repeat the cycle.
- If both bits are zero → **terminate loop**.

### Loop-tick decision table (page 5 of sketches)

At each loop tick, count `(new_mail, new_tasks)` and pick action:

| new_mail | new_tasks | action | set bits |
|---|---|---|---|
| 0 | 0 | **end loop** | (terminate) |
| 1 | 0 | **read mail** | (1, 0) repeat |
| 1 | 1 | **read mail, then do tasks until blocked** | (1, 1) repeat |
| 0 | 1 | **do task** (xian may have added a task since last check) | (0, 1) repeat |

The (0, 1) row is the load-bearing case for PM-injected tasks — PM can drop a new task into the task list while the loop is running, and the next tick picks it up without requiring new mail to arrive.

### The Flywheel (Loop 3, orchestrator) **(pending PM walkthrough on page 6)**

From the page 6 sketch (initial read; PM walkthrough TBD): three day-parts compose the day-shape:

1. **START** — sync, identify ready tasks, check from log, open new logs, go to WORK
2. **WORK** — the mail loop + task loop flywheel (the two loops above, composing)
3. **STOP** — sync, close out logs, sync

**Pending PM clarification**: how START transitions into WORK (cron-triggered? manual?), what STOP includes beyond logs (e.g., does it include explicit cycle branch squash-fold?), and where the IDLE state sits between WORK cycles.

### The CIO-Cycle instance **(pending PM walkthrough on page 7)**

From the page 7 sketch (initial read): scheduled at 9:00 (or analogous time), if loop not already running, start loop. Then runs CHECK → START → WORK → IDLE → CHECK → WORK → ... → STOP through the day. PM interrupt pathway routes to "review blockers / plans" then returns to idle.

This is the per-role concrete instance of the abstract Flywheel. **Pending PM clarification**: per-role timing variation (e.g., HOST and Docs differ from CIO), interrupt-recovery semantics, and end-of-day handoff to the next day's START.

## The three per-agent documents

Per PM: each cohort agent (in V1 cycle scope) has **three docs** related to the duty cycle, separate from but coordinated with the existing per-session log:

### Doc 1: Daily Tracker

- Purpose: where the agent is in the loop + primary agenda for the day
- **Renewed daily** (fresh doc per day)
- **Not duplicative with the session log** — session log is detailed turn-by-turn record; tracker is at-a-glance current state

Open question: filename convention, location (likely `dev/YYYY/MM/DD/{role}-tracker-YYYY-MM-DD.md`), and what fields it contains (current loop position? today's agenda items? blocked items?).

### Doc 2: Task List

- Purpose: the **official task list of record** for the agent
- Many agents currently have ad hoc task lists (standing items trackers, notes in session logs, etc.); this becomes the canonical surface
- Persists across days; tasks added/removed as they're queued + completed

Open question: how this relates to existing `dev/active/{role}-standing-items.md` files (which already serve this purpose for some roles, including CIO). Whether the standing-items tracker becomes the task list, or whether the task list is a new doc that the standing-items tracker feeds.

### Doc 3: Items for PM Attention

- Purpose: items captured for PM during the day, surfaced "next time we sync"
- This is the **PM-batching surface** — the "focus batched-up questions for PM" feature PM flagged Monday afternoon as the MVP framing
- Items accumulate during the day; PM scans when bandwidth permits

Open question: filename convention, retention policy (clear after PM sync? persist as audit trail?), relationship to the existing per-agent escalations file (which is the structurally similar surface that already exists).

## Composition of loops within the day

Putting it all together:

```
DAY START (9:00 or analogous):
  ↓
START ritual:
  - sync
  - open daily tracker
  - open day's session log
  - identify ready tasks
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
    - do tasks; capture blockers + send memos
    - check (new_mail, new_tasks) per decision table
    - end when (0, 0)
  ↓
  IDLE
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
  - update items-for-PM-attention doc
  - sync
```

## Mapping to current infrastructure

What's already filed (and how it maps):

| Sketch element | Current state |
|---|---|
| Mail loop step 1 (sync) | V3 cycle's `git fetch origin -q` |
| Mail loop step 2 (check mail) | V3 cycle's `git ls-tree origin/main mailboxes/{role}/inbox/` |
| Mail loop step 3 (read mail) | V3 cycle's Postel 3-tier extract (methodology-32) |
| Mail loop step 3.5 (clear inbox / sort) | **NOT YET BUILT** — V3 is observation-only |
| Mail loop step 4 (update task list) | **NOT YET BUILT** — task list doesn't formally exist |
| Mail loop step 5 (loop back) | **NOT YET BUILT** — V3 fires once per cron tick, doesn't self-loop |
| Task loop | **NOT YET BUILT** entirely |
| Decision table | **NOT YET BUILT** entirely |
| Daily tracker | **NOT YET BUILT** — per-day; session log is per-day but not at-a-glance |
| Task list | Partially — CIO's `cio-standing-items.md` is closest analog; not all roles have one |
| Items for PM Attention | Partially — CIO's escalations file is closest analog; not all roles have one |
| START / WORK / STOP day-parts | **NOT YET BUILT** as formal structure; session start/sign-off are loose analogs |
| PM interrupt pathway | Implicit — PM messages route to conversational follow-up |

Existing methodology that survives the redesign:

- **methodology-31 (Append-Only Autonomous-Cycle Architecture)** — applies to cycle-branch hygiene; relevant for cycle-log writes within mail loop, less relevant once mail loop becomes action-taking
- **methodology-32 (Postel for Memo Headers)** — still the canonical inbound-parsing discipline
- **methodology-33 (Session-Type Determines Git-Permission Scope)** — still relevant for cloud-session future
- **methodology-29 (Pattern Formation via Successful Imitation)** — the framework for cohort-wide adoption

What needs new methodology / pattern entries:

- **Task list / Daily tracker / Attention doc** — three-doc-per-agent pattern (methodology-corpus candidate when ratified)
- **Decision table loop-tick semantics** — pattern for "agent's per-tick action selection" (methodology candidate)
- **Mail-loop-then-task-loop composition** — pattern for how mail and work compose into a flywheel (methodology candidate)
- **Loop-start-on-idle** detection (operational discipline; methodology candidate)
- **Three day-parts (START / WORK / STOP)** ritual (operational discipline; methodology candidate)

## Pending PM input

Items flagged above as **(pending PM)** plus:

1. **Page 6 walkthrough** — Flywheel + Day-parts in detail
2. **Page 7 walkthrough** — CIO-Cycle instance and how cohort roles parameterize it
3. **Three-doc filename conventions and location**
4. **Relationship of task list to existing standing-items trackers**
5. **Relationship of items-for-PM-attention doc to existing escalations files**
6. **Idle-detection mechanism** — manual for now (agent toggles); automatic-detection design later
7. **Cohort-wide rollout sequencing** — does this design supersede the V3 Phase 5 cycle in flight, or compose with it?

## Cross-references

- **Sketches**: `docs/operations/duty-cycle design/sketches/` (7 PNG pages)
- **CIO Phase 5 V3 redesign memo (May 17)**: `mailboxes/cio/sent/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-phase-5-v3-redesign-plus-hook-race-finding-2026-05-17.md`
- **methodology-31 / 32 / 33** under `docs/internal/development/methodology-core/`
- **Phase 6+ pre-design sketch (May 18)**: `dev/active/cio-v1-phase-6-plus-pre-design-sketch-2026-05-18.md` (this design supersedes the Option B sidecar lean if PM ratifies)
- **Kit v2 (cohort-extension setup doc)**: `dev/active/cio-v1-cohort-extension-kit-v2-2026-05-18.md` (will need v3 update reflecting new design)
- **Inbox Triage Gate proposal (May 18)**: `mailboxes/docs/inbox/memo-cio-to-docs-cc-ceo-host-session-start-inbox-triage-gate-proposal-2026-05-18.md` (the START-ritual analog)

---

*v0.1 draft filed 2026-05-20 ~13:30 PT by CIO Vehicle 2, capturing PM image-by-image walkthrough notes (sketches 1-5) + PM's three-doc-per-agent design (image 2 thought). Sketches 6 + 7 walkthrough pending PM availability post-1:30 PT call.*
