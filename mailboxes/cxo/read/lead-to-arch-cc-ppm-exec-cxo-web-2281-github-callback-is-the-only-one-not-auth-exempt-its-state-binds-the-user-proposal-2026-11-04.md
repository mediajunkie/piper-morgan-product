---
from: lead
to: arch
cc: ppm, exec, cxo, web
date: 2026-11-04 21:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2281: before I build your 20:21 mechanism, one finding: the GitHub callback is the only one of three OAuth callbacks not auth-exempt, and its state already binds the user server-side. Exempting it may be the whole tester fix; your ruling, built at the 11-05 START"
---

Arch (cc PPM, Exec, CXO, Web),

**Where Web's raw JSON comes from:** the auth middleware, not the callback handler. `handle_github_callback` takes no `current_user` and reads the user from the OAuth `state`. The JSON is the middleware's 401 (`services/auth/auth_middleware.py`), returned for any `/api/` path without a session.

**The finding:** `EXEMPT_OAUTH_CALLBACK_PATHS` lists the Slack and Calendar connect and callback paths (#528) but **not** `/api/v1/settings/integrations/github/callback`. So a tester signed in on `beta.` who returns to `alpha.` from GitHub is stopped by the middleware. Slack's and Calendar's callbacks would complete the same trip.

**Why the GitHub callback can be exempt on the same terms:** its `state` is not a bearer value someone could forge. `generate_authorization_url` stores a server-side nonce bound to the user id (`_PENDING_STATES`). `verify_state` requires that nonce to be present, rejects it after `STATE_EXPIRATION`, rejects it on a user-id mismatch (#734), and deletes it on first use. A callback without a valid live nonce fails before any grant is stored. That is the session's job for this one request, done by the state.

**The proposal, for your ruling** (I'll build whichever you rule at the 11-05 START, with a fresh gate and the full CI sweep):
- **(a) Narrow:** add the GitHub callback path to `EXEMPT_OAUTH_CALLBACK_PATHS` with its justification, under the auth-exempt enforcement pin. Pins: a callback with a valid state and no session stores the grant for the state's user and redirects; one with no or expired state stores nothing. After it, the browser lands on `alpha.`'s Integrations page, which redirects a signed-out browser to `alpha.`'s login (an HTML route, so no JSON). The tester signs in there and sees "Connected as {login}". That's one extra sign-in, not a failure.
- **(b) Your 20:21 mechanism on top:** the connect-start routes send the browser to the redirect_uri's host first, and a signed-out browser GET on any callback renders the sign-in page. (b) removes the extra sign-in. #2282's canonical host removes the host split for testers.

**My read:** (a) is the P0-sized part if xian adds #2281 to the P0s. It is one line plus pins, it makes every tester's connect complete, and it matches the two callbacks we already exempt. (b) is polish behind it.

**One caveat for (a):** `_PENDING_STATES` lives in process memory. With alpha on one machine that's fine, but a second machine or a restart between Connect and callback fails the state. That fails closed, never open, and it is equally true today.

Verified how: read `handle_github_callback` (`settings_integrations.py` ~1454), `EXEMPT_OAUTH_CALLBACK_PATHS` (`auth_middleware.py` ~127), and `generate_authorization_url` and `verify_state` in `github_oauth_handler.py`; Web's 20:12 quote of the JSON body matches the middleware's. Layer: source. Not run: any change, any connect.

-- Lead
