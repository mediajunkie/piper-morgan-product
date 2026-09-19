---
from: Architect (Chief Architect)
to: CEO (xian)
cc: Lead Developer, PPM (Principal Product Manager), CXO (Chief Experience Officer), CIO (Chief Innovation Officer), HOST (Head of Sapient Trust), exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-15
subject: e2e suite design — proposal for generalized simulation-harness pattern as project-scope architectural commitment
priority: normal — pre-trigger architectural design work; no deadline
response-requested: CEO ratification of the proposal direction; Lead Dev refinement on implementation feasibility; CXO refinement on probe-set scoping; CIO consideration of methodology shelf
relates-to: ADR-061 (LLM-touch boundary enforcement, three-phase calibration); workstream-042-arch May 4 "test-rigor assessment" + May 4 PM ratification of e2e-suite-design as architectural-session item alongside BYOC
---

# e2e suite design — pre-trigger architectural proposal

## Why this now

Per the May 4 test-rigor walkthrough conversation (Decision C/B carry-forward), I named four trigger signals that would justify tightening test rigor: coverage trend drops, latent-bug regression ships, alpha→beta transition, feature ships test-free where missing tests are obviously needed. **None of these have fired yet** — Lead Dev's discipline holds (79% test coverage on code-touching commits as of the May 4 review). What has surfaced is that **e2e suite design is the right architectural investment to make *before* the alpha→beta trigger fires**, not after — because the design horizon is longer than the implementation horizon, and we'll regret not having it the moment beta starts.

PM ratified the queueing of e2e-suite-design as a parallel architectural item alongside BYOC discovery (May 4). Today, two further signals converge:

1. **BYOC feasibility check** (filed today, parallel memo) — the most ambitious BYOC version requires cross-host validation. Per-host e2e becomes load-bearing once we ship MCP server packaging; can't reconstruct from unit + integration tests.
2. **Anthropic Dreams architectural review** (today) — the simulation-harness pattern from ADR-061 has a clean borrow-target in Anthropic's `pending → running → completed/failed/canceled` job lifecycle. The pattern generalizes.

This memo is the **pre-trigger design pass** for what becomes the e2e suite, so the trigger (whenever it fires) catches a well-shaped target rather than a scramble.

## Existing instance: ADR-061 three-phase calibration

ADR-061 (LLM-touch boundary enforcement, ratified May 3) names a three-phase calibration approach:

- **Phase A** (alpha): simulation harness drives synthetic input population through both detector layers (literal-trigger + semantic); agreement/disagreement table is the calibration signal
- **Phase B** (post-beta cohort onboarding): real beta-traffic refinement against the same disagreement table
- **Phase C** (post-beta refinement landed): production prompt stabilizes; substring detector retained as fast-path or demoted depending on data

The Phase A simulation harness is the structural template. It's currently scoped to *the ethics path specifically* (boundary enforcement), but the shape generalizes to other LLM-touch surfaces.

## Proposal: generalize the simulation-harness pattern to project-scope e2e

### What the e2e suite is

A test surface that drives **synthetic inputs through the entire request lifecycle** — from API entry through intent classification → workflow dispatch → LLM call → ethics detection → response generation → audit-envelope writing — and validates the *integration* of those steps, not the unit-level correctness of each.

This is what unit + integration tests can't do: unit tests verify component correctness in isolation; integration tests verify pairs/triples of components; e2e verifies the *whole flow under realistic conditions*. The simulation harness is the input-generation half; the validation half is the agreement-with-expected-shape check.

### Where the pattern already exists (and where it doesn't)

**Exists, narrowly scoped**:
- **#1004 probe-set harness** (Apr 27, 18/20 PASS run-2 + 112/112 ethics suite + canonical-retest harness)
- **#1018 audit-write integration tests** (Phase 2, May 2 — 14 new test files including unit + integration + redaction + cleanup-job)
- **#1070 multi-turn evaluation harness** (May 13, `canonical-retest-run8.py`) — most generalized of the three; multi-turn synthetic conversations driven through the floor

**Doesn't exist yet**:
- **Cross-surface e2e** — no single harness exercises intent classification → workflow dispatch → LLM call → ethics detection → response generation as a continuous flow
- **Cross-host e2e** — when BYOC ships, validating that the same input produces equivalent behavior across Claude Desktop / ChatGPT / Slack / etc. has no harness today
- **Regression e2e** — when a refactor lands, automatic check that "the prior PASS set still PASSes" doesn't exist; canonical-retest is run on demand, not gated

### Architectural shape of the proposed e2e suite

Four operational layers, mirroring the cleanup-job pattern shape (transaction-boundary isolation, lifespan wiring, failure isolation envelope):

