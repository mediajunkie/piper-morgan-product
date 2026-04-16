# Memo: Two Published Posts Need Narrative Correction (PDR-004 Principles)

**To**: Communications Director
**From**: Documentation Management
**CC**: PM, CXO
**Date**: April 16, 2026
**Re**: PDR-004 principles paraphrased incorrectly in two published posts

---

## What Happened

The CXO noticed that a paraphrase of PDR-004's four principles propagated from a Mar 22 omnibus entry into published content. The paraphrase ("presence over performance, specificity as care, honest boundaries, growth through use") does not match the actual PDR-004 principles.

**The canonical PDR-004 principles** (from `docs/internal/product/pdr/PDR-004-experience-philosophy.md`, approved 2026-03-22):

1. **The Session Belongs to the User** — workflows are guests; user redirects always win
2. **Offer-First Activation** — Piper offers; user decides. No auto-capture
3. **Piper Coordinates Understanding** — Piper closes the gap between what participants think they know and what's true
4. **The LLM Floor Guarantee** — always at least as good as a well-prompted LLM with context

## Affected Posts

Both are live and need narrative rewrites, not find-and-replace — the wrong paraphrase is tied to specific design decisions with parenthetical explanations that don't map onto the actual principles.

### 1. The Closing Sprint (Apr 14)
- Blog: https://pipermorgan.ai/blog/the-closing-sprint/
- Medium: https://medium.com/building-piper-morgan/the-closing-sprint-72365b7995ca
- Source: `docs/public/comms/drafts/the-closing-sprint.md`
- Affected passage: "The experience philosophy" section, paragraph starting "But the bigger deliverable was PDR-004..." (lines 61-65)

The current paragraph names four wrong principles and ties each to a specific design decision (floor-first routing, contextual fallback messages, "never say I can't" voice rule, learning system design). The real principles don't map onto these decisions the same way, so this needs a rewrite rather than a substitution.

### 2. Weekly Ship #036: Approaching the Gate (Apr 1)
- Blog: https://pipermorgan.ai/shipping-news/weekly-ship-036-approaching-gate
- LinkedIn: https://www.linkedin.com/pulse/weekly-ship-036-approaching-gate-christian-crumlish-gmhcc/
- Source: `docs/public/comms/drafts/published/weekly-ship-036.md`
- Affected passages: Line 15 (Product & experience section) and line 109 (Weekend reading section)

Line 15 is a brief factual summary. Line 109 is a pullquote format. Both need rewriting with the correct principle names.

## What I'd Suggest

For both posts, open the canonical PDR-004 doc (`docs/internal/product/pdr/PDR-004-experience-philosophy.md`) and quote the actual principle names verbatim. If the narrative wants to tie principles to design decisions, the PDR itself gives the origin stories per principle — those can be used directly.

Once you deliver revised text for each affected passage, I'll update the source drafts and the website's `blog-content.json`, then redeploy. PM is deciding separately whether to edit the Medium/LinkedIn syndicated versions.

## Going Forward

CXO's recommendation (which I've adopted): **when a draft references a PDR/ADR/Pattern by name, confirm the principle names against the canonical source before publication.** I'm proposing we add a "canonical source" header to the draft template listing the canonical doc path for reference. The verification step is lightweight — just open the file — but it prevents exactly this kind of drift.

The fundamental rule: **quote the source; don't paraphrase from memory.**

— Docs
