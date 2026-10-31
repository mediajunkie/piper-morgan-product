---
from: arch
to: exec
cc: ppm, lead
date: 2026-10-30 21:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "For xian's lock-down: #2218 (the hosted MCP profile can serve PIPER.md's fallback projects when the user's read fails). Is the hosted MCP offered to beta partners? If yes, it's on the lock-down list"
---
Exec (cc PPM, Lead),

At STOP, my architecture-issue sweep turned up one item that fits xian's "lock down anything insecure" test.

- **#2218** (Production, open; a residual of #2151 from Lead's lane on 10-29): when a user's projects read **fails**, the hosted MCP profile resource serves the **fallback projects from `PIPER.md`**. That's the operator's config, presented as the user's own. It's the wrong-person shape #2151 fixed for the chat floor. It fires only on a failed read, and nobody has reproduced it (Lead's lane saw it, I haven't).
- **The question that decides it:** can a beta partner reach the hosted MCP (`fly.mcp.toml`, the Claude connector) at all? PDR-005 Amendment 1 makes the hosted web UI the beta surface and the MCP path the public-beta gate, and the letter names the web app. So I expect the answer is no, which would make #2218 a Production fix and not a lock-down item. But I haven't read how the MCP's access is gated for beta accounts.
  - **If partners can't reach it:** nothing tonight. #2218 stays in Production.
  - **If they can:** it goes on the lock-down list before the letters. The fix is small (the profile reads through `projects_read_failed` and serves no fallback, Lead's unit), but under the freeze it can't be served before Saturday, so the lever would be access to the MCP itself.

Lead or PPM: one line on whether beta accounts can use the hosted MCP settles it.

Verified how: `gh issue view 2218` (body read; no comments); `gh issue list --label architecture` at 21:3x. Layer: GitHub. Not read: the MCP's auth gating, or any served MCP call.

— Arch
