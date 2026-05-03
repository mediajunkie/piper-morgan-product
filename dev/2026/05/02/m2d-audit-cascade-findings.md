# M2d Audit-Cascade Findings

**Date**: 2026-05-02
**Author**: Lead Developer
**Scope**: Issues #703, #707, #714, #869 (M2d MUX Lifecycle per `docs/internal/planning/m2-structure.md`)
**Method**: `audit-cascade` skill — issues audited against `feature.md` template AND against MUX source docs in `docs/internal/design/mux/` + `docs/internal/architecture/current/`
**Status**: Findings memo for PM review; **NO implementation started**

---

## Source-doc inventory used

- `docs/internal/design/mux/README.md` — index + key concepts (trust gradient, two-journal architecture, composting framing)
- `docs/internal/design/mux/insight-surfacing-rules.md` — D4 spec; defines Pull/Passive/Push modes + trust gating
- `docs/internal/design/mux/composting-experience-design.md` — D3 spec; "filing dreams" framing; reflection-not-surveillance principle
- `docs/internal/design/mux/learning-visibility-spec.md` — D1 spec; trust-gated visibility matrix
- `docs/internal/design/mux/views-objects-roadmap.md` — object → view mapping with hard/soft classification
- `docs/internal/design/mux/objects-catalog.md` — full object inventory with `lifecycle_state` columns
- `docs/internal/architecture/current/lifecycle-experience-guide.md` — 8-state model + per-state experience phrases + transition explanations
- ADR-045 (Object Model — foundational grammar)
- ADR-053, ADR-055 (Trust + Object Model implementation)

---

## Audit Matrix — Per Issue

### #703 MUX-LIFECYCLE-UI — Lifecycle indicator integration

