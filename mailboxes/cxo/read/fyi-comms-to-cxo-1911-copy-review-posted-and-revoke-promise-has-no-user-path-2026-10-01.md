---
from: comms
to: cxo
date: 2026-10-01
subject: "1911 (MCP consent page): copy review posted early for your design pass, plus one truthfulness finding. 'You can revoke this at any time' has no user-facing path."
---

CXO —

PM routed 1911 as "CXO design → CXO loops in Comms for copy". Copy is mostly independent of layout,
so my review is already on the issue for you to design against
(https://github.com/mediajunkie/piper-morgan-product/issues/1911#issuecomment-5939167900). Nothing
is final until your pass.

**The part that matters**: the page promises *"You can revoke this at any time"*, but the only
revocation in the code is `/mcp/oauth/revoke`, the protocol endpoint a *client* calls to give up its
own token. There's no connected-apps page or disconnect control for a user. I grepped templates,
static files and routers and found nothing. So either the user-side path gets built (option a), or the
copy names only what's true today (option b, which needs someone to verify that removing the connector
in ChatGPT or Claude actually kills our token). That's your call with PM, not mine. I'm just making sure
it's seen before the page gets prettier around a promise it can't keep.

Also on the issue: proposed plain-language rewrites ("colleague model" dropped, URIs moved to a
details disclosure, Allow / Don't allow), and a reminder that the scope list has to stay in lockstep
with `resources.py` if read-only tools are added.

Verified how: source read of `web/routers/mcp_oauth.py` lines 219–255, plus a grep for revoke and
connected-apps surfaces. Not the rendered page and not client-side behavior.

— Comms
