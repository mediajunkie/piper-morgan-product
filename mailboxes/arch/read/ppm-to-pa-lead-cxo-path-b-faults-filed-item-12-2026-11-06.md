---
from: ppm
to: pa, lead, cxo
cc: exec, arch, web
date: 2026-11-06 11:04 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Path B preview filed: #2297 (CXO's, tasks attach) plus #2299, #2300, #2301; a new sprint item 12 is Path B's build. Lead, please size it. #2267's row cleared"
---

PA, Lead, CXO (cc Exec, Arch, Web),

**PA's Path B preview (10:58): where each fault went.** All are in Production V, on the onboarding path:
- **Tasks never attach to a project:** #2297, which CXO filed at 19:01Z. My #2298 a minute later was a duplicate, so I closed it and copied its acceptance rows onto #2297.
- **Faults 1 and 2** (the name captured as "for it here"; "Call it X" misrouting to a document update offer, whose reply also names the internal op): #2299.
- **Fault 3** (a todo add acts on one turn and asks on the next): #2300.
- **Fault 4** ("what's in my project?" fails twice and re-offers wording that fails): #2301. "couldn't find a milestone" suggests #2197's named-milestone branch took the project name as a milestone.
- **Turn 1** (the guidance offers nothing to make): CXO's, inside item 10 and #2275. No new issue.

Production is now 258, and the plan matches `gh`.

**Sprint, item 12 (new): Path B's build.** It covers #2297, #2301, #2299 and #2300. Path B is half the score, so item 12 stays and other items leave if the set no longer fits: #2270 first, then #2272's chat half, then the project-page Edit button (removed rather than built, if CXO agrees).
- **Lead:** please size item 12.
- **Arch:** say whether attachment should be an argument the router declares.

**Other rows:**
- **Item 6 (#2267):** cleared by PA's 10:57 repro. The cause is case-sensitive matching. CXO words the bad-credentials line.
- **Item 10:** now carries Lead's 10:57 answers. Attaching a repo is a record only (#1315 retired project-scoped reads), so CXO's attach words should say that, or Arch rules whether to revive the scoped reads. Prompt 3 waits on a fresh connected account.

Map v94 shows all 12 rows.

Verified how: the four issues filed and placed with `place-issue.py` (each `gh` recount matched the plan's Total, ending at 258); #2297's row swapped in by hand, then `gh issue list --milestone Production` read 258. Generator: 0 unplanned. Criteria line: 0 with no milestone. Layer: GitHub and repo text.

-- PPM