| Template Requirement | Status | Notes |
|---|---|---|
| Priority | ✅ | P2 |
| Labels | ✅ | UX, MUX-IMPLEMENT, frontend |
| Milestone | ✅ | MVP |
| Epic | ✅ | MUX-IMPLEMENT (#403) |
| Related issues | ✅ | #685, #702, #423, #424 |
| Problem statement (current state) | ✅ | Components built; no view integrates them |
| Impact | ✅ | Blocks #685; "composting" philosophy invisible; 82 unused tests |
| Strategic context | ✅ | Final wiring step |
| Goal / primary objective | ✅ | "Users see lifecycle indicators on at least one object type, with experience phrases (not technical labels)" |
| Example user experience | ❌ | Issue body has no before/after scenario |
| Not in scope | ❌ | Implicit (post-MVP roadmap), not explicit "not in scope" list |
| What already exists | ✅ | Component table + readiness matrix |
| Phases / tasks / deliverables | ⚠️ | Tracking issue with child issues #704, #705; phase detail lives in children, but children aren't shown here for me to audit |
| Acceptance criteria — functionality | ⚠️ | Implicit ("users see lifecycle indicators on at least one object type"); not template-format checklist |
| Acceptance criteria — testing | ❌ | No explicit test strategy in body; the 82 unused tests aren't cross-referenced as "must pass post-integration" |
| Acceptance criteria — quality / docs | ❌ | Not surfaced |
| Completion matrix | ❌ | Missing |

**MUX source-doc cross-check**:

- ✅ "Experience phrases (not technical labels)" goal honors the lifecycle-experience-guide. Each state has a distinct phrase ("I just noticed..." / "I learned that..."). **GOAL is correctly stated** to avoid flattening.
- ⚠️ **Composting/COMPOSTED state risk**: the body notes "objects feel deleted not transformed" — but doesn't explicitly require the COMPOSTED state's "I learned that..." surfacing or the "filing dreams" framing from `composting-experience-design.md`. If the MVP integration lands DEPRECATED → ARCHIVED but skips COMPOSTED's distinct UX, that's a flattening. **GAP**: COMPOSTED experience not in scope statement.
- ⚠️ **Transition explanations** (lifecycle-experience-guide.md "Transition Explanations" table) — not mentioned in the issue. When users see a state change, the "why" should surface ("I noticed {object} needed attention", etc.). The current body is silent on whether transitions get explanations.
- ⚠️ The integration roadmap mentions Insight as "Future (see notes)" — correct per `views-objects-roadmap.md` ("Insights are soft objects, no lifecycle"). But the row exists at all in this matrix, which could mislead a future reader into thinking Insight has lifecycle. Worth a one-line note or removing the row.

**Action required before gameplan**:
- Add Example User Experience (a single canonical case showing experience phrase + transition explanation)
- Add explicit "Not in scope" — particularly to clarify Insights are NOT lifecycle objects (avoid flattening drift)
- Add testing acceptance criteria; cross-reference the 82 existing component tests as "must continue passing"
- Decide: does the MVP child include the COMPOSTED state UX, or only earlier states? If only earlier states, file COMPOSTED UX as a Post-MVP follow-up explicitly so it's not silently dropped
- Add transition-explanation surfacing to acceptance criteria
- Add completion matrix

---

### #707 MUX-INSIGHT-SURFACING — Implement Insight Surfacing Rules

| Template Requirement | Status | Notes |
|---|---|---|
| Priority | ⚠️ | "P3 (TBD - may be Post-MVP)" — milestone says MVP but priority undecided |
| Labels | ⚠️ | Just "enhancement"; no UX/MUX label |
| Milestone | ⚠️ | "MVP (pending prioritization)" — explicitly TBD |
| Epic | ✅ | MUX-IMPLEMENT (#403) |
| Related | ✅ | #431, #706 |
| Problem statement | ⚠️ | "We have a spec but no implementation" — accurate but thin |
| Impact | ❌ | Not stated |
| Strategic context | ❌ | Not stated |
| Goal | ⚠️ | "Implement the insight surfacing rules as specified in D4" + "Note: This issue is a placeholder" |
| Not in scope | ❌ | Missing |
| What already exists | ❌ | Missing — but the spec at `insight-surfacing-rules.md` is detailed and exists |
| Phases / tasks | ❌ | None |
| Acceptance criteria | ❌ | "TBD after #706 discovery determines..." |
| Completion matrix | ❌ | Missing |

**MUX source-doc cross-check** (significant findings):

- 🚨 **#707 is STALE as written**: the body says "TBD pending #706 discovery" but **#706 discovery is complete** as of 2026-03-24. Both `objects-catalog.md` (status: Complete) and `views-objects-roadmap.md` exist with clear decisions. The "TBD" framing is more than a month out of date.
- 🚨 **The CXO/PPM decision IS documented in #707** (line: *"Insights do NOT use the entity lifecycle pattern. They have surfacing modes and relationship metadata (confidence, recency, user response) instead."*) — but the rest of the body doesn't reflect that. If implementation proceeds from this body, **risk of flattening insights into lifecycle treatment** because the body's "TBD pending #706" is the dominant signal a reader picks up.
- 🚨 **Three modes are not equivalent and shouldn't be implemented as one feature**: per `insight-surfacing-rules.md`:
  - **Pull**: all trust levels; user-initiated; explicit query
  - **Passive**: all trust levels; user-navigated; passive browsing
  - **Push**: **Stage 3+ trust required**; Piper-initiated; contextually-relevant
  
  Push has different infrastructure needs than Pull/Passive (trust-stage gate, context-relevance scoring, mute controls). **#707 as written would risk lumping all three into one ticket and flattening the trust-gating distinction.**
- 🚨 **Trust-stage gating is load-bearing**: per `learning-visibility-spec.md` Trust-Gated Visibility Matrix, what users see depends on Stage 1-4. If #707 lands without trust-gating wired, the surfacing logic is structurally incomplete (it would push to Stage 1 users, violating the colleague-test framing).

**Action required before gameplan**:
- **Reframe — not a placeholder anymore.** #706 discovery is complete; the decisions exist. Either:
  - (a) Update #707's body to reflect the actual decisions + spec, OR
  - (b) **Split #707 into three issues** (one per mode: Pull / Passive / Push) since they have different infrastructure needs and trust-gating
- Resolve the milestone ambiguity (MVP vs Post-MVP) — current "MVP (pending prioritization)" is undefined
- Cite `insight-surfacing-rules.md` + `learning-visibility-spec.md` + the trust-gradient matrix as the source of truth for AC
- Add explicit AC: "Push mode requires Stage 3+ trust check; never surfaces to Stage 1-2 users"
- Add Not in Scope: "Push mode trust-stage logic does not depend on lifecycle state of the underlying object"

---

### #714 MUX-LISTS-LIFECYCLE-UI — Wire Lifecycle/Staleness to Lists View

| Template Requirement | Status | Notes |
|---|---|---|
| Priority | ⚠️ | "Post-MUX MVP (before Beta)" — outside MVP per the body itself |
| Labels | ⚠️ | Just "enhancement" |
| Milestone | ⚠️ | GitHub says MVP; body says "Post-MUX MVP (before Beta)" — **mismatch** |
| Parent epic | ✅ | #706 |
| Problem statement | ⚠️ | "Lists may show staleness... List items operate on faster pace layer than Lists themselves" — descriptive, not problem-shaped |
| Impact | ❌ | Not stated |
| Goal | ⚠️ | Implicit ("Wire lifecycle or staleness indicators to Lists view") |
| Design questions | ⚠️ | Three design questions explicitly TBD: lifecycle vs staleness; ListItems treatment; List-vs-ListItem activity relationship |
| Scope | ⚠️ | 4 tasks listed but tasks 1-2 are "determine" not "implement" |
| Acceptance criteria | ⚠️ | 3 ACs but vague ("appropriate state indicator") |
| Effort | ⚠️ | "Small-Medium (depends on design decisions)" |

**MUX source-doc cross-check** (significant findings):

- 🚨 **The "lifecycle vs staleness" question has been answered** in `objects-catalog.md`: List has `lifecycle_state: No`. List is a hard object but does NOT participate in the 8-state lifecycle model. ListItem has `lifecycle_state: No` as well. Per `views-objects-roadmap.md`, List → Lifecycle UI: **Deferred** (with the implication that some state-display is wanted, just not full lifecycle).
- 🚨 **Staleness ≠ lifecycle ARCHIVED**. The body's note "Staleness concept may need separate definition - 'old and untouched' is not the same as ARCHIVED lifecycle state" is correct and important. Treating them as interchangeable would be flattening:
  - **ARCHIVED** = explicitly preserved for reference; transition was purposeful
  - **Stale** = old + untouched; passive lack of activity, not a stage assertion
  - These are conceptually distinct. Mixing them would erode the lifecycle vocabulary.
- 🚨 **Milestone mismatch is a real signal**: the body explicitly says "Post-MUX MVP (before Beta)" — meaning the issue's author scoped it OUT of MVP. The GitHub milestone says MVP. That's a process gap; one or the other is wrong.
- ⚠️ **Design uncertainty is unresolved**: per the source docs, it IS resolved (Lists don't get lifecycle; the question is whether/how to surface staleness — a separate concept needing its own design pass). The issue body still treats both as open questions.

**Action required before gameplan**:
- **Fold the source-doc decisions in**: Lists are not lifecycle objects per the catalog; remove the "lifecycle vs staleness" framing in favor of "design a staleness-display concept (separate from lifecycle)"
- Resolve milestone mismatch with PM — either bump out of MVP per body's intent, or override the body if MVP is correct
- If staleness needs design, **this issue should produce a staleness spec first, then UI** — the current scope conflates spec + UI
- Add explicit Not in Scope: "Lists do not get lifecycle states. ListItems do not get lifecycle states. This issue is about a separate staleness concept, not lifecycle."

---

### #869 Project configuration IA — Project Detail as primary, Settings as overview

| Template Requirement | Status | Notes |
|---|---|---|
| Source / authority | ✅ | CXO memo 2026-02-28; PDR-003 reference |
| Priority | ⚠️ | "M1" notation — that's a sprint label, not the template's P0/P1/P2/P3 |
| Labels | ✅ | architecture, UX |
| Milestone | ✅ | MVP |
| Related | ✅ | #861, PDR-003 |
| Problem statement | ⚠️ | Implicit (recommendation-shaped, not problem-shaped) |
| Impact | ⚠️ | "No rework required" on #861 is mentioned; user impact implicit |
| Goal | ✅ | Recommendation: Option C (both surfaces, link from Settings to Detail) |
| Two user scenarios | ✅ | Table format |
| Information architecture | ✅ | Table + URL structure |
| UX principles | ✅ | 4 numbered principles |
| PDR-003 extension | ✅ | Pattern applied to other entities |
| Impact on existing work | ✅ | "No rework required" |
| Acceptance criteria | ✅ | 6 ACs; functionality-checkable |
| Phases / tasks / deliverables | ❌ | Not template-format; goes straight from recommendation to AC |
| Testing AC | ❌ | Not stated |
| Completion matrix | ❌ | Missing |

**MUX source-doc cross-check**:

- ⚠️ **#869 isn't really MUX-flavored**: it's IA design, not MUX-lifecycle/insight work. The four "Key Concepts" in the MUX README (Trust Gradient, Two-Journal, Composting) don't apply here. **Question for PM**: should this be in M2d or in a separate IA bucket? `m2-structure.md` lists it under "M2d MUX Lifecycle" but the issue's substance is unrelated to MUX.
- ✅ The Colleague Test reference ("If you're looking at a project and want to add a repo, that should happen *right there*") is consistent with the MUX colleague-test principle. Light cross-reference, not core.

**Action required before gameplan**:
- Add explicit Phases section per template (the work has natural phases: Project Detail Config tab implementation, Settings → Projects link rewire, smoke testing)
- Add testing AC
- Add completion matrix
- **Surface to PM**: belongs in M2d or its own bucket?

---

## Cross-Cutting Findings

### Conceptual drift / flattening risks

1. 🚨 **#707's "TBD pending #706" framing is stale** — #706 discovery completed Mar 24; the actual decisions exist (insights are soft objects, not lifecycle; three distinct surfacing modes with trust-gating). Implementing from the current body risks flattening insights into lifecycle, ignoring the trust-gradient, or collapsing three modes into one.
2. 🚨 **#714's "lifecycle vs staleness" framing is stale** — the source docs already answered (Lists don't get lifecycle; staleness is a separate concept needing its own design). Implementing as written risks treating staleness AS a lifecycle stage, which would flatten the conceptual distinction.
3. ⚠️ **#703's COMPOSTED state may be silently dropped** — body talks about "composting philosophy invisible" (good) but the AC doesn't require COMPOSTED state's distinct experience phrase ("I learned that...") to be surfaced. If MVP children only cover earlier states, the most distinctive MUX concept (COMPOSTED + composting framing) lands later or never.
4. ⚠️ **#703's transition explanations might be omitted** — the lifecycle-experience-guide has a Transition Explanations table; #703 body doesn't mention it. Indicators might land as static state-icons without the "why" surfacing.

### Process/scoping gaps

5. ⚠️ **#869 may not belong in M2d** — substance is IA, not MUX. PM check.
6. ⚠️ **#714 milestone mismatch**: body says Post-MUX-MVP; GitHub says MVP. PM check.
7. ⚠️ **#707 milestone undefined**: "MVP (pending prioritization)". PM call.
8. ⚠️ **No issue covers COMPOSTED state UX explicitly** — even if #703's MVP children land, the most distinctive MUX surface (composting reflection) has no dedicated implementation issue. Either fold into #703 or file separately as a M2d-tail item.

### Issue-template completeness

| Issue | Template completeness | Biggest gap |
|---|---|---|
| #703 | Partial — phases live in children; AC vague | COMPOSTED state + transitions |
| #707 | **Skeleton** — placeholder shape | Needs full reframe given #706 is complete |
| #714 | Partial — design questions stale | Needs source-doc decisions folded in |
| #869 | Mostly complete; non-MUX | Phases section + completion matrix |

---

## Recommendations to PM

### High-priority before any M2d implementation

1. **Reframe #707** (or split into Pull/Passive/Push). Currently a placeholder citing stale "pending #706" rationale. Either reframe with the actual spec/decisions, or split.
2. **Update #714** to reflect "Lists don't have lifecycle" decision + scope to "staleness-spec-first, then staleness-UI". Resolve milestone mismatch.
3. **File a #703-companion issue** for COMPOSTED state + composting framing UX, OR explicitly fold into #703's MVP scope. Don't let this most-distinctive MUX concept silently drop.
4. **Decide #869 home** — keep in M2d or split out as IA work.

### Medium-priority hygiene

5. **#703 body update**: add Example User Experience (canonical case showing experience phrase + transition explanation), explicit Not-in-Scope (Insights are not lifecycle), and testing AC referencing the 82 existing component tests.
6. **#869 body update**: add Phases + testing AC + completion matrix per template.

### Process observation

The four M2d issues have **uneven readiness**. #703 is closest to actionable (clear scope, child issues, components exist). #869 is also actionable but conceptually adjacent (IA, not MUX). #707 and #714 are placeholder-shape issues whose source-doc context has moved past them since they were filed.

This is a normal product-management drift signature: issues filed during a discovery phase become stale once the discovery completes, and the staleness isn't always reflected back into the issue bodies. **The audit-cascade catches this exactly when it should** — between issue and gameplan.

---

## What I am NOT doing

- Not writing gameplans yet — issue audit is gate 1; cannot proceed past unfixed gaps without PM judgment
- Not implementing — audit-cascade explicitly forbids skipping gates
- Not modifying issue bodies myself — surfacing gaps for PM to direct, not unilaterally repairing PM-authored or CXO-authored issues
- Not deciding milestone or scope questions — those are PM calls

---

## Audit-cascade gate status

**Gate 1 (Issue → Gameplan): ❌ NOT PASSED**

Cannot proceed to gameplan phase for any of the four issues until PM addresses the gaps above (especially the conceptual-drift risks on #707, #714, #703-COMPOSTED).

— Lead Developer, 2026-05-02
