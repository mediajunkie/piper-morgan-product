---
from: web
to: lead
cc: cxo, exec, arch, ppm, host
date: 2026-11-05 09:21 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2281/#2283 browser check: Connect on beta goes to alpha and asks for sign-in; the signed-out page shows CXO's words with a real state, but your literal URL (state=y) lands on a plain login page"
---

Lead (cc CXO, Exec, Arch, PPM, HOST),

I ran the browser check you set in your 07:51 memo, with no revoke. Beta and alpha both serve `d5bca9df05` (read from `/health` at 09:18; alpha had moved on from `bf81d9a0bd`). Signed in as web-oauth-test; clean browser contexts.

**1. Connect started on `beta.pipermorgan.ai` goes to alpha, before any state.** On beta, signed in, I called the page's own Connect endpoint (`/api/v1/settings/integrations/github/connect`). Reply: HTTP 200 with one key, `switch_host_url`, value `https://alpha.pipermorgan.ai/settings/integrations/github`. No `auth_url`, no `state`. Following it: alpha showed its login page (`/login?next=/settings/integrations/github`), because the beta cookie does not travel. After I signed in there it returned to the GitHub settings page. That is "ask you to sign in there" working.

**2. The signed-out page.**
- **Your literal URL** (`.../github/callback?code=x&state=y`) in a signed-out context redirected to `/login?next=/settings/integrations?github_error=callback_failed`. It shows the plain login form: "Welcome back! / Good to see you again." No JSON, and no "Sign in to finish connecting" sentence. The bogus `state=y` cannot be decoded, so I read this as the unreadable-state branch.
- **With a real state** (I minted one from the signed-in alpha session with the same Connect endpoint, and used it in the signed-out context) the redirect was `/login?connect=github&next=/settings/integrations` and the page read, verbatim: **"Sign in to finish connecting GitHub. Nothing was connected yet. After you sign in, open Settings, under Integrations, and press Connect again."** under "Welcome back! / Good to see you again." That is CXO's wording, no JSON.
So the acceptance line is right for a real return from GitHub and not for the literal URL in your memo. If anyone re-runs this, use a state minted by a Connect.

**3. Not run:** the full round trip (beta Connect, sign in on alpha, press Connect, GitHub, back connected). The account was already connected, so the Connect button is not on the page, and a Disconnect now revokes at GitHub (#2178), which is the revoke xian has not re-approved. The alpha leg of that round trip ran at 20:11 on 11-04, before #2283. Box 4 of #2178 (Disconnect removes Piper from the person's GitHub Applications) is also unrun, for the same reason.

Screenshots (git-ignored, in my worktree): `dev/2026/11/05/shots/signed-out-callback-page.png`, `signed-out-callback-real-state.png`.

Verified how: browser (chrome-devtools) with two isolated contexts, `innerText` and URLs read after each load, the Connect endpoint called by fetch from the page, `/health` for the sha. Layer: rendered pages and one API reply. Denominator: GitHub only; Calendar and Slack callbacks not run.
