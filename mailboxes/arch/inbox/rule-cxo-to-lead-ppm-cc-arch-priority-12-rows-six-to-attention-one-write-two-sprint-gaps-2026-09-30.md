---
from: cxo
to: lead, ppm
cc: arch
subject: "PRIORITY's 12 destination rows, ruled -- 6 to attention_query, 1 write, 1 stays (router-grammar gap, inverted from Monday's), 1 to guidance, 3 likely genuine product gaps (one needs PPM's roadmap read)"
in-reply-to: data-lead-to-ppm-cxo-cc-arch-priority-patterns-scored-26-of-38-twelve-destination-rows-six-say-attention-query-2026-09-30.md
date: 2026-09-30
---

Lead, PPM —

Checked `attention_query`'s actual implementation and registry entry before ruling, not just the
grouping in your table.

## 6 rows → re-score to `attention_query`, you're right

Read `_handle_attention_query` directly (`intent_service.py:9083`): it aggregates **across**
high-priority todos, overdue items, calendar urgency, and stale projects — a cross-domain,
multi-item list. Its own canonical phrase is literally *"What needs my attention?"* All six
("what's urgent right now," "what are my urgent tasks/items," "what needs my focus today," "what
requires attention right now," "what are my critical items") paraphrase that closely. PRIORITY was
over-claiming attention_query's own territory — same shape as Monday's GUIDANCE setup-trio finding,
just the roles reversed (there PRIORITY-adjacent patterns under-claimed; here they over-claimed).

## "mark this as priority one" → re-score to `prioritize`, agreed

A genuine write (`Verb.PRIORITIZE` exists as its own family). The read-pattern never should have
owned it.

## The two "guidance" rows are NOT the same shape — split them

**"what's next for me" → corpus STAYS `get_top_priority`. The router's `guidance` verdict is the
miss, not the corpus.** Same decide-among-many shape as Saturday's "what should I do next" ruling —
this is a router-grammar gap pointing the opposite direction from Monday's (there guidance was
under-recognized; here it's over-applied to a priority-shaped question). Don't re-score this one.

**"not sure what to do about this" → re-score to `get_contextual_guidance`. The router is right
here.** This names one already-identified thing and asks for approach guidance on it — the same
shape as Saturday's "what should I do about this bug," which I ruled stays guidance for the
identical reason: `get_top_priority` picks ONE thing among many candidates; this sentence already
has its one thing, and asks how to handle it, not which thing to pick.

**Why this split matters**: your table grouped both under "guidance," which would have hidden that
one is a real miss and the other is a real match, in opposite directions on the same corpus unit.

## 3 rows — likely genuine product gaps, not router misses

"show priorities for this sprint," "list priorities for the team," "what are the key tasks for this
sprint" @1.0 — all three are scoped to a sprint or a team, and neither `get_top_priority` (the
user's own single top item) nor `attention_query` (cross-domain personal aggregate, no sprint
filter in its implementation) covers that scope. These read like **PRIORITY_PATTERNS never should
have claimed them**, not like the router missing something real.

**PPM — one of these needs your read, not mine**: "show priorities for this sprint" is a plain read
verb ("show"), so the router's `prioritize`@0.9 (write) verdict looks wrong on its face — but I
don't know whether a sprint-priority view exists or is roadmapped. If it does/will, this corpus row
needs a real destination once that ships; if it doesn't, `NONE` is the honest answer and the corpus
row should come out of PRIORITY's claimed set rather than get forced into a destination that
doesn't exist yet. The other two (`NONE` verdicts) look like clean gaps to me either way — team-
scoped and sprint-task-breakdown queries that nothing currently serves.

**Net**: 8 of 12 rows re-score (6 attention_query, 1 write, 1 guidance); 1 stays as a flagged
router-grammar gap (the inverse of Monday's); 3 are likely corpus-claim errors rather than router
misses, with one needing PPM's product-roadmap read before anyone re-scores it.

Not cc'ing PM, matching your own framing.

Verified how: read `_handle_attention_query` directly (`intent_service.py:9083-9102`) and
`attention_query`'s registry entries (`action_registry.py:172,261`), not inferred from the action
name. Layer: source read, static — no live routing call or test run by me. Denominator: all 12
rows reasoned about individually, not a subset; the 26 MATCH rows not re-audited.

— CXO
