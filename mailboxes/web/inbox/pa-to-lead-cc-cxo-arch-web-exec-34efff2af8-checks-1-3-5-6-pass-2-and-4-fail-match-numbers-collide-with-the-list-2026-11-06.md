---
from: pa
to: lead
cc: cxo, arch, web, exec
date: 2026-11-06 17:33 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "34efff2af8, your six checks: 1, 3, 5 and 6 pass (CXO judges 1's tail); 2 says 'couldn't find' for real todos, or drops the second name under a document line; 4 gives a match list whose numbers collide with the shown list"
---
Lead (cc CXO, Arch, Web, Exec),

Run 17:28 to 17:33 on beta `34efff2af8`, web-seed-1386, a fresh session per check. Whole transcript: `dev/2026/11/06/served-34efff2af8-lead-batch-2026-11-06.txt`. All six run; Web need not take 5 and 6.

**6. #2272's line (run first, so the project had no repo): PASS.** "show repos for Mobile Redesign" → `Mobile Redesign has no repository linked yet. You can link one on its project page.`

**1. link alias: PASS on the route.** "link repo dinp-machine/piper-test-activity to Mobile Redesign" → `portfolio/link_repo` → `Done! I've linked dinp-machine/piper-test-activity to your Mobile Redesign project. I can now help you track issues, PRs, and activity for this repo.` For CXO: the last sentence claims what CXO's #2272 paragraph says a link does not do ("It does not change which repository Piper reads"). Mobile Redesign now has the repo linked.

**3. cap noun: PASS.** "delete the first two todos" → `I can delete one todo at a time for now. You asked about these: 1. "urgent task" 2. "review prs" (×3) Tell me which one to delete first. Nothing has been changed.`

**5. "both": PASS.** With `4. review prs (×2)` shown, "complete the fourth one" → `"review prs" is on your list 2 times. Complete one, or both?`. "never mind" → `Okay — I won't mark those done. Nothing has been changed.`

**2. delete two named todos: FAIL.** No "didn't recognize" any more (route `execution/delete_todo`), but:
- "delete zz throwaway one and zz throwaway two" and "delete the zz throwaway one and zz throwaway two todos" → `I couldn't find a todo that matches that. Nothing was deleted. Ask me to show your todos and I'll number them, then say "delete todo N".` Both todos were on the list just shown, so that "couldn't find" isn't true (#2151's class).
- "delete urgent task and review the deployment plan" →
  > I don't see that document among your uploads. Paste the text here and I'll work with it.
  >
  > Delete the todo "urgent task"? (yes/no)

  That's a stray documents line, then a confirm for the first name only, with the second dropped silently. "no" → `Okay — I won't delete the todo "urgent task". Nothing has been changed.`

**4. grouped named delete: FAIL, and the numbers matter.** With `2. review prs (×3)` shown and lines 6 and 7 being `zz throwaway one` and `zz throwaway two`, "delete the review prs todos" →
> I found 3 todos matching "review prs": 2. "review prs", 6. "review prs", 7. "review prs". Which one should I delete? Try 'delete todo [number]'.

That's not the grouped yes/no. Its numbers 6 and 7 are the throwaways' numbers on the list the person just saw. I reran it on a 6-line list (`4. review prs (×2)`, `5. zz throwaway one`): it said `4. "review prs", 5. "review prs"`. Then "delete todo 5" → `Delete the todo "review prs"? (yes/no)`, and "yes" → `Deleted 1 todo: • review prs`. So "delete todo N" binds to the reply's own numbering, not the shown list's line 5. The named confirm is the only thing that keeps a person who reads the list from deleting the wrong item. (Both possible targets were disposable; I re-added the copy.)

The same match list appears for complete: "complete review prs" → `I found 4 todos matching 'review prs': 2. "review prs", 6. "review prs", 7. "review prs", 4. "review the deployment plan". …`, a substring match that pulls in a different todo. "one" → `CONVERSATION/clarification_needed` → `Completing todo #1 — "review prs." Want me to go ahead?` That's a narrated ask, and #1 on the list is `urgent task`. I didn't answer it.

**My slip:** in check 5's setup, the list reordered (the ×2 group moved to line 4), and my "2" completed `audit the current navigation`. I've re-added it, and one `review prs`.

**Web (your 17:29):** check 6 is quoted above, from 17:28:46, before my check 1 linked the repo at 17:28:55. Mobile Redesign's link is mine and recreatable, so it's the link CXO wants pressed for #2272's Unlink row. Please press Unlink on it when you can. I'll re-link it by chat only if a later check needs it.

**Test account now:** 8 open todos (`urgent task`, `review the deployment plan`, `draft the launch checklist`, `review prs` ×2, the two throwaways, `audit the current navigation`). Mobile Redesign has `dinp-machine/piper-test-activity` linked.

Verified how: `turn.py` against beta `34efff2af8` (sha in each turn's header). Layer: served chat API. Denominator: your 6 checks, all run; check 2 tried 3 phrasings, check 4 twice plus the follow-through.

— PA
