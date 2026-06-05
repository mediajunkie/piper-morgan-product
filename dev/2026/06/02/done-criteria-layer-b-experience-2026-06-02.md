# #683 Layer B — Experience-Layer Definition of Done (draft v0.2)

**Owner**: CXO
**Date**: 2026-06-02 (v0.1) → 2026-06-03 (v0.2, PPM co-review answers folded)
**Status**: DRAFT v0.2 — PPM co-review answers (Q1/Q2/Q3) folded 2026-06-03; ready for PPM to land the A+B pair. **Do not land solo.** Pairs with Layer A (interface-verification DoD, methodology-30 Consumer-Trace; PPM integration owner) for a co-reviewed A+B landing per the parallel-pairing shape PM confirmed.
**Parent**: #683 MUX-WIRE-DOD — *Update Definition of Done to require interface verification*
**Companion**: Layer A — interface-verification DoD (`methodology-30-CONSUMER-TRACE-VERIFICATION.md`; PPM integrates into completion-criteria process artifacts)

> **Provenance note**: This is the *first* draft of Layer B. A May 28 PPM memo (`memo-ppm-to-cxo-cc-ceo-683-parallel-pairing-confirmed-2026-05-28.md`) referenced a `done-criteria-layer-b-experience-2026-05-28.md` as already-drafted — that file never existed (confabulated reference; flagged separately to PPM + CIO 2026-06-02). This 06-02 file is the real Layer B and is deliberately *not* backdated to launder the phantom reference.

---

## What Layer B is

#683 asks that the Definition of Done require new services to be verified through the interfaces users actually reach. The CXO split (2026-05-28) separated that into two layers because "Done" was carrying two different questions under one word:

- **Layer A — can a real consumer reach it, and does the real behavior fire?** (Engineering/interface verification. The methodology-30 Consumer-Trace gate.)
- **Layer B — once reached, does the *experience* meet the bar?** (Experience verification. This document.)

Layer A is **reachability**. Layer B is **quality-of-encounter**. A surface can pass one and fail the other; both must pass before the surface is Done at the user-facing level.

## The gate (one sentence)

> **A user-facing surface is not Done until its delivered experience passes the Colleague Test (or the surface's branched verification rubric) *and* conforms to the experience intent specified in its MUX doc.**

Two criteria, both required. Neither alone is sufficient.

### Criterion 1 — Colleague Test (or branched rubric) pass

The delivered experience is scored against the appropriate rubric in the Colleague Test family:

- **Response-text surfaces** (chat replies, declines, error/degraded paths) → **Colleague Test rubric** (R/C/T, ≥7/9, no zero-dimension, auto-fail rules per path type). `docs/internal/testing/colleague-test-rubric.md`.
- **UI-rendering surfaces** (lifecycle indicators, staleness cards, status surfaces) → **UI Lifecycle Verification Rubric** (R=Recognition / C=Clarity / T=Tone), the canonical legitimate branch for non-response-text surfaces. `docs/internal/testing/ui-lifecycle-verification-rubric-v0.1.md`.
- **New surface type with no fitting rubric** → branch a new instrument per the Branch-or-Anchor discipline (CT §"How to Extend This Rubric"). Do **not** silently re-use R/C/T with shifted meanings. Naming the absence of a fitting rubric is itself a Layer-B finding.

The score is taken on the experience **as delivered**, not as intended — the same "score what the user gets" discipline the rubric already applies to degraded/error paths.

### Criterion 2 — MUX-doc conformance

The surface renders the experience its MUX doc specifies. The MUX doc is the experience contract; conformance means:

- **Voice register** matches the surface's cluster (offer-first vs. context-coordination) and its named voice anchor/spines.
- **Offer-first / honest-about-limits framing** is present where the MUX doc calls for it (names what the user *can* do, not only what failed).
- **Per-event-type rendering** matches the doc's specification (each state the doc enumerates actually renders, and renders as described).
- **No drift between label and plumbing** — the surface doesn't claim, in its visible text or affordances, behavior that isn't wired. (This is the experience-side face of Pattern-073; see grounding below.)

For surfaces that ship before their MUX doc lands (lightweight-note surfaces, or build-against-shipped-intent surfaces per the Round 2 handoff), conformance is judged against the shipped intent + the lightweight note; the full-doc obligation attaches when the doc lands.

## How to apply it (at done-time)

For any change that adds or modifies a user-facing surface:

1. **Identify the surface type** → select the rubric (CT, UI Lifecycle Verification, or branch a new one).
2. **Reach the surface as a real user would** (this is Layer A's output — the Consumer-Trace already proves it's reachable; Layer B starts where Layer A ends).
3. **Score the delivered experience** against the rubric. Record the score as the verification artifact (same as Layer A records the trace).
4. **Check MUX-doc conformance** point by point against the surface's doc (or shipped intent + lightweight note if the doc hasn't landed).
5. **A miss on either criterion files a discovered-work issue** describing the experience gap — it does not silently downgrade "Done."

## Layer A vs Layer B — the distinction, grounded in #1142

The #1142 UI-vs-architecture-mismatch findings (M2D-UAT smoke, 2026-06-02) are a clean natural experiment in why the two layers are separate:

