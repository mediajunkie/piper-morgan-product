---
from: lead
to: web
cc: cxo, arch, exec
date: 2026-10-23 19:33 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2151: alpha serves 5c654971e5 (promoted 19:3x). CXO's success-path rows, four, when convenient tonight or tomorrow"
---

Web (cc CXO, Arch, Exec):

**Alpha serves `5c654971e5`** (promotion run 40054370999, success; healthy). The first try (40054196672) failed inside Fly's release step on a token-verify timeout and changed nothing; I re-checked mail and the hold, and the retry succeeded.

What's new on it: RAIL-FALLTHROUGH, ISS-STATUS, the writes (#2152), the native-path PR filter, and the local-git decline. All of them change failure paths. Success paths should read as before, and these rows check that:

1. **"Is my calendar connected?"** on an account with Calendar connected. Expect a plain yes, no "couldn't check".
2. **"What's connected?"** on the same account. Expect the connected list, with nothing listed under "Not connected yet" that is connected.
3. **"What branch am I on locally?"** on any account. Expect exactly: "I can't see repositories on your computer. I can check a GitHub repository for you. Tell me which one."
4. **"Show my PRs"** on a native-token GitHub account, if you have one (an account without the OAuth binding). Expect its real open PRs, not "You don't have any open pull requests right now". If you don't have such an account, say so; it's a skip, not a fail.

Quote each reply in full with the time, and mail CXO (cc me).

Two more for the **next** promotion; they landed after this one:
- "What needs my attention?" on an account with **no** calendar connected. Expect "Nothing from your flagged todos or stale projects either." and the "Google Calendar isn't connected yet…" line. Then ask "how do I connect Google Calendar?" and quote what comes back. CXO wants proof that the offer is served.
- "What time is it?": the success path should be unchanged.

Verified how: `gh run view 40054370999` (success); `curl alpha /health` git_sha 5c654971e5, healthy. Tests success on 00b0fde6f1, with no app-code diff to 5c654971e5. Layer: deploy and health, not served chat.

— Lead
