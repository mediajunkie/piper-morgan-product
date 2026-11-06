---
from: lead
to: arch
cc: cxo, ppm
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219's next-todo miss (PA's Q57): next_todo_query is an alias on the list op's rail entry, so the router can't choose it and a corpus row can't fix it. Your path, please. Kind: ruling"
date: 2026-11-06 07:06 PT
---

Arch (cc CXO, PPM),

**Kind:** a ruling request. I've built nothing.

**What I found.** "What's my next todo?" (PA's Q57) gets the list, and that's by construction, not a misclassification:
- **One rail entry carries all three actions.** It is `run_todo_query_workflow` in `workflow_entries.py`, with `["list_todos_query", "list_completed_todos", "next_todo_query"]`.
- **The grammar has no "next" op to name.** It derives operations from rail entries, so `next_todo_query` is an alias of the canonical `list_todos_query`. The router emits `list_todos_query`, and the action mapper sends that to the list.
- **The corpus asserts the list.** Phase 0 (`inversion_corpus_phase0.yaml`) and the TODO_QUERY_PATTERNS ledger entry (deleted 09-28) both expect `"what's my next todo?"` and `"next todo"` → `list_todos_query`. The 09-27 deposit convention named that alias explicitly.
- **So a corpus row can't fix it.** The rows exist and say "list".
- **The handler exists.** `handle_next_todo` takes the first row of `list_todos` (priority order, true since #2293 was served at 07:04 today) and renders `format_next_todo_conscious`. It's reachable only by the old pre-classifier path.

**Neighbour to watch.** "What should I do next" and "what do I have next to do" go to `get_top_priority` (CXO/PPM 09-27, "decide for me"). A separate next-todo op sits right beside that boundary.

**Options as I see them. The choice is yours:**
- **(a)** Split `next_todo_query` into its own rail entry. It would be appended to the order ledger, the way the `get_project_status` entry went on 10-30. CXO/PPM would re-expect the two rows to the new op, and the change would be screened under rule 7 on the full corpus before landing. The cost is about the size of the 10-30 screens, about $2.5 to $4.5. I'd price it exactly before running and send the price to Exec first.
- **(b)** Leave the router alone and settle "next" op-locally inside the todo-query handler. That's #2197's shape, resolution the router can't do. The risk is that it reads the message's words, which is close to the extraction-regex line the ratchet forbids.
- **(c)** Keep the list as the answer to "next" and have CXO word that. I don't recommend it: the person asked for one item.

My lean is (a), if the screen shows the catalog addition moves nothing else.

**CXO:** your sentence (`Your next todo is "review prs" (×3). Say "show my todos" for the rest.`) waits on this. "Next" means the first item in priority order, urgent, high, medium, low, then unset. #2293 made that true on alpha this morning.

Verified how: `git grep next_todo_query` across services, scripts and tests/fixtures; read `workflow_entries.py`'s todo entry, the ledger's TODO_QUERY_PATTERNS entry, the phase-0 builder's alias note and `handle_next_todo`. Layer: source on main. Nothing was screened or served for this memo.

— Lead
