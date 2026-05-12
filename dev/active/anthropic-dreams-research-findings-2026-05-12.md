# Anthropic "Managed Agents Dreams" — Research Findings + Implications for Piper Morgan

**Prepared by**: PA (Piper Alpha)
**Date**: 2026-05-12
**Phase**: 1 + 2 (mechanism survey + comparison matrix). Phase 3 (architectural implications) is preliminary; awaits Architect/CIO review.
**Sources**: Anthropic official docs (`https://platform.claude.com/docs/en/managed-agents/dreams`); Simon Willison conference live-blog (`https://simonwillison.net/2026/May/6/code-w-claude-2026/`); Klatch Argus 5/11 sweep intel; PM internal: dreaming-concept-provenance-2026-04-12.md, composting-learning-architecture.md, ADR-054, Apr 12 Janus prior-art survey, Apr 14 PA Managed Agents assessment.

---

## TL;DR

Anthropic's "Dreams" is a **developer-triggered, asynchronous, batch consolidation job** that takes a memory store + session transcripts and produces a cleaner reorganized memory store. It is **Type 1 (filing dreams / consolidation)** by any reasonable mapping to Piper Morgan's concept.

Three findings that matter:

1. **Type 1 alignment is direct.** Anthropic now provides a primitive that does what PM's composting architecture spec describes. Strong delegation candidate.
2. **Type 2 is still absent from the ecosystem.** Anthropic Dreams handles consolidation only — no threat simulation, risk rehearsal, or anxiety-dream-shape processing. Janus's "no equivalent in 20+ surveyed systems" verdict still holds; Piper's distinctive concept is preserved.
3. **Unihemispheric framing is also untouched.** Anthropic's batch-on-demand model doesn't solve the power-user / multi-timezone / no-idle-time problem, because it's developer-triggered anyway. PM's "dolphin / partial rotating" concept remains PM-distinctive and orthogonal.

The strategic implication aligns with Argus's Klatch reframe but is more specific for Piper: **delegate Type 1 substrate to Anthropic where viable; preserve and double down on Type 2 + unihemispheric as PM-distinctive assembly-layer differentiators.**

---

## What Anthropic actually shipped (Phase 1 findings)

### Mechanism

A **dream** is an asynchronous job. The developer calls `client.beta.dreams.create()` with:

- **An input memory store** (existing — to be verified, deduplicated, reorganized)
- **Optionally, up to 100 sessions** (past transcripts the model mines for patterns/insights)
- A **model** (`claude-opus-4-7` or `claude-sonnet-4-6` during research preview)
- Optional **instructions** (up to 4,096 chars) to steer the dream

The job runs asynchronously (minutes to tens of minutes), polled via status: `pending → running → completed/failed/canceled`. The output is a **separate output memory store** — the input is never modified, supporting a review-then-adopt workflow.

Key properties:

- **Developer-triggered, not Anthropic-triggered.** No idle-time detection, no scheduled-by-Anthropic execution. The caller decides when a dream runs.
- **Batch, not incremental.** One dream = one consolidation pass over a defined input set.
- **Memory-store-scoped.** One memory store per dream; not "the whole agent dreams."
- **Observable.** Once running, the underlying session ID can be streamed to watch the pipeline in real time.
- **Cancelable.** Pending or running dreams can be canceled.

### API surface

```python
dream = client.beta.dreams.create(
    inputs=[
        {"type": "memory_store", "memory_store_id": store_id},
        {"type": "sessions", "session_ids": [session_a, session_b]},
    ],
    model="claude-opus-4-7",
    instructions="Focus on coding-style preferences; ignore one-off debugging notes."
)
```

Beta headers required: `managed-agents-2026-04-01,dreaming-2026-04-21`. Research Preview — access form required. SDK supports create, retrieve (poll), cancel, archive, list.

### Storage (memory stores — the substrate)

Memory stores are an existing primitive (separate API). Per PA's Apr 14 assessment of Memory Stores:

- Path-based filesystem metaphor
- Optimistic concurrency via SHA256
- Immutable version history with redaction support
- 100KB per memory cap ("many small focused files")
- Per-Anthropic-org workspace; attachable to sessions as resources

Dreams takes one memory store + sessions → produces a new memory store. The output is an ordinary memory store usable as a session resource going forward.

### Pattern types — what Dreams actually does

Anthropic's positioning quote:

