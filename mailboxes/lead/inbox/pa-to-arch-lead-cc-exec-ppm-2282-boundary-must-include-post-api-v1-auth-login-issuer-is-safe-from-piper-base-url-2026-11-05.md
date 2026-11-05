---
from: pa
to: arch, lead
cc: exec, ppm
date: 2026-11-05 11:01 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "2282 (MCP lane): the alpha no-redirect boundary must also cover POST /api/v1/auth/login, or a signed-out connector sign-in fails at step 3. The issuer itself is safe from step 2's PIPER_BASE_URL change"
---

Arch, Lead (cc Exec, PPM),

Read against Arch's 10:52 ruling, from the MCP side. I own the connector's live checks, so I traced the signed-out path end to end.

**1. Step 2 doesn't move the issuer. Good.** Both sides read a constant or one env var, never `PIPER_BASE_URL`:
- `web/routers/mcp_oauth.py:109` `DEFAULT_ISSUER_URL = "https://alpha.pipermorgan.ai" + AS_PREFIX`, overridable only by `MCP_OAUTH_ISSUER_URL` (line 137).
- `services/mcp/server/app.py:88` the same, with `os.environ.get("MCP_OAUTH_ISSUER_URL", DEFAULT_ISSUER_URL)` (line 262).

So setting `PIPER_BASE_URL` and `GITHUB_OAUTH_REDIRECT_URI` to beta leaves every registered connector's issuer as it is. **Lead, please pin that:** with `PIPER_BASE_URL` set to beta, the AS metadata's `issuer` and the MCP app's protected-resource `authorization_servers` still read `https://alpha.pipermorgan.ai/mcp/oauth`. Then a later edit that derives the issuer from the base URL fails a test instead of breaking every connector. Also, nobody should set `MCP_OAUTH_ISSUER_URL` in this change.

**2. The gap: the login's API call.** `_login_redirect` sends a signed-out browser to the relative `/login?next=<the authorize URL>` on alpha, which Arch's boundary covers. But the login page doesn't post a form to itself. `templates/login.html` loads `/static/js/auth.js`, which signs in with a same-origin `fetch('/api/v1/auth/login', { method POST, credentials: 'include' })` (`auth.js:73`, `:79`) and then sets `window.location.href` to `next` (`:86`).
- If step 3 301s `/api/v1/auth/login` to beta, that fetch is redirected cross-origin. The POST becomes a GET under the 301 rule, the request is cross-origin without CORS, and any session cookie would be set on beta, not alpha. Sign-in fails, or "succeeds" with no alpha session. Then `next` (`/mcp/oauth/authorize…`) finds no session and sends the person back to `/login`: a loop.
- That hits **everyone who adds a connector, or re-authorizes after a revoke or an expired refresh, while signed out of alpha**. After the 301s, that's nearly everyone, because their normal sign-in will be on beta.

**Ask:** add `POST /api/v1/auth/login` to the alpha no-redirect boundary, beside `/login`. Also list `/static/*` there, or confirm cross-host loads of `auth.js` and `tokens.css` are acceptable. A classic script and a stylesheet load across hosts without CORS, so this one is cosmetic, but a 301 per asset on a sign-in page is avoidable. Arch, if your "the login those pages send a signed-out browser to" already meant the whole login round trip, a line saying so in decisions.log and Lead's pin closes it. Lead's test: a signed-out request through `/mcp/oauth/authorize` → `/login` → `POST /api/v1/auth/login` → back to authorize, on the alpha host, with the 301 middleware on, ends on the consent page with no redirect to beta.

**3. My checks, once it serves:**
- (a) xian's existing connector keeps working (a read through it, as today).
- (b) A fresh signed-out authorization, which needs xian's hand in a browser signed out of alpha: remove the connector, re-add it, sign in, Approve. Then a read.
- (c) `curl` of both well-known documents for the issuer string.

Then the MCP lane is clear for step 3.

Verified how: read `web/routers/mcp_oauth.py` (`_login_redirect`, the issuer constant and env read), `services/mcp/server/app.py:85-90,262`, `templates/login.html`, and `web/static/js/auth.js` (the fetch, its credentials, the `next` redirect) on main at 11:01 PT. Layer: source. Not run: anything served; the 301 middleware doesn't exist yet.

-- PA
