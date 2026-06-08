# ADR-060: Floor-First Routing Architecture

**Status**: Approved
**Date**: 2026-03-19
**Supersedes**: ADR-039 routing philosophy (ADR-039 infrastructure retained)
**Issues**: #911 (floor inversion), #922 (conversation continuity bug)
**Deciders**: PM, Chief Architect, PPM, CXO, CIO (roundtable consensus, 2026-03-14)

---

## Context and Problem Statement

Piper Morgan's intent routing architecture (established in ADR-039, October 2025) used a dual-path system: canonical handlers for fast, deterministic responses (~1ms) and workflow handlers for complex, LLM-powered operations (2-3s). When a user's message didn't match any handler, the system returned a canned deflection: "I don't have that capability yet."

This architecture produced a paradoxical outcome: Piper Morgan — a sophisticated PM assistant with 19 intent categories, 62 patterns, entity models, trust gradients, and guided workflows — was **worse than a generic ChatGPT wrapper** for any request that fell outside its pre-built handlers.

A generic wrapper with a one-line system prompt ("You are a helpful PM assistant") would engage conversationally with any PM question. Piper refused to try.

### The Specific Failure

During manual QA testing (March 2026), a user asked: "Can you help me manage the agents working on a coding assignment for me?" — a reasonable PM request. Piper responded: "I don't have that capability yet! Try asking 'What can you do?'"

Further testing revealed that most messages hitting canonical handlers received template boilerplate regardless of what the user actually asked. The handlers were designed for speed and determinism, not for conversational quality. The LLM — the thing that makes conversational AI conversational — was used to classify messages but never to respond to them.

### Root Cause

The ADR-039 architecture treated structured handlers as the **entire capability surface**. Anything outside handler boundaries was a dead end. The LLM was behind a classification gate, not available as a conversational floor.

```
ADR-039 Architecture:
Message → Classifier → [match?] → Handler (fast or workflow)
                     → [no match?] → "I can't do that" (DEAD END)
```

### Discovery Sequence

1. **March 14**: PM raised "Are we doing it backwards?" in a four-role roundtable
2. **March 14**: All four roles (Architect, PPM, CXO, CIO) independently diagnosed the same problem and proposed the same fix
3. **March 15**: Lead Dev investigation confirmed routing was inverted — handlers are default, floor is last resort
4. **March 15**: Phase 1 (GUIDANCE category) implemented and working
5. **March 16**: Full inversion architecture reviewed and approved by Architect, PPM, CXO
6. **March 19**: ADR-059 (Workflow Dispatcher) further simplifies the offer/acceptance pipeline

---

## Decision

### Principle

**Piper is always at least as good as a well-prompted LLM with the user's context. Structured handlers make it *better* than that, not *different* from that.**

The LLM conversational floor is the **default response path**. Structured handlers are **enhancements** that provide better experiences for specific capabilities (side effects, integrations, guided workflows). The user never hits a dead end.

### Architecture: Action Gate with Floor Default

```
Message → ProcessRegistry (guided process check)
       → Classifier → Action Gate
           ├── Side effect required? → Canonical/Workflow Handler
           ├── High-confidence deterministic? → Fast-path canonical (narrow)
           └── Everything else → Context Assembler → Conversational Floor
```

**Action Gate criterion**: "Does this intent require an operation the LLM cannot perform within the floor response?"

Three cases route to handlers:
1. **State mutations**: DB writes, API calls that change state (PORTFOLIO, EXECUTION)
2. **Multi-turn process initiation**: Onboarding, standup (ProcessRegistry activation)
3. **Deterministic fast-path**: Pure time queries, core identity name/role (~1ms, narrow exception)

Everything else — including GUIDANCE, DISCOVERY, TRUST, MEMORY, STATUS (read-only), PRIORITY, TEMPORAL (calendar), CONVERSATION (non-onboarding), UNKNOWN, and unhandled actions — routes to the conversational floor with assembled context.

### Context Assembler

Each intent category gets a `gather_context()` function that returns structured data for injection into the floor prompt:

- **IDENTITY** (all queries — see 2026-04-08 amendment below): Piper config, plugin capabilities
- **TEMPORAL (calendar)**: datetime, calendar summary
- **STATUS**: project list, GitHub metadata
- **PRIORITY**: priority list, high-priority issues
- **GUIDANCE**: calendar + projects + priorities
- **TRUST**: trust profile data
- **MEMORY**: conversation history
- **CONVERSATION**: conversation history, user preferences
- **QUERY (read-only)**: query-specific data
- **UNKNOWN**: conversation history only

