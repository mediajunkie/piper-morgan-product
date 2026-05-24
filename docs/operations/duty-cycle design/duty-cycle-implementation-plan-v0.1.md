# Duty Cycle Implementation Plan — v0.1

**Status**: Draft v0.1 — stepwise implementation plan derived from v0.5 design (DESIGN SOLID 2026-05-24)
**Author**: CIO (Vehicle 2)
**Design reference**: `docs/operations/duty-cycle design/duty-cycle-design-v0.5.md`
**Scope**: pilot on CIO first; learn operationally; then re-extend to cohort

---

## Strategy: pilot-then-cohort

V1 era taught us: extending to cohort before the pilot has settled creates rework when the design shifts. v0.5 design is solid but operational details (filename conventions, IDLE-launch detection, START step 2, SessionStart hook extension) will surface friction we can't fully predict.

Plan structure: **CIO pilot first; document learnings; cohort re-adopt with v0.6 design + implementation-validated kit**.

### Sequencing

```
Phase A: CIO pilot setup       (~half-day; this week)
Phase B: CIO pilot operation   (3-5 days observation)
Phase C: Document learnings     (~half-day; produces v0.6 design + implementation kit)
Phase D: Cohort re-adoption     (HOST + Docs first; then PA + Exec; defer focus-intensive)
Phase E: Wider rollout          (per-role pacing)
```

---

## Phase A: CIO pilot setup

### A1. Reframe existing surfaces (no new doc creation, per formalizing-not-proliferating principle)

- **Task list**: `dev/active/cio-standing-items.md` stays at current filename; add header note clarifying its task-list role under the new design
- **Attention doc**: `dev/active/duty-cycle-escalations-cio.md` stays at current filename; add header note clarifying its PM-attention-doc role under the new design
- **Daily tracker**: this IS a new doc (the third per-agent doc PM proposed). Location: `dev/YYYY/MM/DD/cio-tracker-YYYY-MM-DD.md`. Renewed daily. Distinct from session log (which captures detailed turn-by-turn record).

Estimated: ~30 min (header notes + first tracker instance).

### A2. Document the canonical procedures

Build small procedure docs under `docs/operations/duty-cycle design/procedures/`:

- `check.md` — CHECK sub-procedure (5 steps; day-part dispatcher)
- `start.md` — START sub-procedure (5 steps; day-open ritual)
- `work-parts.md` — WORK PARTS (3 steps; flywheel orchestration)
- `mail-loop.md` — Mail Loop (6 steps; sync → check → read → sort → update task list → loop)
- `task-loop.md` — Task Loop (3 steps; 2-bit termination)
- `stop.md` — STOP sub-procedure (3 steps; sync-bracketed close)
- `decision-table.md` — Loop-tick decision table (4 rows)
- `idle.md` — IDLE state (formal definition; PM-collaboration mode)

These are the operational manuals each role uses to run the cycle. Built from v0.5 content (no new design work).

Estimated: ~1.5 hr (writing concrete operational steps for each).

### A3. Wake mechanism — manual session-open as primary

For CIO pilot, the **primary wake path is manual session-open**:

- PM opens Claude Code → session starts → CIO's first message in session is to run CHECK
- Mechanism: explicit text in CLAUDE.md / role briefing instructing CIO to run CHECK at session-open
- No new code; documentation discipline only

**Optional**: SessionStart hook extension to auto-fire CHECK. Defer to Phase C+ if manual proves friction-y.

**Optional**: 4am cron wake. Defer until manual flow is operating; cron is bonus, not requirement.

Estimated: ~15 min (CLAUDE.md / CIO briefing edit).

### A4. First-day pilot run

- Open new session tomorrow morning (2026-05-25)
- Run CHECK → START (open daily tracker; close previous log if needed; new session log; go to WORK)
- Run WORK PARTS (sync → if-new-mail → flywheel: mail loop + task loop → sync → end)
- Return to IDLE
- PM engages during IDLE as opportunities permit
- Repeat CHECK → WORK → IDLE through the day
- Eventually CHECK detects >11pm AND PM not actively talking → STOP

**Calibration items to watch on first run**:
- 15-min silence threshold for IDLE-engaged → IDLE-passive (too eager? too patient?)
- START step 2 ("work in branch") — actually a thing, or no-op?
- Three-doc layout — does the daily tracker add value vs duplicate session log?
- Task list / attention doc — does the rename-only approach hold, or do filenames need to change for clarity?

Estimated: 1 working day of observation (2026-05-25 Mon).

---

## Phase B: CIO pilot operation (3-5 days)

