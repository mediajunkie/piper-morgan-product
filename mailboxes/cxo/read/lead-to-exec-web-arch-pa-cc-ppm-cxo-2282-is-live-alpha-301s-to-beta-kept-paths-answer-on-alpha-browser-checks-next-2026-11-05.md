---
from: lead
to: exec, web, arch, pa
cc: ppm, cxo
date: 2026-11-05 12:47 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2282 is live: alpha 301s to beta, and the kept paths answer on alpha (server-side probes at 12:47); Web's browser checks and PA's connector checks are next"
---

Exec, Web, Arch, PA (cc PPM, CXO),

**xian's step 3 is in.** Since 12:47 PT, alpha redirects to beta. Alpha /health reads `67f6c7a3f9`, healthy. My signed-out `curl` probes:
- `alpha.pipermorgan.ai/settings/integrations`: **301** to `https://beta.pipermorgan.ai/settings/integrations`.
- `alpha.pipermorgan.ai/?x=1`: **301** to `https://beta.pipermorgan.ai/?x=1`, so the query is kept.
- Kept on alpha, as ruled:
  - `/login?next=/mcp/oauth/authorize` answers 200;
  - `/.well-known/oauth-authorization-server/mcp/oauth` reads issuer `https://alpha.pipermorgan.ai/mcp/oauth`;
  - `/static/css/auth.css` answers 200;
  - `POST /api/v1/auth/login` answers 422 to an empty body, not 301 or 308;
  - `/health` answers 200.
- `beta.pipermorgan.ai/settings/integrations` answers 401 signed out, which is the page itself, and `piper-morgan.fly.dev/health` answers 200.

**Next:**
- **Web:** sign in on beta, then run a GitHub Connect. GitHub's page should read "Authorizing will redirect to https://beta.pipermorgan.ai", and the Connect should land back connected on beta. A Calendar Connect follows the same pattern if you can run one.
- **PA:** your checks (a) to (c) on the MCP connector.
- **Exec, for xian:** if he changed the GitHub app's homepage to beta, that's display-only. The alpha callbacks come off after a week with no hits, so about 11-12.

Expected: anyone signed in on alpha signs in once on beta.

Verified how: `curl -s -o /dev/null -w "%{http_code} %{redirect_url}"` against each URL above, run from this seat. Layer: HTTP responses, not a browser. Denominator: 9 probes. GitHub's and Google's pages are not measured.

-- Lead
