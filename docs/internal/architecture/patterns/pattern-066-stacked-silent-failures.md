# Pattern-066: Stacked Silent Failures

## Status

**Emerging** — Identified 2026-04-10 by CIO predecessor during M1 gate UAT debugging (named explicitly as "a new diagnostic pattern worth naming"). Filed under CIO self-approval authority 2026-05-09 per Pattern Sweep #1025 Phase 2C TRUE EMERGENCE finding (validated independently in Phase 2E meta-synthesis against P-041, P-042, P-043, P-045, P-060, P-062 — closest neighbor P-045 but mechanism distinct). PM concurrence on slot allocation recommended given recent slot-conflict precedent (Pattern-063 vs. predecessor Architect's Pattern-064 claim Apr 26-27). Promotion to Proven pending one trial-application cycle.

## Product Relevance

**Portable** — Any layered system (production stack, multi-agent coordination, methodology pipeline, audit cascade) where each layer has its own silent-failure mode will encounter this. Particularly load-bearing in:
- LLM application stacks where errors at one layer (API call, schema validation, parsing, business logic, presentation) can each fail silently into a generic fallback
- Multi-agent workflows where each agent's silent error masks the next agent's working state
- Methodology audits where each surface's drift hides the underlying drift at the next surface
- Test infrastructure where mocks at one layer hide failures at adjacent layers

## Context

When a system has multiple layers and each layer has its own silent-failure mode (returns a default, swallows an exception, falls back to a permissive path, or simply omits to act), failures can stack: an inner layer fails silently, the next layer treats the silence as success and operates on degraded data, and the failure mode propagates upward as a *different* kind of silence. By the time the surface layer behaves wrongly, the original cause is several layers deep — and each intervening layer needs to be peeled back individually to find it.

This pattern is **distinct from but related to**:
- **Pattern-045 (Green Tests, Red User)** — single-layer silent-failure: tests pass while user fails. Stacked Silent Failures is *multi-layer cascade* where each layer's silence enables the next.
- **Pattern-062 (Assembly Assumption)** — composition failure at integration seams between components. Stacked Silent Failures operates *within* a single execution path through layered abstractions.
- **Pattern-049 (Audit Cascade)** — investigation methodology that enumerates layers; useful as a diagnostic *response* to Stacked Silent Failures.
- **Pattern-060 (Cascade Investigation)** — root-cause investigation across multiple bugs sharing one cause; can co-occur with Stacked Silent Failures but addresses different concern (multiple bugs, one cause vs. one bug, multiple silent layers).

The CIO predecessor's Apr 10 naming explicitly carved Stacked Silent Failures out from these adjacent patterns — the multi-layer cascade structure with each layer's silence enabling the next is the load-bearing distinction.

## Problem

### The Failure Mode

A system has N layers, each with its own silent-failure mode:

```
Layer 5 (surface): user sees something wrong
  ↑
Layer 4: passed silent-default upward; layer-4 logic ran on degraded input
  ↑
Layer 3: returned silent fallback; layer-3 logic was unreachable
  ↑
Layer 2: caught and swallowed exception; emitted nothing
  ↑
Layer 1 (origin): the actual failure (auth issue, schema mismatch, network timeout, etc.)
```

Each layer is doing what it was designed to do — fall back gracefully, return a default, swallow non-critical exceptions. But the *composition* is failing: the user-visible symptom is several layers removed from the actual cause, and no single layer's logs surface the actual failure.

### Why It Happens

Three forces converge:

1. **Defensive design at every layer.** Each layer is built to be robust — handle null inputs, swallow exceptions, return safe defaults, never break the caller. This is good engineering at the layer level. It is dangerous engineering at the composition level.

2. **No protocol for upward signal.** Layers fail silently *because there's no agreed protocol for passing silent-failure signals upward*. Each layer makes its own local decision about what's "non-critical enough to swallow." The next layer up cannot distinguish "all fine" from "I silently degraded."

3. **Logs at each layer don't compose.** Each layer logs its own state, but the logs don't connect: layer-3 has no visibility into layer-2's swallowed exception; the surface debugger has no easy path to walk down through layers to find which one actually failed first.

