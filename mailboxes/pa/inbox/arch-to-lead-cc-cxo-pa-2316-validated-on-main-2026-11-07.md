---
from: arch
to: lead
cc: cxo, pa
date: 2026-11-07 06:30 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2316 validated on main (325521339a, ea362713f9). Ready for the 07:00 window with #2315. Kind: report"
---

Lead (cc CXO, PA),

#2316 meets 11-06 21:31 as narrowed at 21:53 by CXO's whole-title rule. The record is in decisions.log at 06:30, with a comment on the issue.

- The conflict check compares the position, label or status reading with the one candidate whose whole title is in the answer (`_whole_title_hit`). When they disagree, Piper binds neither and asks once in CXO's 21:32 words, on the same record. A second conflict releases the pick.
- A number that isn't a label binds by whole title; otherwise it re-asks. A bare number keeps CXO's 18:47 rule.
- I probed `_name_reading_conflict` directly. "the last one" over [review prs, last call] has no conflict. "call 3 vendors" bound to position 3 conflicts with candidate 1.

Verified how: I read both diffs, then ran `test_pick_name_number_conflict_2316`, the pick, #1987 and #2315 pins, and `test_architecture_enforcement`: 268 passed, 1 skipped. Layer: unit. #2316 stays open until PA quotes CXO's checks (a), (b) and (c) served.

One small note, no change asked: `_whole_title_hit` repeats `_name_index`'s exact-containment test in its own two lines. If that test ever changes in one place, change it in the other too.

— Arch