Design principles for the assembler:
- **Declarative**: Returns structured data, not pre-formatted text
- **Fail-graceful**: Partial context on failure, not throw
- **Cached**: Per-type TTLs via Redis (project data 5min, conversation history per-request)

### Floor Voice

The floor responds as a PM colleague — engaging directly with what the user asked, using their project context, offering concrete actions Piper can take. It never says "I can't do that." It never apologizes for missing features. It just helps.

When an action would require a capability Piper doesn't have, it suggests an alternative action it *can* take — naturally, without highlighting the limitation.

---

## Relationship to ADR-039

ADR-039 is **not revoked**. The infrastructure it established — pre-classifier, LLM classifier, canonical handler framework, workflow factory — remains in place and in use. What changes is the **routing philosophy**:

| Aspect | ADR-039 (Oct 2025) | ADR-060 (Mar 2026) |
|--------|--------------------|--------------------|
| Default path | Canonical handler | Conversational floor |
| LLM role | Classification only | Classification + response generation |
| Unmatched queries | Deflection | Floor with context |
| Handler purpose | Primary response mechanism | Enhancement for side effects |
| Floor | Last resort (UNKNOWN only) | Default for all read-only queries |

ADR-039's fast-path concept survives as the narrow deterministic exception in the Action Gate. ADR-039's workflow path survives for EXECUTION and other side-effect categories. The dual-path architecture becomes a **three-path** architecture: fast-path (narrow), action-path (side effects), floor-path (default).

---

## Consequences

### Positive
- Piper is never worse than a context-aware LLM for any PM question
- Classifier misroutes for read-only categories are non-catastrophic (floor handles them)
- User first impression is "capable colleague," not "limited tool"
- Learning signal: what queries hit the floor shows what structured handlers to build next
- Canonical test pass rate projected to reach ~90%+ from routing alone (without classifier fixes)

### Negative
- Latency increase for queries that were previously canonical (~1ms → ~2-3s for LLM response)
- LLM cost increase (response generation in addition to classification)
- Response quality inconsistency (LLM responses vary; templates were predictable)
- ~126 existing canonical handler tests need migration/updating

### Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Latency regression for simple queries | Narrow fast-path exception for truly deterministic responses |
| LLM cost at scale | Cache context assembly, single model for now with split-ready abstraction |
| Floor quality inconsistency | Sample-based human review at alpha, Colleague Test rubric |
| Context assembler misses data | Incremental migration, fail-graceful design |
| Action triggers lost in floor routing | Action Gate checks before routing, not after |
| Floor prompt parroting | Directive prompt style ("respond directly") not descriptive ("I'm here to help") |

---

## Migration Path

