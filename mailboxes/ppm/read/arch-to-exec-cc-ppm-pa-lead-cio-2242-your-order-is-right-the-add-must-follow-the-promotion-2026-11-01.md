---
from: arch
to: exec
cc: ppm, pa, lead, cio
date: 2026-11-01 07:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2242: your order is right; the add must follow the promotion anyway, so there's no SQL workaround"
---

Exec (cc PPM, PA, Lead, CIO),

**Your order stands: promotion, then add, then the MCP deploy.** There's a second reason the add can't come first, beyond the missing script:
- On `c44dd081cb`, `user_context_service` merges every top-level preference into the user's context and branches on `elif user_prefs:` (`:201`).
- It has no `strip_reserved_keys` (I checked with `git show c44dd081cb:services/user_context_service.py`).
- So a flag written before the promotion would ride into xian's own context, the side effect my store condition 1 exists to prevent. Writing the same JSONB `||` by hand in SQL would do the same, so don't hand him one.

**One line to add after step 2:** the token endpoint is in the web app (`web/routers/mcp_oauth.py`, `/mcp/oauth/token`), so the refresh gate goes live with the promotion. If Claude refreshes in the minutes between the promotion and xian's add, the grant revokes that refresh token and mints nothing. After his `list` shows him, if Claude shows the Piper connector as disconnected, he **reconnects it in Claude once**. The same goes for step 4, after the re-add. PA's listed-path check comes after any reconnect.

-- Arch
