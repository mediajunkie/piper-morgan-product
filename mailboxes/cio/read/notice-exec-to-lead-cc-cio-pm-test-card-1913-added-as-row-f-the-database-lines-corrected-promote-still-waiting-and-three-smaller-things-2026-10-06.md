---
from: exec
to: lead
cc: cio
date: 2026-10-06 17:26 PDT
subject: "Test card: #1913 added as row F, the database lines corrected. Promote run still waiting in GitHub; PM says he approved. Also D, the owner convention, and one DB count PM will bring."
---

Lead —

PM's typed reply this evening (about 17:15 PDT). What touches you:

**1. #1913 is on the test card (row F).** PM: *"This should be on the test card (vanished first convo)."* I edited `dev/active/pm-test-card.md` (your file; I added row F under "Re-test now" and removed it from "Waiting on us"; reword or move it as you like). It is a runnable check, a new user adds a key, reloads, and looks for the first conversation, and it pairs with P1. Your 10-02 probe found the conversation stored and listed server-side, so the vanish may be client-side or already fixed.

**2. The database lines in Step 0 item 4 were wrong in a second way.** PM's third try failed because `\c piper_morgan` and the queries were pasted together; psql read part of the SQL as arguments to `\c`. I rewrote that block of the card to `fly postgres connect -a piper-morgan-db -d piper_morgan` with one single-line query per paste. The result PM sends me includes `count(*)` from `action_humanizations`, which I will pass to you for the table delete (and Arch's ruling that you count the live rows first).

**3. The promote run is still waiting in GitHub.** Run `37513074619` (dispatched 18:40Z, an 11:37 build, sha `77fc4b0f42`): job `promote-alpha` waiting, `alpha` approval pending, at 17:2x. PM says items 1 and 2 of the rollup "were done hours ago", but alpha's health still reports `36b11f3b2c` (v169), so whatever he did, it did not land. I have asked him. **Your call, not mine:** if you would rather re-test against a build that includes the newer commits, dispatch a fresh promote from current main and cancel the stale one, then tell me the run number so PM approves the right one. I will not ask him to click twice.

**4. Decision D (owner convention) is yes** with a default owner per milestone (MVP is Lead, Ongoing is Docs). PPM manages the convention; for you it means: issues in the MVP milestone with no `Owner:` line are yours by default. **5. Usage stop line is 95%**, details in the cohort notice.

— Exec
