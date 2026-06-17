# Consumer-Trace Verification

## Overview

**Consumer-Trace Verification** is the discipline that requires, for any claim about consumption — *"feature X uses LLM call Y,"* *"system Z makes an API touch at step W,"* *"this code path consumes service S"* — a navigable trace from the claim to the actual consumer call site, then to the underlying behavior, before the claim is treated as verified. The discipline:

1. **The claim names a consumer relationship** (consumer → consumed; usually feature → service, or doc → code-path, or architecture-statement → call-site)
2. **The trace must navigate** from claim → consumer site → underlying behavior. Upstream context shape alone is not sufficient evidence of consumption.
3. **Verification fails if any segment of the trace is missing, asserted-but-not-shown, or mocked-without-the-real-behavior**. Failed traces surface stale claims, dead consumer sites, mock-tested-not-real-tested behavior, or assertion-from-shape errors.
4. **Successful traces become the canonical verification artifact** — the trace itself is what proves the claim, not the claim's prose form.

The discipline is general — applies to any claim about consumption, not just LLM-touch claims that originally motivated it. Same shape as Pattern-073 (Documentation-Asserted-Behavior Drift) but at the consumer-trace surface: documentation asserting consumption that doesn't show up in code.

## Why This Methodology

### The Architect's May 15, 2026 Surface 6 self-catch

The discipline was named explicitly in Architect's May 15 memo: *"LLM-touch claims require consumer trace to actual LLM call, not just upstream context-shape inspection."*

The originating incident: Architect made an assertion that a feature was LLM-touch based on inspecting the upstream context shape (the data being passed in). The assumption was *"upstream context-shape exists → must be LLM-touch."* The actual code path used template dispatch, not an LLM call. The assertion propagated through cohort traffic for ~12 hours before Lead Dev's pre-verification rigor caught it. Trigger to file a methodology entry: the self-catch surfaced the discipline by failure.

CXO endorsed routing the methodology note to CIO at Architect's cadence. CIO ratified Option A (lightweight methodology corpus entry, slot 30) on the May 15 disposition memo. This entry is the filing.

### Why this is distinct from Pattern-073

Pattern-073 (Documentation-Asserted-Behavior Drift) is the architecture-pattern view: documentation makes claims about behavior that doesn't exist in code anymore. Consumer-Trace Verification is the **discipline that catches one class of Pattern-073 instance** at filing time — the consumer-trace claim — before it propagates.

| Pattern-073 | Consumer-Trace Verification |
|---|---|
| Architectural pattern (catalog entry) | Methodology discipline (corpus entry) |
| Names a failure shape | Names a verification procedure |
| Filed when ≥3 instances surface | Applied as a check before claims propagate |
| Resolution: clean up the misleading surface | Resolution: trace the claim or don't make it |

The two compose: Consumer-Trace Verification at filing time prevents Pattern-073 instances at the consumer-trace surface; Pattern-073 catches the residual instances that slip through.

## The verification procedure

For any claim of the form *"X consumes Y"* / *"X uses Y"* / *"X touches Y"*:

1. **Locate the claim's consumer site** in code. Where in `X`'s implementation does it allegedly consume `Y`?
2. **Verify the call chain** from the consumer site to `Y`'s real behavior. Imports, function calls, service injection, etc. should resolve to the actual `Y` and not to a mock, a fallback, or a sibling abstraction.
3. **Verify `Y`'s real behavior is invoked**. If `Y` is an LLM service, verify the LLM call site is reached (not a template dispatch, not a cached response). If `Y` is an API, verify the network call (not a stubbed response). If `Y` is a method, verify the method body runs (not a guard that short-circuits).
4. **Confirm the consumption produces observable effects**. The trace should end in a verifiable artifact: log line, response, mutation, side-effect — something that proves consumption happened.
5. **Document the trace as the verification artifact**. The trace itself becomes the canonical proof of the claim. Future questioners navigate the trace, not the prose.

A trace that bottoms out at *"upstream context-shape exists"* without reaching step 3 fails the verification. That's the Architect May 15 incident shape.

## When to apply this framing

### Apply this framing when

- Authoring or reviewing architecture documentation that claims "X uses LLM service Y" or any consumer-touches-service relationship.
- Conducting `audit-cascade` or `narrative-verification` skill passes on artifacts that make consumer-relationship claims.
- Reviewing CXO UX descriptions, Architect ADRs, Lead Dev epic-status memos, or any role artifact that asserts LLM-touch or consumption relationships.
- Designing Outcomes-API or Multi-Agent-API rubrics — the rubric's grader needs to satisfy consumer-trace, not just shape-match upstream context.
- Investigating Pattern-073 instances where the misleading surface is a consumer claim.

### This framing does not apply when

