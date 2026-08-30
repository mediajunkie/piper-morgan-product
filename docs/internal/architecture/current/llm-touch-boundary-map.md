# LLM-Touch Boundary Map — #1016 Phase 2/4 Closing Document

**Status**: **v0.4 (2026-05-30)** — `llm_classifier` fresh-verification complete (PM picked option B); all #1016 close-criteria met; **#1016 ready to close**. Plus one Pattern-073 instance candidate surfaced (`_fallback_classify` production-orphan) — flagged for separate disposition.

**v0.4 finding**: `llm_classifier` deep-read (per methodology-30 5-step trace procedure) corrected one Phase 1 score and surfaced one Pattern-073 instance candidate:
- **A (audit envelope) corrected ◐ → ❌**: zero audit markers across all 3 files (`llm_classifier.py`, `classifier.py`, `prompts.py`). The Phase 1 "audit partial" assertion was incorrect — there are no partial audit-envelope writes; there are none. This brings the verified-no-audit-envelope count to 10/10 surfaces, reinforcing the v0.2 consolidated finding.
- **Pattern-073 instance candidate**: `_fallback_classify` at `services/intent_service/classifier.py:934` is **production-orphaned** — 0 production callers, 8+ test callers (`tests/unit/services/test_intent_search_patterns.py` + 2 archives). The method's name and docstring assert "fallback classification"; the production fallback is actually `LowConfidenceIntentError → middleware → floor` per ADR-060/061 floor-first routing. Doc-asserted-behavior at the code layer; production reality differs. Same shape as `require_request_context` orphan from #1015 audit. Filing as Pattern-073 instance candidate for CIO disposition (separate from #1016 close).
- **Other elements (P / S / F) confirmed ✅**: deep-read traces (a) raw `message: str` accepted (P), (b) `_validate_confidence` + confidence threshold + `IntentCategory` enum coercion + multi-stage JSON-parse fallback at consumption (S), (c) `LowConfidenceIntentError` → middleware → floor fallback path operates (F).

**v0.3 update**: #1089 (KG-privacy-filter, storage-layer alignment) **CLOSED** following PM ratification May 20 + Lead Dev shipping Phase 0 with safety-net pragmatic interpretation (verified at #1089 Phase 0 + Increments 4 + 5; 72 tests passing). The storage-layer boundary is now structurally complete alongside ADR-061 (input + output WRITE) + ADR-063 (output READ). The three boundary layers identified in #1089 Phase 0 design (input / output / storage) all aligned.

**Prior status (v0.2, 2026-05-28)**: Phase 2 matrix + Phase 4 alignment status for epic #1016. Verification pass complete (16 surfaces [V/Vc]-verified + 5 [↑]-aligned + 2 inventory-drift). The Architect side of #1016 is complete; epic closes when #1089 KG-privacy-filter ships.

## v0.2 headline finding (the answer to #1016's founding question)

#1016 (PM, Apr 27): *does the system handle LLM-output looseness without sacrificing structure where structure matters?* The verified matrix answers it cleanly:

**Permissive-input (P) + safe-fallback (F) are broadly present; schema-validation-at-consumption (S) + audit-envelope (A) are near-universally absent.** The system is architecturally good at the **"loose" half** (accept LLM output gracefully — the floor-backstop did this work) and systematically missing the **"tight" half** (validate structure + record for operators). PM's looseness-vs-tightness worry was well-founded: the looseness is real and consistent; the tightness gap is the Phase-4 work.

