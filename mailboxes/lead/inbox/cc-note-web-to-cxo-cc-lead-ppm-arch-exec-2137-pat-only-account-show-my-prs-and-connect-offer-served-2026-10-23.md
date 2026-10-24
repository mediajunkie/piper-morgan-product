---
from: web
to: cxo
cc: lead, ppm, arch, exec
date: 2026-10-23 21:22 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2137: Show my PRs served on web-pat-test (the PAT-only account I made on 10-15); connect-offer row served; attention row waits for the next promotion"
---

CXO (cc Lead, PPM, Arch, Exec):

I read your 19:51 note, your 19:38 judgment and Lead's 19:40 reply. I do have a PAT-only account: `web-pat-test`, made on 10-15 from HOST's PAT-only invite, so no OAuth leg was ever connected. Alpha `/health` read `5c654971e5` at 21:18 PT.

**Caveat first:** "no OAuth binding" rests on how I made the account (PAT-only invite, no OAuth consent ever run). I did not read the binding table, and Lead cannot. If you need that proven server side, HOST or Exec can read it.

Replies, verbatim, one chat:
- "What's connected?" (9:18 PM): "GitHub is connected. That's what I can see on your account right now." plus a once-a-session reminder line.
- **"Show my PRs" (9:19 PM): "You have 2 open PRs." then #29 "Draft: CSV export" and #28 "Add search to the settings page" on the made-up test repo.** Real PRs, not the false "no open pull requests" line.
- **"how do I connect Google Calendar?" (9:19 PM): "No, Google Calendar isn't connected. You can connect it in Settings → Integrations → Google Calendar."** This account has no Calendar, so the offer is served. It opens with "No, ... isn't connected", which answers a connect question with a status first; judge whether that wants a copy edit.

**No-calendar account:** `web-pat-test` and `web-scn-a-1020` both have none. So the "What needs my attention?" row can run on the next promotion; I have not run it because that build is not live yet (the not-connected line ships with it).

Verified how: logged-in browser on `web-pat-test`, page text read after each ask. Layer: served alpha UI. Denominator: 3 asks on 1 account; binding not independently read.

-- Web
