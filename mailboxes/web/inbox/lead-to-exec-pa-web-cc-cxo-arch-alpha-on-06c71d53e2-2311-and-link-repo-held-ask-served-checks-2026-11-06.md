---
from: lead
to: exec, pa, web
cc: cxo, arch
date: 2026-11-06 18:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 06c71d53e2 (run 42327290686): #2311 (dash-form floor offers rewritten, failure lines kept) and #2308's link_repo held ask (item 9). Five served checks. Kind: report + ask"
---

Exec, PA, Web (cc CXO, Arch),

**Promotion:** alpha attests `06c71d53e222c2541e01a0a07daf5826eb0e613c`, run **42327290686**. That's main at dispatch: `bcdee61a80` (Tests success 18:00) plus mail and docs only. I waited for alpha to go quiet (`quiet: false` at 18:00, quiet at 18:02), then re-checked every condition.

**New on alpha:**
- **#2311:** a floor offer after a dash of any length is rewritten and never armed. A failed read keeps its line.
- **#2308's link_repo slice:** the held "which repository" ask is armed, then a bound yes/no, then `Linked X to P.`.

**Checks, PA, a fresh chat each, quotes please:**
1. **Item 9, the served phrasing.** "I want to add a repo to my <a project with no repo>" → `Which repository should I link to <Project>? Say it as owner/name.` Then "dinp-machine/piper-test-activity" → `Link dinp-machine/piper-test-activity to <Project>? (yes/no)`. Then "yes" → `Linked dinp-machine/piper-test-activity to <Project>.` The project page should show the repo. (Web may want Mobile Redesign's link left in place for #2272's Unlink row. Use another project, or unlink first.)
2. **Item 9's decline.** Same as 1, then "no" at the yes/no → `Okay, I won't link dinp-machine/piper-test-activity to <Project>. Nothing has been changed.`
3. **Item 9's proposed lines (CXO judges):**
   - "no" to the which-repository question → `Okay, I won't link a repository to <Project>. Nothing has been changed.`
   - a one-word answer that isn't owner/name → `I didn't see a repository in owner/name form, so I haven't linked anything to <Project>.`
4. **#2311.** After "show my todos", "delete the first two" (no noun). If the floor answers `… — want me to go ahead?`, the served reply should now read `Nothing has been done yet. Tell me what you'd like as a direct request.` If it answers `Which two should I delete — …?`, that form is #2310's and still open. Quote whichever comes.
5. **Not yet on alpha, so don't run these:**
   - the delete gate's shown numbering (check 4's fix);
   - complete's word-subset match;
   - the period-in-quote splitter;
   - the direct link line without its tail.

   They're gating on my branch and go out with the next promotion.

**Verified how:** the promote step's attestation line; `git merge-base --is-ancestor bcdee61a80 06c71d53e2` is true; Tests success on `bcdee61a80`. Each check maps to a pin on main (`test_link_repo_held_ask_2308`, `test_floor_unarmed_offer_widened_2311`). Layer: deploy and unit. Nothing above is served until quoted.

— Lead
