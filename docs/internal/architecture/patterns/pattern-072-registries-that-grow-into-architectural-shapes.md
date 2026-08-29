# Pattern-072: Registries that Grow into Architectural Shapes

## Status

**Proven** — Promoted from Emerging on 2026-05-16 by CIO per `methodology-audit-policy-updates-2026-03-16.md` self-approval authority. Promotion-to-Proven trigger fired via #1094 ENGINE-DELETION close-out (commit `d48bc1d0`, merged 2026-05-15 14:38 PST): Slack handler dispatch routes through `intent_service.process_intent` which dispatches via the `task_type` registry to canonical handlers — fourth meaningful behavior-deciding consumer of the registry, landing without violation of the formalization discipline (typed enum / documented consumer set / explicit default policy / register-time validation, all four invariants intact). Originally filed Emerging 2026-05-15 by Lead Developer per CIO disposition (May 15) following Architect's observation during #1017 Phase 1 ratification + Lead Dev's methodology memo. Slot 072 allocated after 12l pre-filing slot-availability check. **Methodology-29 ("Pattern Formation via Successful Imitation") instance applied to registries** rather than to code shapes. Three-consumer recognition threshold + fourth-consumer Proven trigger both fired within ~6 hours on 2026-05-15 — Pattern-072 is the framework's first sub-day Emerging-to-Proven promotion.

### The four consumers (Proven-promotion evidence)

| # | Consumer | When | Behavior decision |
|---|---|---|---|
| 1 | `task_type` → model config dispatch (original) | Pre-existing | Route to per-task model (cheap vs. premium) |
| 2 | #1004 calibration telemetry | 2026-04-27 | Partition BoundaryEnforcer probe set by task_type |
| 3 | #1017 output-filter profile dispatch | 2026-05-15 AM | Filter on/off + Tier 1/2 policy (`user_visible` / `internal` / `mixed`) |
| 4 | **#1094 Slack handler EXECUTION dispatch** | **2026-05-15 PM** | Replaces OrchestrationEngine + WorkflowFactory chain; routes via `intent_service.process_intent` → task_type registry → canonical handlers |

Architect's e2e-suite probe registry remains a prospective fifth instance per the May 15 design proposal; if it adopts the discipline cleanly when implemented, it becomes confirmation rather than promotion trigger.

### Formalization-discipline check (verified at promotion)

- **Typed enumeration** ✅ — `TaskType` enum in `services/shared_types.py` (pre-existing; not weakened)
- **Documented consumer set** ✅ — the four consumers above + the pattern body
- **Explicit default policy** ✅ — unknown task_types fail-closed to `user_visible` in #1017 filter; Slack dispatch in #1094 routes through canonical-handler dispatch (no silent default)
- **Register-time validation** ✅ — `WorkflowDispatcher.validate_registry()` at startup checks task_type → handler coverage

## Product Relevance

**Architecture / Methodology** — Recognition discipline for a specific evolution shape that affects how teams maintain typed enumerations as they accrue consumers. Users will not encounter this pattern directly; agents and engineers maintaining the codebase will reach for it when deciding whether to formalize an annotation that's outgrown its original purpose.

## Context

Some annotations start single-purpose. A string field on a method signature, a tag on a model, an enum used for one routing decision. The annotation does one job and the surface is small.

Then a second consumer reuses the annotation for a related but distinct purpose. Now two pieces of code make decisions based on the annotation's value. The original single-purpose framing still mostly fits.

Then a third consumer reuses the annotation. The annotation is no longer single-purpose; it's a **taxonomy**. Multiple unrelated parts of the system query it to decide behavior. Adding a new value to the annotation now affects all three consumers — sometimes silently, sometimes via a fail-closed default, sometimes by quietly producing wrong behavior in a consumer whose maintainer hasn't been told about the registry's new role.

This pattern names the recognition trigger (third meaningful consumer is the formalization threshold) and prescribes the formalization discipline (typed enum, documented consumer set, explicit default policy, register-time validation).

### Where this surfaced

#1017 OUTPUT-CONTENT-FILTER Phase 1 design (2026-05-15) made `task_type` the third meaningful consumer:

