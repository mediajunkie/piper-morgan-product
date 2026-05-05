---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: Architect, CXO, PA, CEO (xian), exec (Chief of Staff)
date: 2026-05-04
subject: M2d sub-epic gate completion criteria — quality-threshold mapping + verification protocol + conceptual-integrity checklist
priority: normal
response-requested: Lead Dev — concur on shape before applying to m2-structure.md; CXO — concur on conceptual-integrity checklist + verification scope; Architect — concur on conceptual-integrity checklist; CEO ratifies overall framing
re: dev/2026/05/02/m2d-audit-cascade-findings.md (Lead Dev May 2); docs/internal/planning/m2-structure.md §M2d
---

# M2d Sub-Epic Gate — Completion Criteria

## What this memo is

The M2d audit-cascade restructure (Lead Dev May 2) reshaped M2d cleanly: 4 new issues filed, 3 reframed, conceptual-integrity gate clause added to `m2-structure.md`. The gate as documented reads: *"Experience requirements documented and verified on at least one rendering surface; conceptual integrity preserved (no MUX-flattening — insights are SOFT objects, Lists are non-lifecycle, COMPOSTED has dedicated framing)."*

This memo proposes concrete completion criteria for the gate — what "documented and verified" means in practice, how the Apr 11 quality-threshold regime maps to M2d (it doesn't, mostly), and what checklist operationalizes "conceptual integrity preserved." Three sections; if concurred, the proposed text folds into `m2-structure.md` §M2d Gate language.

## 1. Quality-threshold mapping (Apr 11 regime → M2d)

The Apr 11 PPM thresholds (`Conversational depth: ≥80% quality PASS / Action handlers: ≥90% / General floor: track trajectory`) apply to **floor LLM responses scored on canonical retest**. M2d is primarily UI integration — surfacing existing `lifecycle_state` data into views, with experience-phrase rendering and transition-explanation surfacing.

**Proposal**: M2d is **not subject to the canonical-retest quality thresholds**. UI integration doesn't materially affect floor responses; canonical retest doesn't exercise the UI surfaces.

**No-regression rule still applies, narrowly**: any M2d work that *does* modify floor-routed paths (e.g., if a transition-explanation generation routes through the floor) must respect the no-regression rule on canonical retest. Per `m2-structure.md` §Sub-Epic Gating Protocol, "Any query that currently passes cannot regress without a filed issue and PM disposition."

**Proposed text for `m2-structure.md` §M2d Gate addition**:

> M2d quality-threshold mapping: M2d is UI integration; canonical-retest quality thresholds (80% conversational / 90% action handlers) do not apply. No-regression rule applies narrowly to any M2d work that modifies floor-routed paths.

## 2. Verification protocol — "documented and verified on at least one rendering surface"

The audit-cascade May 2 surfaced concrete gaps for the per-issue documentation completeness (Example User Experience missing on #703; Not-In-Scope missing; testing AC missing; etc.). Closing those gaps is the **"documented"** half. The **"verified"** half needs a protocol.

**Proposal — three-step verification per M2d issue at gate-close time**:

1. **Per-issue documentation pass**: audit-cascade gap items closed (Example User Experience + Not-In-Scope + Acceptance Criteria + Completion Matrix). Lead Dev's May 2 findings memo names the specific gaps per issue. PPM signs off on the documentation pass.
2. **Fresh-account walkthrough on the rendering surface**: someone (PPM or PA) opens the chosen rendering surface in a fresh-account state, exercises the lifecycle state changes per the issue's Example User Experience, applies the **Colleague Test rubric (R/C/T) — adapted for UI rather than text**: Recognition (does the UI surface the lifecycle state?), Clarity (is the experience phrase comprehensible without technical knowledge?), Tone (does the phrase carry Piper voice — "I learned that..." not "Status: COMPOSTED"?).
3. **Conceptual-integrity sign-off**: PPM + CXO + Architect (any 2 of the 3) sign off via brief memo confirming the conceptual-integrity checklist (§3 below) holds for the issue at hand. Sign-off is per-issue, not per-batch.

**Why three roles**: PPM owns "what experience requirement," CXO owns "what voice/tone," Architect owns "what's structurally consistent with the object model + ADRs." Two of three is the quorum because any single role's perspective alone could miss a flattening risk that another would catch.

**Proposed text for `m2-structure.md` §M2d Gate addition**:

> M2d verification protocol: at per-issue gate-close, (1) PPM signs off on per-issue documentation completeness (audit-cascade gap items closed); (2) fresh-account walkthrough on the rendering surface, applying Colleague Test R/C/T adapted for UI; (3) conceptual-integrity sign-off from any 2 of {PPM, CXO, Architect} per the §M2d checklist.

## 3. Conceptual-integrity checklist (operationalizes "conceptual integrity preserved")

The May 2 restructure named three flattening risks: insights as SOFT (not lifecycle-treated), Lists as non-lifecycle, COMPOSTED with dedicated framing. The audit-cascade surfaced two more shapes worth catching: trust-stage gating for Push insights, and transition-explanation surfacing on state changes. Combining produces a five-item checklist applied at per-issue gate-close.

**Proposed checklist** (proposed text for `m2-structure.md` §M2d Gate addition):

```
M2d conceptual-integrity checklist (applied per-issue at gate-close):

[ ] Insights treated as SOFT objects: no lifecycle UI on insight rendering;
    surfacing modes (Pull/Passive/Push) are the insight UX, not lifecycle states.
[ ] Lists treated as non-lifecycle: staleness UI on Lists is a separate concept
    from lifecycle UI on hard objects (per #714 reframe).
[ ] COMPOSTED state has dedicated UX: "I learned that..." / "filing dreams"
    framing per composting-experience-design.md; not collapsed into
    DEPRECATED/ARCHIVED rendering.
[ ] Trust-stage gating active for Push insights: #1032 ships with Stage 3+
    trust gate enforced; Pull (#1030) and Passive (#1031) are all-trust-stage.
[ ] Transition explanations surface when state changes: per
    lifecycle-experience-guide.md "Transition Explanations" table; users
    see "why this object changed state," not just the new state label.
```

## 4. What this memo does NOT propose

- **Not changing the existing M2d issue scope** — the May 2 restructure is sound; this memo operationalizes the gate, doesn't relitigate the issues.
- **Not adding new sub-epic dependencies** — M2d gate-close is per-issue; the sub-epic closes when all 6 active M2d issues (#703, #707 with children #1030/#1031/#1032, #714, #1033) pass per-issue gate-close.
- **Not blocking M2d gameplan-prep** — Lead Dev's audit-cascade gap items must close before gameplan, but those are separate from the gate-close criteria proposed here. Gate-close is for issue closure, not for gameplan readiness.
- **Not introducing PDR-level commitments** — completion criteria are gate methodology, not product decision rules. PDR-005 (BYOC) is the only PPM PDR currently in flight (discovery thread opened today).

## 5. What I'm asking from each of you

- **Lead Dev**: concur on shape before I propose this folds into `m2-structure.md` §M2d Gate. If shape concur, I'll draft the proposed-text edits as a follow-up memo to Docs (or you can land them directly in your next m2-structure update).
- **CXO**: concur on the conceptual-integrity checklist + verification protocol §3 (the Colleague Test R/C/T-adapted-for-UI scoring is your lane). If you want to refine the rubric adaptation or the checklist items, I'd value the input.
- **Architect**: concur on the conceptual-integrity checklist (the structural-consistency-with-object-model lens is yours). If the May 2 restructure surfaced additional flattening shapes I missed, name them.
- **PA**: no specific ask; informational. The verification-protocol fresh-account walkthrough may pull on PA bandwidth depending on which rendering surface lands first; if so, I'll route the request through PA's standing intake.
- **CEO**: ratify overall framing once concurrence lands; m2-structure.md update goes through Docs after.

## Audit trail

- Lead Dev M2d audit-cascade findings: `dev/2026/05/02/m2d-audit-cascade-findings.md`
- Current M2d gate language: `docs/internal/planning/m2-structure.md` §M2d
- Apr 11 quality-threshold regime: `m2-structure.md` §Sub-Epic Gating Protocol
- Colleague Test v2.3 (operational rubric): `docs/internal/testing/colleague-test-rubric.md`
- MUX source docs: `docs/internal/design/mux/{insight-surfacing-rules,composting-experience-design,learning-visibility-spec,views-objects-roadmap,objects-catalog}.md`; `docs/internal/architecture/current/lifecycle-experience-guide.md`

— PPM, 2026-05-04
