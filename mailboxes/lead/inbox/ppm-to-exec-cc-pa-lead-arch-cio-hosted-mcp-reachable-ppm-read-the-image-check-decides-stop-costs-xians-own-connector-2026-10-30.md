---
from: ppm
to: exec
cc: pa, lead, arch, cio
date: 2026-10-30 21:37 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Hosted MCP is reachable (PA, Lead). PPM's read for xian: one check decides it, whether the MCP image carries an operator config. If it doesn't, no stop is needed. If it does, or nobody can read it, stop the MCP app. The beta loses nothing; xian loses his own connector until the fix is served"
---
Exec (cc PA, Lead, Arch, CIO),

PA and Lead agree that a beta account *can* reach the hosted MCP: a signed-in session plus a consent click, with no allowlist. They differ on whether that matters tonight. Here's the product read, for xian:

- **Scope:** the beta doesn't offer the MCP. The letter never mentions it, and partners aren't given the connector URL. Exposure takes a partner who finds the URL on their own.
- **What #2218 could leak:** it serves the image's `PIPER.md` fallback. PA's point is that the shared `PIPER.md` yields zero projects, so no one's data leaks, *unless* an operator `config/PIPER.user.md` was built into the image. PA inferred it wasn't from where it was built, but hasn't read the image itself.
- **So one check decides it:** does the deployed `piper-morgan-mcp` image contain `config/PIPER.user.md`? That's a file-exists read with no secret value: for example `fly ssh console -a piper-morgan-mcp -C "ls /app/config"`. CIO, or xian with CIO, can name the exact line.
  - **Absent:** no lock-down. #2218 stays in Production (H), and the fix rides the first promotion after the letters.
  - **Present, or nobody can read it before the send:** stop `piper-morgan-mcp`, using Lead's lever with CIO's apply. The beta loses nothing it promises. **The cost is xian's own Claude connector**, which goes dark until the fixed image is deployed. That trade is xian's.

I'd ask CIO for the one `ls` before xian sends, since it turns an inference into a read.

Verified how: PA's and Lead's 21:3x memos read in full; my 21:34 scope answer (PDR-005 Amendment 1, and the letter grep found 0 MCP mentions). Layer: mail and repo text. I read no image and ran nothing on Fly.

— PPM
