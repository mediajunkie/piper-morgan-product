# Audit: #1252 Gameplan against `knowledge/gameplan-template.md` (v9.5)

_Lead Dev · 2026-06-15 · audit-cascade GAMEPLAN gate. Template open during audit._

| Template Requirement | Status | Notes |
|---|---|---|
| Phase -1 Part A (current understanding) | ✅ | grounded in #1241 audit + ADR-071 (not assumed) |
| Phase -1 Part A.2 (worktree assessment) | ✅ | ephemeral default (Option B); noted A.2's `.trees/` flow is deprecated (#1206 item-2) |
| Phase -1 Part B (PM verification) | ✅ | SATISFIED — PM endorsed the refactor + directed gameplan-first; ADR ratified |
| Phase -1 Part C (proceed/revise) | ✅ | PROCEED |
| Phase 0 (GitHub investigation) | ✅ | issues verified (#1252/#1238/#1250/#1248/#1239); current state from audit |
| Phase 0.5 (FE-BE contract) | ✅ | scoped to #1250/#1248; core is data-layer |
| Phase 0.6 (data flow) | ✅ | the core — principal origination→threading→data-layer; #490 lookup-key pitfall named |
| Phase 0.7 (conversation design) | ✅ | Not applicable per template's own condition (not conversational); not a unilateral N/A |
| Phase 0.8 (post-completion integration) | ⚠️→✅ | **GAP FIXED**: was missing. Refactor changes DB records (owner_id columns/backfill/drop) → applies. Added side-effects table + downstream-behavior table + verification queries (incl. the #1250 orphan-FK check) |
| Phases 1-N (with deliverables + DDD/TDD) | ✅ | P1–P8 + parallel #1248 + Phase Z; per-file detail deferred to the PROMPTS gate (progressive bookending) |
| Multi-Agent Coordination Plan (routing/wiring integration tests) | ⚠️→✅ | **GAP FIXED**: was missing. Added — deployment approach + the #521 routing-integration-test + #490 wiring-integration-test callouts (directly relevant to the P5 D4-threading) + cross-validation gate |
| Phase Z (final bookending & handoff) | ✅ | present |
| Success Criteria (measurable) | ✅ | 5 measurable criteria |
| Test Strategy | ✅ | DDD+TDD per phase; layers; privacy-isolation assertions; env-strip |
| Rollback Plan | ✅ | per-phase/per-commit; the m-40 shim is the safety net; sequence-safety |
| Dependencies | ✅ | internal (P-order) + external (ADR-070 D8, PPM entity-model) + Arch P0 confirm |
| GitHub Progress/Closeout Discipline | ✅ | per-phase close-issue-properly + decisions.log + the issue completion matrix (referenced) |

## Gaps found + fixed (before proceeding to execution)
1. **Phase 0.8 (Post-Completion Integration)** — missing. The template applies it to features that change DB records; this refactor does (schema migrations + backfill + column drops). Added migration-side-effects + downstream-behavior tables + verification SQL (including the `learning_settings` orphan-FK check that validates #1250).
2. **Multi-Agent Coordination + integration-test discipline** — missing. Added the deployment approach + the routing-integration (#521) and wiring-integration (#490) test callouts — directly load-bearing for P5 (the D4 threading is a wiring change; a mocked-internal test would hide the very degradation being fixed).

## Result
All template requirements ✅ after the 2 fixes. **GAMEPLAN gate PASSED.** Next: per-phase **PROMPTS gate** when each phase is picked up (the gameplan defers per-file breakdown there — progressive bookending). Recommended first execution: P0 Arch-confirm → P4 ((a,3) leak fixes, independent privacy win) → P1 → P2 (#1238) … per the execution order.
