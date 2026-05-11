# UI Lifecycle Verification Rubric v0.1

**Purpose**: Score UI rendering of lifecycle state on canonical M2d-style integration surfaces.

**Provenance**: Derived from Colleague Test v2.3 (R/C/T 0-3 each, ≥7/9 PASS) with deliberate branching per Methodology-24 (Branch-or-Anchor). The dimension *shapes* mirror CT v2.3's; the dimension *meanings* are explicitly different and apply to UI rendering, not response text.

**Ratified**: 2026-05-10 three-way concurrence: Architect (May 4) + Lead Dev (May 5) + CXO (May 10), consolidated by PPM (May 10 memo: `memo-ppm-to-lead-cc-arch-cxo-pa-ceo-exec-m2d-gate-criteria-consolidated-2026-05-10`).

**Scope**: M2d gate verification protocol step 2 (fresh-account walkthrough on rendering surface). May be reused for M2e UI integration territory if shape warrants.

---

## Dimensions

### R — Recognition (UI surfaces the lifecycle state)

- **0**: state is not visible on the rendering surface
- **1**: state is hinted (color, icon) but not labeled/named
- **2**: state is labeled but not distinguishable from adjacent states (flattened)
- **3**: state is visible AND distinguishable from adjacent states (no flattening)

### C — Clarity (experience phrase is comprehensible without technical knowledge)

- **0**: rendering uses raw state labels ("Status: COMPOSTED") or technical jargon
- **1**: phrasing is technical-but-readable ("Composted on May 8")
- **2**: phrasing is plain-English but generic ("Archived")
- **3**: experience phrase is plain-English, self-explaining, matches user mental model ("Filed for later — you can bring this back anytime")

### T — Tone (rendering carries Piper voice into UI)

- **0**: voice-flat ("Status: ARCHIVED") or off-voice (chatbot-warmth, content-filter cadence)
- **1**: neutral and competent but not voiced
- **2**: voiced but inconsistent — drifts between Piper and generic-tool registers
- **3**: identifiably Piper — "I learned that..." / "I noticed..." rendering shape

---

## Verdict

**PASS**: ≥7/9 summed AND no single dimension at 0 (auto-fail rule consistent with CT v2.3).

**MARGINAL**: 5-6/9 summed with no zeros — informational pass; surface in audit-cascade for follow-up but doesn't block gate.

**FAIL**: <5/9 OR any dimension at 0.

---

## Note on C-axis difference from CT v2.3

CT v2.3's C-axis is **Context-of-response** (does the response use Piper-specific assembled context).

This rubric's C-axis is **Clarity-of-UI-rendering** (is the UI text comprehensible).

These are different instruments measuring different things; the dimension shape is preserved for cohort-cognitive-load reasons but the meaning is explicitly branched per Methodology-24 (Branch-or-Anchor).

---

## Methodology-24 worked example

This rubric is the canonical worked example of legitimate branching per Methodology-24:

- **Recognized parallel-authoring drift risk**: CT v2.3's "C" axis and this rubric's "C" axis are the same letter with different meanings. Without explicit branching, future agents could conflate them.
- **Disambiguation via naming**: rubric name "UI Lifecycle Verification Rubric v0.1" + explicit provenance + the cross-reference at CT v2.3 §"How to Extend This Rubric" make the branching legible.
- **Preserved cognitive load advantage**: the R/C/T shape is reused; only the meanings differ. Reduces context-switching cost for raters who know both instruments.

CXO holds the lane on updating CT v2.3 §"How to Extend This Rubric" to cross-reference this rubric.

---

## How to apply (verification walkthrough)

1. Spin up a fresh canonical-test or PM-test account (no prior state)
2. Trigger the rendering surface under audit (e.g., Insight Journal, MUX-lifecycle indicator on standup, COMPOSTED-state archive view)
3. Capture screenshot or transcript of rendering
4. Score R + C + T per the dimension guides above
5. Apply verdict
6. If MARGINAL or FAIL: file as audit-cascade gap item before per-issue gate close
7. If PASS: cite the verification in the issue closure evidence

---

## Cross-references

- Colleague Test v2.3: `docs/internal/testing/colleague-test-rubric.md`
- Canonical Query Test Matrix v3: `docs/internal/testing/canonical-query-test-matrix-v3.md`
- M2d Gate: `docs/internal/planning/m2-structure.md` §M2d (and §M2d gate criteria — consolidated three-way concurrence)
- Methodology-24 Branch-or-Anchor: (see methodology corpus)
- Pattern-063 Parallel-Authoring Drift: `docs/internal/architecture/current/patterns/pattern-063-parallel-authoring-drift.md`

— Authored: PPM (proposed text), Lead Developer (landed); 2026-05-10
