# WORK PARTS — procedure

**Purpose**: the WORK day-part's internal structure. Wraps the Mail Loop + Task Loop flywheel with sync-bracketing + log update.

**Entered from**: CHECK (when dispatcher detects mid-day, not new-day, not past-11pm).

**Exits to**: CHECK (next tick re-evaluates day-part).

---

## Steps

1. **If idle, sync with origin/main**
   - `git fetch origin -q && git pull origin main --ff-only` (if on main; otherwise just fetch)
   - **End if 0 new messages** (no-mail shortcut — saves running the full flywheel when nothing to do)

2. **Run flywheel + update log (DUAL-SURFACE)**
   - Execute Mail Loop (per `mail-loop.md`)
   - Hand off to Task Loop (per `task-loop.md`)
   - Decision Table orchestrates further iterations (per `decision-table.md`)
   - **Log the fire on BOTH surfaces** *(skill v1.5 Step-5)*: the full per-fire entry → the **cycle log** (`dev/active/cycle-log-{role}-{date}.md`, ephemeral working state); a **one-line summary** → the **session log** (`dev/YYYY/MM/DD/...`, durable institutional-memory, what Docs reads for the omnibus). Every substantive fire writes both; trivial quiet-holds need neither. Logging only the cycle log is the displacement leak (m-41); the dual-surface rule makes it impossible-by-construction (m-36 Class-2).
   - Continue until Decision Table returns "end loop" (0, 0 state)

3. **Sync with origin/main**
   - `git fetch origin -q && git push origin main` (if there are local commits)
   - **End** (return to CHECK)

---

## Why two sync points

- **Step 1 sync**: catches anything from origin since the last WORK pass; without this, mail loop would not see other agents' recent commits
- **Step 3 sync**: pushes whatever this WORK pass produced (mailbox triage moves, log updates, task list updates, attention doc updates); without this, work stays local and invisible

The sync-bracketing pattern (sync before work, sync after work) mirrors the STOP procedure's sync-bracketed close.

---

## What the WORK pass DOES write

- Session log (turn-by-turn record of this WORK pass's activity)
- Mailbox triage moves (`mailboxes/{role}/inbox/*` → `mailboxes/{role}/read/*`) — committed to main per hook-enforced discipline
- Task list updates (`dev/active/{role}-standing-items.md` — the reframed task list per v0.5)
- Attention doc updates (`dev/active/duty-cycle-escalations-{role}.md` — the reframed attention doc per v0.5)
- Outbound memos (`mailboxes/{role}/sent/*` + recipient `inbox/*` distribution)
- Daily tracker if needed (`dev/YYYY/MM/DD/{role}-tracker-YYYY-MM-DD.md`)

## What the WORK pass does NOT do

- Day-rollover (that's START's job)
- Day-end cleanup (that's STOP's job)
- Cross-day work (each WORK pass is bounded by sync brackets)

## Cross-references

- `mail-loop.md` / `task-loop.md` / `decision-table.md` — the flywheel internals
- `check.md` — what dispatches to WORK PARTS
- `start.md` / `stop.md` — sibling day-part rituals
- v0.6 design — WORK PARTS + drain-until-IDLE semantics (Correction 3): `docs/operations/duty-cycle design/duty-cycle-design-v0.6.md`
- `cron-lifecycle.md` — cron-bind-to-IDLE + PM-presence-pause disciplines (v0.6 Corrections 1 + 2)
- v0.5 design — predecessor (preserved)
