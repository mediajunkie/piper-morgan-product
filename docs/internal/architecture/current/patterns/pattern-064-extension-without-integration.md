# Pattern-064: Extension Without Integration

## Status

**Proven** — Promoted from Emerging May 8, 2026 (CIO promotion authority per `methodology-audit-policy-updates-2026-03-16.md`; Architect concurrence implicit through May 4 review's diagnostic use). Trial-application evidence: Architect May 4 architectural-soundness review identified two new in-the-wild instances using pattern's exact "alive scaffolding" framing — (1) `KnowledgeGraphService` legacy `BoundaryEnforcer` import + permanently-None argument + if-guarded dead paths (canonical instance per Architect's framing); (2) `boundary_enforcer_refactored.py:343-358` commented-out adaptive-learn TODO with self-acknowledged dead allocation. Pattern operationally diagnostic at population scale, not just origin. Originally sketched in predecessor Architect's Apr 25 handoff; formalized 2026-04-28 by Chief Architect alongside ADR-061. Sibling sub-pattern to Pattern-063 (Parallel-Authoring Drift, CIO Apr 26). Promotion analysis at `dev/active/cio-pattern-promotion-analysis-2026-05-08.md`.

## Product Relevance

**Process-only** — This is an architectural-development discipline, not a user-facing feature. Piper's users will not encounter this pattern; teams building Piper-like systems will.

## Context

When an existing infrastructure component is *extended* to a new context (a new entry point, a new caller, a new use case) without being *integrated* with that context's realistic input shape, the extension can pass all tests, get fully wired, and ship — while still failing on the actual input the new context produces.

The component's own unit tests pass because they use inputs that fit the component's original assumptions. The new context's tests pass because they exercise the wiring (does the call go through?), not the semantics (does the component handle the input correctly?). The integration is mechanical-but-not-semantic: the call site is wired, but the component's effective behavior on the new input shape was never verified.

This pattern was sharpened during the Apr 25–27 #1002/#1003/#1004 cluster, which produced both the canonical reference instance and the conceptual reframe (detection-effectiveness vs. routing-order).

### Relationship to Pattern-062 (Assembly Assumption)

Pattern-062 is the general parent: when components work in isolation but compose incompletely, the failure is at the integration seam. Pattern-064 is the specific sub-instance where **the seam is between an existing component and a new context that calls it**. The component is unchanged; the context is new; the integration is the seam.

Pattern-062 covers any composition failure (parallel features at sprint scale, omnibus synthesis at documentation scale, multi-step LLM workflows at orchestration scale). Pattern-064 specifically covers extension-into-new-context failures. The other sibling sub-pattern, Pattern-063 (Parallel-Authoring Drift, CIO), covers parallel-authoring failures of shared resources.

| | Pattern-062 (parent) | Pattern-063 (CIO) | Pattern-064 (this) |
|---|---|---|---|
| **Failure shape** | Composition is incomplete | Parallel authoring of shared resource diverges | Extension to new context misses input shape |
| **Trigger** | Multiple components composed | Two authors extend same canonical reference | Existing component extended to new caller |
| **Diagnostic question** | What integration seams were never specified? | If the two authors scored each other's work, would they get the same answer? | Was the component's behavior verified against the new context's actual input shape? |
| **Reference instance** | M0 sprint 9 integration gaps (Feb 2026) | Phase E rubric C-axis drift (Apr 26) | BoundaryEnforcer #197 substring-detector recall on naturally-phrased input (Apr 25–26) |

## Problem

### The Failure Mode

```
Existing component (Comp): [designed for context A] → [tested ✅ in context A] → "works"

New extension: Comp called from context B
  → [wiring ✅: the call site is connected]
  → [Comp's tests still pass: same inputs as before]
  → [context B's tests pass: the call goes through]
  → [activation flag exists: the gate is present]
  → "extension complete"

Reality: context B produces input shape Comp was not designed for
  → Comp returns confidently-wrong output (often: "no problem detected")
  → Audit envelope shows clean activation
  → User-facing behavior unchanged, because Comp didn't actually engage
```

The trap is that *every observable signal at the architecture's surface looks correct*. The component runs. The flag activates. The audit envelope populates correctly when the component triggers. None of these signals are wrong — they're just measuring the wrong thing. The signal that's missing is *did the component's effective behavior change for this new context's actual input?*

### Why It Happens

Three forces converge:

1. **Component reuse incentives favor extension over rewriting.** When a component already exists for context A and a new context B needs similar capability, extending the component is cheaper than building a new one. The architectural decision is correct in principle. The execution risk is in the integration depth.

2. **Test scoping inherits component boundaries.** When Comp gets called from context B, the natural test scope is "does context B call Comp correctly?" — not "does Comp produce correct output for context B's input shape?" The latter requires *adversarial input from context B* in the test suite, which requires *specifying what context B's adversarial input looks like*, which is exactly the work that wasn't done.

3. **The activation gate gives false confidence.** Once the new wiring exists and the activation flag is present, the surface signal is "the system is ready to use Comp for context B." If activation is gated on cleanly-implemented infrastructure (which it should be), the gate readiness is interpreted as integration readiness. They are not the same.

### Concrete Example: BoundaryEnforcer #197 Phase 2D

The BoundaryEnforcer was originally designed for **content-filter-style use** — checking specific user inputs against pattern lists for harassment, professional boundaries, inappropriate content. Pattern matching against literal trigger words was the design.

In #197 Phase 2D, BoundaryEnforcer was extended to a **universal entry point** at `IntentService._process_intent_internal` — every user message routes through it before classification. This is a new context: not specific user-flagged content, but the full population of natural-language input.

The extension was correctly executed at every observable layer:
- The call site was wired (`services/intent/intent_service.py:627`)
- The activation flag was added (`ENABLE_ETHICS_ENFORCEMENT`)
- The audit envelope was structured (`BoundaryDecision` fields)
- Unit tests passed (using inputs that quoted trigger words)
- The redirect_context handoff was designed (#992 Phase A)

What was *not* done: verify the BoundaryEnforcer's effective behavior against the new context's actual input shape. Naturally-phrased natural-language input does not contain the literal trigger words the substring detector matches against. The detector ran; it didn't detect. The gate was structurally correct; the integration was semantically incomplete.

The failure surfaced when the activation gate was tested in #992 Phase E (Apr 25, 2026): the audit envelope was empty for canonical harassment scenarios. A diagnostic comparison run (#1003, Apr 26) confirmed `flag=true` and `flag=false` produced indistinguishable output — the flag was observably inert because the detector wasn't engaging on the new context's input shape.

### Adjacent Manifestations

The same pattern recurs at other layers in the codebase (per #1016 Phase 1 codebase review, Apr 27):

- **`get_selected_client` phantom import** (`services/intent/intent_service.py:8032`): the import statement extends the file's surface to call a function that doesn't exist; wrapped in try/except, so the call site is wired but the integration with the actual `services.llm.clients` module was never verified.
- **`adaptive_boundary_system` import in `staging_health.py:858+`**: imports a non-existent name (actual singleton: `adaptive_boundaries`). Health check extended to monitor adaptive learning; integration with the actual module never verified.
- **`UserHistoryService.get_history_summary()` call in `context_assembler.py:341`**: extends context-assembly to consume long-term memory; the called method does not exist.
- **`GreetingContextService` in `services/memory/greeting_context.py`**: fully implemented + tested + exported; never instantiated. Extension *of the codebase* to support adaptive greetings; integration *into the request path* never completed.

The shared shape: surface integration (import statements, wiring, structure) without semantic integration (does the new caller actually exercise the component correctly?).

## Solution

### The Integration Pass

After a component is extended to a new context, perform a dedicated **integration pass** — a focused session whose sole purpose is verifying that the component's effective behavior is correct for the new context's actual input shape. This is distinct from:

- **Wiring verification** (does the call go through?) — necessary but not sufficient
- **Component unit testing** (does the component handle its original inputs?) — necessary but not sufficient
- **Activation testing** (does the flag turn the path on?) — necessary but not sufficient

The integration pass produces a *probe set*: representative samples of the new context's actual input shape, run through the component, with assertions on the component's effective behavior (not just wiring success).

### Integration Pass Protocol

**1. Specify the new context's input shape.** Before testing, characterize what realistic input from context B looks like. For natural-language input contexts, this means: write down the kinds of phrasings real users will produce. Do not rely on the component's existing test inputs.

**2. Run the component against probe inputs.** Use the probe set to exercise the component, capturing outputs.

**3. Assert effective behavior, not wiring.** The probe assertions check whether the component *did the thing* (detected the violation, classified the intent, produced the correct output) — not whether the call went through.

**4. If the probe set fails, the integration is incomplete.** Wiring success is not a substitute for behavior success. The fix may require changes to the component (new detection layer), changes to the prompt/configuration (better instruction), or changes to the architecture (acknowledge that the component cannot handle this context's input shape and add a fallback).

**5. Annotate the audit envelope to surface the integration shape.** When the component runs, the audit envelope should record *which* path engaged (literal-trigger vs. semantic vs. floor-implicit) so operators can see whether the component is doing its work or whether a fallback is.

### Specific Application: ADR-061 Two-Layer Detector

The #1004 work (April 26–27) is the canonical remediation of this pattern's reference instance:

- Probe set design: 15+ probes across 5 BoundaryType categories with naturally-phrased violations + 5 false-positive controls (per CXO's prompt-body draft, Apr 26)
- Two-layer detector: literal-trigger fast-path (preserves the original component's correct cases) + semantic LLM detector (handles the new context's input shape) + floor backstop (handles input that bypasses both)
- Audit envelope `detector` field: records which path engaged
- Run-1 (16/20) → prompt v0.2 → run-2 (18/20) → ship: empirical validation of effective behavior, not just wiring

This is the integration pass executed retrospectively, two months after the original extension shipped. The cost of the late integration was measurable (months of theatrical activation), but the methodological output was a probe-set discipline now reusable for future extensions.

## Anti-Pattern Indicators

The following signals suggest Pattern-064 may be present:

- **A component is wired into a new context but the new context's input shape was never enumerated in writing.** ("It's the same component; we're just calling it from a new place.")
- **Activation testing checks "does the flag turn the path on" rather than "does the component produce correct output for real input."**
- **Audit envelopes are structured for the component's original use case, not for the new context's failure modes.** (e.g., the audit envelope captures "no violation detected" identically whether the detector ran-and-correctly-passed or ran-and-missed-the-violation.)
- **Tests pass and the system "looks right," but operators report no observable behavior change after activation.**
- **A diagnostic comparison run (`flag=true` vs. `flag=false`) shows indistinguishable behavior on representative input.**

The last is the strongest signal: when activation has no observable effect, the most likely explanation is that the activated component isn't engaging on the input it's purportedly handling.

## Cross-References

- **Pattern-062 (Assembly Assumption)**: parent pattern; this is a specific sub-instance
- **Pattern-063 (Parallel-Authoring Drift, CIO)**: sibling sub-pattern of 062; different failure mechanism
- **Pattern-045 (Green Tests, Red User)**: related anti-pattern; Pattern-064 is a specific structural cause when 045 manifests at the infrastructure layer
- **ADR-060 (Floor-First Routing)**: adjacent decision; the floor's de-facto safe-fallback role addresses input shapes the BoundaryEnforcer didn't anticipate
- **ADR-061 (LLM-Touch Boundary Enforcement)**: the architectural remediation for this pattern's reference instance; the four-element principle (permissive input shape / schema validation at consumption / safe-fallback path / audit envelope) is the design discipline that prevents recurrence

## References

- Predecessor Architect handoff (Apr 25, 2026), Section 1: original sketch — *"Pattern-063 (Extension Without Integration): Proposed by the predecessor, still not formalized. Sub-pattern of 062. Six bugs from same cause. Worth formalizing when there's bandwidth."* (Slot allocation later resolved: Pattern-063 = CIO's Parallel-Authoring Drift; this becomes Pattern-064.)
- Architect Apr 26 #1002 scoping memo (`mailboxes/arch/sent/memo-arch-to-lead-cc-ppm-pm-cxo-pa-exec-1002-scoping-2026-04-26.md`): the reframe from routing-order to detection-effectiveness
- Architect Apr 27 batch-3 codebase review findings (`dev/2026/04/27/codebase-review-batch-3-findings-2026-04-27.md`): cross-cutting Insight 1 surfacing the same shape across surfaces
- Architect Apr 27 batch-4 codebase review findings (`dev/2026/04/27/codebase-review-batch-4-findings-2026-04-27.md`): Insight 5 (phantom-method-call pattern) and Insight 7 ("alive scaffolding") as additional manifestations
- CIO Apr 27 Pattern-063 slot allocation memo (`mailboxes/arch/inbox/memo-cio-to-arch-cxo-cc-pm-ppm-lead-pa-exec-pattern-063-slot-and-rule-2026-04-27.md`): the slot-allocation that produced Pattern-064 numbering

---

*Formalized: 2026-04-28 by Chief Architect (Code instance). Predecessor's Apr 25 sketch was the seed; the #1002–#1004 cluster produced the canonical reference instance and the structural reframe.*
