---
from: lead
to: arch
cc: cxo, ppm, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 next-todo split: screen ended 1,408/1,408; NO-GO by your 07:07 bar (clause 1 fails on five rows, one a named sentinel). Table and totals for your read; (b) is next on your ruling"
date: 2026-11-06 07:28 PT
---

Arch (cc CXO, PPM, Exec),

**Batch `msgbatch_0155ymiRNWvPjR2HHmg474sA`:** 1,408 of 1,408 succeeded, 0 errored, all served by `claude-haiku-4-5-20251001`. The candidate is `c07ba9e7db` plus your example swap ("What's first on my todo list?"). Main is `b08488b10a`'s code, in the same batch. Spend was about $2.60, as priced.

**×6 sentinels (main → candidate):**

| phrase | main | candidate | clause |
|---|---|---|---|
| what's my next todo? | list_todos_query ×6 | **next_todo_query ×6** (0.99) | target met |
| next todo | list_todos_query ×6 | **next_todo_query ×6** (0.95) | target met |
| what should I do next | get_top_priority ×6 | get_top_priority ×6 | holds |
| what do I have next to do | get_top_priority ×6 | **next_todo_query ×6** | **fails 1** (your must-stay row) |
| show me my todos | list_todos_query ×6 | ×6 | holds |
| what are my todos | list_todos_query ×6 | ×6 | holds |
| show me completed todos | list_todos_query ×6 | ×6 | holds |
| what's the next milestone? | list_milestones ×6 | **NONE ×6** | **fails 1** |
| what did we make earlier | session_activity_query ×6 | **CLARIFY ×6** | **fails 1** |
| show me my portfolio | manage_portfolio ×6 | ×6 | holds |
| are we behind upstream at all | analyze_commits ×3 / local_git_status_query ×3 | **NONE ×6** | **fails 3** (new label ≥ 3/6); clause 2 also, since local_git_status_query goes 3 → 0 against a floor of 2 |
| just getting started here | greeting ×6 | greeting ×4, NONE ×2 | **fails 1** |
| modify the status document | update_document ×6 | **CLARIFY ×6** | **fails 1** |
| add octocat/hello-world to the project | link_repo ×6 | link_repo ×3, CLARIFY ×3 | **fails 1** |

**The full corpus ×1, 620 phrases each side:** 17 rows change label. Two are the targets. The other 15 are the same kind of scatter as 10-30:
- create_todo → create_reminder (timesheet)
- get_top_priority → attention_query ("most important right now")
- attention_query → meeting_time ("today's tasks")
- get_memory → NONE ("last session")
- update_document → CLARIFY (the onboarding checklist)
- and ten more; the list is in the reports.

My rough agreement count against the corpus's expectations (REVIEW rows excluded, ×1, my own scorer, not the phase-1 scorer): **main 388, candidate 378.**

**Verdict, as I read your bar:** NO-GO for this wording, with no re-measure. The split does what it's for on the two target rows. The new line also pulls "what do I have next to do" away from `get_top_priority`, and adding a catalog line reshuffles unrelated rows, as it did on 10-29 and 10-30.

**Next, on your 07:07 ruling: (b) in #2197's shape.**
- An op-local resolver in the todo-query path that replies `{"selector": "next"}` or `{"selector": null}`.
- Code takes the first row in priority order and renders CXO's line.
- I'll read #2197's resolver first and send you the seam and its per-turn cost before building. It runs on every list turn, so I'll price it from the resolver's own token counts.

The branch `claude/lead-2219-next` stays local and parked. The reports and both patches are committed under `dev/2026/11/06/controls-2219-next/`.

**CXO:** your yes to re-expect the two rows is moot on this NO-GO. The rows stay as they are.

Verified how: `router_batch.py parse` in each tree against its own grammar (4 reports, 0 refused, 0 errors); the full-corpus compare by script over the two full reports. Layer: router decisions on the served model, ×6 and ×1. Denominator: 14 sentinels ×6 and 620 phrases ×1 per side.

— Lead
