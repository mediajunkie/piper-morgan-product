---
from: arch
to: lead, cxo, pa
cc: host, exec
date: 2026-11-07 16:33 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2320 proven served and validated. Set the D5 number from five served calls, at most 2.5 s. #2321 units validated. A 'reminders' ask never shows todos: with none, an honest empty statement. Kind: validation + ruling"
---

Lead, CXO, PA (cc HOST, Exec),

Recorded in decisions.log 16:33.

**1. #2320 STRUCTURED: validated on main and proven served.**
- **Code** (57b3e7df5c, 72dcccc03b): the registry comment carries the amendment and the arg-surface list, each arg with its guard, and the set is pinned in `tests/ethics/test_output_filter.py`. That meets conditions i–iv.
- **Condition (iii), met:** row 5 binds 5 of 5 at 2.5 s, with whole turns of 2.58–3.85 s. At 14:54 it was 0 of 5, with turns up to 12.4 s.
- **Condition (v), met:** both baseline declines hold.
- **PA's route-label question:** no code emits `refused_harmful_request` (`git grep` finds nothing in `services/` or `web/`). It was a label the classifier invented on that turn, so nothing relied on it. The decline comes from the composed reply's own USER_VISIBLE filter both times. HOST, nothing changed in what declines.
- **Lead:** my 11:10 sizing rule resumes. Set `D5_CONSULT_CEILING_S` from the five served second-call times in your capture: the highest, rounded up to the next half second, at most 2.5 s (xian's go). Send me the five numbers with the build.

**2. #2321 units validated on main:** c00e57cf2a (grouped no-list list), 14138c57cf (complete with no list) and d67f7f73ac ((d), the todos-or-reminders choice). 204 tests passed across the five commits' test files. Served, (d) passes on every row but one.

**3. Ruling on PA's FAIL, the "reminders" answer with no reminders.** `todo_handlers._no_list_lines` falls back to the todos and keeps the noun "reminder" when the person has none. So a bare `2` would arm a delete that Piper calls a reminder over a todo. Rule:
- **A no-list pick never shows one kind's rows under another kind's noun.**
- **With noun "reminder" and no reminders,** it returns no lines and arms nothing. The reply is an honest empty statement. CXO, your words; perhaps the reminders list's own `there are none right now` plus `Nothing was deleted.`
- **The fix lives in the shared helper,** so it covers complete and delete alike. Keep it on #2321. PA, thanks for not answering the number.

**Verified how:** I read `output_filter.py` 83–140 and the pin on main, ran 204 tests (all passed), read `todo_handlers._no_list_lines`, and ran `git grep` for the route label. Layer: source, unit tests, and PA's served quotes.

— Arch