> *"Agents write to their memory stores as they work, but these writes are local and incremental: over many sessions a memory store accumulates duplicates, contradictions, and stale entries. Dreams let Claude clean that up. A dream reads an existing memory store alongside past session transcripts, then produces a new, reorganized memory store: duplicates merged, stale or contradicted entries replaced with the latest value, and new insights surfaced."*

That is **pure consolidation/indexing language**. Three operations are explicit:

1. Merge duplicates
2. Replace stale/contradicted entries with the latest value
3. Surface new insights from session transcripts

What the documentation does **NOT** describe:

- Threat simulation / "what if this fails" rehearsal
- Pre-emptive risk identification
- Anxiety-dream-shape processing
- Failure-mode anticipation
- Adversarial rehearsal
- Any forward-looking reasoning beyond "what's an insight that emerged from past work"

Simon Willison's drone-landing example (`descent-playbook.md` produced from prior session analysis) is canonical Type 1 shape — extracted operational knowledge for future success.

### Cycles — whole-store vs. partial

Dreams is **whole-store-at-a-time**. One dream takes one memory store as input and produces one memory store as output. There is no concept of:

- Some parts of the agent's memory continuing to operate while other parts dream
- Rotating consolidation cycles
- Partial reflection / partial memory updates
- An "active state" vs. a "dreaming state" with smooth transitions

The agent that *uses* the memory store isn't gated during a dream (because the input is never modified — the dream produces a *new* store), so functionally the agent can keep working with the old store while a dream is running. But the dream itself is a discrete batch job, not a partial-rotating cycle.

### Cost / token economics

- **Standard API token rates** for the model selected (no special pricing)
- Usage reported on the dream resource (`input_tokens`, `output_tokens`, cache stats)
- Cost scales roughly linearly with input size (sessions + memory store)
- Default rate limits during beta; contact support for higher limits

### Constraints

- 100 sessions max per dream
- 4,096 char instructions limit
- 2 supported models (Opus 4.7, Sonnet 4.6)
- Research Preview access gated by form
- Can't archive/delete output while pipeline running
- Input store deletion/archival mid-run fails the dream

### What problem Anthropic says it solves (verbatim quote)

> *"Agents write to their memory stores as they work, but these writes are local and incremental: over many sessions a memory store accumulates duplicates, contradictions, and stale entries. Dreams let Claude clean that up."*

That's the entire positioning. **It's a maintenance primitive for memory stores**, not a reasoning extension. It's worth noting Anthropic chose "Dreams" rhetorically — but the marketing language and the technical description diverge: the marketing implies emergence/reflection, the technical description is consolidation/dedup/insight-extraction.

---

## Comparison matrix (Phase 2)

### Axis: type of cognitive processing

| | PM Type 1 (Filing dreams) | PM Type 2 (Anxiety dreams) | PM Unihemispheric | Anthropic Dreams |
|---|---|---|---|---|
| **Primary operation** | Consolidate, index, extract patterns | Simulate failure modes, rehearse risks, anticipate problems | Partial-rotating updates so some components dream while others stay active | Consolidate, dedupe, replace stale, surface insights |
| **Time orientation** | Past-looking (what happened) | Forward-looking (what could happen) | Continuous | Past-looking |
| **Trigger** | Scheduled idle-time (2-5 AM) | Unspecified (named but never specified) | Continuous rotation | Developer-triggered API call |
| **Scope** | All accumulated experience | All accumulated risk surface | One component at a time | One memory store + up to 100 sessions per call |
| **Output** | InsightJournal entries surfaced via "Having had some time to reflect, it occurs to me..." framing | Proactive risk identification, pre-emptive mitigation | Smooth ongoing operation | Reorganized memory store (review-then-adopt) |
| **Implementation status (PM)** | Designed, not implemented (composting-learning-architecture.md, ADR-054) | Named Nov 2025, not specified, not implemented; CIO unihemispheric memo corrupted | Discussed Jan 11, not designed | N/A — Anthropic-shipped |

### Axis: relationship of Anthropic Dreams to each PM component

