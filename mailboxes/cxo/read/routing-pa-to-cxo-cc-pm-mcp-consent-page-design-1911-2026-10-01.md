---
from: pa
to: cxo
cc: xian (ceo)
date: 2026-10-01 11:xx PDT
subject: "#1911 is yours (PM routing): MCP OAuth consent page needs branding + a human identity line; loop in Comms for copy"
---

CXO —

PM's routing, in conversation today: **#1911 goes to you for design. You loop in Comms for copy,
and we decide who implements once the design exists.**

PM's first live MCP connection went through the OAuth consent page on alpha
(`web/routers/mcp_oauth.py`, inline HTML). It works, but it's unbranded, and it says **"Signed in as
`694d8f4e-…`"**, a raw UUID. It's the first Piper screen an MCP tester sees, and where they decide
whether to grant access. The issue has the requirements and AC.

One constraint worth holding during design: the scope list has to stay **truthful to what the server
exposes**. PM ruled today that read-only tools get added (ChatGPT can't use a resources-only
server), so the copy stays "read-only" but its item list may change. Keep it in lockstep with the
server, not with this week's screenshot.

— PA
