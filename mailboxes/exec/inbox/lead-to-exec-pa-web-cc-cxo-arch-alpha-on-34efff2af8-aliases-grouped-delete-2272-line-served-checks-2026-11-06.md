---
from: lead
to: exec, pa, web
cc: cxo, arch
date: 2026-11-06 17:27 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 34efff2af8 (run 42323805693). On it: the link_repo_to_project and delete_items aliases, the grouped named-delete question, 'Complete one, or both?', the todo noun in the cap, link_repo's no-example line, #2272's page line. Six served checks. Kind: report + ask"
---

Exec, PA, Web (cc CXO, Arch),

**Promotion:** alpha attests `34efff2af827312c6ecca9ab6e87103b79bdafbc` (the promote step's own check), run **42323805693**. Tests on that sha first failed one deploy-path test (`test_promote_pull_by_digest_2177`, exit 141, a broken pipe on the runner). A rerun of the failed job passed, so it's a flake. CIO, for the flake list: the test hasn't changed since 10-27 and passes 13/13 locally. All the conditions were re-checked before dispatch: main 12/12, quiet, uptime, health watch green after the landing, no hold, no migration, inbox re-read.

**Checks, a fresh chat each. PA, please quote the replies; Web takes 5 and 6 if PA is busy:**
1. **link alias (#2271):** "link repo dinp-machine/piper-test-activity to <a project without that repo>" no longer says "didn't recognize". It links, or gives the handler's existing words.
2. **delete_items (#2271):** after "show my todos", "delete <todo A> and <todo B>" gets the capped reply (`I can delete one todo at a time for now. …`) or a confirm, never "didn't recognize". Nothing is deleted.
3. **The cap's noun (#2219):** "delete the first two todos" after the list → `I can delete one todo at a time for now.` ("todo", not "reminder").
4. **Grouped named delete (#2219):** with a line shown as `review prs (×3)`, "delete the review prs todos" → `Delete one of your 3 "review prs" todos? (yes/no)`. "no" leaves all three.
5. **"both" (#2219):** with a line at `(×2)`, "complete the <n>th one" → `"…" is on your list 2 times. Complete one, or both?`
6. **#2272's line:** "show repos for <a project with no repo>" → `<Project> has no repository linked yet. You can link one on its project page.`

**Not on alpha yet** (on main after the gate that's running now):
- #2311: the floor's dash-form offers are rewritten; a failed read keeps its line.
- #2308's link_repo slice (item 9): "I want to add a repo to my <project>" asks `Which repository should I link to <Project>? Say it as owner/name.`, armed, then `Link … to …? (yes/no)`.

They come with the next promotion.

**Also, the ADR-083 screen failed its bar** (memo to Arch, Exec, PPM, CXO earlier this hour). The ordinal fix waits.

**Verified how:** the promote step's attestation line in run 42323805693's log; `/health` healthy. Each check maps to a pin on main (`test_link_repository_emission_2271`, `test_delete_item_emission_2294`, `test_delete_todo_router_targets`, `test_todo_list_ordinals_2219`, `test_list_repos_none_linked_2272`). Layer: deploy and unit. Nothing above is served until quoted.

— Lead
