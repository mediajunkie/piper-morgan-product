# Canonical Cron-Prompt Template — v0.7

**Purpose**: the normalized middle-weight cron prompt every adopting agent registers. Replaces the per-agent improvisation that produced the cron-script spectrum (Lead ~6 lines too terse for new adopters; CIO/Docs ~40 lines heavier than needed once fluent). This is the cohort-canonical version.

**Filed**: 2026-05-28 by CIO (cycle-design lane) per PM-eager distribution directive (PA relay ~8:15 AM PDT).

**v0.7 context**: incorporates worktree-as-cycle-default (PM-ratified "do not register on main") + Rule-2 Model-A + v0.6.1 0th-step + v0.6.2 mail-check-at-interruption + v0.6.3 advance-low-priority.

---

## How to use

1. Copy the template below.
2. Replace `{ROLE}` / `{role}` with your role (e.g., `CIO` / `cio`).
3. Replace `{WORKTREE_PATH}` with your cycle worktree path (per the v0.7 worktree-cycle mechanism Lead Dev + Architect are landing — DO NOT register on shared main).
4. Fill the STATE block with today's artifact paths.
5. Pick a cron offset minute not already taken (current slate below).
6. Register via CronCreate ONLY after your worktree is set up (per "do not register on main").

**Current offset slate** (avoid collisions): CXO `:02` · CIO `:07` · Docs `:17` · Lead `:27` · Exec `:32` · HOST `:37` · PA `:42` · Arch `:52`. Open: `:12`, `:22`, `:47`, `:57`. (PPM/Comms pick from open.)

---

## The template

```
DUTY CYCLE TICK ({ROLE} — v0.7 worktree-cycle)

Autonomous loop fire; no human driving this turn. Hold the discipline; be holistic-not-tactical.

WORKTREE: cd {WORKTREE_PATH} (v0.7 — cycle runs in your own worktree, NOT shared main; mailbox writes bridge to main per the workflow below)

STATE (today):
- Session log: {path}
- Tracker: {path}
- Cycle log: {path}
- Task list: dev/active/{role}-standing-items.md
- Attention doc: dev/active/duty-cycle-escalations-{role}.md

CRITICAL SEMANTICS (drain-until-IDLE): each fire = wake from IDLE → drain ALL unblocked work → return to IDLE only when nothing left. NOT one-work-unit-per-fire.

CHECK DISPATCHER:
- New day (no session log for today)? → START (5 steps; procedures/start.md)
- Past 11pm local + PM not active? → STOP (3 steps; procedures/stop.md)
- Otherwise → WORK PARTS: Mail Loop drain to inbox-zero → Task Loop drain to blocked-or-empty → re-check mail → loop until (0,0)

CRON LIFECYCLE (procedures/cron-lifecycle.md):
- Rule 1 (strict): substantive multi-step WORK (>2 min) → CronDelete first, do work, CronCreate when back to IDLE
- Rule 2 (Model A): leave cron running during PM conversation — runtime idle-only-fire suppresses; do NOT CronDelete just for PM messages
- v0.6.2: quick mail-check before substantive PM engagement
- v0.6.3: at (0,0), advance smallest-scope unblocked low-priority work before pronouncing IDLE (skip if nothing safely-advanceable-now)

WORKTREE WORKFLOW:
- Substantive cycle work commits to your worktree branch
- Merge to main at natural points (STOP, or per-task-completion)
- Mailbox writes: brief checkout-main → commit → return-to-worktree (batched; minimize main traffic)
- EXPLICIT-PATHS-ONLY on git add — never directory-level mailbox adds

PROCEDURE EACH FIRE:
1. Time check: date "+%H:%M %Z"
2. CronList (get cron-id for Rule-1 pauses)
3. CHECK dispatcher → execute
4. Append fire entry to cycle log (append-only per methodology-31)
5. Commit + push work product (explicit paths)
6. Brief status report (1-3 sentences)

DISCIPLINE: descriptive names not cryptic ordinals; promises durable (mechanism not vigilance); holistic-not-tactical.
```

---

## Design rationale (why this weight)

- **Middle-weight** (~30 lines): heavier than Lead's 6-line (which assumes fluency new adopters lack) but lighter than the original CIO/Docs ~40-line full-state prompts. Critical semantics inline; everything else by-reference to procedures.
- **Worktree-first**: per PM "do not register on main" — the WORKTREE line is first + load-bearing.
- **Explicit-paths reminder baked in**: the directory-add lapse (CIO Fire 8 today) recurred under scale; the template embeds the reminder so it's not vigilance-dependent.
- **Rule-2 Model-A baked in**: no more recreate-on-go-autonomous burden.

## Known open item before broad adoption (HOST + Exec flagged)

**Overnight-continuity / never-recreate gap**: under v0.7, STOP must address how the cycle resumes the next day. The conditional-dispatch pattern (post-STOP cron checks date → no-op or START) worked for CIO's 2 overnight crossings on main. The worktree version needs the equivalent. **This is a Lead Dev + Architect + CIO cycle-design item to resolve before broad adoption** — flagged so PA/Comms/PPM don't adopt a known-gap mechanism. Until resolved, manual-session-open START is the safe fallback.

## Cross-references

- v0.6 design + v0.7 markers: `docs/operations/duty-cycle design/duty-cycle-design-v0.6.md`
- cron-lifecycle.md (Rules 0/1/2 + sub-rules): `docs/operations/duty-cycle design/procedures/cron-lifecycle.md`
- v0.7-candidates.md #10 (worktree-as-cycle-default): `docs/operations/duty-cycle design/v0.7-candidates.md`
- Worktree-cycle mechanism (Lead Dev + Architect, in design): forthcoming

---

*Filed by CIO Vehicle 2, 2026-05-28 ~8:35 AM PDT. The canonical template the cohort waits on; pairs with the Lead Dev + Architect worktree-cycle mechanism for the complete v0.7 adoption package.*