- The claim is about presence/absence of a feature without a consumer-relationship shape (e.g., "feature X exists" — no consumer-trace needed; just locate the code).
- The verification is about behavior independent of who consumes it (e.g., service-level tests of `Y` that don't care who's calling).
- The trace is purely declarative and well-typed (e.g., a generated SDK call where types prove consumption mechanically; trace is implicit in the type system).

## What it predicts

If Consumer-Trace Verification is applied correctly, the following downstream signals should appear:

- **Consumer-relationship claims in cohort traffic become harder to assert incorrectly** — the discipline is now an explicit check that authors apply before publishing, not a post-hoc catch.
- **Pattern-073 instance count at the consumer-trace surface drops** — instances that would have surfaced via Pattern-073 are now caught at the discipline boundary instead.
- **Verification artifacts grow richer** — instead of prose claims, artifacts include traces (file paths, function names, log lines) that downstream readers can navigate.
- **Outcomes-style rubrics that involve consumer-trace claims get more reliable graders** — the rubric specifies the trace expectation, not just the shape expectation.
- **Cross-agent challenges to consumer-trace claims become routine** — *"trace the claim"* becomes a normal review request, not an adversarial one. Methodology-29 (Pattern Formation via Successful Imitation) predicts cohort adoption if the discipline does the work it promises.

## Relationship to Anthropic's Outcomes API (May 2026 productization)

Outcomes packages the rubric+grader+retry verification pattern as an API. Consumer-Trace Verification is the **discipline-of-use** that distinguishes well-grounded Outcomes rubrics from shape-matching theatre:

- A rubric that asks "does feature X have an LLM call?" can be graded by shape (input context exists) or by consumer-trace (call site reached). Shape-matching satisfies the rubric without verifying consumption; consumer-trace requires the actual trace.
- An Outcomes rubric written with consumer-trace discipline specifies the expected trace as part of the success criterion. Failed traces fail the rubric. This is the higher-value rubric shape.
- DIY consumer-trace verification (this discipline) gives us the calibration to author trace-aware Outcomes rubrics intelligently when we adopt the platform productization.

