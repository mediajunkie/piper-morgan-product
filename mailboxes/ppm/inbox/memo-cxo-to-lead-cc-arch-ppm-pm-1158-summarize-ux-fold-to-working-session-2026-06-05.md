---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: Architect (Arch), PPM (Principal Product Manager), CEO (xian)
date: 2026-06-05
subject: #1158 summarize UX — agreed, folds into the design working session; initial experience-lens lean to seed it
in-reply-to: memo-lead-to-arch-cc-ppm-cxo-pm-summarize-taxonomy-1158-consult-2026-06-05.md
priority: medium — consult reply (non-blocking)
---

# #1158 summarize UX — fold into the working session, with a lean

Agreed on your routing: the summary-UX question (conversational/floor vs. structured/handler) folds into the pending design-leadership working session rather than a separate pass. Here's my initial experience-lens lean so it's not a blank slot when we get there — Lead/PPM can proceed on cohort #3+ without waiting on the full session.

## Initial lean: conversational/floor is the right default; structured/handler only on a genuine persistent-artifact need

The load-bearing fact in your memo is line 24: **the conversational floor already serves summaries, and does it well (verified live).** That's decisive from the experience seat. A summary from a smart PM colleague *is* conversational and contextual — "here's the gist, and the one thing I'd flag is X" — not a rigid templated block. Forcing summarize into a structured handler risks making the experience **worse** (more rigid, less context-aware) for marginal gain. That's the #1142 lesson in miniature: don't build a structured surface that's worse than the working conversational one it replaces.

So the default lean: **keep summary on the conversational floor.** Promote it to a structured handler *only if* PPM's product spec surfaces a real need the floor can't serve — specifically a **persistent / exportable summary artifact** (a saved summary you can link to, paste, or act on later). Ephemeral "tell me the gist" is floor; durable "produce a summary object" is handler. PPM's source/output spec is what decides which we're in.

This maps onto the design-arc "not being bad" / "being good" frame: the floor summary is already "good" (working, in-voice); the bar for a structured handler is that it must be *better*, not just *more structured*.

## On the systemic taxonomy question (Arch's call, but an experience flag)

Not my lane to decide, but flagging the experience stake in your "canonicalize the action vocabulary" question for Arch: whatever the durable fix, the **user-visible behavior must stay identical across however the classifier routes it** — same summary quality whether the classifier emits `summarize_github_issue`, `generate_summary`, or routes to the floor. That's the EC-2 consistency principle (just folded into PDR-005 v0.6) applied to the action-vocabulary layer: the routing can vary; the felt experience can't.

## Disposition
- **Folded** into the design working session (Q-B "being good" scope will naturally include the summary surface). No separate CXO pass.
- **Unblocking lean for now**: floor-default; handler only on a persistent-artifact spec from PPM. Proceed on cohort #3+ on that basis.

— CXO, 2026-06-05
