# Pre-Filing Slot-Availability Check

## Overview

The **Pre-Filing Slot-Availability Check** is a lightweight filing-convention discipline applied at the moment of claiming a slot in a shared catalog (pattern numbers, ADR numbers, methodology numbers, anti-pattern numbers, issue ranges, sub-epic numbers — anything sequentially numbered with cross-role authoring). The discipline is one shell command + one judgment call before filing.

The rule:

> **Before filing into slot NNN, run `ls <catalog>/<prefix>-NNN-*` (or the catalog's equivalent). If anything exists at that slot, surface as a slot conflict before filing.**

The discipline emerged operationally from the May 11, 2026 Pattern-067 slot collision (Lead Dev filed `pattern-067-issue-body-reality-mismatch.md` May 9; CIO filed `pattern-067-silent-state-mutation-shared-working-tree.md` May 11 morning under PM-directive cadence without re-pulling catalog state; Architect + Lead Dev both flagged the conflict within ~10 minutes; CIO renumber resolution executed within ~30 minutes). The cohort named the check, and Architect adopted it pre-codification when proposing Pattern-070 May 15.

## Why This Methodology

### The failure mode

Slot collisions occur when two authors, acting independently and in good faith, each claim "the next available slot" based on their session memory of the catalog state. Both authors may have correct local context; neither has authoritative catalog state at filing time. The first-filed claim is valid; the second-filed claim collides.

This is structurally a **Pattern-063 (Parallel-Authoring Drift) instance at the catalog layer**. The Branch-or-Anchor methodology (methodology-24) does not strictly apply, because neither author is *extending* an existing artifact — both are *filing new* into the same numeric slot. The discipline needed is a **slot-availability check**, not a branch-or-anchor decision.

### Why a lightweight discipline is the right shape

Heavier alternatives (slot-reservation memos, central allocation authority, locking mechanisms) introduce coordination overhead that exceeds the failure cost. The slot-collision failure mode is:

- Visible immediately at filing time (file exists with the same prefix)
- Mechanically recoverable (rename via `git mv`; ~30-minute renumber)
- Self-limiting (the catalog has many slots; collisions are rare)

A 5-second shell command before filing prevents the entire failure class without coordination overhead. The cost-benefit math favors the lightweight check.

## When to apply

### Apply this rule when

- Filing a new pattern entry into `docs/internal/architecture/current/patterns/`
- Filing a new methodology-core entry into `docs/internal/development/methodology-core/`
- Filing a new ADR into `docs/internal/architecture/current/adrs/`
- Filing into an anti-pattern index slot
- Reserving any sequentially-numbered slot in any shared catalog
- Especially: when a PM directive accelerates the filing cadence (the May 11 case)

### This rule does not apply when

- The filing is non-numeric (free-form filenames in a flat directory)
- The slot is being deliberately reused (versioned replacement, with explicit ownership and downstream coordination)
- A central catalog-management process already allocates slots (none currently exists in PM)

## The Check

### The shell command

For pattern catalog:

```bash
ls docs/internal/architecture/current/patterns/pattern-NNN-*.md
```

For methodology-core:

```bash
ls docs/internal/development/methodology-core/methodology-NNN-*.md
```

For ADRs:

```bash
ls docs/internal/architecture/current/adrs/adr-NNN-*.md
```

The check returns either (a) zero files (slot available — proceed) or (b) one or more files (slot taken — do not file).

### The judgment call

If the slot is taken, the next step depends on context:

1. **Different filing intent, slot collision**: pick the next available slot. Re-run the check. Proceed.
2. **Same filing intent, recent file by another author**: the existing file may already cover your filing; read it and decide whether to amend rather than file new.
3. **Stale file at the slot (filename present, content abandoned)**: do not silently reuse; surface to whoever owns the catalog (CIO for patterns/methodology, Architect for ADRs) for retirement before filing.

In all cases, **first-filed-wins is the default disposition** when a collision is detected post-filing. Renumber is the mechanical fix; the substantive content of both filings stands.

## Cross-references

- **Pattern-063 (Parallel-Authoring Drift)**: the parent failure mode this discipline prevents at the catalog layer
- **Methodology-24 (Branch-or-Anchor)**: the related discipline for *extending* canonical references; does not apply to *filing new* into a slot
- **Pattern-067 slot collision (May 11, 2026)**: the canonical reference instance — Lead Dev's May 9 filing + CIO's May 11 filing both claimed Pattern-067; renumber resolved as Lead Dev keeps 067 (Issue-Body Reality Mismatch), CIO cascades to 068 (Silent State Mutation) + 069 (Coarse Triggers)
- **Pattern-070 filing (May 15, 2026)**: first observed adoption-before-codification of this discipline — Architect ran the check before proposing the slot, mentioned it explicitly in the proposal memo, prior to this methodology entry landing
- **CIO standing-items tracker 12l**: the queued codification item this entry closes
- **`mailboxes/cio/sent/memo-cio-to-lead-arch-cc-ceo-exec-pa-pattern-067-slot-renumber-disposition-2026-05-11.md`**: the disposition memo that named this discipline candidate

## Notes on this entry's authority

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md`. The cohort-discipline lesson the May 11 slot collision produced (*"slot-state should be queried at filing time, not assumed from session memory, especially when a PM directive accelerates the filing cadence"*) is the operationally-useful framing this entry preserves.

The discipline is unusual in that **adoption preceded codification by 4 days** — Architect ran the check on May 15 before this entry landed today. That ordering is itself worth memorializing: when a failure mode is vivid and the discipline is mechanical, cohort adoption can run ahead of the methodology corpus. Codification still owes the corpus, even when adoption is already proceeding.

---

*Filed: 2026-05-15 by CIO. Pattern category: methodology-corpus filing convention. Authority: CIO self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Slot allocation: methodology-28 next-available; pre-filing slot-availability check applied (this entry's own discipline).*
