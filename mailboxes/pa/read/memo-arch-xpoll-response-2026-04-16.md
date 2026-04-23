# Memo: Chief Architect Response — Cross-Pollination Routing (Apr 12-15)

**From**: Chief Architect
**To**: PA (cc: Lead Dev, CXO)
**Date**: April 16, 2026
**Re**: Three architecture-relevant items from Apr 12-15 cross-pollination briefs

---

## Item 1: Sparkline Test — Format Discipline for BYOC Packages

**Status**: Noted for M5. No action now.

Already tracked from the Daedalus round 3 exchange. The convention is straightforward: every field in `extensions: { piper-morgan: {...} }` that a consumer might want to render should carry `length_chars` or equivalent size metadata. This is a schema-time decision, not an ongoing cost.

Standing note for whoever scopes #957 (DIST-MCPB-BUNDLE): review Daedalus's sparkline test heuristic and Klatch's `STEP-10-PHASE-1-PACKAGE-FORMAT.md` before defining the PM manifest schema. The format conventions should be conscious, not inherited.

---

## Item 2: AAXT/Colleague Test Cross-Reference + Fabrication Probes

Two sub-items, both actionable.

### 2a. Six-failure-mode vocabulary for #929 scorer — ADOPT

**Lead Dev**: If the DeepEval scorer's output vocabulary is still mutable, align it with AAXT's six-failure-mode taxonomy: Correct, Reconstructed, Confabulated, Absent, Phantom, Subliminal.

This does **not** change the Colleague Test rubric — the rubric stays as our quality gate. The AAXT vocabulary becomes the diagnostic layer underneath it. The Colleague Test tells you pass/fail; the AAXT taxonomy tells you *why* it failed.

The benefit is cross-project result comparison for free. When Klatch runs AAXT probes and we run DeepEval, both produce results in the same vocabulary. No translation needed.

If the scorer vocabulary has already been committed and changing it is nontrivial, this drops to a "nice to have for next revision" — don't break working infrastructure for vocabulary alignment. But if it's still soft, adopt now.

### 2b. Standalone fabrication probe set — DO IT

**Lead Dev**: Build a standalone 5-10 probe set covering the five absence categories (file, entity, memory, history, channel absence). Each probe asks the floor about something that doesn't exist and checks whether the response fabricates or honestly acknowledges absence.

This is a low-effort regression fence for the floor system prompt guardrail committed Apr 11. The guardrail addressed the specific Pattern-045 instance we caught in UAT (todo completion), but fabrication is a class of failure, not a single bug. We need to know whether the guardrail holds across diverse absence categories, not just the case that revealed the original failure.

Implementation: manually constructed probes, scored by hand initially. Doesn't depend on M2 testing infrastructure. Can be a discrete task within M2a or a standalone validation exercise.

**CXO**: The fabrication probe results may be relevant to your floor quality assessment. If the probes surface failures, they'd inform whether the Colleague Test rubric needs an explicit fabrication dimension (currently it catches this indirectly through Competence scoring, but not as a named failure mode).

---

## Item 3: ExportReviewPanel Trust Transitions — Reference for M3

**Status**: Noted for M3 scoping. No action now.

Klatch's accept/edit/reject pattern with provenance-tracked trust transitions is the closest reference implementation for ADR-054 composting write governance. Iris's design (review as part of the export service — "the moving company showing you what's being packed before the truck leaves") is the right UX metaphor for artifact lifecycle review.

Standing note for M3 scoping: review Klatch's `iris-to-daedalus-phase35d-spec-2026-04-14.md` when #952 (ARTIFACT-MODEL) reaches Architect review. The five-criteria filter for meaningful field notes (actionable, specific, non-obvious, relational, durable) should inform our write governance for artifact persistence.

---

## Summary

| Item | Action | Owner | Timing |
|------|--------|-------|--------|
| Sparkline test format discipline | Note for M5 scoping | Whoever scopes #957 | M5 |
| AAXT scorer vocabulary | Adopt if still mutable | Lead Dev | Now (low effort) |
| Fabrication probe set | Build 5-10 probes | Lead Dev | M2a or standalone |
| ExportReviewPanel reference | Note for M3 scoping | Architect | M3 |

---

*Chief Architect — April 16, 2026*
