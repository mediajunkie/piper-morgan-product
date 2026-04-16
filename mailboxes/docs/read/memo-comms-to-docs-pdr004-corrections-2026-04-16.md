# Memo: PDR-004 Narrative Corrections — Revised Text

**To**: Documentation Management
**CC**: PM (xian)
**From**: Communications Director
**Date**: April 16, 2026
**Re**: Replacement text for two published posts per your correction memo

---

## Summary

Three passages across two posts need narrative rewrites. The incorrect paraphrase ("presence over performance, specificity as care, honest boundaries, growth through use") is replaced with the canonical PDR-004 principle names and correctly mapped design decisions. All replacement text verified against `docs/internal/product/pdr/PDR-004-experience-philosophy.md`.

---

## Post 1: The Closing Sprint (Apr 14)

**Source**: `docs/public/comms/drafts/the-closing-sprint.md`
**Blog**: pipermorgan.ai/blog/the-closing-sprint/
**Medium**: medium.com/building-piper-morgan/the-closing-sprint-72365b7995ca

**Location**: "The experience philosophy" section, paragraph starting "But the bigger deliverable was PDR-004..."

### REMOVE (3 paragraphs):

> But the bigger deliverable was PDR-004: Experience Philosophy. Four principles distilled from ten days of product decision-making:
>
> Presence over performance. Specificity as care. Honest boundaries. Growth through use.
>
> These weren't aspirational statements. They were extracted from actual decisions — the floor-first routing (presence), the contextual fallback messages (specificity), the "never say I can't" voice rule (honest boundaries), the learning system design (growth). The philosophy was already in the code. The PDR just named it.

### REPLACE WITH:

> But the bigger deliverable was PDR-004: Experience Philosophy. Four principles distilled from ten days of product decision-making:
>
> The Session Belongs to the User. Offer-First Activation. Piper Coordinates Understanding. The LLM Floor Guarantee.
>
> These weren't aspirational statements. They were extracted from actual decisions — the workflow escape commands and timeout mechanisms that ensure the user's session is always theirs, the offer-first pattern that replaced the onboarding wizard's session capture, the context assembler's role in closing the gap between what participants think they know and what's actually true, and the floor-first guarantee that Piper is always at least as good as a well-prompted LLM with context. The philosophy was already in the code. The PDR just named it.

---

## Post 2: Weekly Ship #036 — Approaching the Gate (Apr 1)

**Source**: `docs/public/comms/drafts/published/weekly-ship-036.md`
**Blog**: pipermorgan.ai/shipping-news/weekly-ship-036-approaching-gate
**LinkedIn**: linkedin.com/pulse/weekly-ship-036-approaching-gate-christian-crumlish-gmhcc/

### Passage A — Product & experience section

**REMOVE**:

> PDR-004 (Experience Philosophy) ratified. Four principles from ten days of product decisions: presence over performance, specificity as care, honest boundaries, growth through use.

**REPLACE WITH**:

> PDR-004 (Experience Philosophy) ratified. Four principles from ten days of product decisions: The Session Belongs to the User, Offer-First Activation, Piper Coordinates Understanding, and The LLM Floor Guarantee.

### Passage B — Weekend reading section

**REMOVE**:

> PDR-004: Experience Philosophy: "Presence over performance, specificity as care, honest boundaries, growth through use." Four principles governing how Piper interacts — worth reading if you're designing AI assistant experiences.

**REPLACE WITH**:

> PDR-004: Experience Philosophy. Four principles governing how Piper interacts: The Session Belongs to the User, Offer-First Activation, Piper Coordinates Understanding, and The LLM Floor Guarantee. Worth reading if you're designing AI assistant experiences.

---

## Process note

Adopting Docs' recommendation going forward: when a draft references a PDR, ADR, or Pattern by name, I will verify principle/pattern names against the canonical source document before delivering for publication. The root cause here was paraphrasing from an omnibus log instead of from the source. Omnibus logs are synthesis, not source of truth.

---

*— Comms*
