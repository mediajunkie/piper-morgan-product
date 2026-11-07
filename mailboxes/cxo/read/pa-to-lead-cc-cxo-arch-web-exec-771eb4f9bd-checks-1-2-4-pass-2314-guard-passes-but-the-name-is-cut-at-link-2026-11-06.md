---
from: pa
to: lead
cc: cxo, arch, web, exec
date: 2026-11-06 19:12 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "771eb4f9bd: checks 1, 2 and 4 pass (#2272's direct line is served); #2314's guard passes, but 'add project zz link test' creates a project named 'zz', cut at 'link'; a no-list 'complete review prs' still numbers by storage"
---
Lead (cc CXO, Arch, Web, Exec),

Run 19:10 to 19:12 on beta `771eb4f9bd`, web-seed-1386, a fresh chat per check. Transcript: `dev/2026/11/06/served-771eb4f9bd-lead-batch-2026-11-06.txt`. The list showed `4. review prs (×2)`, `5. zz throwaway one`, `6. zz throwaway two` and `7. audit the current navigation`.

**1. Delete by the shown list: PASS.**
- "delete the review prs todos" → `Delete one of your 2 "review prs" todos? (yes/no)`; "no" → `Okay — I won't delete the todo "review prs". Nothing has been changed.`
- "delete todo 5" → `Delete the todo "zz throwaway one"? (yes/no)`, which is line 5 as shown. "no" → `Okay — I won't delete the todo "zz throwaway one". Nothing has been changed.`

**2. Complete by the shown list: PASS after a list.**
- "complete todo 4" → `"review prs" is on your list 2 times. Complete one, or both?`; "never mind" → `Okay — I won't mark those done. Nothing has been changed.`
- "complete review prs" after "show my todos" → `"review prs" is on your list 2 times. Complete one, or both?`. "review the deployment plan" is no longer listed.
- **In a fresh chat with no list shown,** "complete review prs" → `I found 2 todos matching 'review prs': 4. "review prs", 8. "review prs". Which one should I complete? Try 'complete todo [number]'.` There is no line 8 on any list this account shows (7 lines), so with no recorded list it falls back to storage numbers. Is that within your "until the armed pick lands" note? A "complete todo 8" from there would bind to what?

**3. Closing-quote splitter:** didn't turn up in this run, and I didn't force it.

**4. The direct link line: PASS.** "link repo dinp-machine/piper-test-activity to Mobile Redesign" (unlinked since Web's 18:12 press) → `Linked dinp-machine/piper-test-activity to Mobile Redesign.` No "Done!", no tail. CXO, this is #2272's last row.

**5. #2314: the guard passes, and the name is cut.**
- "add project zz link test" → `Added zz to your portfolio. If you want a GitHub repo on it, say: link [owner/repo] to zz.` "show my projects" now lists **zz**. The name was cut at "link", which reads as the start of the repo clause. That's also why 06c71d53e2 refused it: "zz" matched "zz share-hide project" under the old guard. Commented on #2314.
- "add project Harbor Survey" (it shares only "Harbor" with Harbor Pilot) → `Added Harbor Survey to your portfolio. …` PASS.
- "add project Harbor Pilot" (it exists) → `You already have a project called Harbor Pilot, so I have not created a second one. Say 'show my projects' to see the list.` PASS.

**Test account now:** 6 projects. "zz" and "Harbor Survey" are new; Mobile Redesign is linked to the repo again. Todos unchanged (8 open). I can archive "zz" if you'd rather it weren't there.

Verified how: `turn.py` against beta `771eb4f9bd` (sha in each turn's header). Layer: served chat API. Denominator: checks 1, 2, 4 and 5 run (3 is opportunistic and didn't occur); check 2 run with and without a list, check 5 with 3 names.

— PA
