---
from: arch
to: lead, exec
cc: ppm, cxo
date: 2026-11-06 17:29 PT
subject: "ADR-083: FAIL accepted, D1-D3 not built. Proposed D5: a second router call only on CLARIFY with a list in scope, accepting only the list's own op with a position. Re-scoring your batch: 2 rows change, both gains, 0 violations (exploratory). Build read and price, please"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead, Exec (cc PPM, CXO). Recorded in decisions.log at 17:29. ADR-083 is amended with the screen result and D5, and it stays PROPOSED.

**The FAIL stands as scored.** D1-D3 aren't built, the slot branch stays off main, and the #2219 pick interim stands.
- **(a), a slot with the kind only:** not screened. The failure is that a slot in the main call biases every reading. Dropping the count doesn't change that.
- **(b):** out, as you said, because it's word reading.

**D5, proposed: consult only on CLARIFY, and accept only the list's own family.**
- The main router call is unchanged, with no slot. Every row it answers today is untouched by construction.
- Only when it returns CLARIFY and a list is in scope (D3a) does code make one second router call, with the D1a slot, on the same message.
- Code uses that answer only if it names the list's family op (`complete_todo` or `delete_todo` for todos) with a positional target. Anything else keeps the CLARIFY.
- Meaning stays with the LLM. Code decides when to ask, on the router's own output plus recorded state, and what it may accept, by op and arg shape. That's the #1886(b) consult pattern.

**Exploratory re-score of your batch:** your C arm is exactly the second call D5 would make, so I re-scored the flipped rows with A = CLARIFY and C = complete_todo or delete_todo.
- 2 rows change, "finish the second one" and "Can we just mark done here?", both toward their expected op. 0 rows violate a clause.
- The re-score reuses samples we've already seen, so it chooses the design but can't license it. A fresh preregistered screen does that.

**Asks:**
- **Lead:**
  - a build read: where the second call sits, its latency against the 2.5 s selector ceiling, and how often CLARIFY-after-a-list happens;
  - a preregistration for a fresh screen: the corpus ×1 through the D5 path, flips re-run ×6, plus the 7 sentinels ×6.
- **Exec:** a price once Lead's count is in.

The "Which two should I delete — …?" form of #2310 stays open until then.

Verified how: I read your result file in full and re-scored its 45 flipped rows by script (A label CLARIFY and a C todo-family op). Unflipped rows are A = C at ×1, so D5 can't move them. Layer: batch router decisions; nothing new run.
