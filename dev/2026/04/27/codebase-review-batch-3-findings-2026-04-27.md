# Codebase Review Batch 3 — Findings (Track 1, Apr 27 afternoon)

**Author**: Chief Architect
**Date**: 2026-04-27
**Session**: `dev/2026/04/27/2026-04-27-0815-arch-opus-log.md`
**Surfaces reviewed**: Ethics infrastructure full surface (`services/ethics/`), LLM-driven content generation (12 surfaces across `services/intent_service/`, `services/integrations/`, `services/knowledge/`, `services/project_context/`), Orchestration + Process layers (`services/orchestration/`, `services/process/`)
**Method**: 3 Explore subagents in parallel + Architect synthesis; LLM-touch boundary characterization lens applied per epic #1016
**Companion doc**: `dev/2026/04/27/codebase-review-batch-2-findings-2026-04-27.md`

---

## Findings table

| ID | Finding | Surface | Severity | Effort | Status / Tracking |
|---|---|---|---|---|---|
| **I** | No PII / safety filter on LLM-generated output reaching users — Apr 17 PA "Gap 2" confirmed absent | Ethics × content gen × conversational | **P1 (production-relevance)** | 8-10 days (3-phase scope) | **[#1017](https://github.com/mediajunkie/piper-morgan-product/issues/1017)** filed |
| **II** | Ethics audit log is in-memory only (Python list, 10K cap, 90-day TTL) — user-facing transparency endpoints can lie after restart | Ethics | **P1 (production-relevance)** | 4-5 days (3-phase scope) | **[#1018](https://github.com/mediajunkie/piper-morgan-product/issues/1018)** filed |
| **III** | `adaptive_boundaries.py` is alive scaffolding — module is called but learned patterns don't influence decisions (hardcoded enhancement dict at `boundary_enforcer_refactored.py:196-204`); commented-out integration at `:273-277` | Ethics | P3 | ~1-3 days (recommend Path C: remove for now) | **[#1019](https://github.com/mediajunkie/piper-morgan-product/issues/1019)** filed |
| **IV** | `OrchestrationEngine` multi-step LLM workflows have no schema validation between steps — malformed task output cascades to downstream tasks (worst case: garbage to GitHub) | Orchestration | P3 | 4-5 days (3-phase scope) | **[#1020](https://github.com/mediajunkie/piper-morgan-product/issues/1020)** filed |

## Smaller findings (folded into existing or new minor issues)

| ID | Finding | Surface | Disposition |
|---|---|---|---|
| **V** | `services/api/health/staging_health.py:858+` imports non-existent `adaptive_boundary_system` (actual singleton: `adaptive_boundaries`) — runtime NameError if reached | Ethics × health | Folded into [#1019](https://github.com/mediajunkie/piper-morgan-product/issues/1019) (cleanup includes removing broken health imports) |
| **VI** | `ethics_metrics.get_prometheus_metrics()` hardcodes `environment="staging"` (line 238) | Metrics | Folded into [#1012](https://github.com/mediajunkie/piper-morgan-product/issues/1012) dead-code sweep, item to add: parameterize or remove environment hardcode |
| **VII** | Default deployment is **ethics-unaware** — `ENABLE_ETHICS_ENFORCEMENT` defaults to `false` per Issue #197 gradual-rollout intent | Ethics | Known design choice; not a defect. Worth documenting in BRIEFING when fuller briefing audit happens (queued). |
| **VIII** | `content_generator.py` lines 141-156 has explicit prompt-level placeholder instructions (`[SPECIFIC EXAMPLE NEEDED: ...]`) that surface incomplete information rather than fabricate. **Only this surface uses the pattern.** | Content gen | Worth generalizing as Phase 4 alignment item under [#1016](https://github.com/mediajunkie/piper-morgan-product/issues/1016) — candidate template for `document_handlers`, `issue_analyzer`, `conversational_floor` |

---

## Cross-cutting architectural insights

### Insight 1 (REFRAMED from batch 2): "Most LLM-touch surfaces have no boundary posture at all"

Batch 2 made the picture look like *each surface picks a posture and is internally consistent* (loose-at-boundary / tight-at-core). Batch 3 reveals: **most surfaces have no posture at all**. They call LLM, pass output through, and rely on the LLM behaving.

Concretely:
- 12 LLM-content surfaces inventoried; **only 1** (`content_generator.py`) has structured fallback + sanitization + length caps
- **Zero** apply BoundaryEnforcer to LLM **output** (only inputs)
- **Only `llm_classifier.py`** has multi-stage retry/regeneration (5-strategy fallback at lines 415-542); content surfaces don't retry on malformed output
- Orchestration's multi-step LLM workflows have **no schema validation between tasks**
- `conversational_floor` has elaborate prompt-level prohibitions but no post-generation enforcement

**The "looseness" wasn't a design choice; it was unreflective.** Each surface's developer made local decisions in isolation; no architectural principle was articulated to guide them.

This shifts the Phase 3 hypothesis for #1016. Original framing: *"trust at boundary, validate at dispatch, safe-fallback to floor."* That was an idealized reading of intent classification. The reality across surfaces is that **most don't have any of these three elements**. Phase 3 has to address what *should* be there (post-generation safety filter, audit signals, length caps, fallback patterns) rather than just classifying what is.

The good news: the principle, once articulated, is straightforwardly applicable — most surfaces just need the three elements added in some form. The work is mechanical, not architecturally fraught. The **#1016 epic Phase 4 alignment** is the place to do it.

### Insight 2: The default deployment posture is structurally weaker than Phase F discussion implied

The Phase F (#992) DO NOT AUTHORIZE recommendation was made on the basis of #1002 + #1003 detection-brittleness on inputs. Today's review surfaces three additional structural facts:

1. **`ENABLE_ETHICS_ENFORCEMENT` defaults to `false`** (Finding VII) — default deployment skips even the input check
2. **No LLM-output filter** (Finding I) — even when input enforcement is on, LLM-generated content is unfiltered
3. **No durable audit log** (Finding II) — even when both layers fire, the operator-visible record evaporates on restart

The combination means: **the default deployment has no input enforcement, no output filtering, and no durable audit trail.** Even if Fix B (#1004) ships and works perfectly, #1017 + #1018 are required complements before the system can credibly claim "ethics enforcement" to users or operators. Phase F's hold is more justified than I'd realized; the work isn't just #1002/#1003 closure but a layered set of structural prerequisites.

**This isn't an alarm; it's a structural observation.** None of these are user-affecting today (alpha cohort is small; no public claims of compliance have been made). The risk window is the period between "we say ethics enforcement is active" and "all three layers actually work." Sequencing #1017 + #1018 alongside #1004 closure manages that window.

### Insight 3: One "good design hidden in plain sight" — `BoundaryEnforcer`'s `redirect_context` (#992 Phase A)

While the substring detector is brittle, the `redirect_context` design pattern in `boundary_enforcer_refactored.py:343-380` is a sophisticated piece of architecture worth surfacing as the **template** for what an LLM-touch boundary should look like at output:

- **Audit-safe by construction**: category-only mapping; never user content or matched patterns
- **Structured handoff between layers**: enforcement layer produces a small typed value; voice layer consumes it
- **No raw content leak across boundaries**: the enforcement layer's matched patterns never reach the voice layer

This is the "enforcer detects, Piper speaks" Apr 16 design principle made concrete. It's the model for what #1017's output-filter handoff should look like, what #1004's semantic detector audit envelope already follows, and what other LLM-touch boundaries should converge toward.

**Worth elevating in the #1016 Phase 3 principle articulation as the canonical reference instance.**

### Insight 4: One safety pattern worth generalizing — placeholder instructions (`content_generator.py:141-156`)

`content_generator.py` instructs the LLM to emit structured placeholders (`[SPECIFIC EXAMPLE NEEDED: ...]`, `[FACT CHECK: ...]`) when information is missing, rather than fabricate. Only this one surface uses the pattern. It's a leading-practice safety move that mitigates LLM hallucination at the prompt level — distinct from post-generation filtering (#1017).

Candidate Phase 4 alignment item under #1016: generalize to `document_handlers`, `issue_analyzer`, `conversational_floor`. Each surface where the LLM might otherwise invent specifics gets the placeholder discipline.

---

## #1016 Phase 1 progress

The LLM-touch boundary principle epic #1016 has Phase 1 as "survey every LLM-touch surface in the codebase." Batch 2 + batch 3 together cover the major surfaces; remaining surfaces (memory layer PDR-002 territory, plugin system, learning layer) are still queued for subsequent batches.

**Surfaces characterized so far** (Phase 1 progress):

| Surface | Posture summary | Boundary characterization complete? |
|---|---|---|
| Intent classification (`prompts.py`, `pre_classifier.py`, `classifier.py`) | Loose boundary (free-form `action: str`); tight core (34-pair registry); safe-fallback (FLOOR) | ✅ batch 2 |
| LLM provider abstraction (`services/llm/`) | Loose boundary (per-call provider selection); tight core (tier mapping); fallback (Anthropic→Gemini→OpenAI) | ✅ batch 2 |
| Web layer Pattern-007 (degradation) | Loose boundary (200-OK with error); intent-only | ✅ batch 2 |
| BoundaryEnforcer (input substring detector) | Rigid boundary (substring); no semantic core; **no safe-fallback** | ✅ batch 2 (#1002 + #1003) |
| BoundaryEnforcer (post-#1004 semantic detector) | Loose boundary (semantic LLM); tight core (5 categories + audit envelope); safe-fallback (floor) | ✅ batch 2 (in flight) |
| BoundaryEnforcer redirect_context (#992 Phase A) | Audit-safe handoff template (worth elevating) | ✅ batch 3 |
| `adaptive_boundaries` | Inert scaffolding; no posture | ✅ batch 3 |
| `audit_transparency` | Logging-only, ephemeral | ✅ batch 3 |
| `document_handlers` (Q&A, comparison, synthesis) | **No posture** — input truncation only; LLM output passes through | ✅ batch 3 |
| `content_generator` (GitHub issue gen) | Structured fallback + sanitization + length caps (the **leading example**) | ✅ batch 3 |
| `conversational_floor` | Elaborate prompt-level prohibitions; no post-generation enforcement | ✅ batch 3 |
| `issue_analyzer` | No posture | ✅ batch 3 |
| `knowledge_graph` ingestion | Light JSON parse; no fallback documented | ✅ batch 3 |
| `project_context` inference | String match + hard-fail on unknown | ✅ batch 3 |
| `llm_classifier` (LLM fallback classifier) | **5-strategy retry** (only surface with this) | ✅ batch 3 |
| `slot_extractor` | Graceful empty-dict fallback | ✅ batch 3 |
| `work_item_extractor` | Fallback to text-based WorkItem | ✅ batch 3 |
| Orchestration tasks (`engine.py`) | **No per-task validation** — output assumed valid | ✅ batch 3 |
| Memory layer (`services/memory/`) | TBD | ⏳ next batch |
| Plugin system (`services/plugins/`) | TBD | ⏳ next batch |
| Learning layer (`services/learning/`) | TBD | ⏳ next batch |
| Database/repositories (PII placeholder threads) | TBD | ⏳ next batch |

Phase 1 is ~75% complete. Remaining surfaces likely produce additional findings but are unlikely to materially change the reframed hypothesis. **Phase 1 should close in 1-2 more batches.** Then Phase 2 analysis (matrix of postures), Phase 3 principle articulation, Phase 4 alignment plan, Phase 5 documentation.

---

## Forward-looking items — issues filed (cumulative across batches 2 + 3)

| Issue | Title | Covers | Priority | Batch |
|---|---|---|---|---|
| [#1010](https://github.com/mediajunkie/piper-morgan-product/issues/1010) | ARCH-CLEANUP: Refactor knowledge_graph_service.py to domain layer; remove legacy boundary_enforcer.py | Apr 27 morning observation | P3 | (pre-batch-2) |
| [#1011](https://github.com/mediajunkie/piper-morgan-product/issues/1011) | ARCH-DESIGN: Slash-command dispatch precedence — post-MVP design decision | Apr 27 morning observation | (post-MVP) | (pre-batch-2) |
| [#1012](https://github.com/mediajunkie/piper-morgan-product/issues/1012) | ARCH-CLEANUP: Small dead-code sweep | Findings B, C, D, F, G + VI | P3 | 2 |
| [#1013](https://github.com/mediajunkie/piper-morgan-product/issues/1013) | ARCH-CLEANUP: /auth and /setup route prefixes violate /api/v1/ convention | Finding A | P2 | 2 |
| [#1014](https://github.com/mediajunkie/piper-morgan-product/issues/1014) | ARCH-CLEANUP: AuthMiddleware exclude_paths refactor | Finding E | P3 | 2 |
| [#1015](https://github.com/mediajunkie/piper-morgan-product/issues/1015) | ARCH: Complete ADR-051 RequestContext migration (epic) | Finding H | P2 | 2 |
| [#1016](https://github.com/mediajunkie/piper-morgan-product/issues/1016) | ARCH-DESIGN: LLM-touch boundary principle (epic) | Cross-cutting Insight 1 | P1 | 2 (Phase 1 in flight via batches 2+3) |
| **[#1017](https://github.com/mediajunkie/piper-morgan-product/issues/1017)** | ARCH-DESIGN: Post-generation content filter for LLM outputs (PII/safety) | Finding I | **P1** | 3 |
| **[#1018](https://github.com/mediajunkie/piper-morgan-product/issues/1018)** | ARCH-CLEANUP: Persist ethics audit log to durable storage | Finding II | **P1** | 3 |
| [#1019](https://github.com/mediajunkie/piper-morgan-product/issues/1019) | ARCH-CLEANUP: adaptive_boundaries scaffolding alive but inert — complete or remove | Findings III + V | P3 | 3 |
| [#1020](https://github.com/mediajunkie/piper-morgan-product/issues/1020) | ARCH-DESIGN: Per-task LLM output validation in OrchestrationEngine workflows | Finding IV | P3 | 3 |

**Total: 11 issues filed across 2 days of architectural review.**

---

## Subsequent batch surfaces (queued)

- **Memory layer** (`services/memory/` — PDR-002 territory)
- **Plugin system** (`services/plugins/`)
- **Learning layer** (`services/learning/`)
- **Database/repositories layer** (the PII placeholder threads from #1010)
- **Test infrastructure shape** (coverage map, gaps, structure)

PM has signaled "no rush; period of catching up; further review warranted" — pace will continue at 2-3 surfaces per session.

---

*Last Updated: 2026-04-27 (initial creation, batch 3 synthesis)*
