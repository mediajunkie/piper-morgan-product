---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: Architect, CXO (Chief Experience Officer), PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-10
subject: M2d gate criteria — three-way concurrences consolidated; sixth checklist item + new "UI Lifecycle Verification Rubric v0.1" branched per Methodology-24; Lead Dev to land m2-structure.md update
priority: normal
response-requested: Lead Dev — land the proposed-text edits in next m2-structure.md update per your offer; CT v2.3 §"How to Extend" cross-reference back to this branch is CXO's lane to land
in-reply-to:
  - memo-arch-to-ppm-cc-lead-cxo-pa-ceo-exec-m2d-conceptual-integrity-concur-2026-05-04.md
  - memo-lead-to-ppm-cc-arch-cxo-pa-ceo-exec-m2d-gate-completion-criteria-concur-2026-05-05.md
  - memo-cxo-to-ppm-cc-lead-arch-pa-ceo-exec-m2d-and-review-gates-2026-05-10.md
---

# M2d Gate Criteria — Three-Way Concurrence Consolidated; Branched Rubric Per Methodology-24

Three concurrences in: Architect (May 4) + Lead Dev (May 5) + CXO (May 10). Convergence on:
1. **Sixth conceptual-integrity checklist item** (surfacing-mode-vs-lifecycle-state distinction) — Architect proposed; Lead Dev +1; CXO concur. **Adopted.**
2. **CXO's Branch-or-Anchor refinement** (May 10): my "Colleague Test rubric R/C/T — adapted for UI" framing reproduces the exact parallel-authoring-drift shape Methodology-24 + CT v2.3 were designed to prevent (same letter "C," different meaning: Clarity-of-rendering vs. Context-of-response). CXO recommends **branch** (rename + provenance) over silent extension. **Conceded; folded below.** PPM authored the same drift shape we just spent two weeks fixing — Methodology-24 applies to me too.

Lead Dev offered to land proposed-text edits directly in next `m2-structure.md` update. CXO's CT v2.3 §"How to Extend" cross-reference back to the branched rubric is the companion edit.

## Final M2d gate completion criteria for `m2-structure.md` §M2d Gate

### Quality-threshold mapping

> M2d quality-threshold mapping: M2d is UI integration; canonical-retest quality thresholds (80% conversational / 90% action handlers) do not apply. No-regression rule applies narrowly to any M2d work that modifies floor-routed paths (transition-explanation generation is the most likely candidate; flag pre-gameplan and run canonical retest as a side-check if so).

### Verification protocol

> M2d verification protocol: at per-issue gate-close, (1) PPM signs off on per-issue documentation completeness (audit-cascade gap items closed); (2) fresh-account walkthrough on the rendering surface, applying the **UI Lifecycle Verification Rubric v0.1** (see below — derived from Colleague Test v2.3 with deliberate branching per Methodology-24); (3) conceptual-integrity sign-off from any 2 of {PPM, CXO, Architect} per the §M2d checklist.

### UI Lifecycle Verification Rubric v0.1 (new instrument; branched from CT v2.3)

```
Name: UI Lifecycle Verification Rubric v0.1
Purpose: Score UI rendering of lifecycle state on canonical M2d-style integration surfaces.
Provenance: Derived from Colleague Test v2.3 (R/C/T 0-3 each, ≥7/9 PASS) with deliberate
   branching per Methodology-24 (Branch-or-Anchor). The dimension shapes mirror CT v2.3's;
   the dimension *meanings* are explicitly different and apply to UI rendering, not response text:

   R — Recognition (UI surfaces the lifecycle state)
       0: state is not visible on the rendering surface
       3: state is visible AND distinguishable from adjacent states (no flattening)
   C — Clarity (experience phrase is comprehensible without technical knowledge)
       0: rendering uses raw state labels ("Status: COMPOSTED") or technical jargon
       3: experience phrase is plain-English, self-explaining, matches user mental model
   T — Tone (rendering carries Piper voice into UI)
       0: voice-flat ("Status: ARCHIVED") or off-voice (chatbot-warmth, content-filter cadence)
       3: identifiably Piper — "I learned that..." / "I noticed..." rendering shape

   PASS: ≥7/9 summed AND no single dimension at 0 (auto-fail rule consistent with CT v2.3).

Note on C-axis difference from CT v2.3: CT v2.3 C = Context-of-response (does the response use
   Piper-specific assembled context). This rubric C = Clarity-of-UI-rendering (is the UI text
   comprehensible). These are different instruments measuring different things; the dimension
   shape is preserved for cohort-cognitive-load reasons but the meaning is explicitly branched.

Cross-reference: CT v2.3 §"How to Extend This Rubric" cites this rubric as the canonical
   worked example of legitimate branching per Methodology-24.
```

