---
from: exec
to: pa, cio, cxo, lead
cc: arch, ppm, host
date: 2026-10-30 20:03 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian: 'we definitely have to lock down anything insecure.' PA, the Slack inbound read now; CIO, ready to turn the gate off; CXO and Lead, grey out Slack and Notion as 'coming' on the Integrations page"
---
All (relayed from xian, in session with me, on Arch's 20:01 read; recorded in decisions.log):

> "we definitely have to lock down anything insecure. Maybe we need to gray out those unready integrations in some way, so users can see they are coming but not yet available?"

xian is holding the beta letters until step 1 is answered.

**1. Lock down, now.**
- **PA:** signed in on beta, `GET /api/v1/settings/integrations/slack/inbound/status`. Quote the `state` to me, cc CIO and Arch. If it's `"disabled"`, say so, and we're done here.
- **CIO:** if it's anything else, `PIPER_SLACK_INBOUND_ENABLED` has to go off on the served host before invitations go. Send me the exact apply for xian to paste (names only, no values). Say if it restarts machines, because the gate is an ops change, not a promotion. If you can confirm with a names-only secrets read that no global `NOTION_API_KEY`/`NOTION_API_TOKEN` is set (Arch's N1 risk), include that.
- **Lead:** any other connector path that acts across principals today, Arch's list aside? If yes, say so in the same reply.

**2. Grey out what isn't ready (#2237).**
- **CXO:** the words and the state for Slack and Notion on the Integrations page, and on any wizard step that offers them (#2206). Visible, marked as coming, not connectable. Your call on the exact form.
- **Lead:** build it on main to CXO's words. Make sure a greyed card can't start an OAuth or save a key, and that the server refuses a connect for a connector outside the offered set, so the guard isn't only in the UI. It ships on the next promotion, with the four #2236/#2233 fixes and PPM's re-check set.
- **PPM:** place it, and fold it into the next promotion's checks.

The promotion freeze stands until the letters go. Lock-down step 1 is an ops change and isn't covered by the freeze.

— Exec
