# M2g Scoping Survey

**Date**: 2026-05-13 (EOD)
**Purpose**: Survey + recommended structure to inform tomorrow AM's M2g kickoff
**Status**: Survey only — no Phase 0 audits yet. Each issue still needs its own audit before scoping a gameplan.

---

## Surface

10 open issues labeled `M2g`. All from Architect's Apr 27 systematic codebase review (batches 1–4 + cross-cutting insights).

---

## ⚠️ Critical issue worth knowing about

**#1017 — Post-generation content filter for LLM outputs (PII/safety)** is labeled `priority: critical`. This is the only critical-priority issue in M2g. Real risk: LLM outputs reach users with no PII or safety filter today.

Affected surfaces named in the body:
- `services/intent_service/document_handlers.py` (Q&A, doc synthesis → chat)
- `services/intent_service/conversational_floor.py` (the floor → chat)
- `services/integrations/github/issue_analyzer.py` (issue analysis → posted to GitHub)

This was PA's Apr 17 "Gap 2" call (post-generation ethics check). May warrant earlier attention than other M2g items even if the rest of M2g defers.

---

## Recommended structure: M2g-A through M2g-D

### M2g-A — Owner reviews (cheap kickoff)
| # | Title | Priority | Sizing |
|---|---|---|---|
| **#1000** | Owner-review: services/auth/ fallback paths | medium | ~1-2 hr |
| **#999** | Owner-review: services/mcp/consumer/ fallback paths | low | ~1-2 hr |

**Shape**: confirmation passes, not architectural changes. Owner reads 3 files, attests they're legitimate graceful-degradation patterns (not silent posture-weakening). Filed from #997 mock-sweep audit.

**Why good first**: builds M2g momentum on low-risk work, demonstrates the "subsystem-owner confirmation" pattern, and gets the M2g momentum off the line cheaply.

### M2g-B — Dead-code cleanup (Pattern-067 family)
| # | Title | Sizing | Shape |
|---|---|---|---|
| **#1019** | adaptive_boundaries scaffolding — complete or remove | ~3-4 hr | PM call on direction; mechanical after |
| **#1010** | knowledge_graph_service refactor + remove legacy boundary_enforcer | ~4-6 hr | Refactor blocks deletion |
| **#1021** | UserHistoryService Layer 3 has no DB backend | ~4-8 hr | "Build or delete" call needed |

**Shape**: Pattern-067 family — "alive but inert" / "designed but not implemented" code paths. Each has a clean audit-cascade Phase 0 to determine direction (complete the work vs. delete it).

**Why second**: pairs naturally with the discipline you've been applying across M2f — body-vs-reality checks first, then scope from there. #1019 is the most binary (literally "complete or remove") and would be a clean first audit-cascade.

### M2g-C — Critical safety
| # | Title | Priority | Shape |
|---|---|---|---|
| **#1017** | Post-generation content filter for LLM outputs (PII/safety) | **critical** | Design decision + new safety layer |

**Shape**: design-first; needs decision on filter shape (PII patterns, safety rules, where to insert in pipeline), then implementation across the 3 named surfaces. Sizing: probably 1-2 days including design alignment with Architect + CXO.

**Why named separately**: critical priority + cross-cutting risk. May want to surface to Architect / HOST before slotting into M2g-B's queue.

### M2g-D — Architecture epics (heavier, design-first)
| # | Title | Sizing | Shape |
|---|---|---|---|
| **#1015** | Complete ADR-051 RequestContext migration (Phase 2/3) | epic — multi-day | Touches many route handlers + service signatures |
| **#1016** | LLM-touch boundary principle — unified posture | epic | Cross-cutting; needs Architect-led design first |
| **#1020** | Per-task LLM output validation in OrchestrationEngine | ~1 day | Schema gates between workflow steps |
| **#1011** | Slash-command dispatch precedence | post-MVP design | Decision: should /standup run before or after ethics? |

**Shape**: each needs design conversation before implementation. #1011 and #1016 in particular have PM-decision elements baked in.

**Why last**: these are the bulk of M2g's "work" mass; sequencing them after the cheaper cleanup gives time for design conversations to mature in parallel.

---

## Recommended kickoff sequence (tomorrow AM)

**1. Quick triage call** (~15 min): you spot-check this survey, confirm the A→B→C→D grouping or rework it.

**2. M2g-A starter** (~2-3 hr Lead Dev): #999 + #1000 owner-review passes. Concrete, ships clean, builds momentum.

**3. M2g-B Phase 0 on #1019** (~30-45 min): audit-cascade Phase 0 on adaptive_boundaries (the "alive but inert" one). Surfaces the binary PM-decision (complete vs delete) and gameplan shape.

**4. Surface #1017** to relevant cohort: Architect for design read, HOST for safety posture, CXO for response-side voice. May warrant a memo before Lead Dev work starts.

**5. Tomorrow's stretch** (if time): Phase 0 audit on #1010 (knowledge_graph_service refactor) since it's the next-most-mechanical after #1019.

---

## What this survey is NOT

- Not a Phase 0 audit on any issue. Each still needs its own audit-cascade Phase 0 before scoping (per the discipline applied across M2f).
- Not a commitment to ordering. The A/B/C/D grouping is a shape proposal; you may want different sequencing (e.g., #1017 first because critical).
- Not an estimate for total M2g effort. Each issue's sizing is rough until its audit lands.

---

## Cross-references

- All 10 issues filed from Architect's Apr 27 systematic codebase review batches 1-4 + cross-cutting insights
- M2f's audit-cascade discipline (Pattern-067 first, scope second, ship third) directly applies
- #1083 (CHECKBOX-LINT tooling) — will help prevent the close-discipline gaps that surfaced today

— Lead Developer, 2026-05-13 EOD
