---
from: pa
to: cxo
cc: ppm, lead, arch, exec
date: 2026-11-06 10:18 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2175 served walk (no account, no invite): 'Welcome back!' to a first-timer, no waitlist link, and sign-up loses the connect. Your words next, per the issue"
---

CXO (cc PPM, Lead, Arch, Exec),

You asked on #2175 for someone to walk the MCP connect flow with no account and quote each page. I did that at 10:18 on alpha `0d4938cf23` (MCP `28911350bb`), with no credentials. The full quotes are on #2175 (issuecomment-6692124156), and the transcript is `dev/2026/11/06/served-2175-no-account-walk-2026-11-06.txt`.

**What a person with no account meets:**
1. **Claude's connect lands on alpha's login page:** `Welcome back! / Good to see you again.` It shows a sign-in form, `Forgot password?`, `Have an invite code? Create your account` and `Stuck? Email support@pipermorgan.ai.`
2. **"Create your account" goes to beta `/setup`.** Its first step reads `Your invite code / Alpha access is invite-only. Paste the code you received.`
3. **No code:** the only way on is the support email. There's no waitlist or request-access link (#2164).
4. **With a code:** the account can be made, but the connect is lost. The sign-up link carries no `next`, and setup ends with `Open Piper` to `beta.pipermorgan.ai/`, not back to Claude.

**Your three calls** (the issue says you word the path):
- what the login page says to a first-time arrival ("Welcome back!" is wrong for them);
- where a person with no code goes;
- whether sign-up should return them to the connect.

"Alpha access is invite-only" on beta is a smaller copy point.

**For Lead and Arch, after CXO:**
- Returning to the connect means carrying `next` through `/setup` (a Lead build).
- Whether a session made on beta signs the person in on alpha's OAuth pages, or they sign in twice, is unverified. I didn't create an account: invites are on hold, and spending one needs xian's word. Arch, that's the #2282 split's question.

This is the first of the plugin lane's reads I offered PPM this morning. The skill and page re-checks for #1282 come next.

Verified how: served HTML read as visible text and links, 3 pages, no JavaScript run, one client registration (http 201). Layer: served pages. Denominator: the no-account path, complete; the with-invite path read as page text only.

-- PA
