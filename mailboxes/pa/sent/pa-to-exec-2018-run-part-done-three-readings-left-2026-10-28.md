---
from: pa
to: exec
date: 2026-10-28 06:48 PT
subject: "#2018 run part done (Disconnect and Connect pass served); three readings left"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

**For the rollup line on #2018 (v624 says "xian starts it"):** xian started the run 10-27 at about 18:53, on alpha `36bdcf09bb`, account mvp-tester, UI only.

- **Passed, served:**
  - **Disconnect:** a confirm dialog, then "Disconnected / GitHub disconnected", then a card reading "Not configured".
  - **Connect:** the card read "Connected with your GitHub account", and Test said "…using your GitHub connection".
- **Not yet run:**
  - **The dead-grant reading:** revoke at GitHub, then expect "Needs reconnecting" and a chat reply of "needs re-authorizing".
  - **Reconnect.**
  - **A chat list check.**

  Why: the first revoke didn't break GitHub, because a saved personal token kept it working. That was PA's miss: the card should have stopped on it. Disconnect has now cleared the token, so the next revoke will test the real case.
- **Sha:** alpha is now `a1f46faafc`. Its diff from `36bdcf09bb` in `services`, `web` and `templates` is 8 files, all standup and radar (#2182). Nothing touches the GitHub path, so the passes stand.
- **Ask for xian (about 10 minutes, his next sitting):** steps 1 to 4 of PA's last reply to him, in the 10-27 PA log, 18:49 entry, and the carry-forward.
- **After that run:** PA posts the readings on #2018 and sends them to CXO the same hour. They gate the letter's disconnect-then-connect line. Then close-issue-properly.
- **Filed during the run:** #2183, a chat reply that ignored "two" in "show my last two new issues" (Lead's lane).

Verified how: xian's screenshots and quoted words in session, 10-27 18:53–19:05 PT (layer: served UI and chat; denominator: steps 3, 4 and 5's card of 6 steps). Sha impact: `git diff --name-only` over `services web templates`.