After A4's first-day run:

- Observe the cycle over 3-5 days
- Capture friction points to a `dev/active/cio-duty-cycle-pilot-observations-2026-05-XX.md` running doc
- Iterate procedure docs in-place as needed
- Avoid major design changes (those go to v0.6); focus on operational refinements

**Decision gates during Phase B**:
- Day 1: does basic CHECK → START → WORK → IDLE → STOP cycle work? (architectural validation)
- Day 2-3: does the directed-work-done silence threshold feel right? (calibration)
- Day 4-5: is the daily tracker proving useful or redundant? (formalization-not-proliferation check)

If a fundamental issue surfaces (e.g., daily tracker IS redundant with session log) — surface to PM for design adjustment before Phase C.

---

## Phase C: Document learnings + v0.6 design (if needed)

After Phase B observation:

- Synthesize observations into a v0.6 design doc (if architectural updates needed) OR an operational addendum to v0.5 (if only operational refinements)
- Build the cohort-adoption kit (parameterized for any role; reflects pilot-validated operational decisions)
- Brief PM on findings + propose cohort re-adoption

Estimated: half-day after Phase B closes.

---

## Phase D: Cohort re-adoption (HOST + Docs first)

HOST + Docs already have V1-era experience (and have already retired their V1 cycles). They're the natural first re-adopters because:
- Existing muscle memory + worktree patterns
- Already adopted role-specific overlay flags (HOST: trust-property-touch, role-health-touch; Docs: briefing-touch, manifest-touch, narrative-touch) — these carry forward
- They've each surfaced V1-era refinements that informed v0.5

Sequence:
- Distribute v0.6 (or v0.5 + addendum) + cohort-adoption kit to HOST + Docs
- Per-role adoption at agent cadence
- Observe 3-5 days at the 2-role + CIO scale
- Then add PA + Exec (lower volume; benefit from CIO + HOST + Docs precedent)
- Defer Architect + Lead Dev until cadence pattern for focus-intensive roles is designed (per v0.5 deferred discussion)

---

## Phase E: Wider rollout

Per-role pacing post-Phase D. The full cohort (7 leadership + Docs + Lead Dev) would all be running cycles in the steady state — except focus-intensive roles which need different cadence design.

---

## Open implementation questions (carried from v0.5)

1. **Three-doc filename conventions** — defer to A1; cheap to retroactively rename
2. **IDLE-launch detection mechanism** — manual at first (A3); automatic-on-idle aspirational
3. **START step 2 "work in branch"** — empirical resolution in A4 / B
4. **Cohort rollout sequencing** — codified in this plan (D)
5. **SessionStart hook extension** — defer to C+; manual-first in A3

---

## Estimated total time to "design + implementation + pilot validated"

- Phase A: half-day (today or this week)
- Phase B: 3-5 calendar days observation (mostly passive; runs while CIO does normal work)
- Phase C: half-day post-Phase-B
- **Total to CIO-pilot-validated**: ~1 week wall-clock; ~1.5 days of focused work

- Phase D: 1-2 days per adopter, 3-5 days observation each → 2-4 weeks for HOST + Docs + PA + Exec rollout
- Phase E: continues as cohort + design matures

**Decision point at end of Phase B**: do CIO pilot results validate v0.5 architecturally, or do we need v0.6 design revisions before cohort rollout? Most likely outcome: v0.6 is a small operational addendum to v0.5, not a structural change.

---

## What this plan IS

- Stepwise pilot-then-cohort path from v0.5 DESIGN-SOLID to cohort steady-state
- Operational specifics for CIO Phase A (the immediate work)
- Decision gates surfaced for Phase B (when to escalate vs iterate)
- Cohort sequencing rationale for Phase D

## What this plan is NOT

- Not a code-shipping plan — most of this is procedure-documentation + discipline; very little code beyond optional SessionStart hook extension
- Not a re-litigation of v0.5 design decisions (those are settled)
- Not pre-committing to v0.6 changes (those depend on Phase B observations)

---

## Cross-references

- v0.5 design (DESIGN SOLID): `docs/operations/duty-cycle design/duty-cycle-design-v0.5.md`
- v0.4 / v0.3 / v0.2 / v0.1: historical drafts (architecture content lives in v0.4 + v0.5)
- Sketches: `docs/operations/duty-cycle design/sketches/`

---

*v0.1 implementation plan filed 2026-05-24 ~12:30 PT by CIO Vehicle 2. Phase A starts whenever PM greenlights; Phase A items can fit in today's remaining bandwidth if desired.*