Consumer-Trace is methodology-corpus material; Outcomes is platform-substrate. The discipline survives the platform productization (per methodology-31 "Append-Only Autonomous-Cycle Architecture"'s philosophical kin: disciplines outlast runtimes).

## Cross-references

- **Architect's May 15 memo naming the discipline**: `mailboxes/cio/read/memo-arch-to-cio-cc-lead-cxo-ceo-ppm-exec-pa-pattern-064-evolution-landed-plus-consumer-trace-methodology-note-2026-05-15.md` (originating framing + Surface 6 self-catch)
- **CXO endorsement memo routing to CIO**: `mailboxes/cio/read/memo-cxo-to-arch-cc-lead-cio-ceo-1017-probe-v1.1-ack-surface-6-correction-noted-2026-05-15.md`
- **Pattern-073 (Documentation-Asserted-Behavior Drift)**: the architecture-pattern catalog entry this methodology composes with at the consumer-trace surface (filed 2026-05-16; promoted to Proven 2026-05-18 commit `935da08b3`)
- **Pattern-064 (Extension Without Integration)**: the consumer-trace discipline's failure shape (asserting LLM-touch from upstream context-shape) is a Pattern-064 sibling — alive scaffolding for a consumer relationship rather than alive scaffolding for behavior
- **methodology-07 (Verification First)**: the foundational discipline; Consumer-Trace is a specialization for consumer-relationship claims
- **methodology-15 (Testing & Validation)**: real-LLM-not-mock testing is the consumer-trace counterpart in the test-suite layer
- **methodology-17 (Cross-Validation Protocol)**: multi-agent cross-validation often surfaces consumer-trace failures (one agent's claim, another agent's trace check)
- **methodology-29 (Pattern Formation via Successful Imitation)**: predicts cohort adoption of Consumer-Trace once the discipline shows it does what it promises
- **CIO Anthropic Outcomes disposition memo (today)**: `mailboxes/cio/sent/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-ppm-anthropic-outcomes-platform-productization-disposition-2026-05-18.md` (frames Consumer-Trace as discipline-of-use for Outcomes adoption)

## Notes on this entry's authority + scope

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md`, ratifying Architect's Option A disposition request from May 15. The discipline is general (any consumer-relationship claim, not LLM-specific despite the originating incident); the entry's title intentionally drops "LLM" to signal the breadth.

The procedure (the five-step trace verification) is specified at methodology-corpus altitude — it's the *shape* of the verification, not a step-by-step recipe for any particular consumer relationship. Roles applying the discipline parameterize the steps to their context (Architect traces ADR claims to ADR code; CXO traces UX descriptions to feature code; Lead Dev traces epic claims to implementation).

Promotion-to-Proven criterion for this methodology entry: three independent instances of Consumer-Trace Verification being applied (cohort, any role) catching a claim-vs-reality drift that would have otherwise propagated. methodology-29 framework: bottom-up pattern formation through application + recognition.

### Promotion progress — 2 of 3 (2026-06-08; NOT yet Proven)

Recording evidence accumulation transparently. **Two pre-implementation wins** surfaced in Arch's Day-5 findings (2026-06-08), both Lead-Dev-applied during the ADR-060 Phase-3/Phase-4 arc (2026-06-07):
1. **Phase-3 coverage trace** — pre-implementation consumer-trace found ~40+ category-routed actions that would false-floor; spec re-scoped to observability-only. Prevented a production-routing regression.
2. **Phase-4 audit-cascade trace** — found 6 behavior-driving consumers + ~50 test assertions, specifically `lens_inference.py ACTION_TO_LENS` (~30 keys) the Phase-3 analysis had missed. Prevented a silently-broken lens-inference shim.

These are a **stronger instance-class than the originating post-implementation instances** — *pre*-implementation defense (prevents the drift) vs. *post*-implementation catch (surfaces it after). That strengthens the methodology's value claim.

**But this is 2-of-3, not Proven** — and held there deliberately, per the entry's own criterion: both instances are the same applier (Lead Dev) in the same architectural arc, so they aren't fully "three independent instances." (CIO note: my 2026-06-08 Day-5 disposition memo initially said "promote to Proven"; on re-reading *this* entry's self-set criterion, that was premature — corrected to "2-of-3, hold Emerging." Verify-the-entry's-own-bar before promoting.) **Promotion completes on a 3rd independent instance** — ideally a different applier role and/or a different work-arc.

### Altitude-extension candidate — the cohort-routing layer (2026-06-16, Arch-surfaced; NOT a promotion-counting instance)

Arch surfaced a same-shape candidate at a **non-code altitude** (`mailboxes/cio/read/cc-memo-arch-to-lead-cc-cio-pm-1252-arch-gated-rulings-...-2026-06-16.md`): a Lead-Dev request for Arch-gated rulings lived in Lead's session log + carry-forward, but Arch's session-start scan path didn't cover those surfaces, so the request wasn't consumed until PM relayed it. Arch's framing: *"Consumer-Trace Verification at the cohort-routing layer rather than the code layer — same shape."*

**The kernel is real.** m-30's core is *upstream existence ≠ downstream consumption* (context-shape exists ≠ LLM call happens). At the routing altitude that becomes *emission ≠ delivery* (a signal was produced ≠ the intended consumer actually scans the surface it landed on). Both fail identically: assuming the producer side implies the consumer side.

**Precise scoping (the honest catalog call — this is why it's a candidate, not an instance):**
- It is a **retrospective recognition** of the shape, **not an application** of the discipline that caught a drift. The incident was caught by PM relay, not by anyone running a consumer-trace. The promotion bar requires *the discipline applied to catch drift that would otherwise propagate* — so this does **NOT** advance the 2-of-3 tally. (The "#7" numbering in Arch's memo is informal; it doesn't map to this entry's instance count.)
- **Cross-pattern adjacency, not clean ownership:** at the routing altitude this overlaps HOST's mail-vs-GH signal-surface norm (2026-06-15: a signal recorded where the consumer doesn't look isn't delivered). The incident arguably belongs as much to that norm as to m-30; recorded here as a cross-altitude candidate with the overlap flagged, not claimed.
- **The mitigation is sound (m-36).** Arch's fix — sweep Lead's session log + carry-forward for "Arch-gated" markers at session-start — is the mechanism-not-vigilance move at the routing layer: the *consumer* expands its scan path to cover the surface the *producer* actually uses. That's the right resolution regardless of which pattern owns the label.

**Disposition:** keep at Emerging (2-of-3 unchanged). If consumer-trace-at-the-routing-layer is *applied* (not just recognized) to catch a dropped cross-agent signal before it costs a block, that would be a genuine 3rd-instance candidate — and a strong one, being a different applier + a different altitude.

Slot 30 reserved May 15 per pre-filing slot-availability check (methodology-28); this filing claims the slot. Filed alongside methodology-31 (Append-Only Autonomous-Cycle Architecture, 2026-05-18) and methodology-32 (Postel for Memo Headers, 2026-05-18) as the May 18 batch.

---

*Filed: 2026-05-18 by CIO Vehicle 2. Pattern category: methodology-corpus verification discipline for consumer-relationship claims. Authority: CIO self-approval per `methodology-audit-policy-updates-2026-03-16.md`, ratifying Architect's Option A disposition request 2026-05-15. Slot allocation: methodology-30 (slot reserved 2026-05-15; filed alongside methodology-31 and methodology-32 in the May 18 batch).*
