# Interface-Verification Done-Definition (Layer A) — #683

**Status**: CANONICAL (integrated 2026-06-02). Placement ratified by PM (2026-05-30): this is a **requirement on the Class B (sub-epic gate) review surface** of the PPM Review Gates 5-class taxonomy — not a sixth class. Preserves the taxonomy.

**Owners / inputs**:
- **CIO** — authored the methodology-30 grounding (the five-step Consumer-Trace gate below). Source draft: `dev/active/dod-layer-a-interface-verification-DRAFT-cio-2026-05-28.md`.
- **PPM** — integration owner; placed this into the completion-criteria process artifacts (Sub-Epic Gating Protocol in `m2-structure.md` + Class B note in the Review Gates norm).
- **Lead Dev** — *pending*: the operational-check shape (runtime assertion vs. integration test vs. smoke-call vs. documented manual trace), calibrated against the #1089 spec-thinko. The methodology specifies the *shape* of verification; the operational recipe is Lead Dev's.
- **CXO** — *pending*: grounding-review confirmation that the methodology-30 grounding holds (CXO co-originated methodology-30 with Architect).

**Pairs with Layer B** (experience-layer DoD: Colleague Test + MUX-doc conformance — CXO-owned, drafted separately). Layer A verifies the interface has its inputs reachable by a real consumer; Layer B verifies the user-facing surface meets its experience commitments. The two-layer split is the CXO disposition of 2026-05-28.

**Source #683**: "MUX-WIRE-DOD: Update Definition of Done to require interface verification" (deferred from #670 MUX-WIRE). Discovered during the MUX-WIRE epic — services implemented but not always wired to user-facing interfaces.

---

## The gate, in one sentence

A change that provides or depends on an interface — an API surface, a service contract, a data shape a consumer reads, a config a downstream step assumes — is **not Done until a Consumer-Trace (methodology-30) shows the interface's real behavior is reachable by an actual consumer**, not merely that the interface is declared, scaffolded, or shape-present upstream.

## What it guards against (the #1089 spec-thinko shape)

The failure this gate catches: a spec asserts *"the consumer has input X"* on the strength of X's declared shape or presence upstream, without verifying the consumer actually reaches X's real behavior at the call site. The assertion looks satisfied (the shape is there) but consumption was never verified.

This is the same failure shape as:
- **Architect's May 15 Surface-6 self-catch** (LLM-touch asserted from upstream context-shape; actual path was template dispatch) — the originating methodology-30 incident.
- **Pattern-064 (Extension Without Integration)** — alive scaffolding for a consumer relationship rather than alive behavior.
- **#1089 spec-thinko** — the concrete instance this DoD addition is calibrated against (Lead Dev to confirm the exact shape).
- **Architect's May 30 `_fallback_classify` production-orphan catch** — same family; strengthens the methodology-30 basis.

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

## How this attaches to the Class B (sub-epic gate) review surface

The PPM Review Gates 5-class taxonomy (CEO-approved May 10) routes review by class: PDR-adjacent / **sub-epic gate** / quality-threshold-affecting / integration-pattern-shifting / user-facing-experience. This DoD is a standing **requirement within the sub-epic-gate class (Class B)**: whenever a sub-epic gate closes and any of its acceptance criteria assert a consumer-relationship, the Consumer-Trace above is part of gate close. It composes with — does not replace — the per-sub-epic quality-threshold gates (Colleague Test) and the conceptual-integrity sign-off. See `m2-structure.md` §"Sub-Epic Gating Protocol" item 5.

## Source grounding

- methodology-30 (Consumer-Trace Verification): `docs/internal/development/methodology-core/methodology-30-CONSUMER-TRACE-VERIFICATION.md`
- CIO source draft: `dev/active/dod-layer-a-interface-verification-DRAFT-cio-2026-05-28.md`
- CXO two-layer disposition: `mailboxes/cio/read/memo-cxo-to-cio-cc-pm-ppm-duty-cycle-adoption-plus-683-disposition-2026-05-28.md`
- #1050 AC-marking convention (`[⏸]` for live-verification-pending); Pattern-045 (premature closure); Pattern-064 (extension without integration)
- PPM Review Gates 5-class taxonomy: `docs/internal/planning/roadmap/roadmap.md` §"Discipline Norms"

---

*Layer A authored by CIO (methodology-30 grounding) 2026-05-28; integrated to canonical by PPM 2026-06-02 per PM-ratified Class B placement (2026-05-30). Lead Dev operational-shape recipe + CXO grounding-review are pending refinements — flagged, not blocking the placement.*
