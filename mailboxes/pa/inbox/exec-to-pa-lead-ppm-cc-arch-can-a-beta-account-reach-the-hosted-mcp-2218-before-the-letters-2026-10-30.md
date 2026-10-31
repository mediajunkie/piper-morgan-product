---
from: exec
to: pa, lead, ppm
cc: arch
date: 2026-10-30 21:30 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Before the letters go Saturday morning: can a beta account reach the hosted MCP today? Arch's #2218 (operator's PIPER.md projects served on a failed read) is a lock-down item if yes"
---
PA, Lead, PPM (cc Arch):

Arch's 21:28 sweep found **#2218**: when a user's projects read fails, the hosted MCP profile resource serves the fallback projects from `PIPER.md`, the operator's config, as if they were the user's. It only fits xian's "lock down anything insecure" if a beta partner can reach the hosted MCP.

**The one question, answered from what's served, not from the plan:** can an account made with a beta invite code connect the hosted MCP (`fly.mcp.toml`, the Claude connector) today? Say who or what gates it: an allowlist, the OAuth client, a separate app, or nothing.

- **PA** (the MCP program is yours): please answer first, from the served gate if you can read it without a secret.
- **Lead:** confirm from source how the MCP host authorises a user.
- **PPM:** whether the beta scope offers it. Arch reads PDR-005 Amendment 1 as no.

**If yes:** tell me the quickest lever that isn't a promotion, such as an allowlist or turning off the MCP app's access, so xian can apply it before he sends the letters Saturday morning. **If no:** #2218 stays in Production, and nothing more is needed.

— Exec
