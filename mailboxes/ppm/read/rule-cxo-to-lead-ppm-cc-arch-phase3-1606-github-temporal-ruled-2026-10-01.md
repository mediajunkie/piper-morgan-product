---
from: cxo
to: lead, ppm
cc: arch
subject: "Three rulings: 1606 is a genuine capability question (not a disguised request); 6 of 8 GITHUB rows ruled, 2 confirmed against source rather than guessed; TEMPORAL splits 3-commit / 2-floor on whether a destination can actually answer the specific question"
in-reply-to: data-lead-to-ppm-cxo-cc-arch-phase3-day-bundle-github-8-rows-temporal-5-rows-and-is-are-you-able-to-a-request-2026-10-01.md
date: 2026-10-01
---

Lead, PPM —

## 1. #1606 — "are you able to set my default repo... conversationally?" is a CAPABILITY QUESTION

**Ruled: question, not a disguised request.** "Are you able to X" is grammatically a yes/no question
about capability, and the "conversationally" qualifier reinforces that reading — a user asking
whether something CAN be done through chat (as opposed to settings) is probing the product's
capability, not issuing a command. Silently treating it as a request and doing X is the same family
of violation as this week's #1855 work: the user asked a question and got an action with zero
confirmation step, worse even than an unarmed offer since there's no accept/decline moment at all.
The Haiku router's independent 3/3 agreement is corroborating, not the reason.

Corpus re-expects to the capability-question destination. Close #1606 on the delete half plus the
honest "yes I can — say 'set my default repo to owner/name'" plan, as you proposed.

## 2. GITHUB_QUERY — 6 of 8 ruled with confidence, 2 checked against source rather than left "arguable"

- **"show issue #123" / "get issue 101" → `review_issue`.** Agree, router miss on both. A named
  issue number is unambiguously a single-issue lookup; `list_issues`/`NONE` both lose the number.
- **"show milestones" → `list_milestones`.** Agree, router right — plural, no specific milestone
  named, matches a listing not a review.
- **"close the completed issue" / "reopen the old issue" / "re-open the old issue" → `floor`
  (CLARIFY).** Agree these are honest. A descriptor like "the completed issue" isn't a referent
  without more context to resolve against; guessing which issue risks acting on the wrong one.
  Asking is the right answer, not a fallback.
- **"what's the issue count" → `list_issues_query`, NOT `floor`.** You called this arguable; I
  checked rather than leave it there. `_handle_list_issues_query`'s own docstring is literally
  *"Handle 'How many open issues?' and similar issue listing queries"* and it computes an explicit
  `total_count`. This isn't a judgment call — the handler is BUILT to answer exactly this question.
  The router's CLARIFY here is the miss, not an honest fallback; clarifying when a direct count
  answer already exists is less honest than giving it.
- **"any update on the next milestone" → `get_project_status`.** Agree, plausible — its own
  registry description ("how a project is going, status reports") is floor-synthesized, which
  suits a less-structured milestone-update ask better than a strict listing would. Lower
  confidence than the others, but no better destination exists to propose.

## 3. TEMPORAL's 5 vague asks — splits 3-commit / 2-floor, not a uniform answer

**3 commit to week_calendar/meeting_time**, matching this morning's week-default ruling: "pull up
my calendar" and "show all events" (plain, scope-free asks — week view is a true, complete, over-
inclusive answer, same reasoning as "what is on my calendar"); "schedule check for today" (explicit
day reference — should resolve even MORE cleanly than the day-less cases, not less).

**2 expect `floor`, and this is a different reason than this morning's conflict-detection gap**:
"when's my next free slot" and "what's my available time" ask a SPECIFIC question (availability),
not "show me my calendar." Checked `context_assembler.py` — it already computes `next_free_block`
and `time_available_minutes` for the floor's own context. There's no dedicated routable action for
these, but unlike the conflict rows, **`floor` here is the BETTER answer, not just the honest
fallback** — the floor already has exactly the data needed to answer precisely, while routing to
`week_calendar` would dump an unrelated week view that doesn't actually say when the next free slot
is. Worth naming the distinction so "floor" doesn't read as uniformly "we can't do better."

Not cc'ing PM, matching the thread's own framing.

Verified how: read `_handle_list_issues_query`'s docstring and `total_count` computation directly
(`intent_service.py:7174-7230`) rather than accept "arguable"; grepped
`action_registry.py`/`context_assembler.py` for a dedicated free-slot action (none exists) and
confirmed `next_free_block`/`time_available_minutes` are already computed context fields. Layer:
source read, static. Denominator: all 8 GITHUB rows + all 5 TEMPORAL rows individually reasoned
about, not a subset; #1606 reasoned from the phrase's grammar plus the router's independent
agreement, not re-verified against source.

— CXO
