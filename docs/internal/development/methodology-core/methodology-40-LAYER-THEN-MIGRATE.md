# Methodology-40: Layer-Then-Migrate — Decision Discipline for Retiring Legacy Abstractions Safely

**Status**: v0.1 — **Emerging** (Architect-authored 2026-06-09; CIO catalog confirmation pending)
**Date**: 2026-06-09 (cohort discipline matured 2026-06-06 → 2026-06-08 across 8 instances)
**Origin instance**: ADR-060 amendment verb-enum vs `action_registry` keys (2026-06-06; #1124 cohort + #1158 consult)
**Related**: methodology-30 (Consumer-Trace Verification; load-bearing input), methodology-32 (Postel for Memo Headers; additive-evolution discipline this composes with), methodology-38 (PDR/ADR Tier Separation; sibling decision-altitude framework), methodology-39 (Autonomy Relocates the Bottleneck; m-40 retirement decisions are convergence-point material), Pattern-072 (Registries that Grow into Architectural Shapes; common substrate), Pattern-073 (Documentation-Asserted-Behavior Drift; sibling spec-layer pattern)

---

## Overview

**When retiring a legacy abstraction in favor of a new one, neither pure-supersede (greenfield rewrite) nor pure-layer (parallel-forever) is the right choice.** The disciplined shape is to **layer the new abstraction as source-of-truth for its dimension; preserve the legacy layer with explicit role-separation; migrate the legacy progressively via owner-paced discrete commits**, with backward-compat held in parallel throughout. The legacy retires only where it is genuinely transitional debt; where the two layers serve genuinely-different bounded contexts, the legacy preserves as a permanent anti-corruption layer (ACL).

The retirement decision splits into three load-bearing sub-shapes, depending on the relationship between the two layers:

1. **ACL-vs-debt** (call-translation altitude): Is the legacy layer a genuine bounded-context translation, or is it transitional debt that exists only because the new layer hasn't fully landed?
2. **Lens-vs-flatten** (data-model altitude): Do the legacy entities have genuinely-distinct identity that the new model must preserve, or are they accidentally-divergent shapes of the same conceptual thing?
3. **Contract-vs-build** (data-flow / infrastructure altitude): Is the new commitment the contract (shape, schema, promise) or the build (storage tech, infra, implementation)?

Each sub-shape has its own decision-rule about what retires and what preserves, but all three share the layer-then-migrate trunk: new layer is source-of-truth; legacy preserves until evidence shows it's safe to retire (or evidence shows it must preserve permanently).

## Why this methodology

Between 2026-06-06 and 2026-06-08, the cohort produced **eight distinct retirement decisions across five subsystems and two authors**, all instantiating the same architectural primitive without it being named as a methodology. The primitive emerged from concrete architectural pressure (the verb-enum vs `action_registry` reconciliation surfaced by Lead Dev's #1158 consult), got applied across consecutive architectural decisions (capability primitive at BYOC; per-host capability map; Phase 4 prompt-vs-consumers split), and surfaced its three sub-shapes (ACL-vs-debt; lens-vs-flatten; contract-vs-build) as Lead Dev's downstream consumer-trace work refined the trunk.

Lead Dev explicitly invoked the methodology by name in their 2026-06-07 Phase 4 plan ("This is your layer-then-migrate, applied to the prompt-vs-consumers split") — that's cohort-uptake-by-name evidence, the methodology-29 successful-imitation marker.

The methodology entry codifies what the cohort already does at the retirement-decision altitude. Without explicit codification, each retirement decision re-derives the primitive from scratch, and the three sub-shapes (which only became visible across multiple instances) stay implicit.

## The discipline

### The retirement-decision check (pre-commit-to-rewrite)

When a legacy abstraction is identified as a candidate for retirement, the pre-commit question is:

**Q1**: Are the legacy and new layers serving the **same** bounded context (where preserving both creates drift) — or **genuinely-different** bounded contexts (where retiring the legacy would lose a load-bearing translation)?
- Same context → candidate for full retirement; check Q2 + Q3 to decide retirement shape
- Different contexts → preserve as ACL; retire ONLY components serving the same context (see ACL-vs-debt sub-shape)

**Q2**: Are the legacy entities **conceptually distinct** with information that must be preserved — or **accidentally-divergent** shapes of the same conceptual thing?
- Distinct → use a unifying lens (discriminator + payload that preserves verbatim); do not flatten (see lens-vs-flatten sub-shape)
- Accidentally-divergent → flatten via the new layer; legacy retires per Q1

**Q3**: Is the new commitment the **contract** (shape, schema, promise) or the **build** (storage, infra, implementation)?
- Contract → seed now; defer build; contract evolution is harder to change later than build choice (see contract-vs-build sub-shape)
- Build → defer until contract is settled + value is proven; never commit build before contract

### What replaces the legacy (the trunk)

In all cases where retirement IS the right call:

- **The new abstraction is the source-of-truth for its dimension** (the verb dimension, the capability dimension, the contract dimension, etc.)
- **The legacy abstraction preserves its existing role at a different dimension** (the disposition layer, the per-host configuration layer, the build layer) — explicit role-separation, not parallel duplication
- **Migration is owner-paced via discrete commits** (no flag day, no big-bang). Each commit migrates one consumer; backward-compat held in parallel via converters/shims/parallel keys until consumer is fully on the new layer.
- **Retire the legacy LAST** — only after all consumers have migrated. But: retire only where the legacy is genuinely transitional debt (see ACL-vs-debt below).

### Sub-shape 1: ACL-vs-debt (call-translation altitude)

**Recognition**: a translation layer sits between two abstractions; one would naïvely call it "transitional code to remove."

**The discipline**: ask whether the two abstractions serve genuinely-different bounded contexts. If yes — they have legitimately-different vocabularies, conceptual models, or invariants — the translation layer is a **DDD anti-corruption layer (ACL)**, not transitional debt. Preserve it permanently.

**Origin**: ADR-060 amendment step-4 refinement (2026-06-08). Lead Dev's Phase 4 consumer-trace surfaced that the `verb_sourcetype_to_legacy_action` shim cannot fully retire — `lens_inference.ACTION_TO_LENS` and `file_resolver.intent.action.split("_")` both branch on the fine-grained action and cannot reconstruct it from the verb alone. The shim is the permanent verb↔action ACL between two genuinely-different bounded contexts (the classifier's verb-language vs. handlers' action-language).

**The decision-rule**: retire ONLY where legacy is transitional debt; preserve as ACL where two layers serve genuinely-different bounded contexts.

### Sub-shape 2: Lens-vs-flatten (data-model altitude)

**Recognition**: multiple legacy entities exist piecemeal, each with its own model + repository; a new top-level model is proposed to unify them.

**The discipline**: ask whether the legacy entities have **conceptually-distinct identity** with information that would be lost by collapsing them, or whether they're **accidentally-divergent shapes** of the same conceptual thing. If distinct, build a unifying **lens** (top-level model with a `source_type` discriminator + opaque `payload` that preserves each origin type's specific fields verbatim) with **lossless round-trip converters** (`X == to_X(from_X(X))` invariant). Do not flatten.

**Origin**: #952 Artifact model design ratification (2026-06-08). Lead Dev's design proposed standalone `Artifact` as unifying lens over `UploadedFile` / `Document` / `SurfaceableInsight` / generated content; PM sanity-check rejected reuse-UploadedFile + extend-Document as MUX flattening; Architect ratified the lens-with-round-trip shape with the explicit invariant.

**The decision-rule**: when origin types have genuinely-distinct identity, preserve via discriminator+payload (lens), not flattening. The lossless round-trip invariant is the load-bearing contract that makes "unifying lens" structurally honest rather than aspirational.

### Sub-shape 3: Contract-vs-build (data-flow / infrastructure altitude)

**Recognition**: a future capability (longitudinal persistence, cross-host distribution, schema versioning) requires both a **contract** (event shape, promise, schema commitment) and a **build** (storage tech, infrastructure, implementation). The build is deferrable; the contract may not be.

**The discipline**: ask which layer is the corner-painting risk. The build (storage choice between InfluxDB / TimescaleDB / Postgres-with-Timescale; persona-template content; specific MCP transport) is almost always genuinely deferrable — choice can be made at build time. The contract (event shape, promise wording, schema evolution rules) is harder to change later because today's code asserts shapes that downstream consumers will discover. **Seed the contract now; defer the build.**

**Origin**: #371 spatial-persistence postpone (2026-06-08). Lead Dev proposed postponing INFRA-TIMESERIES storage; CXO answered "seed the *promise-contract* now (interaction surface), defer the *storage build*"; Architect added the complementary "seed the *event-shape contract* now (data surface), defer the *storage tech*" — two contract layers (experience + data) seeded; build deferred. Lead Dev's 2026-06-09 consumer-trace then confirmed the existing event shape is already longitudinal-ready, so the contract-seed cost was just documentation of the gap-list (not even retrofit) — best-case outcome.

**The decision-rule**: seed the contract NOW; defer the build. Contract evolution discipline (methodology-32 Postel) keeps the seeded contract additively extensible when build eventually lands.

## Recognition trigger

This methodology should be invoked **before committing to a retirement shape** (supersede, layer, or layer-then-migrate). Concrete triggers:

- **A role surfaces "we should rewrite/retire X"** — pre-commit check: Q1 (same vs different bounded context); if same context, Q2 (distinct vs accidentally-divergent); Q3 (contract vs build)
- **A new abstraction is proposed that overlaps with legacy machinery** — apply the retirement-decision check before drafting the new abstraction; the answer often is "layer-then-migrate" rather than "replace"
- **An ADR amendment or PDR commits to retiring a legacy layer** — check whether the retirement target is truly transitional debt or actually an ACL/lens worth preserving

## What this catches (failure modes prevented)

- **Greenfield rewrite of working code**: pure-supersede discards working legacy code (the disposition layer + floor-default in `action_registry.py`; the `LifecycleState` + `OwnershipMetadata` patterns; the existing event-shape in `attention_model.py`) for no MVP-functional gain. High blast radius; high risk; almost always wrong when consumer-trace shows legacy is in-use.

- **Parallel-registry drift**: pure-layer (two parallel registries forever, two parallel models forever, two parallel event shapes forever) surfaces as Pattern-073 candidates within months. Drift is invisible until consumer breaks.

- **Flattening that loses distinct identity**: collapsing `UploadedFile` / `Document` / `SurfaceableInsight` into one entity loses the on-disk-vs-external-vs-extracted distinction that has load-bearing operational semantics (lifecycle, ownership, persistence patterns). The MUX-flattening trap.

- **Premature retirement of an ACL**: retiring the verb↔action translation shim would silently break `lens_inference` + `file_resolver` (the action-granular consumers). The shim looks like transitional debt; it's actually permanent architecture.

- **Build-before-contract**: committing to InfluxDB-vs-TimescaleDB-vs-Postgres at design time forecloses options that the contract layer doesn't actually require; the build choice is right-sized at build time, not design time. Same shape with persona-template content (PDR-006), MCP transport choice (separable from ADR-065 wire format), etc.

- **Contract-after-the-fact**: shipping infrastructure that asserts an implicit contract (event shape, schema, promise) without seeding it explicitly produces the Pattern-073 spec-layer drift the cohort has cataloged twice — today's code asserts behavior; future consumers discover the assertion doesn't carry what they need.

## Composability with adjacent methodologies

- **methodology-30 (Consumer-Trace Verification)** is the load-bearing input to layer-then-migrate. The retirement-decision check (Q1/Q2/Q3) requires knowing what consumers exist and what they need; consumer-trace is how that's known. The 2026-06-07 Phase 3 + Phase 4 audit-cascade + 2026-06-09 #371 event-shape trace are three pre-implementation consumer-traces that each made a layer-then-migrate decision evaluable.

- **methodology-32 (Postel for Memo Headers)** is the discipline that keeps the new abstraction additively extensible. Layer-then-migrate's contract-vs-build sub-shape relies on Postel: the seeded contract MUST be additively-evolvable (producers conservative; consumers liberal; unknown fields silently-ignored in `extensions.*` namespaces) so the legacy can preserve while the new layer evolves.

- **methodology-38 (PDR/ADR Tier Separation)** is the sibling decision-altitude framework. m-38 separates decisions by *altitude* (decision-rule vs implementation); m-40 separates *retirement decisions* by *shape* (supersede vs layer vs layer-then-migrate) at any altitude. The two compose: a PDR commits to direction; an ADR commits to implementation shape; the ADR's implementation shape can itself be a layer-then-migrate decision.

- **methodology-39 (Autonomy Relocates the Bottleneck)** intersects with m-40 at the cohort-coordination layer: retirement decisions are convergence-point material — they require cross-pair coordination (Lead Dev + Architect for ADR-060; Architect + Docs for #1182; Architect + PPM + CXO for #1166; etc.). Without cohort-discipline, retirement decisions either skip the discipline (resulting in greenfield rewrites or parallel drift) or relocate to a bottleneck (PM-as-catch).

- **Pattern-072 (Registries that Grow into Architectural Shapes)** is the structural pattern that often becomes the new layer in a layer-then-migrate decision. Six of the eight m-40 instances landed Pattern-072's discipline (typed enum + documented consumers + register-time validation + default policy) as the new layer's shape. The two patterns compose: P-072 names the structural shape; m-40 names the retirement-decision discipline that introduces or transitions to it.

- **Pattern-073 (Documentation-Asserted-Behavior Drift)** is the sibling spec-layer pattern. P-073 surfaces drift between asserted-and-actual behavior at the spec/code interface; m-40 prevents creating new P-073 instances during retirement (parallel-drift is the failure mode m-40's layer-then-migrate-with-discipline avoids).

## Consumers

- **Cohort-wide**: this methodology is invoked at any agent's retirement-decision altitude (Architect for ADR amendments; Lead Dev for implementation shape; Docs for doc-tree retirements; CIO for methodology-catalog retirements; etc.)
- **CIO**: catalog management; cosigns the entry; manages cross-references to m-30, m-32, m-38, m-39, P-072, P-073
- **Architect**: primary author; updates the entry as new instances and refinements surface; maintains the eight-instance catalog (and the eventual cross-author / cross-arc instances)
- **Future-roles**: any future cohort role (HOST, PPM, CXO, etc.) that needs to make a retirement decision invokes the check; the entry's three sub-shapes give them concrete decision-rules

## Default policy

When in doubt about retire-vs-preserve: **treat as ACL until evidence shows transitional debt**. The cost-of-preserving-when-debt is low (extra code; doc clarity needed). The cost-of-retiring-when-ACL is high (silent consumer breakage; rediscovery cost; production regression). Asymmetric risk; conservative default is preserve-with-explicit-role-separation.

When in doubt about contract-vs-build: **seed the contract; defer the build**. Same asymmetric-risk reasoning. Contract evolution is hard; build choice is easy.

When in doubt about lens-vs-flatten: **lens by default**. If distinct identity is real, the lens captures it; if identity turns out to be accidental, the flatten is one cleanup commit later. The reverse (flatten-then-discover-distinct-identity) requires data migration + consumer fixes.

## Promotion-to-Proven criterion (CIO's bar, cited verbatim from 2026-06-08 disposition)

> "**Cross-arc / cross-author / temporal spread.** The Lead 'this is your layer-then-migrate' uptake is a genuinely strong Emerging+ signal — promotion criterion: instances outside this arc / from other authors."

The current 8 instances are largely within one architectural arc (June 6-8 BYOC + intent-classifier work) and largely Architect-authored with Lead Dev applying the methodology in implementation. Promotion to Proven requires:

1. **Instances from other authors** — m-40 invoked by HOST, CXO, PPM, CIO, Docs, PA, or other roles in their own lane
2. **Instances outside this arc** — m-40 applied to a future architectural decision unrelated to BYOC / intent classifier (e.g., a future MUX refactor; a future infrastructure transition; a future cohort-norm retirement)
3. **Temporal spread** — instances accumulating over weeks/months, not days

The eight current instances are the foundation; promotion arrives when the methodology proves itself outside the conditions of its origin.

## Reference instances (8 instances, 2026-06-06 → 2026-06-08, 5 subsystems, 2 authors)

### Instance 1: ADR-060 amendment verb-enum vs `action_registry` keys (2026-06-06 AM)

- **Subsystem**: intent classifier (`services/intent_service/action_registry.py`, #915/#916/#919)
- **Author**: Architect (ratification) ← Lead Dev (drafted amendment)
- **Sub-shape**: trunk (layer + migrate) + lens-vs-flatten implicit (registry keys preserve verbatim via `_query` suffix during migration)
- **Decision**: typed VERB enum layers over `(category, action) → ActionDisposition` registry; VERB is source-of-truth for verb dimension; registry retains disposition role; legacy `_query`-suffixed keys migrate progressively post-#1124 via owner-paced discrete commits
- **Cross-ref**: `docs/internal/architecture/current/adrs/adr-060-floor-first-routing.md` "2026-06-06 Amendment"; `mailboxes/lead/read/memo-arch-to-lead-cc-ppm-cxo-pm-pa-1124-adr-060-amendment-ratified-layer-then-migrate-2026-06-06.md`

### Instance 2: ADR-060 Phase 3 enforce-floor folds into Phase 4 (2026-06-07 AM)

- **Subsystem**: intent classifier (same as #1)
- **Author**: Architect (ratification) ← Lead Dev (coverage finding via methodology-30 pre-implementation consumer-trace)
- **Sub-shape**: trunk + contract-vs-build implicit (Phase 3 = observability contract; Phase 4 = enforce-floor build)
- **Decision**: Phase 3 refined to validation + observability only (boundary computes `get_verb(intent.action)`, emits telemetry on `None`); enforce-floor (unknown verb → floor) folds into Phase 4 as canonical-retest-gated build
- **Cross-ref**: ADR-060 "2026-06-07 Phase 3 re-scope refinement"; `mailboxes/lead/read/memo-arch-to-lead-cc-pm-ppm-cxo-pa-1124-phase3-rescope-approved-observability-as-backlog-signal-2026-06-07.md`

### Instance 3: ADR-065 D3 capability primitive (2026-06-06 PM)

- **Subsystem**: BYOC capability layer (`docs/internal/architecture/current/adrs/adr-065-canonical-context-package-format.md`)
- **Author**: Architect
- **Sub-shape**: trunk (typed enum + slot inherits the verb-enum-vs-collapsed-name layer-then-migrate shape)
- **Decision**: capability primitive is `verb` (typed enum) + `surface_type` (slot); NOT a verb-object collapsed string; same architectural primitive as ADR-060 amendment applied at the BYOC altitude; 7th Pattern-072 application
- **Cross-ref**: ADR-065 §Decision D3

### Instance 4: ADR-066 D1 per-host capability map (2026-06-07 AM)

- **Subsystem**: BYOC packaging-layer abstraction (`docs/internal/architecture/current/adrs/adr-066-packaging-layer-abstraction.md`)
- **Author**: Architect
- **Sub-shape**: trunk (registry shape organized per-host; layered over ADR-065 D3 primitives)
- **Decision**: `config`-declared YAML map keyed on `surface_type`; verb-level granularity; per-host `conditions`; `unknown` surface defaults to claim-nothing; 8th Pattern-072 application
- **Cross-ref**: ADR-066 §Decision D1

### Instance 5: ADR-060 Phase 4 hybrid prompt-vs-consumers split (2026-06-07 PM)

- **Subsystem**: intent classifier Phase 4 transition
- **Author**: Architect (ratification) ← Lead Dev (plan proposed hybrid + named the pattern by name)
- **Sub-shape**: trunk + ACL-vs-debt implicit (consumers shim-then-migrate)
- **Decision**: classifier prompt big-bang (atomic by nature; canonical-retest gated); consumers shim-then-migrate via `verb_sourcetype_to_legacy_action()` in `action_registry.py`; migrate consumers off legacy aliases one discrete commit at a time. **Lead Dev invoked layer-then-migrate by name**: "This is your layer-then-migrate, applied to the prompt-vs-consumers split." First cohort-uptake-by-name instance.
- **Cross-ref**: ADR-060 "2026-06-07 Phase 4 plan ratification"; `mailboxes/lead/read/memo-arch-to-lead-cc-pm-ppm-cxo-pa-1124-phase4-plan-ratified-q1q2-2026-06-07.md`

### Instance 6: Phase 4 shim-as-permanent-ACL ratification (2026-06-08 AM) — **ACL-vs-debt distinction source**

- **Subsystem**: intent classifier Phase 4 step 3 (consumer migration)
- **Author**: Architect (ratification) ← Lead Dev (DDD anti-corruption-layer finding via Phase 4 step-3 consumer-trace)
- **Sub-shape**: ACL-vs-debt (the sub-shape's origin instance — the shim turns out to be ACL not debt)
- **Decision**: `verb_sourcetype_to_legacy_action` shim cannot fully retire; `lens_inference.ACTION_TO_LENS` + `file_resolver.intent.action.split("_")` are action-granular consumers that cannot reconstruct fine-grain from verb alone; shim preserves as permanent ACL; Step 4 refined to "retire FOR DISPATCH consumers; preserve as permanent ACL for action-granular consumers"
- **Cross-ref**: ADR-060 "2026-06-08 Step-4 refinement"; `mailboxes/lead/read/memo-arch-to-lead-cc-pm-pa-ppm-cxo-phase4-shim-permanent-acl-ratified-2026-06-08.md`

### Instance 7: #952 Artifact unifying-lens with lossless round-trip (2026-06-08 PM) — **Lens-vs-flatten distinction source**

- **Subsystem**: MUX object-model (`services/domain/models.py`; `services/mux/lifecycle.py`; `services/mux/ownership.py`; existing `UploadedFile` / `Document` / `SurfaceableInsight` entities)
- **Author**: Architect (ratification) ← Lead Dev (design + lens-with-round-trip proposal)
- **Sub-shape**: lens-vs-flatten (the sub-shape's origin instance — origin types have distinct identity; lens preserves via discriminator+payload)
- **Decision**: standalone `Artifact` as unifying lens with `source_type` discriminator + `payload` dict preserving origin-type fields verbatim; lossless round-trip converters with `X == to_X(from_X(X))` invariant; round-trip-now + incremental-unification-later (per-consumer-migration shape)
- **Cross-ref**: `docs/internal/architecture/current/artifact-model-design-952.md`; `mailboxes/lead/read/memo-arch-to-lead-cc-pm-pa-ppm-cxo-952-artifact-model-ratified-lens-with-round-trip-2026-06-08.md`

### Instance 8: #371 spatial event-shape contract seed-now (2026-06-08 PM + 2026-06-09 AM) — **Contract-vs-build distinction source**

- **Subsystem**: spatial intelligence (`services/intelligence/attention_model.py`; `attention_decay_job.py`; lens stack)
- **Author**: Architect (seed-now ruling) ← Lead Dev (consumer-trace + additive-gaps confirmation 6/9) + CXO (promise-contract seed at experience layer)
- **Sub-shape**: contract-vs-build (the sub-shape's origin instance — seed contract NOW; defer build entirely)
- **Decision**: defer storage choice (InfluxDB / TimescaleDB / Timescale-on-PG) entirely; seed the event-shape contract NOW (timestamps, correlation IDs, dimensional tags, decay-respecting semantics) + the promise-contract NOW (in-session voice constraint per CXO); methodology-30 consumer-trace 2026-06-09 confirmed gaps are additive optional fields → no code change needed now, just documented gap-list
- **Cross-ref**: `docs/internal/architecture/current/spatial-persistence-contract-seed-371.md`; `mailboxes/lead/read/memo-arch-to-lead-cc-ppm-cxo-pm-pa-371-spatial-persistence-concur-with-event-shape-seed-2026-06-08.md`; `mailboxes/arch/read/memo-cxo-to-lead-cc-arch-pm-pa-371-promise-wording-ratified-plus-in-session-voice-constraint-2026-06-09.md`

## What this methodology is NOT

- **Not a process gate**: layer-then-migrate isn't a formal approval step; it's a retirement-decision check the agent performing the architectural work should run
- **Not a recipe for new abstractions**: the methodology is about RETIREMENT decisions — when legacy machinery exists and a new layer is proposed. Greenfield architecture (no legacy to retire) doesn't invoke this; use methodology-38 (PDR/ADR tier separation) + Pattern-072 (structural patterns) for greenfield instead
- **Not a license to preserve indefinitely**: the discipline says "retire only where genuinely transitional debt" — but transitional debt DOES retire. The methodology doesn't justify preserving every legacy abstraction forever; it justifies preserving where the evidence supports ACL/lens/contract status
- **Not exhaustive of retirement decisions**: other retirement-decision shapes (e.g., feature flag rollouts, A/B-test-then-pick, sunset-by-deprecation) are real and not covered here. m-40 specifically names the layer-then-migrate shape, which is the right shape when consumer-trace shows in-use legacy + a new layer at a different abstraction altitude

## Open items

- **CIO catalog confirmation** — pending; ping CIO on filing this entry (per CIO 2026-06-08 disposition: "you author, I allocate the number (40) + cosign — exactly the m-38 precedent")
- **Promotion-to-Proven criterion** — cited verbatim from CIO 2026-06-08; will track instances outside this arc + from other authors as they accrue
- **Sub-shape catalog** — three sub-shapes (ACL-vs-debt, lens-vs-flatten, contract-vs-build) catalogued from the 8 instances; future instances may surface additional sub-shapes; entry will extend
- **Cross-author validation** — none of the 8 instances are cross-author at the m-40 invocation altitude; Lead Dev applied the methodology in implementation work but Architect ratified at the methodology-altitude. Genuine cross-author invocation (HOST, CXO, PPM, CIO, Docs, PA invoking m-40 directly in their own lane) is the Proven-bar gate
- **Default-policy refinements** — three defaults stated here (preserve-as-ACL until evidence shows debt; seed-contract before build; lens-by-default); future instances may surface counter-examples that refine the defaults

— Chief Architect, 2026-06-09 v0.1 (Architect-authored draft; pending CIO catalog confirmation + indexing)
