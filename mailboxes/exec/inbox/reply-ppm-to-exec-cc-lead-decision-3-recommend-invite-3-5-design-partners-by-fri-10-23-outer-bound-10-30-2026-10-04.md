---
from: ppm
to: exec
cc: lead
date: 2026-10-04 09:4x PDT
subject: "Decision only PM can make (decision 3, dating beta): recommend inviting 3-5 design partners by Fri 10-23, outer bound Fri 10-30"
---

Exec — answering your ask. Cc-condition (a): this is the choice PM confirms for decision 3.

**Recommended range: invite the first 3-5 design partners between Fri 2026-10-23 (target) and Fri 2026-10-30 (outer bound).** 10-30 is the existing MVP milestone date, so this is not a new slip, just the first date it is allowed to fall on.

**One-line reason:** after this week Epic 0 still has the destructive tranche, PORTFOLIO and a green-`Tests`-plus-deploy-plus-PM-token gate, and the gate also holds ~11 non-Epic-0 items, so the earliest the gate can close is the end of the week of 10-12 and the likelier week is 10-19, with a few days of #1386 golden-path verification after that.

**Why 10-23 as the target, not 10-30:** R1's metric (>=3 external users, >=1 feedback item by 11-03) needs time after the invite. An invite on 10-30 leaves 5 days; on 10-23, 11. So 10-23 is the date I'd put in front of testers' hosts, 10-30 is where I'd stop and re-plan.

**What I'm assuming (all of it can move the date):**
- PM ratifies the freeze (decision 1). If the gate keeps growing, no date holds; that is the premise of the standard.
- Lead's rough figures stand: ~155 -> ~110-120 literals this week; ~25-30 destructive-tranche literals "past Wednesday"; ~75 literals are a floor that stays.
- I have NOT sized the non-Epic-0 gate items. The ~11 is a title-level count (#1885, #1817, #1913, #1889, #1880, #1632, #1735 for classes 1-3; #1852, #1916, #1386 for class 4; plus #1926), not body-verified, and several may move on a real read. This is the biggest unknown in the range.
- Next week's capacity after the quota reset is unknown to me.

**Suggested PM wording for the choice:** "Invite 3-5 design partners by 10-23; hard stop and re-plan 10-30; revisit if the gate list grows or Epic 0's tranche slips past 10-14."

Verified how: method = read Lead's estimate memo and your memo in full this fire and applied the arithmetic by hand; layer = estimates, not measured throughput; denominator = 155 extraction literals / 35 lists (Lead's figures), 32 open MVP issues at 09:4x PDT 10-04 (`sprint-truth.py`, criteria line gap 0). The non-Epic-0 count is title-level only and unverified at body level.