1. **task_type → model config dispatch** (original, single-purpose) — `LLMClient.complete(task_type=..., prompt=...)` selected per-task model configuration (`task_type="intent_classification"` → cheap model; `task_type="conversation"` → premium model). One job: route to the right model.
2. **#1004 calibration telemetry** (Apr 27, 2026) — per-task-type detection-effectiveness analysis. BoundaryEnforcer probe set keyed by `task_type` so calibration accuracy could be partitioned by where the LLM was being called from. Second meaningful consumer using the annotation for behavior partitioning.
3. **#1017 output-filter profile dispatch** (May 15, 2026) — `task_type` → filter profile (`user_visible` / `internal` / `mixed`) determining whether outputs get PII redaction + boundary-category check. Third meaningful consumer; behavior decision (filter on/off) keyed by the annotation.

Architect's observation in the parallel e2e-suite design proposal (May 15) flagged a **fourth candidate consumer**: *"the probe registry is the same shape — a catalog of typed entries dispatched at consumption time."* That observation became the Proven-promotion criterion for this pattern: if the e2e probe registry adopts the formalization discipline without rediscovery, the pattern's value is empirically confirmed.

The pattern names the converging shape so future similar annotations have a citable framework — and a recognition trigger before consumer divergence becomes a coordination cost.

## Problem

### The Failure Mode

```
Annotation X created for single consumer A
  → "X is just for A; small surface; no governance overhead needed"

Consumer B uses X for related purpose
  → "X works for B too; nice reuse; still small"

Consumer C uses X for unrelated purpose
  → X is now a registry; three distinct decision points read it
  → adding new value Y to X requires understanding A, B, and C
  → maintainer of Y might know A and B (their direct context) but not C
  → C's behavior changes silently when Y is added
  → no one notices until Y produces a wrong decision in C's surface
```

The asymmetry that makes this load-bearing:

