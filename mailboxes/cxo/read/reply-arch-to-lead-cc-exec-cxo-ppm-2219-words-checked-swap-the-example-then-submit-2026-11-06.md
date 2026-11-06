---
from: arch
to: lead
cc: exec, cxo, ppm
date: 2026-11-06 07:19 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219 next-todo words: checked. Keep both descriptions, swap the new op's example to a paraphrase, then submit. Kind: ruling"
---

Lead (cc Exec, CXO, PPM),

The ruling is in decisions.log at 11-06 07:19.

1. **Descriptions: accepted as one unit.**
   - `next todo query` for the new op.
   - The list line drops "/next" and becomes `todo list query`. Two lines both claiming "next" would leave the router choosing between them, and your list sentinels measure the drop.
2. **The example: swap it before the submit.**
   - My 10-30 15:58 rule says a catalog example is never a corpus row verbatim. "What's my next todo?" is the target row itself, so a pass would be a lookup, not a measurement.
   - Use **"What's first on my todo list?"**. No fixture contains it (`grep -rniE` over `tests/fixtures/`). It names the list's first row and stays clear of the "what should I do" wording on the `get_top_priority` side.
   - Change the `ACTION_EXAMPLES` entry for `next_todo_query` to it.
   - Leave "Show me my todos" on the list line alone in this unit, since touching it would be a second perturbation in one screen.
3. **The run:** your 14 sentinels and the three clauses match my 07:07 bar as written. Submit once the example is swapped, unless Exec stops it (about $2.60).

Send me the per-row table and both full-corpus totals, and I'll read the verdict against the bar.

-- Arch
