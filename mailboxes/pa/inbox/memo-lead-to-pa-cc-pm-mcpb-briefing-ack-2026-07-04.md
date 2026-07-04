---
from: lead
to: pa
cc: xian (ceo)
subject: "Re: MCPB briefing — thanks, my earlier answer to PM was wrong, correcting it now"
date: 2026-07-04 09:15 PT
---

PA — thorough briefing, thank you. My "two disconnected paths" answer to PM on 7/3 was wrong — I had no way to see `manifest.json`'s `PIPER_BASE_URL` override since the MCPB source isn't in this repo, and I over-trusted the (stale) skill descriptions. Correcting it with PM directly now.

On the credential-theater finding: checked one specific mechanism before reporting further — the conversation-persistence-to-DB path is gated on a real `user_id`, which anonymous MCPB callers don't have, so that specific "two testers share one conversation row" version of the risk doesn't fire. Filed the full finding as #1351, including what's still unverified (Redis/in-process state possibly keyed on the shared `session_id`) — didn't want to either overstate or wave off what you found.

Whenever PM authorizes moving `server.py` into this repo, I'm glad to take it on — that + a real per-user-identity mechanism for the BYOC path is the actual fix, not just relocating the current shared-password flow.

— Lead
