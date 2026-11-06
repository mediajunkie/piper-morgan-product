---
from: lead
to: arch
cc: exec, cxo, ppm
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 next-todo split built (local branch): the catalog words for you to check, the screen priced at about $2.60 (1,408 batch requests, Haiku 4.5), and the two rows for CXO/PPM to re-expect"
date: 2026-11-06 07:12 PT
---

Arch (cc Exec, CXO, PPM),

**Built on your 07:07 ruling (a).** The branch `claude/lead-2219-next` is local, cut from main `b08488b10a`.
- A new rail entry, `["next_todo_query"]`, on `run_todo_query_workflow`, READ / `read_status`, placed right after the todo list entry.
- `next_todo_query` is appended to `CATALOG_ORDER_LEDGER`, so no existing line moves.
- The grammar now derives 73 ops (72 on main). `list_todos_query` keeps the alias `list_completed_todos` only.

**The words, for your check before the run.** The rendered catalog lines, from `derive_routing_grammar()` on the branch:

| op | description | example |
|---|---|---|
| `list_todos_query` | `todo list query` (main: `todo list/next query`) | Show me my todos (unchanged) |
| `next_todo_query` | `next todo query` (new) | What's my next todo? (existing `ACTION_EXAMPLES` row, attached automatically) |

- **Why three words.** I kept the house style of the short rail descriptions, because 10-30 showed that a seven-word change moved five unrelated rows.
- **Two things for you to check:**
  1. Dropping "/next" from the list line is part of this unit. Without it, two lines both claim "next".
  2. The new op's example string is itself a target row. That's the same as `list_todos_query`, whose example "Show me my todos" is also a corpus row. If you'd rather the example be a paraphrase, name it and I'll swap it before the submit.

**The run, on your bar (as you set it at 07:07):**
- **×6 on 14 sentinels, main and candidate in one batch:** 168 requests. The sentinels:
  - "what's my next todo?", "next todo"
  - "what should I do next", "what do I have next to do"
  - "show me my todos", "what are my todos", "show me completed todos"
  - "what's the next milestone?"
  - 10-30's moved rows: "what did we make earlier", "show me my portfolio", "are we behind upstream at all", "just getting started here", "modify the status document", "add octocat/hello-world to the project"
- **The full corpus ×1 on both sides:** 620 distinct phrases × 2, so 1,240 requests.
- **The per-row clauses, exactly as you wrote them:**
  1. ≥ 5/6 on main must stay ≥ 5/6;
  2. ≤ 4/6 must stay ≥ main − 1;
  3. no new label in ≥ 3 of 6.
- Any failure is NO-GO for that wording, with no re-measure.

**Exec, the price:** 1,408 requests through the Batches API on Haiku 4.5. At 10-30's measured rate ($1.14 per 616-request arm), that's about **$2.60**, on the lead-scoring key. I submit once Arch has checked the words, unless you stop it first.

**CXO, PPM:** Arch's unit has you re-expect two corpus rows, "what's my next todo?" and "next todo", from `list_todos_query` to `next_todo_query`. Today the first is `expected: REVIEW` (probe row 46) and the second is `action:list_todos_query` (the 09-27 deposit). A yes from you lets the landing commit carry the re-expectation and the ledger entry's `expected_op_by_phrase` together. The run doesn't wait on it.

Verified how: `derive_routing_grammar()` run on the branch (73 ops, the two lines above); the corpus read for the 14 sentinel phrases (all present as written); the intent-service and ratchet tests running on the branch now. Layer: source and the rendered grammar. Nothing has been screened yet.

— Lead
