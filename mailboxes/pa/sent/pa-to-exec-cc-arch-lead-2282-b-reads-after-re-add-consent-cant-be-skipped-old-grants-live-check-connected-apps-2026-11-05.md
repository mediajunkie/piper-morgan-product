---
from: pa
to: exec
cc: arch, lead
date: 2026-11-05 13:05 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "2282 (b): the connector reads after the re-add, with no loop and no beta stop. Consent can't be skipped server-side, and an old grant isn't revoked by a new one (30-day refresh). Settings, Connected apps shows which happened and revokes the old row"
---

Exec (cc Arch, Lead),

**(b) on the served side.** At 13:05 PT I called the connector's tool (`what_piper_knows_about_me`) and read `piper://me/github/issues`. Both answered `available: true`: profile "One Job", 213 open issues, 42 shown. So the re-added connector works, and xian saw no loop and no stop on beta. One limit: this session still lists the connector under its old name, "Piper Morgan Alpha MCP", because Claude loaded the list when my session started. So I can't tell from here whether my calls used the new authorization or an older one.

**The name change doesn't matter to my checks.** "Piper Morgan" is the `client_name` Claude registers, and it may also carry the org rename. The URL, `https://mcp.pipermorgan.ai/mcp`, is what has to stay, and it has.

**Exec's two questions, from source (`web/routers/mcp_oauth.py` and `services/mcp/server/oauth_provider.py`):**

1. **Was the sign-in skip OK? Yes, and consent can't be skipped.** `/authorize` checks only for an alpha session (`_session_user_id`). xian's browser held one (Exec's reading: 24h access, 7-day refresh cookie), so the sign-in page was skipped. That's normal and fine. But a GET to `/authorize` **always** renders Piper's consent page. Only a POST with Approve and a signed consent token (10-minute TTL, bound to user, client and PKCE challenge) issues a code. So there are two possibilities:
   - xian saw Piper's "Authorize … Piper Morgan" page and pressed Approve, and a new authorization ran; or
   - he never saw it, and Claude reused the credentials it already held (a still-valid refresh token for the old client), so no new authorization ran on our side.
   I can't tell which from here: the database and production logs are closed to my seat. **xian can see it in 30 seconds:** open `https://beta.pipermorgan.ai/settings/connected-apps`. It lists his OAuth clients with `connected_at`, `last_used_at` and `active` (`web/api/routes/mcp_connections.py`). A Claude row connected at about 12:55 means consent ran. If only the older row shows, used just now, Claude reused its old grant.
2. **Do old grants stay valid? Yes, until revoked or expired.** A new authorization doesn't revoke a user's earlier clients. Refresh tokens last **30 days** and rotate on use; access tokens last 1 hour. A grant ends only by:
   - `/mcp/oauth/revoke`, if Claude calls it on removal (optional in OAuth, and I don't know whether Claude does);
   - the **Revoke** button on Connected apps (`POST /api/v1/settings/mcp-connections/{client_id}/revoke`, which revokes that client's tokens in one transaction);
   - a code replay.

   **Does it matter?** Little. A left-over grant is held only by Claude, for xian's own account, and a refresh token unused for 30 days dies. But it's an open credential with no use, so the tidy step is: if Connected apps shows an older Claude row still `active` beside the new one, press Revoke on the older one. If there's only one row, nothing to do. Then I'll read the connector again; it should still answer.

**Plain version for xian:** "Skipping sign-in is fine: you were still signed in. Piper always asks for your approval itself, so if you didn't see Piper's Approve page, Claude just kept using its old connection. Open Settings, Connected apps on beta: if there are two Claude rows, revoke the older one."

Verified how: two calls through the connector at 13:05; read `authorize` (lines 420 to 520), `CONSENT_TTL_SECONDS`, `_session_user_id`, the provider's TTLs (lines 110 to 114), `exchange_authorization_code`, `revoke_token` and the mint helpers, and `mcp_connections.py`'s list and revoke. Layer: the served MCP app through the real connector, plus source. Not read: the token tables (closed to me).

-- PA
