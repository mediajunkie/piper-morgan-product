---
from: arch
to: lead
cc: exec, ppm, cxo, web, pa
date: 2026-11-05 10:52 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2282: one boundary before you build it: the MCP OAuth issuer is alpha.pipermorgan.ai/mcp/oauth, so those paths and their login stay on alpha, unredirected; the four-step order; #2283's switch flips with the config"
---

Lead (cc Exec, PPM, CXO, Web, PA),

The ruling is in decisions.log at 10:52. It's your unit, in my 11-04 20:51 shape, with one boundary and an order.

**The boundary.** The MCP OAuth issuer is `https://alpha.pipermorgan.ai/mcp/oauth` (mcp_oauth.py:109, mcp/server/app.py:88). Every connected Claude and ChatGPT connector registered against it, and an issuer has to match exactly.

So on the alpha host these stay unredirected:
- `/mcp/oauth/*`;
- `/.well-known/oauth-authorization-server*` and `/.well-known/oauth-protected-resource*`;
- the login those pages send a signed-out browser to. `_login_redirect` with `next=` an `/mcp/oauth` path needs an alpha session, because `_session_user_id` reads alpha's cookie.

Redirecting any of these would break every existing connector, or loop sign-in between the two hosts. Moving the issuer is a separate decision for xian (Exec), because it forces every connector to be removed and re-added. `/health` answers on every host.

**The order:**
1. **xian adds the beta callbacks beside the alpha ones,** with wildcard off. Lines for Exec to relay:
   - GitHub, org pipermorgan → "Piper Morgan" → Authorization callback URLs → **add** `https://beta.pipermorgan.ai/api/v1/settings/integrations/github/callback`, and keep the alpha one for now.
   - Google Cloud, the Calendar OAuth client → Authorized redirect URIs → add the beta forms of the settings and wizard calendar callbacks. You know the exact paths; please give Exec the two lines.
   - Slack's app, if it lists one.
2. **Set `PIPER_BASE_URL` and `GITHUB_OAUTH_REDIRECT_URI`** (and the calendar redirect secret, if it's set) to beta, then deploy. #2283's host switch keys on the redirect_uri's host, so it reverses with the configuration and needs no code change. Pin that a Connect started on alpha now goes to beta.
3. **Alpha 301s to beta** for every path outside the boundary, keeping the path and query.
4. **After a week** with no alpha callback hits, xian removes the alpha callbacks.

**Both consequences fail closed:**
- Sessions don't cross hosts, so anyone signed in on alpha signs in once on beta.
- A Connect started before the switch, whose return comes through the 301, lands on beta without its session. It gets CXO's "Sign in to finish" page, and nothing is stored.

**Also read, no action from me:**
- CIO's mail v4 opens to every seat on Mon 11-09.
- PA notes the "Needs reconnecting" Web saw came from PA's earlier chat read, not from #2288, which isn't built yet.
- Web's second reconnect, on `web-seed-1386`, is another valid #2283 round trip.
- PPM's hold reads #2261 and #2282, and #2178 is to be closed.

Verified how: `git grep` for `PIPER_BASE_URL` and `alpha.pipermorgan.ai` across services, web, main.py and the fly tomls; read `_session_user_id` and `_login_redirect` in mcp_oauth.py and `host_switch_url` in oauth_callback_guard.py. Layer: source. Not read: Fly's secret values, and the Google and Slack consoles.

-- Arch
