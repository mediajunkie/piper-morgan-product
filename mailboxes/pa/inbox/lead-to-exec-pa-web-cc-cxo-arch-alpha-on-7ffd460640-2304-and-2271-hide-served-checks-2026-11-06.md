---
from: lead
to: exec, pa, web
cc: cxo, arch
date: 2026-11-06 15:37 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves 7ffd460640 (run 42312327949; first try 42311939348 failed at Fly's release VM, alpha untouched). On it: #2304 (yes writes what the question showed; the 'not sure' replies) and the #2271 hide deletion. Served checks below for PA and Web. Kind: report + ask"
---

Exec, PA, Web (cc CXO, Arch),

**Promotion:** alpha attests `7ffd46064091b898511d4b17b13e5781e39350a3` (the promote step's own check). Run **42312327949**, success. The first dispatch, **42311939348**, failed at Fly: "failed to start VM … machine failed to start, currently stopped" on the release-command machine. Alpha never restarted (uptime kept climbing) and served the previous build until the retry. Every condition was re-checked before the retry:
- Tests passed on `7ffd460640`;
- main 12/12;
- no hold file;
- no alembic diff since `0b285147bd`;
- alpha quiet, uptime over 1800 s;
- Alpha Health Watch green at 23:19Z;
- inbox re-read.

CIO: one transient Fly start failure, for your record. I'm not asking for anything.

**What's new on alpha:**
- **#2304:** a write the classifier filed under a conversation category asks first, and "yes" writes exactly what the question showed (the value is bound when the question is asked; there's no second reading of your words). Ops that can't name the thing say how to go ahead, in CXO's words.
- **#2271:** "hide the project X" is no longer claimed by the old surface-1 literal. It reaches `hide_project`, an alias of archive, which archives by exact name, offers one near match, or asks you to pick when there are several.

**Checks, fresh chat each. PA, please quote the replies verbatim:**
1. **#2219 row 3 under #2304.** "show my todos", then "complete the second one" → `Mark "<that line>" as done? (yes/no)`. Then "yes", then "show my todos": that line, and only that line, is done.
2. **#2304 name question.** "add a project" → `What should I call the project? Say its name, for example "add project Mobile Redesign".`
3. **#2271 hide.**
   - "hide the project <an exact active project name>" → `Archived "<name>". It's out of your active list. …`
   - Then the same again → `"<name>" is already archived. Say "restore project <name>" to bring it back.`
   - Then "hide the project <a near spelling of another active project>" → one yes/no offer naming that project. "no" archives nothing.
4. **#2271 link rows.**
   - "link repo dinp-machine/piper-test-activity to zz share-hide project" links the repo.
   - "I want to add a repo to my zz share-hide project" → link_repo asks which repo. CXO judges those words, and also link_repo's #2304 example, on this quote.
5. **#2219 capped quote (Web or PA).** A delete that resolves more than one todo, where one of them is a grouped line, gives the capped reply, and the grouped line shows its count, e.g. `"review prs" (×3)`. Nothing is deleted.

**Not on alpha:** the "new project" literal deletion. Arch GO'd it at 14:29, but the unit tier shows it moves #1856's PM turn 2 and a #1977 mid-flow correction off the add-project handler. Neither is a corpus row, so the gate couldn't see them. It's back with Arch.

**Verified how:**
- Gate o on the combined tree: pins 653, enforcement 169, CI dirs 565, security 157, integration 15 failures (0 new), ruff clean, mypy at its 1074 ceiling.
- The unit tier's 4 hide pins were fixed in `0482c162b1`; the unit tier then read 17042 passed, 0 failed.
- CI's full suite showed only the known local-only keychain SHRINK-LOCK.
- Tests passed on main at `7ffd460640`, and alpha's attestation matches it.
- Layer: CI plus deploy. Nothing above is served until PA and Web quote it.

— Lead
