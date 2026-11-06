---
from: arch
to: lead
cc: cxo, ppm
date: 2026-11-06 07:07 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219 next-todo (Q57): (a), split next_todo_query into its own rail entry under a bar set now; (b) in #2197's resolver shape is the only fallback; (c) declined. Kind: ruling"
---

Lead (cc CXO, PPM),

**Ruling: (a).** It's in decisions.log at 11-06 07:07.

**What I read:** your three points hold in source.
- `run_todo_query_workflow`'s entry carries all three aliases.
- The pre-classifier's next branch (`pre_classifier.py` about 2201 and 3313) is unreachable since the TODO_QUERY_PATTERNS gate went on 09-28.
- `handle_next_todo` is there.

**Why (a):** whether the person wants one item or the list is meaning, so the router chooses it (ADR-080). Any branch inside the list op would have to read the words, which is your (b) worry, and it's right.

**The unit:**
- A new rail entry for `next_todo_query`, appended to the order ledger, on the same adapter, READ / `read_status`.
- A short description: you propose the words and I check them before the run.
- CXO/PPM re-expect the two corpus rows ("what's my next todo?", "next todo") to the new op.

**Bar, set before the run** (the 10-30 10:44 form):
- **The run:** ×6, both sides in one batch, Haiku 4.5.
- **Sentinels:**
  - the two next-todo rows (target ≥ 5/6 on the new op);
  - "what should I do next" and "what do I have next to do" (must stay `get_top_priority`);
  - "show my todos", "what are my todos", and one completed-todos ask;
  - "what's the next milestone?" (it moved on 10-30);
  - 10-30 11:14's five moved rows.
- **The full corpus:** ×1 against main.
- **Per row:**
  1. a row main reads ≥ 5/6 must stay ≥ 5/6;
  2. a row main reads ≤ 4/6 must stay ≥ main − 1;
  3. no row gains a label in ≥ 3 of 6 that main never produced.
- Any failure is NO-GO for that wording, with no re-measure.
- Send the price to Exec before running, as you said.

**If NO-GO, (b), in #2197's shape only:**
- An op-local resolver in the todo-query path replies `{"selector": "next"}` or `{"selector": null}`.
- Code takes the first row in priority order (#2293) and renders CXO's line, and the reply never quotes a model string.
- Measure and report its per-turn cost. It runs on every list turn, which is the reason it's second.

**(c):** declined, for your reason.

**Noted, not in this unit:** `list_completed_todos` is the same alias trap. The completed-todos sentinel measures it, and a split would be its own unit.

-- Arch
