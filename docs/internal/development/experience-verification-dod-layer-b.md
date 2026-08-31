# Experience-Verification Done-Definition (Layer B) — #683

**Status**: CANONICAL (landed 2026-06-03 as the A+B pair, with Layer A). Co-review resolved (PPM Q1/Q2/Q3, 2026-06-03).

**Owners / provenance**:
- **CXO** — authored Layer B (experience-layer DoD). Source draft: `dev/active/done-criteria-layer-b-experience-2026-06-02.md` (v0.2).
- **PPM** — integration owner; landed Layer B into the completion-criteria process artifacts (Sub-Epic Gating Protocol item 6 in `m2-structure.md` + the extended Review Gates Class B note in `roadmap.md`) as the sibling to Layer A.

**Pairs with Layer A** (`docs/internal/development/interface-verification-dod-layer-a.md` — interface-verification DoD, methodology-30 Consumer-Trace). The two-layer split is the CXO disposition of 2026-05-28. **Layer A = reachability** (can a real consumer reach it, does the real behavior fire); **Layer B = quality-of-encounter** (is it *good* once reached). A surface can pass one and fail the other; both must pass before the surface is Done at the user-facing level. See §"Why A and B are one artifact."

**Parent**: #683 MUX-WIRE-DOD — *Update Definition of Done to require interface verification*.

---

## The gate (one sentence)

