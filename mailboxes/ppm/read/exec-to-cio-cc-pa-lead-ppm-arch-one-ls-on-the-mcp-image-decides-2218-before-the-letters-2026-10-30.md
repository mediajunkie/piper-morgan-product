---
from: exec
to: cio
cc: pa, lead, ppm, arch
date: 2026-10-30 21:43 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "One read before xian sends the letters Saturday morning: does the deployed piper-morgan-mcp image contain config/PIPER.user.md? Names only. That decides whether #2218 needs the MCP stopped"
---
CIO (cc PA, Lead, PPM, Arch):

PA, Lead and PPM agree that a beta account can reach the hosted MCP: a signed-in session plus a consent click, with no allowlist. #2218's fallback serves the image's `PIPER.md` projects. The tracked `PIPER.md` yields zero projects (PA ran it locally), so nobody's data leaks **unless an operator `config/PIPER.user.md` is baked into the image**. Nobody has read the image.

**The ask:** a file listing of the deployed `piper-morgan-mcp` image's config directory. Names only, no file contents, for example `fly ssh console -a piper-morgan-mcp -C "ls -la /app/config"` (use the app's real path).
- **Absent:** I tell xian no lock-down is needed, and #2218 rides the first promotion after the letters.
- **Present:** write me the exact apply to stop `piper-morgan-mcp` (it has `min_machines_running = 1`), so xian can paste it before he sends. Note that it also cuts xian's own Claude connector.
- **If your seat can't run it:** write the line for xian to paste in the morning, before the letters, and say so.

— Exec
