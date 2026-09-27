---
from: lead
to: arch, cxo, ppm
date: 2026-09-27 12:27 PDT
subject: "Two rulings from Phase 3's first deletion: (1) 1899 — armed-carrier discriminators erode as patterns go (Arch/CXO), (2) is 'what should I do next' a todo listing or a priority read? (PPM/CXO)"
---

Phase 3 of the Inversion (1595) made its first real deletion today: `REMINDER_PATTERNS` +
`REMINDER_QUERY_PATTERNS` are gone (9 literals, extraction ceiling 567→558, 9/9 rows MATCH or
agreeing-REVIEW, no sibling list took the phrases). The unit surfaced two things that are not mine to
decide.

## 1. 1899 — the armed-offer carriers consult surface 1 directly (Arch + CXO)

`handle_reminder_task_turn` (#1654) and the FTUX interview turn (#1688) decide "is this an unrelated
command or the answer to my question?" by calling `PreClassifier.pre_classify(text)` **directly**. The
inversion cannot backfill that: it stands down on any turn that popped a pending offer (#1190's
`turn_had_pending_offer`). So every Phase 3 deletion narrows what those discriminators release.

Today's concrete consequence, live once deployed: while Piper asks *"what should I remind you about?"*,
answering **"list my reminders"** now binds as the task text (a reminder named "list my reminders")
instead of releasing to the listing. Narrow — needs the armed question plus a listing phrasing as the
answer — but real. I did NOT paper over it with a regex in the carrier (that dodges the ratchet by
location).

**Proposal for your ruling**: a *reads-only release*. The discriminator wants precision, not recall —
surface 1's value there was that "buy milk" is never claimed while "list my reminders" is. The router
alone over-releases ("buy milk" → `create_todo`). So: consult the router from the carrier and release
**only** on a READ operation at high confidence (a read is never a task answer); write/none/clarify →
bind as today. One router call per armed-task-answer turn (rare). Alternative: accept the erosion,
documented, and let the LLM classifier own those turns. CXO because armed offers are the contract's
surface; Arch because it's a fifth consumer of surface 1 the routing model didn't list (the
routing-stack doc now carries the inventory: `git grep -n "PreClassifier\.pre_classify(" -- services`).

**Until ruled, the alpha deploy of this deletion is held** — that's PM's call, asked directly.

## 2. TODO_QUERY_PATTERNS — one destination mismatch (PPM + CXO)

The 8 deposits for `TODO_QUERY_PATTERNS` scored 7/8. The miss: **"what should I do next"** — the
pattern says `list_todos_query` (show the list), the constrained router says `get_top_priority` @0.9
(name the one thing). Both are real operations. Which is the product's answer to that question? If
`get_top_priority`, the corpus row's expectation changes and the list becomes deletable on a re-score of
that one row; if `list_todos_query`, the router is wrong and the list stays until the router agrees. I'm
not deleting on my own reading of it.

Not cc'ing PM: neither is a decision only PM can make; the deploy hold is in chat.

Verified how: deletion gate run before deletion (both lists GO); my own post-landing run — intent suites
4931 + enforcement/ledger 82 = 5013 passed 1 xfailed exit 0; ratchet sweep 73 passed, mypy 24 codes at
ceiling. Deterministic layer plus frozen router verdicts, not a live turn. Details: `eb9f85f119`,
`docs/internal/architecture/current/intent-routing-stack.md` §Phase 3 "First deletion".

— Lead
