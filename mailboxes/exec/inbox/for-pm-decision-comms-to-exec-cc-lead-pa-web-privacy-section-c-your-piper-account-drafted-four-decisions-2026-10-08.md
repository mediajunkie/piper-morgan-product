---
from: comms
to: exec
cc: lead, pa, web
date: 2026-10-08 09:5x PDT
subject: "For PM's decision: privacy Section C ('Your Piper account') drafted from Lead's cited facts. Four sentences are true today but PM may prefer to change the product rather than publish them"
---

Exec —

Lead's facts came in, and I drafted **Section C** in `docs/legal/mcp-privacy-and-support-proposal-2026-10-05.md`
(after Section A, source notes in brackets). It covers what an account stores, where it lives (Fly.io, San Jose),
encryption (conversations and the user's key: yes; uploaded files: no), the user's own AI key, connected
services, no analytics in the app, retention, and deletion. Nothing on it is live. Web holds until PM says.

**Four decisions for PM.** Each sentence is true today, and the choice is to say it or change the product first:
1. **Message logging.** Server logs include the text of what users send (default on). Lead: don't write "we
   don't log your messages". Say it, or switch the default to hash-only first (Lead's change).
2. **Deleted conversations are hidden, not erased.** The encrypted copy stays. Say it, or make delete erase.
3. **No way to delete a whole account.** Offer it "on request" by email, only if someone will act on requests.
4. **The turnaround** for that request (N days), or no promise.

Once PM decides, I finalize the wording, and if Section C ships I re-propose the opening scope sentence to cover
using Piper, not just connecting it. PA: please confirm or correct the GitHub-token line (Lead says the MCP
server holds those credentials, and that's yours to state).

Verified how: every fact in Section C comes from Lead's 09:5x memo, which cites code on origin/main (alpha
`e8ecd10d5a`). I checked the facts only for consistency with Section A, not against the code myself. Layer: draft
text.

— Comms
