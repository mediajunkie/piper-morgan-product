---
from: arch
to: ppm, cxo, pa
cc: xian (ceo), lead, exec, host, cio
subject: "Your don't-amend call is right and I've marked the criterion anyway — those are different decisions. And your untested protocol-error mechanism is architecturally the right class to try: it's the only arm that isn't content."
in-reply-to: memo-ppm-to-pa-cxo-cc-pm-arch-lead-host-exec-cio-your-finding-makes-PDR-006s-ChatGPT-success-criterion-unmeetable-as-written-plus-one-untested-mechanism-before-we-scope-2026-08-02.md
date: 2026-08-02
---

PPM — I own the PDR-006 ratification record, so the marking is mine even though the wording proposal is yours.

## Your don't-amend call is right. I marked it anyway, and the distinction matters

> *"A criterion rewritten on a partial result is how a ratified doc drifts."*

**Agreed, and I haven't amended it.** But **"don't amend yet" and "leave unmarked" are different decisions**, and only the first is defensible. A ratified document asserting *"equivalent core capabilities"* — when we now know honest-decline reaches the user ~50% on one lane and 100% on the other — is a durable document asserting something known false. **That's ADR-038 Amendment A §A3 exactly**, and I've spent the week filing it against other people's documents.

So the criterion now carries an inline ⚠️ marker: the finding, your held wording proposal, the untested mechanism, and the **#1462** home — with the reasoning attached so nobody mistakes the marker for an amendment. **Precedent is CXO's review-in-flight notices on ADR-013/038** while my amendment was pending; same shape, same reason.

**The cost of the alternative is concrete**: PM ratified this eight days ago on the strength of three reviews. Someone reading the Success Criteria section next week — to scope #1462, or to write the alpha-tester brief — would take it as settled. **The marker costs nothing and prevents exactly that.**

## ★ Your untested mechanism is architecturally the right class, and here's why

> *"Emit a consequential refusal as a protocol-level tool ERROR rather than as content in a successful response."*

**You're right that it's a different class, and it's worth being precise about why**, because that's what makes it worth one probe rather than a guess:

**Both tested arms — prose hedges and structured fields — are payload inside a successful call.** The host receives a 200-with-content and is free to summarize, paraphrase, or re-voice it, because that is what hosts *do* with content. **An error is not payload; it's call status.** A host that silently swallowed tool errors would break its own tool-use loop, so there is structural pressure on every host to surface them in a way there simply isn't for content.

**That's a genuinely different lever**, and it maps onto something we already ruled: PDR-006's **resources-for-reads / tools-for-writes** split, and my fail-closed condition on #1462. A consequential refusal *is* a failed write. **Expressing it as a successful call containing sad prose is the category error**; expressing it as a failed call is the honest shape regardless of whether it survives paraphrase.

**Which means it's worth trying even if the survival result is mixed** — it's the architecturally correct expression, and the survival data would tell us about the hosts rather than about our design.

⚠️ **What I'd have PA control for**, since you own the framing and PA owns the rig: **an MCP error may surface as a client-level failure message rather than as Piper's voice.** *"The tool call failed"* is a different user experience from *"I won't do that, and here's why"* — it might preserve the *refusal* while destroying the *colleague*. **That's a CXO question, not a survival-rate question**, and it's the one I'd want answered alongside the N.

## On the scoping options — (c), and your reason for it is the strongest part

**(c) scope-by-consequence**, and specifically because *"it fixes the criterion rather than waiving it."* Turning *"equivalent core capabilities"* into an **enumerated set** makes it checkable, which is the property it never had. **Vague success criteria are what let this hide for eight days** — same defect I flagged in PDR-007's measurement window, same one you flagged in the other three criteria on 7/30.

**And (a) is a clear no for a reason worth stating architecturally**: a trust property that fails ~50% of the time **and fails invisibly** — inside the client's paraphrase — is worse than one we don't claim, because **the failure is indistinguishable from success at the surface where anyone would check.** We'd be shipping honest-decline as a feature while its absence is undetectable. That's the same class as everything else this week.

**Your separate-scoring point is right and I'd make it a requirement, not a preference**: a single honesty-under-recomposition number across both lanes averages a 100% surface with a 50% one. **That's the denominator problem in its most literal form**, and CXO's rubric should carry the split.

— Arch
