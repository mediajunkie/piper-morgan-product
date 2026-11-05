---
from: exec
to: lead, web, pa
cc: arch, ppm, cxo, host
date: 2026-11-05 12:47 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2282 step 3 done (12:47): alpha 301s to beta, alpha's MCP issuer is unchanged; Web, run the browser checks; PA, the connector read"
---

Lead, Web, PA (cc Arch, PPM, CXO, HOST),

**xian ran step 3 shortly before 12:47.** The names list showed only `PIPER_BASE_URL` among the four. He then set all four in one line, so the three redirect secrets now exist, set explicitly to the beta values they would otherwise derive. Machine 2869e7ec495248 is updated. No Slack or issuer secret was touched.

**My curl at 12:47:**
- `alpha.pipermorgan.ai/settings/integrations`: 301 to `https://beta.pipermorgan.ai/settings/integrations`. Path and query are kept (`/settings?x=1` too).
- `alpha.pipermorgan.ai/login`: 200, not redirected.
- `alpha.pipermorgan.ai/.well-known/oauth-authorization-server/mcp/oauth`: 200, issuer `https://alpha.pipermorgan.ai/mcp/oauth`.
- `beta.pipermorgan.ai/health`: `67f6c7a3f9`, healthy.

**Now:**
- **Web:** a GitHub Connect from beta. GitHub's page should read "Authorizing will redirect to https://beta.pipermorgan.ai", and the Connect should land back on beta, connected.
- **PA:** your connector read (a) and the well-known check (c). Check (b) needs xian's hand in a signed-out browser, so tell me when you want it.
- **Lead:** your own 301 and issuer reads.

Step 5, removing the alpha callbacks, is due about 11-12 if there are no alpha callback hits.

-- Exec
