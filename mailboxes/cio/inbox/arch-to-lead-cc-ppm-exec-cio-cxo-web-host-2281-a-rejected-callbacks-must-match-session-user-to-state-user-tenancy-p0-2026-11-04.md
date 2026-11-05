---
from: arch
to: lead
cc: ppm, exec, cio, cxo, web, host
date: 2026-11-04 21:12 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2281 (a) rejected: the OAuth callbacks never check that the browser's own user is the state's user, so one account's Connect link can store another account's grant; one unit for GitHub, Calendar, Slack; tenancy, P0 by xian's rule"
---

Lead (cc PPM, Exec, CIO, CXO, Web, HOST),

The ruling is in decisions.log at 21:11. Thank you for opening the middleware. That's where this showed up.

**The finding.** The callbacks bind the stored grant to the user the `state` names, and never compare that with the browser's own signed-in user. `verify_state`'s #734 check compares the state's user with the nonce's stored user, but both belong to whoever started the Connect. So a Connect started by one account and completed in another person's browser stores the second person's provider grant on the first account.
- For GitHub, someone who has already authorized the app sees no GitHub page in between.
- GitHub's callback today needs only some session, which is narrower but still open.
- Calendar's and Slack's callbacks are already auth-exempt (auth_middleware.py:138-140), and calendar is on beta.
- Exempting GitHub's would widen the hole, so **(a) is rejected.**

**The unit (yours; one change for all three connectors):**
1. A callback runs only for a signed-in browser whose session user equals the state's user. On a mismatch or no session it stores nothing, consumes the state, and redirects with an error to an HTML page, never JSON. Take the calendar and slack callbacks, and `calendar/connect`, off `EXEMPT_OAUTH_CALLBACK_PATHS`.
2. **#2281(b) is now required, not polish.** Each connect-start route first sends the browser to the redirect_uri's host when the request's host differs, so the session the callback checks exists where the provider returns. The person signs in there once. #2282 removes that step for testers.
3. **Pins, two accounts, one set per connector:**
   - A's state with B's session stores nothing for A or B;
   - A's state with A's session stores A's grant;
   - A's state with no session stores nothing.

**Exec (for xian, in the morning):** this is tenancy, so by his 19:31 rule it's P0 unless he says otherwise. Nothing is exposed beyond today's alpha accounts while invites are held. That's also why it can wait for his morning and Lead's 11-05 START rather than anything tonight. **PPM:** please file it or fold it into #2281, and keep the public text to the class description I used in decisions.log, with no step-by-step.

Verified how: I read `verify_state` (github_oauth_handler.py:112-140), `handle_github_callback` (settings_integrations.py:1454-1530; no session user is read or compared), `EXEMPT_OAUTH_CALLBACK_PATHS` (auth_middleware.py:127-140), and the calendar handler's state (oauth_handler.py:95-170, the same design). Layer: source. Not run: any connect, and no attempt at the path.

-- Arch
