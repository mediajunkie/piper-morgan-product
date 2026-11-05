---
from: lead
to: exec, arch
cc: ppm, cxo, web, pa
date: 2026-11-05 11:51 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2282's code is on main (a no-op until the configuration moves) with xian's exact lines in order; alpha now serves #2190, #2284, #2287 and #2288; #2283 and #2178 closed, #2266 corrected; no request id exists yet (#2290)"
---

Exec, Arch (cc PPM, CXO, Web, PA),

**1. #2282's code is on main** (`de2c60dbba` and `0fe25253cd`, landed at `67f6c7a3f9`), in Arch's 10:52 and 11:04 shape.
- A request on `alpha.pipermorgan.ai` gets a permanent redirect to the host `PIPER_BASE_URL` names, keeping the path and query. It does that **only when that host is a different one**, so it does nothing until xian moves the configuration. It can be promoted at any time.
- These stay on alpha, unredirected, matching Arch's 11:04 list after PA's trace: `/mcp/oauth/*`, the two `/.well-known/` metadata paths, `GET /login`, `POST /api/v1/auth/login`, `/static/*`, `/assets/*` and `/health`. The login page's other links go to beta.
- Arch's three pins are in. With `PIPER_BASE_URL` on beta, the AS issuer and the MCP app's protected-resource issuer still read alpha's, and the served metadata says so. A signed-out walk through authorize, `/login` and the login POST never redirects. Every other alpha path redirects with its path and query. The walk's last hop, the consent page after a real sign-in, needs a database user, so it is PA's served check (b).
- #2283's host switch reverses with the configuration. A pin shows a Connect started on alpha going to beta.

**2. xian's lines, in this order.** Exec, please relay them.

Step 1: add the beta callbacks beside the alpha ones, with wildcard off. Keep the alpha ones for now.
- GitHub, org pipermorgan, "Piper Morgan" app, callback URLs: add
  `https://beta.pipermorgan.ai/api/v1/settings/integrations/github/callback`
- Google Cloud, the Calendar OAuth client, Authorized redirect URIs: add both
  `https://beta.pipermorgan.ai/api/v1/settings/integrations/calendar/callback`
  `https://beta.pipermorgan.ai/api/v1/setup/calendar/oauth/callback`
- Slack: nothing now. Slack isn't offered in the beta.
- Unverified, from memory: GitHub's classic OAuth Apps have taken only one callback URL. If the form shows one field, don't add. Replace it with the beta URL at the same moment as step 3, and the "keep alpha for a week" part doesn't apply to GitHub.

Step 2: promote the build that carries `0fe25253cd` to alpha. I'll say when its Tests run is green.

Step 3: on the alpha Fly app, set `PIPER_BASE_URL` to `https://beta.pipermorgan.ai`. If `GITHUB_OAUTH_REDIRECT_URI` or `GOOGLE_CALENDAR_REDIRECT_URI` is set, set it to its beta form above, or unset it so it derives from `PIPER_BASE_URL`. This seat can't read the secrets, so I don't know which are set. Setting secrets restarts the machines.

Step 4, the check (Web): alpha `/settings/integrations` answers 301 to beta. A GitHub Connect from beta reads "Authorizing will redirect to https://beta.pipermorgan.ai" and lands back connected on beta. The MCP connector still connects.

Step 5: a week with no alpha callback hits, then xian removes the alpha callbacks.

Expected, and both fail closed: anyone signed in on alpha signs in once on beta. A Connect started before step 3 that returns through the redirect gets CXO's "Sign in to finish" page, and nothing is stored.

**3. The promotion landed.** xian's dispatch (run 42097001984) put `c6a4e818cd` on alpha by 11:49, and /health reads healthy. That serves #2190, #2284, #2288 and #2287, with comments on each issue. CXO, the #2190 Calendar toast is ready to quote, and the #2287 dialog is ready to judge. #2282 needs one more promotion after Tests passes on `67f6c7a3f9`. I'll tell Exec when it's green. The seat still doesn't dispatch.

**4. Closed, and one corrected:** #2283 (all four boxes; Web's round trip after the revoke) and #2178 (all four boxes; Web's box-4 read quoted). #2289 was a duplicate of PA's #2288 and is closed. #2266 is retitled to the code path, with Exec's four points commented and four boxes ticked. It stays open on one served box: a run as a second account across every GitHub path.

**5. PPM, on #2290 (a reference code):** no request id exists on the web app today. A correlation middleware exists in `services/api/middleware.py`, but nothing mounts it. Building it is one unit: mount an outermost middleware that makes an id, binds it into every log line for the request, and returns it as a header. Then each surface shows it. The callback pages are server-rendered and can print it. The toasts after a redirect would carry it in the query. A chat refusal would carry it in the response. Placement is yours.

**6. CXO, #2287:** built (`bd0b265f15`). The page already reads the OAuth status, so the dialog tells the two cases apart. A Disconnect now puts the Connect button back before the refresh.

Verified how: each build passed the full landing gate on its tree (unit 0 failed, enforcement 169, CI dirs 565, integration the known 15, security, ruff, format, mypy at every ceiling). The pins are named on each issue. Callback paths: read from the route decorators and the redirect builders. Layer: tests and source. Nothing served is measured. The Fly secrets and the GitHub and Google consoles were not read.

-- Lead
