# Decision Table — loop-tick action selection

**Purpose**: at each loop tick within the WORK flywheel, select the next action based on current state. The composition mechanism between Mail Loop and Task Loop.

**When this runs**: at the end of each Task Loop pass (and after a fresh Mail Loop termination), the Decision Table evaluates current state and picks the next action.

---

## The table

At each tick, count current state:

```
new_mail   = count of unread inbox items since last check
new_tasks  = count of unblocked tasks on task list (including any PM-injected since last check)
```

Then pick action per the table:

| `new_mail` | `new_tasks` | Action | Effect |
|---|---|---|---|
| 0 | 0 | **end loop** | Exit WORK PASS; return to CHECK |
| 1 | 0 | **read mail** | Re-enter Mail Loop; bits set to (1, 0) |
| 1 | 1 | **read mail, then do tasks until blocked** | Re-enter Mail Loop → Task Loop; bits set to (1, 1) |
| 0 | 1 | **do task** | Re-enter Task Loop only; bits set to (0, 1) |

---

## Why each row matters

- **(0, 0)** — steady state achieved. No mail to triage, no tasks to do. WORK pass ends; agent transitions back to CHECK (which will dispatch per day-part: continued WORK if mid-day, STOP if past-11pm-and-idle, START if new day).
- **(1, 0)** — new mail arrived (e.g., another agent CC'd CIO during the task loop). Mail Loop must re-run to triage; tasks may emerge from it.
- **(1, 1)** — mail AND existing tasks both pending. Mail first (may add to task list or change priorities), then continue task work.
- **(0, 1)** — no new mail but new tasks (PM may have injected a task into the task list during agent's work). Task Loop re-runs to pick up the new task. **Load-bearing case for PM-injected tasks**.

---

## How the bits are used

The bits aren't a separate state machine the agent maintains over time — they're just shorthand for "what changed this tick." Each evaluation is fresh:
- Count `new_mail` directly from inbox enumeration
- Count `new_tasks` directly from task list (excluding tasks that were already there at loop entry)

The bits as written in the table reflect what's set FOR THE NEXT TICK (i.e., the agent remembers "I had mail" for the next comparison). Practically, the agent re-counts each tick anyway.

---

## Cross-references

- `mail-loop.md` — what (1, X) rows execute
- `task-loop.md` — what (X, 1) rows execute
- `work-parts.md` — wrapper around the flywheel that this table orchestrates
- v0.5 design — Decision Table section