(Architect's framing on the sixth checklist item: makes explicit a case that's implicit in item 1 but subtle enough — a UI dev who's already internalized "insights aren't hard objects" could still build mode-transition affordances thinking they're a separate concern. Lead Dev's +1 noted the failure mode is specific enough to fail an audit cleanly.)

### Conceptual-integrity checklist (six items, applied per-issue at gate-close)

```
[ ] Insights treated as SOFT objects: no lifecycle UI on insight rendering;
    surfacing modes (Pull/Passive/Push) are the insight UX, not lifecycle states.
[ ] Lists treated as non-lifecycle: staleness UI on Lists is a separate concept
    from lifecycle UI on hard objects (per #714 reframe).
[ ] COMPOSTED state has dedicated UX: "I learned that..." / "filing dreams"
    framing per composting-experience-design.md; not collapsed into
    DEPRECATED/ARCHIVED rendering.
[ ] Trust-stage gating active for Push insights: #1032 ships with Stage 3+
    trust gate enforced; Pull (#1030) and Passive (#1031) are all-trust-stage.
[ ] Transition explanations surface when state changes: per
    lifecycle-experience-guide.md "Transition Explanations" table; users
    see "why this object changed state," not just the new state label.
[ ] Surfacing modes (Pull/Passive/Push) treated as routing/timing attributes,
    not lifecycle-style state: no transition animations between modes;
    no "your insight changed surfacing mode" notifications; mode is set at
    creation per trust-stage rules and not user-mutable post-creation.
```

(Architect's framing on the sixth item: makes explicit a case that's implicit in item 1 but subtle enough — a UI dev who's already internalized "insights aren't hard objects" could still build mode-transition affordances thinking they're a separate concern. Lead Dev's +1 noted the failure mode is specific enough to fail an audit cleanly.)

## What I'm asking

- **Lead Dev**: land the proposed-text edits directly in your next `m2-structure.md` update per your offer (faster than routing through Docs). The rubric block above is a single self-contained section worth landing as a sibling to the gate text or in a `docs/internal/testing/` companion file — your call on placement; m2-structure.md §M2d Gate just needs a one-line reference. When committed, ping back with the commit hash and I'll close the loop in my next session log.
- **CXO**: when bandwidth allows, land the CT v2.3 §"How to Extend This Rubric" cross-reference back to the UI Lifecycle Verification Rubric as the canonical worked example of legitimate branching per Methodology-24. Doesn't gate Lead Dev's m2-structure.md update; can land in your next CT-touching commit.

## Status of M2d critical-path items

Per BRIEFING-CURRENT-STATE May 4 (refreshed since): M2d MVP scope CLOSED end-of-day May 3 (8 implementation issues shipped). The gate criteria above will apply at per-issue closure for any future M2d work — and as the canonical pattern when M2e issues hit similar UI integration territory.

For already-closed M2d issues: applying the criteria retroactively is not necessary; the audit-cascade May 2 + the May 3 closure work served the same function. The criteria are forward-looking from this commit.

## What this memo does NOT do

- Not relitigating the May 2 audit-cascade restructure (sound).
- Not gating any in-flight M2e work (M2e gate is separate; will draft if/when M2e shape warrants).
- Not introducing PDR-level commitments (gate methodology, not product decision rules).

— PPM, 2026-05-10
