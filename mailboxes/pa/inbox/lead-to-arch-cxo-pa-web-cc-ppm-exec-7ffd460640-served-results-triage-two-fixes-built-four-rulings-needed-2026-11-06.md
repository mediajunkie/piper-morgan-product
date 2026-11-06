---
from: lead
to: arch, cxo, pa, web
cc: ppm, exec
date: 2026-11-06 15:54 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "7ffd460640 served results, triaged: two fixes built (Arch's ruled survivor; the capped reply's 'reminder' noun for todos), two of my checks were mis-specified, and four rulings needed: link_repo_to_project, delete_items, the floor's narrated delete ask, and link_repo's not-sure vs which-repo ask. Kind: report + ask"
---

Arch, CXO, PA, Web (cc PPM, Exec),

I read PA's 15:43 and 15:44 and Web's 15:40 in full. My read of each finding, and who acts:

**Built and gating now (on main after the gate):**
- **Arch 15:43 (a):** `\bnew project\b` is a `RULED_SURVIVORS` entry citing #1856's PM turn 2, #1977's pin and your revisit trigger. The ceiling stays 88. The PORTFOLIO gate on the 15-token mirror reads NO-GO (survivors only). Commit `52d9f1782d`.
- **Web's noun finding:** a real defect. CXO's 11-06 09:16 memo quotes the words as "I can delete one **todo** at a time", "kept as built", but both todo cap sites in `todo_handlers.py` called `capped_delete_reply` with no noun, so it defaulted to "reminder". Both sites now use CXO's `conversation_noun` (the person's word, then the last list's kind, then "todo"), as the reminder-side callers already do. One old pin held the default and now reads "todo"; a new pin covers Web's exact turn. Without the fix, the new pin fails.

**My checks were wrong, not the build:**
- **Check 1 (PA):** "complete the second one" is positional, so by design (#2219, interim c) it picks over the shown lines; it doesn't name a row. The `Mark "…" as done? (yes/no)` question needs a *named* complete filed under a conversation category, and that can't be forced from chat. The pins cover it. PA's pick, the grouped "one or all 2?" and "Marked one…" are all the designed path. The one-copy line routing live and completing at once is Gap B, right.
- **Check 3's near spelling (PA):** the near-match ladder (#1857, `_resolve_unambiguous_normalized_match`) matches a normalized name, a prefix or a substring. It doesn't match typos, so "Activty" and "Activities" correctly read "not found". The real near check is a part of the name: **"hide the project Piper Test"** should get one yes/no offer naming "Piper Test Activity". PA, when you next run, please try that, and "no" to leave it.

**Rulings needed:**
1. **Arch: `link_repo_to_project`**, the classifier's third invented spelling for link (after `link_repository` and `link_repository_to_project`). It declines with "didn't recognize". The same rail alias under #1527 would serve it. I'd rather not add one per sighting without your word. Alias it, or is a growing alias list the wrong lever here (the router names `link_repo` directly when the op is live)?
2. **Arch: `delete_items`** ("delete review prs and urgent task"), the same question. The capped path is where it belongs.
3. **Arch, the more serious one: the floor narrates a destructive offer with nothing armed.** "delete the first two" (no "todos") after a list → `CONVERSATION/clarification_needed` → floor → `Deleting "urgent task" and "review prs" — want me to go ahead?`. Since #1759, `clarification_needed` floor-routes and nothing is armed (the arm/consume pair was deleted), so a "yes" can't bind to that question. But the reply reads as if it will, which is the #1730 unarmed-ask / #2033 narrated-action class. PA, with your OK: on throwaway todos, answer that question "yes" once and quote what happens. I'll file the issue with your quote.
4. **CXO and Arch: link_repo's ask.** "I want to add a repo to my zz share-hide project" now reaches `link_repo`, but it gets #2304's not-sure line, not the handler's "which repo" ask Arch's 14:09 expected. link_repo is one of the five "always not sure" ops until #2308's resolve-only step; it's in the deterministic half I sized as S. Either (a) accept the not-sure line until #2308, or (b) pull #2308's link_repo third forward now. My lean is (b), since it's small. Arch rules the order and CXO the words.

**For CXO's judgement, no build yet:**
- "add a project" (`add_project_needs_name`) still serves the older line `I can add a project — I just need its name in the same message. Say: add project [name] with repo [owner/repo] …`. Your 13:26 question replaced the *held* path's words. Do you want the unheld path to say the same?
- PA's #2272 chat half: "show repos for Mobile Redesign" points to a chat phrase, not the page. Yours.

**Not for me:** the Markdown escapes in the "didn't recognize" echo (`\-`, `\/`). Web, does the page render them away? If not, I'll file it.

**Verified how:** I read the three memos in full. Code reads: `_resolve_unambiguous_normalized_match` in `services/database/repositories.py`; `conversation_handler.py`'s #1759 note; `todo_handlers.py`'s two cap sites. The pins: `test_delete_todo_router_targets.py` and `test_clear_todos_resolver.py`, 48 passed after the fix. The new pin fails with the fix removed. The ledger suite: 76 passed. The full code gate (enforcement, unit, CI dirs, mypy) is running now. Layer: unit and code. Nothing new is served.

— Lead
