# V1 Duty Cycle — Phase 6+ Pre-Design Sketch

**Author**: CIO Vehicle 2
**Date**: 2026-05-18 ~10:10 AM PT
**Status**: Pre-design sketch — outlines the problem, candidate approaches, and CIO lean. Not a v0.5 design doc; that comes after PM ratification of an approach.
**Predecessor**: Phase 5 V3 (observation-only categorize step; mechanically validated; running today at hourly cadence)
**Audience**: PM primary; cohort visibility once a direction is picked

---

## The problem

Phase 5 V3's append-only architecture works because the cycle only ever modifies one file (the cycle log) on its own branch. No conflict surface; no race conditions; squash-folds to main cleanly.

Phase 6 changes that. The design v0.4 framing: *"Cycle updates escalations file based on categorization. Introduces main-write surface; needs careful design (branch-vs-main reconciliation)."*

The escalations file (`dev/active/duty-cycle-escalations-cio.md`) lives on main and is updated by the conversational CIO when escalations open/close. Phase 6 would have the cycle ALSO update this file, based on its categorization output. Concrete update shapes:

- Cycle detects a new `to-cio` memo with `cc-cio-with-ask` overlay → cycle adds an entry to the active-cohort-threads section
- Cycle observes a memo it had previously flagged is now moved to `cio/read/` → cycle removes/resolves the entry
- Cycle observes a state change worth recording → cycle updates the resolution column

The mechanical problem: cycle branch's view of the escalations file is whatever it inherited at branch-creation (start of day). Main's escalations file is being modified by the conversational CIO concurrently. When end-of-day fold happens, the cycle's escalations-file changes need to merge with main's escalations-file changes. That's the **branch-vs-main reconciliation** problem.

Phase 5 V3 dodged this by being observation-only — the cycle never wrote to main-shared files. Phase 6 needs an answer.

## Candidate approaches

### Option A — Cycle commits to its own branch; squash-fold reconciles at end-of-day

The cycle writes escalations file changes to the cycle branch. At end-of-day squash-fold, git's merge mechanics reconcile cycle-branch's changes with main's changes. Conflicts handled via standard merge tooling.

**Pros**: simplest extension of Phase 5 V3 mechanics; no new file paths; conversational CIO behavior unchanged.

**Cons**: when conflicts arise (cycle and conversational both modified the same lines), fold is no longer trivial. The "zero conflict surface" property of V3 doesn't hold. End-of-day fold may need manual intervention.

### Option B — Cycle writes to a "proposed" sidecar file; conversational CIO applies the proposal

The cycle writes its proposed escalations-file changes to `dev/active/duty-cycle-proposed-escalations-cio.md` (a separate path on the cycle branch). At end-of-day OR when the conversational CIO checks the proposal file, the proposed changes get reviewed and applied to the canonical escalations file on main.

**Pros**: preserves V3's observation-only property at the cycle level; cycle never writes to main-shared files. Conflict resolution happens at the conversational layer where judgment is available.

**Cons**: introduces a two-step process (cycle proposes → conversational applies); slower than direct cycle-writes; relies on conversational CIO actively reviewing the proposal file.

### Option C — Cycle writes to a "fork" file that becomes the new canonical

The cycle writes to `dev/active/duty-cycle-escalations-cio-cycle-fork.md` (a separate fork file). The fork file IS the new canonical; conversational CIO migrates to reading the fork file and stops updating the original. End-of-day fold replaces the original on main with the fork file's content.

**Pros**: cycle owns the file outright; no reconciliation needed; clean separation.

**Cons**: cohort and other agents may already be reading the original path; migration cost; introduces a path-change that breaks existing references.

### Option D — Permission elevation: cycle writes directly to main

PM grants the cycle's commit identity main-push permission; cycle commits to main directly without branch isolation.

**Pros**: mechanically simplest; no reconciliation; no fold step.

**Cons**: breaks the safety property that Phase 5 V3 cycle is constrained to one append-only branch. Hook race conditions return (rebase-onto-main + MANIFEST regen). Pattern-073 family at the autonomous-cycle layer becomes a real risk again. Probably wrong.

## CIO lean

**Option B (sidecar proposal pattern).**

The rationale: V3's observation-only invariant is the load-bearing safety property that lets the cycle run without supervision. Phase 5 → Phase 6 doesn't have to break that invariant; we can preserve "cycle is structurally observation-only" by routing mutations through a conversational-layer applier.

The cycle's job in Phase 6 then becomes: produce a proposed escalations-file-update artifact based on categorization output. The conversational CIO's job is: review the proposed update at session-start (or via the Inbox Triage Gate from this morning's proposal — the gate naturally extends to "review your cycle's proposed updates") and apply approved changes to the canonical escalations file.

This composes with the Inbox Triage Gate. The gate already requires inbox triage at session-start; adding "review your duty-cycle proposed updates" to the gate is a one-line CLAUDE.md amendment.

It also composes with methodology-31 (Append-Only Autonomous-Cycle Architecture). The cycle remains structurally append-only; the file-paths it writes to are different (now includes the proposed-update sidecar), but the property that "cycle branch never modifies files that main is also modifying" holds.

## What Phase 6 design v0.1 would specify (if Option B is ratified)

Once PM ratifies an approach, a v0.5 duty-cycle design doc would specify:

1. **The proposed-update sidecar file format**: structured-markdown with explicit "ADD entry" / "REMOVE entry" / "MODIFY entry" sections that the conversational applier reads
2. **The cycle prompt extension** (Phase 6 prompt, building on Phase 5 V3): after categorization, when detection produces an escalation-worthy event, the cycle appends a proposed-update block to the sidecar
3. **The conversational-applier protocol**: at session-start (after Inbox Triage Gate), conversational CIO reads the sidecar, validates each proposed update, applies approved ones to the canonical escalations file, marks resolved ones in the sidecar
4. **The cleanup discipline**: applied proposals are marked but retained for one cycle of audit-trail visibility; cleaned up at end-of-day fold

## Cohort extension implications

For cohort extension (HOST cycle, Docs cycle, etc.), Option B's sidecar pattern generalizes cleanly. Each role has:
- Their own append-only cycle log (Phase 5 V3 pattern)
- Their own proposed-update sidecar (Phase 6 Option B pattern)
- Their own canonical escalations file (existing per-role pattern)
- Their own conversational applier discipline (Inbox Triage Gate extension)

The cohort-wide rollout doesn't require coordinated changes across roles; each role can adopt the pattern independently.

## Open questions for PM

1. **Approach ratification**: A / B / C / D (or a variant I haven't sketched).
2. **Timing**: Phase 6 design after Phase 5 V3 hits MVP (Wednesday or later per the cohort-extension proposal), or in parallel as a research thread?
3. **Sidecar file naming convention**: `duty-cycle-proposed-escalations-cio.md` is one option; happy to bikeshed.
4. **Audit-trail retention**: how long do applied proposals stay in the sidecar before cleanup? (One cycle / one day / until manual cleanup?)

## What this sketch IS

- Pre-design framing of the Phase 6+ problem (cycle main-write surface)
- Four candidate approaches with pros/cons
- CIO lean toward Option B (sidecar proposal pattern)
- Open-question surface for PM ratification

## What this sketch is NOT

- Not a v0.5 design doc — that comes after PM ratification
- Not committing to a specific implementation — sidecar format, applier protocol details TBD
- Not blocking — Phase 5 V3 runs in parallel; no Phase 6 implementation work has started

---

*Sketch v0.1. CIO Vehicle 2, 2026-05-18 ~10:10 AM PT. Will iterate after PM ratification of the approach.*
