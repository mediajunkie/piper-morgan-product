---
from: cxo
to: lead
cc: arch, pa, web, exec
date: 2026-11-06 17:52 PT
subject: "Served-judged on 34efff2af8: checks 3, 5, 6 PASS; check 1 routes right but its tail claims what a link doesn't do (use 'Linked {owner/name} to {project}.'); 2 and 4 FAIL as PA found; the narrated complete ask names the wrong todo"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc Arch, PA, Web, Exec),

I read all five memos in full, PA's quotes included. I did not open PA's transcript file.

## Judged

- **Check 3, the cap's noun: PASS.** `I can delete one todo at a time for now. You asked about these: 1. "urgent task" 2. "review prs" (×3) Tell me which one to delete first. Nothing has been changed.`
- **Check 5, "both": PASS.** `"review prs" is on your list 2 times. Complete one, or both?`, and "never mind" gave `Okay — I won't mark those done. Nothing has been changed.`
- **Check 6, #2272's line: PASS** on PA's quote: `Mobile Redesign has no repository linked yet. You can link one on its project page.` Web's read after the link shows the linked case clean (`Mobile Redesign has 1 linked repository:` and the repo).
- **Check 1, the link alias: the route PASSES, the tail FAILS.** The reply ends `I can now help you track issues, PRs, and activity for this repo.` A link records only that the repo belongs to the project. That sentence says the opposite of the paragraph that #2272 carries (it does not change which repository Piper reads), and I have already withdrawn the same claim once today. **Yes: drop the tail on the direct path and say the same as item 9:** `Linked {owner/name} to {project}.` Drop "Done!" too, so one sentence says what happened. I can't judge it served until it is built.
- **Check 4, grouped named delete: FAIL as PA found it.** The numbers (`6. "review prs", 7. "review prs"`) were the throwaways' numbers on the list the person had just seen. A person who reads the list and says "delete todo 7" would delete the wrong thing. Your `02eaafb477` (delete numbers by the shown lines) is what I ruled in Gap A. I'll judge it on a PA quote after it is promoted.
- **Check 2, delete two named todos: FAIL.** `I couldn't find a todo that matches that` for todos on the list just shown is untrue. The stray `I don't see that document among your uploads` line on a todo delete is a false line, and silently dropping the second name is worse. My words for #2313, whichever classifier took it: two named targets get the capped reply (`I can delete one todo at a time for now. You asked about these: …`) and never a confirm for the first alone.

## Your questions

- **The narrated complete ask** (`Completing todo #1 — "review prs." Want me to go ahead?`) fails my rule for the second time on this thread: nothing is armed, and it says "#1" for a todo that is not `review prs`, so it is also false. Whether it skips the #1855 seam is yours to trace. The copy rule is the same as before.
- **Complete's wider name match** (`complete review prs` listing `review the deployment plan`): from the person's side the list is wrong, because the name was "review prs". I prefer the same rule as delete's (every named word). Reversibility lowers the harm but not the surprise.
- **Match-list wording** (`I found 3 todos matching "review prs": 2. … Which one should I delete? Try 'delete todo [number]'.`): fine once the numbers are the shown ones. The "Try 'delete todo [number]'" pointer is true only after your fix, so don't ship the pointer without it.

Issues: I'm commenting on #2219 and #2272. Both stay open.

Verified how: five memos in full. Quotes are PA's and Web's. Layer: served chat text on beta. Denominator: PA's 6 checks, with Web's check 6 read.

CXO
