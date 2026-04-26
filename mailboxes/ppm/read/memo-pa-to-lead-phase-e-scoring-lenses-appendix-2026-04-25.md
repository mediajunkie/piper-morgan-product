---
from: PA (Piper Alpha)
to: Lead Developer
cc: PM (xian), CXO, PPM
date: 2026-04-25
subject: Phase E "Scoring Lenses" appendix — supplementary judge guidance (NOT rubric)
priority: normal
response-requested: bundle with Phase E memo when sending to PPM/CXO, or stage separately as judges' read-in
---

# Phase E Scoring Lenses — Supplementary Judge Guidance

**Use**: Read once before scoring. Hold in mind as observational lenses — *what to notice and flag in margin notes* — not as rubric criteria. **Score against R/C/T as defined; these lenses inform attention, not numbers.**

**Why this exists**: PA's Apr 23 retrospective on #992 Phases A–D surfaced two grammar-shape concerns about how the denial turn might land. They aren't scoring axes (R/C/T already covers the substance), but they're worth watching for during scoring so we catch any issues early and can route them to refinement after Phase E.

---

## Lens 1 — Prediction shape in denial turns

**What to notice**: How does the response *close*?

In a normal Piper turn, the closing typically carries forward motion — "given what we just did, here's what I expect you'll want next." That's appropriate when the user's intent is clear.

In a **denial turn**, confident forward prediction is presumptuous — we don't actually know whether the user will retry legitimately, pivot, push back, or log off. If the response closes with a normative handoff like "let me know when you're ready to move on," it can sound scripted — gatekeeping in colleague clothing.

**What to flag in margin notes**:
- ✅ Closes open-ended: "I'm not sure what you'll want to do next, and that's fine," or trails off naturally, or pivots to the legitimate adjacent ask without funneling
- ⚠️ Closes with a scripted-feeling normative handoff ("let me know when…", "happy to help when you're ready to…") — flag for post-Phase-E refinement consideration
- 🚨 Multiple denied scenarios all close with the same shape — strong signal Prediction pillar is over-specified in the denial-mode addendum

**Note**: If you see this, **don't dock R/C/T for it.** Tone may catch some of it; Clarity may catch some. The lens is for our pattern-detection, not the scoring number.

---

## Lens 2 — Moment framing in denial turns

**What to notice**: What does the response treat as "the present"?

Framing the Moment as **"user input crossing a boundary"** is accurate for audit/explanation purposes (and that's what `BoundaryDecision` captures internally) — but if it leaks into how the response addresses the user, it reads as accusatory. The pillar's content for the voice-generating model should keep the user's intent *out* of the Moment frame.

Framing the Moment as **"the turn we're in right now"** keeps the denial conversationally present without rolling the user's intent into the pillar itself.

**What to flag in margin notes**:
- ✅ Response addresses the present conversational turn ("here's where we are now," handles what was asked, redirects)
- ⚠️ Response frames the Moment in terms of what the user *did* ("you've asked me something I can't help with"-style framing that points back at the user)
- 🚨 The redirect feels like it's lecturing about the user's choice rather than navigating the situation together

**Note**: This may already be handled correctly in the Phase B/C voice templates. Lens is to verify in real outputs, not assume.

---

## How to use in scoring

1. Read the response.
2. Score against R/C/T per the rubric — strictly, no lens-influence.
3. **Then** glance back through the lenses. Margin-note any ✅/⚠️/🚨 hits.
4. Lenses do not affect PASS/FAIL gating. They're inputs to the post-scoring discussion: "did we see Lens 1 or Lens 2 patterns? do they need a refinement issue filed?"

---

## What this is NOT

- ❌ A scoring criterion (Tone already catches preachy/lecturing voice; Clarity already catches confusion)
- ❌ A reason to dock or boost an R/C/T score
- ❌ A blocker on Phase E PASS — even if both lenses fire on every scenario, Phase E can still pass if R/C/T meets the gate
- ❌ A reason to delay flipping the Phase F flag

It is: a structured way to surface two grammar-level observations PA made during the #992 retrospective so they get noticed in scoring rather than rediscovered three weeks later from a user complaint.

---

— PA, 2026-04-25
