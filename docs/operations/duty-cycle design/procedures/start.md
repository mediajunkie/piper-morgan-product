# START — procedure

**Purpose**: day-open ritual. Previous-day cleanup + new-day open.

**Entered from**: CHECK (when dispatcher detects new day since last check).

**Exits to**: WORK (typically WORK PARTS step 1).

**Frequency**: once per calendar day, at the first CHECK tick of the day (typically at 4am wake OR at first PM-session-open of the day, whichever happens first).

---

## Steps

1. **Sync**
   - `git fetch origin -q && git pull origin main --ff-only` (if on main; otherwise just fetch + reconcile)

2. **[Working assumption: "work in branch"]**
   - PM's handwriting illegible on this step; PM's own best guess is "work in branch"
   - Provisional interpretation: ensure correct worktree branch is active for today's substantive work; create new worktree if today's work warrants per worktree-default discipline
   - **May be no-op operationally** — if Phase B observation shows no gap, this step can be removed in v0.6

3. **Check previous log**
   - Locate previous day's session log (`dev/YYYY/MM/DD-1/{role}-code-opus-log.md` or analog)
   - If log doesn't have end-of-day wrap entry, close it out now (add brief wrap noting any context for today)
   - If log was already closed, no-op

4. **Start new log**
   - Create today's session log (`dev/YYYY/MM/DD/{role}-code-opus-log.md`)
   - Header per session-log-discipline (role, slug, branch identity, date, prior session reference)
   - Create today's daily tracker (`dev/YYYY/MM/DD/{role}-tracker-YYYY-MM-DD.md`) — fresh per day; not duplicative with session log

5. **Go to WORK**
   - Hand off to WORK PARTS (per `work-parts.md`)

---

## What START is NOT

- Not task work (that's WORK PARTS)
- Not mail triage (Mail Loop inside WORK PARTS)
- Not status reporting to PM (that happens via attention doc updates throughout the day)

## Day-open ritual is housekeeping

START's job: yesterday closed, today opened, ready to WORK. Quick + ritualized. Should take < 5 minutes operationally.

## Cross-references

- `check.md` — dispatcher that triggers START
- `work-parts.md` — what START hands off to
- `stop.md` — symmetric day-close ritual
- v0.5 design — START section
