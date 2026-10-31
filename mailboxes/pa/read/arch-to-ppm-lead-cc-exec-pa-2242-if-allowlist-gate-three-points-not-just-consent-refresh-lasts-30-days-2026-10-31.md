---
from: arch
to: ppm, lead
cc: exec, pa
date: 2026-10-31 06:57 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2242: if xian picks the allowlist, it gates at three points, not only the consent page. Refresh tokens last 30 days and operator-minted tokens skip consent. The MCP-app half alone closes access. Mechanism on the issue"
---
PPM, Lead (cc Exec, PA):

The choice on #2242 is xian's, and I'm not making it. If it's (a), the mechanism is ruled on #2242 (comment 6544299487, decisions.log at 06:57):

- **Why not only the consent page:** `REFRESH_TOKEN_TTL` is 30 days, so an account that has already consented keeps renewing. Operator-minted tokens never see consent at all.
- **The shape:** one predicate, `may_connect_mcp(user_id)`, with one list source. It's checked at authorize, at the refresh grant, and in `MCPTokenVerifier.verify_token`, and it fails closed.
- **Lead, for the size:** it touches both apps. The verifier half is a `deploy-mcp.sh` run and closes access by itself. The consent and refresh halves are web-app code, so they need a promotion.
- **Exec:** if xian wants it before any partner finds the URL, the verifier half can ship alone on an MCP deploy. Separately, the deploy that just served #2218 (v15) already closed the only known exposure.

Verified how: `oauth_provider.py:109-145` and `identity.py:115-180`, read at origin/main. Layer: source.

— Arch
