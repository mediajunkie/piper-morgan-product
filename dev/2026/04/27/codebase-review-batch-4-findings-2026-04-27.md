# Codebase Review Batch 4 — Findings (Track 1, Apr 27 late afternoon — #1016 Phase 1 closure)

**Author**: Chief Architect
**Date**: 2026-04-27
**Session**: `dev/2026/04/27/2026-04-27-0815-arch-opus-log.md`
**Surfaces reviewed**: Memory layer (`services/memory/`), Floor input-construction stack (`services/intent_service/{context_assembler, conversation_context, lens_inference, personality_bridge, warmth_calibration}.py`)
**Method**: 2 Explore subagents in parallel + Architect synthesis; **closing batch for #1016 Phase 1**
**Companion docs**: `codebase-review-batch-2-findings-2026-04-27.md`, `codebase-review-batch-3-findings-2026-04-27.md`

---

## Findings table

| ID | Finding | Surface | Severity | Effort | Status / Tracking |
|---|---|---|---|---|---|
| **IX** | `GreetingContextService` (244 LOC) is fully implemented + exported but never instantiated anywhere — PDR-002's adaptive-greeting feature is dead-on-arrival | Memory × PDR-002 | Cosmetic | trivial (delete or wire) | Folded into [#1012](https://github.com/mediajunkie/piper-morgan-product/issues/1012) dead-code sweep |
| **X** | `services/intent_service/context_assembler.py:341` calls `UserHistoryService.get_history_summary()` — method does not exist; only avoided runtime failure by try/except wrapper | Memory × Intent | Latent (fails if path exercised) | ~10 min | Folded into [#1012](https://github.com/mediajunkie/piper-morgan-product/issues/1012) (same pattern as Finding B's `get_selected_client` phantom) |
| **XI** | `UserHistoryService` Layer 3 (long-term cross-session memory) has only `InMemoryUserHistoryRepository`; no DB backend implementation exists | Memory × ADR-054 | Architectural debt (designed but unimplemented layer) | 4-6 days (3-phase scope) | **[#1021](https://github.com/mediajunkie/piper-morgan-product/issues/1021)** filed |
| **XII** | Memory layer has no audit trail — separate `AuditLog` table exists but memory retrieval/recording isn't logged; can't debug "why did Piper say that — was it remembered or hallucinated?" | Memory × Audit | Architectural debt (observability gap) | ~1 day | Folded into [#1018](https://github.com/mediajunkie/piper-morgan-product/issues/1018) audit log durability scope |
| **XIII** | No formal schema contract between `ContextAssembler` output and floor prompt expectations — `_format_domain_context()` does defensive `isinstance()` checks instead of schema validation. Adding a new context key requires touching both modules; drift risk | Input-construction | Architectural debt | 1-2 days (Pydantic model + validation) | Phase 4 alignment item under [#1016](https://github.com/mediajunkie/piper-morgan-product/issues/1016) |
| **XIV** | `services/mux/workspace_memory.py:161` comment claims "7-day window from ConversationalMemoryService" but the service uses `WINDOW_HOURS=24` — comment lies about implementation | Memory | Cosmetic | trivial (fix comment or fix code) | Folded into [#1012](https://github.com/mediajunkie/piper-morgan-product/issues/1012) |

## Smaller observations (no action needed)

| ID | Observation | Surface |
|---|---|---|
| XV | Privacy state (`PrivacyModeService._session_privacy`) is in-memory only — session-level privacy is ephemeral; retroactive privacy persists via `UserHistoryService.is_private` flag. Mixed durability is intentional but documentation-thin. | Memory |
| XVI | Janus memory research issues (#972-976) are research-phase only — none implemented in current Layer 1-3 architecture. Code predates research synthesis. Worth knowing when PRD-level memory work happens. | Memory |
| XVII | `personality_bridge.py` (290 LOC) is NOT in the floor input loop — applied to `Intent` post-classification but the floor only sees raw `Intent.category/action/confidence`. Personality narratives apply to *output formatting* later. Not a defect; worth knowing. | Input-construction |
| XVIII | Conversation history is capped at **6 turns** in floor prompt assembly (line 10100, 10247, 10327 in intent_service.py) but `ConversationContext.max_turns=10` (per PM-034). Intentional asymmetry: floor sees recent context, not full session history. Easy to miss without grep. | Input-construction |
| XIX | No token budgeting at the context-assembly layer — `ContextAssembler` is token-agnostic; LLM client handles truncation downstream. Acceptable for current scale; worth flagging for future scale. | Input-construction |

---

## Cross-cutting insights from this batch

### Insight 5: The phantom-method-call pattern recurs at multiple layers

Three findings across batches share the same pattern: **a method or function is called by name, but the called name does not exist** at the target. Wrapped in try/except, so the call site doesn't crash; but the intended behavior never happens.

- Batch 2 / Finding B: `services/intent/intent_service.py:8032` imports `get_selected_client` from `services.llm.clients` — function does not exist
- Batch 3 / Finding V: `services/api/health/staging_health.py:858+` imports `adaptive_boundary_system` and `audit_transparency_system` — actual singletons are `adaptive_boundaries` and `audit_transparency`
- Batch 4 / Finding X: `services/intent_service/context_assembler.py:341` calls `UserHistoryService.get_history_summary()` — method does not exist

These are scaffolding from earlier exploration that didn't get closed-out. The try/except masking is the methodological hazard: the system *appears* to work because the exception path is silent. **Phase 4 alignment item under #1016 (or as a sibling concern)**: a periodic phantom-call audit using static analysis (e.g., `mypy --strict`, or a lightweight `grep`-driven sweep matching `from X import Y` against `Y`'s actual presence in `X`) would catch these structurally.

For now: the dead-code sweep (#1012) is absorbing all three instances. Worth doing the sweep with a sharper eye for this pattern specifically.

### Insight 6: Input-side LLM-touch surfaces have *better* structural shape than output-side

Counter to my batch-3 framing that "most LLM-touch surfaces have no boundary posture at all," the input-construction stack actually exhibits **2-of-4 elements** of the working principle:

- ✅ **Permissive input shape** (Dict[str, Any] passed around)
- ❌ **Schema validation at consumption** (defensive isinstance checks, not schema)
- ✅ **Safe-fallback path** (fail-graceful per gatherer; missing data is silent absence, not error)
- ❌ **Audit envelope** (no record of what context was assembled for a given LLM call)

That's better than most output-side surfaces (which ranged 0-1 of 4). The asymmetry suggests **input-side architecture had more thought put into it** than output-side — probably because the floor LLM is downstream of well-developed intent classification work, while content-generation surfaces accreted as separate features without a unified boundary discipline.

This sharpens the Phase 4 alignment plan: input-side surfaces need the missing 2 elements (schema contract + audit signal); output-side surfaces need all 4. Different scope per surface.

### Insight 7: Memory layer is the canonical case of "designed but partially wired"

Of ADR-054's three layers:
- **Layer 1** (24-hour conversational memory): wired, DB-persisted, integrated ✅
- **Layer 2** (greeting context): coded + tested but never instantiated ⚠️
- **Layer 3** (long-term cross-session): coded but only in-memory repository ⚠️

The full ADR-054 vision is **one layer's worth of value today**. PDR-002's adaptive-greetings vision is downstream of Layer 2 and Layer 3, neither of which is production-functional.

This isn't unique to memory. The pattern shows up across the codebase: `adaptive_boundaries` is alive scaffolding (#1019); the LLM-output filter doesn't exist (#1017); audit log is in-memory only (#1018); orchestration's per-task validation is missing (#1020). **Multiple architectural layers are partially wired in similar shape**: the design is in code, the load-bearing integration is missing.

This is a methodological observation worth carrying forward: **"alive scaffolding"** (designed + coded + tested + exported, but never instantiated or never the load-bearing path) is a recurrent class of architectural debt. Worth a Pattern catalog entry, possibly as a sub-pattern of Pattern-062 (Assembly Assumption) or as its own pattern. CIO has equity here. Will queue for Phase 5 of #1016.

---

## #1016 Phase 1 — CLOSED

23 LLM-touch surfaces characterized across batches 2-4 (yesterday + today). Phase 1 survey is **substantively complete** for the LLM-touch boundary epic.

### Surface inventory (cumulative)

**Output-consuming surfaces** (batch 3):
1. `document_handlers.py` — Q&A, comparison, synthesis
2. `content_generator.py` — GitHub issue generation (the leading example: 4-of-4 elements)
3. `conversational_floor.py` — floor LLM responses
4. `issue_analyzer.py` — GitHub issue analysis
5. `knowledge_graph/ingestion.py` — relationship metadata generation
6. `project_context.py` — project name inference
7. `llm_classifier.py` — LLM-based classifier fallback (only surface with multi-stage retry)
8. `slot_extractor.py` — slot-value extraction
9. `work_item_extractor.py` — work item extraction
10. `text_analyzer.py` — text analysis
11. `document_analyzer.py` — PDF analysis
12. Orchestration tasks (`engine.py`) — multi-step LLM workflows

**Input-shaping surfaces** (batch 4):
13. `context_assembler.py` — category-specific context gathering
14. `conversation_context.py` — in-memory session state
15. `lens_inference.py` — conversation lens inference (with optional LLM decoder)
16. `personality_bridge.py` — personality context (NOT in floor input loop)
17. `warmth_calibration.py` — warmth level inference

**Memory surfaces** (batch 4):
18. `conversational_memory.py` — Layer 1 24-hour window
19. `user_history.py` — Layer 3 long-term (no DB backend)
20. `greeting_context.py` — Layer 2 (unused)
21. `conversation_summarizer.py` — rule-based summarization
22. `workspace_memory.py` — three-layer composition

**Detection / enforcement surfaces** (batches 2-3):
23. `boundary_enforcer_refactored.py` — substring detector (pre-#1004) + semantic detector (under #1004 in flight)

### Phase 1 → Phase 2 transition

Phase 2 (analysis matrix — score each surface against the 4 elements + identify the gap shape per surface) can begin from the captured findings. Phase 3 (principle articulation) follows once the matrix is filled in. Both are tractable now that surface coverage is complete.

**Plan**: Phase 2 starts in a future session (no rush); Phase 3 ratification will need a checkpoint with Lead Dev / CXO / CIO / PM before kicking off Phase 4 alignment work.

---

## Cumulative issue inventory (across batches 2-4)

| Issue | Title | Priority | Batch |
|---|---|---|---|
| [#1010](https://github.com/mediajunkie/piper-morgan-product/issues/1010) | ARCH-CLEANUP: Refactor knowledge_graph_service.py to domain layer | P3 | (pre-2) |
| [#1011](https://github.com/mediajunkie/piper-morgan-product/issues/1011) | ARCH-DESIGN: Slash-command dispatch precedence post-MVP | post-MVP | (pre-2) |
| [#1012](https://github.com/mediajunkie/piper-morgan-product/issues/1012) | ARCH-CLEANUP: Small dead-code sweep | P3 | 2 (+ B/C/D/F/G/IX/X/XIV folds) |
| [#1013](https://github.com/mediajunkie/piper-morgan-product/issues/1013) | ARCH-CLEANUP: /auth and /setup route prefixes | P2 | 2 |
| [#1014](https://github.com/mediajunkie/piper-morgan-product/issues/1014) | ARCH-CLEANUP: AuthMiddleware exclude_paths refactor | P3 | 2 |
| [#1015](https://github.com/mediajunkie/piper-morgan-product/issues/1015) | ARCH: Complete ADR-051 RequestContext migration (epic) | P2 | 2 |
| [#1016](https://github.com/mediajunkie/piper-morgan-product/issues/1016) | ARCH-DESIGN: LLM-touch boundary principle (epic) | P1 | 2 (Phase 1 CLOSED in batch 4) |
| [#1017](https://github.com/mediajunkie/piper-morgan-product/issues/1017) | ARCH-DESIGN: Post-generation content filter (PII/safety) | P1 | 3 |
| [#1018](https://github.com/mediajunkie/piper-morgan-product/issues/1018) | ARCH-CLEANUP: Persist ethics audit log to durable storage (+ memory audit trail per XII fold) | P1 | 3 |
| [#1019](https://github.com/mediajunkie/piper-morgan-product/issues/1019) | ARCH-CLEANUP: adaptive_boundaries scaffolding | P3 | 3 |
| [#1020](https://github.com/mediajunkie/piper-morgan-product/issues/1020) | ARCH-DESIGN: Per-task LLM output validation (orchestration) | P3 | 3 |
| **[#1021](https://github.com/mediajunkie/piper-morgan-product/issues/1021)** | ARCH-CLEANUP: UserHistoryService Layer 3 has no DB backend | P3 | 4 |

**Total: 12 issues filed across 2 days of architectural review.** Of these:
- 3 are P1 (production-relevance): #1016 (epic), #1017, #1018
- 3 are P2 (real defects): #1013, #1015 (epic)
- 6 are P3 (architectural debt): #1010, #1012, #1014, #1019, #1020, #1021

#1016 Phase 1 is closed; Phase 2-5 sequenced via Phase 2 → checkpoint → Phase 3 (principle ratification) → Phase 4 (per-surface alignment, sequenced via gap matrix from Phase 2) → Phase 5 (documentation).

---

## End of #1016 Phase 1

Track 1 codebase review continues tomorrow with the non-LLM-touch surfaces (memory layer further depth as needed; plugin system; learning layer; database/repositories layer; test infrastructure; integrations; auth; trust; mux; scheduler). Per Architect's Apr 27 calibration: ~50-60% through Track 1 overall; 3-5 more sessions to architectural close.

---

*Last Updated: 2026-04-27 — batch 4 synthesis + #1016 Phase 1 close*
