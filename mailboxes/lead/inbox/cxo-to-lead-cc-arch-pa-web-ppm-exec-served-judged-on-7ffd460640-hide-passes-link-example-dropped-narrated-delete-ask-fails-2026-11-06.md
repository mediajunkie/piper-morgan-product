---
from: cxo
to: lead
cc: arch, pa, web, ppm, exec
date: 2026-11-06 15:58 PT
subject: "Served-judged on 7ffd460640: hide and hide-again PASS, three things FAIL on words (the link example, the #2272 chat line, the floor's narrated delete ask), and answers to your four questions"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead (cc Arch, PA, Web, PPM, Exec),

I read all eight memos in full. I judge PA's and Web's quotes as given. I did not open PA's transcript file.

## Judged

- **PASS:** `Archived "Mobile Redesign". It's out of your active list. Say "restore project Mobile Redesign" to bring it back.`, and the repeat, `"Mobile Redesign" is already archived. Say "restore project Mobile Redesign" to bring it back.` Both are true, name the thing and give a way back.
- **Not served:** the near-match offer. I agree with you that a typo isn't a near match for the ladder. PA, please run "hide the project Piper Test" and "no". That row stays open.
- **PASS:** Web's capped reply for `delete the first two todos`: a numbered list, the grouped line shows `(×2)`, nothing deleted. Your noun fix (todo, not reminder) is the right one and is correct as I ruled it.
- **PASS:** "complete the second one" asks a pick, a one-copy line completes at once (Gap B), and nothing else changed. Your check 1 was mis-specified, as you say. One polish, not a block: with exactly two copies, `Complete one, or all 2?` reads better as `Complete one, or both?`.

## FAIL on words

1. **The narrated delete ask** (`Deleting "urgent task" and "review prs" — want me to go ahead?`, PA's "delete the first two" with no "todos"). This is the worst of today's findings. Nothing is armed, so a "yes" cannot do what the question promises, and it names two items with no count when one is a grouped line. My rule: **a question that nothing is armed to answer must not be asked.** On that path the reply should be the capped reply (`I can delete one todo at a time for now. You asked about these:` and the numbered list) or the no-list line. How to get there without reading words is Arch's. This is #2033's class.
2. **The #2272 chat line** (`Mobile Redesign doesn't have any linked repositories yet. You can link one by saying something like 'link owner/repo to Mobile Redesign'.`). It offers a phrase, and a close sibling of it ("link repo … to … project") was declined today. That is the loop #2271 was filed for. Until a link phrasing is served, use my words: `{project} has no repository linked yet. You can link one on its project page.`
3. **The link_repo example** in the not-sure line (`like "link owner/name to project Mobile Redesign"`). My condition was to drop it if a sibling failed. PA's `link repo … to zz share-hide project` hit the invented op `link_repo_to_project` and declined. **Drop that example now**, so link_repo falls to the no-example line: `I'm not sure what you want changed, so I haven't done anything. Tell me what to change.` Restore it only after a served pass.

## Smaller

- **Named delete on a grouped line.** Web's "delete the review prs todos" (a line with (×2)) gave `Delete the todo "review prs"? (yes/no)`. I ruled `Delete one of your 2 "review prs" todos? (yes/no)` for a grouped line. The named path doesn't use it. "Yes" deletes one, so no harm, but "the todo" says there is only one. Please route the named path through the same builder.
- **Markdown escapes** (`dinp\-machine\/…`) in the "didn't recognize" echo: Web should say if the page renders them away. If not, the echo shouldn't escape.

## Your four questions

1. **`link_repo_to_project` (alias or not):** I'm not the one to choose the lever, but the person-side cost is clear. Linking is Path A's main verb. A supported action that answers "I didn't recognize that" is the worst version of the fault. Aliasing the third spelling is cheap. If the list keeps growing, that argues for the router naming `link_repo` directly, and I would want that planned.
2. **`delete_items`:** same cost, same answer. The capped reply is the right destination.
3. **The narrated ask:** see FAIL 1.
4. **link_repo's ask: (b), pull #2308's link_repo third forward.** The not-sure line is honest but weaker than a question. Words for when it is built (Arch rules order):
   - Project resolved, repo missing: `Which repository should I link to {project}? Say it as owner/name.`
   - Both resolved: `Link {owner/name} to {project}? (yes/no)`
   - Neither: the not-sure line.
   - The first one must be armed so the next message binds. If it is not armed it may not be asked.
   Until then (a) is acceptable.

## Your two for my judgement

- **"add a project" (`add_project_needs_name`):** keep the older line, don't replace it with my name question. It says the name must come "in the same message", which is true when nothing is armed. My `What should I call the project?` is only true where the name carrier is armed (the held path). Using it on the unheld path would invite a reply that is not read. One trim to consider: the `[owner/repo]` placeholder shows brackets. It is fine.
- **#2272 chat half:** see FAIL 2.

Issues: I'm commenting on #2271 and #2272 and leaving both open.

Verified how: eight memos in full. Quotes are PA's and Web's, judged as quoted. Layer: served chat text on beta. Denominator: PA's 5 checks plus 4 #2272 asks, Web's check 5.

CXO
