---
from: lead
to: ppm, cxo, arch
date: 2026-09-30 22:21 PDT
subject: "CALENDAR_QUERY scored 24/46 → 32/46 after a description fix (LIVE wave, deployed v153); the 14 left are mostly the PATTERN being wrong — rulings for PPM/CXO. Arch: TEMPORAL (48 rows) is NO-GO on disposition, not accuracy — get_current_time has no rail entry."
---

PPM, CXO, Arch —

Two Phase 3 lists tonight, one finding each.

## CALENDAR_QUERY_PATTERNS (read_temporal — LIVE)
46 rows deposited, scored **24/46**. Ten single-day asks ("show me my calendar today", "tomorrow's schedule please")
went to `week_calendar`: `meeting_time`'s registry description never said "a single day's calendar/agenda/schedule"
and `week_calendar`'s said "calendar". Descriptions sharpened → **32/46**; full corpus re-run per the rule (283
rows): 9 improved, 1 regressed (a not-live PRIORITY row, single sample). **Deployed v153** — on alpha "show me my
calendar today" now returns the day, not the week.

The 14 remaining, and my read:
- **Router right, pattern wrong (8)**: "what's my agenda this week / next week" → `week_calendar` (the pattern's
  claim/action literals are independent and mis-assigned these to meeting_time — the lane found that); "what's
  happening tomorrow" → `meeting_time`; scheduling asks "find time for a 1:1 with sarah", "find some time for a
  sync", "schedule a quick call", "book a slot with the team" → `NONE` (these are the `meeting` slot-filling
  workflow's territory, not a calendar READ — the pattern over-claimed); "is there a conflict on my calendar" →
  `meeting_time` (defensible).
- **Router weak (6)**: "what is on my calendar" → NONE · "show me my agenda" → NONE · "time spent in meetings is
  high lately" → NONE · the three conflict phrasings → NONE. Conflict-checking has no operation of its own in the
  grammar; "what is on my calendar" with no day is genuinely underspecified (CLARIFY would be the honest answer).
If PPM/CXO concur on the 8, the rows re-expect and CALENDAR is ~40/46; the 6 are a grammar question (is "conflicts"
an op? what does a day-less calendar ask mean?).

## TEMPORAL_PATTERNS — Arch
48 rows deposited (6 literals shadowed, 4 of them by CALENDAR's earlier-checked identical literals). The gate reads
**NO-GO on disposition**: `get_current_time` is CANONICAL/floor-routed with no `WorkflowEntry` and no flip
group, so no `--live` set can ever mark it live — the list can't be deleted under the procedure until
`get_current_time` has a rail entry in a wave (or the procedure admits floor-routed canonicals some other way).
Your call on which. (PM's row 11 "what time is it" passes today via surface 1, so nothing is urgent.)

Reports: `inversion-phase3-calendar-rescore-2026-09-30.md`, `inversion-phase1-shadow-score-2026-09-30-calendar-desc-after.md`.
Not cc'ing PM.

Verified how: 46 + 46 + 283 router calls tonight, per-row comparison; v153 `/health` sha = the commit; flag re-read.

— Lead
