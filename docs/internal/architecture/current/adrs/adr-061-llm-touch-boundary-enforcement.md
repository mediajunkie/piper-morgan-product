# ADR-061: LLM-Touch Boundary Enforcement — Two-Layer Detection with Floor as De-Facto Ethics Layer

**Status**: Draft v1.0 (Lead Dev review applied; CXO + CIO review optional; PM ratification pending)
**Date**: 2026-04-28 (v0.1) → 2026-04-30 (v1.0 — Lead Dev fixes applied)
**Supersedes**: None (extends ADR-060 with a complementary boundary-enforcement architecture)
**Issues**: #1002 (the reframe), #1003 (the diagnostic), #1004 (the structural fix), #992 (ETHICS-ACTIVATE Phase A redirect_context), #1016 (LLM-touch boundary principle epic)
**Related**: ADR-060 (Floor-First Routing), Pattern-062 (Assembly Assumption), Pattern-064 (Extension Without Integration — companion)
**Deciders**: Chief Architect (drafted); Lead Developer + CXO + CIO + PM (review pending)

---

## Context and Problem Statement

The BoundaryEnforcer (#197 Phase 2A, refactored October 2025) was the project's first ethics-enforcement infrastructure. It was wired at the universal entry point of `IntentService._process_intent_internal` (`services/intent/intent_service.py:627`), upstream of the intent classifier. The architecture appeared correct: ethics gate runs before any other dispatch, populates an audit envelope on violation, and routes the request through the conversational floor for voice-appropriate decline ("the enforcer detects, Piper speaks" — #992 Phase A design principle).

In practice, when the gate was activated for testing during #992 Phase E (Apr 25, 2026), the audit envelope was empty for naturally-phrased harassment input. A diagnostic comparison run (#1003, Apr 26) confirmed: `ENABLE_ETHICS_ENFORCEMENT=true` and `=false` produced indistinguishable responses on the same input. The flag was observably inert.

### The Specific Failure

The BoundaryEnforcer's harassment detector is a substring matcher against ten literal trigger words (`"harass", "harassment", "bully", "bullying", "intimidate", "threaten", "inappropriate", "unwanted", "uncomfortable", "offensive"` — `services/ethics/boundary_enforcer_refactored.py:121-132`). Naturally-phrased harassment vectors do not contain any of these words. The detector returns `confidence: 0.0` and `violation_detected: False` for input that any reader would recognize as harassment.

Three additional findings sharpened the picture:
- **PROFESSIONAL category had accidentally-decent recall** because its pattern words (`"personal", "private", "relationship", "family"`) appear in normal speech (#1003 follow-up vector run, Apr 26)
- **PERSONAL and DATA_PRIVACY categories had zero recall** because no detection methods are called for those categories at all (#1004 contract review, Apr 26)
- **The conversational floor was already producing appropriate harassment redirects** via general LLM competence — empathetic acknowledgment, rejection of harmful framing, constructive alternatives (#1003 Phase E S1 r2 transcript, Apr 25)

### Initial Misframing and Reframe

PPM and Lead Developer initially framed the failure as a **routing problem** — *"pre-classifier keyword-match dispatch shadows ethics floor"*. Architectural verification (Apr 26 #1002 scoping) showed the gate was already at the universal entry point; the pre-classifier ran *inside* `classify_multiple` further downstream of the ethics gate at `services/intent/intent_service.py:631`. **The bypass was not routing-order; it was detection-effectiveness.** The substring detector ran but did not detect.

The reframe was load-bearing: a routing fix would have produced no observable behavior change. A detector fix is the actual work.

### Root Cause

The BoundaryEnforcer architecture treated **literal-pattern matching as the entire detection surface**. Anything outside the 10-30 trigger words across categories was invisible to the gate. The LLM — the thing that makes naturally-phrased input legible — was not consulted at the boundary.

This is a specific manifestation of **Pattern-064 (Extension Without Integration)** at the infrastructure layer: BoundaryEnforcer was extended to a universal entry point in #197 Phase 2D without ever being integrated with realistic input shape. The unit tests passed because they used inputs that quoted trigger words; the activation gate was wired; the audit envelope was structured. None of these elements caught the integration failure with naturally-phrased input.

It is also a specific manifestation of **Pattern-045 (Green Tests, Red User) at the infrastructure layer**: tests passed, gate activated, audit envelope populated correctly when triggered — and yet user-facing behavior was unchanged because the detector was too narrow to fire on the input shape it was purportedly detecting.

---

## Decision

### Principle

**At LLM-touch boundaries, four elements must be present at every surface where LLM output is consumed or natural-language input is evaluated:**

1. **Permissive input shape** — boundary validation does not constrain input to enums or rigid patterns. Natural-language input is naturally fuzzy; rigid validation cannot encode open-domain semantics.
2. **Schema validation at consumption** — at the point of consumption, parse and validate against a structured contract. On failure, structured fallback (not silent pass-through).
3. **Safe-fallback path** — when validation fails, a known path runs. For natural-language input: the floor LLM's general competence. For LLM output: redaction, canned response, or retry-with-stricter-prompt.
4. **Audit envelope** — every LLM-touch event records (which surface, raw output size, validation result, action taken) for operator legibility.

The substring detector pre-#1004 was the inversion of this principle: rigid pattern matching at the boundary (1), no semantic schema (2), no architected safe-fallback (3 — though the floor was *implicitly* doing the work, the architecture didn't acknowledge it), and audit envelope that was empty when the detector failed silently (4).

### Architecture: Two-Layer Detector + Floor Backstop

```
User message
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Literal-trigger fast-path (current substring impl) │
│   - Cheap, deterministic, fast (~10ms when hit)             │
│   - Catches obvious cases that quote literal trigger words  │
│   - audit_data.detector = "literal-trigger"                 │
│   - audit_data.fast_path_hit = True                         │
└────────────┬────────────────────────────────────────────────┘
             │ no fast-path hit
             │ audit_data.fast_path_hit = False (recorded for
             │ calibration-window observability)
             ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Semantic LLM detector (#1004 Fix B)                │
│   - Structured JSON output (Pydantic-validated)             │
│   - confidence-tiered: 0.85+ block / 0.6–0.85 ambiguous /   │
│     <0.6 pass                                               │
│   - LRU cache (1024 entries); audit_data.cache_hit records  │
│   - audit_data.detector = "semantic" (when violation found) │
│                          = "none" (when no violation found) │
└────────────┬────────────────────────────────────────────────┘
             │ violation_detected (either layer)
             ▼ (existing path, unchanged from #992 Phase C)
       Floor LLM (denial_mode=True, redirect_context hint)
       composes decline voice
             │
             │ no violation detected (either layer);
             │ audit_data.detector = "none"
             ▼
       Floor LLM (denial_mode=False, normal context)
       general competence handles the request — including
       implicit ethics work for input shapes the detectors miss
       (FLOOR_IMPLICIT_ETHICS Phase 2 telemetry case)
```

The floor LLM is the **de-facto ethics layer for natural-language input** that doesn't trip either detector. This was already true pre-#1004 (the #1003 evidence showed the floor handling harassment vectors competently). The architecture now *acknowledges* this rather than treating the floor as accidental backstop.

### Audit Envelope (Fix C1)

`BoundaryDecision.audit_data` gains six new fields:

```python
audit_data = {
    # ... existing fields ...
    "detector": "literal-trigger" | "semantic" | "none",  # which path fired
    "decision_tier": "block" | "ambiguous" | "pass",
    "semantic_confidence": float | None,  # semantic path only
    "semantic_reasoning": str | None,  # audit-only; never user-routed
    "fast_path_hit": bool,  # whether literal-trigger fast-path matched first
    "cache_hit": bool,  # whether semantic detector result came from LRU cache
    # ... rest of existing fields ...
}
```

The `detector: "none"` value is load-bearing: it distinguishes "neither layer fired; floor is handling implicitly" from "Layer 1 fired" and "Layer 2 fired." This is what makes the FLOOR_IMPLICIT_ETHICS case (Telemetry Phase 2 sibling concern) operator-detectable.

`fast_path_hit` and `cache_hit` are operator-distinguishable signals worth documenting separately from `detector`:
- `fast_path_hit`: even when `detector == "semantic"`, knowing whether the fast-path was *checked first* is informative — feeds the calibration-window enhancement (`semantic-runs-alongside-literal-trigger` log-only disagreement detection in §"Neutral / Open" below)
- `cache_hit`: relevant to latency/cost observability and cache-warming patterns

Three operator-distinguishable cases:
1. **BoundaryEnforcer fired (literal-trigger or semantic)** — `detector` field is `"literal-trigger"` or `"semantic"`; audit envelope present
2. **Floor handled with `denial_mode=True`** — semantic detector caught it, floor performed the decline (case 1 with `denial_mode=True` downstream)
3. **Floor handled with `denial_mode=False` but ethics-shaped behavior** — `detector == "none"`; implicit ethics work; FLOOR_IMPLICIT_ETHICS counter (Telemetry Phase 2) records via structural heuristic `category=="unknown" AND floor_hit==true`

### The redirect_context Handoff (#992 Phase A)

The `redirect_context` field on `BoundaryDecision` (declared at `boundary_enforcer_refactored.py:81-88`; computed via `_derive_redirect_context()` and `_compute_redirect_context()` helpers; consumed at the floor handoff site) is the **canonical reference instance** for structured layer-to-layer handoff in this architecture:

- **Audit-safe by construction**: category-only mapping; never user content or matched patterns
- **Structured handoff between layers**: enforcement layer produces a small typed value; voice layer consumes it
- **No raw content leak across boundaries**: matched patterns never reach the voice layer

This is the model for any future LLM-touch boundary handoff: enforcement and voice are separate concerns with a typed contract between them.

### What This ADR Does *Not* Establish

- **A claim that the architecture is complete.** The four-element principle applies to ~23 LLM-touch surfaces inventoried during #1016 Phase 1. Most have 0–2 of the four elements. Bringing them to 4 is incremental Phase 4 alignment work tracked under #1016, not in scope for this ADR.
- **A claim that the BoundaryEnforcer is now sufficient.** Sibling issues address the structural prerequisites: #1017 (post-generation content filter for LLM outputs), #1018 (durable audit log), #1019 (adaptive_boundaries scaffolding cleanup), #1020 (per-task LLM output validation in orchestration). #1004 + this ADR are necessary but not sufficient for a production-credible ethics-enforcement claim.
- **A statement that the floor is a *complete* ethics layer.** The floor is the *de-facto* ethics layer for naturally-phrased input — empirically capable, architecturally unacknowledged-until-now. Operator visibility into when the floor is doing implicit ethics work is a gap (FLOOR_IMPLICIT_ETHICS telemetry, sibling concern).

---

## Consequences

### Positive

- **The activation flag-flip becomes architecturally defensible.** The two-layer detector + audit envelope + floor-as-acknowledged-de-facto-layer means turning on `ENABLE_ETHICS_ENFORCEMENT` activates real coverage with operator legibility, not Pattern-045-shaped theater.
- **The four-element principle becomes citable.** Future LLM-touch surfaces (Phase 4 alignment work under #1016) have a named architectural reference. The principle is general; this ADR's two-layer detector is one specific application.
- **The floor's role is no longer accidental.** Acknowledging the floor as the de-facto ethics layer for naturally-phrased input clarifies that adding a more aggressive upstream filter would not improve coverage; the work is at the detector layer (#1017 for outputs) and the audit layer (#1018 for durability).

### Negative

- **The semantic detector adds an LLM call to every request that misses the literal-trigger fast-path.** Cost and latency impact (measured against probe-set v0.1 run-2, prompt v0.2 against Claude Sonnet 4 default tier, ~2000 prompt tokens × ~85 completion tokens, Apr 27): **~2-4 seconds added latency on uncached semantic-detector calls**. Specifically: p_min 2.1s / p_avg 3.2s / p_max 4.9s across 20 probes (`dev/2026/04/27/1004-probe-set-v0-1-run-2.md`). Plus per-call LLM inference cost. Mitigations: literal-trigger fast-path short-circuits at <10ms for inputs that quote trigger words (so observed p99 latency depends heavily on the fast-path hit rate in real traffic); LRU cache (1024 entries) mitigates repeated identical inputs; conservative fallback on detector failure (no false-positives from infrastructure failure).
- **The principle prescribes more work than is currently scoped.** 23 LLM-touch surfaces; most have 0-2 of four elements. Phase 4 alignment under #1016 spans multiple sprints. This ADR does not commit to a timeline for that work; it provides the framework for sequencing.
- **The "floor as de-facto ethics layer" framing depends on the floor LLM being a sufficiently capable model.** If model capability degrades (provider change, model regression, prompt drift), the implicit ethics coverage degrades silently. This is a real risk; mitigation is FLOOR_IMPLICIT_ETHICS telemetry (sibling concern) plus periodic review of floor responses against ethics-shaped probe set.

### Neutral / Open

- **The calibration-window enhancement** (semantic-runs-alongside-literal-trigger 7-14 days, log-only disagreement detection) is logged for post-flip implementation. Will produce data on whether literal-trigger fires on cases the semantic detector would also have caught (validation) or on cases the semantic detector would have passed (false-positive risk on PROFESSIONAL pattern words). This data informs whether to keep the literal-trigger fast-path long-term or eventually demote to semantic-only.
- **Pattern-063 (Parallel-Authoring Drift, CIO) and Pattern-064 (Extension Without Integration, this ADR's grounding sub-pattern) are sibling sub-patterns of Pattern-062 (Assembly Assumption).** Both arise in this work cluster; both will reference each other and Pattern-062 in their formalization.

---

## Implementation Notes

The implementation shipped in #1004 (commit `b26d6c85`, Apr 27, 2026):

- `services/ethics/semantic_boundary_detector.py` (310 LOC + 196-line v0.2 production prompt body)
- Two-layer dispatch in `services/ethics/boundary_enforcer_refactored.py`
- Telemetry Phase 1 structured logging
- Probe set v0.1: **CXO authored the 20-probe content** (`dev/2026/04/27/1004-probe-set-v0-1.md`); **Lead Dev authored the test wiring** (typed `Probe` dataclass, runner, assertion harness at `tests/ethics/probe_set/probe_definitions.py` + `redirect_hint_assertions.py` + `probe_runner.py`). 18/20 PASS against production prompt v0.2 — CXO-confirmed ship criterion
- 112/112 tests passing post-merge

The activation flag (`ENABLE_ETHICS_ENFORCEMENT=true` in `docker-compose.yml`) is held pending PM/PA decision per Lead Developer's recommendation (Apr 27 memo `2322907a`). This ADR's ratification is the documented-coverage prerequisite the team has chosen to land before the flip.

---

## Related Patterns and Decisions

- **ADR-060 (Floor-First Routing)**: adjacent decision. ADR-060 establishes the floor as the default response path for natural-language input. ADR-061 acknowledges that this same floor competence is the de-facto ethics layer for naturally-phrased input. The two ADRs are complementary: ADR-060 says "the floor handles the user's request"; ADR-061 says "and that handling includes the implicit ethics work."

- **Pattern-062 (Assembly Assumption)**: parent pattern. The substring-detector failure is a specific composition failure where the components (substring matcher, audit envelope, activation flag, unit tests) each work in isolation but the assembly is incomplete in a way no individual test surfaced.

- **Pattern-064 (Extension Without Integration)**: companion sub-pattern of Pattern-062, formalized alongside this ADR. Names the specific failure mode the BoundaryEnforcer #197 manifested: extension to a universal entry point without integration testing against realistic input shape.

- **Pattern-045 (Green Tests, Red User) at infrastructure layer**: this ADR captures a specific application — infrastructure tests that pass with literal trigger words; activation gate exists; audit envelope wired; user-facing behavior unchanged because the detector is too narrow to catch realistic input shape.

---

## Review and Ratification

**v0.1** drafted by Chief Architect 2026-04-28; distributed to Lead Dev / CXO / CIO for review.

**v1.0** updated 2026-04-30 with Lead Dev review feedback applied:
- Detector discriminator updated to three-way (`literal-trigger` / `semantic` / `none`); §"Architecture" diagram and §"Audit Envelope" schema both updated
- Audit envelope schema extended with `fast_path_hit` and `cache_hit` fields (six total new fields, was four)
- Latency claim refined from pre-implementation estimate (~150-300ms) to measured numbers (~2-4s on uncached calls; p_min 2.1s / p_avg 3.2s / p_max 4.9s per Apr 27 run-2)
- Line-number citations refreshed to current HEAD
- Probe-set authorship attributed (CXO authored content; Lead Dev authored wiring)

CXO and CIO reviews remain optional; their input on voice/experience framing and methodology framework respectively is welcome but not blocking ratification, given Lead Dev's substantive review is the implementation-accuracy gate. Either can submit feedback for a v1.x revision.

**PM ratification pending**. Once ratified, this ADR is the documented-coverage prerequisite for the Phase F flag-flip per Lead Developer's Apr 27 recommendation.
