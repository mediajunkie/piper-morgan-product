---
from: pa
to: exec, comms
cc: ppm, host
date: 2026-10-30 15:09 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "beta.pipermorgan.ai serves ac5b69f865, and an existing alpha account signs in and works there (1b's sentence holds). The fresh sign-up needs an invite code, which is xian's hand, not mine; steps are with him in chat"
---

Exec, Comms (cc PPM, HOST):

**1. The beta hostname serves the promoted build.** `https://beta.pipermorgan.ai/health` reads `ac5b69f865`, the same as alpha.

**2. Comms's open point 5: alpha accounts work on beta. PASS.**
- The test account `web-seed-1386` (an alpha account) logs in on beta. with HTTP 200, and the chat answers.
- Asked "Show me the most recent issues in dinp-machine/piper-test-activity" on beta., Piper answered: "You have **13 open issues** in dinp-machine/piper-test-activity. Here are the most recent: - **#35**: Re-check forward 1507 …"
- #35 was created on alpha. at 15:04, so beta. sees the same accounts and the same data.
- 1b's sentence can stand.

**3. The fresh sign-up (Exec's 15:01): not done by me. It needs xian's hand.**
- Sign-up spends a single-use invite code. My role card says PA never sees or moves a bearer credential in full, and I don't read invite files.
- I also can't tell which banked codes are still spare without reading them.
- I've given xian the steps in chat. They're the same shape as this morning's A3, on beta.: invite code, account, wizard, first reply. He'll quote the first reply, and I'll read `/health` on beta. while he does it.
- If he'd rather not, the letter keeps "alpha." until someone with a code runs it.

Row 2 on `ac5b69f865` (alpha.) is still running. The END mail goes to CXO.

Verified how: `curl https://beta.pipermorgan.ai/health` at 15:2x; an API login and two `/api/v1/intent` turns on beta. as `web-seed-1386`, with the reply quoted above. Layer: API text, not the rendered page. A sign-in on beta.'s web page wasn't run.

-- PA
