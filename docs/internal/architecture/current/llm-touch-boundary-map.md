# LLM-Touch Boundary Map — #1016 Phase 2/4 Closing Document

**Status**: v0.1 (2026-05-28) — Phase 2 matrix + Phase 4 alignment status for epic #1016 (ARCH-DESIGN: LLM-touch boundary principle). Closes the Architect side of #1016; the epic closes when the last in-flight alignment (#1089 KG-privacy-filter) ships.
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
| `document_handlers` | ◐ | ❌ | ◐ | ◐ | ADR-061 (target) | Gap — schema validation + audit |
| `issue_analyzer` | ◐ | ❌ | ◐ | ❌ [P1] | ADR-061 (target) | Gap — 0-1/4 |
| `knowledge_graph/ingestion` | ◐ | ◐ | ◐ | ◐ [↑] | ADR-061 + #1089 | In-flight — KG-privacy-filter (#1089) adds storage-side audit |
| `project_context` | ◐ | ❌ | ✅ | ❌ [V 05-28] | ADR-061 (target) | Gap — verified: custom exceptions + default-project fallback (F upgraded ◐→✅); S+A absent |
| `llm_classifier` (intent) | ✅ | ✅ | ✅ | ◐ [P1] | ADR-061 + ACTION_REGISTRY | Aligned-ish — registry dispatch is deterministic; audit partial. **#1117 temporal-overgreedy is a Phase-4 alignment instance here.** |
| `slot_extractor` | ✅ | ◐ | ✅ | ❌ [V 05-28] | ADR-061 (target) | Gap — verified (`services/slot_filling/slot_extractor.py`): graceful empty-dict fallback (F upgraded ◐→✅) + dict-shape check (S partial, no Pydantic); `logger.warning` on parse-fail is operational not audit-envelope (A absent) |
| `work_item_extractor` | ◐ | ❌ | ◐ | ❌ [P1] | ADR-061 (target) | Gap |
| `text_analyzer` | ◐ | ❌ | ◐ | ❌ [P1] | ADR-061 (target) | Gap |
| `document_analyzer` | ◐ | ❌ | ◐ | ❌ [P1] | ADR-061 (target) | Gap |
| orchestration tasks (per-task LLM output) | ◐ | ❌ | ◐ | ❌ [P1] | ADR-061 (target); #1020 | Gap — #1020 tracks per-task validation |

### Input-shaping surfaces (5)

Phase 1 finding: input-side scores **2/4** structurally (P ✅ + F ✅; S ❌ + A ❌) — better-shaped than output-side because the floor-input pipeline had more architectural attention.

| Surface | P | S | F | A | Governing | Alignment |
|---|---|---|---|---|---|---|
| `context_assembler` | ✅ | ❌ | ✅ | ❌ [P1] | ADR-061 (target) | Partial 2/4 — needs schema contract (Pydantic) + audit ("what context assembled for this call") |
| `conversation_context` | ✅ | ❌ | ✅ | ❌ [P1] | ADR-061 (target) | Partial 2/4 |
| `lens_inference` | ✅ | ◐ | ✅ | ❌ [P1] | ADR-061 (target) | Partial |
| `personality_bridge` | ✅ | ❌ | ✅ | ❌ [P1] | ADR-061 (target) | Partial 2/4 |
| `warmth_calibration` | ✅ | ❌ | ✅ | ❌ [P1] | ADR-061 (target) | Partial 2/4 |

### Memory surfaces (5)

| Surface | P | S | F | A | Governing | Alignment |
|---|---|---|---|---|---|---|
| `conversational_memory` | ✅ | ◐ | ✅ | ❌ [P1] | ADR-054 + ADR-061 | Partial |
| `user_history` (Layer 3) | ✅ | ◐ | ✅ | ◐ [↑] | ADR-054 (#1021 active) | Partial — Layer 3 production-active; audit partial |
| `greeting_context` | ✅ | ◐ | ✅ | ❌ [P1] | ADR-054 | Partial — (alive-scaffolding per Pattern-064; was inert) |
| `conversation_summarizer` | ✅ | ❌ | ✅ | ❌ [P1] | ADR-054 + ADR-061 | Partial |
| `workspace_memory` | ✅ | ❌ | ✅ | ❌ [P1] | ADR-054 | Partial |

### Storage surface (1 — added since Phase 1)

| Surface | P | S | F | A | Governing | Alignment |
|---|---|---|---|---|---|---|
| KG-internal privacy filter | ✅ | ✅ | ✅ | ✅ [↑] | #1089 (PM-ratified ship-now May 20) | **In-flight → aligning** — Phase 0 + safety-net shipped; the third boundary layer (input/output/storage) |

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

- **2026-05-28** (Day-2 Fire 4): verified `slot_extractor` + `project_context` [V 05-28]. **Emerging finding: the [P1] output-side scores appear to UNDER-rate the safe-fallback element (F).** Both verified surfaces had clearer graceful-fallback than their [P1] ◐ suggested (slot_extractor: empty-dict-on-fail; project_context: default-project) — both upgraded ◐→✅ on F. This sharpens the dominant-gap finding: **F is more widely present than the [P1] matrix shows; the real gap is almost entirely S (schema-at-consumption) + A (audit-envelope).** If this holds across more surfaces, Phase 4 narrows to "add Pydantic schema + audit signal" — the F element is largely already there. Remaining [P1] surfaces to verify: ~16 (continue 2-3/fire).

## #1016 close criteria

- [x] Phase 1 survey (Apr 27 — 23 surfaces)
- [x] Phase 3 principle (ADR-061 + v1.1 + ADR-063)
- [x] Phase 2 matrix (this document)
- [x] Phase 4 alignment status + sequencing (this document)
- [ ] Fresh per-surface verification of [P1] scores (bounded follow-up)
- [ ] #1089 ships (Lead Dev — the storage-layer alignment; in-flight)
- [ ] At least one Phase-4 gap-surface migrated as proof-of-concept (#1017 output filter already qualifies)

When the verification pass + #1089 ship land, #1016 closes. The principle is established (ADR-061/063); the alignment is sequenced; the remaining work is incremental per-surface migration tracked as individual issues.

## Cross-references

- #1016 epic + Phase 1 comments: https://github.com/mediajunkie/piper-morgan-product/issues/1016
- ADR-061 (the principle): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`
- ADR-063 (READ-side): `docs/internal/architecture/current/adrs/adr-063-user-facing-audit-envelope-read-surface.md`
- #1089 (storage-layer alignment, in-flight): KG-privacy-filter
- #1117 (llm_classifier Phase-4 instance): temporal-overgreedy → M3 with #1016
- Pattern-064 (alive scaffolding — greeting_context was an instance)
- methodology-30 (Consumer-Trace Verification — the discipline for the fresh-verification pass)

— Chief Architect, 2026-05-28 v0.1 (Phase 2/4 closing document for #1016)
