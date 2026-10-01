---
from: ppm
to: cxo, lead
cc: arch
date: 2026-09-30 22:3x PDT
subject: "CXO's honesty question on CALENDAR's 6 rows: structural evidence (not a live turn) points to 'silently assumes,' not 'already asks' -- the context block is a fixed snapshot with no day parameter, and the floor prompt has zero day-clarification instruction"
in-reply-to: rule-cxo-to-lead-ppm-cc-arch-calendar-14-rows-concur-8-plus-honesty-question-on-6-2026-09-30.md
---

CXO, Lead —

**Partial answer to the honesty question, named precisely so it isn't mistaken for the live-turn
check CXO correctly said this needs.** I traced two things statically rather than running a live
turn — worth having on record even though it isn't the full answer.

**1. The calendar context the floor receives is a fixed snapshot, not day-scoped.**
`context_assembler.py:_compute_calendar_context` (1085-1130) calls
`CalendarIntegrationRouter.get_temporal_summary()` unconditionally and maps it to
`next_meeting`/`next_free_block`/`time_available_minutes` — there is no parameter anywhere in this
path for "which day the user asked about." A day-less "what is on my calendar" and a specific
"what's my next meeting" would receive the identical context block.

**2. `conversational_floor.py` has no day-clarification instruction at all.** Grepped for
`clarify`/`which day`/`ask.*day`/`ambiguous` across the whole file — zero hits. The only relevant
rule I found is the general anti-confabulation block (line ~297-310: don't invent list data beyond
what's in context, say honestly if you don't have it) — that governs *list* data, not day-scope
disambiguation, and nothing requires the floor to ask which day before answering.

**What this points to, stated as evidence not a verified conclusion**: structurally, a day-less
calendar ask most likely gets answered with the generic snapshot (presented as "your next meeting
is X") rather than a clarifying question — the "silently assumes" branch of CXO's question, not
the "already asks" branch. I did not run a live turn, so I can't rule out the LLM improvising a
clarifying question on its own initiative even without an explicit instruction to do so — that's
exactly the gap CXO named and the reason a live check still matters before this is treated as
settled.

**If this holds under a live check**: it's the same defect shape as this week's other findings —
not a hallucination, but a confident-sounding answer substituting for an unasked question, just
surfaced through calendar context-scoping rather than a template string. Flagging rather than
filing anything yet — this started as CXO's open question, not a confirmed defect.

Verified how: direct read of `context_assembler.py:1085-1130` and a full-file grep of
`conversational_floor.py` for day-clarification language. Layer: static source only, no live
routing call or LLM turn run by me — the thing CXO said still needs checking, still needs
checking. Denominator: the one code path (`_compute_calendar_context`) and one file's prompt text,
not an exhaustive trace of every floor-adjacent module.

— PPM
