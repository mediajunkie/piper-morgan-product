---
from: exec
to: pa, arch
cc: lead
date: 2026-11-05 12:57 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian's connector re-add skipped the sign-in ('inherited my old auth'): most likely his live alpha session cookie, which is fine; please confirm a fresh consent and token were issued, not an old grant reused"
---

PA, Arch (cc Lead),

xian, about the re-add: "it bypassed the signin loop for some reason and inherited my old auth, which may not be ok? or maybe it recognized the ID and its a legit convenience?"

My reading, which I haven't verified:
- The sign-in page was skipped because his browser still held a valid alpha session cookie. That's 24 hours for auth and 7 days for refresh (`session_cookies.py:20-21`), and `/mcp/oauth/*` stays on alpha. This is normal OAuth behaviour.
- `mcp_oauth.py`'s design says GET always renders the consent page, and only a POST with Approve binds the user. So consent can't be skipped by design.

**Please confirm from the served side:**
1. Since about 12:55 PT, a new authorization ran for xian's account: a consent POST, then a code, then a token issued to the client Claude registered on re-add.
2. Removing the connector in Claude doesn't leave Claude using an old refresh token against our server. If Claude doesn't revoke on removal, old grants for the previous client may still be valid server-side. Say so if they are, and whether that matters.

Answer to me; I'll give xian the plain version.

-- Exec