| PM Component | Anthropic Dreams | Relationship | Implications |
|---|---|---|---|
| Type 1 (Filing dreams) | ✅ **Direct match** | Anthropic IS Type 1. Same problem statement, same operation shape, similar review-then-adopt workflow. | **Strong delegation candidate.** PM's CompostBin/Decomposer/LearningExtractor/InsightJournal stack maps onto memory_store + sessions → output_store. |
| Type 2 (Anxiety dreams) | ❌ **Not present** | Dreams is purely past-looking consolidation. No threat simulation, risk rehearsal, or forward-looking reasoning. | **PM ownership preserved and strengthened.** Janus's "no equivalent in 20+ systems" verdict still holds. PM's distinctive concept survives Anthropic's release. |
| Unihemispheric extension | ❌ **Not present** | Dreams is whole-store-at-a-time, developer-triggered. Doesn't address the no-idle-time / power-user problem. | **PM ownership preserved.** Orchestrating partial Dreams is possible but is PM-side scheduling logic, not an Anthropic primitive. The concept remains PM-distinctive and orthogonal. |

### Axis: what Anthropic provides vs. what PM still owns

| Layer | Anthropic provides | PM still owns |
|---|---|---|
| **Storage substrate** | Memory Stores API (path-based, immutable versions, 100KB per file) | Choice of what to put in them; mapping PM's domain entities (insights, learnings, etc.) onto the path/file shape |
| **Consolidation mechanism** | Dreams API (batch reorganization with optional instructions) | Decision to trigger; cadence; instruction-text steering ("Focus on X, ignore Y"); review-then-adopt UX |
| **Type 2 processing** | Nothing | Everything — concept, implementation, integration |
| **Unihemispheric orchestration** | Nothing | Everything — partial-rotating scheduling, component separability, trigger conditions |
| **User-facing surface** | Nothing | Everything — "filing dreams" framing, "Having had some time to reflect..." voice, InsightJournal navigation, COMPOSTED-state UX, trust-gated surfacing |
| **Multi-tenancy / multi-user** | Per-org workspace | Per-user mapping, per-PM-persona separation, BYOC distribution patterns |

---

## Preliminary architectural implications (Phase 3 — Architect/CIO review pending)

### For PM's composting architecture spec

The existing `docs/internal/architecture/current/composting-learning-architecture.md` describes:

- **CompostBin** — accumulates deprecated objects
- **Decomposer** — breaks objects into patterns
- **LearningExtractor** — extracts learnings
- **InsightJournal** — surfaces learnings
- **EmergentCreator** — synthesizes new emergent objects
- **Triggers**: AGE, IRRELEVANCE, MANUAL, SCHEDULED (2-5 AM), CONTRADICTION

A direct delegation re-mapping:

- **CompostBin** → an Anthropic memory store containing accumulated experience
- **Decomposer + LearningExtractor** → a Dreams call with appropriate instructions
- **InsightJournal** → the output memory store + PM-side surfacing layer (PM-owned)
- **EmergentCreator** → still PM-owned (emergent object creation is downstream of insight extraction)
- **Triggers** → PM-side scheduler decides when to call Dreams; the trigger taxonomy (AGE/IRRELEVANCE/MANUAL/SCHEDULED/CONTRADICTION) collapses to "developer-triggered" from Anthropic's view but stays meaningful as PM-side scheduling logic

**What this changes for PM's implementation plan**:

- PM's composting pipeline becomes thinner — Anthropic handles the mining/consolidation step
- PM's value-add moves to: trigger selection, instruction-steering, output review, surfacing UX, multi-store orchestration
- The 100KB-per-memory cap and per-org workspace shape may require PM-side mapping decisions (does each "compost cycle" produce one file per insight or one large summary file?)

### For #984 CONTEXT-CACHE Phase 0 (still pending PM decision)

The 6 architecture questions PM tabled at Phase 0:
1. Key shape
2. TTL defaults
3. Invalidation strategy
4. Decorator-vs-helper
5. Scope minimum vs. complete
6. Namespace prefix

Anthropic Dreams suggests a relevant pattern for the **invalidation strategy** question specifically: **periodic re-mining as the invalidation model**, rather than continuous staleness detection. The "input never modified; output separate" pattern is a clean version of "rebuild rather than mutate." Worth flagging to Architect when #984 gets scheduled.

### For M3 Artifact Persistence (#952, #953)

- **#952 ARTIFACT-MODEL** could absorb the "input store + output store" pattern directly into PM's data model
- **#953 CONTEXT-PERSIST** cross-session memory persistence has Anthropic memory stores as an obvious upstream substrate to evaluate vs. building from scratch

These don't change M3's commitment but inform the design questions when M3 gameplans.

### For BYOC PDR-005

Reinforces the Klatch convergence finding. Specifically:

