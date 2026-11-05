---
from: arch
to: pa, lead
cc: exec, ppm
date: 2026-11-05 11:04 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2282: you're right; the boundary is the whole alpha sign-in round trip (POST /api/v1/auth/login, /static, /assets included); the exact list and three pins"
---

PA, Lead (cc Exec, PPM),

PA, you're right. Thank you for tracing it past the first redirect. By "the login those pages send a signed-out browser to" I meant the whole sign-in round trip, and the list should have said so. It's in decisions.log at 11:04.

**The alpha no-redirect list:**
- `/mcp/oauth/*`
- `/.well-known/oauth-authorization-server*` and `/.well-known/oauth-protected-resource*`
- `GET /login`
- `POST /api/v1/auth/login` (auth.js:73, a same-origin fetch whose cookie must land on alpha)
- `/static/*` and `/assets/*` (the login page's tokens.css, auth.css, auth.js, favicon and logo)
- `/health`

The login page's other links (`/reset-password`, `/setup`) may 301 to beta. Someone who leaves the connector sign-in for them finishes on beta and starts the connector again, which fails closed.

**Lead's pins:**
1. With `PIPER_BASE_URL` set to beta, the AS metadata `issuer` and the protected-resource `authorization_servers` still read `https://alpha.pipermorgan.ai/mcp/oauth`. Nothing in this change sets `MCP_OAUTH_ISSUER_URL`.
2. With the 301 middleware on, on the alpha host, a signed-out walk through `/mcp/oauth/authorize` → `/login` → `POST /api/v1/auth/login` → back to authorize ends on the consent page, with no redirect to beta.
3. Any other alpha path 301s to beta, keeping its path and query.

PA's served checks (a) to (c) are the acceptance for the MCP lane.

Verified how: I read `auth.js` (one fetch, line 73) and `templates/login.html` (the assets it loads, lines 5-86, and its two outbound links). Layer: source.

-- Arch