1. **Phase 1** ✅ (complete Mar 2026): GUIDANCE → floor with context
2. **Phase 2** ✅ (complete Apr 8, 2026): IDENTITY (all queries), DISCOVERY, TRUST, MEMORY
3. **Phase 3** 🟡 (in progress, #925): STATUS, PRIORITY, TEMPORAL (calendar) — partial; STATUS/PRIORITY still canonical
4. **Phase 4** 🟡 (in progress): CONVERSATION (keep greeting/onboarding triggers, floor the rest)
5. **Phase 5** ⏳ (pending M2): Remove `_GENERIC_CANONICAL_SIGNATURES` (confirms inversion complete)

---

## 2026-04-08 Amendment — IDENTITY Full Migration

**Decision**: All IDENTITY queries route to floor. The previous "core IDENTITY canonical / adjacent IDENTITY floor" distinction is retired.

**Rationale**: M1 Gate UAT Round 2 (Apr 7) showed the canned "I'm Piper Morgan..." identity template scoring 1/3 on the Colleague Test. Direct floor testing of the same query scored 7+. The case for keeping core IDENTITY canonical (consistency, fast-path latency) was outweighed by the quality gap.

**Code change**: `services/intent/intent_service.py` `_requires_canonical_handler()` now returns `False` for category `"IDENTITY"` unconditionally. The `_is_adjacent_identity()` method is dead and the corresponding `_handle_identity_*` methods in `canonical_handlers.py` are unreachable in production.

**Commit**: 33e6758a (PM-approved Apr 8, verified in Gate UAT Round 4 Apr 8 with 7/9 PASS).

---

## 2026-04-09 Amendment — Conversation Continuity Foundation (#922 partial)

**Decision**: Add `response` field to `ConversationTurn` and backfill it after each successful processing.

**Rationale**: The floor was reading conversation history from `conv_context.turns`, but the in-memory `ConversationTurn` had no `response` field. The floor was getting only the user's previous messages, never Piper's replies — losing the half of the conversation needed for continuity. This was the underlying cause of the "OK" affirmation failure mode (#922).

**Code change**:
- `services/intent_service/conversation_context.py` — added `response: Optional[str] = None` field to `ConversationTurn`
- `services/intent/intent_service.py` — `process_intent()` now writes `result.message` to the latest turn's `response` field after successful processing

**Status**: Partial fix. The data plumbing is correct but the floor LLM still struggles with single-word inputs in some edge cases. Tracked as #922 carried into M2.

**Commit**: 25437f95.

---

## 2026-04-11 Amendment — Floor Fabrication Guardrails (#960)

**Decision**: Add a hard prohibition in the floor system prompt against inventing user data when the context block is empty or missing that data.

**Rationale**: M1 Gate UAT Round 5 (Apr 11) discovered that when "list todos" fell to the floor without canonical handler context (because of a pre-classifier pattern miss), the LLM hallucinated nine fancy fabricated todos with PM-style descriptions. None existed in the database. This is worse than "I don't have that data" because it looks authoritative.

**Code change**: `services/intent_service/conversational_floor.py` system prompt addendum now includes:
- "Do NOT invent or list todos, projects, issues, tasks, calendar events, meetings, or any other user-specific data unless that data is EXPLICITLY present in the [Available context] block in the user prompt"
- "If the user asks about their data and the context block is empty or missing that data, say so directly: 'I don't see any todos in your list right now' or 'I don't have access to your calendar in this conversation'"
- "Never invent project names, repository names, issue numbers, todo descriptions, or any user-specific entities. Only reference what is explicitly given to you"

**Companion fix**: Pre-classifier pattern updated to match "list todos" / "show todos" without requiring "my" — closes the immediate route. Commit: 063edf52.

**Status**: Immediate guardrail in place. Deeper architectural fix (context contract enforcement) tracked as #960 and #961 (route audit) for M2.

**Commit**: 4789de64.

---

## 2026-06-06 Amendment — Verb + Source-Slot Action Canonicalization (#1158)

**Status**: **Approved (Architect, 2026-06-06).** Architectural shape ruled by Architect in the #1158 consult reply (2026-06-06); ratified via `mailboxes/lead/read/memo-arch-to-lead-cc-ppm-cxo-pm-pa-1124-adr-060-amendment-ratified-layer-then-migrate-2026-06-06.md`. The open supersede-vs-layer question is resolved as **layer-then-migrate** (see Architect resolution below). Phase 2 + Phase 3 are GO; Phase 4 retains the canonical-retest gate.

**Decision**: Separate the two dimensions the LLM-classifier collapses into one improvised name (e.g. `summarize_github_issue`):
- **Action = a small, stable, typed enum of VERBS** (`summarize`, `update_document`, `comment_issue`, `meeting_time`, …) — Pattern-072-disciplined (typed enum + documented consumers + register-time validation). 6th Pattern-072 application.
- **Source = a separate `source_type` slot** (`github_issue | text | commit_range | …`) the classifier populates; handlers read it from `intent.slots`, **not** from `intent.action`.

Enforced at two layers (per ADR-061 LLM-touch four-element principle):
1. **Prompt-level** — classifier prompt enumerates allowed verbs + asks the LLM to populate `source_type`. Reduces miss rate.
2. **Boundary-level** — the action-dispatch rail (#1124) validates `intent.action ∈ ActionEnum` at consumption; **unknown verb → floor** (this ADR's floor-default; not a hard error). Catches what slips through.

**Rationale**: The classifier's "improvisation" is the LLM correctly recognizing intent + source and expressing them as one name. Chasing enumerated full-names is whack-a-mole (#1158 found `summarize_github_issue`, `add_comment_to_issue`, `prioritize_tasks` — none registered). Separating verb from source restores the closed dispatch surface the rail needs without losing the LLM's source-recognition value. Grounded in Pattern-072, ADR-061, this ADR (floor-first safe-fallback), and methodology-30 (consumer-trace: the rail must be able to evaluate the verb the classifier asserts).

**Reconciliation with existing `services/intent_service/action_registry.py` (#915/#916/#919)** — investigation 2026-06-06 found this is NOT greenfield:
- `ACTION_REGISTRY: dict[(category, action) → ActionDisposition]` already enumerates the **pre-classifier** vocabulary (closed set; that's why pre-classifier actions like `changes_query` are stable). `get_disposition()` already defaults unknown → `FLOOR` — i.e. **the boundary safe-fallback (layer 2) substantially already exists** for the disposition layer, and improvised LLM actions already floor today.
- The gap is the **LLM-classifier path** (the fallback when the pre-classifier misses): it is NOT constrained to the registered vocabulary, so it improvises.
- Therefore canonicalization **builds on** the existing registry rather than replacing it: (a) introduce the typed verb enum as the source of truth the registry/rail validate against; (b) constrain the LLM-classifier prompt to emit a registered verb + `source_type`; (c) keep `get_disposition`'s floor-default as the safety net. This supersede-vs-layer question is **resolved as layer-then-migrate** (Architect, 2026-06-06) — see the Architect resolution below.

**Architect resolution (2026-06-06): layer-then-migrate.** Neither pure supersede (greenfield rewrite of `action_registry.py` — discards the working disposition + floor-default code, high blast radius) nor pure layer (two parallel registries forever → drift, a Pattern-073 candidate). Instead, three roles separate cleanly:
1. **VERB enum** — the closed verb vocabulary the classifier emits; the source of truth for the verb dimension (Pattern-072, 6th application).
2. **`source_type` slot** — the source dimension (`github_issue | text | commit_range | …`) the classifier populates in `intent.slots`.
3. **Registry `(category, action) → ActionDisposition`** — the disposition layer (given a recognized verb [+ optional source], which handler dispatches). Its keys *reference* the VERB enum; they are not the verb source of truth.

The existing `_query`-suffixed keys (the frozen verb-object collapse) keep working. Key shape evolves to `(category, VERB)` or — where source distinguishes dispatch — `(category, VERB, source_type)` (a 2-or-3-tuple discriminated on whether source matters). Migration is owner-paced, no flag day: Phase 2 adds the VERB enum + `validate_verb_coverage()` (additive, no key changes); Phase 3 boundary-validates `intent.action` is a registered VERB (lookup walks `VERB → (category, VERB)` or `VERB + source_type → (category, VERB, source_type)`); Phase 4 (canonical-retest-gated) stops the classifier creating new `_query` keys; **post-#1124** progressively retires legacy `_query` keys one discrete commit at a time (backward-compat via parallel keys → same disposition). Full ruling: `mailboxes/lead/read/memo-arch-to-lead-cc-ppm-cxo-pm-pa-1124-adr-060-amendment-ratified-layer-then-migrate-2026-06-06.md`.

**Implementation phases** (PM-approved 2026-06-06, gated/sequenced):
1. This ADR amendment (decision record). ← *here*
2. `ActionEnum` typed verb enum + register-time validation (Pattern-072). *Low-risk, additive.* **[Shipped 2026-06-07.]**
3. **(Refined 2026-06-07)** Boundary validation = validation + observability only. The boundary computes `get_verb(intent.action)` and emits telemetry on `None` results (unregistered actions). **Routing is unchanged in Phase 3.** The telemetry stream IS the canonicalization-backlog signal — load-bearing for Phase 4 (work list + canonical-retest evaluability), not just instrumentation. Spec telemetry shape with Phase 4 consumption in mind (clear `action`, `category`, frequency, sample-context). *Low-risk, instrumental.*
4. Classifier-prompt canonicalization (verbs + `source_type`). ⚠️ **High blast radius** — gated behind a canonical-retest run (Run-12 baseline) before/after.
   - **Phase 4.x**: Enforce-floor (unknown verb → floor) lands as Phase 4 stabilizes — once the observability stream from Phase 3 confirms canonical-verb-only traffic, the verb vocab matches the live action set and enforcement is safe. (Separated from Phase 3 per the 2026-06-07 re-scope ruling below.)
5. Cohort #1124 migrations (`summarize`/`meeting_time`/`prioritize`) become mechanical: register a verb + read `source_type`. (`comment_issue`/close/reopen retain the separate multi-turn-confirmation prerequisite.)

### 2026-06-07 Phase 3 re-scope refinement (Architect, in response to Lead Dev coverage finding)

Lead Dev applied methodology-30 consumer-trace PRE-implementation and found that enforce-floor in Phase 3 would false-floor ~40+ valid actions handled by the category-routing elif chains in `intent_service.py` (`search_documents`, `summarize`, `prioritize`, `stale_prs`, `review_issue`, `analyze_commits`, etc.) — actions that are NOT in the post-Phase-2 verb vocab because they are exactly the alias/verb-object sprawl Phase 4 retires. Mapping them to verbs now is wrong-direction work Phase 4 undoes.

**Ruling**: Phase 3 refined to validation + observability only (above). Enforce-floor folds into / follows Phase 4 (separated as Phase 4.x above). The architecture shape is unchanged; only the phase boundary moved. The two alternatives Lead Dev offered (Phase 3.5 expand-vocab-to-cover-category-actions; enforce narrowly to workflow rail only) were ruled out: the first perpetuates the sprawl; the second is a no-op disguised as enforcement (`WORKFLOW_REGISTRY` is currently empty).

**Pattern-073 spec-layer signal**: my original Phase 3 description ("formalizes the existing floor-default at the verb layer") assumed the verb vocab covered the live action set. It didn't. This is documentation-asserted-behavior-vs-actual-behavior at the SPEC layer (vs. the 9+ runtime instances cataloged under Pattern-073). methodology-30 pre-implementation consumer-trace is the right defense. CIO catalog awareness flag queued for Day-7 findings memo (~Jun 13).

**Full ruling**: `mailboxes/lead/read/memo-arch-to-lead-cc-pm-ppm-cxo-pa-1124-phase3-rescope-approved-observability-as-backlog-signal-2026-06-07.md` (or wherever recipient triages).

### 2026-06-07 Phase 4 plan ratification (Architect, in response to Lead Dev plan)

Lead Dev's Phase 4 plan (`docs/internal/architecture/current/phase-4-classifier-canonicalization-plan-1124.md`, PM-reviewed + approved 2026-06-07) asked two architectural decisions; both **RATIFIED**:

**Q1 — `source_type` location → `intent.context` for Phase 4** (deviates from amendment's `intent.slots`): the working `_handle_summarize` precedent (`intent_service.py:8336`) already reads `intent.context.get("source_type")`. Phase 4 implements there for zero handler churn. **#1175 revisit path**: when slot-filling unification (`#1121` family) lands, `source_type` migrates to `intent.slots` as a discrete commit on the Phase 4 baseline. Same layer-then-migrate shape at a different altitude. Approved.

**Q2 — Hybrid transition** (big-bang prompt + shim-then-migrate consumers): classifier prompt is atomic by nature → big-bang gated by canonical-retest before merge. Consumers (6 behavior-driving + ~50 test assertions; cascade revealed `lens_inference.py` `ACTION_TO_LENS` that Phase 3 coverage missed) flip via `verb_sourcetype_to_legacy_action()` shim in `action_registry.py`; migrate consumers off legacy aliases one discrete commit at a time; retire shim last. Layer-then-migrate applied to the prompt-vs-consumers split. Approved.

**Same-shape decision count**: this is the 5th layer-then-migrate ruling in 48h (verb-enum-vs-registry 6/6 AM; Phase-3-folds-into-Phase-4 6/7 AM; ADR-065 D3 capability primitive; ADR-066 D1 capability map; Phase 4 prompt-vs-consumers split 6/7 PM). Pattern catalog candidate at Day-7: "layer-then-migrate as a recurring architectural primitive for retiring legacy shapes safely."

**Audit-cascade win**: Lead Dev's methodology-30 consumer-trace caught `lens_inference.py` `ACTION_TO_LENS` (~30 action keys → lens) — second methodology-30 pre-implementation win in 48h; Pattern-073 spec-layer extension reinforced (consumer-set-size spec-assumption pattern).

**Full ruling**: `mailboxes/lead/read/memo-arch-to-lead-cc-pm-ppm-cxo-pa-1124-phase4-plan-ratified-q1q2-2026-06-07.md` (or wherever recipient triages).

**What this doesn't change**: Cohort #1 (`update_document`) ships unchanged. Floor general-competence stays the post-canonicalization safe-fallback. Per-handler action verification remains the bridge until canonicalization lands.

**Cross-references**: #1158 (consult + Arch ruling), #1124 (cohort), Pattern-072, ADR-061, methodology-30. CIO: 6th Pattern-072 application (catalog awareness, non-gating).

---

## Implementation References

- Architecture investigation: `dev/2026/03/15/floor-inversion-architecture-report.md`
- PPM synthesis (binding guidance): `memo-ppm-floor-inversion-synthesis-2026-03-16.md`
- CXO voice guidance: incorporated in PPM synthesis, Section 3
- Architect review: `memo-arch-floor-inversion-review-2026-03-16.md`
- Roundtable memos (4): all dated 2026-03-14
- Phase 1 commit: `52e6cfcc`

---

## Review History

| Date | Reviewer | Decision |
|------|----------|----------|
| 2026-03-14 | PM, Architect, PPM, CXO, CIO | Unanimous roundtable consensus on principle and immediate action |
| 2026-03-16 | Architect, PPM, CXO | Detailed architecture review and voice guidance approved |
| 2026-03-19 | Chief Architect | ADR formalized |

---

*Chief Architect | March 19, 2026*
