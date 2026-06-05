# DRAFT — #683 Layer A: Interface-Verification Done-Definition (methodology-30-grounded)

**Status**: DRAFT for PPM integration. Authored by CIO (methodology-30 grounding) per the #683 two-layer split (CXO disposition 2026-05-28). PPM owns placement into the completion-criteria process artifacts (Review Gates 5-class taxonomy + M2d completion criteria). Lead Dev provides the operational-check shape (#1089 spec-thinko). CXO reviews the methodology-30 grounding (co-originated).

**Pairs with**: Layer B (experience-layer DoD: Colleague Test + MUX-doc conformance) — CXO-owned, drafted separately. Layer A verifies the interface has its inputs; Layer B verifies the user-facing surface meets its experience commitments.

---

## The gate, in one sentence

A change that provides or depends on an interface — an API surface, a service contract, a data shape a consumer reads, a config a downstream step assumes — is **not Done until a Consumer-Trace (methodology-30) shows the interface's real behavior is reachable by an actual consumer**, not merely that the interface is declared, scaffolded, or shape-present upstream.

## What it guards against (the #1089 spec-thinko shape)

The failure this gate catches: a spec asserts *"the consumer has input X"* on the strength of X's declared shape or presence upstream, without verifying the consumer actually reaches X's real behavior at the call site. The assertion looks satisfied (the shape is there) but consumption was never verified.

This is the same failure shape as:
- **Architect's May 15 Surface-6 self-catch** (LLM-touch asserted from upstream context-shape; actual path was template dispatch) — the originating methodology-30 incident.
- **Pattern-064 (Extension Without Integration)** — alive scaffolding for a consumer relationship rather than alive behavior.
- **#1089 spec-thinko** — the concrete instance this DoD addition is calibrated against (Lead Dev to confirm the exact shape).

## The completion gate (parameterized to the work's interface)

For any acceptance criterion of the form *"consumer C uses / consumes / touches interface I"*:

1. **Locate C's consumer site for I in code** — where C allegedly consumes I, not where the spec asserts it does.
2. **Trace C's call chain to I's real behavior** — imports, calls, injection resolve to the actual I, not a mock, fallback, or sibling abstraction.
3. **Verify I's real behavior is invoked** at that site — LLM call reached (not template dispatch / cached response); network call made (not a stub); method body runs (not a guard short-circuit).
4. **Confirm an observable effect** — log line, response, mutation, side-effect that proves consumption happened.
5. **Attach the trace** (file paths, function names, log lines) to the issue as the verification artifact. The trace is the proof; the prose claim is not.

## Gate disposition (how it interacts with AC marking)

- **PASS** — trace reaches steps 3–4 with an observable effect → the AC may be marked `[x]`.
- **FAIL** — trace bottoms out at *"upstream shape exists"*, or any segment is missing / mocked-without-real-behavior / asserted-but-not-shown → the AC stays `[ ]` or `[⏸]` (per the #1050 convention). **Not** `[x]`-with-a-deferred-parenthetical — that's the premature-closure failure mode (Pattern-045) the gate exists to prevent.

## Scope — when this gate applies (mirrors methodology-30 §"when to apply")

**Applies when** the acceptance criterion asserts a consumer-relationship (C uses/touches/consumes I): API consumption, service injection, doc-to-code-path claims, config a downstream step reads.

**Does NOT apply when**:
- The claim is feature-presence without a consumer-relationship shape (*"feature X exists"* — just locate the code; no trace needed).
- The verification is about I's behavior independent of who consumes it (service-level tests of I that don't care about the caller).
- Consumption is mechanically proven by types (a generated/well-typed SDK call where the type system makes the trace implicit).

## Integration notes (handing off)

- **PPM (integration owner)**: place this as an interface-verification gate within the Review Gates 5-class taxonomy (likely a requirement on the integration gate, or a sixth cross-cutting class — PPM's call) + an M2d-style completion-criteria entry. Flag if placement surfaces a taxonomy question.
- **Lead Dev (engineering input)**: define the operational shape of the check — is it a runtime assertion, an integration test, a smoke-call, or a manual documented trace? Calibrate against #1089. The methodology specifies the *shape* of verification (the five-step trace); the operational recipe is yours.
- **CXO (grounding review)**: confirm the methodology-30 grounding holds (you co-originated it with Architect).

## Source grounding

- methodology-30 (Consumer-Trace Verification): `docs/internal/development/methodology-core/methodology-30-CONSUMER-TRACE-VERIFICATION.md`
- CXO two-layer disposition: `mailboxes/cio/read/memo-cxo-to-cio-cc-pm-ppm-duty-cycle-adoption-plus-683-disposition-2026-05-28.md`
- #1050 AC-marking convention (`[⏸]` for live-verification-pending); Pattern-045 (premature closure); Pattern-064 (extension without integration)

---

*Drafted by CIO Vehicle 2, 2026-05-28 ~9:40 AM PDT (autonomous cycle, Task-Loop). Handed to PPM for completion-criteria integration; gated PPM Layer A work now unblocked.*
