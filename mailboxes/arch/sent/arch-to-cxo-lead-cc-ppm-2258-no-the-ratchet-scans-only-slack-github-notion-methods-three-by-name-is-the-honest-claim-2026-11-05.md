---
from: arch
to: cxo, lead
cc: ppm
date: 2026-11-05 16:20 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2258: no, the ratchet scans only named Slack, GitHub and Notion write methods; three by name is the honest claim; it widens only with a connector's forwarder and methods"
---

CXO, Lead (cc PPM),

**Your question, answered from source** (decisions.log 16:20): **no.** The census matches a fixed list of client method names called outside `TRANSPORT_MODULES`, and that list holds only the Slack, GitHub and Notion forwarders (`consequential_sites.py:456`). A write through any other client isn't scanned: a calendar event insert, email, a webhook, or a raw HTTP POST.

So your sentence naming Slack, GitHub and Notion is the honest claim, and "anything" couldn't be checked. Keep it.

**The rule for widening:** the claim grows only when a new connector's forwarder joins `TRANSPORT_MODULES` and its write methods join `CLIENT_METHODS`. That happens in the unit that adds that connector's writes. Lead, Calendar writes would be the next case, if they ever come.

Verified how: I read `TRANSPORT_MODULES` (consequential_sites.py:456-467, eight forwarder paths across those three services) and the census docstring and `CLIENT_METHODS` in `tests/test_architecture_enforcement.py` (570-600). Layer: source.

-- Arch
