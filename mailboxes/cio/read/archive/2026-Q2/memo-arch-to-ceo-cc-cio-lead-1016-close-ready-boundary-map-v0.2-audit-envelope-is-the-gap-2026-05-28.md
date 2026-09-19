---
from: Architect (Chief Architect)
to: CEO (xian)
cc: CIO (Chief Innovation Officer), Lead Developer
date: 2026-05-28
subject: #1016 close-ready — boundary-map v0.2 complete; the answer to your Apr-27 looseness-vs-tightness question is "audit-envelope is the systematic gap"
priority: standard — epic close-milestone; Architect side complete
response-requested: PM — disposition on #1016 close (Architect side done; only #1089 ship remains) + whether the Phase-4 "add audit-envelope per surface" recommendation becomes a tracked M3 issue
in-reply-to: (none — #1016 epic close-readiness report)
---

# #1016 close-ready — and it answered your founding question

The LLM-touch boundary-map is at v0.2 (`docs/internal/architecture/current/llm-touch-boundary-map.md`) — verification pass complete across 16 surfaces. The Architect side of #1016 is done. Surfacing the headline because it directly answers the question you raised Apr 27.

## Your Apr-27 question, answered

You worried: *"looseness versus tightness... it sounds like an element of inattention and ad hoc sloppiness... we need to get it right in a focused way and not as a side effect of other decisions."*

The verified matrix gives a clean answer: **the system is architecturally good at the "loose" half and systematically missing the "tight" half.**

- **Permissive-input (P) + safe-fallback (F)** — broadly present. The floor-backstop architecture (ADR-060) did this work well; some surfaces are overwhelmingly graceful (context_assembler has 64 fallback markers).
- **Schema-validation-at-consumption (S) + audit-envelope (A)** — near-universally absent. **Audit-envelope is absent at 0/16 verified surfaces** (only the dedicated ethics/output-filter/KG-internal paths have it).

So the looseness you sensed is real and *consistent* — not ad hoc sloppiness, but a systematic architectural lean: accept-LLM-output-gracefully is everywhere; validate-and-record-it is nowhere except the surfaces that got focused ADR-061 attention. The "getting it right in a focused way" you asked for is now scoped: it's one repeatable migration, not a per-surface scramble.

## The Phase-4 recommendation (the deliverable)

**Add an audit-envelope signal (primary) + a Pydantic schema-at-consumption contract (secondary) at each LLM-touch surface.** One repeatable shape, ~16 surfaces. Highest-leverage is the audit-envelope — it's the element NO surface has, and it's exactly what you named ("make boundary-mode visible to operators"). P + F are already supplied by the floor-backstop, so Phase 4 is narrower than the original 4-element framing implied.

## #1016 close status

| Phase | Status |
|---|---|
| Phase 1 survey (23 surfaces) | ✅ Apr 27 |
| Phase 3 principle (ADR-061 + v1.1 + ADR-063) | ✅ |
| Phase 2 matrix (boundary-map v0.2) | ✅ today |
| Phase 4 alignment status + recommendation | ✅ today |
| Phase-4 proof-of-concept (#1017 output filter) | ✅ |
| #1089 KG-privacy-filter ships (storage layer) | ⬜ in-flight (Lead Dev) |

**Architect side complete.** The epic closes when #1089 ships. The Phase-4 "add audit-envelope per surface" work is the natural M3 follow-on — recommend it becomes a tracked issue (sibling to #1016, or #1016's child) rather than reopening the epic.

## Two findings worth your awareness

1. **Inventory drift**: 2 of the original 23 surfaces no longer exist — `issue_analyzer` (renamed/removed) + orchestration-tasks (OrchestrationEngine deleted #1094; dispatch now via task_type registry). The boundary-map's own surface-list is a Pattern-073 instance at the inventory layer; v0.2 flags both. A clean example of why the fresh-verification-pass mattered — the Apr-27 inventory had drifted.

2. **One anomaly for a confirming read**: `personality_bridge` showed 0 fallback markers (either a pure deterministic transform with no failure path needed, or a genuine safe-fallback gap). Flagged [Vc] in the matrix; wants a deep read before its score is decision-relied-upon. Minor; doesn't change the headline.

## What this memo IS / IS NOT

- **IS**: #1016 close-readiness report; the boundary-map v0.2 headline; Phase-4 recommendation as a tracked-issue candidate
- **IS NOT**: a request to close #1016 right now (it closes on #1089 ship); not reopening the epic for Phase-4 (that's M3 follow-on)

## Cross-references

- Boundary-map v0.2: `docs/internal/architecture/current/llm-touch-boundary-map.md`
- #1016 epic: https://github.com/mediajunkie/piper-morgan-product/issues/1016
- ADR-061 / ADR-063 (the principle + READ-side)
- #1089 (storage-layer alignment, in-flight)
- methodology-30 Consumer-Trace (the discipline the verification pass applied)

— Architect, 2026-05-28 ~13:50 PDT (Day-2 Fire 7; cycle-driven; the verification pass turned out to produce the Phase-4 prioritization, not just confirm the matrix)
