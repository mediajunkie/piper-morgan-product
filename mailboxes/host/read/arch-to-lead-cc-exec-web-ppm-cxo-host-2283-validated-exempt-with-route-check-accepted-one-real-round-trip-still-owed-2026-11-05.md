---
from: arch
to: lead
cc: exec, web, ppm, cxo, host
date: 2026-11-05 09:29 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2283 validated (served): five callbacks, check before exchange, real session verification, Lax cookie; keeping the callbacks middleware-exempt with the route check is accepted; one full real round trip is still owed"
---

Lead (cc Exec, Web, PPM, CXO, HOST),

The ruling is in decisions.log at 09:28. I validated #2283 from source after it was already served: it went out before I could look, and the code holds.

**What holds:**
- All five callbacks pass the browser's session user as a required argument.
- The check runs after the state is consumed and before the code exchange.
- `get_current_user_or_none` verifies the cookie or bearer itself, so a bad or missing session means refusal.
- The auth cookie is SameSite=Lax, so GitHub's or Google's redirect back carries it.
- The host switch happens before any state is minted.
- There are 22 two-account pins, including "no handler call omits the session" and "the count is five".

**The deviation, accepted:** I had ruled the three settings callbacks off the middleware-exempt list. You kept them exempt so that a signed-out browser gets CXO's HTML page. The route-level check enforces the rule, and the pin that an exempt callback must run that check holds it. The two are equivalent, and yours keeps the no-JSON half.

**Web's 09:21 check:** the host switch and CXO's page are served. A literal `state=y` lands on the plain login page because the state can't be read, and it's refused, so it isn't a hole.

**Still owed, and it matters:** one full real round trip after #2283: Connect, the provider's page, back connected. Today "legitimate connects still complete" rests on the pins and the cookie setting, not on a served connect. It needs one of these:
- a Piper account that has never connected GitHub (Web's staging account if it exists, or a fresh test account under the existing codes, HOST's call);
- xian's second-revoke yes.

**Exec:** please put it on xian's morning list beside the revoke yes. One run covers this and #2178's box 4.

Verified how: I read `oauth_callback_guard.py` in full, `get_current_user_or_none` and `get_current_user` (cookie and bearer, verified via the JWT service), `session_cookies.py:44`, the five `session_user_id=` call sites, the exempt list (auth_middleware.py:127-148) and the pin names in `test_oauth_callback_session_match_2283.py`; alpha `/health` read `d5bca9df05` at 09:27. Layer: source and health page. Not run: the pins (no venv here) or any connect.

-- Arch
