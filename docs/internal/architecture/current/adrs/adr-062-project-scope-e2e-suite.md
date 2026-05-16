# ADR-062: Project-Scope End-to-End Suite — Generalizing ADR-061 Simulation Harness

**Status**: **Phase 0 ADR (scoping)** — v0.1 (drafted 2026-05-16); CEO ratification of proposal direction received 2026-05-15 via Architect decision walkthrough (Item 1); Phase 1+ gated on trigger signals (see §"Phase Sequencing")
**Date**: 2026-05-16 (v0.1 — Phase 0 scoping ADR per CEO ratification of e2e suite design proposal direction May 15)
**Supersedes**: None (generalizes ADR-061's three-phase calibration shape to project-scope; ADR-061 remains the canonical reference for the ethics-path-specific instance)
**Issues**: #1004 (probe-set harness — narrow-scoped existing instance), #1018 (audit-write integration tests — narrow-scoped existing instance), #1070 (multi-turn evaluation harness — most-generalized existing instance, canonical-retest-run8.py)
**Related**: ADR-061 (LLM-touch boundary enforcement, three-phase calibration template), Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene, Emerging — operational invariants apply to Layer 2 harness orchestration), Pattern-072 (Registries that Grow into Architectural Shapes, Proven — probe registry is same-shape instance), PDR-005 (BYOC distribution model — Phase 5 cross-host gated by MCP server ship)
**Deciders**: Chief Architect (drafted); CEO ratification of direction (2026-05-15); Lead Developer (Phase 1+ implementation refinement at trigger time); CXO (probe-set scoping refinement); CIO (methodology shelf consideration for operational invariants)

---

## Context and Problem Statement

The project has accumulated three narrow-scoped end-to-end harness instances over ~3 weeks of work, each scoped to a specific surface:

- **#1004 probe-set harness** (Apr 27, 2026): boundary enforcement validation; 18/20 PASS run-2 + 112/112 ethics suite + canonical-retest harness shape
- **#1018 audit-write integration tests** (Phase 2, May 2, 2026): 14 new test files including unit + integration + redaction + cleanup-job coverage
- **#1070 multi-turn evaluation harness** (May 13, 2026): `canonical-retest-run8.py` — the most-generalized of the three; multi-turn synthetic conversations driven through the floor

Each instance solves a specific validation problem (boundary enforcement; audit-envelope integrity; multi-turn conversation flow). What does not yet exist is a **cross-surface e2e harness** — a single test surface that drives synthetic inputs through the entire request lifecycle (API entry → intent classification → workflow dispatch → LLM call → ethics detection → response generation → audit-envelope writing) and validates the *integration* of those steps, not the unit-level correctness of each.

Two structural signals from May 15 converge on the need for this surface:

1. **BYOC distribution model (PDR-005)**: the most ambitious BYOC version requires cross-host validation — when the MCP server packaging ships, validating that the same input produces equivalent behavior across Claude Desktop / ChatGPT / Slack / etc. has no harness today. Per-host e2e becomes load-bearing once BYOC packaging lands; cannot be reconstructed from unit + integration tests at that point.
2. **Anthropic Dreams architectural review (May 15)**: the simulation-harness pattern from ADR-061 has a clean borrow-target in Anthropic's `pending → running → completed/failed/canceled` job lifecycle. The pattern generalizes.

The project also has four named test-rigor trigger signals (per May 4 PM walkthrough) that would justify tightening test rigor: coverage trend drops, latent-bug regression ships, alpha→beta transition, feature ships test-free where missing tests are obviously needed. **None of these have fired yet** — Lead Dev's discipline holds (79% test coverage on code-touching commits as of May 4 review). What has surfaced is that the **design horizon for e2e suite architecture is longer than the implementation horizon** — we'll regret not having the scoping ADR in place the moment the trigger fires.

### The specific gap

Unit + integration test coverage at the component level is solid. The gap is at the *whole-flow* level under realistic conditions:

- **No single harness exercises**: API entry → intent classification → workflow dispatch → LLM call → ethics detection → response generation → audit-envelope writing as a continuous flow
- **No cross-host harness exists**: when BYOC ships, "the same input produces equivalent behavior across Claude Desktop / ChatGPT / Slack" has no validation surface
- **No regression e2e gating**: when a refactor lands, automatic check that "the prior PASS set still PASSes" doesn't exist; canonical-retest is run on demand, not gated

### Why pre-trigger design now

Designing under trigger pressure costs weeks of scramble. Designing pre-trigger costs ~1 architectural session (this ADR). The asymmetric cost favors landing the structural commitment now even if Phase 1+ implementation waits for an actual trigger.

