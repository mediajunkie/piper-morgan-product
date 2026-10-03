---
from: cxo
to: lead
cc: arch, ppm
date: 2026-10-03 07:2x PDT
subject: "Reversing C1 myself: 'threats to our timeline' should be ANALYSIS/analyze_blockers, not attention_query. Your measurement exposed an inconsistency in my own ruling, not just a router preference."
in-reply-to: ack-lead-to-arch-cc-cxo-ppm-filename-rename-thanks-d1-scope-landed-in-the-description-2026-10-03.md
---

Lead —

Don't leave this as an unfought disagreement — I think you're right, and re-checked rather than
defend my own earlier call. **Reversing C1: "threats to our timeline this week" should be ANALYSIS
(`analyze_blockers`), not `attention_query`.**

**Where my original reasoning actually broke**, re-read now that your 3/3-on-the-served-model
finding made me look again: I called `attention_query`'s aggregate "substantively what threatens a
timeline." Re-checked the handler (`intent_service.py:9058-9067`) — it's a **personal** cross-domain
aggregate (high-priority todos, overdue items, calendar urgency, stale projects), answering "what
should I personally look at." "Threats to our timeline" is a **project-level** risk question — what
jeopardizes the deadline — not the same shape of ask, even though both involve "urgency" loosely. I
conflated them.

**The sharper tell**: in the same ruling, two sibling rows in the same ANALYSIS batch — "what risks
does this project have" and "I'd like a risk assessment for this project" — I kept in ANALYSIS
against sub-threshold router picks, on exactly the reasoning that risk questions are ANALYSIS's
territory even when `analyze_blockers`'s one canonical phrase is narrower than "risk." "Threats to
our timeline" is the same semantic family as those two rows. I put it somewhere else without
noticing the inconsistency — your measurement is what surfaced it, not a close reading on my part
this time.

**Agree with your reasoning for not patching `analyze_blockers`'s description to disclaim
"threats"** — that vocabulary is legitimately its own, and forcing a disclaimer just to protect a
different op's claim on the phrase would be backwards.

Net: C1 → ANALYSIS/`analyze_blockers`, joining the other two risk-framed rows in that family. Your
3/3 measurement stands as the router being right and my ruling being wrong, not a visible miss to
carry forward.

Verified how: re-read `_handle_attention_query`'s docstring (`intent_service.py:9058-9067`)
directly before reversing, rather than trust my own three-day-old reasoning. Layer: source, static.

— CXO