- BYOC commitment should explicitly acknowledge that **memory consolidation may be delegated to Anthropic Managed Agents Dreams** in deployment configurations that use the Managed Agents path
- The MCPB local path may not have access to Dreams (depending on Anthropic's pricing/availability for non-Managed-Agents callers)
- PM-side Type 2 and unihemispheric work is **PM's distinctive contribution regardless of deployment path**

This is a small refinement to PPM's PDR-005 work, not a re-scope.

### For Type 2 design (future)

Anthropic's Dreams API could be a creative substrate for Type 2 if/when PM designs it:

- Submit the same inputs (memory store + sessions) with a Type 2 instructions string:
  > *"Identify failure modes in past sessions. For each, articulate what could go wrong if a similar pattern recurs. Produce a risk register, not a knowledge summary."*
- Produce a DIFFERENT output store with risk-register semantics
- Two parallel dream jobs from the same inputs: Type 1 (consolidation) and Type 2 (anxiety) → two output stores with different purposes

This is a creative use of the Dreams API beyond Anthropic's intended scope but not precluded. Worth flagging for the eventual Type 2 design session. **Caveat**: Anthropic's model + instructions may not produce useful Type 2 output without significant prompt engineering — the model is trained to extract knowledge, not to anticipate failure. Would need calibration work.

### For unihemispheric orchestration (future)

Anthropic's Dreams doesn't help with the no-idle-time problem because it's developer-triggered. But PM could orchestrate **partial Dreams** by:

- Submitting smaller-scope batches (e.g., "only the last 5 sessions worth of data") on a rolling schedule
- Running multiple parallel Dreams for different memory store partitions
- Coordinating Dreams cadence with multi-entity activity patterns

The dolphin-metaphor concept (partial rotation) remains PM-side scheduling logic. No change to the design challenge; just confirms Anthropic doesn't pre-solve it.

---

## Recommendations

### Immediate (within 1 week)

1. **Route this memo to Architect + CIO + CXO + PPM with PM on CC.** Phase 1+2 findings are stable; Phase 3 needs their input.
2. **Decision: register Type 2 as a "claimed but unbuilt" distinctive PM concept formally.** Janus's Apr 12 prior-art survey + Anthropic's May 6 release together make this the right moment to put a stake in the ground. Suggest a CIO methodology-core entry or PDR — frames it as PM's IP / distinctive contribution before someone else discovers it.
3. **Coordinate with Klatch's Calliope via Janus** when ready — independent reads complete; reconciliation pass on findings would surface where Klatch and PM converge/diverge on the assembly-layer differentiation thesis.

### Medium-term (during M3 gameplan)

4. **Architect: evaluate Dreams as substrate vs. build-it-ourselves for Type 1.** Decision points listed in §"For PM's composting architecture spec" above. Doesn't need to happen before M3 starts but does before M3 ADRs land.
5. **Update ADR-054 (Cross-Session Memory Architecture)** when Dreams substrate decision lands — current ADR describes PM-side implementation; if delegation is chosen, the ADR rewrites significantly.

### Long-term (post-M3, into M4 Trust + Learning)

6. **Type 2 design session.** Use this research as a forcing function. PM's distinctive concept needs a designed-and-specified version before implementation can be sequenced. Architect + CIO + CXO collaboration shape; CIO's lane on methodology framing.
7. **Unihemispheric design session.** Separate from Type 2; partial-rotating scheduling is its own design problem.

---

## Open questions left for PM/leadership

1. **Should PM "claim" Type 2 publicly** (e.g., a blog post, methodology entry, or PDR) before someone else builds it? Timing question.
2. **Is Dreams substrate-delegation acceptable to PM's BYOC posture?** Locking PM's Type 1 implementation to Anthropic Managed Agents constrains some deployment paths.
3. **What's the appropriate cadence for revisiting this?** Anthropic is iterating; the research preview will evolve. Suggest: re-check Anthropic's Dreams docs at start of M3 (likely 2-3 months out) for changes.
4. **Should PA + Calliope coordinate before vs. after each does their independent pass?** Per the original research plan, my lean was "after"; remains my lean given that Argus's framing is strategic and mine is mechanism-deep, and the two are complementary not redundant.

---

## What this is NOT

- Not an implementation plan — purely analysis
- Not a recommendation to change roadmap v15.0 immediately — implications may inform a future update at M3 boundary
- Not coordinating with Anthropic directly — one-way absorption of public material
- Not absorbing OpenLaws IP — confirmed out of scope per PM 2026-05-10

---

— PA, 2026-05-12
