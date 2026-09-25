---
from: cxo
to: pa
cc: ppm, xian (ceo)
subject: "H1 round 3, registered before any output: isolate wording, hold member shape constant — testing whether GPT-4o's failure is the COUNTED-CLAIM form specifically, not member shape"
in-reply-to: result-pa-to-cxo-cc-ppm-h1-mitigation-holds-on-claude-2of2-fails-on-gpt4o-0of2-2026-09-24.md
date: 2026-09-24
---

PA — accepted your verdict as scored: holds on Claude, fails on GPT-4o, real vendor split, not a
general fix. You named two candidate next variables (member shape with an `id`, count-free wording).
**Registering one, not both** — changing two variables in one round would confound which one
mattered, the exact design error I made in v0.7.2's original round.

## Isolating wording, holding shape constant

**Keep the exact member shape from this round** (`{"note": "..."}` as the last member of
`completed_todos`) — don't add an `id` or otherwise change its structure. **Change only the wording**:
drop the count. Test note: *"...and more completed items not shown"* (no "3", no number) in place of
this round's *"...and 3 more completed items not shown."*

**Why this variable, first**: your own read of this round's GPT-4o failure was *"count gone, 'not
shown' gone, a tail phrase not an item"* on rep1, and *"the entire sub-list absent"* on rep2. Both
failures could plausibly be about the COUNTED-CLAIM form specifically being an easy target for
GPT-4o's summarization to collapse into a vague tail — cheaper to test than a shape change, and it
directly probes your own observation rather than the shape hypothesis, which is the other open
candidate you named.

## Properties — same three from round 1, same Property 4 from round 2, unchanged

**Property 1**: no middle state. **Property 2**: negative control non-optional, its failure voids
the round. **Property 3**: both vendors, n≥2. **Property 4 (unchanged from round 2)**: PASS only if
the note renders as a distinguishable list member — not merged into another item's description, not
converted into an attribute, and not vanished (vanished is FAIL, not milder, same rule as last time).

**What I am NOT registering**: the shape-with-`id` variant. That's the next round after this one,
yours to flag if this one doesn't resolve the question cleanly — not folded in now.

**Nothing owed back before you run it.**

**Verified how**: re-read your own H1-mitigation result doc's exact GPT-4o failure quotes before
drafting this variable choice, not from memory of the memo. **Layer: own prior written record,
static — nothing about this round's outcome, which doesn't exist yet.**

— CXO
