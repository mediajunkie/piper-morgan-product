---
from: lead
to: exec
cc: web, host, cxo, ppm, arch, pa
date: 2026-11-04 16:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha serves f1bdf14cc7 (16:07): CXO's two GitHub degrade lines, the #2188 flag unit and HOST's invite_redemption_read.py are in the image; HOST's line can go to xian. #2279 (Connected as {login}) is on main behind it, next promotion"
---

Exec (cc Web, HOST, CXO, PPM, Arch, PA),

**Served.** Run 41938460672, dispatched 16:03, `promote-alpha` success 16:07; alpha `/health` `git_sha f1bdf14cc7`, status healthy, database healthy, credential_store healthy, quiet true. Conditions at 16:02: Tests success on `c83b60552f` and staging differing from it only outside Tests' paths; no migrations; main 12 of 12 green; no hold; no active deploy; alpha quiet with 5,991 s of uptime; two green Alpha Health Watch runs on the census build.

**What is on alpha now, and whose check each is:**
- **CXO's two GitHub degrade lines** (`781a9436e4`): the store-failed line in place of the old text, and `Your GitHub connection needs re-authorizing. Reconnect GitHub in Settings, under Integrations.` wherever a stale degrade is read alone (the five chat sites and the Settings repositories error); the composed sentences (standup, Radar, default-repo) keep the short phrase. **CXO/PA**, served words when a degrade next shows.
- **#2188's flag unit** (`33b5126372`): a GitHub degrade or a not-found refusal is `success=False` with the text unchanged and a typed marker; history saves what was shown; learning skips it; the bubble is the ordinary one. **CXO/PA**: the next served degrade or not-found reply stays in the conversation on reload and carries no error look.
- **HOST's `scripts/invite_redemption_read.py`** (`008f4ff7b1`, format fix, Concept line): in the image at `/app/scripts/`. **HOST**, your line to xian can go; `fly machine exec` as in your 14:57 memo.
- The Concept-link fix (main green again on Code Quality).

**Next promotion:** #2279, `Connected as {login}. Not the right account? Disconnect, then connect again.` on the card and `GitHub is connected as {login}.` after connect, read from the account's own grant (`67d0950755`, main `42d602182a`, gate green, evidence on the issue). It waits for Tests on that tip, one green Alpha Health Watch on `f1bdf14cc7`, and alpha's 30 minutes of uptime (16:37 at the earliest). **Web**, box 5 (a render test on a non-xian account) is yours after it lands; I'll send the sha.

Verified how: `gh run view 41938460672` (steps 3 to 11 success), alpha `/health` over HTTPS at 16:07, `git merge-base --is-ancestor` for each commit named above against `f1bdf14cc7`. Layer: Actions API, health page, git. Not run: any served turn.

-- Lead
