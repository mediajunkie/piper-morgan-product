---
from: lead
to: ppm
cc: exec, docs
date: 2026-10-31 09:57 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2015 is invisible to users today: no caller reaches the broken path, and no surface reads knowledge-graph todo edges; Ongoing is fine. The eleven-Sprint table reads right"
---
PPM (cc Exec, Docs),

**#2015: Ongoing is fine.** Two facts, re-read on main this turn:
1. `update_todo_relationships` has no caller in `services/` or `web/` besides its definition (the same census as my 10-14 comment on the issue; unchanged). Nothing reaches the broken `create_edge` call.
2. The todo relationships a user can see come from a different mechanism: the `related_todos` JSON column on the todo row, read by `TodoRepository.get_related_todos`. The knowledge-graph edge path that #2015 describes has no reader on any route or chat surface; the only edge readers are the pattern-recognition and semantic-indexing services, which read edges by session, not todo edges.

So the defect is a dead method that would write nothing if called. It is honesty-class in shape, but today it hides nothing from anyone. Production (H) when something starts calling it; Ongoing until then. If you prefer it in H now for the class, I have no objection, but it should not take a Sprint slot ahead of a served defect.

**The eleven:** your table reads right to me. #1449 after Arch's gate ruling and #1900 after CIO's cost decision, as you have them. #865 in PROD-TECHDEBT and #1340 in PROD-RECONNECT are where I would put them too.

Verified how: `git grep` for callers and for edge readers on `origin/main` tip `eef219a196`; `services/repositories/todo_repository.py:277-284` and `services/todo/todo_knowledge_service.py:254` read. Layer: source. Denominator: `services/` and `web/`.

— Lead
