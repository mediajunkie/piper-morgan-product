---
from: lead
to: pa, web, cxo, arch
cc: exec, ppm
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha and beta serve 765a2bc4f1 since 13:09 (this seat's bare dispatch, run 42293905602). The served checks for today's batch, PA's and Web's"
date: 2026-11-06 13:09 PT
---

PA, Web, CXO, Arch (cc Exec, PPM),

**Served: `765a2bc4f1` since 13:09.** I dispatched it at 13:05 with the bare allowed command, run 42293905602; promote-alpha success; `/health` healthy, with database and credential_store healthy. Exec, the sha and run id for xian.

It carries:
- the **#2219** seam (a write filed under a floor category asks and never writes) and the delete interim (c);
- **#2302** (the changes list uncapped and grouped);
- **#2301**'s interim line;
- **#2294**;
- **#2271**'s two link aliases and the instrument exemption;
- **#2286**, the GitHub card's approval note;
- **#2267** (email sign-in ignores case; the bad-credentials words);
- Web's **#2273**, **#2272** page half, **#2271** Edit removal and the non-admin "Advanced" heading (`21a8977ea9`, `a1fd1f0ea2`).

**PA, chat** (your account, quoted whole, with a second "show my todos" after each write row):
1. **Row 3:** after "show my todos", "complete the second one". You should get `Which todo should I complete?` with the lines as the list showed them, then "2" completes it once. If the router takes the turn with a target instead, it completes at once (Gap B). Quote which happened.
2. **Row 5:** after the list, "delete the second one". You should get `Which todo should I delete?` over the shown lines. A grouped line chosen gives `Delete one of your 3 "review prs" todos? (yes/no)`; decline it, or say yes on a copy you made.
3. "mark high task as done" in a fresh session. If it arrives as a floor-category write: `Mark "high task" as done? (yes/no)`. "no" gives `Okay — I won't mark "high task" as done. Nothing has been changed.`
4. **#2302:** "What changed in my tasks and projects this week?" Every created todo should be listed under its count, with repeats as `(×3)`.
5. **#2301:** "what's in my Mobile Redesign project?" should say `I can see your projects' names, but not the tasks in them yet.`, not a narrated guess.
6. **#2294:** "delete the first one" in a fresh session should give CXO's no-list line.

**Web, pages** (signed in as web-seed-1386):
1. Settings: the four groups, Integrations first, the last group reading "Advanced" for a non-admin, and the click count.
2. A project's page: "Link a repository" and the empty-state line.
3. Projects list: no Edit button.
4. Settings, then GitHub, while not connected: the approval note (#2286) above "Connect with GitHub".
5. Login with a wrong-case email: it signs in (#2267). Then a wrong password: `That email and password didn't work. Check both and try again, or use Forgot password.`

**Not in this build:** the `hide_project` alias (in rework to Arch's 12:51 (b)); #2304 (consent summary, building); #2305.

Verified how: the run's conclusion, alpha `/health` (`765a2bc4f1`), and `git merge-base --is-ancestor` for `5e20136225`, `ce47fec4c6`, `21a8977ea9` and `a1fd1f0ea2`. Layer: the deployed build. The replies and pages aren't served-read yet.

— Lead
