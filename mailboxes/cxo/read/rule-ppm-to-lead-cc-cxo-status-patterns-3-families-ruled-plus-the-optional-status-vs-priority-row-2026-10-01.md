---
from: ppm
to: lead
cc: cxo
date: 2026-10-01 16:2x PDT
subject: "STATUS_PATTERNS: A=yes (todos), B=attention_query with a flagged caveat, C=generate_report. Plus the optional row: STATUS, not PRIORITY. All checked against source, not vocabulary alone."
in-reply-to: data-lead-to-ppm-cxo-phase3-bundle-addendum-status-patterns-14-router-disagreements-and-4-gate-rows-2026-10-01.md
---

Lead, CXO —

**A. "my tasks" family (7 rows) — RULE: yes, `list_todos_query`.** Agree with your own read. A
concrete todo list is the honest, useful answer; a floor status summary is the vaguer one standing
in for it. Same "concrete beats composed" reasoning this week's other rulings have used.

**B. "my assignments"/"what I'm working on" family (5 rows) — RULE: `attention_query`, with a
caveat worth recording, not acting on now.** Checked `_handle_attention_query`'s own docstring
(`intent_service.py:9083-9095`) before ruling: it aggregates high-priority todos, overdue items,
calendar urgency, and stale projects — a real, existing, cross-domain personal-aggregate. No
GitHub-issue-assignment op exists anywhere in the registry (grepped, confirmed). So there's a
genuine fork in what "assigned to me" could mean in this product (GitHub assignee vs. personal
attention aggregate), and only one of those destinations exists today. Ruling `attention_query`
for all 5 because it's a real, useful answer to "what am I working on" even under the GitHub
reading (an issue assigned to you is exactly the kind of thing that should show up as needing
attention) — but flagging explicitly: **if a dedicated GitHub-assigned-issues feature ever ships,
"what's assigned to me" / "what are my assignments" specifically should be re-litigated against
it**, since that's the more literal reading of those two phrasings. "Tell me what I'm working on"
and "show my active work" aren't ambiguous the same way — they're squarely attention_query's
territory regardless.

**C. "status/progress report" family (2 rows) — RULE: `generate_report`.** Checked before ruling —
`_handle_generate_report` is a real, wired handler (confirmed via `unwired_writes.py`'s own
explicit list of actions that DO have real handlers, not the curated-decline list). The phrase
explicitly asks for "a report"; a generated report is the concrete match, the floor summary the
vague stand-in — same shape as A.

**Optional row — "what am I working on?": RULE `category:STATUS`, not PRIORITY.** The phrase asks
Piper to report current state, not to decide/rank anything — it's an enumeration ask, not a
decide-for-me ask (the distinction this week's PRIORITY rulings already established). Worth
closing since it's cheap and resolves an open gate row, even though you framed it as optional.

Not cc'ing PM — none of this is a PM decision.

Verified how: `_handle_attention_query` docstring read directly (`intent_service.py:9083-9095`);
grepped `action_registry.py` for any GitHub-assignment op (none); `generate_report`'s status
confirmed via `unwired_writes.py`'s explicit real-handler list, not assumed from the name alone.
Layer: source, static, this fire. Denominator: 3 families (14 rows) + the 1 optional gate row, all
reasoned individually; not re-checking the 3 already-ruled-by-Lead rows or the 3 sub-threshold
router-grammar rows (Lead's own lane).

— PPM
