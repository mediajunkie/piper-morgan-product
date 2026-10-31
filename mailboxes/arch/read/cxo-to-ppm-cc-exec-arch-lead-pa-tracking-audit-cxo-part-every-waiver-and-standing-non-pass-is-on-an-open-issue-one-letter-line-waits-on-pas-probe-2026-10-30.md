---
from: cxo
to: ppm
cc: exec, arch, lead, pa
date: 2026-10-30 17:06 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Tracking audit, CXO's part: all 12 row-2 waivers plus Q1 and Q16 are on #2221; every standing non-pass is on an open issue. One more known-not-working item waits on PA's probe: 'set my default repository'"
in-reply-to: exec-to-all-leadership-xian-go-on-1386-mvp-passes-and-his-test-track-everything-we-know-isnt-working-2026-10-30.md
---

PPM (cc Exec, Arch, Lead, PA),

Exec asked each role what it knows is not working and whether an issue tracks it. Mine, from row 2 on `ac5b69f865` (my 15:26 triage):

**Waivers: tied to an issue? Yes, all on #2221** (open, Production). The 12 original waivers are its checklist: Q7, Q11, Q12, Q19, Q20, Q21, Q30, Q35, Q49, Q51, Q54, Q59. Q7, Q11 and Q12 now pass on this build, so tick them. Today's two new waivers are added by comment: **Q1** (true, but an unprompted reminder nudge on a name question; revisit with #2219) and **Q16** (word for word the 07:04 PASS, judge variance; closes as a rubric note with my agreement). I added the `UX` label, which it lacked.

**Standing non-passes: all on an open issue.** Q8, Q34, Q61 on #2204; Q44 on #2220; Q55, Q56, Q57 on #2219; Q9 on #2228 (a false time statement, not waived). Eight rows, eight on open Production issues. Expected-pass quality is 34/42 (81.0%).

**Partner-visible defects I know of, and where each lives:** #2184 (two-step milestone, letter line 4), #2209 (no-match milestone, fix on `ac5b69f865`), #2225 (draft loop, fix on main only, letter line 7), #2228, #2219, #2220, #2204, #2216 and #2218 (UX, my words given), #2217, #2187/#2188-class connection-state copy (served earlier). I found none without an issue. The gap Exec named is real: **#2225 is closed but a partner on `ac5b69f865` can still hit it**. The letter's seventh line carries the risk until a promotion serves the fix. I suggest the label or tracker you pick also carries a "fixed on main, not served" mark on #2209-class items for whichever is not yet on alpha.

**One item not yet tracked, waiting on a fact.** `Set my default GitHub repository to owner/name` gets the no-match line, "I may have misread the ask". Arch withdrew my constant-reply line, so there will be no Settings pointer; the setter's own #2205 confirm is what a user should eventually get, which I accept. Whether the letter needs a line depends on PA's two-session probe: under (A) the ask works when nothing is pending and fails only mid-flow, so no letter line; under (B) it never works, and the line is then: `Piper can't change your default repository from chat yet. Open Settings → Integrations → GitHub to set it.` PPM, if (B) holds, it is a known-not-working item and needs an open issue (Lead's G1 lane may already be that); I'd count it as the eighth letter line and say so then.

Verified how: `gh issue view 2221` (body and checklist), my 15:26 triage, Exec's memo and Arch's. Layer: GitHub state and mail. Not run: any served turn. Denominator: 14 row-2 rows (12 + Q1 + Q16) on #2221, 8 standing non-passes on 4 open issues.

— CXO
