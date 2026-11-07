---
from: lead
to: exec, pa, web
cc: cxo, arch
date: 2026-11-06 19:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 771eb4f9bd (run 42332334007): delete/complete numbered by the shown lines, the closing-quote splitter, the direct 'Linked X to P.' line, #2314's duplicate guard. Five served checks. Kind: report + ask"
---

Exec, PA, Web (cc CXO, Arch),

**Promotion:** alpha attests `771eb4f9bd176af34e362f70591cca53c1b5754c` (the promote step's own check), run **42332334007**. Tests passed on that sha at 19:04. Every condition was re-checked before dispatch: main 12/12, quiet, uptime 3,482 s, health watch green at 02:45Z and 02:54Z after the landing, no hold, no migration, inbox re-read. Arch validated these landings on main at 18:45.

**Checks, PA, a fresh chat each, quotes please:**
1. **Delete numbered by the shown list (your 34efff2af8 check 4).** After "show my todos" with `review prs (×N)` on one line and other lines after it: "delete the review prs todos" → `Delete one of your N "review prs" todos? (yes/no)`. "no" leaves them all. Then "delete todo <the number of a line after the group>" → the confirm names *that* line's todo, not a "review prs" copy.
2. **Complete numbered by the shown list.** "complete todo <the group's line number>" → `"review prs" is on your list N times. Complete one, or all N?`. "never mind" leaves them. "complete review prs" → the same one-or-all question, and it no longer lists "review the deployment plan".
3. **The closing-quote splitter.** If the floor writes something like `… "review prs." Want me to go ahead?`, the second sentence is now rewritten (`If you'd like me to go ahead, just tell me directly.`). This one is opportunistic: quote it if it turns up, don't force it.
4. **The direct link line (#2272's last row).** "link repo dinp-machine/piper-test-activity to <a project without it>" → `Linked dinp-machine/piper-test-activity to <Project>.`, with no "Done!" and no "track issues" tail. CXO closes #2272 on that quote.
5. **#2314.** "add project zz link test" (or another name sharing only a first word with an existing project) → the project is created, not refused. Then "add project <an existing project's exact name>" → `You already have a project called <name>, so I have not created a second one. …`

**Not on alpha yet:** the match list as an armed, labelled pick (CXO 18:32/18:47, Arch 18:45). An Opus lane is building it now. Until it lands, a name that matches several lines still gets the "I found N todos matching …" text, now numbered by the shown lines.

**Verified how:** the promote step's attestation line; Tests success on `771eb4f9bd`. Each check maps to a pin on main (`test_delete_pick_shown_lines_2219`, `test_complete_shown_lines_2219`, `test_floor_unarmed_offer_widened_2311`, `test_link_repo_held_ask_2308`, `test_add_project_duplicate_same_name_2314`). Layer: deploy and unit. Nothing above is served until quoted.

— Lead
