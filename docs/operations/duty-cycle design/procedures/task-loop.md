# Task Loop — procedure

**Purpose**: do unblocked work; capture blockers + send memos to other agents; report when fully blocked. Second half of the WORK flywheel.

**Entered from**: Mail Loop (when mail loop terminates with empty inbox) — OR — explicit Task Loop re-entry per Decision Table.

**Exits to**: Decision Table evaluation (which determines whether to repeat the flywheel, stay in WORK, or terminate the WORK pass).

---

## Steps

0. **Sync** (canonical anchor — every loop begins with sync)
   - `git fetch origin -q`

1. **Unblocked task loop**
   - 1.1. Do task at top of task list (or task on cron, if any)
   - 1.2. *While doing the task*:
     - Capture questions / blockers for PM attention → write to attention doc (Doc 3)
     - Send memos to other agents as needed (per-memo commit-push norm; mailbox-on-main)
   - 1.3. Repeat until fully blocked (no more unblocked tasks)

2. **Report when fully blocked**
   - Surface state to PM via attention doc
   - Summary line: "Fully blocked at {time}; {N} items in attention doc"

---

## Termination logic (2-bit state machine)

At loop entry, set two bits:
```
new_mail_at_last_check = 0
new_tasks_at_last_check = 0
```

After one cycle through the loop:
- Re-evaluate `(new_mail, new_tasks)` state
- Hand off to Decision Table to pick next action

Decision Table determines whether Task Loop repeats, transitions back to Mail Loop, or exits the WORK pass entirely. See `decision-table.md` for the action selection.

---

## What this loop is NOT

- Not for PM-conversational work — that's handled in IDLE-engaged sub-state
- Not for autonomous risky actions — captured blockers go to PM via attention doc; agent does NOT auto-resolve blockers requiring PM input
- Not the only place memos get sent — memos are sent throughout the day as natural cohort coordination; this step explicitly includes "send memos" so the task loop doesn't artificially constrain that behavior

## Cross-references

- `mail-loop.md` — first half of the flywheel
- `decision-table.md` — loop-tick action selection
- `work-parts.md` — the WORK PARTS wrapper that contains the flywheel
- v0.5 design — Task Loop section
