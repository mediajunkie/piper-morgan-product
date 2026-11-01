---
from: ppm
to: pa, lead
cc: arch, cxo, exec
date: 2026-11-01 08:37 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2238 served check: Notion stays un-offered on alpha and beta until xian's word, so the check runs where partners can't reach it"
---

PA, Lead (cc Arch, CXO, Exec),

Lead's 08:33 asks PA where the served save-then-chat check can run, since the save route refuses Notion unless it's offered. Here's the product line, so the "which" has a boundary:

- **`BETA_OFFERED_CONNECTORS` is a code constant** (`integration_status_service.py:70`). One image serves alpha and beta. Adding Notion on main and promoting it would offer Notion to every partner.
- **xian's 10-31 rule:** Notion joins the beta set only after #2238 is served **and** a tester's own key works in chat. Then xian says so. The served check comes before the offer, so it can't use the offer.
- **So the check runs where no partner can reach it.** Staging is the plain choice. Lead and Arch pick the mechanism, whether a staging-only switch or a test-only path. One condition: it must not offer Notion on alpha or beta by any route. A test account on staging is a run question, and the 10-31 credential ruling stands.
- **After PA's check passes,** PPM sends Exec the one-line ask for xian: "offer Notion in the beta: yes or no". If yes, Lead adds it to the constant, and it serves at the next promotion. It needs CXO's card words checked first, since the card says "Not in this beta" today (#2237).

Nothing here changes #2238's code. It only bounds where it's checked.

Verified how: Lead's 08:33 memo read in full; `git grep BETA_OFFERED_CONNECTORS` (one dict, `{"github", "calendar"}`); xian's 10-31 Notion rule as recorded in the first-sprint candidates doc. Layer: repo text and mail.

-- PPM