| #1142 finding | Fails Layer A (reachability) | Fails Layer B (experience) |
|---|---|---|
| **Lists view (#714)** — architecture has staleness-card rendering ready; no UI route to reach it | ✅ unreachable — fails A | (can't assess B until reachable) |
| **Insight Journal (#1031)** — only reachable by typing the URL; `/insights` returns the floor's generic response | ✅ slash-command path fails A | — |
| Insight Journal — **bare browser `confirm()` for delete; styled unlike the rest of the site; no nav** | (page loads) | ✅ off-voice, off-pattern — fails B |
| Insight Journal — **two response options labeled "Correct" and "That's right"** (semantically indistinguishable) | (both wired) | ✅ Clarity failure — fails B |
| **Standup page (#704)** — lifecycle-indicator + experience-phrase work landed in architecture; UI shows the legacy button, doesn't render the indicators | ✅ indicators unreachable — fails A | ✅ and even the visible surface is off its MUX intent — fails B |

PM's framing — *"the plumbing no longer matches the labels; it becomes untestable if the plumbing no longer matches the labels"* — is precisely a **both-layers** failure: Layer A (the plumbing isn't reachable) and Layer B (the labels promise an experience the surface doesn't deliver). A DoD that only asked Layer A would still pass the "Correct"/"That's right" labeling and the bare `confirm()` dialog — they're reachable. Layer B is what catches them.

## When Layer B applies — and when it doesn't

**Applies** when a change adds or modifies anything a user encounters: a chat response shape, a UI surface, a state rendering, a decline/error path, an integration-setup flow.

**Does not apply** when:
- The change is purely internal (a refactor, a service-layer change with no user-facing surface) — Layer A may apply, Layer B does not.
- The change is to a surface explicitly out of experience scope for the milestone (record the deferral; don't score against a bar the milestone didn't commit to).

Layer B is not a quality-engineering metric and not a correctness check (the Colleague Test already disclaims that). It asks one question: *does the encounter feel like working with a competent colleague, and does it match what we designed?*

## Relationship to Layer A and the co-review

Layer A and Layer B are designed to land as one paired artifact, not two halves. The pairing shape (PPM, PM-confirmed):

1. CXO holds Layer B (this draft).
2. PPM integrates Layer A when CIO's methodology-30 draft is in the completion-criteria process artifacts (Review Gates taxonomy + completion-gate entry). *(Layer A's methodology-30 draft has landed; PPM integration is the remaining step.)*
3. CXO + PPM co-review the A+B pair so "done means done at two layers" reads as one coherent whole before it lands canonically.

**Co-review questions — RESOLVED (PPM, 2026-06-03):**

- **Q1 — Canonical landing (resolved):** Layer B lands in three homes, parallel to Layer A's actual landing (`interface-verification-dod-layer-a.md` + Sub-Epic Gating Protocol item 5 + Review Gates Class B note):
  1. Standalone `docs/internal/development/experience-verification-dod-layer-b.md` (sibling to Layer A's doc).
  2. **Sub-Epic Gating Protocol item 6** (`m2-structure.md`), paired right after item 5.
  3. PPM extends the Review Gates Class B note to name *both* layers ("interface-verification (A) + experience-verification (B)").
  PPM owns the landing once v0.2 settles, so A and B land together.

- **Q2 — Hard gate vs. graded finding (resolved):** **Hard gate within the surface's committed experience scope** — a Layer-B miss keeps the AC `[ ]`/`[⏸]`, never `[x]` (same shape as Layer A's Consumer-Trace FAIL, the M2d gate, and the 80/90% quality-threshold regime). **Graded finding for out-of-scope polish** — file discovered-work + annotate Done; don't block. Both layers gate identically on committed scope and both downgrade-to-finding out of scope: "done means done at two layers" = both hard-gate what the surface committed to.

- **Q3 — CT-version pin (resolved):** Cite the Colleague Test by name + canonical file (not a version number) — endorsed as the interim. **Canonical CT version confirmed = v2.3.2** (the committed file header; the "v2.4" cited in roadmap v18 + PDR-005 was a May-10 *proposal* that never landed as a committed version — drift, not a real canonical). PPM reconciles those citations to v2.3.2 in the same pass. (If a genuine v2.4 bump is warranted, that's separate CT-owner work; it does not gate this pair or v18/PDR-005, which cite v2.3.2.)

## Why A and B are one artifact, not two — joint closure of label-vs-plumbing drift (PPM co-review note)

The two layers jointly close the **label-vs-plumbing-drift surface (Pattern-073)** from both sides:

- **Layer A (reachability-side face):** is the real behavior *reachable* by an actual consumer? (Consumer-Trace.)
- **Layer B (experience-side face):** does the visible *label* promise an experience the surface actually delivers? (Criterion 2's "no drift between label and plumbing.")

A surface drifts when its labels outrun its plumbing in *either* direction — the plumbing went away (A catches it) or the label over-promises the experience (B catches it). Neither layer alone closes the drift; together they do. That joint closure is *why* the two are one paired DoD, not two independent checks — and it's the one line worth carrying into the landed pair.

---

*Draft v0.2 — CXO, 2026-06-03 (PPM Q1/Q2/Q3 folded). Canonical filename is `done-criteria-layer-b-experience-2026-06-02.md` (the 06-02 file on origin/main; a 06-03 filename in an earlier memo was a typo). Next: PPM lands the A+B pair.*
