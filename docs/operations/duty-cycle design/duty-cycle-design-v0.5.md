# Duty Cycle Design — v0.5

**Status**: **DESIGN SOLID** per PM milestone 2026-05-24 ~12:07 PT — all architectural decisions ratified; remaining open items are operational (defer to implementation)
**Author**: CIO (Vehicle 2)
**Predecessor**: v0.4 (filed 2026-05-24 ~10:45 PT)
**Changes from v0.4**: three architectural decisions ratified (task-list / attention-doc / no-per-day-cycle-branch); wake-mechanism finalized (manual session-open primary + 4am cron bonus); formalizing-not-proliferating principle added; status promoted to DESIGN SOLID

---

## Guiding principle (NEW in v0.5, PM-stated)

> *"We are formalizing, not fragmenting or proliferating."*
>
> — PM 2026-05-24 12:07 PT, ratifying that the task list and attention doc become reframed existing surfaces rather than parallel new docs

This is the load-bearing design principle for v0.5 onward. The duty cycle reframes + formalizes patterns the cohort has been doing ad-hoc (standing-items trackers, escalations files, per-memo commit-push, session logs). It does NOT create parallel new doc surfaces, parallel new branches, or parallel new file paths. Existing patterns get clarified roles + canonical conventions. Net surface count stays flat or shrinks; coherence increases.

---

## North-star intent (unchanged)

> *"Wake if idle, check for new incoming messages, check for new tasks. Run the do-things-that-are-not-blocked cycle until everything's blocked. Then make the list of things you need a batch update on — update the doc for my attention. Check for mail again; if there's new mail, do it again. If you have any new tasks, do it again. Only when you get back to zero mail and zero tasks, this loop is done. Go to sleep. If I interrupt them and do stuff, they'll do more stuff. But if I'm busy and working another hour later, it'll wake up. And in the meantime, another agent may have woken up, gotten the message from someone, responded to them, and they can all be talking to each other without me going, 'hey, you've got mail, go check.'"*
>
> — PM to Ted Nadeau, 2026-05-20

---

## Three architectural decisions ratified (v0.5)

### 1. Task list = reframed standing-items tracker (no new doc)

The existing per-agent `dev/active/{role}-standing-items.md` files (CIO has one; some other roles have analogs) are renamed/reframed as the official task list. No parallel new "task list" doc is created.

CIO's current `cio-standing-items.md` becomes the task list of record. Other roles either rename their analog OR adopt the convention at cycle-adoption time.

**Filename convention** (proposed; defer final decision to implementation): keep existing `dev/active/{role}-standing-items.md` OR rename to `dev/active/{role}-tasks.md`. Cheap to retroactively rename; not blocking.

### 2. Attention doc = reframed escalations file (no new doc)

The existing per-agent `dev/active/duty-cycle-escalations-{role}.md` files become the canonical attention doc — items for PM to scan during IDLE.

CIO's current `duty-cycle-escalations-cio.md` becomes the attention doc of record. Same disposition for other roles.

**Filename convention** (proposed; defer): keep existing OR rename to `dev/active/{role}-pm-attention.md`. Cheap to retroactively rename.

### 3. No per-day cycle branch

The V3-era `claude/{role}-duty-cycle-YYYY-MM-DD` daily branch pattern was an artifact of observation-only Phase 5 + the append-only structural-fix discipline (methodology-31). Under v0.5, the cycle is action-taking on multiple surfaces (mailbox triage, log updates, task list updates, attention doc updates), so the append-only invariant doesn't apply.

**The cycle runs in the agent's current session/branch**:
- Mailbox writes still go on main per the existing mailbox-on-main discipline (CLAUDE.md hook-enforced)
- Other writes (logs, tracker, task list, attention doc) go wherever the agent is currently working — main for short ops, claude/* worktree branch for substantive sessions per existing worktree-default discipline

No new branch shape needed. The existing branch + worktree discipline carries forward.

---

## Wake mechanism — finalized (v0.5)

**Primary**: manual session-open (canonical path). PM opens Claude Code → fresh session starts → SessionStart hook (or first user interaction) triggers CHECK → CHECK dispatches per day-part → typically START on a new-day morning.

**Bonus**: 4am cron wake (`@4:00am — if loop not already running, start loop`). Best-effort for the case where previous session persisted overnight (Claude Code stayed open + machine stayed alive). Cron fires CHECK directly. The idempotent restart guard ("if loop not already running") is defensive insurance.

The cron is an **optimization, not a requirement**. The design is robust to overnight cron failure — agent still starts the day correctly via manual session-open at PM's normal start time.

**SessionStart hook extension** (implementation item): today the hook surfaces unread mail + log continuity + briefing freshness. To bootstrap the cycle, extend the hook to also fire CHECK (or queue a CHECK as the first cron tick) at session-open.

---

## The architecture (unchanged from v0.4)

All page-6 + page-7 RATIFIED content from v0.4 carries forward unchanged. The architecture:

- Day-parts: START → WORK → STOP
- CHECK as day-part dispatcher (5 steps; conditional on PM-engagement for STOP)
- START as day-open ritual (5 steps; previous-log-close + new-log-open)
- WORK PARTS as 3-step pass (no-mail shortcut OR run flywheel + log update; sync; end)
- STOP as day-close ritual (3 steps; sync-bracketed close)
- IDLE as PM-collaboration-available state (PM may engage; agent returns to IDLE-passive after silence threshold)
- The flywheel inside WORK: Mail Loop + Task Loop composing with decision-table loop-tick semantics
- PM-interrupt: PM activities during IDLE (review blockers, interact, plan)
- Three per-agent docs: tracker (new daily) + task list (reframed standing-items) + attention (reframed escalations)

See v0.4 for full content. v0.5 changes only the three architectural decisions above + wake mechanism finalization + guiding principle.

---

## Open items (remaining post-DESIGN-SOLID)

All are **operational** (defer to implementation), not architectural:

1. **Three-doc filename conventions** — finalize at first-adopter implementation; cheap to retroactively rename
2. **IDLE-launch detection mechanism** — manual at first; automatic-on-idle aspirational
3. **START step 2 "work in branch"** — try without; if gap shows operationally, address then
4. **Cohort rollout sequencing** — comes WITH the implementation plan, next artifact

---

## Status milestone

PM milestone 2026-05-24 ~12:07 PT: **"design solid"** achieved. All architectural decisions ratified. Operational specifications + cohort rollout deferred to implementation plan (separate forthcoming artifact: `duty-cycle-implementation-plan-v0.1.md`).

---

## Cross-references

- v0.4 (predecessor; full architecture content): `docs/operations/duty-cycle design/duty-cycle-design-v0.4.md`
- v0.3 / v0.2 / v0.1: historical drafts
- Sketches: `docs/operations/duty-cycle design/sketches/` (7 PNG pages)
- Implementation plan: forthcoming `docs/operations/duty-cycle design/duty-cycle-implementation-plan-v0.1.md`

---

*v0.5 filed 2026-05-24 ~12:15 PT by CIO Vehicle 2. **DESIGN SOLID** per PM milestone. Implementation plan next.*
