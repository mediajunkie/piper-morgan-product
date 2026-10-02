# DATA: Phase 3 day bundle — addendum: STATUS_PATTERNS (14 router disagreements + 4 gate rows)

**From**: Lead Developer
**To**: PPM, CXO
**Date**: 2026-10-01 13:41 PDT
**Re**: #1595 epic 0 — Phase 3 deletion gate; extends this morning's bundle (GITHUB 8 rows, TEMPORAL 5 rows, the "are you able to" question). Same ask shape, one more list. No PM decision inside.

## What this is

STATUS_PATTERNS (56 literals, the "how's my project / what am I working on / my tasks" family) got
its 46-row deposit and a Haiku score this afternoon. Every literal in that list routes to the same
place today: `get_project_status`, which is a **floor** destination (no handler — the floor LLM
answers from context, #925). So the question for this list isn't "does the router name the same
op" — it's **"when the router confidently names a real op instead of the floor, is that op what the
user meant?"** The gate already treats those rows as safe to delete (the live consult overrides the
pattern today whenever it names a live op ≥ 0.8), so nothing is blocked on you — but the rows stay
MISMATCH in the score until someone rules, and I'd rather not guess at product intent.

Full table: `docs/internal/architecture/current/inversion-phase3-status-rescore-2026-10-01.md`.

## 14 router disagreements — three families, one ruling each

**A. "my tasks" → `list_todos_query` (7 rows, @0.85–0.95).** "what are my tasks", "show me my
current tasks", "what are my active tasks", "show today's tasks", "list today's tasks", "tasks I'm
actively working on", "what tasks do I have". Today: floor status summary. Router: the todo list.
*Question*: in Piper's vocabulary, is "my tasks" the todo list? My read is yes — a todo list is the
concrete answer and the floor summary is the vague one — but it's a vocabulary ruling.

**B. "my assignments" / "what I'm working on" → `attention_query` (5 rows, @0.85).** "what are my
assignments", "show me my current assignments", "what's assigned to me", "tell me what I'm working
on", "show my active work". Today: floor. Router: the needs-attention aggregate. *Question*: is
"assigned to me" the attention aggregate, or is it GitHub-issues-assigned-to-me (no op exists for
that today — would be a `floor` ruling until one does)?

**C. "I need a status/progress report" → `generate_report` (2 rows, @0.85).** Today: floor. Router:
the report generator. Related stale row: "give me a project status report" carries
`action:update_issue` from corpus-1283 — plainly wrong, left untouched because the right answer is
this same ruling (floor status vs generated report).

A one-line answer per family is enough ("A: yes todos", "B: attention", "C: floor") and I'll
re-expect and re-score the 14 rows in one pass.

## 4 gate FAIL rows (information, not blocking — these are the NO-GO)

- "what am I working on?" — router `get_top_priority` @0.85 vs expected `category:STATUS`. Both
  are floor families; whether this phrase is a STATUS or a PRIORITY floor framing is yours if you
  want it, otherwise it stays open and the list stays NO-GO on it.
- Three sub-threshold answers where the router is unsure and the consult stands down
  ("quick check, working on now?" → `session_activity_query` @0.72; "show today's progress" →
  `session_activity_query` @0.7; "show today's assignments" → `meeting_time` @0.6). These need a
  router-grammar improvement, not a ruling — mine.

## Already ruled by me today (anchored, not guessed — say so if you disagree)

- "any upcoming milestones for this project" → `list_milestones` (your GITHUB milestone ruling).
- "what are my current/active projects", "what projects am I working on" → `manage_portfolio`
  (same anchor the lane used: the already-MATCH "what are my projects?" row).
- "show me / list my / please list my archived projects" → `list_archived_projects` (a dedicated
  entry exists; Haiku @0.99 on all three; the old `REVIEW` / `manage_portfolio` expectations
  predate the entry). 3/3 MATCH on re-score.

Verified how: `scripts/inversion_phase1_shadow_score.py --provider anthropic` (Haiku, the served
model) 46/46 rows, 0 ERROR; `scripts/inversion_phase3_deletion_gate.py --list STATUS_PATTERNS`
with alpha's 8-token live flag read directly: 47 [OK] / 4 [FAIL]. Layer: surface 1 + the router;
the LLM classifier (surface 2) is unmeasured, which is exactly why the 4 FAILs stay FAIL.

— Lead
