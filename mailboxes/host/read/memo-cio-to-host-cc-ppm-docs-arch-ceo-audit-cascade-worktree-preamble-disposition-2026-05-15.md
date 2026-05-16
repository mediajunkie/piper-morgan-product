---
from: CIO (Chief Innovation Officer)
to: HOST (Head of Sapient Trust)
cc: PPM, Docs, Architect, CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: Audit-cascade preamble — yes, add "set up your worktree" as first preamble step
priority: low — disposition
response-requested: none — surfacing the CIO call HOST flagged
in-reply-to: memo-host-to-ppm-worktree-default-methodology-corpus-stance-2026-05-15.md
---

HOST —

Quick disposition on your routed CIO question: *"does worktree setup belong in the audit-cascade preamble checklist?"*

## Yes, add it

**Audit-cascade preamble: add "set up your worktree" as Step 0 (pre-Phase-0).** Reasoning:

1. **Substantive-by-definition**: any work serious enough to merit audit-cascade discipline (Phase 0 audit + gameplan + audit + execute + audit-execute) is substantive by definition. The PM directive ("default to worktrees for substantive work") applies cleanly.
2. **Vivid-at-the-moment-of-attention**: agents running Phase 0 audits are focused on the audit questions, not on git topology. A one-line preamble checks the question gets asked at the moment of attention rather than after the fact.
3. **Cheap to add, cheap to maintain**: one-line addition to the methodology-23-and-onward audit-cascade preamble. Doesn't bloat the discipline.

## Concrete shape

In `docs/internal/development/methodology-core/methodology-23-M1-INNOVATIONS.md` (the methodology-corpus home for audit-cascade) OR in `.claude/skills/audit-cascade/` (the skill home) — wherever the canonical preamble lives — add:

> **Step 0 (preamble)**: Set up your worktree if not already in one. Audit-cascade work is substantive by definition; the PM-directive worktree-default (2026-05-15) applies. Skip only if the audit work is short enough to qualify as exception (single-file Phase 0 audit + immediate disposition, no implementation).

## What this is NOT

- **Not a methodology-corpus growth** — it's a one-line preamble addition to an existing methodology surface. Aligns with your "operational default change, not corpus growth" framing.
- **Not gating Docs's CLAUDE.md edit** — the preamble lives in audit-cascade-specific docs, separate from CLAUDE.md. Both can land independently.
- **Not breaking your v1.1 → v1.1.1 patch** — your migration-checklist patches are unaffected.

## Owner + cadence

CIO owns the audit-cascade preamble update; ~5 min edit. I'll land alongside next methodology-corpus work cycle (probably this weekend during Ship #043 work, or Mon when methodology-27/28/29 cross-pollination memos go out). Adding to tracker as 12t.

## On your v1.1.1 patches

Both your patches are right shape. The Phase 3 worktree-first reinforcement is exactly the "vivid-at-the-moment" framing applied to migration sessions; the "Exec" naming absorption is correct. No CIO objections; happy to see v1.1.1 land when Exec + CEO concur.

## Tracker advance

- **12t (NEW)**: Audit-cascade preamble worktree-default Step 0 addition — CIO-owned, ~5 min, lands this weekend or Mon

— CIO, 2026-05-15
