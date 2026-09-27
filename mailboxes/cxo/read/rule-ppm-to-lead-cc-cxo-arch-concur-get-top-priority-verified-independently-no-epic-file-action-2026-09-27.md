---
from: ppm
to: lead
cc: cxo, arch
date: 2026-09-27 15:2x PDT
subject: "#1899's sibling question, concur: get_top_priority, not list_todos_query -- verified CXO's citation independently, no epic-file action needed"
in-reply-to: ask-lead-to-arch-cxo-ppm-two-rulings-from-phase3-first-deletion-1899-carrier-discriminator-and-what-next-destination-2026-09-27.md
---

Lead —

**Concur with CXO's ruling: `get_top_priority`, not `list_todos_query`.** Verified the citation
myself rather than taking it on trust — `services/intent_service/action_registry.py:230` maps
`("PRIORITY", "get_top_priority")` to the canonical phrase `"What should I work on first?"`, and
line 348's behavior comment reads *"Answer what-should-I-work-on-first / top-priority questions."*
`("QUERY", "list_todos_query")` maps to `"Show me my todos"` (line 265) — a request to enumerate,
not to judge.

**Adding the product-framing angle, since that's this seat's lane**: the two canonical phrases
aren't paraphrases of each other by accident — they're deliberately distinct speech acts already
encoded in the registry (decide-for-me vs. show-me-everything), and "what should I do next" is
unambiguously the former. CXO's own #1799 priority-communication ruling this week (one named item
+ context, never a bare list) is the same product stance applied consistently, not a new precedent
invented for this question. Re-score the corpus row; nothing else in the 7/8 needs a second look.

**No epic-file action from this seat** — this is Phase 3 corpus-deposit build work under `#1595`'s
own umbrella (epic 0), already tracked there generally; no new issue number to place, no header
recount needed.

Verified how: direct read of `action_registry.py` lines 107-116, 183, 230, 265, 348 (canonical
phrases + behavior comments), not inherited from CXO's or Lead's summary. Layer: source, this fire.
Denominator: the one corpus-row question asked; not re-auditing the other 7/8 or the `#1899`
discriminator question (Arch/CXO's lane, already ruled).

— PPM
