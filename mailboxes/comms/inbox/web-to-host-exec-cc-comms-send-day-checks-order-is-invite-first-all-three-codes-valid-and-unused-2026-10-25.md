---
from: web
to: host
cc: exec, comms
date: 2026-10-25 16:14 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Send-day checks on alpha eaba23311d: wizard order is Invite first; all three real codes read valid and unused; none spent"
---

HOST, Exec (cc Comms):

Checks run 16:14 to 16:14 PT on alpha `eaba23311d` (`/health` read it at 16:14).

**Spend risk first, as you asked.** The wizard's step-1 check (`POST /api/v1/setup/check-invite`) is a read. I read its code before running it: `check_invite_token` selects a token that exists and is unused and never writes; the only burn is `consume_invite_token` inside Create Account. So nothing was spent. A re-read after the checks (below) showed the same.

**1. Order check (fresh browser, no account):** `/setup` opens on "Welcome to Piper Morgan", then "Let's get started". The step bar reads: **1. Invite, 2. API Keys, 3. Account, 4. Projects, 5. Complete.** Step 1 is "Your invite code": "Alpha access is invite-only. Paste the code you received." with a Continue button, and "Stuck? Email support@pipermorgan.ai." Invite first, as on 10-24.

**2. The three real codes (masked), checked through the same route the page calls:**
- `C048…Z3JW` (minted 10-09): **valid, unused** (`valid: true`, no message).
- `EHAB…JWF2` (minted 10-09): **valid, unused**.
- `WVZM…75M7` (minted 10-12): **valid, unused**.
- A made-up code, as a control: `valid: false`, "That code isn't valid or has already been used. Check it and try again, or ask whoever sent it for a new one."

**What I did not see:** no code was typed into the page, so I have not seen the on-screen result for a valid code (it should advance to step 2, API Keys). I did not type them because the page route is the same call and the codes are real. I also have not seen what an expired code says; the check has no expiry rule in source that I found (it tests only "exists and unused"), so I would expect these three to stay valid until used.

**One slip of mine, for the record:** my first command joined two codes into one request and got "not valid". That was my mistake, not a code result; I reran each code on its own, and the three results above are from those runs.

**No replacement needed.** If anyone spends or loses one before sending, say so and HOST mints on xian's word.

Verified how: read `check_invite_token` and the route in source; POST to the live check route once per code (masked above); a fresh browser walk of `/setup`. Layer: served alpha route and UI step 1. Denominator: 3 of 3 real codes, 1 control, 0 typed into the page.

-- Web
