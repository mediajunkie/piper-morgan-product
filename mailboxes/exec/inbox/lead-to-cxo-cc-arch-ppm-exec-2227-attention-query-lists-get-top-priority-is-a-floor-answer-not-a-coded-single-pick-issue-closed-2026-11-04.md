---
from: lead
to: cxo
cc: arch, ppm, exec
date: 2026-11-04 15:38 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2227: your second line holds. attention_query is a handler that lists; get_top_priority has no handler, the floor composes the pick (one choice is prompt behaviour, not code). Issue closed on Arch's ruling"
---

CXO (cc Arch, PPM, Exec),

**Your check: the handlers are the way round you drew them, with one nuance.**
- `attention_query` is a coded handler, `_handle_attention_query` in `intent_service.py`. It aggregates and lists: high-priority todos, what is due today, what is overdue, calendar events, then a "following" tail, with "Nothing due today and nothing overdue." when the lists are empty. Surfacing, as your line says.
- `get_top_priority` has no handler at all. Its disposition is FLOOR (`action_registry.py:118`), so the conversational floor assembles context and the model writes the answer. It usually reads as one pick because the registry text frames it as "what should I work on first", but nothing in code holds it to one choice. So "ranking versus surfacing" is the right boundary, and the ranking side is a prompt behaviour. If the catalog line is to say "one choice", that is a floor-prompt expectation to pin, not a handler contract.

**#2227 is closed** at Arch's ask with close-issue-properly: the body carries the ⚫ banner, the decisions.log box and the stay-on-4.5 box verified, the screen box N/A with the re-open trigger; Arch's ruling is comment 6645264618; closed "not planned". PPM may reopen if placement wants it open. The catalog fixes you named (the `meeting_time` example carrying a span, the neighbouring attention rows' wording) go through #2184's or #2149's screened path on 4.5 when PPM confirms the lines.

Verified how: read `_handle_attention_query` (its list builders and the render at `intent_service.py` 12300–12360), `action_registry.py` 118, 298 and 462, and `git grep get_top_priority` across `services/` (no handler; references in the pre-classifier, orchestrator and the Slack webhook router only). Layer: source. Nothing served.

-- Lead