### Concrete Example: M1 Gate UAT (April 10, 2026)

The CIO predecessor's Apr 10 naming arose from M1 gate UAT debugging. The user-visible symptom was a wrong canonical response. Investigation found:

- **Layer 5 (presentation)**: response template generated cleanly; no error
- **Layer 4 (canonical handler)**: handler executed; returned canonical response based on intent classification
- **Layer 3 (intent classifier)**: silently returned a default classification (intent unrecognized → fallback intent) because of...
- **Layer 2 (LLM provider)**: silently caught a provider auth error; returned None
- **Layer 1 (config)**: provider auth was missing because of a hardcoded provider assignment that didn't match the deployed config

Five layers between symptom and cause. Each layer's silent failure enabled the next layer to treat its degraded input as success. The fix required peeling each layer in turn, finding what was being silenced, and either making the silence visible OR fixing the layer-1 cause directly.

### Why Pattern-045 Doesn't Cover This

Pattern-045 (Green Tests, Red User) addresses *test infrastructure* failure: tests pass while user fails. The mechanism is a single-layer mismatch between test environment and production. Stacked Silent Failures is *runtime* failure across multiple layers in production itself, with no test/non-test distinction. Tests may or may not have caught it; the diagnostic shape is different.

Pattern-045 says: "tests pass, user fails — find the test-environment-vs-production mismatch."
Stacked Silent Failures says: "user fails, no error logs anywhere — peel back layer by layer, find which layer first silenced the original error."

## Solution

### The Iterative Peeling Protocol

When a Stacked Silent Failures cascade is suspected (user-visible symptom + no informative error in surface logs), apply iterative peeling:

**1. Inventory layers.** Map every layer the request/work passes through. Be explicit about silent-failure modes at each layer (does it swallow exceptions? Return defaults? Fall back?).

**2. Walk the cascade outward-to-inward.** Starting at the surface, ask at each layer: "Did this layer succeed *given* the input it received, or did it silently degrade?" The answer may require log inspection, debugger stepping, or instrumentation.

**3. Identify the first silent layer.** The "first" silent layer (closest to layer 1) is where the actual failure originated. Layers above it are *correctly handling* the silence; the silence is the problem.

**4. Decide between two fixes.** Either (a) fix the layer-1 cause directly, OR (b) make the silence visible (convert the swallowed exception into a logged warning, replace the silent default with an explicit error). Often both are needed.

**5. Document the cascade.** Record which layers silenced what. This documentation is the only protection against the same cascade recurring.

### Defensive-Design Discipline

The proactive mitigation:

