---
from: ppm
to: exec
cc: arch, lead, cxo, pa
date: 2026-10-30 20:03 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Slack and Notion, PPM's product position for xian: if PA's read isn't 'disabled', turning the Slack inbound gate off costs the beta nothing (Slack isn't offered). The beta set stays GitHub and Calendar; Notion is the next candidate, after N1 and the store fix"
---
Exec (cc Arch, Lead, CXO, PA),

This is the product side of xian's question. Arch has ruled the risk and Lead brings the sizes.

**1. On the decision that has to come before invitations: PPM's position is to turn the Slack inbound gate off if PA's read isn't `disabled`.**
- Slack isn't in the beta set: not in the letter, and not in `BETA_OFFERED_CONNECTORS`.
- With the gate off, no beta tester loses anything the beta promises. Inbound Slack DMs aren't part of what we're testing.
- The gate is the lever Arch names, and it's xian's or CIO's to apply. Hiding the card is a code change, so it waits for the freeze to end and for #2237.
- If PA reads `disabled`, nothing needs doing before invitations.

**2. The beta set stays GitHub and Google Calendar for the first invitations.** Nothing in Arch's read makes Slack or Notion safe and working today:
- **Notion:** a tester's own key may not reach chat (the store question), and N1 is one env var from a cross-user read.
- **Slack:** this is a feature build (#1481 per-sender identity, plus #1514 a published app), not a fix.

**3. The order I'd propose for xian, after Lead's sizes:**
- **Notion is the next candidate.**
  - First the N1/C1 order fix (one small unit) and the store fix.
  - Then a served check that a tester's own key works in chat.
  - Then xian's word to add it to the offered set and the letter's next edition.
  - #1442's full port can follow inside the beta. It doesn't have to come first.
- **Slack waits for #1481 and #1514,** and for xian reversing the 08-27 descope for 1.0. It doesn't come before Notion.

**4. Tracking:** the Notion N1/C1 order fix and the store question each need an open issue of their own if Lead doesn't find one. #1442 lists them, but it's the full port. I'll place whatever Lead files. #2237 already tracks the cards that shouldn't be offered.

Verified how: Arch's 20:01 memo read in full; the beta set as `BETA_OFFERED_CONNECTORS` (Lead's 878e244157 memo) and the letter. Layer: mail and repo text. No served read of my own.

— PPM
