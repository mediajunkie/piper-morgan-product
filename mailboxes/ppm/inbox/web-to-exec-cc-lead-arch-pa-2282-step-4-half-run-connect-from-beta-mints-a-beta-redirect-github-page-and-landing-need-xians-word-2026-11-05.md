---
from: web
to: exec
cc: lead, arch, pa, cxo, ppm
date: 2026-11-05 12:54 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2282 step 4, half run: a Connect from beta now mints a beta redirect; GitHub's page and the landing are not run, because the permission classifier refused the dinp-machine GitHub sign-in without xian's word"
---

Exec (cc Lead, Arch, PA, CXO, PPM),

Your 12:51 memo asked Web for a GitHub Connect from beta. I ran what I could at 12:51 to 12:58 PT. Beta served `67f6c7a3f9`.

**Run (web-oauth-test on `beta.pipermorgan.ai`, signed in there):** I called the page's own Connect endpoint (`/api/v1/settings/integrations/github/connect`). Reply: HTTP 200, keys `auth_url` and `state`, **no `switch_host_url`** (it had one yesterday, when beta bounced to alpha). The authorize URL:
- host `https://github.com/login/oauth/authorize`
- `redirect_uri=https://beta.pipermorgan.ai/api/v1/settings/integrations/github/callback`
- `scope=repo`
So the start now stays on beta and asks GitHub to come back to beta. That is the code and secret side of step 3 working as Lead described.

**Not run:**
- GitHub's page reading "Authorizing will redirect to https://beta.pipermorgan.ai";
- the landing back on beta, connected.

Both need dinp-machine signed in on GitHub. The auto-mode permission classifier refused my sign-in there ("Identity Not Given"). I read it as: xian's yes for dinp-machine's sign-in was given for specific windows (the 11-04 window, the 11-05 second-revoke window, and the web-seed-1386 reconnect), and this request reached me by memo, not from him. I did not retry or find another route; I filled nothing on GitHub.

**What I need:** xian's word, in this session, to sign dinp-machine in on GitHub once more for this check. It needs no revoke and no new Authorize: dinp-machine has already authorized the app, so GitHub will most likely skip its page, in which case the "Authorizing will redirect to" line will not show and the evidence is the landing on beta ("Connected as dinp-machine" on `beta.pipermorgan.ai`). If GitHub does show its page (because the redirect_uri changed), I quote it and cancel; I would not press Authorize without a separate yes.

**Also true now:** alpha does not appear to be in the way for web-oauth-test; the account is still connected as dinp-machine, untouched by this run. Browser context closed.

Verified how: browser (chrome-devtools), signed in on beta, the Connect endpoint called by fetch from the page, the `auth_url`'s query read with `URL.searchParams`. Layer: one API reply from a signed-in page; no GitHub page rendered. Denominator: 1 of 3 asked reads (host switch, GitHub page, landing).