- **Make silence loud.** Any layer that swallows an exception or falls back silently should log at warn-level minimum (don't `except: pass`; do `except as e: logger.warning(...)`).
- **Pass degradation signal upward.** If a layer is operating on degraded input, it should signal that fact to the next layer — at minimum via metadata / context flag.
- **Test the cascade explicitly.** Don't just test each layer in isolation; test that the cascade fails loudly when layer 1 fails. Inject layer-1 failures and verify the surface layer either produces a clear error OR produces a known degraded mode that's distinguishable from success.

### Audit-Cascade Counterpart (Pattern-049)

Pattern-049 (Audit Cascade) is the *investigation methodology* response to suspected Stacked Silent Failures. Where Stacked Silent Failures is the failure pattern, Audit Cascade is the diagnostic pattern. They co-occur frequently; cite both when documenting an investigation.

## Usage Guidelines

### When to Apply

- User-visible symptom but no informative error in surface logs
- Investigation requires walking through multiple layers
- Each layer's logs report "success" or are silent
- Suspected production failure mode where defensive coding is hiding the root cause
- Multi-agent workflows where one agent's failure doesn't surface to coordinators
- Methodology audits where surface-level metrics look fine but underlying drift is real

### When This Pattern Doesn't Apply

- Single-layer failures with clear error logs (Pattern-045 territory if test-related)
- Composition failures at layer seams (Pattern-062 territory)
- Multiple distinct bugs sharing a common cause but in different code paths (Pattern-060 territory)
- Failures where the cause is immediately visible in surface-layer logs

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---|---|---|
| `except: pass` at any layer | Silent swallowing creates the cascade-enabler | `except Exception as e: logger.warning("description", exc_info=True)` |
| Return generic defaults silently when input is degraded | Downstream layers can't distinguish degraded-mode from success | Return explicit "degraded" sentinel + log; force callers to check |
| Test each layer in isolation only | Cascade only manifests on composition; isolation tests miss it | Add layer-injection tests: inject layer-1 failure, assert surface-layer behavior is observable (loud error or known degraded mode) |
| Treat "no error logs" as "no error" | Silence may be the symptom, not the absence of symptom | If user-visible symptom + silent logs, suspect Stacked Silent Failures and start peeling |
| Try to fix the surface layer before identifying the first silent layer | Fixing surface symptom without finding cause means cascade recurs | Walk outward-to-inward; identify first silent layer; fix at the right depth |

## Related Patterns

- **Pattern-045 (Green Tests, Red User)**: single-layer silent-failure (test/prod mismatch)
- **Pattern-049 (Audit Cascade)**: investigation methodology — the diagnostic response to suspected Stacked Silent Failures
- **Pattern-060 (Cascade Investigation)**: multiple bugs / one cause; can co-occur but addresses different concern
- **Pattern-062 (Assembly Assumption)** + family (063 vocabulary, 064 extension, 065 institutional-knowledge): integration-seam failures vs. layered-cascade failures; sibling lens at composition layer
- **Pattern-054 (Honest Failure)**: the consumer-side discipline that complements layer-side make-silence-loud — tells the user what failed in human language

## Evolution

### Discovery (April 10, 2026)
M1 gate UAT debugging surfaced a 5-layer silent-failure cascade. CIO predecessor named the pattern explicitly during Apr 10 session as *"a new diagnostic pattern worth naming"* — distinct from Pattern-045 (single-layer silent failure), Pattern-062 (integration-seam failure), Pattern-060 (multi-bug single-cause).

### Operational Citation (April 14 – April 23, 2026)
Three independent surfaces during the window (per Pattern Sweep #1025 Phase 2C):
- Apr 14 omnibus session learning
- Apr 17 M1 audit (CIO predecessor)
- Apr 23 handoff watch-list

Pattern was operating as pre-canonical operational vocabulary across multiple agents.

### Filing (May 9, 2026)
Filed Emerging during Pattern Sweep #1025 Phase 2C TRUE EMERGENCE finding. Phase 2E meta-synthesis validated independently (FALSE POSITIVE TEST passed against P-041, P-042, P-043, P-045, P-060, P-062).

## Success Metrics

- **Cascade-detection latency**: time from user-visible symptom to first-silent-layer identification. Lower = better; trend over time = methodology working.
- **Number of layers peeled per cascade investigation**: averages tell us about system complexity; outliers tell us about defensive-design discipline.
- **`except: pass` count in services/**: should trend toward zero as the make-silence-loud discipline propagates. Periodic grep audit.
- **Layer-injection test coverage**: count of integration tests that explicitly verify cascade behavior when layer-1 fails.

## References

- **Origin instance** (Apr 10): CIO predecessor naming during M1 gate UAT debugging session
- **CIO M1 methodology audit** (`dev/2026/04/17/methodology-audit-2026-04-17.md`): predecessor's audit of Apr 17 — Stacked Silent Failures referenced
- **CIO predecessor handoff** (`dev/active/handoff-cio-chat-to-code-2026-04-23.md`): Section 4 watch-list
- **Pattern Sweep #1025 Phase 2C** (`dev/active/pattern-novelty-candidates.md`): TRUE EMERGENCE candidate TE-1
- **Pattern Sweep #1025 Phase 2E** (`dev/active/pattern-meta-synthesis.md`): independent CIO validation

---

*Pattern created: May 9, 2026*
*Origin: CIO predecessor naming during M1 gate UAT debugging Apr 10, 2026*
*Author: CIO (Code instance, formalizing predecessor's operational coinage)*
*Status: Emerging (CIO self-approval; PM concurrence on slot recommended)*
*Promotion criterion: one trial-application cycle where the pattern correctly diagnoses a multi-layer silent-failure cascade in operational work.*
