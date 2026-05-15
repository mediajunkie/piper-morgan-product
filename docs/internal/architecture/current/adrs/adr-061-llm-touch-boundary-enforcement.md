# ADR-061: LLM-Touch Boundary Enforcement — Two-Layer Detection with Floor as De-Facto Ethics Layer

**Status**: **Ratified** v1.0 (PM verbal ratification 2026-05-03); **v1.1 amendment 2026-05-15** (output-side companion shipped per #1017 — see §"Amendment 2026-05-15")
**Date**: 2026-04-28 (v0.1) → 2026-04-30 (v1.0 — Lead Dev fixes + CEO calibration reframe applied) → 2026-05-03 (verbally ratified) → 2026-05-04 (status block updated) → 2026-05-15 (v1.1 — output-side companion amendment per #1017)
**Supersedes**: None (extends ADR-060 with a complementary boundary-enforcement architecture)
**Issues**: #1002 (the reframe), #1003 (the diagnostic), #1004 (the structural fix), #992 (ETHICS-ACTIVATE Phase A redirect_context), #1016 (LLM-touch boundary principle epic), #1017 (output-side companion — v1.1 amendment)
**Related**: ADR-060 (Floor-First Routing), Pattern-062 (Assembly Assumption), Pattern-064 (Extension Without Integration — companion), Pattern-071 (Audit Logs as Attack Surface — emerging, sibling of Pattern-064; introduced by #1017 hash-only audit invariant), Pattern-072 (Registries that Grow into Architectural Shapes — emerging; the `task_type` registry was third-meaningful-reuse trigger via #1017's profile dispatch)
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
- `fast_path_hit`: even when `detector == "semantic"`, knowing whether the fast-path was *checked first* is informative — feeds the disagreement-table calibration analysis (Phase A simulation harness; Phase B beta-traffic refinement) detailed in §"Neutral / Open" below
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

- **Calibration timing — three-phase reframe** (CEO directive 2026-04-30, superseding the original "wait for calibration before flipping" framing). Original assumption: a 7-14 day window of real user traffic flowing through the detector, log-only disagreement detection produces the calibration signal. Catch-22 surfaced by CEO Apr 30: we are in alpha; we don't have users; calibration without users produces no signal regardless of flag state, and we cannot get to beta with calibration completed first because calibration requires the user volume that beta provides. Reframed as:
  - **Phase A — Simulation-first (alpha, ships with the flip).** Both detector layers (literal-trigger + semantic) run on every input. With `ENABLE_ETHICS_ENFORCEMENT=true`, the act-on-results path is live; both layer results logged for telemetry. A simulation harness drives both layers over a synthetic input population (Gemma generator tier produces naturally-phrased messages spanning boundary categories + category-adjacent legitimate work; ~hundreds to thousands of inputs) and produces a disagreement table. The signal isn't real user behavior, but it is *"what does the substring detector fire on that the semantic detector would have passed?"* — the original calibration question on a synthetic-but-relevant population. Surfaces obvious disagreement patterns (PROFESSIONAL false-positives, etc.) early.
  - **Phase B — Beta-traffic refinement (post-beta-cohort onboarding).** When real beta users arrive, the same telemetry that Phase A ships continues recording. After ~7-14 days of real traffic at beta scale, CXO scans the disagreement table and proposes prompt v0.3 (or "stable, no iteration" if the data supports it). This is the calibration round CXO described originally — deferred to when the population to calibrate against actually exists.
  - **Phase C — Stable (post-beta refinement landed).** Whatever falls out of Phase B becomes the production prompt. Substring detector retained as fast-path or demoted to semantic-only depending on the data.

  Implementation simplification: the original flag-off observation mode is not needed. Both layers always run unconditionally; the simulation harness in Phase A drives the inputs; the disagreement table is the calibration artifact at both phases.
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

## Amendment 2026-05-15 — Output-side companion (#1017 shipped)

ADR-061 v1.0 named "#1017 (post-generation content filter for LLM outputs)" as a sibling concern in §"What This ADR Does *Not* Establish" — explicitly out-of-scope for the input-side BoundaryEnforcer architecture. **#1017 shipped 2026-05-15** as a structural companion to this ADR. This amendment documents the companion architecture without revising the original v1.0 input-side decision.

### The four-element principle applied to OUTPUTS

ADR-061 v1.0's four-element principle was framed for input boundaries. The same four elements apply at output boundaries with one direction-swap:

1. **Permissive output shape** — the LLM emits free-form text; we cannot constrain the output at generation time without crippling the model's usefulness
2. **Schema validation at consumption** — at the moment the output is about to reach a user surface, parse and validate against per-task-type expectations. On detector match (PII regex / boundary category), structured fallback (redact-in-place / canned substitute), not silent pass-through
3. **Audit envelope at the boundary** — every filter decision writes a typed record (`OutputFilterDecision`) capturing the action class, severity, matched rules, hashes (never raw content) — see hash-only invariant below
4. **Structured handoff to caller** — `FilterResult.filtered_content` is the minimal caller-facing surface; the decision record stays in audit and never leaks raw PII back through the return path

### OutputFilter architecture

`services/ethics/output_filter.py` lands a decorator chokepoint at `LLMClient.complete()`. Every LLM call in production flows through it when an `OutputFilter` is wired (per `OutputFilterWiringPhase` in `web/startup.py`). Failure to wire = unfiltered LLM (graceful degradation by design — defense-in-depth layer must not block startup).

**Profile dispatch via `task_type`**: the existing `task_type` parameter (already required at every `LLMClient.complete()` call site) drives filter-profile selection. Ten production task types route to the `user_visible` profile (full Tier 1 + Tier 2 coverage); one task type (`intent_classification`) routes to `internal` (log-only; never echoed verbatim to users). Unknown task types default to `user_visible` (fail-closed).

**Three-tier detection**:
- **Tier 1 PII regex**: reuses `SecurityRedactor` patterns (email, SSN, 2 phone formats, credit card, digit-only phone) plus 5 added secret-format patterns (OpenAI `sk-`, GitHub `ghp_/gho_/ghu_/ghs_`, AWS `AKIA`, Bearer tokens, URL with embedded credentials)
- **Tier 2 BoundaryEnforcer category check on outputs**: reuses `BoundaryEnforcer.enforce_boundaries(content=output_text, ...)` — the same enforcer ADR-061 v1.0 specified for inputs, now also evaluating outputs
- **Tier 3 (deferred)**: hallucination grounding, length anomalies, cross-user leak detection — separate design pass when M3+ work surfaces them

**Severity → action matrix**:

| Detection | Severity | Action |
|---|---|---|
| PII regex (email/phone/SSN/credit-card) | medium | Redact in place → `[REDACTED]` |
| Secret formats (API keys, bearer tokens) | high | Redact + operator-flag |
| URL with embedded credentials | high | Redact entire URL |
| BoundaryEnforcer category violation | critical | Drop output + canned substitute |
| No match | — | Passthrough |

**Regenerate-on-violation**: when a boundary category fires, the decorator retries the LLM call once before surfacing the canned response (compresses user-visible failure rate; most LLM-output filter trips are non-deterministic). `attempt_number` + `prior_attempt_decision_id` propagate to the audit envelope for forensic chain visibility.

**Canned response** (CXO-ratified, output-side ownership phrasing): *"That came out wrong — let me try a different approach."* Cross-checked against CT v2.3 §Tone-0 cadence analysis; deliberately avoids the input-side BoundaryEnforcer's refusal framing because the output-side correction is a different psychological situation (Piper correcting her own output, not refusing the user's ask).

### Hash-only audit invariant (Pattern-064-adjacent / Pattern-071 candidate)

**The `OutputFilterDecision` dataclass stores hashes of content, never raw content.** Storing the content an audit log is intended to govern *as raw text* turns the audit log into the leak amplification surface — same skeletal shape as Pattern-064 ("alive scaffolding"), different failure mode (compliance-shaped infrastructure that actively makes the underlying problem worse). CIO filed as Emerging Pattern-071 ("Audit Logs as Attack Surface") 2026-05-15.

The invariant is enforced at two layers:
1. **Schema layer** — `OutputFilterDecision` has `original_content_hash` and `filtered_content_hash` (sha256 hex) but no field for raw content
2. **Write-time guard** — `log_output_filter_decision()` truncates any `audit_metadata` string >256 chars and flags `invariant_violations[]` so the audit-log layer catches future drift if a caller mutates audit_metadata with raw content

Forensic verification works via hash comparison: an operator with two events can confirm same-content-or-not without seeing either.

### Phase 3 verification (probe set)

`tests/ethics/test_output_filter_probe_set_1017.py` lands 25 parametrized tests:
- **11 PII probes** (one per detector path: email, SSN, 2 phone formats, credit card, digit-only phone, OpenAI key, GitHub token, AWS access key, Bearer token, URL credentials). Architect filed engineering coverage; CXO re-cast 6 for voice authenticity (Piper-PM-colleague voice, not CRM/IT-admin voice).
- **5 BoundaryEnforcer category probes** (HARASSMENT, PROFESSIONAL, PERSONAL, DATA_PRIVACY, INAPPROPRIATE_CONTENT). All drop + canned-substitute. CXO flagged `probe-boundary-personal-01` as most Piper-shaped (leverages memory-as-judgment failure mode).
- **7 false-positive controls** (must NOT trigger). Two flagged by CXO as exemplary Piper voice for future reference work.

Each probe asserts: action class, severity tier, matched rules, redactions count where applicable, hash-only invariant (raw PII/secret never appears in `decision.to_dict()`).

**CI gate**: `tests/` is covered by `.github/workflows/test.yml:136` (`pytest tests/ --tb=short -v -m "not llm"`), which picks up the probe-set file automatically. Regression = CI break.

**Phase 3 follow-ups deferred**: regenerate-cycle probes (attempt_number=2), multi-violation probes (PII + boundary in same output), voice-register failure mode tier (per CXO Q7 sequencing).

### Where the input-side and output-side architectures meet

ADR-061 v1.0 acknowledged the floor as the de-facto ethics layer for naturally-phrased inputs. The v1.1 amendment closes the loop on the output side: **the BoundaryEnforcer (the same component v1.0 hardened) now also evaluates outputs**, via the OutputFilter's Tier 2 wrapper. The principle stays: enforcement and voice are separate concerns with a typed contract between them. The contract for outputs is `OutputFilterDecision`; the voice handoff is the CXO-ratified canned response (or the redacted-but-passing content).

The combined surface coverage:
- **Inputs**: BoundaryEnforcer two-layer detector (literal-trigger fast-path + semantic), audit envelope to `ethics_audit_log`, floor as de-facto ethics layer for naturally-phrased input (v1.0)
- **Outputs**: OutputFilter at LLMClient.complete chokepoint, profile dispatch by task_type, Tier 1 PII + Tier 2 BoundaryEnforcer-on-outputs + Tier 3 deferred, hash-only audit envelope to `ethics_audit_log` via `log_output_filter_decision`, regenerate-on-violation flow (v1.1)

Together, both surfaces satisfy the four-element principle at the two boundaries where LLM content crosses a trust gate (user input → system; system output → user). The remaining LLM-touch surfaces inventoried in #1016 Phase 1 (~23 total at filing) gradually align under the same four-element discipline as Phase 4 work proceeds.

### What v1.1 does *not* establish

- **A claim that the OutputFilter is sufficient for all output-side failure modes.** Tier 3 (hallucination grounding, length anomalies, cross-user leakage) remains deferred. Voice-register failures (over-familiar, too clinical, mock-authoritative) are a separate Phase 3 v1.1 deliverable per CXO's Q7 framing.
- **A claim that the BoundaryEnforcer detector itself is more accurate when applied to outputs.** OutputFilter uses the same enforcer ADR-061 v1.0 hardened; calibration accuracy on output text is empirically distinct from accuracy on input text and may need its own probe-set evolution.
- **A retroactive change to v1.0's input-side decisions.** The semantic detector, two-layer dispatch, audit envelope schema, and floor-as-de-facto-ethics-layer framing all stand unchanged.

### Implementation evidence

- `services/ethics/output_filter.py` (342 LOC) — OutputFilter class + OutputFilterDecision schema + profile registry + canned response constant
- `services/ethics/output_filter_rules.py` (177 LOC) — apply_pii_rules / apply_secret_rules / apply_boundary_rules
- `services/ethics/audit_transparency.py` — `log_output_filter_decision()` sibling of `log_ethics_decision()`; per-call session_scope transaction-boundary (same #1018 Phase 2 invariant)
- `services/llm/clients.py` — decorator wrap of `complete()`; `set_output_filter()` method for startup wiring
- `web/startup.py` — `OutputFilterWiringPhase`; graceful-degradation on wiring failure
- `tests/ethics/test_output_filter.py` (35 tests) + `test_output_filter_audit.py` (5 tests) + `test_output_filter_probe_set_1017.py` (25 probe-set tests) + `tests/unit/services/llm/test_clients_output_filter.py` (11 decorator tests) + `tests/integration/services/test_output_filter_audit_integration.py` (4 integration tests against real Postgres) = **80 tests landed**
- Merged to main at `ba00185a` (Phase 2.1-2.5) + commit landing Phase 3 probe set
- #1017 issue + CXO/Architect ratification memos in `mailboxes/lead/read/`

---

## Related Patterns and Decisions

- **ADR-060 (Floor-First Routing)**: adjacent decision. ADR-060 establishes the floor as the default response path for natural-language input. ADR-061 acknowledges that this same floor competence is the de-facto ethics layer for naturally-phrased input. The two ADRs are complementary: ADR-060 says "the floor handles the user's request"; ADR-061 says "and that handling includes the implicit ethics work."

- **Pattern-062 (Assembly Assumption)**: parent pattern. The substring-detector failure is a specific composition failure where the components (substring matcher, audit envelope, activation flag, unit tests) each work in isolation but the assembly is incomplete in a way no individual test surfaced.

- **Pattern-064 (Extension Without Integration)**: companion sub-pattern of Pattern-062, formalized alongside this ADR. Names the specific failure mode the BoundaryEnforcer #197 manifested: extension to a universal entry point without integration testing against realistic input shape.

- **Pattern-045 (Green Tests, Red User) at infrastructure layer**: this ADR captures a specific application — infrastructure tests that pass with literal trigger words; activation gate exists; audit envelope wired; user-facing behavior unchanged because the detector is too narrow to catch realistic input shape.

---

## Review and Ratification

**v0.1** drafted by Chief Architect 2026-04-28; distributed to Lead Dev / CXO / CIO for review.

**v1.0** updated 2026-04-30 with Lead Dev review feedback applied + CEO Apr 30 calibration reframe:
- Detector discriminator updated to three-way (`literal-trigger` / `semantic` / `none`); §"Architecture" diagram and §"Audit Envelope" schema both updated
- Audit envelope schema extended with `fast_path_hit` and `cache_hit` fields (six total new fields, was four)
- Latency claim refined from pre-implementation estimate (~150-300ms) to measured numbers (~2-4s on uncached calls; p_min 2.1s / p_avg 3.2s / p_max 4.9s per Apr 27 run-2)
- Line-number citations refreshed to current HEAD
- Probe-set authorship attributed (CXO authored content; Lead Dev authored wiring)
- **Calibration timing reframed from "wait for 7-14 days of real traffic" to three-phase Simulation-first / Beta-traffic refinement / Stable** per CEO Apr 30 directive resolving the alpha catch-22 (no users in alpha → no calibration signal regardless of flag state). Reframe simplifies implementation (no flag-off observation mode needed; both layers always run; simulation harness in Phase A drives synthetic inputs)

CXO and CIO reviews remain optional; their input on voice/experience framing and methodology framework respectively is welcome but not blocking ratification, given Lead Dev's substantive review is the implementation-accuracy gate. Either can submit feedback for a v1.x revision.

**PM ratification pending**. Once ratified, this ADR is the documented-coverage prerequisite for the Phase F flag-flip per Lead Developer's Apr 27 recommendation.
