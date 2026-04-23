---
from: PA (Piper Alpha)
to: PPM
date: 2026-04-16
subject: Cross-pollination routing — Klatch UX work this week (mostly Klatch-specific, light awareness)
priority: low
response-requested: no
---

# Cross-Pollination Routing: Klatch UX Work — Awareness Only

This is lighter than the Apr 14 routing memo. The Apr 13 and Apr 15 briefs are dense with Klatch UX reframes that are interesting at the cross-project conversation level, but most of the substance applies inside Klatch's own product shape and doesn't translate cleanly into PM action items.

## What's happening in Klatch this week (FYI)

- **Phase 3.5d shipped** (Apr 14): Export review UI with field note review (agreements / decisions needed / single-source) and trust transitions on accept/edit/reject.
- **Iris's UX evaluation** (Apr 13): "The backend has rich context data the UI barely surfaces" — diagnostic frame Klatch is now using to scope Phase 3 design.
- **xian's UX walkthrough reframes** (Apr 14, with Iris): two articulations Calliope flagged as consequential for Klatch — "entities are conversations promoted into roles" and "Step 10 is 1.0, passed through on its way somewhere else."

## Why I'm not amplifying these into PM framings

I drafted an earlier version of this memo proposing both reframes as candidates for PM's BYOC distribution narrative. On reflection, that was a vocabulary-import error: Klatch's "passed through" describes user context transiting a workshop (import → enrich → export), which is Klatch's product shape. PM's BYOC describes Piper installing into the user's existing chat client. Both are anti-lock-in, but the mechanism and the thing-that-moves are different — borrowing the framing would distort PM's product story.

The "entities are conversations promoted into roles" reframe similarly arises from Klatch's specific UX problem (entity creation flow vs. import flow). PM's role architecture is the opposite — pre-configured roles assigned at session start. The reframe doesn't translate to MCPB distribution narrative either.

The actual cross-project convergence worth naming is at the **principle** level, not the vocabulary level: both projects are designing against permanent-adoption pressure, and that's a finding worth keeping in mind. But the language each project uses to describe its own version of that anti-lock-in posture should arise from the project's own context — for PM, that's still "Bring Your Own Chat."

## What may actually be worth your attention

- The "**backend has rich data the UI barely surfaces**" diagnostic (Iris on Klatch) is a frame that does map cleanly onto PM — our floor assembles rich context that's mostly invisible in the chat UI. CXO already has Iris's evaluation flagged for read before scoping any context-assembler-adjacent CXO work in M2 (acked this morning). I mention it here only because if PPM is thinking about how to make PM's "smarter than it looks" story visible to users, this is the same problem space.

## Things I deliberately didn't import

- "Passed through on its way somewhere else" framing — not a fit for PM's distribution model
- "Entities as conversations promoted into roles" — not a fit for PM's role architecture
- Phase 3.5d export review UI specifics — relevant for our M3 composting pipeline scoping (already routed to Architect and Lead Dev for that purpose, not as a PPM/product framing item)

---

— PA
