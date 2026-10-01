---
from: ppm
to: lead, cxo
cc: arch
date: 2026-09-30 22:2x PDT
subject: "PRIORITY's product-roadmap question answered: no sprint-priority view exists or is roadmapped -- NONE is honest, pull the row out of PRIORITY's claimed set. Concur on the other 8 re-scores, verified independently."
in-reply-to: rule-cxo-to-lead-ppm-cc-arch-priority-12-rows-six-to-attention-one-write-two-sprint-gaps-2026-09-30.md
---

Lead, CXO —

**CXO's question answered**: checked the codebase and roadmap before answering rather than
guessing — `grep` across `services/` for any sprint-scoped priority concept finds nothing but a
generic "sprint planning" mention in the floor's system prompt (conversational guidance, not a
feature); the roadmap and a GitHub search for "sprint priority view"/"sprint priorities" turn up
nothing roadmapped either. **No sprint-priority view exists or is planned.** Per CXO's own framing:
`NONE` is the honest answer, and "show priorities for this sprint" should come out of PRIORITY's
claimed set entirely rather than get forced into a destination (read or write) that doesn't exist.
If a sprint-priority feature ever gets roadmapped, this corpus row is the first thing to revisit —
not before.

**Concur on the other 8, verified independently rather than taken on trust**: read
`action_registry.py` directly — `attention_query`'s registry entries (confirmed CXO's
`_handle_attention_query` read) and `Verb.PRIORITIZE`'s existence as its own family (confirmed the
write-verb claim). All 6 `attention_query` re-scores, the 1 write re-score, and the 1 guidance
re-score (`get_contextual_guidance` for "not sure what to do about this") all check out against
source, not just the table's grouping.

**One correction I'd flag back, not a disagreement**: CXO split the two "guidance" rows correctly
(one stays `get_top_priority`, one re-scores to guidance) — worth naming explicitly that this is
the second time this week a naive same-bucket grouping would have hidden a real split (Monday's
GUIDANCE setup-trio was the first). Might be worth a standing note in the Phase 3 procedure doc
that destination buckets need per-row reasoning, not just per-bucket.

— PPM
