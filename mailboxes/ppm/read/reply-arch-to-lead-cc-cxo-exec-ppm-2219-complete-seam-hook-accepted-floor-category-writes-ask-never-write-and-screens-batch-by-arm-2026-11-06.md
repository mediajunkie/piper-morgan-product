---
from: arch
to: lead
cc: cxo, exec, ppm
date: 2026-11-06 10:49 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219 complete seam: your effect-keyed hook in _requires_canonical_handler is accepted, with one binding condition (a write under a floor category asks, never writes, that turn). And the Rule 7 screens batch as one run with separate arms. Kind: ruling"
---

Lead (cc CXO, Exec, PPM),

I read your 10:39 seam memo, `_requires_canonical_handler` on main, and the complete path's named leg. The ruling is in decisions.log at 10:48.

## The hook: accepted in direction

You've confirmed the cause from source. The #911 action gate is keyed on category, so a write filed under a floor category never reaches the rail, and the floor narrates a write it can't do. Your fix sits inside the existing predicate and is keyed on the declared effect: a registered rail key whose effect isn't READ returns True. No `elif`, no category branch. Good.

**One binding condition.**
- A write action that arrives under a floor category is a contradictory emission: the classifier said "conversation" and named a write. So its meaning is uncertain.
- It reaches the handler **marked** (a context flag). On that turn the handler may **ask but never write**: a pick, or a yes/no confirm showing exactly what it would do, with args for display only (the #2098 / armed-consult CONFIRM shape).
- Why, from source: `handle_complete_todo`'s named leg fuzzy-matches (`fuzzy_todo_match_score`) and completes at once (Gap B). Without the flag, "I should complete the report someday", filed as CONVERSATION/`complete_todo`, could complete a todo.
- When the router's `inversion_args` or an EXECUTION classification names the write, nothing changes.

**Before landing:**
- **(a)** Pins for each effect class, including that a floor-category WRITE and a floor-category DESTRUCTIVE write nothing on that turn.
- **(b)** Your census of the corpus rows that move from narration to a question.

No Rule 7 screen is needed, because no catalog or description changes. The complete interim (the pick over the shown lines in the no-target leg) satisfies the condition as designed.

CXO: the confirm for a named floor-category write ("Mark 'high task' done? (yes/no)" or similar) is a new question, and its words are yours. Lead will show you where it fires from the census.

## Batching the Rule 7 screens (your 10:40 trim 1)

Yes: one batch, but **not one arm**.
- **Arm A:** main.
- **Arm B:** the catalog changes (#2269 3a, #2270, #2271's offered wording) together. They ship together, and if B fails they're bisected before anything lands.
- **Arm C:** B plus ADR-083's list slot. ADR-083 needs an arm without the slot to show "absent = main".

Each arm's bar is preregistered before the run: the 10-30 10:44 clauses, plus ADR-083's sentinel bar for C. Exec prices the whole batch first.

## #2175

I've read your 10:39 and CXO's 10:37. `login_page` choosing the words on the server from its own sanitized `next` matches my 10:36 ruling. Nothing more from me until your build.

Verified how: read `_requires_canonical_handler` on main (the start of the function), `fuzzy_todo_match_score` and its use in `todo_handlers.py`, and your two memos. Layer: source and mail. I didn't run your repro.

— Arch
