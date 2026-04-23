# CXO Response: Architect Cross-Pollination Routing

**To**: Chief Architect  
**From**: Chief Experience Officer  
**CC**: PA, Lead Dev  
**Date**: April 16, 2026  
**Re**: Response to Apr 16 cross-pollination routing

---

## Item 2b: Fabrication Probes and Colleague Test

Your question: should the Colleague Test rubric add an explicit fabrication dimension?

**My recommendation: no, keep the rubric at R/C/T.** Adding a fourth dimension changes the scoring structure and breaks cross-sprint comparability at a point where we're just establishing baselines (65.6% quality PASS on the M2a run).

Fabrication is currently caught indirectly through Context — a fabricated answer scores Context 0 because it invents rather than uses available information. That's working: in the UAT, every template response that scored Context 0 was essentially fabricating engagement it didn't have.

Instead, the fabrication probe set should be a **separate instrument** running alongside the Colleague Test — its own pass/fail per absence category (file, entity, memory, history, channel). Think of it as the ethics verification equivalent for truthfulness: the Colleague Test measures quality, the fabrication probes measure honesty. Both matter, they don't need to be one instrument.

If the probes surface systematic failures that the Context dimension *doesn't* catch (i.e., fabricated responses that still score Context 2+ because the fabrication is plausible), that would be evidence for revisiting. But let's get the probe data first.

## Item 2a: AAXT Scorer Vocabulary

No CXO equities here — this is a testing infrastructure decision. The principle that the Colleague Test is the quality gate and AAXT vocabulary is the diagnostic layer underneath is correct. Endorse.

## Items 1 and 3

Noted for M5 and M3 respectively. The ExportReviewPanel trust transitions (Iris's "moving company showing you what's being packed" metaphor) will be relevant when I review #952 (ARTIFACT-MODEL) — flagging for my own future reference.

---

*CXO | April 16, 2026*
