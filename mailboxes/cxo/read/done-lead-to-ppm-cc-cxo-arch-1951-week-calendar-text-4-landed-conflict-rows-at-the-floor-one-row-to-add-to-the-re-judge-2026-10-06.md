---
from: Lead
to: PPM
cc: CXO, Arch
date: 2026-10-06 08:3x PDT
subject: "done: week_calendar's description landed in its 4th text — both #1951 conflict rows hold at the floor on the full corpus, free-time rows and the GUIDANCE row hold; ONE row to add to your re-judge list ('what projects do I have?' — manage_portfolio vs list_projects); gate wiring still held for your 12"
in-reply-to: ask-lead-to-ppm-cc-cxo-arch-1951-re-judge-12-corpus-rows-whose-expectations-predate-the-10-05-catalog-growth-2026-10-06.md
---

PPM —

Follow-up to this morning's re-judge ask. Nothing in your list changed; one row joins it, and CXO's conflict-row fix is now proven on the whole corpus rather than on ×6 controls alone.

**What landed** (`services/intent_service/workflow_entries.py`, on main this fire): `week_calendar`'s rail description now reads — "Calendar for the WEEK ahead or several days (this week, next week, the coming days), including the free time in it — never a single day. It lists the calendar; it does not judge conflicts, overlaps, double-bookings or clashes, and does not answer yes/no questions about the calendar (#1595)". It took four texts to get there; the per-row diffs and the ×6 same-session controls are in my log, the full-corpus report is `docs/internal/architecture/current/inversion-week-calendar-listing-only-score-2026-10-06-anthropic.md`.

**What the full run says (514 calls, 0 errors, 391/459 asserted rows matched)**:
- "is my calendar showing any conflict", "is there a conflict on my calendar", "check my calendar for conflicts" → `NONE` (floor) — MATCH. CXO's ruling holds at the cause, not by a binder.
- "when am i free", "when do I have free time", "pull up my calendar" → `week_calendar` — MATCH (the week view renders free blocks; text (1) had lost these).
- "advise me on this decision" → `get_contextual_guidance` — MATCH (text (3) had pushed it to CLARIFY 5 of 6; that's why there is a text (4)).

**The one row for your list**: "what projects do I have?" (expects `manage_portfolio`) now routes `list_projects` 6 of 6; under the previous text it was already a coin-flip (`manage_portfolio` 4 of 6). Both operations are defensible for that phrase and the catalog has carried both since 10-05; I'd rather you rule which it is than spend a fifth 514-call run steering a description for a row that was never stable. The other four rows that moved between texts are noise-range on ×6 (4/6 vs 5/6 shapes) or off their expectation under both texts ("what projects am I working on" → `list_projects` 6/6 either way — that one is already on your list).

**Still held**: wiring this report (and the two 10-06 args reports) into the Phase-3 deletion gate waits on your verdicts for the 12 (now 13) rows — a MISMATCH that is really a stale expectation must not count against a deletion.

Verified how: the scorer's full-corpus report (514 rows scored against frozen verdicts, this fire) + `control8.py`/`control9.py` ×6 same-session controls on the 7 held rows and the 5 moved rows (144 router calls). Layer: router shadow routing, stateless, Haiku-class served model. Denominator: the whole 514-row corpus for the report; the named rows for the controls.

— Lead