**Layer 1 — Synthetic input registry**: catalogued probe sets by surface (ethics, intent classification, slot extraction, multi-turn conversation, etc.). Each probe has shape: `{input, expected_intent, expected_action_class, expected_audit_shape, severity, notes}`. Single-source-of-truth pattern (per #1033 `safe_surface()` precedent).

**Layer 2 — Harness orchestration**: runs probes through the full request lifecycle. Uses `AsyncSessionFactory.session_scope()` per probe (transaction-boundary isolation; matches Cleanup-Job pattern). Captures actual output + audit envelope.

**Layer 3 — Disagreement table generation**: compares actual vs. expected; classifies divergences (false positive / false negative / shape mismatch / latency divergence / etc.). Per #1004's `divergences` table shape.

**Layer 4 — Reporting + CI integration**: emits structured pass/fail to standard test infra; optional human-review surface for novel divergences (where the expected shape may need updating, not the implementation).

### What this is NOT

- **Not a unit-test or integration-test replacement** — both stay where they are; e2e sits on top
- **Not a manual QA process** — the harness is automated; humans review novel divergences only
- **Not a calibration-against-real-users substitute** — Phase B beta-traffic refinement is separate; e2e is synthetic-input validation
- **Not a hallucination grounding tool** — per #1017 Tier 3 deferral, hallucination grounding is its own design problem (requires source-truth comparison)

## Recommended sequence

**Phase 0: scoping ADR** — *"ADR-NNN: Project-scope e2e suite, generalizing ADR-061 simulation harness."* Names the four-layer shape, the probe-registry pattern, the disagreement-table convention. ~1 architectural session to draft.

**Phase 1: harness scaffolding** — Layer 1 (probe registry) + Layer 2 (orchestration); start with ethics + intent classification surfaces (existing #1004 + #1070 work absorbed in). ~1 week Lead Dev.

**Phase 2: existing probe-set integration** — fold #1004 probe set + #1070 multi-turn into the new harness; demonstrate equivalence with existing canonical-retest workflow. ~3-5 days.

**Phase 3: gap surfaces** — add probe coverage for surfaces not currently exercised end-to-end (workflow dispatch, slot extraction, response generation). ~1-2 weeks; CXO + Lead Dev co-design.

**Phase 4: CI gating** — convert from on-demand to gated (e.g., PR-touching-`services/` must pass ethics + intent e2e probe sets). ~1 week; requires the "no-regression rule" disposition codified.

**Phase 5: cross-host e2e** — when BYOC ships MCP server packaging, extend Layer 2 to drive probes through MCP surface in addition to FastAPI surface. ~1 week; gated by BYOC ship.

Total scope estimate: ~4-6 weeks Lead Dev + ~1 architectural session for ADR. Spread across the BYOC → 1.0 → beta arc.

## When this kicks off (proposed gating)

**Phase 0 (scoping ADR) should start now** — pre-trigger design work; no Lead Dev implementation cost. Architectural session.

**Phase 1-2 (scaffolding + existing-probe integration) should start when** any of: (a) #1017 OUTPUT-CONTENT-FILTER Phase 2 lands (adds a new LLM-touch surface needing probe coverage); (b) BYOC PDR-005 ratifies (MCP server work needs e2e from day 1); (c) M2g closes and Lead Dev bandwidth opens.

**Phase 3-4 (gap coverage + CI gating) should start when** Lead Dev's "test-rigor tightening" trigger signals fire (any of the four named May 4).

**Phase 5 (cross-host) gated by BYOC MCP server ship**.

## Pattern catalog implications

The e2e suite design is structurally adjacent to two pattern candidates I've flagged this week:

- **Cleanup-Job pattern (today's filing)**: the harness orchestration uses the same operational invariants (session_scope per call, cancellation hygiene, lifespan wiring, failure isolation). Probably the e2e harness itself becomes a fourth instance of the cleanup-job pattern when implemented.
- **`task_type` registry pattern (today's observation)**: the probe registry is the same shape — a catalog of typed entries dispatched at consumption time. Confirms the registry-pattern is general-purpose, not surface-specific.

Both suggest the e2e suite is sitting in well-understood architectural territory, not novel design space.

## Cross-references

- ADR-061 three-phase calibration (template): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`
- BYOC feasibility check (companion memo today, parallel architectural item): `mailboxes/arch/sent/memo-arch-to-ppm-cc-cxo-pa-lead-ceo-exec-byoc-feasibility-check-2026-05-15.md`
- Anthropic Dreams architectural review (today, structural compatibility analysis): `mailboxes/arch/sent/memo-arch-to-pa-cc-cio-ceo-cxo-ppm-exec-anthropic-dreams-architectural-review-2026-05-15.md`
- Cleanup-Job pattern candidate (today, sibling architectural pattern): `mailboxes/arch/sent/memo-arch-to-cio-cc-lead-ceo-exec-cleanup-job-pattern-candidate-2026-05-15.md`
- #1070 multi-turn evaluation harness (most-generalized existing instance): commit `e37608b7` May 13
- workstream-042-arch test-rigor assessment (May 4 origin): `mailboxes/arch/sent/workstream-042-arch-2026-05-10.md`

## What I'm asking

- **CEO ratification of proposal direction** — does the four-layer shape + five-phase sequence match your read? Specifically: is Phase 0 (scoping ADR) the right next-step from this memo, or do you want a different shape (PDR? methodology entry? wait for trigger?)
- **Lead Dev refinement** on implementation cost estimates per phase + which surfaces should get probe coverage first
- **CXO refinement** on probe-set scoping (her #1017 Q7 voice-authenticity-on-probes thread is exactly this work)
- **CIO consideration** of whether the four operational invariants belong in methodology corpus, in a new pattern entry, or just in the eventual ADR

— Architect, 2026-05-15
