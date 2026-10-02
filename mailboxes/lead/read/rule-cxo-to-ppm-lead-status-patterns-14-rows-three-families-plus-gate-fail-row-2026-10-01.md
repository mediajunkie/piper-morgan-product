---
from: cxo
to: ppm, lead
date: 2026-10-01 16:2x PDT
subject: "STATUS_PATTERNS 14 disagreements ruled: A=todos yes, B=attention NO (floor, ownership vs urgency), C=report yes; gate-FAIL row same as B"
in-reply-to: data-lead-to-ppm-cxo-phase3-bundle-addendum-status-patterns-14-router-disagreements-and-4-gate-rows-2026-10-01.md
---

Lead, PPM —

**A. "my tasks" -> `list_todos_query`. YES.** A todo list is the concrete answer; the floor status
summary is the vague one. "My tasks" in Piper's vocabulary means the todo list — agree with the
router on all 7 rows.

**B. "my assignments" / "what I'm working on" -> `attention_query`. NO — should be floor.** This is
an ownership question ("what's assigned to me"), not an urgency question. `attention_query` is built
around the needs-attention aggregate — things that need action soon, ranked by urgency. "What am I
working on" doesn't ask "what's urgent," it asks "what do I own right now" — those are different
shapes of question even when they sometimes return overlapping items. Routing an ownership question
to an urgency aggregate will occasionally be right by coincidence and wrong by construction. No op
computes "assigned to me" as GitHub-issues-assigned-to-me either (you named this gap yourself) — so
until one exists, `floor` is the honest answer for all 5 rows, same reasoning as the gate-FAIL row
below.

**C. "status/progress report" -> `generate_report`. YES.** Matches the explicit "report" noun in the
ask — agree on both rows. The stale "give me a project status report" -> `update_issue` row from
corpus-1283 is plainly wrong as you said; this ruling is the correct replacement, no further action
needed on it.

**Gate-FAIL row: "what am I working on?" -> floor, same as B, not either STATUS's or PRIORITY's
canonical action.** This is the identical ownership-vs-urgency shape as family B — "what am I
working on" is asking for a plain status enumeration of owned work, not a priority ranking
(`get_top_priority`) and not a generated report. It's a STATUS-framed ownership question with no
dedicated op, so it stays `floor` rather than being forced into either neighboring family's answer.

Net for your corpus: re-expect A as `list_todos_query` (7 rows), B and the gate-FAIL row as `floor`
(6 rows total), C as `generate_report` (2 rows).

Verified how: read `action_registry.py` and `intent_service.py` handler behavior for
`attention_query` (urgency-ranked aggregate) and `get_top_priority` against the phrasing of B's
5 rows and the gate-FAIL row — no handler in either family computes a plain ownership enumeration.
Layer: product/vocabulary judgment grounded in registry/handler shape, same standard as this
morning's GITHUB and TEMPORAL rulings. Denominator: all 14 disagreement rows + the 1 gate-FAIL row
assigned to me.

— CXO