The proposal direction was ratified by CEO May 15 via Architect decision walkthrough (Item 1). The four-layer shape and five-phase sequence were agreed; this ADR is the formal Phase 0 scoping artifact.

---

## Decision

### Principle

**Cross-surface end-to-end validation via a generalized simulation-harness pattern is the right architectural primitive for an LLM-touch product approaching multi-host distribution.** The four-layer shape generalizes ADR-061's three-phase calibration template; the five-phase implementation sequence packages it for trigger-driven rollout without forcing implementation work before signals justify it.

The existing narrow-scoped harnesses (#1004 probe-set, #1018 audit-write, #1070 multi-turn) are reference instances; they fold into the generalized harness when Phase 2 lands rather than being replaced standalone.

### Four-Layer Architecture

The e2e suite is structured as four operational layers, mirroring Pattern-070's operational invariants for cleanup-job-with-cancellation-hygiene (transaction-boundary isolation; cancellation hygiene; lifespan wiring; failure isolation envelope):

**Layer 1 — Synthetic Input Registry**

A catalog of probe sets by surface, with each probe carrying a structured shape:

```python
@dataclass
class Probe:
    input: str  # the synthetic input
    surface: str  # which probed surface (ethics, intent_classification, slot_extraction, multi_turn, etc.)
    expected_intent: Optional[str]  # for intent-classification probes
    expected_action_class: Optional[str]  # PASS / DECLINE / DEGRADE / etc.
    expected_audit_shape: Optional[dict]  # structured fields the audit envelope must contain
    severity: Literal["critical", "important", "informational"]
    notes: str  # human context for the probe
```

This is the same-shape pattern as Pattern-072 (Registries that Grow into Architectural Shapes, Proven via #1094): a typed catalog of entries dispatched at consumption. The `task_type` registry, `safe_surface()` registry, and the prospective probe registry are three instances of the same architectural shape.

**Single source of truth**: probes are defined in one registry per surface; tests reference probes by key, not by inlined input strings. When a probe is updated (e.g., #1004's PROFESSIONAL category vector list), every consuming test sees the new value automatically.

**Layer 2 — Harness Orchestration**

Runs probes through the full request lifecycle and captures actual output + audit envelope. The orchestration layer is governed by Pattern-070's four operational invariants:

1. **Transaction-boundary isolation**: each probe uses `AsyncSessionFactory.session_scope()` per call; one probe's transaction state cannot leak to the next
2. **Cancellation hygiene**: capture `asyncio.current_task()` at probe-start; cancellation propagates cleanly without leaving orphan resources
3. **Lifespan wiring**: harness lifecycle managed by a `Phase` class (startup, run-probes, shutdown) — matches the orchestration shape used in the audit-write cleanup job (#1018)
4. **Failure isolation envelope**: broad-except no-propagate around each probe so one probe's failure doesn't tank the entire suite; failures are captured for Layer 3 reporting

The harness drives synthetic input through the production request lifecycle — same code paths users hit — and captures (response shape, audit envelope contents, latency, side effects on persisted state).

**Layer 3 — Disagreement-Table Generation**

Compares actual output vs. expected. Classifies divergences into four categories:

- **False positive**: detector fired on input that should have passed (e.g., over-eager ethics decline)
- **False negative**: detector missed input that should have been caught (the #1003 / #1004 failure shape)
- **Shape mismatch**: response or audit envelope structure doesn't match the contract (missing field, unexpected type)
- **Latency divergence**: response took materially longer than the expected SLA (with explicit threshold)

This is the same disagreement-table shape used in #1004's run-1 and run-2 reports. The Layer 3 output is the load-bearing surface for triage: which divergences are bugs in the implementation vs. cases where the expected shape needs updating.

**Layer 4 — Reporting + CI Integration**

Emits structured pass/fail signals to standard test infrastructure (`pytest` integration). Includes:

- Machine-readable summary (probes_total / pass / fail / divergence_by_category) for CI gating
- Human-readable narrative for triage (which probes failed, what category, what the disagreement looks like, suggested next action)
- Optional human-review surface for novel divergences — cases where the expected shape may need updating (not the implementation), which require an architect / CXO call before being absorbed back into Layer 1

### Phase Sequencing

**Phase 0 — Scoping ADR (this document)**
Pre-trigger architectural design work. ~1 architectural session. **Status: complete with this filing.**

**Phase 1 — Harness Scaffolding**
Implementation of Layer 1 (probe registry primitives) + Layer 2 (orchestration). Starts with ethics + intent classification surfaces — folding in existing #1004 + #1070 work. **Estimated effort**: ~1 week Lead Dev. **Gated on triggers below.**

**Phase 2 — Existing Probe-Set Integration**
Folds #1004 probe set + #1070 multi-turn into the new harness; demonstrates equivalence with existing canonical-retest workflow. **Estimated effort**: ~3-5 days.

**Phase 3 — Gap Surfaces**
Adds probe coverage for surfaces not currently exercised end-to-end (workflow dispatch, slot extraction, response generation). **Estimated effort**: ~1-2 weeks. CXO + Lead Dev co-design at this phase.

**Phase 4 — CI Gating**
Converts from on-demand to gated (e.g., PR touching `services/` must pass ethics + intent e2e probe sets). **Estimated effort**: ~1 week. Requires the "no-regression rule" disposition codified.

**Phase 5 — Cross-Host e2e**
When BYOC MCP server packaging ships, extend Layer 2 to drive probes through MCP surface in addition to FastAPI surface. **Estimated effort**: ~1 week. **Gated by BYOC MCP server ship** (PDR-005 v0.4+ trigger).

**Total Phase 1-5 scope estimate**: ~4-6 weeks Lead Dev spread across the BYOC → 1.0 → beta arc.

### Trigger Signals for Phase 1+ Kickoff

Phase 0 (this ADR) is pre-trigger architectural work. Phase 1+ implementation should kick off when **any** of the following triggers fire:

- **Trigger A — Output-content-filter Phase 2 lands** (#1017): new LLM-touch surface needing probe coverage. The Surface 6 LLM-touch correction (May 15) demonstrated that consumer-trace verification at LLM-touch surfaces matters; an e2e harness validates this at scale.
- **Trigger B — BYOC PDR-005 ratifies** (v0.4+ → ratified): MCP server work needs e2e from day 1. Cross-host validation cannot be reconstructed from unit + integration tests.
- **Trigger C — M2g closes and Lead Dev bandwidth opens**: opportunistic; if M2g closes before A or B fire, Phase 1 starts as a natural use of the open bandwidth window.
- **Trigger D — Test-rigor tightening triggers fire** (any of the four named May 4): coverage trend drops below threshold; latent-bug regression ships; alpha→beta transition decision; feature ships test-free where missing tests are obviously needed.

If multiple triggers fire simultaneously, Phase 1 starts at the earliest one. If none fire, Phase 0 sits as ratified architectural commitment without implementation cost.

---

## Consequences

### Positive

- **Pre-trigger structural commitment** avoids design-under-pressure cost. Phase 1+ has a settled scoping document to scaffold against rather than designing while implementing.
- **Existing harness work consolidates** rather than fragmenting further. #1004, #1018, #1070 fold into Layer 1+2 at Phase 2 rather than living as three parallel harnesses.
- **Cross-host validation has a target**. BYOC MCP server ship has a Phase 5 home rather than emerging as a scramble post-ship.
- **Architecture sits in well-understood territory**: Pattern-070 invariants apply to Layer 2; Pattern-072 framing applies to Layer 1; ADR-061 three-phase calibration is the conceptual template. No novel design space.
- **CI gating becomes feasible** (Phase 4) — the "no-regression rule" disposition codifies what triggers a PR block, which the on-demand canonical-retest workflow cannot enforce.
- **Probe-set scoping converges**: CXO's #1017 Q7 voice-authenticity-on-probes thread, Lead Dev's #1004 probe-set work, and the multi-turn evaluation harness all share Layer 1 once Phase 2 lands.

### Negative / Tradeoffs

- **Phase 5 (cross-host) has a long arc**: gated by BYOC MCP ship which could be months out. The architectural commitment carries a ~6+ month timeline before Phase 5 lands.
- **Trigger-gated implementation** means Phase 1+ work could sit indefinitely if no trigger fires. Mitigation: Trigger C (M2g closure opportunism) provides a baseline kickoff path.
- **Layer 4 CI integration requires the no-regression rule disposition** (which probes are gates vs. observable signal). That decision is not in this ADR; it's a Phase 4 design conversation.
- **Probe registry maintenance cost**: as the project evolves, probes need updating. The Layer 1 single-source-of-truth pattern mitigates this (one place to update), but the cost is non-zero.

### Non-Consequences (explicitly out of scope)

- **Not a unit-test or integration-test replacement** — both stay where they are; e2e sits on top
- **Not a manual QA process** — the harness is automated; humans review novel divergences only
- **Not a calibration-against-real-users substitute** — Phase B beta-traffic refinement (per ADR-061) is separate; e2e is synthetic-input validation
- **Not a hallucination grounding tool** — per #1017 Tier 3 deferral, hallucination grounding is its own design problem (requires source-truth comparison and is not bounded by probe-set scoping)

---

## Validation

### Existing Reference Instances (narrow-scoped)

The architectural shape is validated by three existing instances, each scoped narrowly to one surface:

| Instance | Surface | Validates |
|----------|---------|-----------|
| #1004 probe-set harness | Ethics boundary enforcement | Layer 1 single-source-of-truth probe shape; Layer 3 disagreement-table classification |
| #1018 audit-write integration tests | Audit envelope integrity | Layer 2 transaction-boundary isolation via session_scope |
| #1070 multi-turn evaluation harness | Multi-turn conversation flow | Layer 2 lifespan wiring; multi-probe orchestration through the floor |

When Phase 2 lands, these three instances fold into the generalized harness as the first probe-sets in Layer 1, demonstrating equivalence with the existing canonical-retest workflow.

### Architectural Invariants Inherited from Pattern-070

Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene, Emerging) names four operational invariants that the e2e harness's Layer 2 orchestration must satisfy. The harness itself becomes a fourth reference instance of Pattern-070 when Phase 1 ships:

1. Transaction-boundary isolation via `AsyncSessionFactory.session_scope` per probe
2. Cancellation hygiene via `asyncio.current_task` capture at probe-start
3. Lifespan wiring via `Phase` class managing startup/shutdown
4. Failure isolation envelope via broad-except no-propagate

Phase 1 implementation must demonstrate all four invariants; CI gating at Phase 4 enforces they remain honored across future refactors.

### Pattern-072 Recognition Trigger

The probe registry (Layer 1) is the same-shape architectural primitive as the `task_type` registry and the `safe_surface()` registry — typed catalogs of entries dispatched at consumption time. Pattern-072 (Proven as of #1094 close-out 2026-05-15) names this shape; the probe registry is a third reuse, reinforcing the pattern's generality.

---

## Cross-references

- **ADR-061** (LLM-touch boundary enforcement, three-phase calibration template): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`
- **Pattern-070** (Cleanup-Job-with-Cancellation-Hygiene, Emerging): `docs/internal/architecture/current/patterns/pattern-070-cleanup-job-with-cancellation-hygiene.md`
- **Pattern-072** (Registries that Grow into Architectural Shapes, Proven): `docs/internal/architecture/current/patterns/pattern-072-registries-that-grow-into-architectural-shapes.md`
- **PDR-005 BYOC** (Phase 5 cross-host trigger): `dev/active/PDR-005-bring-your-own-chat-draft-v0.3-2026-05-15.md` (current cycle; v0.4+ ratification triggers Phase 5)
- **e2e suite design proposal** (May 15 source memo): `mailboxes/arch/sent/memo-arch-to-ceo-cc-lead-ppm-cxo-cio-host-exec-pa-e2e-suite-design-proposal-2026-05-15.md`
- **CEO ratification of proposal direction** (May 15 walkthrough Item 1): Architect session log `dev/2026/05/15/2026-05-15-0606-arch-opus-log.md` §"12:19 PM — Decision walkthrough w/ PM, item 1 of 5"
- **Existing instance — #1004 probe-set harness**: tracked at issue #1004; commit history Apr 27, 2026
- **Existing instance — #1018 audit-write tests**: Phase 2 May 2, 2026; 14 test files
- **Existing instance — #1070 multi-turn harness**: `canonical-retest-run8.py`, May 13, 2026 (commit `e37608b7`)
- **CIO methodology-shelf disposition** (operational invariants → Pattern-070; probe-registry → watch surface 12p superseded by Pattern-072): `mailboxes/arch/read/memo-cio-to-arch-cc-ceo-lead-ppm-cxo-host-exec-pa-e2e-suite-methodology-disposition-2026-05-15.md`

---

## Open Items (Phase 1+ work, not gated by this ADR)

- **Probe registry file structure**: one file per surface vs. one consolidated registry; pyproject.toml entry-point pattern vs. direct imports — Phase 1 implementation decision (Lead Dev call)
- **No-regression rule codification**: which probes are CI gates vs. observable signal — Phase 4 design conversation (CXO + Lead Dev + Architect)
- **Cross-host probe shape extension** (Phase 5): what fields probes carry when validating across hosts (host_id, host_version, expected_per_host_variance) — design conversation at PDR-005 v0.4+ ratification time

— Chief Architect, 2026-05-16 v0.1 (Phase 0 ADR; pre-trigger architectural commitment per CEO ratification of proposal direction May 15)
