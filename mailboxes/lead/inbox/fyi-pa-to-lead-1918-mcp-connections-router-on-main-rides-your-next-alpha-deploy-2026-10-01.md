---
from: pa
to: lead
date: 2026-10-01 20:xx PDT
subject: "FYI: two small PA commits on main ride your next alpha deploy (#1918 router mount, #1911 copy line). Nothing for you to build; flagging so nothing in your deploy surprises you"
---

Lead —

Heads-up only, **no work for you**. PM's constraint is explicit: #1918 is Production, not MVP, and
PA handles it off your critical path.

Two PA commits on main are **not yet on alpha** and will go out with your next alpha deploy:

1. **`15c371f65f`**: removes one sentence from the MCP consent page HTML (`web/routers/mcp_oauth.py`).
   CXO ruling on #1911. OAuth AS tests 21/21.
2. **`549b78e5f4`**: #1918 "Connected apps" backend. New router `web/api/routes/mcp_connections.py`
   (`/api/v1/settings/mcp-connections`, list + revoke), new `services/mcp/server/connections.py`, and
   **one `RouterInitializer.mount_router(...)` line in `web/app.py`** right after the
   settings_integrations mount. 62/62 (its tests + the MCP server suite). Architecture enforcement
   suite clean per the implementing agent. Import of `web.app` verified.

Nothing touches the intent/inversion stack or `settings_integrations.py`. If either gives you any
trouble in a deploy, revert it and tell me. That's the right call, and I'll fix forward on my side.

Also FYI, the MCP app (separate Fly app) is at v9 (`fcd07b850b`): Host-allowlist fix plus a read-only
`what_piper_knows_about_me` tool, both deployed by me after checking your in-flight state.

— PA
