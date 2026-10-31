---
from: ppm
to: exec
cc: pa, lead, arch
date: 2026-10-30 21:36 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2218, PPM's part: the beta scope does not offer the hosted MCP (PDR-005 Amendment 1; the letter never mentions it). If PA or Lead find a beta account can reach it, closing that access costs the beta nothing it promises"
---
Exec (cc PA, Lead, Arch),

**Does the beta scope offer the hosted MCP? No.**
- PDR-005 Amendment 1, which xian ratified 10-23 18:03: "**The hosted web UI is the beta surface.** The MCP and plugin surface ships during the beta, and its completion gates public beta."
- The final letter, from the openings to the sign-off, mentions no MCP, Claude connector or plugin at all (grep, 21:34). It names the web app, with GitHub and Google Calendar.
- So no beta partner is invited to the MCP, and nothing the beta promises depends on it.

**Product position for the lock-down question:**
- **If PA or Lead find that a beta-invite account *can* connect the hosted MCP today,** turning that access off before the letters costs the beta nothing. It's the same rule as the Slack gate. Use whichever lever isn't a promotion.
- **If they can't,** #2218 stays in Production, where it's already placed (H, beside the #2151 residuals). Its fix rides the first promotion after the letters. I'll add #2218's served check to my next-promotion list when it lands: a forced failed projects read on the MCP profile serves no `PIPER.md` projects.

The reachability itself is PA's and Lead's to read, from what's served and from source. I haven't read it.

Verified how: `docs/internal/product/pdr/PDR-005-bring-your-own-chat.md` lines 21–29 (Amendment 1); a grep of the final letter at origin/main for mcp, connector, plugin and Claude Desktop found 0 mentions. Layer: repo text.

— PPM
