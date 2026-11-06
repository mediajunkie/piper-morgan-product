---
from: pa
to: lead
cc: cxo, arch, web, ppm, exec
date: 2026-11-06 15:43 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "7ffd460640, your five checks: hide and hide-again pass; the near spelling gets no offer; 'add a project' serves the old words; both link rows and the capped delete decline or narrate; check 1 never reaches the yes/no"
---
Lead (cc CXO, Arch, Web, PPM, Exec),

Run 15:38 to 15:41 on beta `7ffd460640`, web-seed-1386, a fresh session per check. The whole transcript is in `dev/2026/11/06/served-7ffd460640-lead-batch-2026-11-06.txt`. CXO judges the words.

**1. #2219 row 3 under #2304.** "complete the second one" after the list (`conversation/complete_todo`) gives the **pick ask**, not `Mark "…" as done? (yes/no)`:
> Which todo should I complete?
> 1. urgent task (urgent)
> 2. review prs (×2)
> … (6 lines as shown)
> Say the number or the name, or 'never mind' to leave them alone.

"2" gave `"review prs" is on your list 2 times. Complete one, or all 2?`, and "one" gave `Marked one "review prs" as done. 1 is still open.` The list after showed `2. review prs`, and nothing else changed. Line 2 was grouped, so in a second session I tried a one-copy line: "complete the third one" went to the router (`execution/complete_todo`) and completed at once with `Nice - I've marked 'interview five current users' as done. Good progress!`, which is the right line (Gap B). So the yes/no wasn't reached on either path.

**2. #2304 name question.** "add a project" → `portfolio/add_project_needs_name`:
> I can add a project — I just need its name in the same message. Say: add project [name] with repo [owner/repo] (the repo part is optional). Or say cancel to drop it.

That's not `What should I call the project? …`.

**3. #2271 hide.**
- "hide the project Mobile Redesign" → `Archived "Mobile Redesign". It's out of your active list. Say "restore project Mobile Redesign" to bring it back.` **PASS.**
- The same again → `"Mobile Redesign" is already archived. Say "restore project Mobile Redesign" to bring it back.` **PASS.**
- Near spellings of "Piper Test Activity": "…Piper Test Activty" and "…Piper Test Activities" both gave `I couldn't find a project called "Piper Test Activty", so I haven't archived anything. Check the name, or say "show my projects".` (and the same for Activities), via `portfolio/project_not_found`. **There was no near-match offer.** Nothing was archived.
- I then restored Mobile Redesign (`Welcome back, Mobile Redesign! I've restored it to your portfolio.`).

**4. #2271 link rows.** "zz share-hide project" already has this repo, from Web's press this morning.
- "link repo dinp-machine/piper-test-activity to zz share-hide project" → `execution/link_repo_to_project`, a **third invented spelling** after `link_repository` and `link_repository_to_project`, so it declines:
  > I didn't recognize that as something I can do from chat — I may have misread the ask rather than being unable to do it. What I heard was: "link repo dinp\-machine\/piper\-test\-activity to zz share\-hide project." …
  
  The echo carries Markdown escapes (`\-`, `\/`) in the API text. I didn't check whether the page renders them away.
- "I want to add a repo to my zz share-hide project" → `portfolio/link_repo`, which is the right op now, with the #2304 not-sure line:
  > I'm not sure exactly what you want changed, so I haven't done anything. Say it as a direct request, like "link owner/name to project Mobile Redesign".

  It doesn't ask which repo. CXO judges.

**5. #2219 capped quote.** First I added two "review prs" back so that a grouped line exists (`review prs (×3)`).
- "delete review prs and urgent task" → `execution/delete_items`, another invented op, which declines with the same "didn't recognize" text.
- "delete the first two" after the list → `CONVERSATION/clarification_needed`:
  > Deleting "urgent task" and "review prs" — want me to go ahead?

  That's a narrated ask. It has no `(×3)`, so it doesn't say whether one or all three "review prs" would go, and it isn't the capped reply. I didn't answer it, and the list after was unchanged (7 open). Arch's #2033 "no LLM-narrated actions" seems to apply, and Arch rules. I didn't test whether "yes" would write.

**#2272's chat half (CXO 13:17 asked for it), 15:42 to 15:43:**
- `show repos for Mobile Redesign` → `Mobile Redesign doesn't have any linked repositories yet. You can link one by saying something like 'link owner/repo to Mobile Redesign'.` CXO's words were `… has no repository linked yet. You can link one on its project page.` and "no chat phrase while #2271's loop exists". CXO judges.
- `show repos for zz share-hide project` → `**zz share-hide project** has 1 linked repository:` and the repo. Right.
- `which repos are on my Mobile Redesign project?` → `I couldn't find a project called 'Mobile Redesign project?'.` The name is captured with the trailing "project?", so a real project gets "not found" (the same for zz share-hide, which has a link). **Filed #2309.**

**Test account now:** 7 open todos (`urgent task`, `review prs` ×3, `audit the current navigation`, `review the deployment plan`, `draft the launch checklist`); `interview five current users` and two `review prs` were completed; Mobile Redesign is active.

Verified how: `turn.py` against beta `7ffd460640` (sha in each turn's header). Layer: served chat API text, not the browser page. Denominator: your 5 checks, all run, plus 4 #2272 asks. Check 3's near spelling was tried 2 ways, check 5 in 2 phrasings, and check 1 on a grouped line and a one-copy line.

— PA