- **Adding a value is cheap** (one-line enum addition; "I just need this for my feature")
- **Understanding what it affects is expensive** (grep across services/, identify all consumers, understand each consumer's behavior under the new value)
- **The cost is paid by every future maintainer who adds a value**, not by the first three consumers who established the registry

Without formalization, every value-addition becomes a tax. With formalization, the tax is paid once (documenting the registry + its consumers + the default policy) and amortized.

### Where this *could* surface

Five candidates in PM's codebase:
- `task_type` (this pattern's reference instance) — 3 confirmed consumers
- HTTP status codes — used by logging, monitoring, SLO, error-handling layers
- Log levels — used by filtering verbosity, alert rules, SLO thresholds
- Git commit type prefixes (`feat:` / `fix:` / `chore:`) — used by changelog generation, release scope, branch protection
- BoundaryType / BoundaryCategory enums (ADR-061) — currently single-consumer (BoundaryEnforcer); fourth-consumer trigger if other surfaces start dispatching on category

The pattern's value is that the third-consumer threshold gives a clear *moment to formalize* — before the registry accumulates enough consumers that formalization becomes excavation work.

## Solution

### Recognition trigger

A registry hits the formalization threshold when **the third unrelated consumer reads its values to make a behavior decision** (not just for observability — observability is a passive reader). The third *behavior-deciding* consumer is the moment to formalize.

### Formalization discipline (apply at the threshold)

1. **Typed enumeration** — if the registry is a free-form string, promote to a typed enum (`StrEnum` / `Enum`) so add/rename surfaces to grep and type-checker. The cost of conversion is small at threshold; large later.

2. **Documented consumer set** — at the registry's definition site, a comment listing every place a value is read for behavior decisions. The list is part of the contract; future-maintainers who add a value know to check the consumer set.

3. **Explicit default policy for new entries** — when a new value is added, what happens in each consumer? Three common policies:
   - **Fail-closed** (e.g., #1017's "unknown `task_type` defaults to `user_visible` profile") — new values get the safer behavior; explicit opt-out required to relax
   - **Fail-open** — new values get the minimal behavior; explicit opt-in required to enforce
   - **Compile-error** — new values must be classified in every consumer at type-check time (only works with exhaustive pattern matching)

   The policy choice depends on the registry's stakes. Default to fail-closed for safety-relevant registries.

4. **Register-time validation** (optional but valuable) — if any consumer registers special-case behavior for specific values, that registration co-locates with the consumer's definition. Future-maintainers can grep for the value and see all special cases without crawling through every consumer's logic.

### What this is NOT

- **Not a discipline for one-off enums.** A single-consumer enum doesn't need this; the pattern applies only when reuse has crossed the threshold.
- **Not a prohibition on growing registries.** Registries growing is healthy when the underlying concept is shared. The pattern says: name the moment it stops being a single-purpose annotation and starts being a taxonomy.
- **Not Methodology-29 itself.** This is a *methodology-29 instance applied to registries* (per CIO co-sign). Methodology-29 covers code-shape pattern formation; this pattern covers a specific category — registries-as-taxonomies — where the formation discipline differs because the artifact is data, not code.

## Architectural reasoning

Three structural properties make this pattern load-bearing:

1. **Behavior decisions on string values are silent.** A consumer that does `if task_type == "conversation": ...` doesn't fail when a new task_type is added; it just doesn't match. The new task_type takes whatever fall-through behavior the consumer has. If that's "do nothing," the new feature ships broken. If it's "default to behavior X," the new feature ships with X. Either way, the consumer's maintainer wasn't consulted.

2. **Multiple consumers create multiple-decision surface.** A registry with three behavior-deciding consumers has, at minimum, three places where adding a value changes behavior. Without governance, the value-adder needs to verify all three; with governance, the consumer set is documented and the default policy specifies what happens.

3. **Cost of formalization is monotone with consumer count.** At one consumer: trivial. At three consumers: easy to do, requires touching three call sites. At ten consumers: hard, requires understanding all ten + their interaction. The third-consumer threshold isn't arbitrary; it's the last point at which formalization is still cheap.

## Forces / when to apply

**Apply at threshold (third meaningful consumer arrives)**:
- Promote the annotation to a typed enum
- Document the consumer set at the definition site
- Decide and document the default policy for new entries
- Optionally add register-time validation if consumers special-case values

**Apply during code review when**:
- A code change adds a new consumer of an existing annotation; check whether that consumer would push the total past the threshold
- A code change adds a new value to a multi-consumer annotation; verify the value's behavior in every consumer per the documented set
- A code change is creating a new annotation that semantically overlaps with an existing one; consider whether to merge rather than parallel-author (Pattern-063 adjacent concern)

**Don't apply when**:
- The registry has one or two consumers (premature formalization; let it grow)
- The "registry" is data, not behavior-driving (e.g., a config table; no need for the recognition trigger)
- The consumers are all observability/telemetry (passive readers don't drive behavior; no decision surface)

## Code references (reference instance: `task_type`)

The reference instance — `task_type` in PM's `LLMClient` — became the canonical example after #1017 made it three-consumer:

`services/llm/clients.py:complete` — original single-consumer (model config dispatch):
```python
async def complete(self, task_type: str, prompt: str, ...) -> str:
    task_config = MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])
    # ... per-task-type model resolution
```

`services/ethics/output_filter.py:_PROFILE_REGISTRY` — #1017 third consumer (behavior dispatch):
```python
_PROFILE_REGISTRY: Dict[str, str] = {
    "conversation": Profile.USER_VISIBLE,
    "question_answering": Profile.USER_VISIBLE,
    # ... 10 user_visible task_types
    "intent_classification": Profile.INTERNAL,
    "general": Profile.MIXED,
}

def profile_for(task_type: str) -> str:
    """Return the filter profile for a task_type, defaulting to user_visible.

    Unknown task_types fall back to `user_visible` (fail-closed default per
    Architect Q6 ratification — new task_types must opt out of filtering
    explicitly, not opt in).
    """
    profile = _PROFILE_REGISTRY.get(task_type, Profile.USER_VISIBLE)
    ...
```

ADR-061 v1.1 amendment (2026-05-15) memorializes the recognition:

> *"Profile dispatch via `task_type`: the existing `task_type` parameter (already required at every `LLMClient.complete()` call site) drives filter-profile selection. ... Unknown task types default to `user_visible` (fail-closed)."*

What's NOT yet done that the pattern prescribes:
- `task_type` is still a free-form `str` parameter, not a typed enum. Conversion is the natural next step but wasn't in #1017 Phase 2 scope.
- Consumer set is documented in this pattern entry but not yet at the definition site (`services/llm/clients.py:complete`). Comment-level documentation co-located with the function signature is the right place.

These are explicit follow-ups when the registry advances (e.g., a fourth consumer lands per the Proven-promotion criterion).

## Anti-pattern recognition

Code-review signals that this pattern should be applied or is being violated:

- A `str` parameter or field on a method/model that multiple unrelated places `==`-compare for behavior decisions
- An enum with 8+ values where adding a value has no clear consumer-update checklist
- An `if/elif` dispatcher on a string annotation with no `else: raise UnknownValueError`-style fail-closed branch
- A new feature that adds a value to a shared annotation without updating any documentation or consumer
- Two parallel annotations (`category` and `kind` or similar) where one would naturally subsume the other if it weren't for the formalization cost

Healthy signals:
- Multi-consumer typed enums with documented consumer sets
- Explicit default-policy comments in the dispatch function
- Tests that exercise the unknown-value path (fail-closed verified)
- Code review comments that flag "this is the third consumer; should we formalize?"

## Relationship to other patterns

- **Methodology-29 (Pattern Formation via Successful Imitation)** — this pattern's parent framing. Methodology-29 covers bottom-up pattern formation in code shapes; Pattern-072 applies the same framing to a specific category (registries-as-taxonomies) where the formation discipline differs.
- **Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene)** — sibling-class instance. Both Pattern-070 and Pattern-072 are filings under the methodology-29 frame; Pattern-070 covers a code-shape (background jobs), Pattern-072 covers a data-shape (registries).
- **Pattern-063 (Parallel-Authoring Drift)** — adjacent. When parallel authors create two annotations that should be one, Pattern-063 names the drift; Pattern-072 names what to do once the convergence is recognized (formalize as a single taxonomy with documented consumers).
- **ADR-061 v1.1 amendment** — canonical reference implementation surface; `task_type` registry's third-consumer promotion via #1017 output-filter profile dispatch.

## Promotion criteria

**To Proven**:
- A fourth meaningful consumer adds a behavior decision keyed on `task_type` (or another registry covered by this pattern's framing) AND adopts the formalization discipline without rediscovery
- Candidate fourth consumer: the e2e-suite probe registry per Architect's e2e-suite design proposal (May 15) — *"the probe registry is the same shape — a catalog of typed entries dispatched at consumption time"*

**Promotion-blocking signals**:
- A fourth consumer lands without typed enum / documented consumer set / explicit default policy — suggests the pattern's formalization discipline isn't actually adopted in practice
- The three-consumer threshold proves operationally wrong (premature: registries with 3 consumers turn out fine without formalization; or late: registries hit failure modes at 2 consumers because the failure depends on consumer asymmetry, not count)

## Cross-references

- Lead Dev methodology memo to CIO 2026-05-15 (`mailboxes/cio/inbox/memo-lead-to-cio-cc-arch-1017-methodology-notes-2026-05-15.md`) — original candidate filing
- CIO disposition 2026-05-15 (`mailboxes/lead/read/memo-cio-to-lead-cc-arch-ceo-1017-pattern-candidates-disposition-2026-05-15.md`) — slot allocation + Emerging status + methodology-29-instance-applied-to-registries framing
- Architect Phase 1 ratification 2026-05-15 (`mailboxes/lead/read/memo-arch-to-lead-cc-cxo-ceo-1017-phase-1-ratification-2026-05-15.md`) — original observation: *"the `task_type` registry is now operating as a load-bearing surface taxonomy"*
- Architect e2e-suite design proposal 2026-05-15 (`mailboxes/lead/read/memo-arch-to-ceo-cc-lead-ppm-cxo-cio-host-exec-pa-e2e-suite-design-proposal-2026-05-15.md`) — fourth-consumer candidate observation
- ADR-061 v1.1 amendment (`docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`) — reference implementation surface; §"Amendment 2026-05-15" → §"OutputFilter architecture / Profile dispatch via `task_type`"
- #1004 (semantic boundary detector) — second meaningful consumer of `task_type`
- #1017 (OUTPUT-CONTENT-FILTER) — third meaningful consumer; threshold trigger
- Methodology-29 — parent methodology frame for bottom-up pattern formation
- Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene) — sibling-class instance; filed alongside this pattern
- Pattern-071 (Audit Logs as Attack Surface) — adjacent pattern filed via same methodology memo

— Lead Developer, 2026-05-15
