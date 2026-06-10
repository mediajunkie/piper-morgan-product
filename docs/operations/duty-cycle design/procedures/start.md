# START — procedure

> ⚠️ **Operative source of truth = the `duty-cycle-tick` skill (`.claude/skills/duty-cycle-tick/SKILL.md`, v1.5+), Step 3 START branch.** This `procedures/*.md` doc is the human-readable companion; it predates the skill (v0.5-era language survives below) and must be kept in sync with it. Where they differ, **the skill wins.** *(Coherence-debt: these parallel-maintained procedure docs are a hand-maintained mirror of the skill — the exact dual-maintenance drift m-36 Class-1 / pattern-073 warn against. The mechanism-correct fix is to thin them to pointers at the skill's authoritative steps rather than re-mirroring detail. Flagged for a future coherence pass; this update mirrors the load-bearing v1.4/v1.5 changes in the meantime.)*

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

3. **Step 0 — verify the prior day STOPped, self-heal if not** *(skill v1.4; PM-ratified 2026-06-09, Comms-surfaced)*
   - Locate the previous day's session log (`dev/YYYY/MM/DD/{date}-{role}-code-opus-log.md`).
   - **Grep for the canonical close-out marker**: `grep -l "DAY-CLOSED" <prior-day session log>`. The marker is a literal **`<!-- DAY-CLOSED: {YYYY-MM-DD} -->`** line that a proper STOP emits in the sign-off section (HTML-comment → grep-able, invisible in rendered markdown).
   - **If the marker is present** → the prior day STOPped properly → no-op; proceed to Step 4.
   - **If the marker is ABSENT** → the prior day ended without a STOP (PM takeover, cron reshape, session-death, or engaged-past-the-STOP-window). **Run its missed close NOW, before today's START**: reconstruct the prior day's wrap from its cycle log + that day's commits — the **day-arc** + the **memory-eval 3-bucket** (#974) + the **sign-off checklist** (`git status` clean / `@{u}..HEAD` empty / `main..HEAD` empty) + emit the **`<!-- DAY-CLOSED: {prior-date} -->`** marker. This is *self-healing* — it catches the gap at the source rather than waiting for Docs's merge-keeper sweep the next morning (that sweep is the reactive net; this is the proactive source-catch).

4. **Start new log**
   - Create today's session log (`dev/YYYY/MM/DD/{date}-{role}-code-opus-log.md`) via the `create-session-log` skill.
   - Header per session-log-discipline (role, slug, branch identity, date, prior session reference).
   - Create today's fresh **cycle log** (`dev/active/cycle-log-{role}-{date}.md`) — the per-fire append-only working record. *(Note: the session log is the **durable** institutional-memory surface; the cycle log is **ephemeral** working state. Per skill v1.5 Step-5 DUAL-SURFACE logging, every substantive fire accretes a one-line summary to the session log in addition to the full cycle-log entry — see `work-parts.md` + m-31's session-log composition discipline. This prevents the cycle-log-displaces-session-log leak, m-41.)*

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