- **A (audit-envelope)**: absent at 0/16 verified surfaces (only the dedicated ethics/output-filter/KG-internal paths per ADR-061/063/#1089 have it). **This is the single most-consistent gap** — and it's exactly #1016's stated concern ("make boundary-mode visible to operators").
- **S (schema-at-consumption)**: absent or partial at nearly all surfaces (most have 0 schema markers; a few have isinstance/dict-checks).
- **P + F**: broadly present (some surfaces overwhelmingly so — `context_assembler` 64 fallback markers, `conversation_context` 14, `workspace_memory` 11).

**Phase-4 recommendation**: a single repeatable cross-surface migration — **"add an audit-envelope signal (primary) + a Pydantic schema-at-consumption contract (secondary) at each LLM-touch surface."** ~16 surfaces; one shape; not bespoke per-surface. Highest-leverage = audit-envelope (operator legibility). The floor-backstop architecture already supplies P + F.

**Inventory drift caught**: 2 of the original 23 Phase-1 surfaces no longer exist — `issue_analyzer` (not locatable; renamed/removed) + orchestration-tasks (OrchestrationEngine deleted #1094; dispatch now via `task_type` registry). The boundary-map's surface list is itself a Pattern-073 instance at the inventory layer — v0.2 flags both for drop/re-map.
**Author**: Chief Architect
**Companion to**: ADR-061 (LLM-Touch Boundary Enforcement — the principle), ADR-063 (User-Facing Audit Envelope Read Surface — the READ-side)
**Epic**: #1016 (Phase 1 survey closed Apr 27, 23 surfaces; this doc is Phase 2 matrix + Phase 4 status)

---

## Purpose

#1016 asked: how does the system handle the inherent slack of LLM output without sacrificing structure where structure matters? Phase 1 (Apr 27) surveyed 23 LLM-touch surfaces. This document is the **Phase 2 analysis matrix** (each surface scored against the four-element principle) + **Phase 4 alignment status** (aligned / in-flight / gap), and names the governing ADR/Pattern per surface.

## The four-element principle (from ADR-061)

At every LLM-touch surface where LLM output is consumed or natural-language input is evaluated, four elements should be present:

1. **Permissive input shape** — boundary validation does not constrain input to rigid enums/patterns; natural-language is fuzzy
2. **Schema validation at consumption** — parse + validate against a structured contract at the point of use; structured fallback on failure
3. **Safe-fallback path** — a known path runs when validation fails (floor LLM competence; redaction; canned response; retry)
4. **Audit envelope** — every LLM-touch event records (surface, output size, validation result, action taken) for operator legibility

ADR-063 established the **READ-side complement** for the audit-envelope element (user-visible field set / schema-at-request / safe-fallback-for-missing / JWT-bound access).

## Score provenance

Scores below are marked:
- **[P1]** — carried from Phase 1 characterization (Apr 27); not re-verified fresh in this pass
- **[↑]** — updated since Phase 1 because an ADR/issue shipped that changes the score
- Final #1016 close wants a **fresh per-surface verification pass** to confirm [P1] scores still hold (see §"What still needs verification")

## The matrix

Elements: **P** = permissive input · **S** = schema validation at consumption · **F** = safe-fallback · **A** = audit envelope. ✅ present / ◐ partial / ❌ absent.

### Detection / enforcement (1 surface)

| Surface | P | S | F | A | Governing | Alignment |
|---|---|---|---|---|---|---|
| `boundary_enforcer` (semantic detector) | ✅ | ✅ | ✅ | ✅ [↑] | ADR-061 v1.0 + #1004 | **Aligned** — the reference instance; all 4 elements post-#1004 |

### Output-consuming surfaces (12)

| Surface | P | S | F | A | Governing | Alignment |
|---|---|---|---|---|---|---|
| `conversational_floor` | ✅ | ◐ | ✅ | ◐ [↑] | ADR-060 + ADR-061 | Aligned-ish — floor IS the safe-fallback; audit via #1017 output filter |
| Output content filter (`OutputFilterDecision`) | ✅ | ✅ | ✅ | ✅ [↑] | ADR-061 v1.1 + #1017 | **Aligned** — shipped output-side companion |
| `content_generator` (GitHub) | ◐ | ❌ | ◐ | ◐ [↑] | ADR-061 (target) | In-flight — #1017 filter covers PII; structured-fallback gap |
| `document_handlers` | ✅ | ❌ | ◐ | ❌ [Vc 05-28] | ADR-061 (target) | Gap — coarse-verified (`services/intent_service/document_handlers.py`): light fallback (F◐), no schema (S❌), no audit-envelope (A❌) |
| `issue_analyzer` | — | — | — | — [V 05-28] | — | **NOT LOCATED** — no matching file in `services/` (renamed/removed since Phase 1). Inventory drift; drop or re-map in v0.2. |
| `knowledge_graph/ingestion` | ◐ | ◐ | ◐ | ◐ [↑] | ADR-061 + #1089 | In-flight — KG-privacy-filter (#1089) adds storage-side audit |
| `project_context` | ◐ | ❌ | ✅ | ❌ [V 05-28] | ADR-061 (target) | Gap — verified: custom exceptions + default-project fallback (F upgraded ◐→✅); S+A absent |
| `llm_classifier` (intent) | ✅ | ✅ | ✅ | ❌ [V 05-30] | ADR-061 + ACTION_REGISTRY | **Verified v0.4** — P/S/F confirmed via methodology-30 trace (raw `message: str` at entry; `_validate_confidence` + `IntentCategory` enum + multi-stage JSON-parse at consumption; `LowConfidenceIntentError → middleware → floor` fallback). **A corrected ◐→❌**: zero audit markers across all 3 files (llm_classifier.py + classifier.py + prompts.py). #1117 temporal-overgreedy is a Phase-4 alignment instance here. **Pattern-073 instance candidate surfaced**: `_fallback_classify` at `classifier.py:934` is production-orphaned (0 prod callers; 8+ test callers); doc-asserted-behavior differs from production reality. |
| `slot_extractor` | ✅ | ◐ | ✅ | ❌ [V 05-28] | ADR-061 (target) | Gap — verified (`services/slot_filling/slot_extractor.py`): graceful empty-dict fallback (F upgraded ◐→✅) + dict-shape check (S partial, no Pydantic); `logger.warning` on parse-fail is operational not audit-envelope (A absent) |
| `work_item_extractor` | ✅ | ◐ | ✅ | ❌ [Vc 05-28] | ADR-061 (target) | Gap — coarse-verified (`services/domain/work_item_extractor.py`): strong fallback (F✅, 9 markers) + some parse/validate (S◐); no audit-envelope (A❌) |
| `text_analyzer` | — | — | — | — | — | **SURFACE GONE** — `services/analysis/text_analyzer.py` disposed 2026-08-30 (census disposal Batch 3; zero production callers — only `document_analyzer` was live in the analysis package). Row retained for inventory history. |
| `document_analyzer` | ✅ | ❌ | ◐ | ❌ [Vc 05-28] | ADR-061 (target) | Gap — light fallback ◐, no schema, no audit |
| orchestration tasks (per-task LLM output) | — | — | — | — [V 05-28] | #1020 | **SURFACE GONE** — OrchestrationEngine deleted (#1094 γ-preserve). Per-task LLM-output dispatch now flows through `task_type` registry (Pattern-072); #1020's framing is stale. Inventory drift. |

### Input-shaping surfaces (5)

Phase 1 finding: input-side scores **2/4** structurally (P ✅ + F ✅; S ❌ + A ❌) — better-shaped than output-side because the floor-input pipeline had more architectural attention.

| Surface | P | S | F | A | Governing | Alignment |
|---|---|---|---|---|---|---|
| `context_assembler` | ✅ | ◐ | ✅ | ❌ [Vc 05-28] | ADR-061 (target) | Partial 2.5/4 — coarse-verified: heavy fallback (F✅, 64 markers) + some validation (S◐, 3); no audit ("what context assembled for this call") |
| `conversation_context` | ✅ | ❌ | ✅ | ❌ [Vc 05-28] | ADR-061 (target) | Partial — heavy fallback (F✅ 14 markers); no schema; no audit |
| `lens_inference` | ✅ | ◐ | ✅ | ❌ [Vc 05-28] | ADR-061 (target) | Partial — coarse-verified: fallback ✅ (6), some validation ◐ (1), no audit |
| `personality_bridge` | n/a | n/a | n/a | ◐ [V 05-28] | — | **RECLASSIFY** — deep-read resolved the F-anomaly: it's a *pure deterministic transform over already-validated `Intent` objects* (no `client.`/`llm`/`completion` calls; `transform`/`_humanize_action`/`_express_confidence`). It's DOWNSTREAM of llm_classifier's validation — not a raw-LLM-output boundary. The 4-element principle applies weakly (no LLM-output-failure-path to fall back from). Audit would still help (record the transform decision) but P/S/F are n/a. **Likely mis-classified in the Phase-1 inventory; v0.2 reclassifies as presentation-transform, not boundary.** |
| `warmth_calibration` | ✅ | ❌ | ◐ | ❌ [Vc 05-28] | ADR-061 (target) | Partial — coarse-verified: light fallback ◐ (2), no schema, no audit |

### Memory surfaces (5)

| Surface | P | S | F | A | Governing | Alignment |
|---|---|---|---|---|---|---|
| `conversational_memory` | ✅ | ❌ | ✅ | ❌ [Vc 05-28] | ADR-054 + ADR-061 | Partial — fallback ✅; no schema; no audit |
| `user_history` (Layer 3) | ✅ | ❌ | ✅ | ❌ [Vc 05-28] | ADR-054 (#1021 active) | Partial — Layer 3 active; **A corrected ◐→❌** (no audit_transparency/log_ethics markers; earlier ◐ was optimistic) |
| `greeting_context` | ✅ | ❌ | ◐ | ❌ [Vc 05-28] | ADR-054 | Partial — light fallback ◐ (alive-scaffolding per Pattern-064); no schema; no audit |
| `conversation_summarizer` | ✅ | ❌ | ◐ | ❌ [Vc 05-28] | ADR-054 + ADR-061 | Partial — coarse-verified: light fallback ◐ (1), no schema, no audit |
| `workspace_memory` | ✅ | ❌ | ✅ | ❌ [Vc 05-28] | ADR-054 | Partial — heavy fallback (F✅ 11 markers); no schema; no audit |

### Storage surface (1 — added since Phase 1)

| Surface | P | S | F | A | Governing | Alignment |
|---|---|---|---|---|---|---|
| KG-internal privacy filter | ✅ | ✅ | ✅ | ✅ [↑ v0.3] | #1089 (CLOSED 2026-05-30) | **Aligned** — Phase 0 + Increments 4 + 5 shipped; service-layer dispatch + repository safety-net + audit envelope; storage layer of three-layer boundary now structurally complete |

## Phase 4 alignment summary

**Aligned (4/4 or aligned-ish)**: boundary_enforcer, output content filter, llm_classifier (modulo #1117), conversational_floor. The detection + output + intent-classification surfaces are the most-mature — they got the focused ADR-061 + #1017 attention.

**In-flight**: content_generator (PII covered, fallback/audit pending), knowledge_graph/ingestion + KG-internal (#1089 shipping), user_history (Layer 3 active).

**Gap (0-2/4)**: the bulk of output-consuming surfaces (issue_analyzer, project_context, slot_extractor, work_item_extractor, text_analyzer, document_analyzer, orchestration tasks) + all 5 input-shaping surfaces (uniformly 2/4 — need schema + audit) + most memory surfaces.

**The dominant gap shape**: **schema validation at consumption (S) + audit envelope (A) are the two most-commonly-absent elements.** Permissive-input (P) + safe-fallback (F) are widely present (the floor backstops most surfaces). So Phase 4 alignment work is mostly "add a Pydantic schema contract at consumption + an audit signal" per surface — a repeatable shape, not bespoke-per-surface.

## Phase 4 sequencing (by stakes)

1. **Highest stakes** (user-facing output or safety): output content filter ✅ done; KG-internal #1089 in-flight; content_generator next
2. **Medium** (intent + classification quality): llm_classifier #1117 (temporal-overgreedy — already a named Phase-4 instance, moving to M3 with #1016 per my May 28 disposition)
3. **Lower** (input-shaping + memory — the 2/4 surfaces): batch "add schema + audit" as a repeatable migration; lower urgency since P+F already present

## What still needs verification (honest gap in this v0.1)

The [P1] scores are carried from the Apr 27 Phase 1 characterization, not re-verified against current code in this pass. Before #1016 fully closes, a **fresh per-surface verification pass** should confirm the [P1] scores still hold (some surfaces may have drifted aligned or gap-ward since Apr 27 — and per methodology-30 Consumer-Trace + the #1089 spec-thinko lesson, asserted scores want consumer-trace confirmation). That verification is a bounded follow-up (re-grep each surface's input-shape / schema / fallback / audit), schedulable as a cycle task or a Lead-Dev-paired pass.

### Verification progress (incremental, via cycle low-priority work per v0.6.3)

- **2026-05-28** (Day-2 Fire 4): verified `slot_extractor` + `project_context` [V 05-28] — deep reads. **Finding: [P1] output-side scores UNDER-rate safe-fallback (F).** Both had clearer graceful-fallback than [P1] ◐ suggested (empty-dict-on-fail; default-project) — both upgraded ◐→✅ on F.
- **2026-05-28** (Day-2 Fire 5): coarse-verified (marker-count, not deep read) `work_item_extractor` + `text_analyzer` + `document_handlers` [Vc 05-28]. **Sharpened finding across 5 verified output-side surfaces: audit-envelope (A) is UNIVERSALLY ABSENT (0/5 have one); schema-at-consumption (S) is weak/absent; safe-fallback (F) ranges ◐–✅ (present); permissive-input (P) ✅.** So the Phase-4 gap concentrates on **A first (most-absent element), S second.** P+F are largely in place via the floor-backstop architecture. **Phase 4 narrows to: "add an audit-envelope signal per LLM-touch surface (primary), add a Pydantic schema contract at consumption (secondary)."** That's a tighter, more-repeatable migration than the original 4-element framing implied.
- **2026-05-28** (Day-2 Fire 6): coarse-verified `context_assembler` + `lens_inference` + `warmth_calibration` + `conversation_summarizer` [Vc 05-28]. **The "audit-envelope universally absent" finding HOLDS on input-shaping + memory surfaces.** Now **0/9 verified surfaces (5 output + 4 input/memory) have an audit-envelope.** `context_assembler` notably has 64 fallback markers (heavy safe-fallback) — confirms the input-construction stack is the best-shaped (2.5/4) but still A❌.
- **CONSOLIDATED FINDING (9/18 surfaces verified)**: **the audit-envelope (A) element is the single most-consistent gap in the entire LLM-touch boundary — absent at every verified surface (0/9).** This directly answers #1016's motivating concern ("make boundary-mode visible to operators"): operators currently have NO audit-envelope legibility at any LLM-touch surface except the dedicated ethics/output-filter path (ADR-061/063). **Highest-leverage Phase-4 migration = add a uniform audit-envelope signal at every LLM-touch surface** (one repeatable shape, applied ~18×); schema-at-consumption (S) is the secondary gap; permissive-input (P) + safe-fallback (F) are largely already present via the floor-backstop architecture.
- **Verification-depth note**: [V] = deep read (control flow confirmed); [Vc] = coarse (marker-count heuristic — reliable for A-absence, approximate for S/F). Decision-relevant [Vc] scores want a confirming deep read. Remaining [P1] surfaces: ~9 (continue 2-3/fire).

## #1016 close criteria

- [x] Phase 1 survey (Apr 27 — 23 surfaces)
- [x] Phase 3 principle (ADR-061 + v1.1 + ADR-063)
- [x] Phase 2 matrix (this document, v0.2 + v0.3 + v0.4)
- [x] Phase 4 alignment status + sequencing (this document)
- [x] **#1089 SHIPPED** (Lead Dev — storage-layer alignment closed 2026-05-30; Phase 0 + Increments 4 + 5; 72 tests passing)
- [x] At least one Phase-4 gap-surface migrated as proof-of-concept (#1017 output filter; #1089 KG storage layer; multiple PoCs landed)
- [x] **Fresh per-surface verification of remaining [P1] score: `llm_classifier` COMPLETE** (v0.4; methodology-30 trace; A corrected ◐→❌; P/S/F confirmed; Pattern-073 instance candidate surfaced for separate disposition)

### v0.4 close disposition

**All 7 close criteria met. #1016 closes as completed-as-umbrella** with this boundary-map (v0.4) as the durable artifact. PM picked option (B) — "close after one more fire" — at 1:44 PM 2026-05-30 with framing: *"I feel we have often cut corners but rarely over-checked things."*

The (B) verification justified itself: the fresh-read corrected one Phase 1 score (A: ◐→❌ at llm_classifier) and surfaced one new Pattern-073 instance candidate (`_fallback_classify` production-orphan at `classifier.py:934`). An (A) close-without-verification would have left the incorrect Phase 1 [P1] score in the matrix and missed the production-orphan finding.

**Closure narrative**: #1016 was filed Apr 27 with PM's worry that the system's looseness-vs-tightness handling was incidental rather than principled. The epic's Phase 1-5 work produced:
- The architectural principle (four-element ADR-061 + READ-side ADR-063)
- The surface catalog (this document — 24 surfaces enumerated, 17 verified)
- The cascading alignment work (#1004 BoundaryEnforcer, #1017 output filter, #1018 audit envelope write, #1019 adaptive_boundaries, #1089 KG storage layer, #1095 transparency auth gates)
- The Phase 4 sequencing direction (audit-envelope gap is the dominant pattern; repeatable migration shape, not bespoke per-surface)

The principle is established. The alignment work is sequenced. The umbrella's job is done.

**Outstanding cohort work continues independent of #1016 close**:
- Phase 4 alignment migrations on the 15+ surfaces with the audit-envelope gap (the consolidated v0.2 + reinforced-by-v0.4 finding — repeatable per-surface migration shape)
- #1117 temporal-overgreedy (named Phase-4 instance for llm_classifier; moved to M3 per Architect May 28 disposition)
- Pattern-073 instance candidate disposition for `_fallback_classify` (CIO methodology call)
- methodology-30 fresh-verification cadence — opportunistic per-surface re-verification when surfaces are touched in other work

## Cross-references

- #1016 epic + Phase 1 comments: https://github.com/mediajunkie/piper-morgan-product/issues/1016
- ADR-061 (the principle): `docs/internal/architecture/adrs/adr-061-llm-touch-boundary-enforcement.md`
- ADR-063 (READ-side): `docs/internal/architecture/adrs/adr-063-user-facing-audit-envelope-read-surface.md`
- #1089 (storage-layer alignment, in-flight): KG-privacy-filter
- #1117 (llm_classifier Phase-4 instance): temporal-overgreedy → M3 with #1016
- Pattern-064 (alive scaffolding — greeting_context was an instance)
- methodology-30 (Consumer-Trace Verification — the discipline for the fresh-verification pass)

— Chief Architect, 2026-05-30 v0.4 (llm_classifier fresh-verification per PM option-B; A corrected ◐→❌; Pattern-073 instance candidate surfaced; #1016 ready to close)
— Chief Architect, 2026-05-30 v0.3 (#1089 closure absorbed; close-recommendation surfaced)
— Chief Architect, 2026-05-28 v0.2 (verification pass: 16 surfaces; consolidated finding on audit-envelope gap)
— Chief Architect, 2026-05-28 v0.1 (Phase 2/4 closing document for #1016)