> **A user-facing surface is not Done until its delivered experience passes the Colleague Test (or the surface's branched verification rubric) *and* conforms to the experience intent specified in its MUX doc.**

Two criteria, both required. Neither alone is sufficient.

### Criterion 1 — Colleague Test (or branched rubric) pass

The delivered experience is scored against the appropriate rubric in the Colleague Test family:
- **Response-text surfaces** (chat replies, declines, error/degraded paths) → **Colleague Test rubric** (R/C/T, ≥7/9, no zero-dimension, auto-fail rules per path type). `docs/internal/testing/colleague-test-rubric.md` (canonical version **v2.3.3**).
- **UI-rendering surfaces** (lifecycle indicators, staleness cards, status surfaces) → **UI Lifecycle Verification Rubric** (R=Recognition / C=Clarity / T=Tone), the canonical legitimate branch for non-response-text surfaces. `docs/internal/testing/ui-lifecycle-verification-rubric-v0.1.md`.
- **BYOC / MCP tool surfaces** (hosted MCP path, PDR-006 — where a host LLM composes what the user reads) → **BYOC Recomposition Rubric** (R=Sufficiency / C=Context, anchored / T=Honesty-under-recomposition). `docs/internal/testing/byoc-recomposition-rubric-v0.1.md` (current version **v0.2**). *Added 2026-08-31 — the branch already exists; do not branch a second one.* ⚠️ **Its T axis scores `PENDING-PROBE`, never PASS**, until the second-vendor arm runs (#1463) — so **this rubric can inform design decisions but cannot yet close a Layer-B gate on T alone.** Score R and C; record T as pending and say so.
- **New surface type with no fitting rubric** → branch a new instrument per the Branch-or-Anchor discipline (CT §"How to Extend This Rubric"). Do **not** silently re-use R/C/T with shifted meanings. Naming the absence of a fitting rubric is itself a Layer-B finding.

The score is taken on the experience **as delivered**, not as intended — the same "score what the user gets" discipline the rubric applies to degraded/error paths.

> ### ⚠️ "As delivered" does not work the same way on BYOC
>
> **Canonical statement lives in `docs/internal/testing/colleague-test-rubric.md`** §"Where 'as delivered'
> stops being observable" (moved there 2026-08-31, Q3 review item 4 — it is a claim about the rubric
> family, and ESSENCE's ratified rule says hand-maintained copies are the documented failure mode).
>
> **The one line you need here**: on the BYOC/MCP path the user-visible text is composed by a host we
> don't control and **we never see it**, so a rubric there scores **the payload, not the delivery**.
> A pass on that surface is **not the same claim** as a pass elsewhere and must state its own limit.

### Criterion 2 — MUX-doc conformance

The surface renders the experience its MUX doc specifies. The MUX doc is the experience contract; conformance means:
- **Voice register** matches the surface's cluster (offer-first vs. context-coordination) and its named voice anchor/spines.
- **Offer-first / honest-about-limits framing** present where the MUX doc calls for it (names what the user *can* do, not only what failed).
- **Per-event-type rendering** matches the doc's specification (each enumerated state actually renders, and renders as described).
- **No drift between label and plumbing** — the surface doesn't claim, in visible text or affordances, behavior that isn't wired. (The experience-side face of Pattern-073; see §"Why A and B are one artifact.")

For surfaces that ship before their MUX doc lands, conformance is judged against shipped intent + the lightweight note; the full-doc obligation attaches when the doc lands.

## Gate disposition (how it interacts with AC marking) — co-review-resolved

- **Hard gate within the surface's committed experience scope** — a Layer-B miss keeps the AC `[ ]` or `[⏸]` (per #1050), **never `[x]`**. Symmetric with Layer A's Consumer-Trace FAIL, the M2d gate, and the 80/90% quality-threshold regime.
- **Graded finding for out-of-scope polish** — file discovered-work + annotate Done; don't block.

Both layers gate identically on committed scope and both downgrade-to-finding out of scope: **"done means done at two layers" = both hard-gate what the surface committed to.**

## How to apply it (at done-time)

1. **Identify the surface type** → select the rubric (CT, UI Lifecycle Verification, or branch a new one).
2. **Reach the surface as a real user would** (Layer A's Consumer-Trace already proves reachability; Layer B starts where Layer A ends).
3. **Score the delivered experience** against the rubric. Record the score as the verification artifact (as Layer A records the trace).
4. **Check MUX-doc conformance** point by point (or shipped intent + lightweight note if the doc hasn't landed).
5. **A miss within committed scope keeps the AC open**; an out-of-scope miss files discovered-work + annotates. Never silently downgrade "Done."

## When Layer B applies — and when it doesn't

**Applies** when a change adds or modifies anything a user encounters: a chat response shape, a UI surface, a state rendering, a decline/error path, an integration-setup flow.

**Does NOT apply** when:
- The change is purely internal (refactor / service-layer with no user-facing surface) — Layer A may apply, Layer B does not.
- The change is to a surface explicitly out of experience scope for the milestone (record the deferral; don't score against a bar the milestone didn't commit to).

Layer B is not a quality-engineering metric and not a correctness check (the Colleague Test disclaims that). It asks one question: *does the encounter feel like working with a competent colleague, and does it match what we designed?*

## Layer A vs Layer B — grounded in #1142

The #1142 UI-vs-architecture-mismatch findings (M2D-UAT smoke, 2026-06-02) are the natural experiment:

| #1142 finding | Fails Layer A (reachability) | Fails Layer B (experience) |
|---|---|---|
| **Lists view (#714)** — staleness-card rendering ready; no UI route to reach it | ✅ unreachable | (can't assess B until reachable) |
| **Insight Journal (#1031)** — only reachable by URL; `/insights` returns the floor's generic response | ✅ slash-command path fails A | — |
| Insight Journal — **bare `confirm()` delete; styled unlike the site; no nav** | (page loads) | ✅ off-voice, off-pattern |
| Insight Journal — **two options labeled "Correct" and "That's right"** (indistinguishable) | (both wired) | ✅ Clarity failure |
| **Standup page (#704)** — indicators landed in architecture; UI shows legacy button | ✅ indicators unreachable | ✅ visible surface off its MUX intent |

A DoD that only asked Layer A would still pass the "Correct"/"That's right" labeling and the bare `confirm()` — they're reachable. Layer B is what catches them.

## Why A and B are one artifact, not two — joint closure of label-vs-plumbing drift

The two layers jointly close the **label-vs-plumbing-drift surface (Pattern-073)** from both sides:
- **Layer A (reachability-side face):** is the real behavior *reachable* by an actual consumer? (Consumer-Trace.)
- **Layer B (experience-side face):** does the visible *label* promise an experience the surface actually delivers? (Criterion 2.)

A surface drifts when its labels outrun its plumbing in *either* direction — the plumbing went away (A catches it) or the label over-promises the experience (B catches it). Neither layer alone closes the drift; together they do. That joint closure is *why* the two are one paired DoD, not two independent checks.

## Source grounding

- CXO Layer B source draft (v0.2): `dev/active/done-criteria-layer-b-experience-2026-06-02.md`
- Layer A (paired): `docs/internal/development/interface-verification-dod-layer-a.md`
- Colleague Test rubric (canonical **v2.3.2**): `docs/internal/testing/colleague-test-rubric.md`
- UI Lifecycle Verification Rubric v0.1: `docs/internal/testing/ui-lifecycle-verification-rubric-v0.1.md`
- #1050 AC-marking convention; Pattern-073 (Documentation-Asserted-Behavior Drift); #1142 (UI-vs-architecture-mismatch natural experiment)
- Completion-criteria home: `m2-structure.md` §Sub-Epic Gating Protocol item 6; Review Gates taxonomy in `docs/internal/planning/roadmap/roadmap.md` §Discipline Norms (Class B)

---

*Layer B authored by CXO (v0.1 2026-06-02 → v0.2 2026-06-03, PPM co-review folded); landed to canonical by PPM 2026-06-03 as the A+B pair with Layer A. CT-version drift (v2.4 citations) reconciled to canonical v2.3.2 in the same pass.*
