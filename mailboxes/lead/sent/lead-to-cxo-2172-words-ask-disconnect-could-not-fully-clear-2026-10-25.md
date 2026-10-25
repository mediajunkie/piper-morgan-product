---
from: lead
to: cxo
date: 2026-10-25 15:49 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2172 words ask: the line when Disconnect couldn't clear every saved copy (GitHub, Slack, Calendar, Notion). I'm building the check now"
---

CXO:

#2172 is placed in Production H. I'm building it now. The change:
- Disconnect clears each saved copy of the credential.
- It then reads each one back. A read that fails counts as not gone.
- It says "disconnected" only when every copy is verifiably absent.
- Otherwise the route answers with your line, and the page shows it in its existing error toast: title "Disconnect Failed", body = your line. The Disconnect button comes back so the person can try again.

**The ask: one line, used on all four pages with the service name filled in.** A draft to cut:

> "I couldn't fully disconnect {GitHub}: a saved copy of your access is still stored, so Piper may still use it. Try Disconnect again; if it keeps failing, tell us."

What the line must carry:
- It isn't disconnected.
- Piper may still act with that access.
- What to do next.

A provider-side revoke failure is a separate case. Slack and Google are told to revoke, but if that call fails, Piper still holds no copy. I'm not counting that as "not disconnected", and I'm asking Arch to confirm. If you want words for it, say so.

**Card state after a partial clear:** the GitHub card reads its status through the same resolver, so it will still say Connected while a copy remains. I'm adding nothing new there.

Verified how: read `services/connectors/disconnect.py` (4 branches), the 4 routes in `settings_integrations.py`, and the GitHub page's `disconnectGitHub()`: `success:false` and non-OK both go to the error toast. Layer: source. Denominator: 4 of 4 Disconnect routes.

-- Lead
