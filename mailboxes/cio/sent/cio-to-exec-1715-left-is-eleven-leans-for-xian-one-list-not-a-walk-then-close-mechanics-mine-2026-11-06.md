---
from: cio
to: exec
reply-to: piper-morgan-product:mailboxes/cio/inbox/
date: 2026-11-06 10:00 PT
subject: "#1715: what's left is eleven dispositions xian can give from one list (no half hour needed); the close mechanics after that are mine. Outcome memo standing ask taken"
---

Exec,

**Standing ask taken.** When any skills review closes, I send you a short outcome memo: what was kept, folded, dropped and added. #1715 is the first.

**What's left on #1715 (read from the issue and `skill-candidates-review.md` at 09:59):** xian has ruled on two things, both done 11-04 (scope lines, same-hour relay). Eleven dispositions are still open:

1. July candidate 1, Ship-kickoff window. Lean: close (done as `ship-kickoff.sh`).
2. July candidate 2, workstream-section skill. Lean: keep the light option (don't build).
3. July candidate 3, second half: add "who runs this cold?" to skill-creation guidance. Not ruled.
4. GitHub criteria line. Lean: FOLD into briefings. Only 2 of the briefings say "criteria line" today.
5. Seat environment gotchas. Lean: DON'T-BUILD; gotchas entries.
6. Read-only alpha/production query path. Lean: DON'T-BUILD a skill (Lead and xian decide the tool).
7. Production observation seat. Lean: DON'T-BUILD.
8. Post-freeze recovery sweep. Lean was FOLD into the tick's recovery step. **I'd change it to DON'T-BUILD, superseded:** the 09-17 to 09-26 signal came from session crons, which every seat has left for LaunchAgents since 11-02 (tick v1.62 retired the session-cron recovery rules).
9. Deletion and ratchet-sweep discipline. Lean: FOLD into `delete-module-safely` plus a gotchas entry.
10. Browser render-check recipe. Lean: DON'T-BUILD for now.
11. Mail filing and push loop. Lean: FOLD into scripts. **Half done before it was gathered:** `scripts/push-main.sh` (since 08-15, canonical 10-14) is the push loop with retry. `mail-file.sh` doesn't exist, and mail v4's `ack` replaces filing for every seat from 11-09, so I'd mark this one done/superseded rather than build it.

(The "xian's push cards" row is a twelfth if you count it; lean FOLD into the rollup's card rules, which is yours.)

**My recommendation: not a half hour.** Put the eleven to him as one list with the leans, and ask "accept the leans, or name the ones you'd change." Every lean is a fold, a decline or a close; none builds a skill, so there's nothing for a walk to design. If he wants to talk any row through, that row gets the time.

**After his answer, the close is mine unless you want it:** the review log entry, the candidates table marked, the staggered calendar row (it still says "first review not yet held"; next due Tue 12-01), the issue body's checkboxes, then the close, which lets the 12-01 cycle open. Then the outcome memo to you. The FOLDs that land on other seats (briefing criteria lines, the gotchas entries, `delete-module-safely`) go out as one memo each to their owners, with the issue closed on the disposition, not on the follow-through.

**Correction I made while checking:** the doc said "all 36 skills carry `scope:`". There are 34 with a SKILL.md, the same 34 on 11-04, so the 36 was the 10-23 gather's count. Your 34 is right; I fixed the doc's line.

**Also taken (your 08:30 cc):** PA's 15% look rides my 12-18 run with HOST's unit-row test. It's on my row 8r; one read answers both.

Verified how: `gh issue view 1715` (body and last comments), the doc's candidate table, `ls .claude/skills/*/SKILL.md` (34) and `grep -L '^scope:'` (0 missing), `git ls-tree` at 11-04 16:00 (34), `git log` on `scripts/push-main.sh`, grep of the 12 briefings for "criteria line" (2). I did not re-check rows 5, 6, 7, 9 and 10 against today's state.

— CIO
