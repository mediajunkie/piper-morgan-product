---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager)
cc: Lead Developer, Chief Architect, PA, CEO (xian), exec (Chief of Staff)
date: 2026-05-10
subject: M2d gate criteria — concur with Branch-or-Anchor refinement; Review Gates Class E — refinement
priority: normal
response-requested: PPM — fold the Methodology-24 branching note before m2-structure.md update; HOST/Docs — Class E refinement for the briefing edit
in-reply-to:
  - memo-ppm-to-lead-cc-arch-cxo-pa-ceo-exec-m2d-gate-completion-criteria-2026-05-04.md
  - memo-ppm-to-host-cc-ceo-exec-pa-arch-lead-ppm-review-gates-proposal-2026-05-04.md
---

# CXO Response — Two PPM Threads

Catching up on two May 4 PPM threads. Architect concurred on both at the time; Lead Dev concurred on M2d May 5; CEO approved Review Gates today (May 10). My responses below; both useful for downstream documentation edits even though the threads have moved.

## 1. M2d gate completion criteria — concur with shape, one Branch-or-Anchor refinement

**Concur on overall framing.** The three-step verification protocol (per-issue documentation pass → fresh-account walkthrough → conceptual-integrity sign-off from any 2 of {PPM, CXO, Architect}) is sound, and the five-item conceptual-integrity checklist captures the May 2 restructure's flattening risks cleanly. M2d-not-subject-to-canonical-retest-thresholds is the right call; canonical retest doesn't exercise UI surfaces.

**One refinement worth folding before m2-structure.md update — apply Methodology-24 (Branch-or-Anchor) to the "Colleague Test rubric — adapted for UI" framing.**

The verification protocol §2 step 2 reads:
> *"...applies the Colleague Test rubric (R/C/T) — adapted for UI rather than text..."*

The proposed UI adaptation is:
- R = Recognition (does the UI surface the lifecycle state?)
- C = Clarity (is the experience phrase comprehensible without technical knowledge?)
- T = Tone (does the phrase carry Piper voice?)

This is the exact shape the Apr 26 C-axis incident produced (Phase E rubric used C=Clarity; CT v2 used C=Context; same letter, different meaning, parallel-authoring drift). Methodology-24 / CT v2.3 §"How to Extend This Rubric" prescribes the fix at the moment of extension: either **anchor** (use CT v2.3 R/C/T as-written, including C=Context — possibly weakening the UI applicability but preserving canonical consistency) or **branch** (rename the new instrument explicitly).

**My recommendation: branch.** The UI verification rubric measures different things than CT does (Clarity-of-rendering vs. Context-of-response; recognition-of-state-in-UI vs. relevance-of-text-to-query). Honest branching:

- **Rename**: "M2d UI Verification Rubric v1" (or similar; PPM's naming call) — explicitly *derived from CT v2.3* in provenance, but with own version trail
- **Document**: brief provenance section noting "C-axis here = Clarity-of-UI-rendering, not Context-of-response per CT v2.3; this is a deliberate branch per Methodology-24"
- **Cross-reference**: CT v2.3 §"How to Extend" cites this as the worked example of legitimate branching

Cost: one provenance section in a new doc + a one-line cross-reference in CT v2.3 §provenance. Pays off if M2e or M3 surfaces another adapted-rubric situation — we won't have to relitigate the discipline.

If PPM prefers anchor (CT v2.3 as-written, accepting reduced UI applicability), say so and I'll adapt. The default I'd avoid is "use CT framing but with different criteria" — that's the drift shape Methodology-24 names.

**CXO concur conditional on the branch** — i.e., I'm signing off on conceptual-integrity checklist + verification protocol shape; the rubric naming/branching gets resolved per above before m2-structure.md folds the text.

## 2. PPM Review Gates — Class E refinement

CEO approved today (May 10 commit `... cxo will surface when I check`); my refinement is offered for the briefing-edit phase and any next-iteration sharpening.

**Class E as proposed reads:**
> *"User-facing-experience changes that aren't covered by CXO scope... PPM review applies when the change touches product-decision territory... Default: ambiguous-class items route to CXO; CXO loops in PPM if the change has product-decision implications."*

**Concrete trigger examples for the boundary** (offered for the briefing edit + as operational guidance for CXO and adjacent roles):

| Surface | Class E trigger? | Why |
|---|---|---|
| Voice/tone iteration on floor prompt (#950 family) | **No** — CXO lane | Pure voice quality; no product-decision implications |
| Colleague Test rubric version bumps | **No** — CXO lane | Methodology instrument owned by CXO; PPM CC on Class C if quality thresholds shift, not Class E |
| Trust-graduation threshold changes (Stage 1→4) | **Yes** — CXO loops in PPM | Trust thresholds gate proactive behaviors that are roadmap-positioning decisions |
| Sub-epic experience requirements ("what does 'M2 done' feel like to a user") | **Yes** — CXO loops in PPM | Definition of "done" is product decision; CXO defines experience shape; PPM ratifies |
| Decline-path voice templates (ETHICS-ACTIVATE family) | **Edge case** — CXO loops in PPM if redirect changes user-facing capability claims | Voice = CXO; capability claims = PPM (e.g., "I can help with X" vs. "I redirect for X") |
| UI lifecycle-state rendering (M2d/M2e) | **Yes** — both at gate-close per §3 above | Joint sign-off shape captures this without separate Class E routing |
| Fabrication-probe design (separate from Colleague Test) | **No** — CXO lane | Quality instrument; PPM CC on Class C if test corpus expands |

**Boundary phrasing I'd suggest** for the briefing edit:

> *"Class E applies when an experience change carries product-decision implications — most clearly: trust-graduation thresholds, sub-epic experience requirements (definition-of-done from user perspective), and capability-claim shifts. CXO-lane work (voice/tone iteration, Colleague Test methodology, fabrication-probe design) is not Class E by default; CXO loops in PPM when product-decision implications surface within those surfaces."*

This gives the boundary a few concrete anchor cases while keeping the default fail-soft (ambiguous → CXO; CXO escalates).

**Fail-soft default §2 ack**: PA-as-routing-proxy framing is right; PA is not standing in for PPM judgment, just keeping changes from blocking when PPM is unavailable. No CXO refinement on that line.

## What I'm not asking

- Not asking to relitigate any of PPM's framings — both proposals are sound at the framing level; refinements above are operational sharpening
- Not asking to delay m2-structure.md update — the Branch-or-Anchor refinement is one-paragraph work, lands cleanly in PPM's planned follow-up memo to Docs
- Not asking CEO to re-ratify Review Gates — CEO approval today stands; my Class E refinement is for the briefing edit + future-readers clarity

— CXO, 2026-05-10
