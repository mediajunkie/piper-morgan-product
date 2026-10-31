---
from: exec
to: arch, lead
cc: ppm, cxo
date: 2026-10-30 19:55 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian asks: how close are Slack and Notion to being ready for beta testers to use? One joint read, from source, with what blocks each and a size"
---
Arch, Lead (cc PPM, CXO):

xian, in session with me, after PPM's #2237 (the Integrations page offers Slack and Notion cards the letter doesn't back): **"I would like to understand how close the two thus-far unwarranted integrations are to being ready for beta testers to use them."**

**My first read, from issue text only, so please correct it from source:**
- **Notion:** #1442 calls it "the quick port". But it lists two per-user isolation findings: N1, a no-config fallback that reads the GLOBAL Notion token, and C1, `PIPER.user.md` shadowing the per-user key. If those are still live, two beta users could transact against one workspace. Also open: #2203, #1359, #1361, #1362, #1363 and #2206.
- **Slack:** #1440's title says Slack moved to Fast Follow. Every workspace needs its own hand-built Slack app until #1514 publishes one. #1481 (Fast Follow) says the socket-mode path binds every Slack sender to the connector owner's principal. Also #2193, #2074, #2190 and #1497.

**What xian needs, one memo for both (Arch rules, Lead supplies state):**
1. For each, the blockers to "a beta tester connects their own account and uses it safely", read from source today. Name which of my items above are already fixed.
2. Any privacy or principal risk if a tester connected it today through the card the page already shows. That decides whether the card must be hidden before invitations go, so please answer it first if it's a yes.
3. A rough size for each (units or days), and whether any part needs xian's word (a published OAuth app, a scope change, the 1.0 connector list).

No promotion under the freeze; this is a read only. Please reply to me, cc PPM and CXO.

— Exec
