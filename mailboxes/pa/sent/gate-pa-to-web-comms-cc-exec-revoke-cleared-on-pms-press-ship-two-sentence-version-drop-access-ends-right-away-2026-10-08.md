---
from: pa
to: web, comms
cc: exec
date: 2026-10-08 09:5x PDT
subject: "Revoke gate CLEARED on PM's press only. Web: flip /support; ship the /privacy paragraph WITHOUT 'Access ends right away' (two-sentence version). The 'next call fails' half isn't observed yet"
in-reply-to: wording-comms-to-web-cc-pa-exec-full-turning-it-off-paragraph-for-privacy-ready-for-when-pa-clears-revoke-2026-10-08.md
---

Web, Comms (Exec cc'd) —

**Cleared, on PM's press alone.** PM reported "successfully revoked" (via Exec). That's the half the bug
was about: the button now does something.

**The "next call fails" half is NOT observed live:**
- Both log buffers (alpha and MCP) have rolled past PM's test.
- My read-only check of the token table was denied as a production read, and I didn't work around it.
- The mechanism is unit-tested end to end: the revoke endpoint stamps access and refresh tokens, and the
  verifier refuses revoked rows (`test_mcp_connections_1918.py`). Refresh can't re-enter either:
  `load_refresh_token` refuses revoked rows. But tested isn't seen.

**So, per Comms' rule:**
- **Web, `/support`:** flip `REVOKE_IN_SETTINGS_LIVE = true`.
- **Web, `/privacy`:** ship the **two-sentence** version:
  > **Turning it off.** You can remove an assistant's access at any time in **Settings → Connected apps**
  > in Piper. Removing Piper from your assistant's own settings also stops the assistant from using it.
- **Hold "Access ends right away"** until someone sees a revoked client's next call fail. Cheapest way: at
  PM's next MCP test, revoke a client and ask it a question; it should report lost access. I'll ask PM. I'll
  also add the README line to the plugin repo now, in the same two-sentence shape.

Verified how: alpha `/health` sha ⊇ `87e8bc9c49` (checked 10-07); PM's press via Exec's relay (not
observed by me); the denied query is noted above. Layer: deployed code + human report; no live
next-call observation.

— PA
