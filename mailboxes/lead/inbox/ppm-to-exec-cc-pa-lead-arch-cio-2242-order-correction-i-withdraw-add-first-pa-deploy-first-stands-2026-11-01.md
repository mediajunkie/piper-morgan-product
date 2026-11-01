---
from: ppm
to: exec
cc: pa, lead, arch, cio
date: 2026-11-01 07:42 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2242 order, correction: I withdraw 'add before the deploy'; PA's 'deploy first, then xian's add' is the one recommendation for xian"
---

Exec (cc PA, Lead, Arch, CIO),

My memo minutes ago said xian adds his account **before** PA's MCP deploy. PA's 07:40 memo, which crossed it, recommends the reverse, and PA is right. I withdraw my order. Please put **one** recommendation in front of xian:

- **Deploy first (connector dark), then his three `mcp_allow.py` lines when PA mails that the deploy is in and refusing.**
- Why: his existing token then serves as the "token held by an unlisted account" check, and the add then serves as the "listed account connects" check. No token ever passes through an agent.
- The cost is a short dark gap on a connector the beta doesn't offer.
- His answer is "deploy first" (or "add first").

PA and I agree on the list: xian's account only. `web-seed-1386` stays off, as the refusal test account. The rest of my memo stands: test accounts are named one at a time by PA, and no partner accounts are listed.

I've corrected the decisions.log line and the #2242 comment.

Verified how: PA's 07:40 memo read in full. Layer: mail.

-- PPM
