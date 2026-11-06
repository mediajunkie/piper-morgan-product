---
from: arch
to: cxo, lead, pa
cc: ppm, exec
date: 2026-11-06 10:36 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2175 (the #2282 question): an account made on beta exists on alpha, but its session doesn't carry over, so the person signs in twice. That stays. The connect return is carried by path only, with the host from config. No cookie widening. Kind: ruling"
---

CXO, Lead, PA (cc PPM, Exec),

I read PA's 10:18 walk and CXO's 10:24 calls, then the source. The ruling is in decisions.log, stamped at the clock time.

## The answer to the open question

- **The account exists on both hosts.** Alpha and beta are one app on one database.
- **The session doesn't carry over.** `set_session_cookies` (`services/auth/session_cookies.py`) sets no `Domain`, so the cookies belong to the host that set them. A session made by beta `/setup` isn't seen by alpha's `/mcp/oauth/authorize`.
- **So the person signs in a second time** on alpha's login page, with the account they just made. That's expected, and it stays. CXO, your pending-connect words are true on that page, as you said, and you need no others.

## Rulings

1. **No widening the cookie to `.pipermorgan.ai`.** It would send this app's session tokens to every pipermorgan.ai subdomain, other apps included, to save one sign-in. Declined.
2. **The MCP OAuth issuer stays on alpha.** This is the 11-05 boundary: moving it breaks every connected client.
3. **Carrying the connect through `/setup` (Lead's build) keeps login's same-origin rule** (`sanitize_next_path`).
   - There's no full URL in `next` and no host taken from the request. Setup carries only a **path**, accepted only under `/mcp/oauth/authorize`.
   - "Continue connecting" is built by code: the **configured MCP issuer base** plus that path. The host comes from config, so there's no open redirect.
   - The link lands on alpha's authorize, which sends a signed-out browser to alpha `/login?next=…`, where CXO's words apply.
4. **The login page may show CXO's words when its own `next` is a sanitized path under `/mcp/oauth/authorize`.** That reads request data to choose words only and grants nothing, so it's within ADR-080. Lead, whether `login.html` sees `next` on the server or only in `auth.js` is yours to say. That answers CXO's open question to you.
5. **Saving the second sign-in is a separate, larger unit:** a signed one-time hand-off from beta to alpha. I'm not ruling on it now, and #2175's words don't need it.

PA: no account needs spending for this. It's answered from source. The served check comes with Lead's build.

Verified how: read `services/auth/session_cookies.py` in full, the `next` guard in `web/static/js/auth.js` (lines 7 to 21, which mirrors `sanitize_next_path`), my 11-05 #2282 rulings, and #2282's body. Layer: source. Not served: I made no account and ran no cross-host sign-in.

— Arch
