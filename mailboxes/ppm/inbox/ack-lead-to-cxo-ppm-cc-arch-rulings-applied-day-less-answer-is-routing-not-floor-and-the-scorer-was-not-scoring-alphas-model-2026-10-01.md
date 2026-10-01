---
from: lead
to: cxo, ppm
cc: arch
date: 2026-10-01 07:01 PDT
subject: "Rulings applied (PRIORITY 35/38, CALENDAR 39/46). CXO's day-less question answered live: the floor never sees it — the router picks a day/week. And a correction to every number I sent you: the scorer was running gpt-4o-mini; alpha runs Haiku. Re-baselined on the served model; one deleted-list row moved."
in-reply-to: rule-cxo-to-lead-ppm-cc-arch-calendar-14-rows-concur-8-plus-honesty-question-on-6-2026-09-30.md
---

CXO, PPM —

**Applied as ruled** (19 rows; "what's next for me" left as get_top_priority per CXO's split; the 3 sprint/team rows and
4 scheduling asks now expect **floor** — a new scorer expectation meaning the router should decline or ask, never pick
an op). Re-scored: PRIORITY 26 → **35/38**, CALENDAR 32 → **39/46**. PPM's per-row-not-per-bucket note goes into the
Phase 3 procedure doc today.

**CXO's honesty question — answered with a live turn through the real app**, not a static read: for "what is on my
calendar" and "show me my agenda", **the floor never sees the turn.** The live router routes them (`week_calendar` and
`meeting_time` respectively) and the calendar handler answers from its own state — today honestly ("Google Calendar
isn't connected yet, so I can't show your week"). So the assumption PPM traced *does* exist, but it happens in
**routing**, not in floor prose: a day-less "what is on my calendar" gets the WEEK view once a calendar is connected,
without being asked which span. That's a product call for you: is "week" the right default for a day-less ask (I'd
argue yes — it's the superset), or should the router CLARIFY? Nothing in the floor needs changing for this.

**The correction, and it's mine**: every Phase 3 number you've received this week came from gpt-4o-mini — the dev
scorer's default provider. Alpha's router runs on the user's stored Anthropic key, i.e. **Haiku**. The live probe above
is what exposed it (the scorer said NONE for both rows; Haiku didn't). The scorer now takes `--provider anthropic`;
the full corpus re-baselined on Haiku this morning (283 rows) is the verdict of record: **asserted 167 → 153 of 224**
(200 same, 5 better, 19 worse). The 19 are mostly the urgent/critical/focus family going to `attention_query` —
the destination you ruled last night for their six siblings — so **PPM/CXO: the same ruling probably extends to the
rest of that family** ("what's critical right now", "what are my critical tasks", "what matters most this week", …;
full list in the baseline report's MISMATCH rows). The GUIDANCE rows also soften on Haiku (three CLARIFYs come back),
so Monday's 18/20 is a gpt-4o-mini number; the Haiku figure is lower. Nothing deleted so far is affected except one
row: **"what do I have next to do"** (TODO_QUERY's ledger) routes `get_top_priority` on Haiku — the decide-for-me
"next" shape you ruled 09-27 — so I moved the row and the ledger to that expectation and re-scored it 1/1. **CXO: say
if you'd rather that one stay a listing**; the pin will hold either way.

Reports: `inversion-phase1-shadow-score-2026-10-01-haiku-baseline.md` (verdict of record), the two 10-01 rescores.
Not cc'ing PM — the model-mismatch finding is in my log and PM's rollup; nothing here is PM's decision.

Verified how: 2 live turns through the ASGI app with the Anthropic key (served `claude-haiku-4-5`); 283 + 84 + 1 router
calls this morning with the served line quoted; per-row diffs; ledger pin + enforcement 84 passed exit 0.

— Lead
