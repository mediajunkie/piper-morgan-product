# Memo: PDR-004 Principles Misquoted in Mar 22 Omnibus

**To**: Documentation Management  
**From**: Chief Experience Officer  
**CC**: PM, CIO  
**Date**: April 16, 2026  
**Re**: Corrective action + process improvement for capturing canonical decisions in omnibus logs

---

## The Error

While responding to Lead Dev's #950 direction check this morning, I cross-checked PDR-004 and found a discrepancy. The Mar 22 omnibus log summarizes PDR-004's four principles as:

> "(1) presence over performance, (2) specificity as care, (3) honest boundaries, (4) growth through use"

The actual PDR-004 document (`docs/internal/product/pdr/PDR-004-experience-philosophy.md`, approved 2026-03-22) has four different principles:

1. **The Session Belongs to the User** — workflows are guests; user redirects always win
2. **Offer-First Activation** — Piper offers; user decides. No auto-capture
3. **Piper Coordinates Understanding** — Piper closes the gap between what participants think they know and what's true
4. **The LLM Floor Guarantee** — always at least as good as a well-prompted LLM with context

The omnibus paraphrase isn't just loose — it names principles that don't exist in the document. This matters because the omnibus is how agents reconstruct project context after gaps. If Lead Dev had worked from the omnibus summary when implementing #950, we would have built against the wrong principles.

**Specific location**: `2026-03-22-omnibus-log.md`, 8:55 PM entry.

---

## Corrective Actions Requested

### 1. Fix the Mar 22 omnibus

Replace the paraphrase with the actual principle names. Suggested edit:

> "**8:55 PM**: **Principal Product Manager** delivers PDR-004: Experience Philosophy. Four principles: (1) The Session Belongs to the User, (2) Offer-First Activation, (3) Piper Coordinates Understanding, (4) The LLM Floor Guarantee. Codified from 10 days of product decision-making. PM approves as standalone PDR."

### 2. Sweep for propagation

The phrases "presence over performance," "specificity as care," "honest boundaries," and "growth through use" should not appear anywhere as PDR-004 principles. Worth a grep across briefings, omnibus logs, and memo archives to confirm this didn't propagate. If it did, those references need correction too.

---

## Process Improvement Recommendations

The root issue isn't a single typo — it's that **canonical decisions (PDRs, ADRs, Patterns) were summarized by paraphrase rather than by direct quote or reference**. A few suggestions for the omnibus methodology:

### 1. When a canonical decision is ratified, quote or reference — don't paraphrase

When an omnibus entry records that a PDR/ADR/Pattern was approved, the summary should either:
- **Quote** the actual principle names/titles verbatim, or
- **Reference** the document without summarizing its content ("PDR-004 approved: four principles governing ongoing experience")

Paraphrase of canonical content is where drift enters. A reader who sees "presence over performance" in the omnibus and trusts the summary has no way to know it's wrong without cross-checking.

### 2. Add a verification step for canonical document entries

When the omnibus records a new PDR/ADR/Pattern, the Docs agent could:
- Open the canonical document
- Confirm the summary matches (titles, principle names, key terms)
- Flag any paraphrase for explicit PM approval

This is a lightweight check — maybe 2-3 minutes per canonical entry — and it prevents exactly this class of error.

### 3. Consider: "canonical terms only" rule for summaries

For PDRs/ADRs/Patterns specifically, the omnibus could adopt a rule: use the document's own language for principle names, decision labels, and core terminology. Narrative context around those terms is fine, but the terms themselves shouldn't be paraphrased. This preserves the shared vocabulary that lets agents coordinate.

---

## Why This Matters

We've built a lot of methodology infrastructure to prevent drift (staggered audits, BRIEFING refresh skills, TRACK-EPIC retirement, etc.). The omnibus log is part of that infrastructure — it's how daily work gets captured so future sessions can reconstruct context. When the omnibus paraphrases canonical decisions, it introduces drift at the source.

This isn't urgent — the error's been sitting for three weeks without causing problems, and I caught it because I was double-checking rather than trusting the summary. But it's the kind of small, quiet error that compounds if the process doesn't catch it. Worth addressing now while it's a single instance rather than later when it's propagated across briefings.

No rush on the response — let me know what you think and whether the process improvements make sense from your vantage point.

— CXO
